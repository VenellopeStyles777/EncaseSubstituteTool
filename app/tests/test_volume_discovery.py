"""Tests for the S2-T03 volume discovery boundary."""

from contextlib import contextmanager
from pathlib import Path
import json
import shutil

from app.backend.forensic_core import (
    LocalFileImageStream,
    VOLUME_DISCOVERY_SCHEMA_VERSION,
    discover_volumes,
)


@contextmanager
def _volume_fixture_directory(name: str):
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


def test_discovers_whole_image_volume_for_non_empty_local_file():
    with _volume_fixture_directory("volume-whole-image") as directory:
        source_path = directory / "tiny.raw"
        _write_bytes(source_path, b"0123456789")

        result = discover_volumes(LocalFileImageStream(source_path))

    assert result.schema_version == VOLUME_DISCOVERY_SCHEMA_VERSION
    assert result.status.code == "ok"
    assert result.read_only is True
    assert result.stream_type == "local-file"
    assert result.source_size == 10
    assert len(result.volumes) == 1

    volume = result.volumes[0]
    assert volume.volume_id == "volume-0"
    assert volume.volume_index == 0
    assert volume.offset == 0
    assert volume.length == 10
    assert volume.volume_type == "whole_image"
    assert volume.status.code == "ok"
    assert volume.read_only is True
    assert volume.source_path == result.source_path


def test_zero_byte_source_returns_structured_empty_image_result():
    with _volume_fixture_directory("volume-empty-image") as directory:
        source_path = directory / "empty.raw"
        _write_bytes(source_path, b"")

        result = discover_volumes(LocalFileImageStream(source_path))

    assert result.status.code == "empty_image"
    assert result.source_size == 0
    assert result.read_only is True
    assert result.volumes == ()
    assert [warning.code for warning in result.warnings] == ["empty_image"]


def test_missing_source_returns_structured_unavailable_result():
    with _volume_fixture_directory("volume-missing-image") as directory:
        source_path = directory / "missing.raw"

        result = discover_volumes(LocalFileImageStream(source_path))

    assert result.status.code == "image_stream_unavailable"
    assert result.source_size is None
    assert result.read_only is True
    assert result.volumes == ()
    assert [warning.code for warning in result.warnings] == ["missing_path"]


def test_volume_discovery_result_shape_is_json_serializable():
    with _volume_fixture_directory("volume-json-shape") as directory:
        source_path = directory / "tiny.raw"
        _write_bytes(source_path, b"abcdef")

        result_dict = discover_volumes(LocalFileImageStream(source_path)).to_dict()
        parsed = json.loads(json.dumps(result_dict, sort_keys=True))

    assert parsed["schema_version"] == VOLUME_DISCOVERY_SCHEMA_VERSION
    assert parsed["status"]["code"] == "ok"
    assert parsed["source_size"] == 6
    assert parsed["volumes"][0]["volume_id"] == "volume-0"
    assert parsed["volumes"][0]["offset"] == 0
    assert parsed["volumes"][0]["length"] == 6
    assert parsed["volumes"][0]["read_only"] is True


def test_whole_image_volume_preserves_read_only_provenance():
    with _volume_fixture_directory("volume-provenance") as directory:
        source_path = directory / "tiny.raw"
        _write_bytes(source_path, b"provenance")

        result = discover_volumes(LocalFileImageStream(source_path))

    assert result.source_path.endswith("tiny.raw")
    assert result.stream_type == "local-file"
    assert result.read_only is True
    assert result.volumes[0].source_path == result.source_path
    assert result.volumes[0].stream_type == result.stream_type
    assert result.volumes[0].source_size == result.source_size
    assert result.volumes[0].read_only is True


def test_unsupported_partition_strategy_returns_structured_status():
    with _volume_fixture_directory("volume-unsupported-strategy") as directory:
        source_path = directory / "tiny.raw"
        _write_bytes(source_path, b"0123456789")

        result = discover_volumes(
            LocalFileImageStream(source_path),
            strategy="partition_table",
        )

    assert result.status.code == "partition_parsing_unsupported"
    assert result.strategy == "partition_table"
    assert result.source_size == 10
    assert result.read_only is True
    assert result.volumes == ()
    assert [warning.code for warning in result.warnings] == [
        "partition_parsing_deferred"
    ]
