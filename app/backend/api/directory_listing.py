"""Backend directory listing view for Stage 2."""

from __future__ import annotations

import json
from typing import Sequence

from app.backend.forensic_core import (
    FilesystemAdapter,
    FilesystemEntry,
    FilesystemResult,
    FilesystemWarning,
    Pytsk3FilesystemAdapter,
    VolumeInfo,
)


DIRECTORY_LISTING_SCHEMA_VERSION = "stage2.directory_listing.v1"


def list_directory(
    volume: VolumeInfo,
    directory_path: str = "/",
    adapter: FilesystemAdapter | None = None,
) -> dict[str, object]:
    """List file metadata for a directory through a filesystem adapter.

    S2-T05 supports root listing over adapter-provided entries. Nested
    directory traversal and file-content reads are intentionally deferred.
    """

    filesystem_adapter = adapter or Pytsk3FilesystemAdapter()
    normalized_path = _normalize_directory_path(directory_path)

    try:
        filesystem_result = filesystem_adapter.inspect_volume(volume)
    except Exception as error:  # pragma: no cover - defensive API boundary
        return _response(
            volume=volume,
            directory_path=normalized_path,
            adapter_name=filesystem_adapter.name,
            adapter_available=getattr(filesystem_adapter, "is_available", False),
            filesystem_type="unknown",
            read_only=bool(getattr(filesystem_adapter, "read_only", False) and volume.read_only),
            status_code="filesystem_error",
            status_message=f"Filesystem adapter raised an unexpected error: {error}",
            warnings=(
                {
                    "source": "directory_listing",
                    "code": "filesystem_error",
                    "message": "Filesystem adapter raised an unexpected error.",
                    "path": normalized_path,
                },
            ),
        )

    if not filesystem_result.status.ok:
        return _from_filesystem_result(
            filesystem_result,
            directory_path=normalized_path,
            status_code="filesystem_unavailable",
            status_message=f"Filesystem adapter did not provide entries: {filesystem_result.status.message}",
            entries=(),
        )

    if normalized_path == "/":
        return _from_filesystem_result(
            filesystem_result,
            directory_path=normalized_path,
            status_code="ok",
            status_message="Directory listing completed.",
            entries=filesystem_result.entries,
        )

    matching_entry = _find_entry(filesystem_result.entries, normalized_path)
    if matching_entry is None:
        return _from_filesystem_result(
            filesystem_result,
            directory_path=normalized_path,
            status_code="path_not_found",
            status_message="Directory path was not found in adapter root entries.",
            entries=(),
            extra_warnings=(
                {
                    "source": "directory_listing",
                    "code": "path_not_found",
                    "message": "Only root adapter entries are available in S2-T05.",
                    "path": normalized_path,
                },
            ),
        )

    if matching_entry.entry_type != "directory":
        return _from_filesystem_result(
            filesystem_result,
            directory_path=normalized_path,
            status_code="path_not_directory",
            status_message="Requested path is not a directory.",
            entries=(),
            extra_warnings=(
                {
                    "source": "directory_listing",
                    "code": "path_not_directory",
                    "message": "S2-T05 lists directories only and does not preview file content.",
                    "path": normalized_path,
                },
            ),
        )

    return _from_filesystem_result(
        filesystem_result,
        directory_path=normalized_path,
        status_code="path_unsupported",
        status_message="Nested directory listing is not implemented in S2-T05.",
        entries=(),
        extra_warnings=(
            {
                "source": "directory_listing",
                "code": "nested_listing_deferred",
                "message": "Only root directory listing is supported in S2-T05.",
                "path": normalized_path,
            },
        ),
    )


def directory_listing_to_json(
    volume: VolumeInfo,
    directory_path: str = "/",
    adapter: FilesystemAdapter | None = None,
    *,
    indent: int | None = 2,
) -> str:
    """Run directory listing and serialize the result as stable JSON."""

    return json.dumps(
        list_directory(volume, directory_path, adapter),
        indent=indent,
        sort_keys=True,
    )


def _from_filesystem_result(
    filesystem_result: FilesystemResult,
    *,
    directory_path: str,
    status_code: str,
    status_message: str,
    entries: Sequence[FilesystemEntry],
    extra_warnings: Sequence[dict[str, object]] = (),
) -> dict[str, object]:
    warnings = _filesystem_warnings(filesystem_result.warnings) + list(extra_warnings)
    return _response(
        volume_id=filesystem_result.volume_id,
        source_path=filesystem_result.source_path,
        volume_offset=filesystem_result.volume_offset,
        volume_length=filesystem_result.volume_length,
        directory_path=directory_path,
        adapter_name=filesystem_result.adapter_name,
        adapter_available=filesystem_result.adapter_available,
        filesystem_type=filesystem_result.filesystem_type,
        read_only=filesystem_result.read_only,
        status_code=status_code,
        status_message=status_message,
        entries=tuple(entry.to_dict() for entry in entries),
        warnings=warnings,
        adapter_dependency=filesystem_result.dependency.to_dict(),
        filesystem_status=filesystem_result.status.to_dict(),
    )


def _response(
    *,
    directory_path: str,
    adapter_name: str,
    adapter_available: bool,
    filesystem_type: str,
    read_only: bool,
    status_code: str,
    status_message: str,
    volume: VolumeInfo | None = None,
    volume_id: str | None = None,
    source_path: str | None = None,
    volume_offset: int | None = None,
    volume_length: int | None = None,
    entries: Sequence[dict[str, object]] = (),
    warnings: Sequence[dict[str, object]] = (),
    adapter_dependency: dict[str, object] | None = None,
    filesystem_status: dict[str, object] | None = None,
) -> dict[str, object]:
    return {
        "schema_version": DIRECTORY_LISTING_SCHEMA_VERSION,
        "status": {
            "code": status_code,
            "ok": status_code == "ok",
            "message": status_message,
        },
        "directory_path": directory_path,
        "source_path": source_path if source_path is not None else volume.source_path if volume else None,
        "volume_id": volume_id if volume_id is not None else volume.volume_id if volume else None,
        "volume_offset": volume_offset if volume_offset is not None else volume.offset if volume else None,
        "volume_length": volume_length if volume_length is not None else volume.length if volume else None,
        "filesystem_type": filesystem_type,
        "adapter": {
            "name": adapter_name,
            "available": adapter_available,
            "dependency": adapter_dependency or {},
        },
        "filesystem_status": filesystem_status or {},
        "read_only": read_only,
        "entry_count": len(entries),
        "entries": list(entries),
        "warnings": list(warnings),
    }


def _normalize_directory_path(path: str) -> str:
    value = (path or "/").strip()
    if not value:
        return "/"

    value = value.replace("\\", "/")
    if not value.startswith("/"):
        value = f"/{value}"

    while "//" in value:
        value = value.replace("//", "/")

    if len(value) > 1:
        value = value.rstrip("/")

    return value or "/"


def _find_entry(
    entries: Sequence[FilesystemEntry],
    path: str,
) -> FilesystemEntry | None:
    for entry in entries:
        if _normalize_directory_path(entry.path) == path:
            return entry
    return None


def _filesystem_warnings(
    warnings: Sequence[FilesystemWarning],
) -> list[dict[str, object]]:
    return [
        {"source": "filesystem_adapter", **warning.to_dict()}
        for warning in warnings
    ]
