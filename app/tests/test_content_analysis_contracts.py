"""Tests for the S4-T01 hash/signature analysis contracts."""

import json
import re

from app.backend.forensic_core import (
    CONTENT_ANALYSIS_SCHEMA_VERSION,
    AnalysisContentSourceIdentity,
    AnalysisSourceProvenance,
    AnalysisStatus,
    AnalysisWarning,
    HashAnalysisRequest,
    HashAnalysisResult,
    HashDigestResult,
    SignatureAnalysisRequest,
    SignatureAnalysisResult,
    hash_analysis_request_to_json,
    hash_analysis_result_to_json,
    signature_analysis_request_to_json,
    signature_analysis_result_to_json,
)
from app.backend.forensic_core.content_analysis import utc_now


FIXED_TIME = "2026-07-14T10:00:00Z"


def _stage2_file_entry(**overrides: object) -> dict[str, object]:
    entry: dict[str, object] = {
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
    entry.update(overrides)
    return entry


def _source() -> AnalysisSourceProvenance:
    return AnalysisSourceProvenance.from_file_entry(
        _stage2_file_entry(),
        case_id="case-test",
        evidence_id="evidence-test",
    )


def _content_source() -> AnalysisContentSourceIdentity:
    return AnalysisContentSourceIdentity(
        provider_name="stub-analysis-provider",
        source_kind="synthetic",
        read_only=True,
        synthetic=True,
        generated=False,
        source_content_size=13,
        status=AnalysisStatus(
            code="analysis_not_started",
            message="Provider bytes are identified but analysis has not started.",
        ),
        parser_name="stub-filesystem-adapter",
    )


def test_status_ok_property_and_warning_serialization():
    ok_status = AnalysisStatus(code="ok", message="Reserved success status.")
    blocked_status = AnalysisStatus(
        code="metadata_only_source",
        message="Filesystem metadata alone is not analysis content.",
    )
    warning = AnalysisWarning(
        code="preview_rendering_not_allowed",
        message="Rendered preview text or hex is not source content.",
        path="/hello.txt",
        source="content_analysis_contract",
    )

    assert ok_status.ok is True
    assert ok_status.to_dict()["ok"] is True
    assert blocked_status.ok is False
    assert warning.to_dict() == {
        "code": "preview_rendering_not_allowed",
        "message": "Rendered preview text or hex is not source content.",
        "path": "/hello.txt",
        "source": "content_analysis_contract",
    }


def test_source_provenance_preserves_stage2_file_entry_without_mutation():
    entry = _stage2_file_entry(case_id="entry-case", evidence_id="entry-evidence")
    before = json.loads(json.dumps(entry, sort_keys=True))

    source = AnalysisSourceProvenance.from_file_entry(entry)
    source_dict = source.to_dict()

    assert entry == before
    assert source_dict["source_path"] == "C:/fixtures/tiny.raw"
    assert source_dict["case_id"] == "entry-case"
    assert source_dict["evidence_id"] == "entry-evidence"
    assert source_dict["volume_id"] == "volume-0"
    assert source_dict["volume_offset"] == 0
    assert source_dict["volume_length"] == 1024
    assert source_dict["file_id"] == "stub-file-hello"
    assert source_dict["file_path"] == "/hello.txt"
    assert source_dict["file_name"] == "hello.txt"
    assert source_dict["entry_type"] == "file"
    assert source_dict["allocated"] is True
    assert source_dict["deleted"] is False
    assert source_dict["filesystem_type"] == "stubfs"
    assert source_dict["adapter_name"] == "stub-filesystem-adapter"
    assert source_dict["read_only"] is True
    assert set(source_dict["timestamps"]) == {
        "created",
        "modified",
        "accessed",
        "metadata_changed",
    }


def test_source_provenance_explicit_ids_override_entry_ids():
    source = AnalysisSourceProvenance.from_file_entry(
        _stage2_file_entry(case_id="entry-case", evidence_id="entry-evidence"),
        case_id="explicit-case",
        evidence_id="explicit-evidence",
    )

    assert source.case_id == "explicit-case"
    assert source.evidence_id == "explicit-evidence"


def test_content_source_identity_labels_synthetic_generated_and_future_real_sources():
    synthetic_source = _content_source()
    generated_source = AnalysisContentSourceIdentity(
        provider_name="generated-fixture-provider",
        source_kind="generated_fixture",
        read_only=True,
        synthetic=False,
        generated=True,
        source_content_size=32,
        status=AnalysisStatus(
            code="analysis_not_started",
            message="Generated fixture bytes are available for later analysis.",
        ),
        source_name="tiny-generated.bin",
        source_version="fixture-v1",
    )
    real_parser_source = AnalysisContentSourceIdentity(
        provider_name="future-real-parser-provider",
        source_kind="real_parser",
        read_only=True,
        synthetic=False,
        generated=False,
        source_content_size=None,
        status=AnalysisStatus(
            code="content_source_unavailable",
            message="Real parser bytes are not available in the current implementation.",
        ),
        parser_name="future-parser",
        parser_version="0.0",
    )

    assert synthetic_source.to_dict()["synthetic"] is True
    assert synthetic_source.to_dict()["generated"] is False
    assert generated_source.to_dict()["source_kind"] == "generated_fixture"
    assert generated_source.to_dict()["generated"] is True
    assert generated_source.to_dict()["source_name"] == "tiny-generated.bin"
    assert real_parser_source.to_dict()["source_kind"] == "real_parser"
    assert real_parser_source.to_dict()["synthetic"] is False
    assert real_parser_source.to_dict()["status"]["code"] == "content_source_unavailable"


def test_hash_request_and_result_placeholders_are_json_serializable():
    request = HashAnalysisRequest(
        source=_source(),
        content_source=_content_source(),
        requested_algorithms=("sha256", "md5"),
        requested_at=FIXED_TIME,
        warnings=(
            AnalysisWarning(
                code="synthetic_content",
                message="Requested content is synthetic and not parsed evidence bytes.",
                path="/hello.txt",
                source="analysis_content_provider",
            ),
        ),
    )
    result = HashAnalysisResult(
        source=_source(),
        content_source=_content_source(),
        requested_algorithms=("sha256", "md5"),
        digests=(
            HashDigestResult(algorithm="sha256"),
            HashDigestResult(algorithm="md5"),
        ),
        created_at=FIXED_TIME,
        warnings=request.warnings,
    )

    request_dict = json.loads(hash_analysis_request_to_json(request))
    result_dict = json.loads(hash_analysis_result_to_json(result))

    assert request_dict["schema_version"] == CONTENT_ANALYSIS_SCHEMA_VERSION
    assert request_dict["analysis_type"] == "hash"
    assert request_dict["requested_algorithms"] == ["sha256", "md5"]
    assert request_dict["content_source"]["provider_name"] == "stub-analysis-provider"
    assert request_dict["warnings"][0]["code"] == "synthetic_content"
    assert result_dict["status"]["code"] == "analysis_not_started"
    assert result_dict["bytes_analyzed"] is None
    assert result_dict["digests"][0]["algorithm"] == "sha256"
    assert result_dict["digests"][0]["digest"] is None
    assert result_dict["digests"][0]["status"]["code"] == "hash_not_computed"
    assert result_dict["digests"][1]["digest"] is None
    assert result_dict["completed_at"] is None
    _assert_json_safe(result.to_dict())


def test_signature_request_and_result_placeholders_are_json_serializable():
    request = SignatureAnalysisRequest(
        source=_source(),
        content_source=_content_source(),
        max_bytes_requested=16,
        requested_at=FIXED_TIME,
    )
    result = SignatureAnalysisResult(
        source=_source(),
        content_source=_content_source(),
        max_bytes_requested=16,
        created_at=FIXED_TIME,
        warnings=(
            AnalysisWarning(
                code="signature_not_checked",
                message="Signature detection is deferred beyond S4-T01.",
                path="/hello.txt",
                source="content_analysis_contract",
            ),
        ),
    )

    request_dict = json.loads(signature_analysis_request_to_json(request))
    result_dict = json.loads(signature_analysis_result_to_json(result))

    assert request_dict["schema_version"] == CONTENT_ANALYSIS_SCHEMA_VERSION
    assert request_dict["analysis_type"] == "signature"
    assert request_dict["max_bytes_requested"] == 16
    assert result_dict["status"]["code"] == "signature_not_checked"
    assert result_dict["bytes_inspected"] is None
    assert result_dict["detected_type"] is None
    assert result_dict["detected_signature"] is None
    assert result_dict["detected_mime_type"] is None
    assert result_dict["warnings"][0]["code"] == "signature_not_checked"
    _assert_json_safe(result.to_dict())


def test_utc_now_uses_project_utc_z_timestamp_format():
    timestamp = utc_now()

    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", timestamp)


def _assert_json_safe(value: object) -> None:
    json.dumps(value, sort_keys=True)
    _assert_no_bytes(value)


def _assert_no_bytes(value: object) -> None:
    if isinstance(value, bytes):
        raise AssertionError("bytes object found in JSON contract output")
    if isinstance(value, dict):
        for item in value.values():
            _assert_no_bytes(item)
    elif isinstance(value, list):
        for item in value:
            _assert_no_bytes(item)
