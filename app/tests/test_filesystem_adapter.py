"""Tests for the S2-T04 filesystem adapter boundary."""

import json
from pathlib import Path
import shutil

from app.backend.forensic_core import (
    FILESYSTEM_ADAPTER_SCHEMA_VERSION,
    LocalFileImageStream,
    Pytsk3FilesystemAdapter,
    StubFilesystemAdapter,
    VolumeDiscoveryStatus,
    VolumeInfo,
)


class FakeImgInfo:
    def __init__(self, *args, **kwargs):
        pass


class FakeName:
    def __init__(self, name, flags=1, meta_addr=42):
        self.name = name
        self.flags = flags
        self.meta_addr = meta_addr


class FakeMeta:
    def __init__(self, meta_type, addr, size):
        self.type = meta_type
        self.addr = addr
        self.size = size
        self.crtime = 0
        self.mtime = 1_700_000_000
        self.atime = 0
        self.ctime = 0


class FakeEntryInfo:
    def __init__(self, name, meta):
        self.name = name
        self.meta = meta


class FakeEntry:
    def __init__(self, name, meta_type, addr, size):
        self.info = FakeEntryInfo(
            FakeName(name.encode("utf-8"), meta_addr=addr),
            FakeMeta(meta_type, addr, size),
        )


class FakeFsInfo:
    def __init__(self, ftype):
        self.ftype = ftype


class FakeFs:
    def __init__(self, module):
        self.info = FakeFsInfo(module.TSK_FS_TYPE_NTFS)
        self._module = module

    def open_dir(self, path="/"):
        if path == "/":
            return [
                FakeEntry(".", self._module.TSK_FS_META_TYPE_DIR, 1, 0),
                FakeEntry("Users", self._module.TSK_FS_META_TYPE_DIR, 2, 0),
                FakeEntry("note.txt", self._module.TSK_FS_META_TYPE_REG, 3, 12),
            ]
        if path == "/Users":
            return [
                FakeEntry(".", self._module.TSK_FS_META_TYPE_DIR, 2, 0),
                FakeEntry("Profile", self._module.TSK_FS_META_TYPE_DIR, 4, 0),
                FakeEntry("nested.txt", self._module.TSK_FS_META_TYPE_REG, 5, 20),
            ]
        raise OSError("path not found")

    def open(self, path="/"):
        if path == "/Users":
            return FakeEntry("Users", self._module.TSK_FS_META_TYPE_DIR, 2, 0)
        if path == "/Users/nested.txt":
            return FakeEntry("nested.txt", self._module.TSK_FS_META_TYPE_REG, 5, 20)
        raise OSError("path not found")


class FakePytsk3:
    TSK_IMG_TYPE_EXTERNAL = 0
    TSK_FS_META_TYPE_DIR = 1
    TSK_FS_META_TYPE_REG = 2
    TSK_FS_META_TYPE_LNK = 3
    TSK_FS_NAME_FLAG_ALLOC = 1
    TSK_FS_NAME_FLAG_UNALLOC = 2
    TSK_FS_TYPE_NTFS = 99
    Img_Info = FakeImgInfo

    @staticmethod
    def FS_Info(_image_info, offset=0):
        return FakeFs(FakePytsk3)


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


def _filesystem_fixture_directory(name: str) -> Path:
    root = Path.cwd() / ".test-artifacts" / "filesystem-adapter"
    directory = root / name
    if directory.exists():
        shutil.rmtree(directory, ignore_errors=True)
    directory.mkdir(parents=True)
    return directory


def test_stub_filesystem_result_shape_and_metadata():
    adapter = StubFilesystemAdapter()

    result = adapter.inspect_volume(_sample_volume())

    assert result.schema_version == FILESYSTEM_ADAPTER_SCHEMA_VERSION
    assert result.adapter_name == "stub-filesystem-adapter"
    assert result.adapter_available is True
    assert result.dependency.available is True
    assert result.filesystem_type == "stubfs"
    assert result.status.code == "ok"
    assert result.root_path == "/"
    assert result.read_only is True
    assert [warning.code for warning in result.warnings] == ["stub_filesystem"]


def test_stub_filesystem_returns_deterministic_root_entries():
    result = StubFilesystemAdapter().inspect_volume(_sample_volume())

    entries = result.entries

    assert [entry.path for entry in entries] == ["/Documents", "/hello.txt"]
    assert [entry.name for entry in entries] == ["Documents", "hello.txt"]
    assert [entry.entry_type for entry in entries] == ["directory", "file"]
    assert entries[0].file_id == "stub-dir-documents"
    assert entries[1].file_id == "stub-file-hello"
    assert entries[1].size == 13
    assert all(entry.allocated is True for entry in entries)
    assert all(entry.deleted is False for entry in entries)


def test_stub_filesystem_entries_preserve_read_only_provenance():
    volume = _sample_volume()
    result = StubFilesystemAdapter().inspect_volume(volume)

    for entry in result.entries:
        assert entry.source_path == volume.source_path
        assert entry.volume_id == volume.volume_id
        assert entry.volume_offset == volume.offset
        assert entry.volume_length == volume.length
        assert entry.filesystem_type == result.filesystem_type
        assert entry.adapter_name == result.adapter_name
        assert entry.read_only is True
        assert entry.status.code == "ok"


def test_pytsk3_dependency_unavailable_behavior_is_structured():
    adapter = Pytsk3FilesystemAdapter(
        pytsk3_module=None,
        import_error=ImportError("No module named 'pytsk3'"),
    )

    result = adapter.inspect_volume(_sample_volume())

    assert adapter.is_available is False
    assert result.adapter_name == "pytsk3-filesystem-adapter"
    assert result.adapter_available is False
    assert result.dependency.name == "pytsk3"
    assert result.dependency.available is False
    assert "pytsk3 is not installed" in result.dependency.message
    assert result.status.code == "dependency_unavailable"
    assert result.entries == ()
    assert result.read_only is True
    assert [warning.code for warning in result.warnings] == ["dependency_unavailable"]


def test_filesystem_result_shape_is_json_serializable():
    result_dict = StubFilesystemAdapter().inspect_volume(_sample_volume()).to_dict()
    parsed = json.loads(json.dumps(result_dict, sort_keys=True))

    assert parsed["schema_version"] == FILESYSTEM_ADAPTER_SCHEMA_VERSION
    assert parsed["adapter_name"] == "stub-filesystem-adapter"
    assert parsed["dependency"]["name"] == "stub"
    assert parsed["volume_id"] == "volume-0"
    assert parsed["entries"][0]["path"] == "/Documents"
    assert parsed["entries"][0]["timestamps"]["created"] is None
    assert parsed["entries"][1]["deleted"] is False


def test_pytsk3_importable_skeleton_is_not_reported_as_ok():
    class FakePytsk3:
        __version__ = "test-version"

    result = Pytsk3FilesystemAdapter(pytsk3_module=FakePytsk3()).inspect_volume(
        _sample_volume()
    )

    assert result.adapter_available is True
    assert result.dependency.available is True
    assert result.status.code == "real_parser_not_implemented"
    assert result.entries == ()
    assert [warning.code for warning in result.warnings] == [
        "real_parser_not_implemented"
    ]


def test_pytsk3_fake_parser_maps_root_entries():
    directory = _filesystem_fixture_directory("fake-parser")
    try:
        source = directory / "tiny.raw"
        source.write_bytes(b"\0" * 4096)
        volume = _sample_volume()

        result = Pytsk3FilesystemAdapter(
            pytsk3_module=FakePytsk3,
            image_stream=LocalFileImageStream(source),
        ).inspect_volume(volume)
    finally:
        shutil.rmtree(directory, ignore_errors=True)

    assert result.status.code == "ok"
    assert result.adapter_available is True
    assert result.filesystem_type == "ntfs"
    assert [entry.path for entry in result.entries] == ["/Users", "/note.txt"]
    assert [entry.entry_type for entry in result.entries] == ["directory", "file"]
    assert result.entries[1].size == 12
    assert result.entries[1].adapter_name == "pytsk3-filesystem-adapter"
    assert result.entries[1].read_only is True
    assert result.warnings[0].code == "real_parser_backed"


def test_pytsk3_fake_parser_lists_nested_directory_entries():
    directory = _filesystem_fixture_directory("fake-parser-nested")
    try:
        source = directory / "tiny.raw"
        source.write_bytes(b"\0" * 4096)
        volume = _sample_volume()

        result = Pytsk3FilesystemAdapter(
            pytsk3_module=FakePytsk3,
            image_stream=LocalFileImageStream(source),
        ).list_directory(volume, "/Users")
    finally:
        shutil.rmtree(directory, ignore_errors=True)

    assert result.status.code == "ok"
    assert result.root_path == "/Users"
    assert [entry.path for entry in result.entries] == ["/Users/Profile", "/Users/nested.txt"]
    assert [entry.entry_type for entry in result.entries] == ["directory", "file"]
    assert result.entries[1].size == 20
    assert result.warnings[0].code == "real_parser_backed"


def test_pytsk3_fake_parser_reports_nested_file_path_not_directory():
    directory = _filesystem_fixture_directory("fake-parser-file-path")
    try:
        source = directory / "tiny.raw"
        source.write_bytes(b"\0" * 4096)
        volume = _sample_volume()

        result = Pytsk3FilesystemAdapter(
            pytsk3_module=FakePytsk3,
            image_stream=LocalFileImageStream(source),
        ).list_directory(volume, "/Users/nested.txt")
    finally:
        shutil.rmtree(directory, ignore_errors=True)

    assert result.status.code == "path_not_directory"
    assert result.entries == ()
    assert result.root_path == "/Users/nested.txt"
    assert result.warnings[0].code == "path_not_directory"
