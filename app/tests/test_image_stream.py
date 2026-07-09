"""Tests for the S2-T02 read-only image byte-stream abstraction."""

from contextlib import contextmanager
from pathlib import Path
import shutil

from app.backend.forensic_core import LocalFileImageStream


@contextmanager
def _stream_fixture_directory(name: str):
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


def _write_bytes(path: Path, data: bytes) -> None:
    path.write_bytes(data)


def test_local_file_stream_reports_source_metadata_and_read_only_status():
    with _stream_fixture_directory("image-stream-metadata") as directory:
        source_path = directory / "tiny.raw"
        _write_bytes(source_path, b"abcdef")

        info = LocalFileImageStream(source_path).describe()
        info_dict = info.to_dict()

    assert info.status.code == "ok"
    assert info.status.ok is True
    assert info.is_readable is True
    assert info.size == 6
    assert info.stream_type == "local-file"
    assert info.read_only is True
    assert info.source_path.endswith("tiny.raw")
    assert info_dict["status"]["code"] == "ok"
    assert info_dict["read_only"] is True


def test_local_file_stream_reads_bounded_byte_range():
    with _stream_fixture_directory("image-stream-range") as directory:
        source_path = directory / "tiny.raw"
        _write_bytes(source_path, b"0123456789")

        result = LocalFileImageStream(source_path).read_at(2, 4)

    assert result.status.code == "ok"
    assert result.read_only is True
    assert result.offset == 2
    assert result.length == 4
    assert result.source_size == 10
    assert result.data == b"2345"
    assert result.bytes_read == 4


def test_local_file_stream_reads_from_offset_zero():
    with _stream_fixture_directory("image-stream-offset-zero") as directory:
        source_path = directory / "tiny.raw"
        _write_bytes(source_path, b"header-data")

        result = LocalFileImageStream(source_path).read_at(0, 6)

    assert result.status.code == "ok"
    assert result.offset == 0
    assert result.data == b"header"


def test_local_file_stream_truncates_range_that_extends_beyond_eof():
    with _stream_fixture_directory("image-stream-truncated") as directory:
        source_path = directory / "tiny.raw"
        _write_bytes(source_path, b"abcdef")

        result = LocalFileImageStream(source_path).read_at(4, 10)

    assert result.status.code == "ok"
    assert result.data == b"ef"
    assert result.bytes_read == 2
    assert result.source_size == 6
    assert [warning.code for warning in result.warnings] == ["read_truncated_at_eof"]


def test_local_file_stream_reports_read_offset_beyond_eof():
    with _stream_fixture_directory("image-stream-beyond-eof") as directory:
        source_path = directory / "tiny.raw"
        _write_bytes(source_path, b"abcdef")

        result = LocalFileImageStream(source_path).read_at(7, 3)

    assert result.status.code == "read_beyond_end"
    assert result.data == b""
    assert result.bytes_read == 0
    assert result.source_size == 6


def test_local_file_stream_reports_missing_path_as_structured_status():
    with _stream_fixture_directory("image-stream-missing") as directory:
        source_path = directory / "missing.raw"

        stream = LocalFileImageStream(source_path)
        info = stream.describe()
        result = stream.read_at(0, 4)

    assert info.status.code == "missing_path"
    assert info.size is None
    assert info.read_only is True
    assert result.status.code == "missing_path"
    assert result.data == b""


def test_local_file_stream_reports_directory_path_as_structured_status():
    with _stream_fixture_directory("image-stream-directory") as directory:
        stream = LocalFileImageStream(directory)

        info = stream.describe()
        result = stream.read_at(0, 4)

    assert info.status.code == "path_is_directory"
    assert info.size is None
    assert result.status.code == "path_is_directory"
    assert result.data == b""


def test_local_file_stream_rejects_negative_offset():
    with _stream_fixture_directory("image-stream-negative-offset") as directory:
        source_path = directory / "tiny.raw"
        _write_bytes(source_path, b"abcdef")

        result = LocalFileImageStream(source_path).read_at(-1, 2)

    assert result.status.code == "invalid_range"
    assert result.data == b""
    assert result.source_size is None


def test_local_file_stream_rejects_negative_length():
    with _stream_fixture_directory("image-stream-negative-length") as directory:
        source_path = directory / "tiny.raw"
        _write_bytes(source_path, b"abcdef")

        result = LocalFileImageStream(source_path).read_at(0, -1)

    assert result.status.code == "invalid_range"
    assert result.data == b""
    assert result.source_size is None


def test_local_file_stream_allows_zero_length_read():
    with _stream_fixture_directory("image-stream-zero-length") as directory:
        source_path = directory / "tiny.raw"
        _write_bytes(source_path, b"abcdef")

        result = LocalFileImageStream(source_path).read_at(3, 0)

    assert result.status.code == "ok"
    assert result.data == b""
    assert result.bytes_read == 0
    assert result.source_size == 6
