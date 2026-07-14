"""Tests for S4-T05 fixture-sized known-file matching."""

import hashlib
from inspect import getsource, signature
import json

from app.backend.forensic_core import (
    AnalysisContentSourceIdentity,
    AnalysisSourceProvenance,
    AnalysisStatus,
    HashAnalysisResult,
    HashDigestResult,
    StubAnalysisContentProvider,
    detect_file_signature,
    evaluate_extension_mismatch,
    hash_file_content,
    known_file_match_result_to_json,
    match_known_file_hashes,
    match_known_files,
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


def _digest(algorithm: str, data: bytes = HELLO_BYTES) -> str:
    return hashlib.new(algorithm, data).hexdigest()


def _hash_result(
    *,
    algorithms: tuple[str, ...] = ("sha256",),
    provider: StubAnalysisContentProvider | None = None,
) -> HashAnalysisResult:
    return hash_file_content(
        _stage2_file_entry(),
        provider=provider or StubAnalysisContentProvider(),
        algorithms=algorithms,
    )


def test_sha256_known_file_match_preserves_record_provenance_and_json_safety():
    hash_result = _hash_result()

    result = match_known_file_hashes(
        hash_result,
        (
            {
                "algorithm": " SHA-256 ",
                "digest": _digest("sha256").upper(),
                "category": "known_good",
                "dataset_name": "fixture-known-files",
                "dataset_version": "2026.07",
                "record_id": "kg-hello",
                "file_name": "hello.txt",
                "note": "caller metadata",
                "metadata": {
                    "nested": {"ok": True},
                    "raw_marker": b"\x00\xff",
                },
            },
        ),
    )
    parsed = json.loads(known_file_match_result_to_json(result))

    assert result.status.code == "known_file_match"
    assert result.status.ok is True
    assert result.matched is True
    assert result.match_category == "known_good"
    assert result.matched_algorithm == "sha256"
    assert result.matched_digest == _digest("sha256")
    assert result.hash_status.code == "ok"
    assert result.bytes_analyzed == len(HELLO_BYTES)
    assert result.source.file_id == "stub-file-hello"
    assert result.content_source.source_kind == "synthetic"
    assert result.content_source.synthetic is True
    assert result.digests == hash_result.digests
    assert result.hash_created_at == hash_result.created_at
    assert result.hash_completed_at == hash_result.completed_at
    assert result.matched_records[0].dataset_name == "fixture-known-files"
    assert result.matched_records[0].dataset_version == "2026.07"
    assert result.matched_records[0].record_id == "kg-hello"
    assert result.matched_records[0].metadata["note"] == "caller metadata"
    assert result.matched_records[0].metadata["raw_marker"]["type"] == "bytes"
    assert result.matched_records[0].original_algorithm == " SHA-256 "
    assert result.matched_records[0].original_digest == _digest("sha256").upper()
    assert [warning.code for warning in result.warnings] == [
        "synthetic_content",
        "synthetic_hash_match_context",
    ]
    assert parsed["matched_records"][0]["dataset_name"] == "fixture-known-files"
    assert parsed["status"]["ok"] is True
    _assert_json_safe(result.to_dict())


def test_md5_and_sha1_known_file_matches_when_present():
    examples = (
        ("md5", "MD5", "known_bad"),
        ("sha1", "sha_1", "known_unknown"),
    )

    for algorithm, record_algorithm, category in examples:
        result = match_known_file_hashes(
            _hash_result(algorithms=(algorithm,)),
            (
                {
                    "algorithm": record_algorithm,
                    "digest": _digest(algorithm).upper(),
                    "category": category,
                },
            ),
        )

        assert result.status.code == "known_file_match"
        assert result.matched is True
        assert result.match_category == category
        assert result.matched_algorithm == algorithm
        assert result.matched_digest == _digest(algorithm)


def test_sha256_is_preferred_and_all_available_digest_matches_are_preserved():
    hash_result = _hash_result(algorithms=("md5", "sha1", "sha256"))

    result = match_known_files(
        hash_result,
        (
            {
                "algorithm": "md5",
                "digest": _digest("md5"),
                "category": "known_bad",
                "record_id": "md5-match",
            },
            {
                "algorithm": "sha1",
                "digest": _digest("sha1"),
                "category": "known_bad",
                "record_id": "sha1-match",
            },
            {
                "algorithm": "sha256",
                "digest": _digest("sha256"),
                "category": "known_good",
                "record_id": "sha256-match",
            },
        ),
    )

    assert result.status.code == "known_file_match"
    assert result.matched_algorithm == "sha256"
    assert result.match_category == "known_good"
    assert [record.record_id for record in result.matched_records] == [
        "md5-match",
        "sha1-match",
        "sha256-match",
    ]


def test_no_known_file_match_returns_structured_no_match():
    result = match_known_file_hashes(
        _hash_result(),
        (
            {
                "algorithm": "sha256",
                "digest": _digest("sha256", b"other bytes"),
                "category": "known_good",
            },
        ),
    )

    assert result.status.code == "known_file_no_match"
    assert result.status.ok is True
    assert result.matched is False
    assert result.match_category is None
    assert result.matched_records == ()


def test_non_ok_hash_result_is_not_matched():
    hash_result = hash_file_content(_stage2_file_entry(), provider=None)

    result = match_known_file_hashes(
        hash_result,
        (
            {
                "algorithm": "sha256",
                "digest": _digest("sha256"),
                "category": "known_good",
            },
        ),
    )

    assert result.status.code == "hash_not_available"
    assert result.status.ok is False
    assert result.matched is None
    assert result.hash_status.code == "metadata_only_source"
    assert result.digests == hash_result.digests
    assert result.warnings[-1].code == "hash_not_available"


def test_ok_hash_without_computed_digest_is_not_matched():
    source = AnalysisSourceProvenance.from_file_entry(_stage2_file_entry())
    hash_result = HashAnalysisResult(
        source=source,
        content_source=AnalysisContentSourceIdentity(
            provider_name="stub-analysis-provider",
            source_kind="synthetic",
            read_only=True,
            synthetic=True,
            source_content_size=13,
            status=AnalysisStatus(
                code="ok",
                message="Analysis content provider returned raw bytes.",
            ),
        ),
        requested_algorithms=("sha256",),
        digests=(
            HashDigestResult(
                algorithm="sha256",
                status=AnalysisStatus(
                    code="hash_not_computed",
                    message="Digest was not computed.",
                ),
            ),
        ),
        status=AnalysisStatus(
            code="ok",
            message="Hash analysis completed from explicit provider bytes.",
        ),
        bytes_analyzed=13,
        created_at="2026-07-14T10:00:00Z",
        completed_at="2026-07-14T10:00:01Z",
    )

    result = match_known_file_hashes(
        hash_result,
        (
            {
                "algorithm": "sha256",
                "digest": _digest("sha256"),
                "category": "known_good",
            },
        ),
    )

    assert result.status.code == "hash_digest_unavailable"
    assert result.matched is None
    assert result.warnings[-1].code == "hash_digest_unavailable"


def test_invalid_known_file_records_are_reported_without_crashing():
    result = match_known_file_hashes(
        _hash_result(),
        (
            {
                "algorithm": "sha512",
                "digest": _digest("sha256"),
                "category": "known_good",
            },
            {
                "algorithm": "sha256",
                "category": "known_good",
            },
            {
                "algorithm": "sha256",
                "digest": _digest("sha256"),
                "category": "known_suspicious",
            },
        ),
    )

    assert result.status.code == "invalid_known_file_record"
    assert result.matched is None
    assert result.matched_records == ()
    assert [warning.code for warning in result.warnings] == [
        "synthetic_content",
        "invalid_known_file_record",
        "invalid_known_file_record",
        "invalid_known_file_record",
    ]


def test_duplicate_same_category_records_are_preserved_as_matches():
    result = match_known_file_hashes(
        _hash_result(),
        (
            {
                "algorithm": "sha256",
                "digest": _digest("sha256"),
                "category": "known_bad",
                "record_id": "bad-1",
            },
            {
                "algorithm": "sha256",
                "digest": _digest("sha256"),
                "category": "known_bad",
                "record_id": "bad-2",
            },
        ),
    )

    assert result.status.code == "known_file_match"
    assert result.matched is True
    assert result.match_category == "known_bad"
    assert [record.record_id for record in result.matched_records] == [
        "bad-1",
        "bad-2",
    ]


def test_conflicting_categories_for_same_digest_are_non_ok():
    result = match_known_file_hashes(
        _hash_result(),
        (
            {
                "algorithm": "sha256",
                "digest": _digest("sha256"),
                "category": "known_good",
                "record_id": "good",
            },
            {
                "algorithm": "sha256",
                "digest": _digest("sha256"),
                "category": "known_bad",
                "record_id": "bad",
            },
        ),
    )

    assert result.status.code == "conflicting_known_file_records"
    assert result.status.ok is False
    assert result.matched is None
    assert result.matched_algorithm == "sha256"
    assert result.matched_digest == _digest("sha256")
    assert [record.record_id for record in result.matched_records] == [
        "good",
        "bad",
    ]
    assert result.warnings[-1].code == "conflicting_known_file_records"


def test_generated_fixture_hash_context_is_preserved_in_match_result():
    provider = StubAnalysisContentProvider(
        source_kind="generated_fixture",
        synthetic=False,
        generated=True,
        source_name="generated-hello.bin",
        source_version="fixture-v1",
    )

    result = match_known_file_hashes(
        _hash_result(provider=provider),
        (
            {
                "algorithm": "sha256",
                "digest": _digest("sha256"),
                "category": "known_unknown",
            },
        ),
    )

    assert result.status.code == "known_file_match"
    assert result.content_source.source_kind == "generated_fixture"
    assert result.content_source.generated is True
    assert result.content_source.source_name == "generated-hello.bin"
    assert [warning.code for warning in result.warnings] == [
        "generated_fixture_content",
        "generated_fixture_hash_match_context",
    ]


def test_matcher_has_no_provider_parameter_and_does_not_recalculate_hashes():
    parameters = signature(match_known_file_hashes).parameters
    source = getsource(match_known_file_hashes)

    assert tuple(parameters) == ("hash_result", "known_files")
    assert "provider" not in parameters
    assert "hash_file_content" not in source
    assert "calculate_hashes" not in source


def test_s4_t02_t03_t04_behaviors_still_use_provider_bytes():
    provider = StubAnalysisContentProvider({"stub-file-hello": b"%PDF-1.7"})

    signature_result = detect_file_signature(
        _stage2_file_entry(name="hello.pdf", path="/hello.pdf"),
        provider=provider,
        max_bytes=5,
    )
    mismatch_result = evaluate_extension_mismatch(signature_result)
    hash_result = hash_file_content(
        _stage2_file_entry(),
        provider=provider,
        algorithms=("sha256",),
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
