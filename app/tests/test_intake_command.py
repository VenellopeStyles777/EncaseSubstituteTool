"""Tests for the Stage 1 intake command boundary."""

from contextlib import contextmanager
import json
from pathlib import Path
import shutil

from app.backend.api.intake import INTAKE_SCHEMA_VERSION, intake_to_json, main, run_e01_intake
from app.backend.forensic_core import PyewfEwfReaderAdapter, StubEwfReaderAdapter


@contextmanager
def _dummy_intake_directory(name: str):
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


def _touch_files(directory: Path, *filenames: str) -> None:
    for filename in filenames:
        (directory / filename).touch()


def _warning_codes(result: dict[str, object]) -> list[str]:
    return [warning["code"] for warning in result["warnings"]]


def test_stub_backed_intake_output_shape_is_json_serializable():
    with _dummy_intake_directory("intake-success") as directory:
        _touch_files(directory, "sample.E01", "sample.E02")

        result = run_e01_intake(directory / "sample.E01", StubEwfReaderAdapter())
        parsed = json.loads(intake_to_json(directory / "sample.E01", StubEwfReaderAdapter()))

    assert result["schema_version"] == INTAKE_SCHEMA_VERSION
    assert result["status"] == "ok"
    assert result["read_only"] is True
    assert result["segment_count"] == 2
    assert result["segment_discovery"]["is_valid_input"] is True
    assert result["adapter"]["name"] == "stub-ewf-reader"
    assert result["adapter"]["available"] is True
    assert result["metadata"]["reader"] == "stub"
    assert result["metadata"]["segment_count"] == 2
    assert result["verification"]["status"] == "not_supported"
    assert "stub_metadata" in _warning_codes(result)
    assert parsed["schema_version"] == INTAKE_SCHEMA_VERSION


def test_unsupported_input_extension_returns_structured_invalid_output():
    with _dummy_intake_directory("intake-unsupported") as directory:
        _touch_files(directory, "sample.raw")

        result = run_e01_intake(directory / "sample.raw", StubEwfReaderAdapter())

    assert result["status"] == "invalid_input"
    assert result["read_only"] is True
    assert result["metadata"] == {}
    assert result["verification"]["status"] == "not_run"
    assert result["segment_discovery"]["is_valid_input"] is False
    assert "unsupported_input_extension" in _warning_codes(result)
    assert "metadata_skipped" in _warning_codes(result)


def test_missing_selected_e01_path_returns_structured_invalid_output():
    with _dummy_intake_directory("intake-missing-e01") as directory:
        selected_path = directory / "missing.E01"

        result = run_e01_intake(selected_path, StubEwfReaderAdapter())

    assert result["status"] == "invalid_input"
    assert result["metadata"] == {}
    assert result["segment_count"] == 0
    assert result["verification"]["status"] == "not_run"
    assert result["segment_discovery"]["is_valid_input"] is False
    assert "selected_segment_not_found" in _warning_codes(result)


def test_dependency_unavailable_adapter_output_is_structured():
    with _dummy_intake_directory("intake-pyewf-unavailable") as directory:
        _touch_files(directory, "sample.E01")
        adapter = PyewfEwfReaderAdapter(
            pyewf_module=None,
            import_error=ImportError("No module named 'pyewf'"),
        )

        result = run_e01_intake(directory / "sample.E01", adapter)

    assert result["status"] == "metadata_unavailable"
    assert result["read_only"] is True
    assert result["adapter"]["name"] == "pyewf-reader"
    assert result["adapter"]["available"] is False
    assert result["adapter"]["dependency"]["available"] is False
    assert result["metadata"] == {}
    assert result["verification"]["status"] == "not_run"
    assert "dependency_unavailable" in _warning_codes(result)


def test_importable_pyewf_adapter_can_return_best_effort_metadata():
    class FakeHandle:
        def open(self, paths):
            self.paths = list(paths)

        def close(self):
            self.closed = True

        def get_media_size(self):
            return 1024

        def get_bytes_per_sector(self):
            return 512

        def get_header_values(self):
            return {"case_number": "CASE-INTAKE"}

    class FakePyewf:
        __version__ = "test-version"

        def __init__(self):
            self.handle_instance = FakeHandle()

        def handle(self):
            return self.handle_instance

    fake_pyewf = FakePyewf()
    with _dummy_intake_directory("intake-pyewf-not-implemented") as directory:
        _touch_files(directory, "sample.E01")
        adapter = PyewfEwfReaderAdapter(pyewf_module=fake_pyewf)

        result = run_e01_intake(directory / "sample.E01", adapter)

    assert result["status"] == "ok"
    assert result["adapter"]["available"] is True
    assert result["metadata"]["media_size"] == 1024
    assert result["metadata"]["bytes_per_sector"] == 512
    assert result["metadata"]["case_number"] == "CASE-INTAKE"
    assert result["verification"]["status"] == "not_supported"
    assert "verification_not_supported" in _warning_codes(result)
    assert fake_pyewf.handle_instance.closed is True


def test_cli_invalid_input_returns_nonzero_and_prints_json(capsys):
    with _dummy_intake_directory("intake-cli-invalid") as directory:
        _touch_files(directory, "sample.raw")

        exit_code = main([str(directory / "sample.raw"), "--adapter", "stub"])

    output = json.loads(capsys.readouterr().out)

    assert exit_code == 2
    assert output["status"] == "invalid_input"
    assert "unsupported_input_extension" in _warning_codes(output)
