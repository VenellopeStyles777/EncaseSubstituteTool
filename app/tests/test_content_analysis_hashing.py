"""Tests for S4-T02 provider-backed hash analysis."""

import hashlib
import json

from app.backend.forensic_core import (
    AnalysisContentProvider,
    AnalysisContentSourceIdentity,
    AnalysisSourceProvenance,
    AnalysisStatus,
    HashAnalysisRequest,
    StubAnalysisContentProvider,
    calculate_hashes,
    hash_analysis_result_to_json,
    hash_file_content,
)


HELLO_BYTES = b"Hello, world!"


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


class CountingAnalysisProvider(StubAnalysisContentProvider):
    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self.read_count = 0

    def get_content(self, source: AnalysisSourceProvenance):
        self.read_count += 1
        return super().get_content(source)


class ExplodingAnalysisProvider:
    name = "exploding-analysis-provider"
    source_kind = "synthetic"
    read_only = True
    synthetic = True
    generated = False

    def get_content(self, source: AnalysisSourceProvenance):
        raise RuntimeError("provider failed")


def test_default_sha256_is_computed_from_explicit_analysis_provider_bytes():
    provider = StubAnalysisContentProvider()

    result = hash_file_content(_stage2_file_entry(), provider=provider)
    parsed = json.loads(hash_analysis_result_to_json(result))

    assert result.status.code == "ok"
    assert result.bytes_analyzed == len(HELLO_BYTES)
    assert result.requested_algorithms == ("sha256",)
    assert result.digests[0].algorithm == "sha256"
    assert result.digests[0].digest == hashlib.sha256(HELLO_BYTES).hexdigest()
    assert result.digests[0].status.code == "ok"
    assert result.content_source.provider_name == "stub-analysis-provider"
    assert result.content_source.source_kind == "synthetic"
    assert result.content_source.synthetic is True
    assert result.content_source.generated is False
    assert result.content_source.source_content_size == len(HELLO_BYTES)
    assert result.content_source.status.code == "ok"
    assert result.content_source.read_only is True
    assert result.source.file_id == "stub-file-hello"
    assert result.source.file_path == "/hello.txt"
    assert result.source.source_path == "C:/fixtures/tiny.raw"
    assert result.source.read_only is True
    assert result.warnings[0].code == "synthetic_content"
    assert parsed["digests"][0]["digest"] == result.digests[0].digest
    _assert_json_safe(result.to_dict())


def test_md5_and_sha1_are_computed_only_when_explicitly_requested():
    result = calculate_hashes(
        _stage2_file_entry(),
        provider=StubAnalysisContentProvider(),
        algorithms=("md5", "sha1"),
    )

    digest_by_algorithm = {
        digest.algorithm: digest.digest for digest in result.digests
    }

    assert result.status.code == "ok"
    assert result.requested_algorithms == ("md5", "sha1")
    assert set(digest_by_algorithm) == {"md5", "sha1"}
    assert digest_by_algorithm["md5"] == hashlib.md5(HELLO_BYTES).hexdigest()
    assert digest_by_algorithm["sha1"] == hashlib.sha1(HELLO_BYTES).hexdigest()
    assert "sha256" not in digest_by_algorithm


def test_algorithm_names_are_normalized_case_insensitively():
    result = hash_file_content(
        _stage2_file_entry(),
        provider=StubAnalysisContentProvider(),
        algorithms=(" SHA-256 ", "MD5", "Sha_1", "sha256"),
    )

    assert result.status.code == "ok"
    assert result.requested_algorithms == ("sha256", "md5", "sha1")
    assert [digest.algorithm for digest in result.digests] == [
        "sha256",
        "md5",
        "sha1",
    ]


def test_unsupported_algorithm_returns_non_ok_without_provider_read():
    provider = CountingAnalysisProvider()

    result = hash_file_content(
        _stage2_file_entry(),
        provider=provider,
        algorithms=("sha256", "sha512"),
    )

    assert provider.read_count == 0
    assert result.status.code == "unsupported_algorithm"
    assert result.bytes_analyzed is None
    assert result.content_source.status.code == "analysis_not_started"
    assert result.digests[0].digest is None
    assert result.digests[0].status.code == "hash_not_computed"
    assert result.digests[1].algorithm == "sha512"
    assert result.digests[1].status.code == "unsupported_algorithm"
    assert result.warnings[0].code == "unsupported_algorithm"
    _assert_json_safe(result.to_dict())


def test_empty_and_invalid_algorithm_requests_do_not_read_provider_bytes():
    empty_provider = CountingAnalysisProvider()
    invalid_provider = CountingAnalysisProvider()
    bad_type_provider = CountingAnalysisProvider()

    empty_result = hash_file_content(
        _stage2_file_entry(),
        provider=empty_provider,
        algorithms=(),
    )
    invalid_result = hash_file_content(
        _stage2_file_entry(),
        provider=invalid_provider,
        algorithms=(" ",),
    )
    bad_type_result = hash_file_content(
        _stage2_file_entry(),
        provider=bad_type_provider,
        algorithms=123,
    )

    assert empty_provider.read_count == 0
    assert empty_result.status.code == "invalid_analysis_request"
    assert empty_result.digests == ()
    assert invalid_provider.read_count == 0
    assert invalid_result.status.code == "invalid_analysis_request"
    assert invalid_result.bytes_analyzed is None
    assert bad_type_provider.read_count == 0
    assert bad_type_result.status.code == "invalid_analysis_request"


def test_metadata_only_source_without_provider_is_not_hashed():
    result = hash_file_content(_stage2_file_entry(), provider=None)

    assert result.status.code == "metadata_only_source"
    assert result.content_source.source_kind == "metadata_only"
    assert result.content_source.status.code == "metadata_only_source"
    assert result.bytes_analyzed is None
    assert result.digests[0].digest is None
    assert result.digests[0].status.code == "hash_not_computed"
    assert result.warnings[0].code == "metadata_only_source"


def test_missing_provider_content_returns_structured_unavailable_result():
    provider = CountingAnalysisProvider()

    result = hash_file_content(
        _stage2_file_entry(file_id="missing-file", path="/missing.txt"),
        provider=provider,
    )

    assert provider.read_count == 1
    assert result.status.code == "content_source_unavailable"
    assert result.content_source.provider_name == "stub-analysis-provider"
    assert result.content_source.status.code == "content_source_unavailable"
    assert result.content_source.source_content_size is None
    assert result.bytes_analyzed is None
    assert result.digests[0].digest is None
    assert result.warnings[0].code == "content_source_unavailable"


def test_directory_entry_returns_path_not_file_without_provider_read():
    provider = CountingAnalysisProvider()

    result = hash_file_content(
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
    assert result.bytes_analyzed is None
    assert result.digests[0].digest is None
    assert result.warnings[0].code == "path_not_file"


def test_provider_exception_returns_structured_error_without_traceback():
    provider: AnalysisContentProvider = ExplodingAnalysisProvider()

    result = hash_file_content(_stage2_file_entry(), provider=provider)

    assert result.status.code == "content_provider_error"
    assert result.status.ok is False
    assert "Traceback" not in result.status.message
    assert "RuntimeError" in result.status.message
    assert result.content_source.status.code == "content_provider_error"
    assert result.bytes_analyzed is None
    assert result.digests[0].digest is None
    assert result.warnings[0].code == "content_provider_error"


def test_generated_fixture_provider_preserves_request_provenance_and_labels():
    source = AnalysisSourceProvenance.from_file_entry(
        _stage2_file_entry(case_id="entry-case", evidence_id="entry-evidence"),
        case_id="case-test",
        evidence_id="evidence-test",
    )
    request = HashAnalysisRequest(
        source=source,
        requested_algorithms=("sha256",),
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
    provider = StubAnalysisContentProvider(
        source_kind="generated_fixture",
        synthetic=False,
        generated=True,
        source_name="tiny-generated.bin",
        source_version="fixture-v1",
    )

    result = hash_file_content(request, provider=provider)

    assert result.status.code == "ok"
    assert result.source.case_id == "case-test"
    assert result.source.evidence_id == "evidence-test"
    assert result.content_source.source_kind == "generated_fixture"
    assert result.content_source.synthetic is False
    assert result.content_source.generated is True
    assert result.content_source.source_name == "tiny-generated.bin"
    assert result.content_source.source_version == "fixture-v1"
    assert result.warnings[0].code == "generated_fixture_content"
    _assert_json_safe(result.to_dict())


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
