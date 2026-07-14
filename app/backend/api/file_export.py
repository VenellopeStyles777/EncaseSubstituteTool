"""Backend fixture/stub file export service for Stage 3."""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
import sqlite3
from typing import Mapping, Protocol

from app.backend.case_store import insert_audit_event
from app.backend.forensic_core import (
    ExportContentSourceIdentity,
    ExportHashSummary,
    ExportManifest,
    ExportRequest,
    ExportResult,
    ExportSourceProvenance,
    ExportStatus,
    ExportWarning,
    export_result_to_json,
)


DEFAULT_MANIFEST_SUFFIX = ".manifest.json"
EXPORT_AUDIT_DETAILS_SCHEMA_VERSION = "stage3.export_audit.v1"


@dataclass(frozen=True)
class ExportContent:
    """Provider-owned raw bytes for export plus source identity."""

    data: bytes
    provider_name: str
    source_kind: str
    read_only: bool = True
    synthetic: bool = False
    parser_name: str | None = None
    parser_version: str | None = None
    warnings: tuple[ExportWarning, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ExportAuditContext:
    """Explicit opt-in case-store audit context for export attempts."""

    connection: sqlite3.Connection
    case_id: str
    evidence_id: str | None = None
    actor: str | None = None
    audit_failed_exports: bool = False


class ExportContentProvider(Protocol):
    """Protocol for raw export byte providers.

    This is intentionally separate from preview providers. Export must consume
    provider-owned raw bytes, not rendered preview text or hex.
    """

    name: str
    source_kind: str
    read_only: bool
    synthetic: bool

    def get_content(
        self,
        source: ExportSourceProvenance,
    ) -> ExportContent | None:
        """Return raw export bytes or None if unavailable."""


class StubExportContentProvider:
    """Deterministic raw export provider for fixture/stub tests."""

    name = "stub-export-provider"
    source_kind = "stub"
    read_only = True
    synthetic = True

    def __init__(self, content_by_file_id: Mapping[str, bytes] | None = None) -> None:
        self._content_by_file_id = {
            "stub-file-hello": b"Hello, world!",
            **(content_by_file_id or {}),
        }

    def get_content(
        self,
        source: ExportSourceProvenance,
    ) -> ExportContent | None:
        file_id = source.file_id or ""
        data = self._content_by_file_id.get(file_id)
        if data is None:
            return None

        return ExportContent(
            data=data,
            provider_name=self.name,
            source_kind=self.source_kind,
            read_only=self.read_only and source.read_only,
            synthetic=self.synthetic,
            parser_name=source.adapter_name,
            warnings=(
                ExportWarning(
                    code="stub_export_content",
                    message="Export bytes are synthetic stub content, not parsed evidence bytes.",
                    path=source.file_path,
                    source="export_content_provider",
                ),
            ),
        )


def export_file(
    file_entry_or_request: Mapping[str, object] | ExportRequest,
    output_directory: str | Path | None = None,
    *,
    provider: ExportContentProvider | None = None,
    output_name: str | None = None,
    audit_context: ExportAuditContext | None = None,
) -> ExportResult:
    """Export explicit provider-backed raw bytes to a selected output directory."""

    export_provider = provider or StubExportContentProvider()
    source = _source_from_input(file_entry_or_request)
    requested_directory = _requested_output_directory(
        file_entry_or_request,
        output_directory,
    )
    requested_output_path = _requested_output_path(file_entry_or_request)

    if source.entry_type != "file":
        return _finalize_result(
            _result(
                status_code="path_not_file",
                status_message="Export requires a file entry.",
                source=source,
                provider=export_provider,
                destination_directory=_path_str(requested_directory),
                requested_output_path=requested_output_path,
                warnings=(
                    ExportWarning(
                        code="path_not_file",
                        message="Directory or non-file entries cannot be exported.",
                        path=source.file_path,
                        source="file_export",
                    ),
                ),
            ),
            audit_context,
        )

    if not _path_str(requested_directory):
        return _finalize_result(
            _result(
                status_code="destination_not_selected",
                status_message="An explicit output directory is required.",
                source=source,
                provider=export_provider,
                requested_output_path=requested_output_path,
                warnings=(
                    ExportWarning(
                        code="destination_not_selected",
                        message="No examiner-selected output directory was supplied.",
                        source="file_export",
                    ),
                ),
            ),
            audit_context,
        )

    destination_dir = Path(requested_directory).expanduser().resolve(strict=False)
    destination_status = _destination_status(source, destination_dir)
    if destination_status is not None:
        return _finalize_result(
            _result(
                status_code=destination_status.code,
                status_message=destination_status.message,
                source=source,
                provider=export_provider,
                destination_directory=str(destination_dir),
                requested_output_path=requested_output_path,
                destination_status=destination_status,
                warnings=(
                    ExportWarning(
                        code=destination_status.code,
                        message=destination_status.message,
                        path=str(destination_dir),
                        source="destination_safety",
                    ),
                ),
            ),
            audit_context,
        )

    requested_name = output_name or requested_output_path or source.file_name
    safe_output_name = _safe_output_name(requested_name)
    if safe_output_name is None:
        return _finalize_result(
            _result(
                status_code="invalid_output_name",
                status_message="Output file name must be a safe file name without traversal.",
                source=source,
                provider=export_provider,
                destination_directory=str(destination_dir),
                requested_output_path=requested_name,
                warnings=(
                    ExportWarning(
                        code="invalid_output_name",
                        message="Output file name contained unsafe characters or path traversal.",
                        path=requested_name,
                        source="file_export",
                    ),
                ),
            ),
            audit_context,
        )

    output_path = destination_dir / safe_output_name
    manifest_path = destination_dir / f"{safe_output_name}{DEFAULT_MANIFEST_SUFFIX}"
    if output_path.exists() or manifest_path.exists():
        existing_path = output_path if output_path.exists() else manifest_path
        return _finalize_result(
            _result(
                status_code="output_exists",
                status_message="Output file or manifest already exists.",
                source=source,
                provider=export_provider,
                destination_directory=str(destination_dir),
                requested_output_path=str(output_path),
                output_path=str(output_path),
                manifest_path=str(manifest_path),
                warnings=(
                    ExportWarning(
                        code="output_exists",
                        message="Refusing to overwrite an existing output or manifest file.",
                        path=str(existing_path),
                        source="file_export",
                    ),
                ),
            ),
            audit_context,
        )

    content = export_provider.get_content(source)
    if content is None:
        return _finalize_result(
            _result(
                status_code="content_source_unavailable",
                status_message="Export provider has no raw bytes for this file entry.",
                source=source,
                provider=export_provider,
                destination_directory=str(destination_dir),
                requested_output_path=str(output_path),
                output_path=str(output_path),
                manifest_path=str(manifest_path),
                content_status_code="content_source_unavailable",
                content_status_message="No raw export content is registered for this file entry.",
                warnings=(
                    ExportWarning(
                        code="content_source_unavailable",
                        message="Filesystem metadata alone is not exportable content.",
                        path=source.file_path,
                        source="export_content_provider",
                    ),
                ),
            ),
            audit_context,
        )

    content_source = _content_source_identity(
        content.provider_name,
        source_kind=content.source_kind,
        read_only=content.read_only,
        synthetic=content.synthetic,
        source_content_size=len(content.data),
        status_code="ok",
        status_message="Export content provider returned raw bytes.",
        parser_name=content.parser_name,
        parser_version=content.parser_version,
    )
    output_created = False
    try:
        destination_dir.mkdir(parents=True, exist_ok=True)
        _write_bytes_exclusive(output_path, content.data)
        output_created = True
        hashes, bytes_written, verification_status, verification_warnings = (
            _verify_exported_output(output_path, expected_byte_count=len(content.data))
        )
        status_code = verification_status.code
        status_message = verification_status.message
        result = _result(
            status_code=status_code,
            status_message=status_message,
            source=source,
            provider=export_provider,
            content_source=content_source,
            destination_directory=str(destination_dir),
            requested_output_path=str(output_path),
            output_path=str(output_path),
            manifest_path=str(manifest_path),
            bytes_requested=len(content.data),
            bytes_written=bytes_written,
            hashes=hashes,
            destination_status=ExportStatus(
                code="ok",
                message="Destination safety checks passed.",
            ),
            warnings=content.warnings + verification_warnings,
        )
        manifest_json = json.dumps(result.to_manifest().to_dict(), indent=2, sort_keys=True)
        _write_text_exclusive(manifest_path, manifest_json)
    except FileExistsError as error:
        if output_created:
            _cleanup_written_output(output_path)
        existing_path = Path(error.filename) if error.filename else output_path
        return _finalize_result(
            _result(
                status_code="output_exists",
                status_message="Output file or manifest already exists.",
                source=source,
                provider=export_provider,
                content_source=content_source,
                destination_directory=str(destination_dir),
                requested_output_path=str(output_path),
                output_path=str(output_path),
                manifest_path=str(manifest_path),
                warnings=(
                    ExportWarning(
                        code="output_exists",
                        message="Refusing to overwrite an existing output or manifest file.",
                        path=str(existing_path),
                        source="file_export",
                    ),
                ),
            ),
            audit_context,
        )
    except OSError as error:
        _cleanup_partial_artifacts(output_path, manifest_path)
        return _finalize_result(
            _result(
                status_code="export_write_failed",
                status_message=f"Export write failed: {error}",
                source=source,
                provider=export_provider,
                content_source=content_source,
                destination_directory=str(destination_dir),
                requested_output_path=str(output_path),
                output_path=str(output_path),
                manifest_path=str(manifest_path),
                warnings=(
                    ExportWarning(
                        code="export_write_failed",
                        message="Output or manifest write failed.",
                        path=str(output_path),
                        source="file_export",
                    ),
                ),
            ),
            audit_context,
        )

    return _finalize_result(result, audit_context)


def export_file_to_json(
    file_entry_or_request: Mapping[str, object] | ExportRequest,
    output_directory: str | Path | None = None,
    *,
    provider: ExportContentProvider | None = None,
    output_name: str | None = None,
    audit_context: ExportAuditContext | None = None,
    indent: int | None = 2,
) -> str:
    """Run export and serialize the result as stable JSON."""

    return export_result_to_json(
        export_file(
            file_entry_or_request,
            output_directory,
            provider=provider,
            output_name=output_name,
            audit_context=audit_context,
        ),
        indent=indent,
    )


def _source_from_input(
    file_entry_or_request: Mapping[str, object] | ExportRequest,
) -> ExportSourceProvenance:
    if isinstance(file_entry_or_request, ExportRequest):
        return file_entry_or_request.source

    return ExportSourceProvenance.from_file_entry(file_entry_or_request)


def _requested_output_directory(
    file_entry_or_request: Mapping[str, object] | ExportRequest,
    output_directory: str | Path | None,
) -> str | Path | None:
    if output_directory is not None:
        return output_directory
    if isinstance(file_entry_or_request, ExportRequest):
        return file_entry_or_request.destination_directory
    return None


def _requested_output_path(
    file_entry_or_request: Mapping[str, object] | ExportRequest,
) -> str | None:
    if isinstance(file_entry_or_request, ExportRequest):
        return file_entry_or_request.requested_output_path
    return None


def _destination_status(
    source: ExportSourceProvenance,
    destination_dir: Path,
) -> ExportStatus | None:
    source_path = _path_str(source.source_path)
    if not source_path:
        return None

    evidence_path = Path(source_path).expanduser().resolve(strict=False)
    evidence_root = evidence_path if evidence_path.is_dir() else evidence_path.parent
    if _same_or_nested(destination_dir, evidence_root) or _same_or_nested(
        evidence_root,
        destination_dir,
    ):
        return ExportStatus(
            code="unsafe_destination",
            message="Output directory overlaps the known source/evidence path.",
        )

    return None


def _same_or_nested(candidate: Path, root: Path) -> bool:
    try:
        candidate.relative_to(root)
    except ValueError:
        return False
    return True


def _safe_output_name(value: str | None) -> str | None:
    if value is None:
        return None

    name = value.strip()
    if not name or name in {".", ".."}:
        return None
    if any(separator in name for separator in ("/", "\\")):
        return None
    if any(part in {"", ".", ".."} for part in Path(name).parts):
        return None
    if any(character in name for character in '<>:"|?*'):
        return None
    if Path(name).name != name:
        return None

    return name


def _write_bytes_exclusive(path: Path, data: bytes) -> None:
    with path.open("xb") as output:
        output.write(data)


def _write_text_exclusive(path: Path, text: str) -> None:
    with path.open("x", encoding="utf-8") as output:
        output.write(text)


def _verify_exported_output(
    output_path: Path,
    *,
    expected_byte_count: int | None,
) -> tuple[ExportHashSummary, int | None, ExportStatus, tuple[ExportWarning, ...]]:
    sha256 = hashlib.sha256()
    bytes_written = 0

    try:
        with output_path.open("rb") as output:
            while True:
                chunk = output.read(1024 * 1024)
                if not chunk:
                    break
                bytes_written += len(chunk)
                sha256.update(chunk)
    except OSError as error:
        status = ExportStatus(
            code="export_verification_failed",
            message=f"Exported output could not be verified after writing: {error}",
        )
        return (
            ExportHashSummary(
                sha256=None,
                status=ExportStatus(
                    code="hash_failed",
                    message="SHA-256 could not be computed from the written output.",
                ),
            ),
            None,
            status,
            (
                ExportWarning(
                    code=status.code,
                    message=status.message,
                    path=str(output_path),
                    source="export_verification",
                ),
            ),
        )

    hash_summary = ExportHashSummary(
        sha256=sha256.hexdigest(),
        status=ExportStatus(
            code="ok",
            message="SHA-256 was computed from the written output.",
        ),
    )
    if expected_byte_count is not None and bytes_written != expected_byte_count:
        status = ExportStatus(
            code="byte_count_mismatch",
            message=(
                "Written output byte count does not match the export provider byte count."
            ),
        )
        return (
            hash_summary,
            bytes_written,
            status,
            (
                ExportWarning(
                    code=status.code,
                    message=(
                        f"Expected {expected_byte_count} bytes but wrote {bytes_written} bytes."
                    ),
                    path=str(output_path),
                    source="export_verification",
                ),
            ),
        )

    return (
        hash_summary,
        bytes_written,
        ExportStatus(
            code="ok",
            message="Export file, manifest, SHA-256, and byte count were verified.",
        ),
        (),
    )


def _cleanup_written_output(path: Path) -> None:
    try:
        path.unlink()
    except OSError:
        pass


def _cleanup_partial_artifacts(*paths: Path) -> None:
    for path in paths:
        _cleanup_written_output(path)


def _finalize_result(
    result: ExportResult,
    audit_context: ExportAuditContext | None,
) -> ExportResult:
    if audit_context is None:
        return result
    if not result.status.ok and not audit_context.audit_failed_exports:
        return result

    insert_audit_event(
        audit_context.connection,
        case_id=audit_context.case_id,
        evidence_id=audit_context.evidence_id,
        action="file_export",
        actor=audit_context.actor,
        details=_export_audit_details(result, audit_context),
    )
    return result


def _export_audit_details(
    result: ExportResult,
    audit_context: ExportAuditContext,
) -> dict[str, object]:
    return {
        "schema_version": EXPORT_AUDIT_DETAILS_SCHEMA_VERSION,
        "action": "file_export",
        "status": result.status.to_dict(),
        "source_path": result.source.source_path,
        "source_file_id": result.source.file_id,
        "source_file_path": result.source.file_path,
        "source_file_name": result.source.file_name,
        "source_case_id": result.source.case_id,
        "source_evidence_id": result.source.evidence_id,
        "volume_id": result.source.volume_id,
        "audit_context": {
            "case_id": audit_context.case_id,
            "evidence_id": audit_context.evidence_id,
            "actor": audit_context.actor,
            "audit_failed_exports": audit_context.audit_failed_exports,
        },
        "destination_directory": result.destination_directory,
        "requested_output_path": result.requested_output_path,
        "output_path": result.output_path,
        "manifest_path": result.manifest_path,
        "bytes_requested": result.bytes_requested,
        "bytes_written": result.bytes_written,
        "hashes": result.hashes.to_dict(),
        "destination_status": result.destination_status.to_dict(),
        "content_source": result.content_source.to_dict(),
        "warnings": [warning.to_dict() for warning in result.warnings],
    }


def _result(
    *,
    status_code: str,
    status_message: str,
    source: ExportSourceProvenance,
    provider: ExportContentProvider,
    content_source: ExportContentSourceIdentity | None = None,
    destination_directory: str | None = None,
    requested_output_path: str | None = None,
    output_path: str | None = None,
    manifest_path: str | None = None,
    bytes_requested: int | None = None,
    bytes_written: int | None = None,
    hashes: ExportHashSummary | None = None,
    destination_status: ExportStatus | None = None,
    content_status_code: str = "export_not_started",
    content_status_message: str = "Export content source has not been read.",
    warnings: tuple[ExportWarning, ...] = (),
) -> ExportResult:
    return ExportResult(
        status=ExportStatus(code=status_code, message=status_message),
        source=source,
        content_source=content_source
        or _content_source_identity(
            provider.name,
            source_kind=provider.source_kind,
            read_only=provider.read_only and source.read_only,
            synthetic=provider.synthetic,
            source_content_size=None,
            status_code=content_status_code,
            status_message=content_status_message,
            parser_name=source.adapter_name,
        ),
        destination_directory=destination_directory,
        requested_output_path=requested_output_path,
        output_path=output_path,
        manifest_path=manifest_path,
        bytes_requested=bytes_requested,
        bytes_written=bytes_written,
        hashes=hashes or ExportHashSummary(),
        destination_status=destination_status
        or ExportStatus(
            code="destination_not_checked",
            message="Destination safety has not been evaluated.",
        ),
        source_read_only=None,
        warnings=warnings,
    )


def _content_source_identity(
    provider_name: str,
    *,
    source_kind: str,
    read_only: bool,
    synthetic: bool,
    source_content_size: int | None,
    status_code: str,
    status_message: str,
    parser_name: str | None = None,
    parser_version: str | None = None,
) -> ExportContentSourceIdentity:
    return ExportContentSourceIdentity(
        provider_name=provider_name,
        source_kind=source_kind,
        read_only=read_only,
        synthetic=synthetic,
        source_content_size=source_content_size,
        status=ExportStatus(code=status_code, message=status_message),
        parser_name=parser_name,
        parser_version=parser_version,
    )


def _path_str(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None
