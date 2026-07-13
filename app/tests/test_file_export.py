"""Tests for the S3-T02 fixture/stub export service."""

from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import shutil

from app.backend.api import (
    DEFAULT_MANIFEST_SUFFIX,
    StubExportContentProvider,
    export_file,
    export_file_to_json,
)
import app.backend.api.file_export as file_export_module
from app.backend.forensic_core import ExportRequest, ExportSourceProvenance


HELLO_SHA256 = "315f5bdb76d078c43b8ac0064e4a0164612b1fce77c869345bfc94c75894edd3"


@contextmanager
def _export_fixture_directory(name: str):
    root = Path.cwd() / ".test-artifacts"
    directory = root / name

    if directory.exists():
        shutil.rmtree(directory)

    directory.mkdir(parents=True)
    try:
        yield directory
    finally:
        shutil.rmtree(directory, ignore_errors=True)
        try:
            root.rmdir()
        except OSError:
            pass


def _stub_file_entry(**overrides: object) -> dict[str, object]:
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


def test_successful_stub_export_writes_file_and_manifest():
    with _export_fixture_directory("file-export-success") as directory:
        output_dir = directory / "exports"

        result = export_file(_stub_file_entry(), output_dir)
        parsed = json.loads(export_file_to_json(_stub_file_entry(), directory / "json-export"))

        output_path = Path(str(result.output_path))
        manifest_path = Path(str(result.manifest_path))
        exported_bytes = output_path.read_bytes()
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert result.status.code == "ok"
    assert output_path.name == "hello.txt"
    assert exported_bytes == b"Hello, world!"
    assert manifest_path.name == f"hello.txt{DEFAULT_MANIFEST_SUFFIX}"
    assert manifest["status"]["code"] == "ok"
    assert manifest["output_path"] == str(output_path)
    assert manifest["manifest_path"] == str(manifest_path)
    assert manifest["bytes_requested"] == 13
    assert manifest["bytes_written"] == 13
    assert manifest["source"]["file_id"] == "stub-file-hello"
    assert manifest["source"]["file_path"] == "/hello.txt"
    assert manifest["content_source"]["provider_name"] == "stub-export-provider"
    assert manifest["content_source"]["source_kind"] == "stub"
    assert manifest["content_source"]["synthetic"] is True
    assert manifest["content_source"]["source_content_size"] == 13
    assert manifest["hashes"]["sha256"] == HELLO_SHA256
    assert manifest["hashes"]["status"]["code"] == "ok"
    assert result.bytes_requested == 13
    assert result.bytes_written == 13
    assert result.hashes.sha256 == HELLO_SHA256
    assert result.hashes.status.code == "ok"
    assert result.destination_status.code == "ok"
    assert parsed["status"]["code"] == "ok"
    assert parsed["hashes"]["sha256"] == HELLO_SHA256


def test_result_and_manifest_agree_on_export_fields():
    with _export_fixture_directory("file-export-agreement") as directory:
        result = export_file(_stub_file_entry(), directory / "exports")
        manifest = json.loads(Path(str(result.manifest_path)).read_text(encoding="utf-8"))

    result_dict = result.to_dict()

    assert manifest["output_path"] == result_dict["output_path"]
    assert manifest["manifest_path"] == result_dict["manifest_path"]
    assert manifest["bytes_requested"] == result_dict["bytes_requested"]
    assert manifest["bytes_written"] == result_dict["bytes_written"]
    assert manifest["source"] == result_dict["source"]
    assert manifest["content_source"] == result_dict["content_source"]
    assert manifest["hashes"] == result_dict["hashes"]
    assert manifest["hashes"]["sha256"] == HELLO_SHA256
    assert manifest["hashes"]["status"]["code"] == "ok"
    assert result_dict["manifest"]["manifest_path"] == result_dict["manifest_path"]


def test_hash_is_calculated_from_exported_file_bytes(monkeypatch):
    written_bytes = b"Jello, world!"

    def write_different_same_size_bytes(path: Path, data: bytes) -> None:
        assert len(data) == len(written_bytes)
        with path.open("xb") as output:
            output.write(written_bytes)

    monkeypatch.setattr(
        file_export_module,
        "_write_bytes_exclusive",
        write_different_same_size_bytes,
    )

    with _export_fixture_directory("file-export-hash-from-disk") as directory:
        result = export_file(_stub_file_entry(), directory / "exports")
        manifest = json.loads(Path(str(result.manifest_path)).read_text(encoding="utf-8"))

    expected_hash = hashlib.sha256(written_bytes).hexdigest()
    assert result.status.code == "ok"
    assert result.bytes_requested == 13
    assert result.bytes_written == 13
    assert result.hashes.sha256 == expected_hash
    assert result.hashes.sha256 != HELLO_SHA256
    assert manifest["hashes"]["sha256"] == expected_hash
    assert manifest["bytes_written"] == 13


def test_byte_count_mismatch_returns_structured_non_ok_status(monkeypatch):
    def write_short_output(path: Path, data: bytes) -> None:
        with path.open("xb") as output:
            output.write(b"short")

    monkeypatch.setattr(file_export_module, "_write_bytes_exclusive", write_short_output)

    with _export_fixture_directory("file-export-byte-count-mismatch") as directory:
        result = export_file(_stub_file_entry(), directory / "exports")
        manifest = json.loads(Path(str(result.manifest_path)).read_text(encoding="utf-8"))

    assert result.status.code == "byte_count_mismatch"
    assert result.bytes_requested == 13
    assert result.bytes_written == 5
    assert result.hashes.sha256 == hashlib.sha256(b"short").hexdigest()
    assert result.hashes.status.code == "ok"
    assert result.warnings[-1].code == "byte_count_mismatch"
    assert manifest["status"]["code"] == "byte_count_mismatch"
    assert manifest["bytes_requested"] == result.bytes_requested
    assert manifest["bytes_written"] == result.bytes_written
    assert manifest["hashes"]["sha256"] == result.hashes.sha256


def test_missing_output_after_write_returns_structured_verification_failure(monkeypatch):
    def write_then_remove_output(path: Path, data: bytes) -> None:
        with path.open("xb") as output:
            output.write(data)
        path.unlink()

    monkeypatch.setattr(
        file_export_module,
        "_write_bytes_exclusive",
        write_then_remove_output,
    )

    with _export_fixture_directory("file-export-missing-after-write") as directory:
        result = export_file(_stub_file_entry(), directory / "exports")
        manifest = json.loads(Path(str(result.manifest_path)).read_text(encoding="utf-8"))

    assert result.status.code == "export_verification_failed"
    assert result.bytes_requested == 13
    assert result.bytes_written is None
    assert result.hashes.sha256 is None
    assert result.hashes.status.code == "hash_failed"
    assert result.warnings[-1].code == "export_verification_failed"
    assert manifest["status"]["code"] == "export_verification_failed"
    assert manifest["bytes_written"] is None
    assert manifest["hashes"]["sha256"] is None
    assert manifest["hashes"]["status"]["code"] == "hash_failed"


def test_missing_provider_content_returns_structured_status_without_writing():
    with _export_fixture_directory("file-export-missing-content") as directory:
        output_dir = directory / "exports"
        result = export_file(
            _stub_file_entry(file_id="missing-file", path="/missing.txt"),
            output_dir,
        )

    assert result.status.code == "content_source_unavailable"
    assert result.output_path is not None
    assert result.manifest_path is not None
    assert not Path(str(result.output_path)).exists()
    assert not Path(str(result.manifest_path)).exists()
    assert result.content_source.status.code == "content_source_unavailable"
    assert result.hashes.sha256 is None
    assert result.hashes.status.code == "hash_not_computed"
    assert result.warnings[0].code == "content_source_unavailable"


def test_directory_entry_returns_path_not_file_without_writing():
    with _export_fixture_directory("file-export-directory-entry") as directory:
        result = export_file(
            _stub_file_entry(
                file_id="stub-dir-documents",
                path="/Documents",
                name="Documents",
                entry_type="directory",
                size=0,
            ),
            directory / "exports",
        )

    assert result.status.code == "path_not_file"
    assert result.output_path is None
    assert result.manifest_path is None
    assert result.warnings[0].code == "path_not_file"


def test_missing_output_directory_returns_destination_not_selected():
    result = export_file(_stub_file_entry(), None)

    assert result.status.code == "destination_not_selected"
    assert result.output_path is None
    assert result.manifest_path is None
    assert result.warnings[0].code == "destination_not_selected"


def test_unsafe_destination_overlapping_source_is_rejected_before_write():
    with _export_fixture_directory("file-export-unsafe-destination") as directory:
        evidence_dir = directory / "evidence"
        evidence_dir.mkdir()
        source_path = evidence_dir / "tiny.raw"
        source_path.write_bytes(b"source")

        result = export_file(
            _stub_file_entry(source_path=str(source_path)),
            evidence_dir / "exports",
        )

    assert result.status.code == "unsafe_destination"
    assert result.destination_status.code == "unsafe_destination"
    assert result.output_path is None
    assert result.manifest_path is None
    assert result.hashes.sha256 is None
    assert result.hashes.status.code == "hash_not_computed"
    assert result.warnings[0].code == "unsafe_destination"


def test_invalid_output_name_or_traversal_is_rejected_before_write():
    with _export_fixture_directory("file-export-invalid-name") as directory:
        traversal_result = export_file(
            _stub_file_entry(name="../hello.txt"),
            directory / "exports",
        )
        explicit_result = export_file(
            _stub_file_entry(),
            directory / "exports",
            output_name="nested/hello.txt",
        )

    assert traversal_result.status.code == "invalid_output_name"
    assert traversal_result.output_path is None
    assert traversal_result.manifest_path is None
    assert explicit_result.status.code == "invalid_output_name"
    assert explicit_result.output_path is None
    assert explicit_result.manifest_path is None


def test_existing_output_file_is_refused_without_overwrite():
    with _export_fixture_directory("file-export-existing-output") as directory:
        output_dir = directory / "exports"
        output_dir.mkdir()
        existing = output_dir / "hello.txt"
        existing.write_bytes(b"existing")

        result = export_file(_stub_file_entry(), output_dir)
        existing_bytes = existing.read_bytes()

    assert result.status.code == "output_exists"
    assert result.output_path == str(existing.resolve(strict=False))
    assert existing_bytes == b"existing"
    assert result.warnings[0].code == "output_exists"


def test_write_time_existing_output_is_refused_without_overwrite(monkeypatch):
    def raise_file_exists(path: Path, data: bytes) -> None:
        error = FileExistsError("output exists at write time")
        error.filename = str(path)
        raise error

    monkeypatch.setattr(file_export_module, "_write_bytes_exclusive", raise_file_exists)

    with _export_fixture_directory("file-export-write-time-output-exists") as directory:
        output_dir = directory / "exports"

        result = export_file(_stub_file_entry(), output_dir)

    assert result.status.code == "output_exists"
    assert result.output_path is not None
    assert result.manifest_path is not None
    assert not Path(str(result.output_path)).exists()
    assert not Path(str(result.manifest_path)).exists()
    assert result.warnings[0].code == "output_exists"


def test_write_time_existing_manifest_is_refused_and_output_is_cleaned(monkeypatch):
    def raise_file_exists(path: Path, text: str) -> None:
        error = FileExistsError("manifest exists at write time")
        error.filename = str(path)
        raise error

    monkeypatch.setattr(file_export_module, "_write_text_exclusive", raise_file_exists)

    with _export_fixture_directory("file-export-write-time-manifest-exists") as directory:
        output_dir = directory / "exports"

        result = export_file(_stub_file_entry(), output_dir)

    assert result.status.code == "output_exists"
    assert result.output_path is not None
    assert result.manifest_path is not None
    assert not Path(str(result.output_path)).exists()
    assert not Path(str(result.manifest_path)).exists()
    assert result.warnings[0].code == "output_exists"


def test_manifest_write_failure_cleans_up_written_output(monkeypatch):
    def raise_manifest_failure(path: Path, text: str) -> None:
        raise OSError("manifest write failed")

    monkeypatch.setattr(file_export_module, "_write_text_exclusive", raise_manifest_failure)

    with _export_fixture_directory("file-export-manifest-write-failure") as directory:
        output_dir = directory / "exports"

        result = export_file(_stub_file_entry(), output_dir)

    assert result.status.code == "export_write_failed"
    assert result.output_path is not None
    assert result.manifest_path is not None
    assert not Path(str(result.output_path)).exists()
    assert not Path(str(result.manifest_path)).exists()
    assert result.warnings[0].code == "export_write_failed"


def test_partial_output_write_failure_cleans_up_partial_output(monkeypatch):
    def write_partial_output_then_fail(path: Path, data: bytes) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"partial")
        raise OSError("partial output write failed")

    monkeypatch.setattr(
        file_export_module,
        "_write_bytes_exclusive",
        write_partial_output_then_fail,
    )

    with _export_fixture_directory("file-export-partial-output-failure") as directory:
        result = export_file(_stub_file_entry(), directory / "exports")

    assert result.status.code == "export_write_failed"
    assert result.output_path is not None
    assert result.manifest_path is not None
    assert not Path(str(result.output_path)).exists()
    assert not Path(str(result.manifest_path)).exists()
    assert result.warnings[0].code == "export_write_failed"


def test_partial_manifest_write_failure_cleans_up_output_and_partial_manifest(monkeypatch):
    def write_partial_manifest_then_fail(path: Path, text: str) -> None:
        path.write_text("partial manifest", encoding="utf-8")
        raise OSError("partial manifest write failed")

    monkeypatch.setattr(
        file_export_module,
        "_write_text_exclusive",
        write_partial_manifest_then_fail,
    )

    with _export_fixture_directory("file-export-partial-manifest-failure") as directory:
        result = export_file(_stub_file_entry(), directory / "exports")

    assert result.status.code == "export_write_failed"
    assert result.output_path is not None
    assert result.manifest_path is not None
    assert not Path(str(result.output_path)).exists()
    assert not Path(str(result.manifest_path)).exists()
    assert result.warnings[0].code == "export_write_failed"


def test_safe_export_request_requested_output_path_is_used():
    with _export_fixture_directory("file-export-requested-output-path") as directory:
        request = ExportRequest(
            source=ExportSourceProvenance.from_file_entry(_stub_file_entry()),
            destination_directory=str(directory / "exports"),
            requested_output_path="custom-name.bin",
        )

        result = export_file(request)
        output_path = Path(str(result.output_path))
        exported_bytes = output_path.read_bytes()

    assert result.status.code == "ok"
    assert output_path.name == "custom-name.bin"
    assert exported_bytes == b"Hello, world!"
    assert result.requested_output_path == str(output_path)


def test_unsafe_export_request_requested_output_path_is_rejected():
    with _export_fixture_directory("file-export-requested-output-traversal") as directory:
        request = ExportRequest(
            source=ExportSourceProvenance.from_file_entry(_stub_file_entry()),
            destination_directory=str(directory / "exports"),
            requested_output_path="../escape.bin",
        )

        result = export_file(request)

    assert result.status.code == "invalid_output_name"
    assert result.output_path is None
    assert result.manifest_path is None
    assert result.warnings[0].code == "invalid_output_name"


def test_provider_source_data_is_not_mutated():
    content = {"stub-file-hello": b"Hello, world!"}
    provider = StubExportContentProvider(content)
    before = provider.get_content(
        ExportSourceProvenance.from_file_entry(_stub_file_entry())
    ).data

    with _export_fixture_directory("file-export-provider-not-mutated") as directory:
        result = export_file(_stub_file_entry(), directory / "exports", provider=provider)

    after = provider.get_content(
        ExportSourceProvenance.from_file_entry(_stub_file_entry())
    ).data

    assert result.status.code == "ok"
    assert before == b"Hello, world!"
    assert after == before
    assert content == {"stub-file-hello": b"Hello, world!"}
