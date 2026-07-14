"""Tests for S4-T03 provider-backed file signature detection."""

import hashlib
import json

from app.backend.forensic_core import (
    AnalysisContentProvider,
    AnalysisContentSourceIdentity,
    AnalysisSourceProvenance,
    AnalysisStatus,
    SignatureAnalysisRequest,
    StubAnalysisContentProvider,
    analyze_file_signature,
    detect_file_signature,
    hash_file_content,
    signature_analysis_result_to_json,
)


def _stage2_file_entry(**overrides: object) -> dict[str, object]:
    entry: dict[str, object] = {
        "file_id": "stub-file-signature",
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


class CountingAnalysisProvider(StubAnalysisContentProvider):
    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self.read_count = 0

    def get_content(self, source: AnalysisSourceProvenance):
        self.read_count += 1
        return super().get_content(source)


class ExplodingAnalysisProvider:
    name = "exploding-signature-provider"
    source_kind = "synthetic"
    read_only = True
    synthetic = True
    generated = False

    def get_content(self, source: AnalysisSourceProvenance):
        raise RuntimeError("signature provider failed")


def _provider_for(data: bytes, **kwargs: object) -> StubAnalysisContentProvider:
    return StubAnalysisContentProvider(
        {"stub-file-signature": data},
        **kwargs,
    )


def test_known_file_signatures_are_detected_from_provider_bytes():
    examples = (
        (b"%PDF-1.7\n", "pdf", "pdf_header", "application/pdf"),
        (b"\x89PNG\r\n\x1a\nrest", "png", "png_header", "image/png"),
        (b"\xff\xd8\xff\xe0rest", "jpeg", "jpeg_soi", "image/jpeg"),
        (b"GIF87arest", "gif", "gif87a_header", "image/gif"),
        (b"GIF89arest", "gif", "gif89a_header", "image/gif"),
        (b"PK\x03\x04rest", "zip", "zip_local_file_header", "application/zip"),
        (b"PK\x05\x06rest", "zip", "zip_empty_archive", "application/zip"),
        (b"PK\x07\x08rest", "zip", "zip_spanned_archive_marker", "application/zip"),
        (b"\x7fELFrest", "elf", "elf_header", "application/x-elf"),
        (
            b"MZrest",
            "mz_executable_candidate",
            "mz_header_candidate",
            "application/x-msdownload",
        ),
    )

    for data, detected_type, signature, mime_type in examples:
        result = detect_file_signature(
            _stage2_file_entry(size=len(data)),
            provider=_provider_for(data),
            max_bytes=16,
        )

        assert result.status.code == "ok"
        assert result.detected_type == detected_type
        assert result.detected_signature == signature
        assert result.detected_mime_type == mime_type
        assert result.bytes_inspected == len(data)
        assert result.content_source.provider_name == "stub-analysis-provider"
        assert result.content_source.source_kind == "synthetic"
        assert result.content_source.synthetic is True
        assert result.content_source.source_content_size == len(data)
        assert result.warnings[0].code == "synthetic_content"
        _assert_json_safe(result.to_dict())


def test_unknown_signature_returns_structured_non_ok_result():
    result = detect_file_signature(
        _stage2_file_entry(),
        provider=_provider_for(b"plain text bytes"),
        max_bytes=16,
    )
    parsed = json.loads(signature_analysis_result_to_json(result))

    assert result.status.code == "unknown_signature"
    assert result.status.ok is False
    assert result.bytes_inspected == 16
    assert result.detected_type is None
    assert result.detected_signature is None
    assert result.detected_mime_type is None
    assert result.warnings[-1].code == "unknown_signature"
    assert parsed["status"]["code"] == "unknown_signature"
    _assert_json_safe(result.to_dict())


def test_insufficient_partial_known_signature_bytes_are_not_guessed():
    result = detect_file_signature(
        _stage2_file_entry(),
        provider=_provider_for(b"%PDF-1.7"),
        max_bytes=4,
    )

    assert result.status.code == "insufficient_signature_bytes"
    assert result.bytes_inspected == 4
    assert result.detected_type is None
    assert result.detected_signature is None
    assert result.warnings[-1].code == "insufficient_signature_bytes"


def test_bounded_inspection_does_not_match_beyond_requested_prefix():
    insufficient_result = detect_file_signature(
        _stage2_file_entry(),
        provider=_provider_for(b"%PDF-1.7"),
        max_bytes=4,
    )
    detected_result = detect_file_signature(
        _stage2_file_entry(),
        provider=_provider_for(b"%PDF-1.7"),
        max_bytes=5,
    )

    assert insufficient_result.status.code == "insufficient_signature_bytes"
    assert insufficient_result.bytes_inspected == 4
    assert detected_result.status.code == "ok"
    assert detected_result.bytes_inspected == 5
    assert detected_result.detected_signature == "pdf_header"


def test_invalid_max_byte_request_is_rejected_before_provider_read():
    for invalid_max_bytes in (0, -1, True, 1.5, "8", "not-an-int"):
        provider = CountingAnalysisProvider(
            {"stub-file-signature": b"%PDF-1.7"}
        )

        result = detect_file_signature(
            _stage2_file_entry(),
            provider=provider,
            max_bytes=invalid_max_bytes,
        )

        assert provider.read_count == 0
        assert result.status.code == "invalid_analysis_request"
        assert result.bytes_inspected is None


def test_missing_provider_content_returns_structured_unavailable_result():
    provider = CountingAnalysisProvider({"other-file": b"%PDF-1.7"})

    result = detect_file_signature(
        _stage2_file_entry(file_id="missing-file", path="/missing.bin"),
        provider=provider,
    )

    assert provider.read_count == 1
    assert result.status.code == "content_source_unavailable"
    assert result.content_source.status.code == "content_source_unavailable"
    assert result.bytes_inspected is None
    assert result.detected_type is None
    assert result.warnings[0].code == "content_source_unavailable"


def test_directory_entry_returns_path_not_file_before_provider_read():
    provider = CountingAnalysisProvider({"stub-dir-documents": b"%PDF-1.7"})

    result = detect_file_signature(
        _stage2_file_entry(
            file_id="stub-dir-documents",
            path="/Documents",
            name="Documents",
            entry_type="directory",
            size=0,
        ),
        provider=provider,
    )

    assert provider.read_count == 0
    assert result.status.code == "path_not_file"
    assert result.bytes_inspected is None
    assert result.detected_signature is None
    assert result.warnings[0].code == "path_not_file"


def test_metadata_only_source_without_provider_is_not_inspected():
    result = detect_file_signature(_stage2_file_entry(), provider=None)

    assert result.status.code == "metadata_only_source"
    assert result.content_source.source_kind == "metadata_only"
    assert result.content_source.status.code == "metadata_only_source"
    assert result.bytes_inspected is None
    assert result.detected_type is None
    assert result.warnings[0].code == "metadata_only_source"


def test_provider_exception_returns_structured_error_without_traceback():
    provider: AnalysisContentProvider = ExplodingAnalysisProvider()

    result = detect_file_signature(_stage2_file_entry(), provider=provider)

    assert result.status.code == "content_provider_error"
    assert result.status.ok is False
    assert "Traceback" not in result.status.message
    assert "RuntimeError" in result.status.message
    assert result.content_source.status.code == "content_provider_error"
    assert result.bytes_inspected is None
    assert result.detected_type is None
    assert result.warnings[0].code == "content_provider_error"


def test_signature_request_preserves_provenance_and_generated_labels():
    source = AnalysisSourceProvenance.from_file_entry(
        _stage2_file_entry(case_id="entry-case", evidence_id="entry-evidence"),
        case_id="case-test",
        evidence_id="evidence-test",
    )
    request = SignatureAnalysisRequest(
        source=source,
        max_bytes_requested=8,
        content_source=AnalysisContentSourceIdentity(
            provider_name="planned-generated-provider",
            source_kind="generated_fixture",
            read_only=True,
            generated=True,
            status=AnalysisStatus(
                code="analysis_not_started",
                message="Generated fixture source has not been read.",
            ),
        ),
    )
    provider = _provider_for(
        b"\x89PNG\r\n\x1a\npayload",
        source_kind="generated_fixture",
        synthetic=False,
        generated=True,
        source_name="tiny-generated.png",
        source_version="fixture-v1",
    )

    result = analyze_file_signature(request, provider=provider)

    assert result.status.code == "ok"
    assert result.max_bytes_requested == 8
    assert result.bytes_inspected == 8
    assert result.source.case_id == "case-test"
    assert result.source.evidence_id == "evidence-test"
    assert result.content_source.source_kind == "generated_fixture"
    assert result.content_source.synthetic is False
    assert result.content_source.generated is True
    assert result.content_source.source_name == "tiny-generated.png"
    assert result.content_source.source_version == "fixture-v1"
    assert result.detected_type == "png"
    assert result.warnings[0].code == "generated_fixture_content"
    _assert_json_safe(result.to_dict())


def test_s4_t02_hash_behavior_still_uses_provider_bytes():
    result = hash_file_content(
        _stage2_file_entry(),
        provider=_provider_for(b"%PDF-1.7"),
    )

    assert result.status.code == "ok"
    assert result.digests[0].algorithm == "sha256"
    assert result.digests[0].digest == hashlib.sha256(b"%PDF-1.7").hexdigest()


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
