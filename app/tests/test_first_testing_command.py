"""Tests for the Stage 4.5 first-testing command shell."""

from contextlib import contextmanager
import csv
import hashlib
import json
from pathlib import Path
import shutil

from app.backend.api import first_testing as first_testing_api
from app.backend.api.first_testing import (
    FILE_LIST_CSV_HEADERS,
    FIRST_TESTING_RUN_SCHEMA_VERSION,
    main,
    run_first_testing,
)
from app.backend.case_store import connect
from app.backend.forensic_core import (
    ImageReadResult,
    ImageStreamInfo,
    ImageStreamStatus,
    PyewfEwfReaderAdapter,
    SelectedFileContentResult,
    SelectedFileContentStatus,
    SelectedFileContentWarning,
)


class FakePyewf:
    __version__ = "fake-pyewf-2.0"

    def __init__(self, handle):
        self._handle = handle

    def handle(self):
        return self._handle


class FakeHandle:
    def open(self, paths):
        self.paths = list(paths)

    def close(self):
        self.closed = True

    def get_media_size(self):
        return 2048

    def get_bytes_per_sector(self):
        return 512

    def get_header_values(self):
        return {"case_number": "CASE-FIRST", "examiner": "Test Examiner"}

    def get_hash_values(self):
        return {"md5": "stored-md5"}

    def verify(self):
        return True


class FakeHashEwfImageByteStream:
    stream_type = "ewf"
    read_only = True
    DATA = b"logical image bytes for hashing"

    def __init__(self, selected_path, *, segment_paths=None, **kwargs):
        self.source_path = str(Path(selected_path).resolve())
        self.segment_paths = tuple(str(Path(path).resolve()) for path in (segment_paths or [selected_path]))
        self.data = self.DATA

    def describe(self):
        return ImageStreamInfo(
            source_path=self.source_path,
            stream_type=self.stream_type,
            size=len(self.data),
            read_only=True,
            status=ImageStreamStatus("ok", "fake stream ok", self.source_path),
        )

    def read_at(self, offset: int, length: int):
        return ImageReadResult(
            source_path=self.source_path,
            stream_type=self.stream_type,
            read_only=True,
            offset=offset,
            length=length,
            source_size=len(self.data),
            data=self.data[offset : offset + length],
            status=ImageStreamStatus("ok", "fake read ok", self.source_path),
        )


SELECTED_BYTES = b"%PDF-1.7\nselected bytes"


class FakeSelectedFileContentReader:
    provider_name = "fake-selected-file-content-reader"
    source_kind = "real_parser"
    parser_name = "pytsk3"
    parser_version = "fake-pytsk3"
    read_only = True
    synthetic = False

    def __init__(self, image_stream, volume, file_entry, **kwargs):
        self.file_entry = dict(file_entry)

    def check(self):
        return self._result(SelectedFileContentStatus("ok", "available"), b"")

    def read_range(self, offset: int, length: int):
        return self._result(
            SelectedFileContentStatus("ok", "read"),
            SELECTED_BYTES[offset : offset + length],
            requested_offset=offset,
            requested_length=length,
        )

    def read_full(self, *, max_bytes: int):
        if int(self.file_entry.get("size") or 0) > max_bytes:
            return self._result(
                SelectedFileContentStatus(
                    "file_too_large_for_in_memory_provider",
                    "too large",
                ),
                b"",
            )
        return self._result(
            SelectedFileContentStatus("ok", "read"),
            SELECTED_BYTES,
            requested_offset=0,
            requested_length=len(SELECTED_BYTES),
        )

    def _result(
        self,
        status,
        data: bytes,
        *,
        requested_offset=None,
        requested_length=None,
    ):
        return SelectedFileContentResult(
            status=status,
            file_entry=self.file_entry,
            source_path=self.file_entry.get("source_path"),
            volume_id=self.file_entry.get("volume_id"),
            volume_offset=self.file_entry.get("volume_offset"),
            volume_length=self.file_entry.get("volume_length"),
            file_id=self.file_entry.get("file_id"),
            file_path=self.file_entry.get("path"),
            file_name=self.file_entry.get("name"),
            entry_type=self.file_entry.get("entry_type"),
            filesystem_type=self.file_entry.get("filesystem_type"),
            adapter_name=self.file_entry.get("adapter_name"),
            source_kind="real_parser" if status.ok else "metadata_only",
            provider_name=self.provider_name,
            parser_name=self.parser_name if status.ok else None,
            parser_version=self.parser_version if status.ok else None,
            read_only=True,
            source_content_size=self.file_entry.get("size"),
            requested_offset=requested_offset,
            requested_length=requested_length,
            bytes_read=len(data),
            data=data,
            synthetic=False,
            warnings=(
                SelectedFileContentWarning(
                    code="real_parser_content",
                    message="fake parser bytes",
                    path=self.file_entry.get("path"),
                    source="selected_file_content_reader",
                ),
            )
            if status.ok
            else (),
        )


@contextmanager
def _dummy_first_testing_directory(name: str):
    root = Path.cwd() / ".test-artifacts" / "first-testing-command"
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
        try:
            root.parent.rmdir()
        except OSError:
            pass


def _touch_files(directory: Path, *filenames: str) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    for filename in filenames:
        (directory / filename).touch()


def _required_artifacts(case_dir: Path, output_dir: Path) -> list[Path]:
    return [
        case_dir / "case.db",
        case_dir / "run-manifest.json",
        case_dir / "command-summary.txt",
        output_dir / "intake.json",
        output_dir / "case.json",
        output_dir / "metadata.json",
        output_dir / "verification.json",
        output_dir / "segment-discovery.json",
        output_dir / "ewf-stream.json",
        output_dir / "volumes.json",
        output_dir / "filesystems.json",
        output_dir / "root-listing.json",
        output_dir / "demo-readiness.json",
        output_dir / "image-hash.json",
        output_dir / "selected-file-readiness.json",
        output_dir / "selected-file-preview.json",
        output_dir / "selected-file-analysis.json",
        output_dir / "selected-file-export.json",
        output_dir / "file-list.json",
        output_dir / "file-list.csv",
        output_dir / "reports" / "summary.html",
        output_dir / "audit.json",
        output_dir / "unsupported-sections.json",
    ]


def _audit_actions(case_db: Path) -> set[str]:
    connection = connect(case_db)
    try:
        return {
            row["action"]
            for row in connection.execute("SELECT action FROM audit_events").fetchall()
        }
    finally:
        connection.close()


def _fake_selected_file_demo_artifacts(*, selected_path, intake_result, adapter_name):
    entry = {
        "file_id": "volume-0:42",
        "path": "/document.pdf",
        "name": "document.pdf",
        "entry_type": "file",
        "size": len(SELECTED_BYTES),
        "allocated": True,
        "deleted": False,
        "source_path": str(selected_path),
        "volume_id": "volume-0",
        "volume_offset": 512,
        "volume_length": 2048,
        "filesystem_type": "ntfs",
        "adapter_name": "pytsk3-filesystem-adapter",
        "read_only": True,
        "timestamps": {},
    }
    volume = {
        "volume_id": "volume-0",
        "volume_index": 0,
        "source_path": str(selected_path),
        "stream_type": "ewf",
        "source_size": 4096,
        "offset": 512,
        "length": 2048,
        "volume_type": "ntfs",
        "description": "fake volume",
        "read_only": True,
        "status": {"code": "ok", "ok": True, "message": "ok"},
        "warnings": [],
    }
    return {
        "ewf_stream": {
            "schema_version": "stage4_5.first_testing_ewf_stream.v1",
            "status": "ok",
            "logical_media_size": 4096,
        },
        "volumes": {
            "schema_version": "stage4_5.first_testing_volumes.v1",
            "status": "ok",
            "strategy": "partition_table",
            "volume_count": 1,
            "volume_discovery": {
                "schema_version": "stage2.volume_discovery.v1",
                "status": {"code": "ok", "ok": True, "message": "ok"},
                "volumes": [volume],
            },
        },
        "filesystems": {
            "schema_version": "stage4_5.first_testing_filesystems.v1",
            "status": "ok",
            "filesystem_count": 1,
            "filesystems": [],
        },
        "root_listing": {
            "schema_version": "stage4_5.first_testing_root_listing.v1",
            "status": "ok",
            "parser_backing": "real_parser_backed",
            "entry_count": 1,
            "entries": [entry],
        },
        "demo_readiness": {
            "schema_version": "stage4_5.first_testing_demo_readiness.v1",
            "status": "real_parser_backed_root_listing_available",
            "root_entry_count": 1,
            "root_listing_parser_backing": "real_parser_backed",
        },
    }


def _fake_file_list_demo_artifacts(*, selected_path, intake_result, adapter_name):
    entries = [
        {
            "file_id": "volume-0:99",
            "path": "/=SUM(A1:A2).txt",
            "name": '=SUM(A1:A2), "quoted"\nline.txt',
            "entry_type": "file",
            "size": 123,
            "allocated": True,
            "deleted": False,
            "source_path": str(selected_path),
            "volume_id": "volume-0",
            "volume_offset": 512,
            "volume_length": 4096,
            "filesystem_type": "ntfs",
            "adapter_name": "pytsk3-filesystem-adapter",
            "read_only": True,
            "status": {"code": "ok", "ok": True, "message": "entry ok"},
            "warnings": [
                {
                    "source": "filesystem_adapter",
                    "code": "entry_warning",
                    "message": "fake warning",
                    "path": "/=SUM(A1:A2).txt",
                }
            ],
            "timestamps": {
                "created": "2026-01-01T00:00:00Z",
                "modified": "2026-01-02T00:00:00Z",
                "accessed": None,
                "metadata_changed": "2026-01-03T00:00:00Z",
            },
        },
        {
            "file_id": "volume-0:100",
            "path": "/Documents",
            "name": "Documents",
            "entry_type": "directory",
            "size": None,
            "allocated": True,
            "deleted": False,
            "source_path": str(selected_path),
            "volume_id": "volume-0",
            "volume_offset": 512,
            "volume_length": 4096,
            "filesystem_type": "ntfs",
            "adapter_name": "pytsk3-filesystem-adapter",
            "read_only": True,
            "status": {"code": "ok", "ok": True, "message": "entry ok"},
            "warnings": [],
            "timestamps": {
                "created": None,
                "modified": None,
                "accessed": None,
                "metadata_changed": None,
            },
        },
    ]
    directory_listing = {
        "schema_version": "stage2.directory_listing.v1",
        "status": {"code": "ok", "ok": True, "message": "Directory listing completed."},
        "directory_path": "/",
        "source_path": str(selected_path),
        "volume_id": "volume-0",
        "volume_offset": 512,
        "volume_length": 4096,
        "filesystem_type": "ntfs",
        "adapter": {
            "name": "pytsk3-filesystem-adapter",
            "available": True,
            "dependency": {"name": "pytsk3", "available": True},
        },
        "read_only": True,
        "entry_count": 2,
        "entries": entries,
        "warnings": [],
    }
    return {
        "ewf_stream": {
            "schema_version": "stage4_5.first_testing_ewf_stream.v1",
            "status": "ok",
            "logical_media_size": 8192,
        },
        "volumes": {
            "schema_version": "stage4_5.first_testing_volumes.v1",
            "status": "ok",
            "strategy": "partition_table",
            "volume_count": 1,
        },
        "filesystems": {
            "schema_version": "stage4_5.first_testing_filesystems.v1",
            "status": "ok",
            "filesystem_count": 1,
            "filesystems": [],
        },
        "root_listing": {
            "schema_version": "stage4_5.first_testing_root_listing.v1",
            "status": "ok",
            "parser_backing": "real_parser_backed",
            "entry_count": 2,
            "directory_listing": directory_listing,
            "entries": entries,
        },
        "demo_readiness": {
            "schema_version": "stage4_5.first_testing_demo_readiness.v1",
            "status": "real_parser_backed_root_listing_available",
            "root_entry_count": 2,
            "root_listing_parser_backing": "real_parser_backed",
        },
    }


def test_direct_e01_with_stub_creates_case_artifacts_and_persistence():
    with _dummy_first_testing_directory("direct-stub") as directory:
        evidence_dir = directory / "evidence & root"
        _touch_files(evidence_dir, "sample.E01", "sample.E02")
        case_dir = directory / "case"
        output_dir = directory / "output"

        result = run_first_testing(
            evidence_dir / "sample.E01",
            case_path=case_dir,
            output_path=output_dir,
            adapter_name="stub",
            actor="tester",
        )

        connection = connect(case_dir / "case.db")
        try:
            evidence_rows = connection.execute(
                "SELECT source_path, selected_path, status, segment_count, adapter_name FROM evidence_sources"
            ).fetchall()
        finally:
            connection.close()

        audit = json.loads((output_dir / "audit.json").read_text(encoding="utf-8"))
        selected_readiness = json.loads(
            (output_dir / "selected-file-readiness.json").read_text(encoding="utf-8")
        )
        selected_preview = json.loads(
            (output_dir / "selected-file-preview.json").read_text(encoding="utf-8")
        )
        file_list = json.loads((output_dir / "file-list.json").read_text(encoding="utf-8"))
        image_hash = json.loads((output_dir / "image-hash.json").read_text(encoding="utf-8"))
        csv_header = (output_dir / "file-list.csv").read_text(encoding="utf-8").splitlines()[0]
        html_summary = (output_dir / "reports" / "summary.html").read_text(encoding="utf-8")
        artifact_exists = all(path.exists() for path in _required_artifacts(case_dir, output_dir))
        actions = _audit_actions(case_dir / "case.db")
        audit_actions = {event["action"] for event in audit["events"]}

    assert result["schema_version"] == FIRST_TESTING_RUN_SCHEMA_VERSION
    assert result["status"] == "ok_with_unsupported_sections"
    assert result["evidence"]["segment_count"] == 2
    assert result["adapter"]["name"] == "stub-ewf-reader"
    assert result["source_modified"] is False
    assert result["read_only_asserted"] is True
    assert result["selected_file"]["requested"] is False
    assert result["selected_file"]["selection_status"] == "not_run"
    assert result["image_hash"]["requested"] is False
    assert result["image_hash"]["status"] == "not_run"
    assert result["image_hash"]["hexdigest_available"] is False
    assert image_hash["status"] == "not_run"
    assert image_hash["hexdigest"] is None
    assert selected_readiness["status"]["code"] == "not_run"
    assert selected_preview["status"] == "not_run"
    assert result["file_list"]["status"] == "not_run"
    assert file_list["status"]["code"] == "not_run"
    assert file_list["entry_count"] == 0
    assert csv_header.split(",") == list(FILE_LIST_CSV_HEADERS)
    assert "Stage 4.5 First-Testing Summary" in html_summary
    assert "Image hash status" in html_summary
    assert "File-list status" in html_summary
    assert artifact_exists
    assert len(evidence_rows) == 1
    assert evidence_rows[0]["source_path"] == str((evidence_dir / "sample.E01").resolve())
    assert evidence_rows[0]["selected_path"] == str((evidence_dir / "sample.E01").resolve())
    assert evidence_rows[0]["status"] == "ok"
    assert evidence_rows[0]["segment_count"] == 2
    assert evidence_rows[0]["adapter_name"] == "stub-ewf-reader"
    assert actions == {
        "first_testing.case_created",
        "first_testing.evidence_intake_completed",
        "first_testing.artifacts_written",
        "first_testing.run_completed",
    }
    assert audit_actions == actions


def test_evidence_dir_and_first_segment_resolves_selected_e01():
    with _dummy_first_testing_directory("evidence-dir") as directory:
        evidence_dir = directory / "evidence"
        _touch_files(evidence_dir, "disk.E01", "disk.E02")
        case_dir = directory / "case"
        output_dir = directory / "output"

        result = run_first_testing(
            evidence_dir=evidence_dir,
            first_segment="disk.E01",
            case_path=case_dir,
            output_path=output_dir,
            adapter_name="stub",
        )

    assert result["status"] == "ok_with_unsupported_sections"
    assert result["command"]["input_form"] == "evidence_dir_first_segment"
    assert result["evidence"]["selected_path"] == str((evidence_dir / "disk.E01").resolve())


def test_default_pyewf_dependency_unavailable_path_writes_honest_unsupported_output(monkeypatch):
    def fake_pyewf_adapter():
        return PyewfEwfReaderAdapter(
            pyewf_module=None,
            import_error=ImportError("No module named 'pyewf'"),
        )

    monkeypatch.setattr(first_testing_api, "PyewfEwfReaderAdapter", fake_pyewf_adapter)

    with _dummy_first_testing_directory("pyewf-unavailable") as directory:
        evidence_dir = directory / "evidence"
        _touch_files(evidence_dir, "sample.E01")
        case_dir = directory / "case"

        result = run_first_testing(evidence_dir / "sample.E01", case_path=case_dir)

        intake = json.loads((case_dir / "outputs" / "intake.json").read_text(encoding="utf-8"))
        metadata = json.loads((case_dir / "outputs" / "metadata.json").read_text(encoding="utf-8"))
        verification = json.loads(
            (case_dir / "outputs" / "verification.json").read_text(encoding="utf-8")
        )
        unsupported = json.loads(
            (case_dir / "outputs" / "unsupported-sections.json").read_text(encoding="utf-8")
        )
        ewf_stream = json.loads(
            (case_dir / "outputs" / "ewf-stream.json").read_text(encoding="utf-8")
        )
        root_listing = json.loads(
            (case_dir / "outputs" / "root-listing.json").read_text(encoding="utf-8")
        )
        file_list = json.loads(
            (case_dir / "outputs" / "file-list.json").read_text(encoding="utf-8")
        )
        image_hash = json.loads(
            (case_dir / "outputs" / "image-hash.json").read_text(encoding="utf-8")
        )

    assert result["status"] == "ok_with_unsupported_sections"
    assert intake["status"] == "metadata_unavailable"
    assert intake["adapter"]["name"] == "pyewf-reader"
    assert intake["adapter"]["available"] is False
    assert intake["metadata"] == {}
    assert intake["verification"]["status"] == "not_run"
    assert metadata["status"] == "metadata_unavailable"
    assert verification["status"] == "not_run"
    assert ewf_stream["status"] == "dependency_unavailable"
    assert root_listing["parser_backing"] == "dependency_blocked"
    assert file_list["status"]["code"] == "not_available"
    assert file_list["entry_count"] == 0
    assert image_hash["status"] == "not_run"
    assert image_hash["requested"] is False
    assert "root_listing_not_real_parser_backed" in [
        warning["code"] for warning in file_list["warnings"]
    ]
    assert not any(section["section"] == "real_ewf_metadata" for section in unsupported["sections"])
    assert not any(section["section"] == "real_ewf_verification" for section in unsupported["sections"])
    assert not any(section["owner"] == "S4.5-IMP03" for section in unsupported["sections"])
    assert all(section["status"] == "not_implemented" for section in unsupported["sections"])


def test_first_testing_writes_metadata_and_verification_artifacts_with_fake_pyewf():
    handle = FakeHandle()
    adapter = PyewfEwfReaderAdapter(pyewf_module=FakePyewf(handle))

    with _dummy_first_testing_directory("fake-pyewf-artifacts") as directory:
        evidence_dir = directory / "evidence"
        _touch_files(evidence_dir, "sample.E01")
        case_dir = directory / "case"
        output_dir = directory / "output"

        result = run_first_testing(
            evidence_dir / "sample.E01",
            case_path=case_dir,
            output_path=output_dir,
            adapter=adapter,
        )

        metadata = json.loads((output_dir / "metadata.json").read_text(encoding="utf-8"))
        verification = json.loads((output_dir / "verification.json").read_text(encoding="utf-8"))
        segments = json.loads((output_dir / "segment-discovery.json").read_text(encoding="utf-8"))
        ewf_stream = json.loads((output_dir / "ewf-stream.json").read_text(encoding="utf-8"))
        root_listing = json.loads((output_dir / "root-listing.json").read_text(encoding="utf-8"))
        summary = (case_dir / "command-summary.txt").read_text(encoding="utf-8")
        unsupported = json.loads(
            (output_dir / "unsupported-sections.json").read_text(encoding="utf-8")
        )
        later_artifacts_exist = [
            (output_dir / "file-list.json").exists(),
            (output_dir / "file-list.csv").exists(),
            (output_dir / "exports").exists(),
            (output_dir / "reports").exists(),
            any(output_dir.rglob("*.html")),
        ]

    assert result["status"] == "ok_with_unsupported_sections"
    assert result["metadata"]["status"] == "metadata_available"
    assert result["verification"]["status"] == "verification_ok"
    assert metadata["status"] == "metadata_available"
    assert metadata["metadata"]["media_size"] == 2048
    assert metadata["metadata"]["case_number"] == "CASE-FIRST"
    assert metadata["metadata"]["hashes"]["md5"] == "stored-md5"
    assert verification["status"] == "verification_ok"
    assert verification["stored_hashes_are_verification"] is False
    assert segments["segment_count"] == 1
    assert ewf_stream["schema_version"] == "stage4_5.first_testing_ewf_stream.v1"
    assert root_listing["schema_version"] == "stage4_5.first_testing_root_listing.v1"
    assert "Metadata status: metadata_available" in summary
    assert "Verification status: verification_ok" in summary
    assert "EWF stream status:" in summary
    assert "Root listing:" in summary
    assert not any(section["section"] == "real_ewf_metadata" for section in unsupported["sections"])
    assert not any(section["section"] == "real_ewf_verification" for section in unsupported["sections"])
    assert not any(section["owner"] == "S4.5-IMP03" for section in unsupported["sections"])
    assert not any(section["owner"] == "S4.5-IMP05" for section in unsupported["sections"])
    assert later_artifacts_exist == [True, True, False, True, True]


def test_hash_image_option_writes_logical_image_hash_artifact(monkeypatch):
    monkeypatch.setattr(first_testing_api, "EwfImageByteStream", FakeHashEwfImageByteStream)
    handle = FakeHandle()
    adapter = PyewfEwfReaderAdapter(pyewf_module=FakePyewf(handle))

    with _dummy_first_testing_directory("image-hash-success") as directory:
        evidence_dir = directory / "evidence"
        _touch_files(evidence_dir, "sample.E01", "sample.E02")
        case_dir = directory / "case"
        output_dir = directory / "output"

        result = run_first_testing(
            evidence_dir / "sample.E01",
            case_path=case_dir,
            output_path=output_dir,
            adapter=adapter,
            hash_image=True,
            image_hash_chunk_size=7,
        )

        image_hash = json.loads((output_dir / "image-hash.json").read_text(encoding="utf-8"))
        metadata = json.loads((output_dir / "metadata.json").read_text(encoding="utf-8"))
        manifest = json.loads((case_dir / "run-manifest.json").read_text(encoding="utf-8"))
        summary = (case_dir / "command-summary.txt").read_text(encoding="utf-8")

    expected_digest = hashlib.sha256(FakeHashEwfImageByteStream.DATA).hexdigest()
    assert result["image_hash"]["requested"] is True
    assert result["image_hash"]["status"] == "completed"
    assert result["image_hash"]["bytes_hashed"] == len(FakeHashEwfImageByteStream.DATA)
    assert result["image_hash"]["hexdigest_available"] is True
    assert image_hash["schema_version"] == "stage4_5.image_hash.v1"
    assert image_hash["status"] == "completed"
    assert image_hash["algorithm"] == "sha256"
    assert image_hash["hexdigest"] == expected_digest
    assert metadata["metadata"]["hashes"]["md5"] == "stored-md5"
    assert image_hash["hexdigest"] != metadata["metadata"]["hashes"]["md5"]
    assert image_hash["byte_count_matches_media_size"] is True
    assert image_hash["source_kind"] == "ewf_logical_image"
    assert image_hash["adapter_name"] == "pyewf-reader"
    assert image_hash["segment_count"] == 2
    assert image_hash["provenance"]["stored_hashes_are_verification"] is False
    assert image_hash["provenance"]["segment_container_hash"] is False
    assert image_hash["provenance"]["selected_file_hash"] is False
    assert image_hash["read_only_asserted"] is True
    assert image_hash["source_modified"] is False
    assert manifest["image_hash"]["status"] == "completed"
    assert manifest["image_hash"]["artifact_path"].endswith("image-hash.json")
    assert "Image hash request: True (completed)" in summary
    assert expected_digest not in summary


def test_hash_image_dependency_unavailable_is_structured(monkeypatch):
    def fake_pyewf_adapter():
        return PyewfEwfReaderAdapter(
            pyewf_module=None,
            import_error=ImportError("No module named 'pyewf'"),
        )

    monkeypatch.setattr(first_testing_api, "PyewfEwfReaderAdapter", fake_pyewf_adapter)

    with _dummy_first_testing_directory("image-hash-dependency-unavailable") as directory:
        evidence_dir = directory / "evidence"
        _touch_files(evidence_dir, "sample.E01")
        case_dir = directory / "case"

        result = run_first_testing(
            evidence_dir / "sample.E01",
            case_path=case_dir,
            hash_image=True,
        )

        image_hash = json.loads(
            (case_dir / "outputs" / "image-hash.json").read_text(encoding="utf-8")
        )

    assert result["image_hash"]["requested"] is True
    assert result["image_hash"]["status"] == "dependency_unavailable"
    assert image_hash["status"] == "dependency_unavailable"
    assert image_hash["hexdigest"] is None
    assert image_hash["bytes_hashed"] == 0
    assert "dependency_unavailable" in [warning["code"] for warning in image_hash["warnings"]]


def test_hash_image_with_stub_adapter_does_not_hash_stub_bytes():
    with _dummy_first_testing_directory("image-hash-stub-refusal") as directory:
        evidence_dir = directory / "evidence"
        _touch_files(evidence_dir, "sample.E01")
        case_dir = directory / "case"

        result = run_first_testing(
            evidence_dir / "sample.E01",
            case_path=case_dir,
            adapter_name="stub",
            hash_image=True,
        )

        image_hash = json.loads(
            (case_dir / "outputs" / "image-hash.json").read_text(encoding="utf-8")
        )

    assert result["image_hash"]["status"] == "stream_unavailable"
    assert image_hash["status"] == "stream_unavailable"
    assert image_hash["hexdigest"] is None
    assert "stub_adapter_image_hash_not_supported" in [
        warning["code"] for warning in image_hash["warnings"]
    ]


def test_first_testing_manifest_can_record_real_parser_backed_root_listing(monkeypatch):
    def fake_demo_artifacts(*, selected_path, intake_result, adapter_name):
        entry = {
            "path": "/Users",
            "name": "Users",
            "entry_type": "directory",
            "adapter_name": "pytsk3-filesystem-adapter",
            "read_only": True,
        }
        return {
            "ewf_stream": {
                "schema_version": "stage4_5.first_testing_ewf_stream.v1",
                "status": "ok",
                "logical_media_size": 4096,
            },
            "volumes": {
                "schema_version": "stage4_5.first_testing_volumes.v1",
                "status": "ok",
                "strategy": "partition_table",
                "volume_count": 1,
            },
            "filesystems": {
                "schema_version": "stage4_5.first_testing_filesystems.v1",
                "status": "ok",
                "filesystem_count": 1,
                "filesystems": [],
            },
            "root_listing": {
                "schema_version": "stage4_5.first_testing_root_listing.v1",
                "status": "ok",
                "parser_backing": "real_parser_backed",
                "entry_count": 1,
                "entries": [entry],
            },
            "demo_readiness": {
                "schema_version": "stage4_5.first_testing_demo_readiness.v1",
                "status": "real_parser_backed_root_listing_available",
                "root_entry_count": 1,
                "root_listing_parser_backing": "real_parser_backed",
            },
        }

    monkeypatch.setattr(first_testing_api, "_filesystem_demo_artifacts", fake_demo_artifacts)
    with _dummy_first_testing_directory("parser-backed-manifest") as directory:
        evidence_dir = directory / "evidence"
        _touch_files(evidence_dir, "sample.E01")
        case_dir = directory / "case"
        output_dir = directory / "output"

        result = run_first_testing(
            evidence_dir / "sample.E01",
            case_path=case_dir,
            output_path=output_dir,
            adapter_name="stub",
        )
        root_listing = json.loads((output_dir / "root-listing.json").read_text(encoding="utf-8"))
        demo_readiness = json.loads(
            (output_dir / "demo-readiness.json").read_text(encoding="utf-8")
        )

    assert result["ewf_stream"]["status"] == "ok"
    assert result["volumes"]["volume_count"] == 1
    assert result["filesystem"]["status"] == "ok"
    assert result["root_listing"]["parser_backing"] == "real_parser_backed"
    assert result["root_listing"]["entry_count"] == 1
    assert root_listing["entries"][0]["adapter_name"] == "pytsk3-filesystem-adapter"
    assert demo_readiness["status"] == "real_parser_backed_root_listing_available"


def test_first_testing_writes_file_list_csv_manifest_and_static_html(monkeypatch):
    monkeypatch.setattr(
        first_testing_api,
        "_filesystem_demo_artifacts",
        _fake_file_list_demo_artifacts,
    )

    with _dummy_first_testing_directory("file-list-output") as directory:
        evidence_dir = directory / "evidence"
        _touch_files(evidence_dir, "sample.E01")
        selected_path = evidence_dir / "sample.E01"
        case_dir = directory / "case"
        output_dir = directory / "output"

        result = run_first_testing(
            selected_path,
            case_path=case_dir,
            output_path=output_dir,
            case_name="<Case & Review>",
            adapter_name="stub",
            redact_paths=True,
        )
        file_list = json.loads((output_dir / "file-list.json").read_text(encoding="utf-8"))
        manifest = json.loads((case_dir / "run-manifest.json").read_text(encoding="utf-8"))
        summary = (case_dir / "command-summary.txt").read_text(encoding="utf-8")
        html_summary = (output_dir / "reports" / "summary.html").read_text(encoding="utf-8")
        with (output_dir / "file-list.csv").open("r", encoding="utf-8", newline="") as handle:
            csv_rows = list(csv.reader(handle))
        unsupported = json.loads(
            (output_dir / "unsupported-sections.json").read_text(encoding="utf-8")
        )

    assert result["file_list"]["status"] == "ok"
    assert result["file_list"]["entry_count"] == 2
    assert file_list["schema_version"] == "stage4_5.file_list.v1"
    assert file_list["status"]["code"] == "ok"
    assert file_list["parser_backing"] == "real_parser_backed"
    assert file_list["entry_count"] == 2
    assert file_list["source_path"] == str(selected_path.resolve())
    assert file_list["redacted_source_path"].startswith("<EVIDENCE_ROOT>")
    assert file_list["entries"][0]["case_id"] == result["case"]["case_id"]
    assert file_list["entries"][0]["evidence_id"] == result["evidence"]["evidence_id"]
    assert file_list["entries"][0]["warning_codes"] == ["entry_warning"]
    assert csv_rows[0] == list(FILE_LIST_CSV_HEADERS)
    assert csv_rows[1][csv_rows[0].index("name")].startswith("'=SUM")
    assert '"quoted"' in csv_rows[1][csv_rows[0].index("name")]
    assert manifest["file_list"]["status"] == "ok"
    assert manifest["file_list"]["entry_count"] == 2
    assert manifest["file_list"]["json_path"].endswith("file-list.json")
    assert manifest["file_list"]["csv_path"].endswith("file-list.csv")
    assert manifest["file_list"]["html_summary_path"].endswith("summary.html")
    assert "File list status: ok" in summary
    assert "File list entries: 2" in summary
    assert "summary.html" in summary
    assert str(evidence_dir.resolve()) not in summary
    assert "&lt;Case &amp; Review&gt;" in html_summary
    assert "File-list status" in html_summary
    assert "directory: 1, file: 1" in html_summary
    assert str(evidence_dir.resolve()) not in html_summary
    assert "<script" not in html_summary.lower()
    assert "http://" not in html_summary.lower()
    assert "https://" not in html_summary.lower()
    assert not any(section["owner"] == "S4.5-IMP05" for section in unsupported["sections"])
    assert not (output_dir / "search-index.json").exists()
    assert not (output_dir / "timeline.json").exists()


def test_first_testing_selected_file_artifacts_use_explicit_selection(monkeypatch):
    monkeypatch.setattr(
        first_testing_api,
        "_filesystem_demo_artifacts",
        _fake_selected_file_demo_artifacts,
    )
    monkeypatch.setattr(
        first_testing_api,
        "E01SelectedFileContentReader",
        FakeSelectedFileContentReader,
    )

    with _dummy_first_testing_directory("selected-file") as directory:
        evidence_dir = directory / "evidence"
        _touch_files(evidence_dir, "sample.E01")
        case_dir = directory / "case"
        output_dir = directory / "output"
        export_dir = directory / "exports"

        result = run_first_testing(
            evidence_dir / "sample.E01",
            case_path=case_dir,
            output_path=output_dir,
            adapter_name="stub",
            selected_file_id="volume-0:42",
            selected_file_export_dir=export_dir,
            selected_file_export_name="selected.bin",
        )
        readiness = json.loads(
            (output_dir / "selected-file-readiness.json").read_text(encoding="utf-8")
        )
        preview = json.loads(
            (output_dir / "selected-file-preview.json").read_text(encoding="utf-8")
        )
        analysis = json.loads(
            (output_dir / "selected-file-analysis.json").read_text(encoding="utf-8")
        )
        export = json.loads(
            (output_dir / "selected-file-export.json").read_text(encoding="utf-8")
        )
        exported_bytes = (export_dir / "selected.bin").read_bytes()
        later_artifacts_exist = [
            (output_dir / "file-list.json").exists(),
            (output_dir / "file-list.csv").exists(),
            any(output_dir.rglob("*.html")),
        ]

    assert result["selected_file"]["requested"] is True
    assert result["selected_file"]["selection_status"] == "ok"
    assert result["selected_file"]["preview"]["status"] == "ok"
    assert result["selected_file"]["analysis"]["hash_status"] == "ok"
    assert result["selected_file"]["analysis"]["signature_status"] == "ok"
    assert result["selected_file"]["export"]["status"] == "ok"
    assert readiness["status"]["code"] == "ok"
    assert readiness["source_kind"] == "real_parser"
    assert preview["status"] == "ok"
    assert preview["preview"]["provider"]["name"] == "e01-preview-content-provider"
    assert analysis["hash"]["status"]["code"] == "ok"
    assert analysis["hash"]["content_source"]["source_kind"] == "real_parser"
    assert analysis["signature"]["status"]["code"] == "ok"
    assert analysis["signature"]["detected_type"] == "pdf"
    assert export["status"] == "ok"
    assert export["export"]["content_source"]["source_kind"] == "real_parser"
    assert exported_bytes == SELECTED_BYTES
    assert result["file_list"]["entry_count"] == 1
    assert later_artifacts_exist == [True, True, True]


def test_e02_primary_input_is_rejected_before_artifact_writes():
    with _dummy_first_testing_directory("reject-e02") as directory:
        evidence_dir = directory / "evidence"
        _touch_files(evidence_dir, "sample.E02")
        case_dir = directory / "case"
        output_dir = directory / "output"

        result = run_first_testing(
            evidence_dir / "sample.E02",
            case_path=case_dir,
            output_path=output_dir,
            adapter_name="stub",
        )
        case_exists = case_dir.exists()
        output_exists = output_dir.exists()

    assert result["status"] == "invalid_input"
    assert result["warnings"][0]["code"] == "select_first_e01_segment"
    assert not case_exists
    assert not output_exists


def test_evidence_case_overlap_is_rejected_before_artifact_writes():
    with _dummy_first_testing_directory("reject-overlap") as directory:
        evidence_dir = directory / "evidence"
        _touch_files(evidence_dir, "sample.E01")
        case_dir = evidence_dir / "case"
        output_dir = directory / "output"

        result = run_first_testing(
            evidence_dir / "sample.E01",
            case_path=case_dir,
            output_path=output_dir,
            adapter_name="stub",
        )
        case_exists = case_dir.exists()
        output_exists = output_dir.exists()

    assert result["status"] == "unsafe_output_path"
    assert result["warnings"][0]["code"] == "case_inside_evidence_dir"
    assert not case_exists
    assert not output_exists


def test_json_only_prints_parseable_manifest(capsys):
    with _dummy_first_testing_directory("json-only") as directory:
        evidence_dir = directory / "evidence"
        _touch_files(evidence_dir, "sample.E01")
        case_dir = directory / "case"

        exit_code = main(
            [
                str(evidence_dir / "sample.E01"),
                "--case",
                str(case_dir),
                "--adapter",
                "stub",
                "--json-only",
            ]
        )

    parsed = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert parsed["status"] == "ok_with_unsupported_sections"
    assert parsed["schema_version"] == FIRST_TESTING_RUN_SCHEMA_VERSION


def test_default_pyewf_cli_dependency_unavailable_still_writes_artifacts(monkeypatch, capsys):
    def fake_pyewf_adapter():
        return PyewfEwfReaderAdapter(
            pyewf_module=None,
            import_error=ImportError("No module named 'pyewf'"),
        )

    monkeypatch.setattr(first_testing_api, "PyewfEwfReaderAdapter", fake_pyewf_adapter)

    with _dummy_first_testing_directory("cli-pyewf-unavailable") as directory:
        evidence_dir = directory / "evidence"
        _touch_files(evidence_dir, "sample.E01")
        case_dir = directory / "case"

        exit_code = main(
            [
                str(evidence_dir / "sample.E01"),
                "--case",
                str(case_dir),
            ]
        )
        console = capsys.readouterr().out
        metadata = json.loads((case_dir / "outputs" / "metadata.json").read_text(encoding="utf-8"))
        verification = json.loads(
            (case_dir / "outputs" / "verification.json").read_text(encoding="utf-8")
        )

    assert exit_code == 0
    assert "Metadata status: metadata_unavailable" in console
    assert "Verification status: not_run" in console
    assert metadata["status"] == "metadata_unavailable"
    assert verification["status"] == "not_run"


def test_redact_paths_redacts_console_and_summary_but_not_local_json(capsys):
    with _dummy_first_testing_directory("redact-paths") as directory:
        evidence_dir = directory / "evidence & root"
        _touch_files(evidence_dir, "sample.E01")
        selected_path = evidence_dir / "sample.E01"
        case_dir = directory / "case"

        exit_code = main(
            [
                str(selected_path),
                "--case",
                str(case_dir),
                "--adapter",
                "stub",
                "--redact-paths",
            ]
        )

        console = capsys.readouterr().out
        summary = (case_dir / "command-summary.txt").read_text(encoding="utf-8")
        html_summary = (case_dir / "outputs" / "reports" / "summary.html").read_text(
            encoding="utf-8"
        )
        intake = json.loads((case_dir / "outputs" / "intake.json").read_text(encoding="utf-8"))
        file_list = json.loads(
            (case_dir / "outputs" / "file-list.json").read_text(encoding="utf-8")
        )

    assert exit_code == 0
    assert "<EVIDENCE_ROOT>" in console
    assert "<EVIDENCE_ROOT>" in summary
    assert str(evidence_dir.resolve()) not in console
    assert str(evidence_dir.resolve()) not in summary
    assert str(evidence_dir.resolve()) not in html_summary
    assert intake["source_path"] == str(selected_path.resolve())
    assert intake["selected_path"] == str(selected_path.resolve())
    assert file_list["source_path"] == str(selected_path.resolve())
    assert file_list["redacted_source_path"].startswith("<EVIDENCE_ROOT>")


def test_first_testing_does_not_create_search_timeline_or_report_system_artifacts():
    with _dummy_first_testing_directory("no-search-timeline-artifacts") as directory:
        evidence_dir = directory / "evidence"
        _touch_files(evidence_dir, "sample.E01")
        case_dir = directory / "case"
        output_dir = directory / "output"

        run_first_testing(
            evidence_dir / "sample.E01",
            case_path=case_dir,
            output_path=output_dir,
            adapter_name="stub",
        )
        file_list_json_exists = (output_dir / "file-list.json").exists()
        file_list_csv_exists = (output_dir / "file-list.csv").exists()
        html_artifacts = [path.name for path in output_dir.rglob("*.html")]
        forbidden_artifacts_exist = [
            (output_dir / "exports").exists(),
            (case_dir / "reports").exists(),
            (output_dir / "search-index.json").exists(),
            (output_dir / "search-results.json").exists(),
            (output_dir / "timeline.json").exists(),
            (output_dir / "timeline-events.json").exists(),
            (output_dir / "reports" / "search.html").exists(),
            (output_dir / "reports" / "timeline.html").exists(),
        ]

    assert file_list_json_exists
    assert file_list_csv_exists
    assert html_artifacts == ["summary.html"]
    assert forbidden_artifacts_exist == [False, False, False, False, False, False, False, False]
