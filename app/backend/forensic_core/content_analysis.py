"""Stage 4 hash and signature analysis contract structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
import math
from typing import Iterable, Mapping, Protocol


CONTENT_ANALYSIS_SCHEMA_VERSION = "stage4.content_analysis.v1"
DEFAULT_HASH_ALGORITHMS = ("sha256",)
DEFAULT_SIGNATURE_MAX_BYTES = 4096
SUPPORTED_HASH_ALGORITHMS = ("sha256", "md5", "sha1")
SUPPORTED_KNOWN_FILE_CATEGORIES = ("known_good", "known_bad", "known_unknown")
_OK_STATUS_CODES = (
    "ok",
    "known_file_match",
    "known_file_no_match",
    "extension_match",
    "extension_mismatch",
)
_HASH_FACTORIES = {
    "sha256": hashlib.sha256,
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
}
_KNOWN_FILE_ALGORITHM_PREFERENCE = SUPPORTED_HASH_ALGORITHMS


@dataclass(frozen=True)
class AnalysisStatus:
    """Structured status for content analysis contract states."""

    code: str
    message: str

    @property
    def ok(self) -> bool:
        return self.code in _OK_STATUS_CODES

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
class AnalysisContent:
    """Provider-owned raw bytes for Stage 4 analysis."""

    data: bytes
    provider_name: str
    source_kind: str
    read_only: bool = True
    synthetic: bool = False
    generated: bool = False
    parser_name: str | None = None
    parser_version: str | None = None
    source_name: str | None = None
    source_version: str | None = None
    warnings: tuple[AnalysisWarning, ...] = field(default_factory=tuple)

    def to_content_source_identity(
        self,
        *,
        status: AnalysisStatus | None = None,
    ) -> AnalysisContentSourceIdentity:
        """Describe these bytes without exposing the bytes in result JSON."""

        return AnalysisContentSourceIdentity(
            provider_name=self.provider_name,
            source_kind=self.source_kind,
            read_only=self.read_only,
            synthetic=self.synthetic,
            generated=self.generated,
            source_content_size=len(self.data),
            status=status
            or AnalysisStatus(
                code="ok",
                message="Analysis content provider returned raw bytes.",
            ),
            parser_name=self.parser_name,
            parser_version=self.parser_version,
            source_name=self.source_name,
            source_version=self.source_version,
        )


class AnalysisContentProvider(Protocol):
    """Protocol for explicit Stage 4 analysis byte providers."""

    name: str
    source_kind: str
    read_only: bool
    synthetic: bool
    generated: bool

    def get_content(
        self,
        source: AnalysisSourceProvenance,
    ) -> AnalysisContent | None:
        """Return raw analysis bytes for a source or None if unavailable."""


class StubAnalysisContentProvider:
    """Deterministic Stage 4 analysis provider for dependency-free tests."""

    def __init__(
        self,
        content_by_file_id: Mapping[str, bytes] | None = None,
        *,
        name: str = "stub-analysis-provider",
        source_kind: str = "synthetic",
        read_only: bool = True,
        synthetic: bool | None = None,
        generated: bool | None = None,
        source_name: str | None = None,
        source_version: str | None = None,
        parser_version: str | None = None,
    ) -> None:
        self.name = name
        self.source_kind = source_kind
        self.read_only = read_only
        self.synthetic = source_kind == "synthetic" if synthetic is None else synthetic
        self.generated = (
            source_kind == "generated_fixture" if generated is None else generated
        )
        self.source_name = source_name
        self.source_version = source_version
        self.parser_version = parser_version
        self._content_by_file_id = {
            "stub-file-hello": b"Hello, world!",
            **(content_by_file_id or {}),
        }

    def get_content(
        self,
        source: AnalysisSourceProvenance,
    ) -> AnalysisContent | None:
        file_id = source.file_id or ""
        data = self._content_by_file_id.get(file_id)
        if data is None:
            return None

        warnings = []
        if self.synthetic:
            warnings.append(
                AnalysisWarning(
                    code="synthetic_content",
                    message=(
                        "Analysis bytes are synthetic provider content, "
                        "not parsed evidence bytes."
                    ),
                    path=source.file_path,
                    source="analysis_content_provider",
                )
            )
        if self.generated:
            warnings.append(
                AnalysisWarning(
                    code="generated_fixture_content",
                    message=(
                        "Analysis bytes are generated fixture content, "
                        "not parsed evidence bytes."
                    ),
                    path=source.file_path,
                    source="analysis_content_provider",
                )
            )

        return AnalysisContent(
            data=data,
            provider_name=self.name,
            source_kind=self.source_kind,
            read_only=self.read_only and source.read_only,
            synthetic=self.synthetic,
            generated=self.generated,
            parser_name=source.adapter_name,
            parser_version=self.parser_version,
            source_name=self.source_name,
            source_version=self.source_version,
            warnings=tuple(warnings),
        )


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
class KnownFileRecord:
    """Caller-supplied fixture-sized known-file hash record."""

    algorithm: str
    digest: str
    category: str
    dataset_name: str | None = None
    dataset_version: str | None = None
    record_id: str | None = None
    file_name: str | None = None
    metadata: Mapping[str, object] = field(default_factory=dict)
    original_algorithm: str | None = None
    original_digest: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "algorithm": self.algorithm,
            "digest": self.digest,
            "category": self.category,
            "dataset_name": self.dataset_name,
            "dataset_version": self.dataset_version,
            "record_id": self.record_id,
            "file_name": self.file_name,
            "metadata": _json_safe_mapping(self.metadata),
            "original_algorithm": self.original_algorithm,
            "original_digest": self.original_digest,
        }


@dataclass(frozen=True)
class KnownFileMatchResult:
    """Result for matching reviewed hashes against caller records."""

    source: AnalysisSourceProvenance
    content_source: AnalysisContentSourceIdentity
    hash_status: AnalysisStatus
    requested_algorithms: tuple[str, ...]
    digests: tuple[HashDigestResult, ...]
    status: AnalysisStatus = field(
        default_factory=lambda: AnalysisStatus(
            code="known_file_not_checked",
            message="Known-file matching has not been run.",
        )
    )
    matched: bool | None = None
    match_category: str | None = None
    matched_algorithm: str | None = None
    matched_digest: str | None = None
    matched_records: tuple[KnownFileRecord, ...] = field(default_factory=tuple)
    bytes_analyzed: int | None = None
    hash_created_at: str | None = None
    hash_completed_at: str | None = None
    created_at: str = field(default_factory=lambda: utc_now())
    completed_at: str | None = None
    warnings: tuple[AnalysisWarning, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": CONTENT_ANALYSIS_SCHEMA_VERSION,
            "analysis_type": "known_file_match",
            "status": self.status.to_dict(),
            "source": self.source.to_dict(),
            "content_source": self.content_source.to_dict(),
            "hash_status": self.hash_status.to_dict(),
            "requested_algorithms": list(self.requested_algorithms),
            "bytes_analyzed": self.bytes_analyzed,
            "digests": [digest.to_dict() for digest in self.digests],
            "matched": self.matched,
            "match_category": self.match_category,
            "matched_algorithm": self.matched_algorithm,
            "matched_digest": self.matched_digest,
            "matched_records": [record.to_dict() for record in self.matched_records],
            "hash_created_at": self.hash_created_at,
            "hash_completed_at": self.hash_completed_at,
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


@dataclass(frozen=True)
class SignatureExtensionRule:
    """Conservative extension allow-list for one detected signature type."""

    detected_type: str
    expected_extensions: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "detected_type": self.detected_type,
            "expected_extensions": list(self.expected_extensions),
        }


@dataclass(frozen=True)
class ExtensionMismatchResult:
    """Result contract for extension/signature mismatch evaluation."""

    source: AnalysisSourceProvenance
    content_source: AnalysisContentSourceIdentity
    signature_status: AnalysisStatus
    status: AnalysisStatus = field(
        default_factory=lambda: AnalysisStatus(
            code="extension_not_checked",
            message="Extension mismatch evaluation has not been run.",
        )
    )
    detected_type: str | None = None
    detected_signature: str | None = None
    detected_mime_type: str | None = None
    observed_extension: str | None = None
    expected_extensions: tuple[str, ...] = field(default_factory=tuple)
    mismatch: bool | None = None
    signature_created_at: str | None = None
    signature_completed_at: str | None = None
    created_at: str = field(default_factory=lambda: utc_now())
    completed_at: str | None = None
    warnings: tuple[AnalysisWarning, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": CONTENT_ANALYSIS_SCHEMA_VERSION,
            "analysis_type": "extension_mismatch",
            "status": self.status.to_dict(),
            "source": self.source.to_dict(),
            "content_source": self.content_source.to_dict(),
            "signature_status": self.signature_status.to_dict(),
            "detected_type": self.detected_type,
            "detected_signature": self.detected_signature,
            "detected_mime_type": self.detected_mime_type,
            "observed_extension": self.observed_extension,
            "expected_extensions": list(self.expected_extensions),
            "mismatch": self.mismatch,
            "signature_created_at": self.signature_created_at,
            "signature_completed_at": self.signature_completed_at,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "warnings": [warning.to_dict() for warning in self.warnings],
        }


@dataclass(frozen=True)
class FileSignatureDefinition:
    """Conservative magic-byte definition for bounded signature detection."""

    detected_type: str
    detected_signature: str
    magic: bytes
    mime_type: str | None = None


SUPPORTED_FILE_SIGNATURES = (
    FileSignatureDefinition(
        detected_type="png",
        detected_signature="png_header",
        magic=b"\x89PNG\r\n\x1a\n",
        mime_type="image/png",
    ),
    FileSignatureDefinition(
        detected_type="gif",
        detected_signature="gif87a_header",
        magic=b"GIF87a",
        mime_type="image/gif",
    ),
    FileSignatureDefinition(
        detected_type="gif",
        detected_signature="gif89a_header",
        magic=b"GIF89a",
        mime_type="image/gif",
    ),
    FileSignatureDefinition(
        detected_type="pdf",
        detected_signature="pdf_header",
        magic=b"%PDF-",
        mime_type="application/pdf",
    ),
    FileSignatureDefinition(
        detected_type="zip",
        detected_signature="zip_local_file_header",
        magic=b"PK\x03\x04",
        mime_type="application/zip",
    ),
    FileSignatureDefinition(
        detected_type="zip",
        detected_signature="zip_empty_archive",
        magic=b"PK\x05\x06",
        mime_type="application/zip",
    ),
    FileSignatureDefinition(
        detected_type="zip",
        detected_signature="zip_spanned_archive_marker",
        magic=b"PK\x07\x08",
        mime_type="application/zip",
    ),
    FileSignatureDefinition(
        detected_type="elf",
        detected_signature="elf_header",
        magic=b"\x7fELF",
        mime_type="application/x-elf",
    ),
    FileSignatureDefinition(
        detected_type="jpeg",
        detected_signature="jpeg_soi",
        magic=b"\xff\xd8\xff",
        mime_type="image/jpeg",
    ),
    FileSignatureDefinition(
        detected_type="mz_executable_candidate",
        detected_signature="mz_header_candidate",
        magic=b"MZ",
        mime_type="application/x-msdownload",
    ),
)


SIGNATURE_EXTENSION_RULES = (
    SignatureExtensionRule(detected_type="pdf", expected_extensions=(".pdf",)),
    SignatureExtensionRule(detected_type="png", expected_extensions=(".png",)),
    SignatureExtensionRule(
        detected_type="jpeg",
        expected_extensions=(".jpg", ".jpeg", ".jpe"),
    ),
    SignatureExtensionRule(detected_type="gif", expected_extensions=(".gif",)),
    SignatureExtensionRule(
        detected_type="zip",
        expected_extensions=(
            ".zip",
            ".jar",
            ".docx",
            ".xlsx",
            ".pptx",
            ".odt",
            ".ods",
            ".odp",
            ".apk",
        ),
    ),
    SignatureExtensionRule(
        detected_type="elf",
        expected_extensions=(".elf", ".so", ".bin", ".run"),
    ),
    SignatureExtensionRule(
        detected_type="mz_executable_candidate",
        expected_extensions=(
            ".exe",
            ".dll",
            ".sys",
            ".scr",
            ".com",
            ".ocx",
            ".cpl",
            ".drv",
        ),
    ),
)

SUPPORTED_SIGNATURE_EXTENSIONS = {
    rule.detected_type: rule.expected_extensions
    for rule in SIGNATURE_EXTENSION_RULES
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


def known_file_match_result_to_json(
    result: KnownFileMatchResult,
    *,
    indent: int | None = 2,
) -> str:
    """Serialize a known-file match result contract as stable JSON."""

    return json.dumps(result.to_dict(), indent=indent, sort_keys=True)


def match_known_file_hashes(
    hash_result: HashAnalysisResult,
    known_files: Iterable[KnownFileRecord | Mapping[str, object]],
) -> KnownFileMatchResult:
    """Match reviewed digest results against caller-supplied records."""

    if hash_result.status.code != "ok":
        status = AnalysisStatus(
            code="hash_not_available",
            message=(
                "Known-file matching was not evaluated because hash analysis "
                "did not complete successfully."
            ),
        )
        return _known_file_match_result(
            hash_result=hash_result,
            status=status,
            warnings=hash_result.warnings
            + (
                AnalysisWarning(
                    code="hash_not_available",
                    message=f"Hash result status was {hash_result.status.code}.",
                    path=hash_result.source.file_path,
                    source="content_analysis",
                ),
            ),
        )

    computed_digests = _computed_hash_digests(hash_result)
    if not computed_digests:
        status = AnalysisStatus(
            code="hash_digest_unavailable",
            message="Known-file matching requires at least one computed digest.",
        )
        return _known_file_match_result(
            hash_result=hash_result,
            status=status,
            warnings=hash_result.warnings
            + (
                AnalysisWarning(
                    code="hash_digest_unavailable",
                    message="Hash result did not include an ok digest value.",
                    path=hash_result.source.file_path,
                    source="content_analysis",
                ),
            ),
        )

    records, record_warnings = _known_file_records_from_input(
        known_files,
        hash_result.source,
    )
    if record_warnings:
        status = AnalysisStatus(
            code="invalid_known_file_record",
            message="One or more known-file records are invalid.",
        )
        return _known_file_match_result(
            hash_result=hash_result,
            status=status,
            warnings=hash_result.warnings + record_warnings,
        )

    matched_records_by_key: dict[tuple[str, str], list[KnownFileRecord]] = {}
    matched_records: list[KnownFileRecord] = []
    for record in records:
        digest = computed_digests.get(record.algorithm)
        if digest != record.digest:
            continue
        matched_records.append(record)
        matched_records_by_key.setdefault((record.algorithm, digest), []).append(record)

    if not matched_records:
        status = AnalysisStatus(
            code="known_file_no_match",
            message="No caller-supplied known-file records matched computed digests.",
        )
        return _known_file_match_result(
            hash_result=hash_result,
            status=status,
            matched=False,
            warnings=hash_result.warnings,
        )

    primary_key = _primary_known_file_match_key(
        matched_records_by_key,
        computed_digests,
    )
    conflict_key = _conflicting_known_file_match_key(
        matched_records_by_key,
        computed_digests,
    )
    if conflict_key is not None:
        status = AnalysisStatus(
            code="conflicting_known_file_records",
            message=(
                "Matched known-file records for the same digest use conflicting "
                "categories."
            ),
        )
        return _known_file_match_result(
            hash_result=hash_result,
            status=status,
            matched=None,
            matched_algorithm=conflict_key[0],
            matched_digest=conflict_key[1],
            matched_records=tuple(matched_records),
            warnings=hash_result.warnings
            + _hash_match_context_warnings(hash_result)
            + (
                AnalysisWarning(
                    code="conflicting_known_file_records",
                    message=(
                        "Caller-supplied records for the same computed digest "
                        "contained more than one category."
                    ),
                    path=hash_result.source.file_path,
                    source="known_file_records",
                ),
            ),
        )

    primary_records = tuple(matched_records_by_key[primary_key])
    status = AnalysisStatus(
        code="known_file_match",
        message="Computed digest matched caller-supplied known-file records.",
    )
    return _known_file_match_result(
        hash_result=hash_result,
        status=status,
        matched=True,
        match_category=primary_records[0].category,
        matched_algorithm=primary_key[0],
        matched_digest=primary_key[1],
        matched_records=tuple(matched_records),
        warnings=hash_result.warnings + _hash_match_context_warnings(hash_result),
    )


def match_known_files(
    hash_result: HashAnalysisResult,
    known_files: Iterable[KnownFileRecord | Mapping[str, object]],
) -> KnownFileMatchResult:
    """Alias for known-file hash matching."""

    return match_known_file_hashes(hash_result, known_files)


def hash_file_content(
    file_entry_or_request: (
        Mapping[str, object] | AnalysisSourceProvenance | HashAnalysisRequest
    ),
    *,
    provider: AnalysisContentProvider | None = None,
    algorithms: Iterable[object] | str | None = None,
    evidence_id: str | None = None,
    case_id: str | None = None,
) -> HashAnalysisResult:
    """Compute hashes from explicit Stage 4 analysis provider bytes.

    Filesystem entries remain metadata-only. This function only analyzes bytes
    returned by an `AnalysisContentProvider`, and it validates requested
    algorithms before calling the provider.
    """

    source = _source_from_hash_input(
        file_entry_or_request,
        evidence_id=evidence_id,
        case_id=case_id,
    )
    requested_values = _requested_hash_algorithms(file_entry_or_request, algorithms)
    normalized_algorithms, validation_status, validation_warning = (
        _normalize_hash_algorithms(requested_values, source)
    )
    content_source = _initial_content_source_identity(
        provider,
        source,
        _request_content_source(file_entry_or_request),
    )

    if validation_status is not None:
        return _hash_result(
            source=source,
            content_source=content_source,
            requested_algorithms=normalized_algorithms,
            status=validation_status,
            digests=_validation_digest_placeholders(
                normalized_algorithms,
                validation_status=validation_status,
            ),
            warnings=(validation_warning,),
        )

    if source.entry_type != "file":
        status = AnalysisStatus(
            code="path_not_file",
            message="Hash analysis requires a file entry.",
        )
        return _hash_result(
            source=source,
            content_source=content_source,
            requested_algorithms=normalized_algorithms,
            status=status,
            digests=_digest_placeholders(normalized_algorithms),
            warnings=(
                AnalysisWarning(
                    code="path_not_file",
                    message="Directory or non-file entries cannot be hashed.",
                    path=source.file_path,
                    source="content_analysis",
                ),
            ),
        )

    if provider is None:
        status = AnalysisStatus(
            code="metadata_only_source",
            message="Filesystem metadata alone is not analysis content.",
        )
        return _hash_result(
            source=source,
            content_source=_content_source_with_status(
                content_source,
                status=status,
                source_content_size=None,
            ),
            requested_algorithms=normalized_algorithms,
            status=status,
            digests=_digest_placeholders(normalized_algorithms),
            warnings=(
                AnalysisWarning(
                    code="metadata_only_source",
                    message=(
                        "No explicit Stage 4 analysis content provider was supplied."
                    ),
                    path=source.file_path,
                    source="content_analysis",
                ),
            ),
        )

    try:
        content = provider.get_content(source)
    except Exception as error:
        status = AnalysisStatus(
            code="content_provider_error",
            message=(
                "Analysis content provider failed before hashes could be computed: "
                f"{type(error).__name__}."
            ),
        )
        return _hash_result(
            source=source,
            content_source=_content_source_with_status(
                content_source,
                status=status,
                source_content_size=None,
            ),
            requested_algorithms=normalized_algorithms,
            status=status,
            digests=_digest_placeholders(normalized_algorithms),
            warnings=(
                AnalysisWarning(
                    code="content_provider_error",
                    message="Analysis content provider raised an exception.",
                    path=source.file_path,
                    source="analysis_content_provider",
                ),
            ),
        )

    if content is None:
        status = AnalysisStatus(
            code="content_source_unavailable",
            message="Analysis content provider has no raw bytes for this file entry.",
        )
        return _hash_result(
            source=source,
            content_source=_content_source_with_status(
                content_source,
                status=status,
                source_content_size=None,
            ),
            requested_algorithms=normalized_algorithms,
            status=status,
            digests=_digest_placeholders(normalized_algorithms),
            warnings=(
                AnalysisWarning(
                    code="content_source_unavailable",
                    message="No raw analysis content is registered for this file entry.",
                    path=source.file_path,
                    source="analysis_content_provider",
                ),
            ),
        )

    digests = []
    for algorithm in normalized_algorithms:
        hash_object = _HASH_FACTORIES[algorithm]()
        hash_object.update(content.data)
        digests.append(
            HashDigestResult(
                algorithm=algorithm,
                digest=hash_object.hexdigest(),
                status=AnalysisStatus(
                    code="ok",
                    message=(
                        f"{algorithm} digest computed from explicit analysis "
                        "provider bytes."
                    ),
                ),
            )
        )

    status = AnalysisStatus(
        code="ok",
        message="Hash analysis completed from explicit provider bytes.",
    )
    return _hash_result(
        source=source,
        content_source=content.to_content_source_identity(),
        requested_algorithms=normalized_algorithms,
        status=status,
        digests=tuple(digests),
        bytes_analyzed=len(content.data),
        warnings=content.warnings,
    )


def calculate_hashes(
    file_entry_or_request: (
        Mapping[str, object] | AnalysisSourceProvenance | HashAnalysisRequest
    ),
    *,
    provider: AnalysisContentProvider | None = None,
    algorithms: Iterable[object] | str | None = None,
    evidence_id: str | None = None,
    case_id: str | None = None,
) -> HashAnalysisResult:
    """Alias for provider-backed hash calculation."""

    return hash_file_content(
        file_entry_or_request,
        provider=provider,
        algorithms=algorithms,
        evidence_id=evidence_id,
        case_id=case_id,
    )


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


def extension_mismatch_result_to_json(
    result: ExtensionMismatchResult,
    *,
    indent: int | None = 2,
) -> str:
    """Serialize an extension mismatch result contract as stable JSON."""

    return json.dumps(result.to_dict(), indent=indent, sort_keys=True)


def detect_file_signature(
    file_entry_or_request: (
        Mapping[str, object] | AnalysisSourceProvenance | SignatureAnalysisRequest
    ),
    *,
    provider: AnalysisContentProvider | None = None,
    max_bytes: object | None = None,
    evidence_id: str | None = None,
    case_id: str | None = None,
) -> SignatureAnalysisResult:
    """Detect file signatures from a bounded provider-backed byte prefix."""

    source = _source_from_signature_input(
        file_entry_or_request,
        evidence_id=evidence_id,
        case_id=case_id,
    )
    requested_max_bytes = _requested_signature_max_bytes(
        file_entry_or_request,
        max_bytes,
    )
    normalized_max_bytes, validation_status, validation_warning = (
        _normalize_signature_max_bytes(requested_max_bytes, source)
    )
    content_source = _initial_content_source_identity(
        provider,
        source,
        _signature_request_content_source(file_entry_or_request),
    )

    if validation_status is not None:
        return _signature_result(
            source=source,
            content_source=content_source,
            max_bytes_requested=normalized_max_bytes,
            status=validation_status,
            warnings=(validation_warning,),
        )

    if source.entry_type != "file":
        status = AnalysisStatus(
            code="path_not_file",
            message="Signature analysis requires a file entry.",
        )
        return _signature_result(
            source=source,
            content_source=content_source,
            max_bytes_requested=normalized_max_bytes,
            status=status,
            warnings=(
                AnalysisWarning(
                    code="path_not_file",
                    message=(
                        "Directory or non-file entries cannot be signature-checked."
                    ),
                    path=source.file_path,
                    source="content_analysis",
                ),
            ),
        )

    if provider is None:
        status = AnalysisStatus(
            code="metadata_only_source",
            message="Filesystem metadata alone is not analysis content.",
        )
        return _signature_result(
            source=source,
            content_source=_content_source_with_status(
                content_source,
                status=status,
                source_content_size=None,
            ),
            max_bytes_requested=normalized_max_bytes,
            status=status,
            warnings=(
                AnalysisWarning(
                    code="metadata_only_source",
                    message=(
                        "No explicit Stage 4 analysis content provider was supplied."
                    ),
                    path=source.file_path,
                    source="content_analysis",
                ),
            ),
        )

    try:
        content = provider.get_content(source)
    except Exception as error:
        status = AnalysisStatus(
            code="content_provider_error",
            message=(
                "Analysis content provider failed before signature detection: "
                f"{type(error).__name__}."
            ),
        )
        return _signature_result(
            source=source,
            content_source=_content_source_with_status(
                content_source,
                status=status,
                source_content_size=None,
            ),
            max_bytes_requested=normalized_max_bytes,
            status=status,
            warnings=(
                AnalysisWarning(
                    code="content_provider_error",
                    message="Analysis content provider raised an exception.",
                    path=source.file_path,
                    source="analysis_content_provider",
                ),
            ),
        )

    if content is None:
        status = AnalysisStatus(
            code="content_source_unavailable",
            message="Analysis content provider has no raw bytes for this file entry.",
        )
        return _signature_result(
            source=source,
            content_source=_content_source_with_status(
                content_source,
                status=status,
                source_content_size=None,
            ),
            max_bytes_requested=normalized_max_bytes,
            status=status,
            warnings=(
                AnalysisWarning(
                    code="content_source_unavailable",
                    message="No raw analysis content is registered for this file entry.",
                    path=source.file_path,
                    source="analysis_content_provider",
                ),
            ),
        )

    inspected_prefix = content.data[:normalized_max_bytes]
    signature = _detect_supported_signature(inspected_prefix)
    content_source = content.to_content_source_identity()
    if signature is not None:
        status = AnalysisStatus(
            code="ok",
            message=(
                "File signature detected from explicit analysis provider bytes."
            ),
        )
        return _signature_result(
            source=source,
            content_source=content_source,
            max_bytes_requested=normalized_max_bytes,
            status=status,
            bytes_inspected=len(inspected_prefix),
            detected_type=signature.detected_type,
            detected_signature=signature.detected_signature,
            detected_mime_type=signature.mime_type,
            warnings=content.warnings,
        )

    partial_signature = _matching_partial_signature(inspected_prefix)
    if partial_signature is not None:
        status = AnalysisStatus(
            code="insufficient_signature_bytes",
            message="More bytes are required to make this signature decision.",
        )
        return _signature_result(
            source=source,
            content_source=content_source,
            max_bytes_requested=normalized_max_bytes,
            status=status,
            bytes_inspected=len(inspected_prefix),
            warnings=content.warnings
            + (
                AnalysisWarning(
                    code="insufficient_signature_bytes",
                    message=(
                        "Inspected bytes are only a partial known signature prefix."
                    ),
                    path=source.file_path,
                    source="content_analysis",
                ),
            ),
        )

    status = AnalysisStatus(
        code="unknown_signature",
        message="No supported file signature was detected in the bounded prefix.",
    )
    return _signature_result(
        source=source,
        content_source=content_source,
        max_bytes_requested=normalized_max_bytes,
        status=status,
        bytes_inspected=len(inspected_prefix),
        warnings=content.warnings
        + (
            AnalysisWarning(
                code="unknown_signature",
                message="Bounded prefix did not match a supported signature.",
                path=source.file_path,
                source="content_analysis",
            ),
        ),
    )


def analyze_file_signature(
    file_entry_or_request: (
        Mapping[str, object] | AnalysisSourceProvenance | SignatureAnalysisRequest
    ),
    *,
    provider: AnalysisContentProvider | None = None,
    max_bytes: object | None = None,
    evidence_id: str | None = None,
    case_id: str | None = None,
) -> SignatureAnalysisResult:
    """Alias for bounded provider-backed file signature detection."""

    return detect_file_signature(
        file_entry_or_request,
        provider=provider,
        max_bytes=max_bytes,
        evidence_id=evidence_id,
        case_id=case_id,
    )


def evaluate_extension_mismatch(
    signature_result: SignatureAnalysisResult,
) -> ExtensionMismatchResult:
    """Evaluate an existing signature result against filename metadata only.

    S4-T04 deliberately does not accept providers and does not re-run
    signature detection. It only compares reviewed S4-T03 result fields with
    the copied source file name/path metadata already present on the result.
    """

    source = signature_result.source
    detected_type = signature_result.detected_type
    expected_extensions = SUPPORTED_SIGNATURE_EXTENSIONS.get(detected_type or "", ())

    if source.entry_type != "file":
        status = AnalysisStatus(
            code="path_not_file",
            message="Extension mismatch evaluation requires a file entry.",
        )
        return _extension_mismatch_result(
            signature_result=signature_result,
            status=status,
            expected_extensions=expected_extensions,
            warnings=signature_result.warnings
            + (
                AnalysisWarning(
                    code="path_not_file",
                    message=(
                        "Directory or non-file entries cannot be checked for "
                        "extension mismatch."
                    ),
                    path=source.file_path,
                    source="content_analysis",
                ),
            ),
        )

    if signature_result.status.code != "ok":
        status = AnalysisStatus(
            code="signature_not_available",
            message=(
                "Extension mismatch was not evaluated because signature "
                "detection did not complete successfully."
            ),
        )
        return _extension_mismatch_result(
            signature_result=signature_result,
            status=status,
            warnings=signature_result.warnings
            + (
                AnalysisWarning(
                    code="signature_not_available",
                    message=(
                        "Signature result status was "
                        f"{signature_result.status.code}."
                    ),
                    path=source.file_path,
                    source="content_analysis",
                ),
            ),
        )

    if not detected_type:
        status = AnalysisStatus(
            code="signature_not_available",
            message=(
                "Extension mismatch was not evaluated because no detected "
                "signature type was present."
            ),
        )
        return _extension_mismatch_result(
            signature_result=signature_result,
            status=status,
            warnings=signature_result.warnings
            + (
                AnalysisWarning(
                    code="signature_not_available",
                    message="Signature result did not include a detected type.",
                    path=source.file_path,
                    source="content_analysis",
                ),
            ),
        )

    if not expected_extensions:
        status = AnalysisStatus(
            code="unsupported_signature_type",
            message=(
                "Extension mismatch rules do not support this detected "
                "signature type."
            ),
        )
        return _extension_mismatch_result(
            signature_result=signature_result,
            status=status,
            warnings=signature_result.warnings
            + (
                AnalysisWarning(
                    code="unsupported_signature_type",
                    message=(
                        "No extension rule is defined for detected type "
                        f"{detected_type}."
                    ),
                    path=source.file_path,
                    source="content_analysis",
                ),
            ),
        )

    observed_extension, has_name_or_path = _observed_extension(source)
    if not has_name_or_path:
        status = AnalysisStatus(
            code="file_name_unavailable",
            message=(
                "Extension mismatch was not evaluated because file name/path "
                "metadata is unavailable."
            ),
        )
        return _extension_mismatch_result(
            signature_result=signature_result,
            status=status,
            expected_extensions=expected_extensions,
            warnings=signature_result.warnings
            + (
                AnalysisWarning(
                    code="file_name_unavailable",
                    message="File name and file path metadata are unavailable.",
                    path=source.file_path,
                    source="content_analysis",
                ),
            ),
        )

    if observed_extension is None:
        status = AnalysisStatus(
            code="extension_missing",
            message=(
                "Extension mismatch was not evaluated because the file "
                "metadata has no extension."
            ),
        )
        return _extension_mismatch_result(
            signature_result=signature_result,
            status=status,
            expected_extensions=expected_extensions,
            warnings=signature_result.warnings
            + (
                AnalysisWarning(
                    code="extension_missing",
                    message="File name/path metadata does not include an extension.",
                    path=source.file_path,
                    source="content_analysis",
                ),
            ),
        )

    mismatch = observed_extension not in expected_extensions
    if mismatch:
        status = AnalysisStatus(
            code="extension_mismatch",
            message="Observed extension is not expected for the detected signature.",
        )
        warnings = signature_result.warnings + (
            AnalysisWarning(
                code="extension_mismatch",
                message=(
                    f"Observed extension {observed_extension} is not in the "
                    "expected extension list for the detected signature."
                ),
                path=source.file_path,
                source="content_analysis",
            ),
        )
    else:
        status = AnalysisStatus(
            code="extension_match",
            message="Observed extension matches the detected signature rule.",
        )
        warnings = signature_result.warnings

    return _extension_mismatch_result(
        signature_result=signature_result,
        status=status,
        observed_extension=observed_extension,
        expected_extensions=expected_extensions,
        mismatch=mismatch,
        warnings=warnings,
    )


def check_extension_mismatch(
    signature_result: SignatureAnalysisResult,
) -> ExtensionMismatchResult:
    """Alias for extension/signature mismatch evaluation."""

    return evaluate_extension_mismatch(signature_result)


def _known_file_match_result(
    *,
    hash_result: HashAnalysisResult,
    status: AnalysisStatus,
    matched: bool | None = None,
    match_category: str | None = None,
    matched_algorithm: str | None = None,
    matched_digest: str | None = None,
    matched_records: tuple[KnownFileRecord, ...] = (),
    warnings: tuple[AnalysisWarning, ...] = (),
) -> KnownFileMatchResult:
    timestamp = utc_now()
    return KnownFileMatchResult(
        source=hash_result.source,
        content_source=hash_result.content_source,
        hash_status=hash_result.status,
        requested_algorithms=hash_result.requested_algorithms,
        digests=hash_result.digests,
        status=status,
        matched=matched,
        match_category=match_category,
        matched_algorithm=matched_algorithm,
        matched_digest=matched_digest,
        matched_records=matched_records,
        bytes_analyzed=hash_result.bytes_analyzed,
        hash_created_at=hash_result.created_at,
        hash_completed_at=hash_result.completed_at,
        created_at=timestamp,
        completed_at=timestamp,
        warnings=warnings,
    )


def _computed_hash_digests(hash_result: HashAnalysisResult) -> dict[str, str]:
    computed: dict[str, str] = {}
    for digest in hash_result.digests:
        algorithm = _normalize_hash_algorithm_name(digest.algorithm)
        digest_value = _normalize_digest_value(digest.digest)
        if (
            algorithm is None
            or digest_value is None
            or digest.status.code != "ok"
        ):
            continue
        computed.setdefault(algorithm, digest_value)
    return computed


def _known_file_records_from_input(
    known_files: Iterable[KnownFileRecord | Mapping[str, object]],
    source: AnalysisSourceProvenance,
) -> tuple[tuple[KnownFileRecord, ...], tuple[AnalysisWarning, ...]]:
    if isinstance(known_files, (KnownFileRecord, Mapping)):
        raw_records = (known_files,)
    else:
        try:
            raw_records = tuple(known_files)
        except TypeError:
            warning = _invalid_known_file_record_warning(
                source,
                0,
                "Known-file records must be supplied as an iterable.",
            )
            return (), (warning,)

    records: list[KnownFileRecord] = []
    warnings: list[AnalysisWarning] = []
    for index, raw_record in enumerate(raw_records):
        record, warning = _known_file_record_from_input(
            raw_record,
            source,
            index,
        )
        if warning is not None:
            warnings.append(warning)
            continue
        if record is not None:
            records.append(record)

    return tuple(records), tuple(warnings)


def _known_file_record_from_input(
    raw_record: object,
    source: AnalysisSourceProvenance,
    index: int,
) -> tuple[KnownFileRecord | None, AnalysisWarning | None]:
    if isinstance(raw_record, KnownFileRecord):
        raw_algorithm = raw_record.algorithm
        raw_digest = raw_record.digest
        raw_category = raw_record.category
        metadata = raw_record.metadata
        dataset_name = raw_record.dataset_name
        dataset_version = raw_record.dataset_version
        record_id = raw_record.record_id
        file_name = raw_record.file_name
        original_algorithm = raw_record.original_algorithm or raw_record.algorithm
        original_digest = raw_record.original_digest or raw_record.digest
    elif isinstance(raw_record, Mapping):
        raw_algorithm = raw_record.get("algorithm")
        raw_digest = raw_record.get("digest")
        raw_category = raw_record.get("category")
        metadata = _known_file_record_metadata(raw_record)
        dataset_name = _optional_str(raw_record.get("dataset_name"))
        dataset_version = _optional_str(raw_record.get("dataset_version"))
        record_id = _optional_str(raw_record.get("record_id"))
        file_name = _optional_str(raw_record.get("file_name"))
        original_algorithm = _optional_str(raw_algorithm)
        original_digest = _optional_str(raw_digest)
    else:
        return (
            None,
            _invalid_known_file_record_warning(
                source,
                index,
                "Record must be a KnownFileRecord or mapping.",
            ),
        )

    algorithm, algorithm_warning = _normalize_known_file_record_algorithm(
        raw_algorithm,
        source,
        index,
    )
    if algorithm_warning is not None:
        return None, algorithm_warning

    digest, digest_warning = _normalize_known_file_record_digest(
        raw_digest,
        source,
        index,
    )
    if digest_warning is not None:
        return None, digest_warning

    category, category_warning = _normalize_known_file_record_category(
        raw_category,
        source,
        index,
    )
    if category_warning is not None:
        return None, category_warning

    return (
        KnownFileRecord(
            algorithm=algorithm or "",
            digest=digest or "",
            category=category or "",
            dataset_name=dataset_name,
            dataset_version=dataset_version,
            record_id=record_id,
            file_name=file_name,
            metadata=_json_safe_mapping(metadata),
            original_algorithm=original_algorithm,
            original_digest=original_digest,
        ),
        None,
    )


def _known_file_record_metadata(record: Mapping[str, object]) -> dict[str, object]:
    recognized_fields = {
        "algorithm",
        "digest",
        "category",
        "dataset_name",
        "dataset_version",
        "record_id",
        "file_name",
        "metadata",
    }
    metadata: dict[str, object] = {
        str(key): value
        for key, value in record.items()
        if str(key) not in recognized_fields
    }
    record_metadata = record.get("metadata")
    if isinstance(record_metadata, Mapping):
        metadata.update({str(key): value for key, value in record_metadata.items()})
    elif record_metadata is not None:
        metadata["metadata"] = record_metadata
    return metadata


def _normalize_known_file_record_algorithm(
    value: object,
    source: AnalysisSourceProvenance,
    index: int,
) -> tuple[str | None, AnalysisWarning | None]:
    if not isinstance(value, str) or not value.strip():
        return (
            None,
            _invalid_known_file_record_warning(
                source,
                index,
                "Record is missing a hash algorithm.",
            ),
        )
    algorithm = _normalize_hash_algorithm_name(value)
    if algorithm not in SUPPORTED_HASH_ALGORITHMS:
        return (
            None,
            _invalid_known_file_record_warning(
                source,
                index,
                "Record uses an unsupported hash algorithm.",
            ),
        )
    return algorithm, None


def _normalize_known_file_record_digest(
    value: object,
    source: AnalysisSourceProvenance,
    index: int,
) -> tuple[str | None, AnalysisWarning | None]:
    digest = _normalize_digest_value(value)
    if digest is None:
        return (
            None,
            _invalid_known_file_record_warning(
                source,
                index,
                "Record is missing a digest value.",
            ),
        )
    return digest, None


def _normalize_known_file_record_category(
    value: object,
    source: AnalysisSourceProvenance,
    index: int,
) -> tuple[str | None, AnalysisWarning | None]:
    if not isinstance(value, str) or not value.strip():
        return (
            None,
            _invalid_known_file_record_warning(
                source,
                index,
                "Record is missing a known-file category.",
            ),
        )
    category = value.strip().lower()
    if category not in SUPPORTED_KNOWN_FILE_CATEGORIES:
        return (
            None,
            _invalid_known_file_record_warning(
                source,
                index,
                "Record category must be known_good, known_bad, or known_unknown.",
            ),
        )
    return category, None


def _normalize_hash_algorithm_name(value: object) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    return value.strip().lower().replace("-", "").replace("_", "")


def _normalize_digest_value(value: object) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    return value.strip().lower()


def _invalid_known_file_record_warning(
    source: AnalysisSourceProvenance,
    index: int,
    message: str,
) -> AnalysisWarning:
    return AnalysisWarning(
        code="invalid_known_file_record",
        message=f"Known-file record {index}: {message}",
        path=source.file_path,
        source="known_file_records",
    )


def _primary_known_file_match_key(
    matched_records_by_key: Mapping[tuple[str, str], list[KnownFileRecord]],
    computed_digests: Mapping[str, str],
) -> tuple[str, str]:
    for algorithm in _KNOWN_FILE_ALGORITHM_PREFERENCE:
        key = (algorithm, computed_digests.get(algorithm, ""))
        if key in matched_records_by_key:
            return key
    return next(iter(matched_records_by_key))


def _conflicting_known_file_match_key(
    matched_records_by_key: Mapping[tuple[str, str], list[KnownFileRecord]],
    computed_digests: Mapping[str, str],
) -> tuple[str, str] | None:
    for algorithm in _KNOWN_FILE_ALGORITHM_PREFERENCE:
        key = (algorithm, computed_digests.get(algorithm, ""))
        records = matched_records_by_key.get(key, ())
        categories = {record.category for record in records}
        if len(categories) > 1:
            return key

    for key, records in matched_records_by_key.items():
        categories = {record.category for record in records}
        if len(categories) > 1:
            return key
    return None


def _hash_match_context_warnings(
    hash_result: HashAnalysisResult,
) -> tuple[AnalysisWarning, ...]:
    warnings: list[AnalysisWarning] = []
    if hash_result.content_source.synthetic:
        warnings.append(
            AnalysisWarning(
                code="synthetic_hash_match_context",
                message=(
                    "Known-file match used a digest computed from synthetic "
                    "analysis bytes, not parsed evidence bytes."
                ),
                path=hash_result.source.file_path,
                source="content_analysis",
            )
        )
    if hash_result.content_source.generated:
        warnings.append(
            AnalysisWarning(
                code="generated_fixture_hash_match_context",
                message=(
                    "Known-file match used a digest computed from generated "
                    "fixture bytes, not parsed evidence bytes."
                ),
                path=hash_result.source.file_path,
                source="content_analysis",
            )
        )
    return tuple(warnings)


def _extension_mismatch_result(
    *,
    signature_result: SignatureAnalysisResult,
    status: AnalysisStatus,
    observed_extension: str | None = None,
    expected_extensions: tuple[str, ...] = (),
    mismatch: bool | None = None,
    warnings: tuple[AnalysisWarning, ...] = (),
) -> ExtensionMismatchResult:
    timestamp = utc_now()
    return ExtensionMismatchResult(
        source=signature_result.source,
        content_source=signature_result.content_source,
        signature_status=signature_result.status,
        status=status,
        detected_type=signature_result.detected_type,
        detected_signature=signature_result.detected_signature,
        detected_mime_type=signature_result.detected_mime_type,
        observed_extension=observed_extension,
        expected_extensions=expected_extensions,
        mismatch=mismatch,
        signature_created_at=signature_result.created_at,
        signature_completed_at=signature_result.completed_at,
        created_at=timestamp,
        completed_at=timestamp,
        warnings=warnings,
    )


def _observed_extension(
    source: AnalysisSourceProvenance,
) -> tuple[str | None, bool]:
    has_name_or_path = False
    for value in (source.file_name, source.file_path):
        text = _stripped_optional_str(value)
        if text is None:
            continue
        has_name_or_path = True
        extension = _rightmost_extension(text)
        if extension is not None:
            return extension, True

    return None, has_name_or_path


def _rightmost_extension(value: str) -> str | None:
    name = value.replace("\\", "/").rsplit("/", 1)[-1]
    if not name:
        return None

    dot_index = name.rfind(".")
    if dot_index <= 0 or dot_index == len(name) - 1:
        return None
    return name[dot_index:].lower()


def _stripped_optional_str(value: str | None) -> str | None:
    if value is None:
        return None
    text = value.strip()
    return text or None


def _source_from_signature_input(
    file_entry_or_request: (
        Mapping[str, object] | AnalysisSourceProvenance | SignatureAnalysisRequest
    ),
    *,
    evidence_id: str | None,
    case_id: str | None,
) -> AnalysisSourceProvenance:
    if isinstance(file_entry_or_request, SignatureAnalysisRequest):
        return file_entry_or_request.source
    if isinstance(file_entry_or_request, AnalysisSourceProvenance):
        return file_entry_or_request
    return AnalysisSourceProvenance.from_file_entry(
        file_entry_or_request,
        evidence_id=evidence_id,
        case_id=case_id,
    )


def _requested_signature_max_bytes(
    file_entry_or_request: (
        Mapping[str, object] | AnalysisSourceProvenance | SignatureAnalysisRequest
    ),
    max_bytes: object | None,
) -> object:
    if max_bytes is not None:
        return max_bytes
    if isinstance(file_entry_or_request, SignatureAnalysisRequest):
        return file_entry_or_request.max_bytes_requested
    return DEFAULT_SIGNATURE_MAX_BYTES


def _signature_request_content_source(
    file_entry_or_request: (
        Mapping[str, object] | AnalysisSourceProvenance | SignatureAnalysisRequest
    ),
) -> AnalysisContentSourceIdentity | None:
    if isinstance(file_entry_or_request, SignatureAnalysisRequest):
        return file_entry_or_request.content_source
    return None


def _normalize_signature_max_bytes(
    requested_value: object,
    source: AnalysisSourceProvenance,
) -> tuple[int, AnalysisStatus | None, AnalysisWarning | None]:
    if not isinstance(requested_value, int) or isinstance(requested_value, bool):
        status = AnalysisStatus(
            code="invalid_analysis_request",
            message="Signature max bytes must be a positive integer.",
        )
        return (
            0,
            status,
            AnalysisWarning(
                code=status.code,
                message=status.message,
                path=source.file_path,
                source="content_analysis",
            ),
        )

    normalized = requested_value
    if normalized <= 0:
        status = AnalysisStatus(
            code="invalid_analysis_request",
            message="Signature max bytes must be greater than zero.",
        )
        return (
            normalized,
            status,
            AnalysisWarning(
                code=status.code,
                message=status.message,
                path=source.file_path,
                source="content_analysis",
            ),
        )

    return normalized, None, None


def _detect_supported_signature(
    inspected_prefix: bytes,
) -> FileSignatureDefinition | None:
    for signature in SUPPORTED_FILE_SIGNATURES:
        if inspected_prefix.startswith(signature.magic):
            return signature
    return None


def _matching_partial_signature(
    inspected_prefix: bytes,
) -> FileSignatureDefinition | None:
    for signature in SUPPORTED_FILE_SIGNATURES:
        if len(inspected_prefix) < len(signature.magic) and signature.magic.startswith(
            inspected_prefix
        ):
            return signature
    return None


def _signature_result(
    *,
    source: AnalysisSourceProvenance,
    content_source: AnalysisContentSourceIdentity,
    max_bytes_requested: int,
    status: AnalysisStatus,
    bytes_inspected: int | None = None,
    detected_type: str | None = None,
    detected_signature: str | None = None,
    detected_mime_type: str | None = None,
    warnings: tuple[AnalysisWarning, ...] = (),
) -> SignatureAnalysisResult:
    timestamp = utc_now()
    return SignatureAnalysisResult(
        source=source,
        content_source=content_source,
        max_bytes_requested=max_bytes_requested,
        status=status,
        bytes_inspected=bytes_inspected,
        detected_type=detected_type,
        detected_signature=detected_signature,
        detected_mime_type=detected_mime_type,
        created_at=timestamp,
        completed_at=timestamp,
        warnings=warnings,
    )


def _source_from_hash_input(
    file_entry_or_request: (
        Mapping[str, object] | AnalysisSourceProvenance | HashAnalysisRequest
    ),
    *,
    evidence_id: str | None,
    case_id: str | None,
) -> AnalysisSourceProvenance:
    if isinstance(file_entry_or_request, HashAnalysisRequest):
        return file_entry_or_request.source
    if isinstance(file_entry_or_request, AnalysisSourceProvenance):
        return file_entry_or_request
    return AnalysisSourceProvenance.from_file_entry(
        file_entry_or_request,
        evidence_id=evidence_id,
        case_id=case_id,
    )


def _requested_hash_algorithms(
    file_entry_or_request: (
        Mapping[str, object] | AnalysisSourceProvenance | HashAnalysisRequest
    ),
    algorithms: Iterable[object] | str | None,
) -> Iterable[object] | str:
    if algorithms is not None:
        return algorithms
    if isinstance(file_entry_or_request, HashAnalysisRequest):
        return file_entry_or_request.requested_algorithms
    return DEFAULT_HASH_ALGORITHMS


def _request_content_source(
    file_entry_or_request: (
        Mapping[str, object] | AnalysisSourceProvenance | HashAnalysisRequest
    ),
) -> AnalysisContentSourceIdentity | None:
    if isinstance(file_entry_or_request, HashAnalysisRequest):
        return file_entry_or_request.content_source
    return None


def _normalize_hash_algorithms(
    requested_values: Iterable[object] | str,
    source: AnalysisSourceProvenance,
) -> tuple[tuple[str, ...], AnalysisStatus | None, AnalysisWarning | None]:
    try:
        raw_values = (
            (requested_values,)
            if isinstance(requested_values, str)
            else tuple(requested_values)
        )
    except TypeError:
        status = AnalysisStatus(
            code="invalid_analysis_request",
            message="Hash algorithms must be supplied as strings or an iterable.",
        )
        return (
            (),
            status,
            AnalysisWarning(
                code=status.code,
                message=status.message,
                path=source.file_path,
                source="content_analysis",
            ),
        )
    if not raw_values:
        status = AnalysisStatus(
            code="invalid_analysis_request",
            message="At least one hash algorithm is required.",
        )
        return (
            (),
            status,
            AnalysisWarning(
                code=status.code,
                message=status.message,
                path=source.file_path,
                source="content_analysis",
            ),
        )

    normalized: list[str] = []
    invalid_values: list[str] = []
    unsupported_values: list[str] = []
    for value in raw_values:
        if not isinstance(value, str) or not value.strip():
            invalid_values.append(str(value))
            continue
        algorithm = value.strip().lower().replace("-", "").replace("_", "")
        if algorithm not in SUPPORTED_HASH_ALGORITHMS:
            unsupported_values.append(algorithm)
            normalized.append(algorithm)
            continue
        if algorithm not in normalized:
            normalized.append(algorithm)

    if invalid_values:
        status = AnalysisStatus(
            code="invalid_analysis_request",
            message="Hash algorithms must be non-empty strings.",
        )
        return (
            tuple(normalized),
            status,
            AnalysisWarning(
                code=status.code,
                message=status.message,
                path=source.file_path,
                source="content_analysis",
            ),
        )

    if unsupported_values:
        status = AnalysisStatus(
            code="unsupported_algorithm",
            message=(
                "Supported hash algorithms are sha256, md5, and sha1."
            ),
        )
        return (
            tuple(normalized),
            status,
            AnalysisWarning(
                code=status.code,
                message=(
                    "Unsupported hash algorithm requested: "
                    f"{', '.join(unsupported_values)}."
                ),
                path=source.file_path,
                source="content_analysis",
            ),
        )

    return tuple(normalized), None, None


def _digest_placeholders(
    algorithms: tuple[str, ...],
    *,
    status: AnalysisStatus | None = None,
) -> tuple[HashDigestResult, ...]:
    placeholder_status = status or AnalysisStatus(
        code="hash_not_computed",
        message="Hash digest was not computed.",
    )
    return tuple(
        HashDigestResult(algorithm=algorithm, status=placeholder_status)
        for algorithm in algorithms
    )


def _validation_digest_placeholders(
    algorithms: tuple[str, ...],
    *,
    validation_status: AnalysisStatus,
) -> tuple[HashDigestResult, ...]:
    if validation_status.code != "unsupported_algorithm":
        return _digest_placeholders(algorithms)

    hash_not_computed = AnalysisStatus(
        code="hash_not_computed",
        message="Hash digest was not computed.",
    )
    return tuple(
        HashDigestResult(
            algorithm=algorithm,
            status=(
                validation_status
                if algorithm not in _HASH_FACTORIES
                else hash_not_computed
            ),
        )
        for algorithm in algorithms
    )


def _initial_content_source_identity(
    provider: AnalysisContentProvider | None,
    source: AnalysisSourceProvenance,
    request_content_source: AnalysisContentSourceIdentity | None,
) -> AnalysisContentSourceIdentity:
    status = AnalysisStatus(
        code="analysis_not_started",
        message="Analysis content source has not been read.",
    )
    if provider is not None:
        return AnalysisContentSourceIdentity(
            provider_name=_provider_str(provider, "name", "analysis-content-provider"),
            source_kind=_provider_str(provider, "source_kind", "unknown"),
            read_only=bool(_provider_bool(provider, "read_only") and source.read_only),
            synthetic=_provider_bool(provider, "synthetic"),
            generated=_provider_bool(provider, "generated"),
            source_content_size=None,
            status=status,
            parser_name=source.adapter_name,
        )

    if request_content_source is not None:
        return _content_source_with_status(
            request_content_source,
            status=status,
            source_content_size=None,
        )

    return AnalysisContentSourceIdentity(
        provider_name="metadata-only-source",
        source_kind="metadata_only",
        read_only=source.read_only,
        synthetic=False,
        generated=False,
        source_content_size=None,
        status=status,
        parser_name=source.adapter_name,
    )


def _content_source_with_status(
    content_source: AnalysisContentSourceIdentity,
    *,
    status: AnalysisStatus,
    source_content_size: int | None,
) -> AnalysisContentSourceIdentity:
    return AnalysisContentSourceIdentity(
        provider_name=content_source.provider_name,
        source_kind=content_source.source_kind,
        read_only=content_source.read_only,
        synthetic=content_source.synthetic,
        generated=content_source.generated,
        source_content_size=source_content_size,
        status=status,
        parser_name=content_source.parser_name,
        parser_version=content_source.parser_version,
        source_name=content_source.source_name,
        source_version=content_source.source_version,
    )


def _hash_result(
    *,
    source: AnalysisSourceProvenance,
    content_source: AnalysisContentSourceIdentity,
    requested_algorithms: tuple[str, ...],
    status: AnalysisStatus,
    digests: tuple[HashDigestResult, ...],
    bytes_analyzed: int | None = None,
    warnings: tuple[AnalysisWarning, ...] = (),
) -> HashAnalysisResult:
    timestamp = utc_now()
    return HashAnalysisResult(
        source=source,
        content_source=content_source,
        requested_algorithms=requested_algorithms,
        digests=digests,
        status=status,
        bytes_analyzed=bytes_analyzed,
        created_at=timestamp,
        completed_at=timestamp,
        warnings=warnings,
    )


def _provider_str(
    provider: AnalysisContentProvider,
    field_name: str,
    default: str,
) -> str:
    value = getattr(provider, field_name, default)
    return str(value) if value is not None else default


def _provider_bool(
    provider: AnalysisContentProvider,
    field_name: str,
) -> bool:
    return bool(getattr(provider, field_name, False))


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


def _json_safe_mapping(value: object) -> dict[str, object]:
    if not isinstance(value, Mapping):
        return {}

    result: dict[str, object] = {}
    for key, item in value.items():
        result[str(key)] = _json_safe_value(item)
    return result


def _json_safe_value(value: object) -> object:
    if value is None or isinstance(value, (str, int, bool)):
        return value
    if isinstance(value, float):
        return value if math.isfinite(value) else str(value)
    if isinstance(value, bytes):
        return {"type": "bytes", "hex": value.hex()}
    if isinstance(value, Mapping):
        return _json_safe_mapping(value)
    if isinstance(value, (list, tuple)):
        return [_json_safe_value(item) for item in value]
    if isinstance(value, set):
        return [_json_safe_value(item) for item in sorted(value, key=str)]
    return str(value)
