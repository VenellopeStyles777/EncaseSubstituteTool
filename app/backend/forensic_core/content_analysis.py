"""Stage 4 hash and signature analysis contract structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
from typing import Mapping


CONTENT_ANALYSIS_SCHEMA_VERSION = "stage4.content_analysis.v1"


@dataclass(frozen=True)
class AnalysisStatus:
    """Structured status for content analysis contract states."""

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
class AnalysisWarning:
    """Structured non-fatal warning for content analysis contracts."""

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
class AnalysisSourceProvenance:
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
    ) -> "AnalysisSourceProvenance":
        """Build analysis provenance from metadata without treating it as bytes."""

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
            evidence_id=evidence_id or _optional_str(file_entry.get("evidence_id")),
            case_id=case_id or _optional_str(file_entry.get("case_id")),
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
class AnalysisContentSourceIdentity:
    """Identity for the explicit source that may provide analysis bytes later."""

    provider_name: str
    source_kind: str
    read_only: bool
    synthetic: bool = False
    generated: bool = False
    source_content_size: int | None = None
    status: AnalysisStatus = field(
        default_factory=lambda: AnalysisStatus(
            code="analysis_not_started",
            message="Analysis content source has not been read.",
        )
    )
    parser_name: str | None = None
    parser_version: str | None = None
    source_name: str | None = None
    source_version: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "provider_name": self.provider_name,
            "source_kind": self.source_kind,
            "read_only": self.read_only,
            "synthetic": self.synthetic,
            "generated": self.generated,
            "source_content_size": self.source_content_size,
            "status": self.status.to_dict(),
            "parser_name": self.parser_name,
            "parser_version": self.parser_version,
            "source_name": self.source_name,
            "source_version": self.source_version,
        }


@dataclass(frozen=True)
class HashDigestResult:
    """Placeholder-ready digest result for one requested hash algorithm."""

    algorithm: str
    digest: str | None = None
    status: AnalysisStatus = field(
        default_factory=lambda: AnalysisStatus(
            code="hash_not_computed",
            message="Hash digest has not been computed.",
        )
    )

    def to_dict(self) -> dict[str, object]:
        return {
            "algorithm": self.algorithm,
            "digest": self.digest,
            "status": self.status.to_dict(),
        }


@dataclass(frozen=True)
class HashAnalysisRequest:
    """JSON-friendly request contract for future provider-backed hashing."""

    source: AnalysisSourceProvenance
    requested_algorithms: tuple[str, ...] = ("sha256",)
    content_source: AnalysisContentSourceIdentity | None = None
    requested_at: str = field(default_factory=lambda: utc_now())
    warnings: tuple[AnalysisWarning, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": CONTENT_ANALYSIS_SCHEMA_VERSION,
            "analysis_type": "hash",
            "source": self.source.to_dict(),
            "content_source": (
                self.content_source.to_dict() if self.content_source else None
            ),
            "requested_algorithms": list(self.requested_algorithms),
            "requested_at": self.requested_at,
            "warnings": [warning.to_dict() for warning in self.warnings],
        }


@dataclass(frozen=True)
class HashAnalysisResult:
    """Result contract for future provider-backed hash analysis."""

    source: AnalysisSourceProvenance
    content_source: AnalysisContentSourceIdentity
    requested_algorithms: tuple[str, ...]
    digests: tuple[HashDigestResult, ...]
    status: AnalysisStatus = field(
        default_factory=lambda: AnalysisStatus(
            code="analysis_not_started",
            message="Hash analysis has not started.",
        )
    )
    bytes_analyzed: int | None = None
    created_at: str = field(default_factory=lambda: utc_now())
    completed_at: str | None = None
    warnings: tuple[AnalysisWarning, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": CONTENT_ANALYSIS_SCHEMA_VERSION,
            "analysis_type": "hash",
            "status": self.status.to_dict(),
            "source": self.source.to_dict(),
            "content_source": self.content_source.to_dict(),
            "requested_algorithms": list(self.requested_algorithms),
            "bytes_analyzed": self.bytes_analyzed,
            "digests": [digest.to_dict() for digest in self.digests],
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "warnings": [warning.to_dict() for warning in self.warnings],
        }


@dataclass(frozen=True)
class SignatureAnalysisRequest:
    """JSON-friendly request contract for future file signature analysis."""

    source: AnalysisSourceProvenance
    max_bytes_requested: int = 4096
    content_source: AnalysisContentSourceIdentity | None = None
    requested_at: str = field(default_factory=lambda: utc_now())
    warnings: tuple[AnalysisWarning, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": CONTENT_ANALYSIS_SCHEMA_VERSION,
            "analysis_type": "signature",
            "source": self.source.to_dict(),
            "content_source": (
                self.content_source.to_dict() if self.content_source else None
            ),
            "max_bytes_requested": self.max_bytes_requested,
            "requested_at": self.requested_at,
            "warnings": [warning.to_dict() for warning in self.warnings],
        }


@dataclass(frozen=True)
class SignatureAnalysisResult:
    """Result contract for future bounded file signature analysis."""

    source: AnalysisSourceProvenance
    content_source: AnalysisContentSourceIdentity
    max_bytes_requested: int
    status: AnalysisStatus = field(
        default_factory=lambda: AnalysisStatus(
            code="signature_not_checked",
            message="File signature analysis has not been run.",
        )
    )
    bytes_inspected: int | None = None
    detected_type: str | None = None
    detected_signature: str | None = None
    detected_mime_type: str | None = None
    created_at: str = field(default_factory=lambda: utc_now())
    completed_at: str | None = None
    warnings: tuple[AnalysisWarning, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": CONTENT_ANALYSIS_SCHEMA_VERSION,
            "analysis_type": "signature",
            "status": self.status.to_dict(),
            "source": self.source.to_dict(),
            "content_source": self.content_source.to_dict(),
            "max_bytes_requested": self.max_bytes_requested,
            "bytes_inspected": self.bytes_inspected,
            "detected_type": self.detected_type,
            "detected_signature": self.detected_signature,
            "detected_mime_type": self.detected_mime_type,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "warnings": [warning.to_dict() for warning in self.warnings],
        }


def hash_analysis_request_to_json(
    request: HashAnalysisRequest,
    *,
    indent: int | None = 2,
) -> str:
    """Serialize a hash analysis request contract as stable JSON."""

    return json.dumps(request.to_dict(), indent=indent, sort_keys=True)


def hash_analysis_result_to_json(
    result: HashAnalysisResult,
    *,
    indent: int | None = 2,
) -> str:
    """Serialize a hash analysis result contract as stable JSON."""

    return json.dumps(result.to_dict(), indent=indent, sort_keys=True)


def signature_analysis_request_to_json(
    request: SignatureAnalysisRequest,
    *,
    indent: int | None = 2,
) -> str:
    """Serialize a signature analysis request contract as stable JSON."""

    return json.dumps(request.to_dict(), indent=indent, sort_keys=True)


def signature_analysis_result_to_json(
    result: SignatureAnalysisResult,
    *,
    indent: int | None = 2,
) -> str:
    """Serialize a signature analysis result contract as stable JSON."""

    return json.dumps(result.to_dict(), indent=indent, sort_keys=True)


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
