"""Tests for the S2-T04 filesystem adapter boundary."""

import json

from app.backend.forensic_core import (
    FILESYSTEM_ADAPTER_SCHEMA_VERSION,
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
