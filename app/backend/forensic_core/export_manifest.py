"""Stage 3 export result and manifest contract structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
from typing import Mapping


EXPORT_MANIFEST_SCHEMA_VERSION = "stage3.export_manifest.v1"


@dataclass(frozen=True)
class ExportStatus:
    """Structured status for export contract/result states."""

    code: str
    message: str

    @property
    def ok(self) -> bool:
        return self.code == "ok"

    def to_dict(self) -> dict[str, object]:
        return {
            "code": self.code,
            "ok": self.ok,
            "message": self.message,
        }


@dataclass(frozen=True)
class ExportWarning:
    """Structured non-fatal export warning."""

    code: str
    message: str
    path: str | None = None
    source: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "code": self.code,
            "message": self.message,
            "path": self.path,
            "source": self.source,
        }


@dataclass(frozen=True)
class ExportSourceProvenance:
    """Source metadata copied from a Stage 2-style filesystem entry."""

    source_path: str | None
    volume_id: str | None
    volume_offset: int | None
    volume_length: int | None
    file_id: str | None
    file_path: str | None
    file_name: str | None
    entry_type: str | None
    filesystem_type: str | None
    adapter_name: str | None
    read_only: bool
    allocated: bool | None = None
    deleted: bool | None = None
    evidence_id: str | None = None
    case_id: str | None = None
    timestamps: Mapping[str, str | None] = field(default_factory=dict)

    @classmethod
    def from_file_entry(
        cls,
        file_entry: Mapping[str, object],
        *,
        evidence_id: str | None = None,
        case_id: str | None = None,
    ) -> "ExportSourceProvenance":
        """Build provenance from a Stage 2 filesystem-entry dictionary."""

        return cls(
            source_path=_optional_str(file_entry.get("source_path")),
            volume_id=_optional_str(file_entry.get("volume_id")),
            volume_offset=_optional_int(file_entry.get("volume_offset")),
            volume_length=_optional_int(file_entry.get("volume_length")),
            file_id=_optional_str(file_entry.get("file_id")),
            file_path=_optional_str(file_entry.get("path")),
            file_name=_optional_str(file_entry.get("name")),
            entry_type=_optional_str(file_entry.get("entry_type")),
            filesystem_type=_optional_str(file_entry.get("filesystem_type")),
            adapter_name=_optional_str(file_entry.get("adapter_name")),
            read_only=bool(file_entry.get("read_only", False)),
            allocated=_optional_bool(file_entry.get("allocated")),
            deleted=_optional_bool(file_entry.get("deleted")),
            evidence_id=evidence_id,
            case_id=case_id,
            timestamps=_string_mapping(file_entry.get("timestamps")),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "source_path": self.source_path,
            "volume_id": self.volume_id,
            "volume_offset": self.volume_offset,
            "volume_length": self.volume_length,
            "file_id": self.file_id,
            "file_path": self.file_path,
            "file_name": self.file_name,
            "entry_type": self.entry_type,
            "filesystem_type": self.filesystem_type,
            "adapter_name": self.adapter_name,
            "read_only": self.read_only,
            "allocated": self.allocated,
            "deleted": self.deleted,
            "evidence_id": self.evidence_id,
            "case_id": self.case_id,
            "timestamps": dict(self.timestamps),
        }


@dataclass(frozen=True)
class ExportContentSourceIdentity:
    """Identity for the explicit source that can later provide export bytes."""

    provider_name: str
    source_kind: str
    read_only: bool
    synthetic: bool
    source_content_size: int | None = None
    status: ExportStatus = field(
        default_factory=lambda: ExportStatus(
            code="export_not_started",
            message="Export content source has not been read.",
        )
    )
    parser_name: str | None = None
    parser_version: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "provider_name": self.provider_name,
            "source_kind": self.source_kind,
            "read_only": self.read_only,
            "synthetic": self.synthetic,
            "source_content_size": self.source_content_size,
            "status": self.status.to_dict(),
            "parser_name": self.parser_name,
            "parser_version": self.parser_version,
        }


@dataclass(frozen=True)
class ExportHashSummary:
    """Placeholder-ready hash fields for later export verification."""

    sha256: str | None = None
    status: ExportStatus = field(
        default_factory=lambda: ExportStatus(
            code="hash_not_computed",
            message="Export hashing is deferred beyond the manifest contract.",
        )
    )

    def to_dict(self) -> dict[str, object]:
        return {
            "sha256": self.sha256,
            "status": self.status.to_dict(),
        }


@dataclass(frozen=True)
class ExportRequest:
    """JSON-friendly request contract for a future export service."""

    source: ExportSourceProvenance
    destination_directory: str | None = None
    requested_output_path: str | None = None
    export_mode: str = "file"
    content_source: ExportContentSourceIdentity | None = None
    examiner_selected_destination: bool = False
    destination_status: ExportStatus = field(
        default_factory=lambda: ExportStatus(
            code="destination_not_checked",
            message="Destination safety has not been evaluated.",
        )
    )
    requested_at: str = field(default_factory=lambda: utc_now())
    warnings: tuple[ExportWarning, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": EXPORT_MANIFEST_SCHEMA_VERSION,
            "source": self.source.to_dict(),
            "destination_directory": self.destination_directory,
            "requested_output_path": self.requested_output_path,
            "export_mode": self.export_mode,
            "content_source": (
                self.content_source.to_dict() if self.content_source else None
            ),
            "examiner_selected_destination": self.examiner_selected_destination,
            "destination_status": self.destination_status.to_dict(),
            "requested_at": self.requested_at,
            "warnings": [warning.to_dict() for warning in self.warnings],
        }


@dataclass(frozen=True)
class ExportManifest:
    """Manifest contract for a future exported artifact."""

    source: ExportSourceProvenance
    content_source: ExportContentSourceIdentity
    status: ExportStatus
    destination_directory: str | None = None
    requested_output_path: str | None = None
    output_path: str | None = None
    manifest_path: str | None = None
    bytes_requested: int | None = None
    bytes_written: int | None = None
    hashes: ExportHashSummary = field(default_factory=ExportHashSummary)
    destination_status: ExportStatus = field(
        default_factory=lambda: ExportStatus(
            code="destination_not_checked",
            message="Destination safety has not been evaluated.",
        )
    )
    created_at: str = field(default_factory=lambda: utc_now())
    completed_at: str | None = None
    source_read_only: bool | None = None
    warnings: tuple[ExportWarning, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": EXPORT_MANIFEST_SCHEMA_VERSION,
            "status": self.status.to_dict(),
            "source": self.source.to_dict(),
            "content_source": self.content_source.to_dict(),
            "destination_directory": self.destination_directory,
            "requested_output_path": self.requested_output_path,
            "output_path": self.output_path,
            "manifest_path": self.manifest_path,
            "bytes_requested": self.bytes_requested,
            "bytes_written": self.bytes_written,
            "hashes": self.hashes.to_dict(),
            "destination_status": self.destination_status.to_dict(),
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "source_read_only": self._source_read_only(),
            "warnings": [warning.to_dict() for warning in self.warnings],
        }

    def _source_read_only(self) -> bool:
        return self.source.read_only if self.source_read_only is None else self.source_read_only


@dataclass(frozen=True)
class ExportResult:
    """Result contract for a future export operation."""

    status: ExportStatus
    source: ExportSourceProvenance
    content_source: ExportContentSourceIdentity
    destination_directory: str | None = None
    requested_output_path: str | None = None
    output_path: str | None = None
    manifest_path: str | None = None
    bytes_requested: int | None = None
    bytes_written: int | None = None
    hashes: ExportHashSummary = field(default_factory=ExportHashSummary)
    destination_status: ExportStatus = field(
        default_factory=lambda: ExportStatus(
            code="destination_not_checked",
            message="Destination safety has not been evaluated.",
        )
    )
    created_at: str = field(default_factory=lambda: utc_now())
    completed_at: str | None = None
    source_read_only: bool | None = None
    warnings: tuple[ExportWarning, ...] = field(default_factory=tuple)

    def to_manifest(self) -> ExportManifest:
        """Return a manifest-shaped view of this result without writing it."""

        return ExportManifest(
            status=self.status,
            source=self.source,
            content_source=self.content_source,
            destination_directory=self.destination_directory,
            requested_output_path=self.requested_output_path,
            output_path=self.output_path,
            manifest_path=self.manifest_path,
            bytes_requested=self.bytes_requested,
            bytes_written=self.bytes_written,
            hashes=self.hashes,
            destination_status=self.destination_status,
            created_at=self.created_at,
            completed_at=self.completed_at,
            source_read_only=self.source_read_only,
            warnings=self.warnings,
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": EXPORT_MANIFEST_SCHEMA_VERSION,
            "status": self.status.to_dict(),
            "source": self.source.to_dict(),
            "content_source": self.content_source.to_dict(),
            "destination_directory": self.destination_directory,
            "requested_output_path": self.requested_output_path,
            "output_path": self.output_path,
            "manifest_path": self.manifest_path,
            "bytes_requested": self.bytes_requested,
            "bytes_written": self.bytes_written,
            "hashes": self.hashes.to_dict(),
            "destination_status": self.destination_status.to_dict(),
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "source_read_only": self._source_read_only(),
            "manifest": self.to_manifest().to_dict(),
            "warnings": [warning.to_dict() for warning in self.warnings],
        }

    def _source_read_only(self) -> bool:
        return self.source.read_only if self.source_read_only is None else self.source_read_only


def export_result_to_json(result: ExportResult, *, indent: int | None = 2) -> str:
    """Serialize an export result contract as stable JSON."""

    return json.dumps(result.to_dict(), indent=indent, sort_keys=True)


def export_manifest_to_json(manifest: ExportManifest, *, indent: int | None = 2) -> str:
    """Serialize an export manifest contract as stable JSON."""

    return json.dumps(manifest.to_dict(), indent=indent, sort_keys=True)


def utc_now() -> str:
    """Return a UTC ISO timestamp using the project case-store convention."""

    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _optional_str(value: object) -> str | None:
    if value is None:
        return None
    return str(value)


def _optional_int(value: object) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _optional_bool(value: object) -> bool | None:
    if value is None:
        return None
    return bool(value)


def _string_mapping(value: object) -> dict[str, str | None]:
    if not isinstance(value, Mapping):
        return {}

    result: dict[str, str | None] = {}
    for key, item in value.items():
        result[str(key)] = None if item is None else str(item)
    return result
