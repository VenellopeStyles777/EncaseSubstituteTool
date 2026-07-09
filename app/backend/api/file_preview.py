"""Backend raw/text/hex preview foundation for Stage 2."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import Mapping, Protocol


FILE_PREVIEW_SCHEMA_VERSION = "stage2.file_preview.v1"
DEFAULT_PREVIEW_MAX_LENGTH = 64
SUPPORTED_PREVIEW_MODES = {"raw", "text", "hex"}


@dataclass(frozen=True)
class PreviewWarning:
    """Structured warning for preview generation."""

    code: str
    message: str
    path: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "code": self.code,
            "message": self.message,
            "path": self.path,
        }


@dataclass(frozen=True)
class PreviewContent:
    """Provider-owned content bytes plus provenance."""

    data: bytes
    provider_name: str
    source_path: str | None = None
    read_only: bool = True
    warnings: tuple[PreviewWarning, ...] = field(default_factory=tuple)


class PreviewContentProvider(Protocol):
    """Protocol for dependency-free preview content providers."""

    name: str
    read_only: bool

    def get_content(self, file_entry: Mapping[str, object]) -> PreviewContent | None:
        """Return preview bytes for an entry or None if unavailable."""


class StubPreviewProvider:
    """Deterministic preview provider for S2-T06 tests and smoke checks."""

    name = "stub-preview-provider"
    read_only = True

    def __init__(self, content_by_file_id: Mapping[str, bytes] | None = None) -> None:
        self._content_by_file_id = {
            "stub-file-hello": b"Hello, world!",
            **(content_by_file_id or {}),
        }

    def get_content(self, file_entry: Mapping[str, object]) -> PreviewContent | None:
        file_id = str(file_entry.get("file_id") or "")
        data = self._content_by_file_id.get(file_id)
        if data is None:
            return None

        return PreviewContent(
            data=data,
            provider_name=self.name,
            source_path=str(file_entry.get("source_path") or ""),
            read_only=self.read_only and bool(file_entry.get("read_only", False)),
            warnings=(
                PreviewWarning(
                    code="stub_preview_content",
                    message="Preview bytes are synthetic stub content, not parsed evidence bytes.",
                    path=str(file_entry.get("path") or ""),
                ),
            ),
        )


def preview_file(
    file_entry: Mapping[str, object],
    *,
    mode: str = "text",
    offset: int = 0,
    length: int | None = None,
    provider: PreviewContentProvider | None = None,
    max_length: int = DEFAULT_PREVIEW_MAX_LENGTH,
    encoding: str = "utf-8",
) -> dict[str, object]:
    """Preview known stub/fixture content for a file entry.

    This function does not perform real filesystem byte extraction. It only
    consumes bytes exposed by an explicit preview provider.
    """

    preview_provider = provider or StubPreviewProvider()
    normalized_mode = (mode or "").lower()

    if normalized_mode not in SUPPORTED_PREVIEW_MODES:
        return _response(
            file_entry=file_entry,
            mode=normalized_mode,
            offset=offset,
            requested_length=length,
            provider_name=preview_provider.name,
            provider_read_only=preview_provider.read_only,
            status_code="unsupported_preview_mode",
            status_message="Preview mode must be one of raw, text, or hex.",
            warnings=(
                PreviewWarning(
                    code="unsupported_preview_mode",
                    message="Unsupported preview mode requested.",
                    path=_entry_path(file_entry),
                ),
            ),
        )

    range_status = _validate_range(offset, length, max_length, file_entry)
    if range_status is not None:
        return _response(
            file_entry=file_entry,
            mode=normalized_mode,
            offset=offset,
            requested_length=length,
            provider_name=preview_provider.name,
            provider_read_only=preview_provider.read_only,
            status_code="invalid_range",
            status_message=range_status.message,
            warnings=(range_status,),
        )

    if str(file_entry.get("entry_type") or "") != "file":
        return _response(
            file_entry=file_entry,
            mode=normalized_mode,
            offset=offset,
            requested_length=length,
            provider_name=preview_provider.name,
            provider_read_only=preview_provider.read_only,
            status_code="path_not_file",
            status_message="Preview requires a file entry.",
            warnings=(
                PreviewWarning(
                    code="path_not_file",
                    message="Directory or non-file entries cannot be previewed.",
                    path=_entry_path(file_entry),
                ),
            ),
        )

    content = preview_provider.get_content(file_entry)
    if content is None:
        return _response(
            file_entry=file_entry,
            mode=normalized_mode,
            offset=offset,
            requested_length=length,
            provider_name=preview_provider.name,
            provider_read_only=preview_provider.read_only,
            status_code="file_not_found",
            status_message="Preview provider has no content for this file entry.",
            source_content_size=None,
            warnings=(
                PreviewWarning(
                    code="file_not_found",
                    message="No preview content is registered for this file entry.",
                    path=_entry_path(file_entry),
                ),
            ),
        )

    source_size = len(content.data)
    if offset > source_size:
        warnings = list(content.warnings)
        warnings.append(
            PreviewWarning(
                code="content_unavailable",
                message="Preview offset is beyond available content.",
                path=_entry_path(file_entry),
            )
        )
        return _response(
            file_entry=file_entry,
            mode=normalized_mode,
            offset=offset,
            requested_length=length,
            provider_name=content.provider_name,
            provider_read_only=content.read_only,
            status_code="content_unavailable",
            status_message="Preview offset is beyond available content.",
            source_content_size=source_size,
            returned_bytes=0,
            truncated=False,
            preview_data=None,
            warnings=tuple(warnings),
            encoding=encoding if normalized_mode == "text" else None,
        )

    requested_length = source_size - offset if length is None else length
    capped_length = min(requested_length, max_length)
    end_offset = min(offset + capped_length, source_size)
    preview_bytes = content.data[offset:end_offset] if offset <= source_size else b""
    truncated = requested_length > len(preview_bytes)

    warnings = list(content.warnings)
    status_code = "ok"
    status_message = "Preview completed."
    if truncated:
        status_code = "preview_truncated"
        status_message = "Preview returned bounded content and was truncated."
        warnings.append(
            PreviewWarning(
                code="preview_truncated",
                message="Requested preview exceeds configured limit or available content.",
                path=_entry_path(file_entry),
            )
        )

    preview_data, render_warnings = _render_preview(
        preview_bytes,
        mode=normalized_mode,
        encoding=encoding,
        path=_entry_path(file_entry),
    )
    warnings.extend(render_warnings)

    return _response(
        file_entry=file_entry,
        mode=normalized_mode,
        offset=offset,
        requested_length=length,
        provider_name=content.provider_name,
        provider_read_only=content.read_only,
        status_code=status_code,
        status_message=status_message,
        source_content_size=source_size,
        returned_bytes=len(preview_bytes),
        truncated=truncated,
        preview_data=preview_data,
        warnings=tuple(warnings),
        encoding=encoding if normalized_mode == "text" else None,
    )


def preview_file_to_json(
    file_entry: Mapping[str, object],
    *,
    mode: str = "text",
    offset: int = 0,
    length: int | None = None,
    provider: PreviewContentProvider | None = None,
    max_length: int = DEFAULT_PREVIEW_MAX_LENGTH,
    encoding: str = "utf-8",
    indent: int | None = 2,
) -> str:
    """Run preview and serialize the result as stable JSON."""

    return json.dumps(
        preview_file(
            file_entry,
            mode=mode,
            offset=offset,
            length=length,
            provider=provider,
            max_length=max_length,
            encoding=encoding,
        ),
        indent=indent,
        sort_keys=True,
    )


def _validate_range(
    offset: int,
    length: int | None,
    max_length: int,
    file_entry: Mapping[str, object],
) -> PreviewWarning | None:
    if offset < 0:
        return PreviewWarning(
            code="invalid_range",
            message="Preview offset must be greater than or equal to zero.",
            path=_entry_path(file_entry),
        )
    if length is not None and length < 0:
        return PreviewWarning(
            code="invalid_range",
            message="Preview length must be greater than or equal to zero.",
            path=_entry_path(file_entry),
        )
    if max_length < 0:
        return PreviewWarning(
            code="invalid_range",
            message="Preview maximum length must be greater than or equal to zero.",
            path=_entry_path(file_entry),
        )
    return None


def _render_preview(
    data: bytes,
    *,
    mode: str,
    encoding: str,
    path: str | None,
) -> tuple[object, tuple[PreviewWarning, ...]]:
    if mode == "raw":
        return {"byte_values": list(data)}, ()
    if mode == "hex":
        return {"hex": data.hex()}, ()

    text = data.decode(encoding, errors="replace")
    warnings: tuple[PreviewWarning, ...] = ()
    if "\ufffd" in text:
        warnings = (
            PreviewWarning(
                code="text_decode_replacement",
                message="Text preview used replacement characters for undecodable bytes.",
                path=path,
            ),
        )
    return {"text": text, "encoding": encoding}, warnings


def _response(
    *,
    file_entry: Mapping[str, object],
    mode: str,
    offset: int,
    requested_length: int | None,
    provider_name: str,
    provider_read_only: bool,
    status_code: str,
    status_message: str,
    source_content_size: int | None = None,
    returned_bytes: int = 0,
    truncated: bool = False,
    preview_data: object | None = None,
    warnings: tuple[PreviewWarning, ...] = (),
    encoding: str | None = None,
) -> dict[str, object]:
    read_only = bool(provider_read_only and file_entry.get("read_only", False))
    return {
        "schema_version": FILE_PREVIEW_SCHEMA_VERSION,
        "status": {
            "code": status_code,
            "ok": status_code == "ok",
            "message": status_message,
        },
        "mode": mode,
        "source_path": file_entry.get("source_path"),
        "volume_id": file_entry.get("volume_id"),
        "volume_offset": file_entry.get("volume_offset"),
        "volume_length": file_entry.get("volume_length"),
        "file_id": file_entry.get("file_id"),
        "file_path": file_entry.get("path"),
        "file_name": file_entry.get("name"),
        "entry_type": file_entry.get("entry_type"),
        "requested_offset": offset,
        "requested_length": requested_length,
        "returned_bytes": returned_bytes,
        "source_content_size": source_content_size,
        "truncated": truncated,
        "read_only": read_only,
        "provider": {
            "name": provider_name,
            "read_only": provider_read_only,
        },
        "encoding": encoding,
        "preview": preview_data,
        "warnings": [warning.to_dict() for warning in warnings],
    }


def _entry_path(file_entry: Mapping[str, object]) -> str | None:
    value = file_entry.get("path")
    return str(value) if value is not None else None
