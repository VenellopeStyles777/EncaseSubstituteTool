"""Tests for the S3-T01 export result and manifest contracts."""

import json
import re

from app.backend.forensic_core import (
    EXPORT_MANIFEST_SCHEMA_VERSION,
    ExportContentSourceIdentity,
    ExportHashSummary,
    ExportManifest,
    ExportRequest,
    ExportResult,
    ExportSourceProvenance,
    ExportStatus,
    ExportWarning,
    export_manifest_to_json,
    export_result_to_json,
    utc_now,
)


FIXED_TIME = "2026-07-13T10:00:00Z"


def _stage2_file_entry() -> dict[str, object]:
    return {
        "file_id": "stub-file-hello",
        "path": "/hello.txt",
        "name": "hello.txt",
        "entry_type": "file",
        "size": 13,
        "allocated": True,
        "deleted": False,
        "source_path": "C:/fixtures/tiny.raw",
        "volume_id": "volume-0",
        "volume_offset": 0,
        "volume_length": 1024,
        "filesystem_type": "stubfs",
        "adapter_name": "stub-filesystem-adapter",
        "read_only": True,
        "timestamps": {
            "created": None,
            "modified": None,
            "accessed": None,
            "metadata_changed": None,
        },
    }


def _source() -> ExportSourceProvenance:
    return ExportSourceProvenance.from_file_entry(
        _stage2_file_entry(),
        evidence_id="evidence-test",
        case_id="case-test",
    )


def _content_source() -> ExportContentSourceIdentity:
    return ExportContentSourceIdentity(
        provider_name="stub-export-provider",
        source_kind="stub",
        read_only=True,
        synthetic=True,
        source_content_size=13,
        status=ExportStatus(
            code="export_not_started",
            message="Provider bytes are identified but no export was attempted.",
        ),
        parser_name="stub-filesystem-adapter",
    )


def test_status_ok_property_and_warning_serialization():
    ok_status = ExportStatus(code="ok", message="Reserved success status.")
    blocked_status = ExportStatus(
        code="content_source_unavailable",
        message="No explicit export content source is available.",
    )
    warning = ExportWarning(
        code="stub_export_content",
        message="Export source would be synthetic stub/provider content.",
        path="/hello.txt",
        source="export_contract",
    )

    assert ok_status.ok is True
    assert ok_status.to_dict()["ok"] is True
    assert blocked_status.ok is False
    assert warning.to_dict() == {
        "code": "stub_export_content",
        "message": "Export source would be synthetic stub/provider content.",
        "path": "/hello.txt",
        "source": "export_contract",
    }


def test_source_provenance_preserves_stage2_file_entry_fields():
    source = _source()
    source_dict = source.to_dict()

    assert source_dict["source_path"] == "C:/fixtures/tiny.raw"
    assert source_dict["volume_id"] == "volume-0"
    assert source_dict["volume_offset"] == 0
    assert source_dict["volume_length"] == 1024
    assert source_dict["file_id"] == "stub-file-hello"
    assert source_dict["file_path"] == "/hello.txt"
    assert source_dict["file_name"] == "hello.txt"
    assert source_dict["entry_type"] == "file"
    assert source_dict["filesystem_type"] == "stubfs"
    assert source_dict["adapter_name"] == "stub-filesystem-adapter"
    assert source_dict["read_only"] is True
    assert source_dict["allocated"] is True
    assert source_dict["deleted"] is False
    assert source_dict["evidence_id"] == "evidence-test"
    assert source_dict["case_id"] == "case-test"
    assert set(source_dict["timestamps"]) == {
        "created",
        "modified",
        "accessed",
        "metadata_changed",
    }


def test_request_contract_serializes_destination_and_content_source_placeholders():
    request = ExportRequest(
        source=_source(),
        destination_directory="C:/exports",
        requested_output_path=None,
        export_mode="file",
        content_source=_content_source(),
        examiner_selected_destination=True,
        requested_at=FIXED_TIME,
        warnings=(
            ExportWarning(
                code="destination_not_checked",
                message="Destination safety is deferred until S3-T02.",
                path="C:/exports",
                source="export_contract",
            ),
        ),
    )
    parsed = json.loads(json.dumps(request.to_dict(), sort_keys=True))

    assert parsed["schema_version"] == EXPORT_MANIFEST_SCHEMA_VERSION
    assert parsed["destination_directory"] == "C:/exports"
    assert parsed["requested_output_path"] is None
    assert parsed["examiner_selected_destination"] is True
    assert parsed["destination_status"]["code"] == "destination_not_checked"
    assert parsed["content_source"]["provider_name"] == "stub-export-provider"
    assert parsed["content_source"]["synthetic"] is True
    assert parsed["warnings"][0]["code"] == "destination_not_checked"


def test_export_result_serializes_not_started_placeholders_without_written_paths():
    result = ExportResult(
        status=ExportStatus(
            code="export_not_started",
            message="S3-T01 defines the contract before export writes exist.",
        ),
        source=_source(),
        content_source=_content_source(),
        destination_directory="C:/exports",
        requested_output_path="C:/exports/hello.txt",
        output_path=None,
        manifest_path=None,
        bytes_requested=None,
        bytes_written=None,
        hashes=ExportHashSummary(),
        created_at=FIXED_TIME,
        warnings=(
            ExportWarning(
                code="hash_not_computed",
                message="Hashing is deferred until S3-T03.",
                source="export_contract",
            ),
        ),
    )
    parsed = json.loads(export_result_to_json(result))

    assert parsed["schema_version"] == EXPORT_MANIFEST_SCHEMA_VERSION
    assert parsed["status"]["code"] == "export_not_started"
    assert parsed["status"]["ok"] is False
    assert parsed["output_path"] is None
    assert parsed["manifest_path"] is None
    assert parsed["bytes_requested"] is None
    assert parsed["bytes_written"] is None
    assert parsed["hashes"]["sha256"] is None
    assert parsed["hashes"]["status"]["code"] == "hash_not_computed"
    assert parsed["source"]["file_id"] == "stub-file-hello"
    assert parsed["content_source"]["source_kind"] == "stub"
    assert parsed["content_source"]["synthetic"] is True
    assert parsed["destination_status"]["code"] == "destination_not_checked"
    assert parsed["manifest"]["output_path"] is None
    assert parsed["warnings"][0]["code"] == "hash_not_computed"


def test_manifest_serializes_content_source_unavailable_status():
    manifest = ExportManifest(
        status=ExportStatus(
            code="content_source_unavailable",
            message="No explicit raw export content source is available.",
        ),
        source=_source(),
        content_source=ExportContentSourceIdentity(
            provider_name="missing-export-provider",
            source_kind="provider",
            read_only=True,
            synthetic=False,
            source_content_size=None,
            status=ExportStatus(
                code="content_source_unavailable",
                message="No provider bytes were available.",
            ),
        ),
        created_at=FIXED_TIME,
        warnings=(
            ExportWarning(
                code="content_source_unavailable",
                message="Filesystem metadata alone is not exportable content.",
                path="/hello.txt",
                source="content_source",
            ),
        ),
    )
    parsed = json.loads(export_manifest_to_json(manifest))

    assert parsed["status"]["code"] == "content_source_unavailable"
    assert parsed["status"]["ok"] is False
    assert parsed["content_source"]["status"]["code"] == "content_source_unavailable"
    assert parsed["content_source"]["source_content_size"] is None
    assert parsed["content_source"]["synthetic"] is False
    assert parsed["output_path"] is None
    assert parsed["manifest_path"] is None
    assert parsed["bytes_written"] is None
    assert parsed["hashes"]["sha256"] is None
    assert parsed["warnings"][0]["message"] == (
        "Filesystem metadata alone is not exportable content."
    )


def test_source_read_only_serialization_derives_from_source_provenance():
    entry = _stage2_file_entry()
    entry["read_only"] = False
    source = ExportSourceProvenance.from_file_entry(entry)
    status = ExportStatus(
        code="export_not_started",
        message="S3-T01 defines the contract before export writes exist.",
    )

    result = ExportResult(
        status=status,
        source=source,
        content_source=_content_source(),
        created_at=FIXED_TIME,
    )
    manifest = ExportManifest(
        status=status,
        source=source,
        content_source=_content_source(),
        created_at=FIXED_TIME,
    )

    assert result.to_dict()["source"]["read_only"] is False
    assert result.to_dict()["source_read_only"] is False
    assert result.to_dict()["manifest"]["source_read_only"] is False
    assert manifest.to_dict()["source"]["read_only"] is False
    assert manifest.to_dict()["source_read_only"] is False


def test_utc_now_uses_project_utc_z_timestamp_format():
    timestamp = utc_now()

    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", timestamp)
