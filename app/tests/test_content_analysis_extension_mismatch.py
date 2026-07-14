"""Tests for S4-T04 extension/signature mismatch evaluation."""

import hashlib
from inspect import signature
import json

from app.backend.forensic_core import (
    AnalysisContentSourceIdentity,
    AnalysisSourceProvenance,
    AnalysisStatus,
    AnalysisWarning,
    SignatureAnalysisResult,
    StubAnalysisContentProvider,
    check_extension_mismatch,
    detect_file_signature,
    evaluate_extension_mismatch,
    extension_mismatch_result_to_json,
    hash_file_content,
)


SIGNATURE_FILE_ID = "stub-file-signature"


def _stage2_file_entry(**overrides: object) -> dict[str, object]:
    entry: dict[str, object] = {
        "file_id": SIGNATURE_FILE_ID,
        "path": "/sample.bin",
        "name": "sample.bin",
        "entry_type": "file",
        "size": 16,
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


def _content_source(
    *,
    source_kind: str = "synthetic",
    synthetic: bool = True,
    generated: bool = False,
) -> AnalysisContentSourceIdentity:
    return AnalysisContentSourceIdentity(
        provider_name="stub-analysis-provider",
        source_kind=source_kind,
        read_only=True,
        synthetic=synthetic,
        generated=generated,
        source_content_size=16,
        status=AnalysisStatus(
            code="ok",
            message="Analysis content provider returned raw bytes.",
        ),
        parser_name="stub-filesystem-adapter",
    )


def _signature_result(
    *,
    name: str | None = "sample.bin",
    path: str | None = "/sample.bin",
    entry_type: str = "file",
    status_code: str = "ok",
    detected_type: str | None = "pdf",
    detected_signature: str | None = "pdf_header",
    detected_mime_type: str | None = "application/pdf",
    content_source: AnalysisContentSourceIdentity | None = None,
    warnings: tuple[AnalysisWarning, ...] = (),
) -> SignatureAnalysisResult:
    source = AnalysisSourceProvenance.from_file_entry(
        _stage2_file_entry(name=name, path=path, entry_type=entry_type),
        case_id="case-test",
        evidence_id="evidence-test",
    )
    status = AnalysisStatus(
        code=status_code,
        message=(
            "File signature detected from explicit analysis provider bytes."
            if status_code == "ok"
            else "Signature detection did not produce a supported result."
        ),
    )
    return SignatureAnalysisResult(
        source=source,
        content_source=content_source or _content_source(),
        max_bytes_requested=16,
        status=status,
        bytes_inspected=16 if status_code == "ok" else None,
        detected_type=detected_type,
        detected_signature=detected_signature,
        detected_mime_type=detected_mime_type,
        created_at="2026-07-14T10:00:00Z",
        completed_at="2026-07-14T10:00:01Z",
        warnings=warnings,
    )


def _provider_for(data: bytes) -> StubAnalysisContentProvider:
    return StubAnalysisContentProvider({SIGNATURE_FILE_ID: data})


def test_evaluator_consumes_signature_result_without_provider_parameter():
    parameters = signature(evaluate_extension_mismatch).parameters

    assert tuple(parameters) == ("signature_result",)


def test_pdf_extension_matches_case_insensitively():
    result = evaluate_extension_mismatch(
        _signature_result(name="REPORT.PDF", path="/REPORT.PDF")
    )

    assert result.status.code == "extension_match"
    assert result.status.ok is True
    assert result.mismatch is False
    assert result.observed_extension == ".pdf"
    assert result.expected_extensions == (".pdf",)
    assert result.source.file_name == "REPORT.PDF"
    assert result.content_source.provider_name == "stub-analysis-provider"
    _assert_json_safe(result.to_dict())


def test_pdf_signature_with_txt_extension_is_mismatch():
    result = check_extension_mismatch(
        _signature_result(name="report.txt", path="/report.txt")
    )
    parsed = json.loads(extension_mismatch_result_to_json(result))

    assert result.status.code == "extension_mismatch"
    assert result.status.ok is True
    assert result.mismatch is True
    assert result.observed_extension == ".txt"
    assert result.expected_extensions == (".pdf",)
    assert result.detected_type == "pdf"
    assert result.detected_signature == "pdf_header"
    assert result.detected_mime_type == "application/pdf"
    assert result.warnings[-1].code == "extension_mismatch"
    assert parsed["mismatch"] is True
    assert parsed["status"]["ok"] is True
    _assert_json_safe(result.to_dict())


def test_jpeg_extension_variants_match():
    for extension in (".jpg", ".jpeg", ".jpe"):
        result = evaluate_extension_mismatch(
            _signature_result(
                name=f"photo{extension}",
                path=f"/photo{extension}",
                detected_type="jpeg",
                detected_signature="jpeg_soi",
                detected_mime_type="image/jpeg",
            )
        )

        assert result.status.code == "extension_match"
        assert result.mismatch is False
        assert result.observed_extension == extension
        assert result.expected_extensions == (".jpg", ".jpeg", ".jpe")


def test_zip_allow_list_extension_matches_docx():
    result = evaluate_extension_mismatch(
        _signature_result(
            name="document.docx",
            path="/document.docx",
            detected_type="zip",
            detected_signature="zip_local_file_header",
            detected_mime_type="application/zip",
        )
    )

    assert result.status.code == "extension_match"
    assert result.mismatch is False
    assert result.observed_extension == ".docx"
    assert ".docx" in result.expected_extensions


def test_mz_executable_candidate_match_and_mismatch():
    exe_result = evaluate_extension_mismatch(
        _signature_result(
            name="program.exe",
            path="/program.exe",
            detected_type="mz_executable_candidate",
            detected_signature="mz_header_candidate",
            detected_mime_type="application/x-msdownload",
        )
    )
    jpg_result = evaluate_extension_mismatch(
        _signature_result(
            name="program.jpg",
            path="/program.jpg",
            detected_type="mz_executable_candidate",
            detected_signature="mz_header_candidate",
            detected_mime_type="application/x-msdownload",
        )
    )

    assert exe_result.status.code == "extension_match"
    assert exe_result.mismatch is False
    assert ".exe" in exe_result.expected_extensions
    assert jpg_result.status.code == "extension_mismatch"
    assert jpg_result.mismatch is True
    assert jpg_result.observed_extension == ".jpg"


def test_file_without_extension_is_not_evaluated_or_mismatched():
    result = evaluate_extension_mismatch(
        _signature_result(name="README", path="/README")
    )

    assert result.status.code == "extension_missing"
    assert result.status.ok is False
    assert result.mismatch is None
    assert result.observed_extension is None
    assert result.expected_extensions == (".pdf",)
    assert result.warnings[-1].code == "extension_missing"


def test_missing_file_name_and_path_metadata_is_not_evaluated():
    result = evaluate_extension_mismatch(_signature_result(name=None, path=None))

    assert result.status.code == "file_name_unavailable"
    assert result.mismatch is None
    assert result.observed_extension is None
    assert result.expected_extensions == (".pdf",)
    assert result.warnings[-1].code == "file_name_unavailable"


def test_non_ok_signature_statuses_are_not_reported_as_mismatches():
    for status_code in ("unknown_signature", "insufficient_signature_bytes"):
        result = evaluate_extension_mismatch(
            _signature_result(
                status_code=status_code,
                detected_type=None,
                detected_signature=None,
                detected_mime_type=None,
            )
        )

        assert result.status.code == "signature_not_available"
        assert result.signature_status.code == status_code
        assert result.mismatch is None
        assert result.expected_extensions == ()
        assert result.warnings[-1].code == "signature_not_available"


def test_unsupported_detected_type_is_not_evaluated():
    result = evaluate_extension_mismatch(
        _signature_result(
            name="archive.rar",
            path="/archive.rar",
            detected_type="rar",
            detected_signature="rar_header",
            detected_mime_type="application/vnd.rar",
        )
    )

    assert result.status.code == "unsupported_signature_type"
    assert result.mismatch is None
    assert result.observed_extension is None
    assert result.expected_extensions == ()
    assert result.warnings[-1].code == "unsupported_signature_type"


def test_directory_source_is_not_evaluated():
    result = evaluate_extension_mismatch(
        _signature_result(
            name="Documents.pdf",
            path="/Documents.pdf",
            entry_type="directory",
        )
    )

    assert result.status.code == "path_not_file"
    assert result.mismatch is None
    assert result.warnings[-1].code == "path_not_file"


def test_provenance_source_identity_signature_warnings_and_timestamps_are_preserved():
    signature_warning = AnalysisWarning(
        code="generated_fixture_content",
        message="Signature bytes are generated fixture content.",
        path="/invoice.txt",
        source="analysis_content_provider",
    )
    result = evaluate_extension_mismatch(
        _signature_result(
            name="invoice.txt",
            path="/invoice.txt",
            content_source=_content_source(
                source_kind="generated_fixture",
                synthetic=False,
                generated=True,
            ),
            warnings=(signature_warning,),
        )
    )

    assert result.status.code == "extension_mismatch"
    assert result.source.case_id == "case-test"
    assert result.source.evidence_id == "evidence-test"
    assert result.content_source.source_kind == "generated_fixture"
    assert result.content_source.generated is True
    assert result.signature_status.code == "ok"
    assert result.signature_created_at == "2026-07-14T10:00:00Z"
    assert result.signature_completed_at == "2026-07-14T10:00:01Z"
    assert result.warnings[0].code == "generated_fixture_content"
    assert result.warnings[-1].code == "extension_mismatch"
    _assert_json_safe(json.loads(extension_mismatch_result_to_json(result)))


def test_signature_and_hash_behaviors_still_use_provider_bytes():
    signature_result = detect_file_signature(
        _stage2_file_entry(name="sample.pdf", path="/sample.pdf"),
        provider=_provider_for(b"%PDF-1.7"),
        max_bytes=5,
    )
    mismatch_result = evaluate_extension_mismatch(signature_result)
    hash_result = hash_file_content(
        _stage2_file_entry(),
        provider=_provider_for(b"%PDF-1.7"),
    )

    assert signature_result.status.code == "ok"
    assert signature_result.detected_type == "pdf"
    assert mismatch_result.status.code == "extension_match"
    assert mismatch_result.mismatch is False
    assert hash_result.status.code == "ok"
    assert hash_result.digests[0].digest == hashlib.sha256(b"%PDF-1.7").hexdigest()


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
