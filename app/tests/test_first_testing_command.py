"""Tests for the Stage 4.5 first-testing command shell."""

from contextlib import contextmanager
import json
from pathlib import Path
import shutil

from app.backend.api import first_testing as first_testing_api
from app.backend.api.first_testing import (
    FIRST_TESTING_RUN_SCHEMA_VERSION,
    main,
    run_first_testing,
)
from app.backend.case_store import connect
from app.backend.forensic_core import PyewfEwfReaderAdapter


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


def test_direct_e01_with_stub_creates_case_artifacts_and_persistence():
    with _dummy_first_testing_directory("direct-stub") as directory:
        evidence_dir = directory / "evidence"
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
        artifact_exists = all(path.exists() for path in _required_artifacts(case_dir, output_dir))
        actions = _audit_actions(case_dir / "case.db")
        audit_actions = {event["action"] for event in audit["events"]}

    assert result["schema_version"] == FIRST_TESTING_RUN_SCHEMA_VERSION
    assert result["status"] == "ok_with_unsupported_sections"
    assert result["evidence"]["segment_count"] == 2
    assert result["adapter"]["name"] == "stub-ewf-reader"
    assert result["source_modified"] is False
    assert result["read_only_asserted"] is True
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
        unsupported = json.loads(
            (case_dir / "outputs" / "unsupported-sections.json").read_text(encoding="utf-8")
        )

    assert result["status"] == "ok_with_unsupported_sections"
    assert intake["status"] == "metadata_unavailable"
    assert intake["adapter"]["name"] == "pyewf-reader"
    assert intake["adapter"]["available"] is False
    assert intake["metadata"] == {}
    assert intake["verification"]["status"] == "not_run"
    assert any(section["section"] == "real_ewf_metadata" for section in unsupported["sections"])
    assert all(section["status"] == "not_implemented" for section in unsupported["sections"])


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


def test_redact_paths_redacts_console_and_summary_but_not_local_json(capsys):
    with _dummy_first_testing_directory("redact-paths") as directory:
        evidence_dir = directory / "evidence"
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
        intake = json.loads((case_dir / "outputs" / "intake.json").read_text(encoding="utf-8"))

    assert exit_code == 0
    assert "<EVIDENCE_ROOT>" in console
    assert "<EVIDENCE_ROOT>" in summary
    assert str(evidence_dir.resolve()) not in console
    assert str(evidence_dir.resolve()) not in summary
    assert intake["source_path"] == str(selected_path.resolve())
    assert intake["selected_path"] == str(selected_path.resolve())


def test_s4_5_imp01_does_not_create_later_slice_artifacts():
    with _dummy_first_testing_directory("no-later-artifacts") as directory:
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
        later_artifacts_exist = [
            (output_dir / "file-list.json").exists(),
            (output_dir / "file-list.csv").exists(),
            (output_dir / "exports").exists(),
            (output_dir / "reports").exists(),
            (case_dir / "reports").exists(),
            any(output_dir.rglob("*.html")),
        ]

    assert later_artifacts_exist == [False, False, False, False, False, False]
