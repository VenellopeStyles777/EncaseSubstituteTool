"""Stage 4.5 first-testing command shell and case workspace orchestration."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from typing import Any, Mapping, Sequence
from uuid import uuid4

from app.backend.api.intake import INTAKE_SCHEMA_VERSION, run_e01_intake
from app.backend.case_store import (
    SCHEMA_VERSION as CASE_STORE_SCHEMA_VERSION,
    connect,
    initialize_schema,
    insert_audit_event,
    insert_case,
    insert_evidence_source,
    list_audit_events,
)
from app.backend.forensic_core import (
    EwfReaderAdapter,
    PyewfEwfReaderAdapter,
    StubEwfReaderAdapter,
)


FIRST_TESTING_RUN_SCHEMA_VERSION = "stage4_5.first_testing_run.v1"
UNSUPPORTED_SECTIONS_SCHEMA_VERSION = "stage4_5.unsupported_sections.v1"

_SEGMENT_SUFFIX_RE = re.compile(r"^\.E(?P<number>\d+)$", re.IGNORECASE)


def run_first_testing(
    evidence_path: str | Path | None = None,
    *,
    evidence_dir: str | Path | None = None,
    first_segment: str | Path | None = None,
    case_path: str | Path | None = None,
    output_path: str | Path | None = None,
    case_name: str | None = None,
    case_description: str | None = None,
    actor: str | None = None,
    adapter_name: str = "pyewf",
    redact_paths: bool = False,
    adapter: EwfReaderAdapter | None = None,
) -> dict[str, object]:
    """Create the first Stage 4.5 case workspace and artifact bundle.

    This function intentionally orchestrates only the command shell, case store,
    existing Stage 1 intake, and unsupported-section output. It does not add real
    EWF metadata, verification, filesystem parsing, file content, file-list,
    report, search, or timeline behavior.
    """

    validation = _validate_request(
        evidence_path=evidence_path,
        evidence_dir=evidence_dir,
        first_segment=first_segment,
        case_path=case_path,
        output_path=output_path,
    )
    if validation["status"] != "ok":
        return _failure_result(
            status=str(validation["status"]),
            code=str(validation["code"]),
            message=str(validation["message"]),
            details=_as_mapping(validation.get("details")),
        )

    selected_path = validation["selected_path"]
    evidence_root = validation["evidence_root"]
    case_dir = validation["case_dir"]
    output_dir = validation["output_dir"]
    input_form = validation["input_form"]

    adapter_instance = adapter or _build_adapter(adapter_name)
    run_id = f"first_testing_{uuid4().hex}"
    started_at = _utc_now()

    case_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    case_db_path = case_dir / "case.db"
    artifact_paths = _artifact_paths(case_dir, output_dir)

    connection = connect(case_db_path)
    try:
        initialize_schema(connection)
        resolved_case_name = case_name or case_dir.name or "First Testing Case"
        case_id = insert_case(
            connection,
            name=resolved_case_name,
            description=case_description,
        )
        insert_audit_event(
            connection,
            case_id=case_id,
            action="first_testing.case_created",
            actor=actor,
            details={
                "run_id": run_id,
                "case_workspace": str(case_dir),
                "case_database": str(case_db_path),
            },
        )

        intake_result = run_e01_intake(selected_path, adapter_instance)
        evidence_id = insert_evidence_source(
            connection,
            case_id=case_id,
            intake_result=intake_result,
        )
        insert_audit_event(
            connection,
            case_id=case_id,
            evidence_id=evidence_id,
            action="first_testing.evidence_intake_completed",
            actor=actor,
            details={
                "run_id": run_id,
                "intake_status": intake_result.get("status"),
                "segment_count": intake_result.get("segment_count"),
                "adapter_name": _as_mapping(intake_result.get("adapter")).get("name"),
            },
        )

        unsupported_sections = _unsupported_sections()
        overall_status = _overall_status(intake_result)
        completed_at = _utc_now()

        case_artifact = _case_artifact(
            case_id=case_id,
            case_name=resolved_case_name,
            case_description=case_description,
            case_dir=case_dir,
            case_db_path=case_db_path,
            evidence_id=evidence_id,
            intake_result=intake_result,
            selected_path=selected_path,
            evidence_root=evidence_root,
            actor=actor,
        )
        metadata_artifact = _metadata_artifact(
            evidence_id=evidence_id,
            intake_result=intake_result,
        )
        verification_artifact = _verification_artifact(
            evidence_id=evidence_id,
            intake_result=intake_result,
        )
        segment_discovery_artifact = _segment_discovery_artifact(
            evidence_id=evidence_id,
            intake_result=intake_result,
        )

        _write_json(artifact_paths["intake"], intake_result)
        _write_json(artifact_paths["case"], case_artifact)
        _write_json(artifact_paths["metadata"], metadata_artifact)
        _write_json(artifact_paths["verification"], verification_artifact)
        _write_json(artifact_paths["segment_discovery"], segment_discovery_artifact)
        _write_json(artifact_paths["unsupported_sections"], unsupported_sections)

        insert_audit_event(
            connection,
            case_id=case_id,
            evidence_id=evidence_id,
            action="first_testing.artifacts_written",
            actor=actor,
            details={
                "run_id": run_id,
                "artifact_paths": {key: str(value) for key, value in artifact_paths.items()},
                "unsupported_section_count": len(unsupported_sections["sections"]),
            },
        )
        insert_audit_event(
            connection,
            case_id=case_id,
            evidence_id=evidence_id,
            action="first_testing.run_completed",
            actor=actor,
            details={
                "run_id": run_id,
                "status": overall_status,
                "source_modified": False,
                "read_only_asserted": True,
            },
        )

        audit_artifact = _audit_artifact(
            list_audit_events(connection, case_id=case_id)
        )
        _write_json(artifact_paths["audit"], audit_artifact)

        manifest = _run_manifest(
            run_id=run_id,
            status=overall_status,
            started_at=started_at,
            completed_at=completed_at,
            input_form=input_form,
            selected_path=selected_path,
            evidence_root=evidence_root,
            case_dir=case_dir,
            output_dir=output_dir,
            case_db_path=case_db_path,
            case_id=case_id,
            case_name=resolved_case_name,
            case_description=case_description,
            evidence_id=evidence_id,
            intake_result=intake_result,
            unsupported_sections=unsupported_sections,
            metadata_artifact=metadata_artifact,
            audit_artifact=audit_artifact,
            artifact_paths=artifact_paths,
            adapter_name=adapter_name,
            actor=actor,
            redact_paths=redact_paths,
        )
        _write_json(artifact_paths["run_manifest"], manifest)

        summary = format_first_testing_summary(manifest, redact_paths=redact_paths)
        artifact_paths["command_summary"].write_text(summary + "\n", encoding="utf-8")
    finally:
        connection.close()

    return manifest


def first_testing_to_json(
    evidence_path: str | Path | None = None,
    *,
    evidence_dir: str | Path | None = None,
    first_segment: str | Path | None = None,
    case_path: str | Path | None = None,
    output_path: str | Path | None = None,
    case_name: str | None = None,
    case_description: str | None = None,
    actor: str | None = None,
    adapter_name: str = "pyewf",
    redact_paths: bool = False,
    adapter: EwfReaderAdapter | None = None,
    indent: int | None = 2,
) -> str:
    """Run the first-testing command shell and serialize the manifest."""

    result = run_first_testing(
        evidence_path,
        evidence_dir=evidence_dir,
        first_segment=first_segment,
        case_path=case_path,
        output_path=output_path,
        case_name=case_name,
        case_description=case_description,
        actor=actor,
        adapter_name=adapter_name,
        redact_paths=redact_paths,
        adapter=adapter,
    )
    return json.dumps(result, indent=indent, sort_keys=True)


def format_first_testing_summary(
    result: Mapping[str, object],
    *,
    redact_paths: bool = False,
) -> str:
    """Return a concise human-readable command summary."""

    status = result.get("status", "unknown")
    if status in {"invalid_input", "unsafe_output_path"}:
        lines = [
            "Stage 4.5 first-testing command",
            f"Status: {status}",
            f"Message: {result.get('message', '')}",
        ]
        warnings = result.get("warnings", [])
        for warning in warnings if isinstance(warnings, list) else []:
            if isinstance(warning, Mapping):
                lines.append(f"Warning: {warning.get('code')} - {warning.get('message')}")
        return "\n".join(lines)

    command = _as_mapping(result.get("command"))
    case = _as_mapping(result.get("case"))
    evidence = _as_mapping(result.get("evidence"))
    adapter = _as_mapping(result.get("adapter"))
    dependency = _as_mapping(adapter.get("dependency"))
    artifacts = _as_mapping(result.get("artifact_paths"))
    unsupported = result.get("unsupported_sections", [])
    warning_count = len(result.get("warnings", [])) if isinstance(result.get("warnings"), list) else 0

    lines = [
        "Stage 4.5 first-testing command",
        f"Status: {status}",
        f"Case workspace: {case.get('workspace')}",
        f"Case database: {case.get('database_path')}",
        f"Output directory: {command.get('output_path')}",
        f"Evidence path: {evidence.get('selected_path')}",
        f"Input form: {command.get('input_form')}",
        f"Intake status: {evidence.get('intake_status')}",
        f"Segment count: {evidence.get('segment_count')}",
        f"Adapter: {adapter.get('name')} (available={adapter.get('available')})",
        f"Dependency: {dependency.get('name')} (available={dependency.get('available')})",
        f"Metadata status: {_as_mapping(result.get('metadata')).get('status')}",
        f"Verification status: {_as_mapping(result.get('verification')).get('status')}",
        f"Warnings: {warning_count}",
        f"Unsupported sections: {len(unsupported) if isinstance(unsupported, list) else 0}",
        "Artifacts:",
    ]
    for name in sorted(artifacts):
        lines.append(f"- {name}: {artifacts[name]}")
    lines.extend(
        [
            "Source modified: false",
            "Read-only asserted: true",
            "Deferred: EWF stream, partition/filesystem parsing, E01-backed file content, file-list output, static HTML, search, and timeline.",
        ]
    )

    text = "\n".join(lines)
    if redact_paths:
        evidence_root = str(command.get("evidence_root") or "")
        text = _redact_evidence_root(text, evidence_root)
    return text


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point for `python -m app.backend.api.first_testing`."""

    parser = argparse.ArgumentParser(
        description="Run the Stage 4.5 first-testing command shell.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        help="Path to the selected .E01 first segment.",
    )
    parser.add_argument("--evidence-dir", help="Evidence directory containing the first segment.")
    parser.add_argument("--first-segment", help="First segment filename when --evidence-dir is used.")
    parser.add_argument("--case", required=True, dest="case_path", help="Case workspace directory.")
    parser.add_argument("--output", dest="output_path", help="Artifact output directory. Defaults to <case>/outputs.")
    parser.add_argument("--case-name", help="Case display name. Defaults to the case folder name.")
    parser.add_argument("--case-description", help="Optional case description.")
    parser.add_argument("--actor", help="Optional audit actor.")
    parser.add_argument(
        "--adapter",
        choices=("pyewf", "stub"),
        default="pyewf",
        help="Reader adapter. Defaults to pyewf with dependency-safe unavailable output.",
    )
    parser.add_argument(
        "--json-only",
        action="store_true",
        help="Print the JSON manifest/result instead of a text summary.",
    )
    parser.add_argument(
        "--redact-paths",
        action="store_true",
        help="Redact the evidence root in console and command-summary text.",
    )
    args = parser.parse_args(argv)

    result = run_first_testing(
        args.path,
        evidence_dir=args.evidence_dir,
        first_segment=args.first_segment,
        case_path=args.case_path,
        output_path=args.output_path,
        case_name=args.case_name,
        case_description=args.case_description,
        actor=args.actor,
        adapter_name=args.adapter,
        redact_paths=args.redact_paths,
    )

    if args.json_only:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(format_first_testing_summary(result, redact_paths=args.redact_paths))

    return 0 if result.get("status") == "ok_with_unsupported_sections" else 2


def _validate_request(
    *,
    evidence_path: str | Path | None,
    evidence_dir: str | Path | None,
    first_segment: str | Path | None,
    case_path: str | Path | None,
    output_path: str | Path | None,
) -> dict[str, object]:
    if case_path is None:
        return _validation_error("invalid_input", "missing_case", "--case is required.")

    has_direct_path = evidence_path is not None
    has_evidence_dir = evidence_dir is not None
    has_first_segment = first_segment is not None

    if has_direct_path and (has_evidence_dir or has_first_segment):
        return _validation_error(
            "invalid_input",
            "conflicting_input_forms",
            "Use either a direct .E01 path or --evidence-dir with --first-segment, not both.",
        )
    if not has_direct_path and not has_evidence_dir:
        return _validation_error(
            "invalid_input",
            "missing_input",
            "Provide a direct .E01 path or --evidence-dir with --first-segment.",
        )
    if has_evidence_dir and not has_first_segment:
        return _validation_error(
            "invalid_input",
            "missing_first_segment",
            "--first-segment is required when --evidence-dir is used.",
        )
    if has_first_segment and not has_evidence_dir:
        return _validation_error(
            "invalid_input",
            "first_segment_without_evidence_dir",
            "--first-segment can only be used with --evidence-dir.",
        )

    if has_evidence_dir:
        evidence_root = _resolve(evidence_dir)
        if not evidence_root.exists():
            return _validation_error(
                "invalid_input",
                "evidence_dir_not_found",
                "The evidence directory does not exist.",
                {"evidence_dir": str(evidence_root)},
            )
        if not evidence_root.is_dir():
            return _validation_error(
                "invalid_input",
                "evidence_dir_not_directory",
                "The evidence directory path is not a directory.",
                {"evidence_dir": str(evidence_root)},
            )
        first_segment_path = Path(str(first_segment))
        if first_segment_path.is_absolute() or len(first_segment_path.parts) != 1:
            return _validation_error(
                "invalid_input",
                "first_segment_must_be_filename",
                "--first-segment must be a filename inside --evidence-dir.",
            )
        selected_path = evidence_root / first_segment_path
        input_form = "evidence_dir_first_segment"
    else:
        selected_path = _resolve(evidence_path)
        evidence_root = selected_path.parent
        input_form = "direct_e01"

    extension_status = _validate_primary_extension(selected_path)
    if extension_status is not None:
        return extension_status

    if not selected_path.exists():
        return _validation_error(
            "invalid_input",
            "input_not_found",
            "The selected .E01 path does not exist.",
            {"selected_path": str(selected_path)},
        )
    if selected_path.is_dir():
        return _validation_error(
            "invalid_input",
            "input_is_directory",
            "The selected evidence path is a directory; select the .E01 file.",
            {"selected_path": str(selected_path)},
        )

    selected_path = _resolve(selected_path)
    evidence_root = _resolve(evidence_root)
    case_dir = _resolve(case_path)
    output_dir = _resolve(output_path) if output_path is not None else case_dir / "outputs"
    output_dir = _resolve(output_dir)

    overlap = _validate_evidence_output_overlap(
        evidence_root=evidence_root,
        case_dir=case_dir,
        output_dir=output_dir,
    )
    if overlap is not None:
        return overlap

    return {
        "status": "ok",
        "selected_path": selected_path,
        "evidence_root": evidence_root,
        "case_dir": case_dir,
        "output_dir": output_dir,
        "input_form": input_form,
    }


def _validate_primary_extension(path: Path) -> dict[str, object] | None:
    match = _SEGMENT_SUFFIX_RE.match(path.suffix)
    if match is not None and int(match.group("number")) > 1:
        return _validation_error(
            "invalid_input",
            "select_first_e01_segment",
            "Select the .E01 first segment as the primary input; .E02 or later cannot start the run.",
            {"selected_path": str(path)},
        )
    if path.suffix.lower() != ".e01":
        return _validation_error(
            "invalid_input",
            "unsupported_input_extension",
            "S4.5-IMP01 accepts only a selected .E01 first segment.",
            {"selected_path": str(path)},
        )
    return None


def _validate_evidence_output_overlap(
    *,
    evidence_root: Path,
    case_dir: Path,
    output_dir: Path,
) -> dict[str, object] | None:
    if _path_contains(evidence_root, case_dir):
        return _validation_error(
            "unsafe_output_path",
            "case_inside_evidence_dir",
            "The case workspace must not be inside the evidence directory.",
            {"evidence_root": str(evidence_root), "case_dir": str(case_dir)},
        )
    if _path_contains(case_dir, evidence_root):
        return _validation_error(
            "unsafe_output_path",
            "evidence_inside_case_dir",
            "The evidence directory must not be inside the case workspace.",
            {"evidence_root": str(evidence_root), "case_dir": str(case_dir)},
        )
    if _path_contains(evidence_root, output_dir):
        return _validation_error(
            "unsafe_output_path",
            "output_inside_evidence_dir",
            "The output directory must not be inside the evidence directory.",
            {"evidence_root": str(evidence_root), "output_dir": str(output_dir)},
        )
    if _path_contains(output_dir, evidence_root):
        return _validation_error(
            "unsafe_output_path",
            "evidence_inside_output_dir",
            "The evidence directory must not be inside the output directory.",
            {"evidence_root": str(evidence_root), "output_dir": str(output_dir)},
        )
    return None


def _failure_result(
    *,
    status: str,
    code: str,
    message: str,
    details: Mapping[str, object] | None = None,
) -> dict[str, object]:
    return {
        "schema_version": FIRST_TESTING_RUN_SCHEMA_VERSION,
        "status": status,
        "message": message,
        "warnings": [
            {
                "source": "first_testing",
                "code": code,
                "message": message,
                "details": dict(details or {}),
            }
        ],
        "artifact_paths": {},
        "read_only_asserted": True,
        "source_modified": False,
    }


def _validation_error(
    status: str,
    code: str,
    message: str,
    details: Mapping[str, object] | None = None,
) -> dict[str, object]:
    return {
        "status": status,
        "code": code,
        "message": message,
        "details": dict(details or {}),
    }


def _build_adapter(adapter_name: str) -> EwfReaderAdapter:
    if adapter_name == "stub":
        return StubEwfReaderAdapter()
    if adapter_name == "pyewf":
        return PyewfEwfReaderAdapter()
    raise ValueError(f"Unsupported adapter: {adapter_name}")


def _artifact_paths(case_dir: Path, output_dir: Path) -> dict[str, Path]:
    return {
        "run_manifest": case_dir / "run-manifest.json",
        "command_summary": case_dir / "command-summary.txt",
        "intake": output_dir / "intake.json",
        "case": output_dir / "case.json",
        "metadata": output_dir / "metadata.json",
        "verification": output_dir / "verification.json",
        "segment_discovery": output_dir / "segment-discovery.json",
        "audit": output_dir / "audit.json",
        "unsupported_sections": output_dir / "unsupported-sections.json",
    }


def _unsupported_sections() -> dict[str, object]:
    rows = [
        (
            "ewf_backed_byte_stream",
            "S4.5-IMP03",
            "EWF-backed byte streaming is not implemented in S4.5-IMP02.",
        ),
        (
            "partition_filesystem_parsing",
            "S4.5-IMP03",
            "Partition and filesystem parsing from E01 evidence is not implemented in S4.5-IMP02.",
        ),
        (
            "e01_backed_preview_export_hash_signature",
            "S4.5-IMP04",
            "E01-backed preview, export, hashing, and signature providers are not implemented in S4.5-IMP02.",
        ),
        (
            "file_list_json_csv_output",
            "S4.5-IMP05",
            "File-list JSON/CSV output is not implemented in S4.5-IMP02.",
        ),
        (
            "static_html_summary",
            "S4.5-IMP05",
            "Static HTML summary output is not implemented in S4.5-IMP02.",
        ),
        (
            "implementation_handoff_manual_test_reconciliation",
            "S4.5-IMP07",
            "Final manual-test guardrail reconciliation is not complete until the later handoff slice.",
        ),
    ]
    return {
        "schema_version": UNSUPPORTED_SECTIONS_SCHEMA_VERSION,
        "status": "unsupported_sections_present",
        "sections": [
            {
                "section": section,
                "status": "not_implemented",
                "owner": owner,
                "message": message,
            }
            for section, owner, message in rows
        ],
    }


def _case_artifact(
    *,
    case_id: str,
    case_name: str,
    case_description: str | None,
    case_dir: Path,
    case_db_path: Path,
    evidence_id: str,
    intake_result: Mapping[str, object],
    selected_path: Path,
    evidence_root: Path,
    actor: str | None,
) -> dict[str, object]:
    return {
        "schema_version": FIRST_TESTING_RUN_SCHEMA_VERSION,
        "case_store_schema_version": CASE_STORE_SCHEMA_VERSION,
        "case": {
            "case_id": case_id,
            "name": case_name,
            "description": case_description,
            "workspace": str(case_dir),
            "database_path": str(case_db_path),
        },
        "evidence": {
            "evidence_id": evidence_id,
            "source_path": str(intake_result.get("source_path") or selected_path),
            "selected_path": str(intake_result.get("selected_path") or selected_path),
            "evidence_root": str(evidence_root),
            "intake_status": intake_result.get("status"),
            "segment_count": intake_result.get("segment_count"),
            "read_only_asserted": bool(intake_result.get("read_only", True)),
            "source_modified": False,
        },
        "actor": actor,
    }


def _audit_artifact(rows: Sequence[Any]) -> dict[str, object]:
    events = []
    for row in rows:
        details_json = row["details_json"]
        try:
            details = json.loads(details_json)
        except json.JSONDecodeError:
            details = {"unparsed_details_json": details_json}
        events.append(
            {
                "audit_event_id": row["audit_event_id"],
                "case_id": row["case_id"],
                "evidence_id": row["evidence_id"],
                "action": row["action"],
                "actor": row["actor"],
                "details": details,
                "created_at": row["created_at"],
            }
        )

    return {
        "schema_version": "stage4_5.first_testing_audit.v1",
        "events": events,
    }


def _metadata_artifact(
    *,
    evidence_id: str,
    intake_result: Mapping[str, object],
) -> dict[str, object]:
    metadata = _as_mapping(intake_result.get("metadata"))
    warnings = intake_result.get("warnings", [])
    reader_warnings = [
        warning
        for warning in warnings
        if isinstance(warning, Mapping) and warning.get("source") == "reader"
    ] if isinstance(warnings, list) else []
    return {
        "schema_version": "stage4_5.first_testing_metadata.v1",
        "status": _metadata_status(intake_result),
        "evidence_id": evidence_id,
        "source_path": intake_result.get("source_path"),
        "selected_path": intake_result.get("selected_path"),
        "segment_count": intake_result.get("segment_count"),
        "adapter": _as_mapping(intake_result.get("adapter")),
        "metadata": dict(metadata),
        "warnings": reader_warnings,
    }


def _verification_artifact(
    *,
    evidence_id: str,
    intake_result: Mapping[str, object],
) -> dict[str, object]:
    warnings = intake_result.get("warnings", [])
    verification_warnings = [
        warning
        for warning in warnings
        if isinstance(warning, Mapping)
        and str(warning.get("code", "")).startswith("verification")
    ] if isinstance(warnings, list) else []
    verification = _as_mapping(intake_result.get("verification"))
    return {
        "schema_version": "stage4_5.first_testing_verification.v1",
        "status": verification.get("status") or "unknown",
        "evidence_id": evidence_id,
        "source_path": intake_result.get("source_path"),
        "selected_path": intake_result.get("selected_path"),
        "segment_count": intake_result.get("segment_count"),
        "adapter": _as_mapping(intake_result.get("adapter")),
        "verification": dict(verification),
        "stored_hashes_are_verification": False,
        "warnings": verification_warnings,
    }


def _segment_discovery_artifact(
    *,
    evidence_id: str,
    intake_result: Mapping[str, object],
) -> dict[str, object]:
    return {
        "schema_version": "stage4_5.first_testing_segment_discovery.v1",
        "status": "ok" if intake_result.get("segment_count") else "not_available",
        "evidence_id": evidence_id,
        "source_path": intake_result.get("source_path"),
        "selected_path": intake_result.get("selected_path"),
        "segment_count": intake_result.get("segment_count"),
        "segment_discovery": _as_mapping(intake_result.get("segment_discovery")),
    }


def _run_manifest(
    *,
    run_id: str,
    status: str,
    started_at: str,
    completed_at: str,
    input_form: str,
    selected_path: Path,
    evidence_root: Path,
    case_dir: Path,
    output_dir: Path,
    case_db_path: Path,
    case_id: str,
    case_name: str,
    case_description: str | None,
    evidence_id: str,
    intake_result: Mapping[str, object],
    unsupported_sections: Mapping[str, object],
    metadata_artifact: Mapping[str, object],
    audit_artifact: Mapping[str, object],
    artifact_paths: Mapping[str, Path],
    adapter_name: str,
    actor: str | None,
    redact_paths: bool,
) -> dict[str, object]:
    adapter = _as_mapping(intake_result.get("adapter"))
    verification = _as_mapping(intake_result.get("verification"))
    sections = unsupported_sections.get("sections", [])
    warnings = intake_result.get("warnings", [])

    return {
        "schema_version": FIRST_TESTING_RUN_SCHEMA_VERSION,
        "run_id": run_id,
        "status": status,
        "started_at": started_at,
        "completed_at": completed_at,
        "command": {
            "input_form": input_form,
            "selected_path": str(selected_path),
            "evidence_root": str(evidence_root),
            "case_path": str(case_dir),
            "output_path": str(output_dir),
            "case_name": case_name,
            "case_description": case_description,
            "actor": actor,
            "requested_adapter": adapter_name,
            "redact_paths": redact_paths,
        },
        "tool_versions": {
            "run_schema_version": FIRST_TESTING_RUN_SCHEMA_VERSION,
            "intake_schema_version": INTAKE_SCHEMA_VERSION,
            "case_store_schema_version": CASE_STORE_SCHEMA_VERSION,
        },
        "case": {
            "case_id": case_id,
            "name": case_name,
            "description": case_description,
            "workspace": str(case_dir),
            "database_path": str(case_db_path),
        },
        "evidence": {
            "evidence_id": evidence_id,
            "source_path": str(intake_result.get("source_path") or selected_path),
            "selected_path": str(intake_result.get("selected_path") or selected_path),
            "evidence_root": str(evidence_root),
            "intake_status": intake_result.get("status"),
            "segment_count": intake_result.get("segment_count"),
            "read_only_asserted": bool(intake_result.get("read_only", True)),
            "source_modified": False,
        },
        "adapter": adapter,
        "metadata": {
            "status": metadata_artifact.get("status"),
            "field_count": len(_as_mapping(metadata_artifact.get("metadata"))),
            "artifact_path": str(artifact_paths["metadata"]),
        },
        "verification": verification,
        "warnings": warnings if isinstance(warnings, list) else [],
        "unsupported_sections": sections if isinstance(sections, list) else [],
        "artifact_paths": {key: str(value) for key, value in artifact_paths.items()},
        "audit_event_count": len(audit_artifact.get("events", [])) if isinstance(audit_artifact.get("events"), list) else 0,
        "read_only_asserted": True,
        "source_modified": False,
    }


def _overall_status(intake_result: Mapping[str, object]) -> str:
    if intake_result.get("status") in {"ok", "metadata_unavailable", "reader_not_implemented"}:
        return "ok_with_unsupported_sections"
    return "intake_failed"


def _metadata_status(intake_result: Mapping[str, object]) -> str:
    if _as_mapping(intake_result.get("metadata")):
        return "metadata_available"
    status = intake_result.get("status")
    if status == "metadata_unavailable":
        return "metadata_unavailable"
    if status in {"reader_error", "reader_not_implemented"}:
        return "metadata_error"
    return "metadata_empty"


def _write_json(path: Path, data: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _path_contains(parent: Path, child: Path) -> bool:
    try:
        child.relative_to(parent)
    except ValueError:
        return False
    return True


def _resolve(path: str | Path | None) -> Path:
    if path is None:
        raise ValueError("Path cannot be None")
    return Path(path).expanduser().resolve(strict=False)


def _as_mapping(value: object) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _redact_evidence_root(text: str, evidence_root: str) -> str:
    if not evidence_root:
        return text
    redacted = text.replace(evidence_root, "<EVIDENCE_ROOT>")
    return redacted.replace(evidence_root.replace("/", "\\"), "<EVIDENCE_ROOT>")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
