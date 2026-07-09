"""Tests for E01 segment discovery."""

from contextlib import contextmanager
from pathlib import Path
import shutil

from app.backend.forensic_core import discover_e01_segments


@contextmanager
def _dummy_segment_directory(name: str):
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


def _touch_segments(directory: Path, *filenames: str) -> None:
    for filename in filenames:
        (directory / filename).touch()


def _warning_codes(result) -> list[str]:
    return [warning.code for warning in result.warnings]


def test_discovers_single_e01_segment():
    with _dummy_segment_directory("single-e01") as directory:
        _touch_segments(directory, "sample.E01")

        result = discover_e01_segments(directory / "sample.E01")

    assert result.is_valid_input is True
    assert result.is_complete is True
    assert result.read_only is True
    assert [segment.filename for segment in result.segments] == ["sample.E01"]
    assert [segment.segment_number for segment in result.segments] == [1]
    assert result.warnings == ()


def test_discovers_ordered_e01_e02_e03_chain():
    with _dummy_segment_directory("ordered-chain") as directory:
        _touch_segments(directory, "sample.E03", "sample.E01", "sample.E02")

        result = discover_e01_segments(directory / "sample.E01")

    assert result.is_valid_input is True
    assert result.is_complete is True
    assert [segment.filename for segment in result.segments] == [
        "sample.E01",
        "sample.E02",
        "sample.E03",
    ]
    assert [segment.segment_number for segment in result.segments] == [1, 2, 3]
    assert result.warnings == ()


def test_warns_for_missing_middle_segment():
    with _dummy_segment_directory("missing-middle") as directory:
        _touch_segments(directory, "sample.E01", "sample.E03")

        result = discover_e01_segments(directory / "sample.E01")

    assert result.is_valid_input is True
    assert result.is_complete is False
    assert [segment.segment_number for segment in result.segments] == [1, 3]
    assert _warning_codes(result) == ["missing_segment"]
    assert result.warnings[0].segment_number == 2
    assert result.warnings[0].path.endswith("sample.E02")


def test_returns_invalid_result_for_unsupported_extension():
    with _dummy_segment_directory("unsupported-extension") as directory:
        _touch_segments(directory, "sample.raw")

        result = discover_e01_segments(directory / "sample.raw")

    assert result.is_valid_input is False
    assert result.is_complete is False
    assert result.segments == ()
    assert _warning_codes(result) == ["unsupported_input_extension"]


def test_handles_segment_extensions_case_insensitively():
    with _dummy_segment_directory("case-insensitive") as directory:
        _touch_segments(directory, "sample.e01", "sample.E02", "sample.e03")

        result = discover_e01_segments(directory / "sample.e01")

    assert result.is_valid_input is True
    assert result.is_complete is True
    assert [segment.filename for segment in result.segments] == [
        "sample.e01",
        "sample.E02",
        "sample.e03",
    ]
    assert [segment.segment_number for segment in result.segments] == [1, 2, 3]
    assert result.warnings == ()


def test_rejects_e00_as_unsupported_sibling_segment():
    with _dummy_segment_directory("reject-e00") as directory:
        _touch_segments(directory, "sample.E00", "sample.E01")

        result = discover_e01_segments(directory / "sample.E01")

    assert result.is_valid_input is True
    assert [segment.filename for segment in result.segments] == ["sample.E01"]
    assert [segment.segment_number for segment in result.segments] == [1]
    assert _warning_codes(result) == ["unsupported_segment_extension"]
    assert result.warnings[0].path.endswith("sample.E00")
