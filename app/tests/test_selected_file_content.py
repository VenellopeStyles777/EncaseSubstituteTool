"""Tests for S4.5-IMP04 selected-file E01 content providers."""

from contextlib import contextmanager
import hashlib
from pathlib import Path
import shutil

from app.backend.api.file_export import export_file
from app.backend.api.file_preview import preview_file
from app.backend.forensic_core import (
    E01AnalysisContentProvider,
    E01ExportContentProvider,
    E01PreviewContentProvider,
    E01SelectedFileContentReader,
    ImageReadResult,
    ImageStreamInfo,
    ImageStreamStatus,
    VolumeDiscoveryStatus,
    VolumeInfo,
    detect_file_signature,
    hash_file_content,
)


PDF_BYTES = b"%PDF-1.7\nhello parser bytes"


class FakeImgInfo:
    def __init__(self, url="", type=0):
        self.url = url
        self.type = type


class FakePytsk3:
    __version__ = "fake-pytsk3"
    Img_Info = FakeImgInfo
    TSK_IMG_TYPE_EXTERNAL = 0

    def __init__(self, data: bytes = PDF_BYTES, *, fail_read: bool = False) -> None:
        self.data = data
        self.fail_read = fail_read

    def FS_Info(self, image_info, offset=0):
        return FakeFilesystem(self.data, fail_read=self.fail_read)


class FakeFilesystem:
    def __init__(self, data: bytes, *, fail_read: bool) -> None:
        self.data = data
        self.fail_read = fail_read

    def open_meta(self, inode):
        assert inode == 42
        return FakeFile(self.data, fail_read=self.fail_read)

    def open(self, path):
        assert path == "/document.pdf"
        return FakeFile(self.data, fail_read=self.fail_read)


class FakeFile:
    def __init__(self, data: bytes, *, fail_read: bool) -> None:
        self.data = data
        self.fail_read = fail_read

    def read_random(self, offset: int, length: int) -> bytes:
        if self.fail_read:
            raise OSError("parser read failed")
        return self.data[offset : offset + length]

    def close(self) -> None:
        self.closed = True


class FakeImageStream:
    stream_type = "ewf"
    read_only = True
    source_path = "C:/evidence/disk.E01"

    def describe(self):
        return ImageStreamInfo(
            source_path=self.source_path,
            stream_type=self.stream_type,
            size=4096,
            read_only=True,
            status=ImageStreamStatus("ok", "ok", self.source_path),
        )

    def read_at(self, offset: int, length: int):
        return ImageReadResult(
            source_path=self.source_path,
            stream_type=self.stream_type,
            read_only=True,
            offset=offset,
            length=length,
            source_size=4096,
            data=b"\x00" * length,
            status=ImageStreamStatus("ok", "ok", self.source_path),
        )


@contextmanager
def _artifact_directory(name: str):
    root = Path.cwd() / ".test-artifacts" / "selected-file-content"
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


def _volume() -> VolumeInfo:
    return VolumeInfo(
        volume_id="volume-0",
        volume_index=0,
        source_path="C:/evidence/disk.E01",
        stream_type="ewf",
        source_size=4096,
        offset=512,
        length=2048,
        volume_type="ntfs",
        description="Fake NTFS partition",
        read_only=True,
        status=VolumeDiscoveryStatus("ok", "ok"),
    )


def _entry(**overrides: object) -> dict[str, object]:
    entry: dict[str, object] = {
        "file_id": "volume-0:42",
        "path": "/document.pdf",
        "name": "document.pdf",
        "entry_type": "file",
        "size": len(PDF_BYTES),
        "allocated": True,
        "deleted": False,
        "source_path": "C:/evidence/disk.E01",
        "volume_id": "volume-0",
        "volume_offset": 512,
        "volume_length": 2048,
        "filesystem_type": "ntfs",
        "adapter_name": "pytsk3-filesystem-adapter",
        "read_only": True,
        "timestamps": {},
    }
    entry.update(overrides)
    return entry


def _reader(entry: dict[str, object] | None = None, *, pytsk3=None) -> E01SelectedFileContentReader:
    return E01SelectedFileContentReader(
        FakeImageStream(),
        _volume(),
        entry or _entry(),
        pytsk3_module=pytsk3 if pytsk3 is not None else FakePytsk3(),
    )


def test_fake_parser_backed_reader_returns_bounded_real_parser_bytes():
    reader = _reader()

    result = reader.read_range(0, 8)

    assert result.status.code == "ok"
    assert result.data == PDF_BYTES[:8]
    assert result.source_kind == "real_parser"
    assert result.parser_name == "pytsk3"
    assert result.parser_version == "fake-pytsk3"
    assert result.read_only is True
    assert result.synthetic is False
    assert "real_parser_content" in [warning.code for warning in result.warnings]


def test_preview_wrapper_feeds_existing_preview_surface():
    provider = E01PreviewContentProvider(_reader(), max_preview_bytes=8)

    result = preview_file(_entry(), mode="hex", provider=provider, max_length=8)

    assert result["status"]["code"] == "ok"
    assert result["provider"]["name"] == "e01-preview-content-provider"
    assert result["preview"]["hex"] == PDF_BYTES[:8].hex()
    assert result["source_content_size"] == 8
    assert provider.last_result.status.code == "ok"
    assert "real_parser_content" in [warning["code"] for warning in result["warnings"]]


def test_export_wrapper_reuses_export_service_and_manifest_verification():
    provider = E01ExportContentProvider(_reader(), max_bytes=1024)

    with _artifact_directory("export") as directory:
        result = export_file(_entry(), directory / "exports", provider=provider)
        exported = Path(str(result.output_path)).read_bytes()

    assert result.status.code == "ok"
    assert exported == PDF_BYTES
    assert result.content_source.provider_name == "e01-export-content-provider"
    assert result.content_source.source_kind == "real_parser"
    assert result.content_source.synthetic is False
    assert result.hashes.sha256 == hashlib.sha256(PDF_BYTES).hexdigest()
    assert provider.last_result.status.code == "ok"


def test_analysis_wrappers_reuse_hash_and_signature_surfaces():
    full_provider = E01AnalysisContentProvider(_reader(), read_mode="full", max_bytes=1024)
    signature_provider = E01AnalysisContentProvider(
        _reader(),
        read_mode="bounded",
        max_bytes=8,
    )

    hash_result = hash_file_content(_entry(), provider=full_provider)
    signature_result = detect_file_signature(_entry(), provider=signature_provider, max_bytes=8)

    assert hash_result.status.code == "ok"
    assert hash_result.content_source.source_kind == "real_parser"
    assert hash_result.content_source.synthetic is False
    assert hash_result.digests[0].digest == hashlib.sha256(PDF_BYTES).hexdigest()
    assert signature_result.status.code == "ok"
    assert signature_result.detected_type == "pdf"
    assert signature_result.content_source.source_kind == "real_parser"
    assert full_provider.last_result.status.code == "ok"
    assert signature_provider.last_result.status.code == "ok"


def test_directory_deleted_and_stub_entries_are_refused_before_parser_reads():
    directory_result = _reader(_entry(entry_type="directory")).check()
    deleted_result = _reader(_entry(deleted=True)).check()
    stub_result = _reader(_entry(adapter_name="stub-filesystem-adapter")).check()

    assert directory_result.status.code == "path_not_file"
    assert deleted_result.status.code == "deleted_recovery_unsupported"
    assert stub_result.status.code == "metadata_only_source"


def test_large_file_full_read_is_refused_under_in_memory_policy():
    reader = _reader(_entry(size=2048))

    result = reader.read_full(max_bytes=1024)

    assert result.status.code == "file_too_large_for_in_memory_provider"
    assert result.data == b""
    assert "large_file_refused" in [warning.code for warning in result.warnings]


def test_parser_exception_becomes_structured_unreadable_status():
    reader = _reader(pytsk3=FakePytsk3(fail_read=True))

    result = reader.read_range(0, 8)

    assert result.status.code == "file_content_unreadable"
    assert result.data == b""
    assert "parser_content_unreadable" in [warning.code for warning in result.warnings]


def test_provider_never_labels_stub_bytes_as_real_parser_when_preflight_fails():
    provider = E01AnalysisContentProvider(
        _reader(_entry(adapter_name="stub-filesystem-adapter")),
        read_mode="full",
        max_bytes=1024,
    )

    result = hash_file_content(_entry(adapter_name="stub-filesystem-adapter"), provider=provider)

    assert result.status.code == "content_source_unavailable"
    assert result.content_source.source_content_size is None
    assert result.content_source.status.code == "content_source_unavailable"
    assert provider.last_result.status.code == "metadata_only_source"
    assert provider.last_result.source_kind == "metadata_only"
