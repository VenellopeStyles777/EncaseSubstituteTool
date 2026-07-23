"""Tests for the S2-T05 backend directory listing view."""

import json

from app.backend.api.directory_listing import (
    DIRECTORY_LISTING_SCHEMA_VERSION,
    directory_listing_to_json,
    list_directory,
)
from app.backend.forensic_core import (
    FilesystemDependencyStatus,
    FilesystemEntry,
    FilesystemResult,
    FilesystemStatus,
    Pytsk3FilesystemAdapter,
    StubFilesystemAdapter,
    VolumeDiscoveryStatus,
    VolumeInfo,
)


def _sample_volume() -> VolumeInfo:
    return VolumeInfo(
        volume_id="volume-0",
        volume_index=0,
        source_path="C:/fixtures/tiny.raw",
        stream_type="local-file",
        source_size=1024,
        offset=0,
        length=1024,
        volume_type="whole_image",
        description="Whole image test volume.",
        read_only=True,
        status=VolumeDiscoveryStatus(
            code="ok",
            message="Whole-image volume discovered.",
        ),
    )


class FakeParserBackedNestedAdapter:
    name = "pytsk3-filesystem-adapter"
    read_only = True

    @property
    def is_available(self):
        return True

    def dependency_status(self):
        return FilesystemDependencyStatus(
            name="pytsk3",
            available=True,
            message="fake parser available",
        )

    def inspect_volume(self, volume):
        return self._result(
            volume,
            root_path="/",
            entries=(
                self._entry(volume, file_id="volume-0:2", path="/Users", name="Users", entry_type="directory"),
                self._entry(volume, file_id="volume-0:3", path="/note.txt", name="note.txt", entry_type="file"),
            ),
        )

    def list_directory(self, volume, directory_path):
        if directory_path == "/Users/nested.txt":
            return self._result(
                volume,
                root_path=directory_path,
                status=FilesystemStatus("path_not_directory", "fake path is a file"),
                entries=(),
            )
        if directory_path != "/Users":
            return self._result(
                volume,
                root_path=directory_path,
                status=FilesystemStatus("path_not_found", "fake path not found"),
                entries=(),
            )
        return self._result(
            volume,
            root_path="/Users",
            entries=(
                self._entry(volume, file_id="volume-0:4", path="/Users/Profile", name="Profile", entry_type="directory"),
                self._entry(volume, file_id="volume-0:5", path="/Users/nested.txt", name="nested.txt", entry_type="file"),
            ),
        )

    def _result(self, volume, *, root_path, entries, status=None):
        return FilesystemResult(
            schema_version="stage2.filesystem_adapter.v1",
            adapter_name=self.name,
            adapter_available=True,
            dependency=self.dependency_status(),
            source_path=volume.source_path,
            volume_id=volume.volume_id,
            volume_offset=volume.offset,
            volume_length=volume.length,
            filesystem_type="ntfs",
            read_only=True,
            status=status or FilesystemStatus("ok", "fake listing ok"),
            root_path=root_path,
            entries=entries,
        )

    def _entry(self, volume, *, file_id, path, name, entry_type):
        return FilesystemEntry(
            file_id=file_id,
            path=path,
            name=name,
            entry_type=entry_type,
            size=10 if entry_type == "file" else 0,
            allocated=True,
            deleted=False,
            source_path=volume.source_path,
            volume_id=volume.volume_id,
            volume_offset=volume.offset,
            volume_length=volume.length,
            filesystem_type="ntfs",
            adapter_name=self.name,
            read_only=True,
            status=FilesystemStatus("ok", "fake entry ok"),
            timestamps={
                "created": None,
                "modified": None,
                "accessed": None,
                "metadata_changed": None,
            },
        )


def test_stub_root_listing_returns_deterministic_entries():
    result = list_directory(_sample_volume(), "/", StubFilesystemAdapter())

    assert result["schema_version"] == DIRECTORY_LISTING_SCHEMA_VERSION
    assert result["status"]["code"] == "ok"
    assert result["directory_path"] == "/"
    assert result["entry_count"] == 2
    assert [entry["path"] for entry in result["entries"]] == [
        "/Documents",
        "/hello.txt",
    ]
    assert [entry["entry_type"] for entry in result["entries"]] == [
        "directory",
        "file",
    ]


def test_directory_listing_response_is_json_serializable():
    parsed = json.loads(
        directory_listing_to_json(
            _sample_volume(),
            "/",
            StubFilesystemAdapter(),
        )
    )

    assert parsed["schema_version"] == DIRECTORY_LISTING_SCHEMA_VERSION
    assert parsed["status"]["code"] == "ok"
    assert parsed["entries"][0]["name"] == "Documents"
    assert parsed["entries"][1]["size"] == 13


def test_listing_entries_preserve_provenance_and_read_only_fields():
    volume = _sample_volume()
    result = list_directory(volume, "/", StubFilesystemAdapter())

    assert result["source_path"] == volume.source_path
    assert result["volume_id"] == volume.volume_id
    assert result["volume_offset"] == volume.offset
    assert result["volume_length"] == volume.length
    assert result["filesystem_type"] == "stubfs"
    assert result["adapter"]["name"] == "stub-filesystem-adapter"
    assert result["read_only"] is True

    for entry in result["entries"]:
        assert entry["source_path"] == volume.source_path
        assert entry["volume_id"] == volume.volume_id
        assert entry["volume_offset"] == volume.offset
        assert entry["volume_length"] == volume.length
        assert entry["filesystem_type"] == "stubfs"
        assert entry["adapter_name"] == "stub-filesystem-adapter"
        assert entry["read_only"] is True
        assert entry["allocated"] is True
        assert entry["deleted"] is False
        assert set(entry["timestamps"]) == {
            "created",
            "modified",
            "accessed",
            "metadata_changed",
        }


def test_nested_directory_path_is_structured_unsupported_status():
    result = list_directory(_sample_volume(), "/Documents", StubFilesystemAdapter())

    assert result["status"]["code"] == "path_unsupported"
    assert result["status"]["ok"] is False
    assert result["directory_path"] == "/Documents"
    assert result["entry_count"] == 0
    assert result["entries"] == []
    assert [warning["code"] for warning in result["warnings"]] == [
        "stub_filesystem",
        "nested_listing_deferred",
    ]


def test_file_path_is_not_treated_as_directory():
    result = list_directory(_sample_volume(), "/hello.txt", StubFilesystemAdapter())

    assert result["status"]["code"] == "path_not_directory"
    assert result["entry_count"] == 0
    assert result["entries"] == []
    assert result["warnings"][-1]["code"] == "path_not_directory"


def test_unknown_path_returns_structured_not_found_status():
    result = list_directory(_sample_volume(), "/missing", StubFilesystemAdapter())

    assert result["status"]["code"] == "path_not_found"
    assert result["entry_count"] == 0
    assert result["entries"] == []
    assert result["warnings"][-1]["code"] == "path_not_found"


def test_directory_path_normalization_is_deterministic():
    volume = _sample_volume()
    adapter = StubFilesystemAdapter()

    empty_result = list_directory(volume, "", adapter)
    no_slash_result = list_directory(volume, "Documents/", adapter)

    assert empty_result["status"]["code"] == "ok"
    assert empty_result["directory_path"] == "/"
    assert no_slash_result["status"]["code"] == "path_unsupported"
    assert no_slash_result["directory_path"] == "/Documents"


def test_parser_backed_adapter_lists_nested_directory_path():
    result = list_directory(
        _sample_volume(),
        "Users/",
        FakeParserBackedNestedAdapter(),
    )

    assert result["status"]["code"] == "ok"
    assert result["directory_path"] == "/Users"
    assert result["entry_count"] == 2
    assert [entry["path"] for entry in result["entries"]] == [
        "/Users/Profile",
        "/Users/nested.txt",
    ]
    assert [entry["entry_type"] for entry in result["entries"]] == ["directory", "file"]


def test_parser_backed_adapter_reports_nested_file_path_not_directory():
    result = list_directory(
        _sample_volume(),
        "/Users/nested.txt",
        FakeParserBackedNestedAdapter(),
    )

    assert result["status"]["code"] == "path_not_directory"
    assert result["entry_count"] == 0
    assert result["entries"] == []
    assert result["filesystem_status"]["code"] == "path_not_directory"


def test_pytsk3_dependency_unavailable_is_not_successful_listing():
    adapter = Pytsk3FilesystemAdapter(
        pytsk3_module=None,
        import_error=ImportError("No module named 'pytsk3'"),
    )

    result = list_directory(_sample_volume(), "/", adapter)

    assert result["status"]["code"] == "filesystem_unavailable"
    assert result["status"]["ok"] is False
    assert result["adapter"]["name"] == "pytsk3-filesystem-adapter"
    assert result["adapter"]["available"] is False
    assert result["adapter"]["dependency"]["available"] is False
    assert result["filesystem_status"]["code"] == "dependency_unavailable"
    assert result["entry_count"] == 0
    assert result["entries"] == []
    assert result["warnings"][-1]["code"] == "dependency_unavailable"


def test_pytsk3_importable_but_not_implemented_is_not_successful_listing():
    class FakePytsk3:
        __version__ = "test-version"

    result = list_directory(
        _sample_volume(),
        "/",
        Pytsk3FilesystemAdapter(pytsk3_module=FakePytsk3()),
    )

    assert result["status"]["code"] == "filesystem_unavailable"
    assert result["adapter"]["available"] is True
    assert result["adapter"]["dependency"]["available"] is True
    assert result["filesystem_status"]["code"] == "real_parser_not_implemented"
    assert result["entry_count"] == 0
    assert result["entries"] == []
