"""Stage 4 hash and signature analysis contract structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from typing import Iterable, Mapping, Protocol


CONTENT_ANALYSIS_SCHEMA_VERSION = "stage4.content_analysis.v1"
DEFAULT_HASH_ALGORITHMS = ("sha256",)
SUPPORTED_HASH_ALGORITHMS = ("sha256", "md5", "sha1")
_HASH_FACTORIES = {
    "sha256": hashlib.sha256,
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
}


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
