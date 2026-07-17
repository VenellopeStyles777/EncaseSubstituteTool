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
from app.backend.api.directory_listing import list_directory
from app.backend.api.file_export import export_file
from app.backend.api.file_preview import DEFAULT_PREVIEW_MAX_LENGTH, preview_file
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
    DEFAULT_SELECTED_FILE_IN_MEMORY_LIMIT,
    DEFAULT_SIGNATURE_MAX_BYTES,
    E01AnalysisContentProvider,
    E01ExportContentProvider,
    E01PreviewContentProvider,
    E01SelectedFileContentReader,
    EwfReaderAdapter,
    EwfImageByteStream,
    PyewfEwfReaderAdapter,
    Pytsk3FilesystemAdapter,
    StubEwfReaderAdapter,
    VolumeDiscoveryStatus,
    VolumeInfo,
    detect_file_signature,
    discover_volumes,
    evaluate_extension_mismatch,
    hash_file_content,
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
    selected_file_id: str | None = None,
    selected_file_path: str | None = None,
    selected_file_export_dir: str | Path | None = None,
    selected_file_export_name: str | None = None,
    selected_file_preview_mode: str = "hex",
    selected_file_max_bytes: int = DEFAULT_SELECTED_FILE_IN_MEMORY_LIMIT,
) -> dict[str, object]:
    """Create the first Stage 4.5 case workspace and artifact bundle.

    This function orchestrates the command shell, case store, existing intake,
    metadata/verification artifacts, and the S4.5 real-E01 filesystem demo.
    Selected-file content is run only when a file is explicitly requested. This
    function does not add file-list, report, search, or timeline behavior.
    """

    validation = _validate_request(
        evidence_path=evidence_path,
        evidence_dir=evidence_dir,
        first_segment=first_segment,
        case_path=case_path,
        output_path=output_path,
        selected_file_id=selected_file_id,
        selected_file_path=selected_file_path,
        selected_file_max_bytes=selected_file_max_bytes,
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
    selection = _selection_request(
        selected_file_id=selected_file_id,
        selected_file_path=selected_file_path,
        export_dir=selected_file_export_dir,
        export_name=selected_file_export_name,
        preview_mode=selected_file_preview_mode,
        max_bytes=selected_file_max_bytes,
    )

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
        demo_artifacts = _filesystem_demo_artifacts(
            selected_path=selected_path,
            intake_result=intake_result,
            adapter_name=adapter_name,
        )
        selected_file_artifacts = _selected_file_artifacts(
            selected_path=selected_path,
            intake_result=intake_result,
            adapter_name=adapter_name,
            demo_artifacts=demo_artifacts,
            selection=selection,
            case_id=case_id,
            evidence_id=evidence_id,
        )

        _write_json(artifact_paths["intake"], intake_result)
        _write_json(artifact_paths["case"], case_artifact)
        _write_json(artifact_paths["metadata"], metadata_artifact)
        _write_json(artifact_paths["verification"], verification_artifact)
        _write_json(artifact_paths["segment_discovery"], segment_discovery_artifact)
        _write_json(artifact_paths["ewf_stream"], demo_artifacts["ewf_stream"])
        _write_json(artifact_paths["volumes"], demo_artifacts["volumes"])
        _write_json(artifact_paths["filesystems"], demo_artifacts["filesystems"])
        _write_json(artifact_paths["root_listing"], demo_artifacts["root_listing"])
        _write_json(artifact_paths["demo_readiness"], demo_artifacts["demo_readiness"])
        _write_json(artifact_paths["selected_file_readiness"], selected_file_artifacts["readiness"])
        _write_json(artifact_paths["selected_file_preview"], selected_file_artifacts["preview"])
        _write_json(artifact_paths["selected_file_analysis"], selected_file_artifacts["analysis"])
        _write_json(artifact_paths["selected_file_export"], selected_file_artifacts["export"])
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
            demo_artifacts=demo_artifacts,
            selected_file_artifacts=selected_file_artifacts,
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
    selected_file_id: str | None = None,
    selected_file_path: str | None = None,
    selected_file_export_dir: str | Path | None = None,
    selected_file_export_name: str | None = None,
    selected_file_preview_mode: str = "hex",
    selected_file_max_bytes: int = DEFAULT_SELECTED_FILE_IN_MEMORY_LIMIT,
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
        selected_file_id=selected_file_id,
        selected_file_path=selected_file_path,
        selected_file_export_dir=selected_file_export_dir,
        selected_file_export_name=selected_file_export_name,
        selected_file_preview_mode=selected_file_preview_mode,
        selected_file_max_bytes=selected_file_max_bytes,
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
    ewf_stream = _as_mapping(result.get("ewf_stream"))
    volumes = _as_mapping(result.get("volumes"))
    filesystem = _as_mapping(result.get("filesystem"))
    root_listing = _as_mapping(result.get("root_listing"))
    selected_file = _as_mapping(result.get("selected_file"))
    selected_preview = _as_mapping(selected_file.get("preview"))
    selected_analysis = _as_mapping(selected_file.get("analysis"))
    selected_export = _as_mapping(selected_file.get("export"))
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
        f"EWF stream status: {ewf_stream.get('status')}",
        f"Logical media size: {ewf_stream.get('logical_media_size')}",
        f"Volume strategy/status/count: {volumes.get('strategy')} / {volumes.get('status')} / {volumes.get('volume_count')}",
        f"Filesystem status: {filesystem.get('status')}",
        f"Root listing: {root_listing.get('parser_backing')} entries={root_listing.get('entry_count')}",
        f"Selected file request: {selected_file.get('requested')} ({selected_file.get('selection_status')})",
        f"Selected file preview status: {selected_preview.get('status')}",
        f"Selected file hash status: {selected_analysis.get('hash_status')}",
        f"Selected file signature status: {selected_analysis.get('signature_status')}",
        f"Selected file export status: {selected_export.get('status')}",
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
            "Deferred: file-list output, static HTML, search, and timeline.",
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
    parser.add_argument("--selected-file-id", help="Explicit root-entry file id to preview/analyze/export.")
    parser.add_argument("--selected-file-path", help="Explicit root-entry path to preview/analyze/export.")
    parser.add_argument("--selected-file-export-dir", help="Explicit export directory for the selected file.")
    parser.add_argument("--selected-file-export-name", help="Safe output filename for selected-file export.")
    parser.add_argument(
        "--selected-file-preview-mode",
        choices=("raw", "text", "hex"),
        default="hex",
        help="Preview mode for an explicitly selected file. Defaults to hex.",
    )
    parser.add_argument(
        "--selected-file-max-bytes",
        type=int,
        default=DEFAULT_SELECTED_FILE_IN_MEMORY_LIMIT,
        help="Maximum selected-file bytes for in-memory hash/export operations.",
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
        selected_file_id=args.selected_file_id,
        selected_file_path=args.selected_file_path,
        selected_file_export_dir=args.selected_file_export_dir,
        selected_file_export_name=args.selected_file_export_name,
        selected_file_preview_mode=args.selected_file_preview_mode,
        selected_file_max_bytes=args.selected_file_max_bytes,
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
    selected_file_id: str | None = None,
    selected_file_path: str | None = None,
    selected_file_max_bytes: int = DEFAULT_SELECTED_FILE_IN_MEMORY_LIMIT,
) -> dict[str, object]:
    if case_path is None:
        return _validation_error("invalid_input", "missing_case", "--case is required.")

    if selected_file_id and selected_file_path:
        return _validation_error(
            "invalid_input",
            "conflicting_selected_file_forms",
            "Use either --selected-file-id or --selected-file-path, not both.",
        )

    if selected_file_max_bytes < 0:
        return _validation_error(
            "invalid_input",
            "invalid_selected_file_max_bytes",
            "--selected-file-max-bytes must be greater than or equal to zero.",
        )

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
        "ewf_stream": output_dir / "ewf-stream.json",
        "volumes": output_dir / "volumes.json",
        "filesystems": output_dir / "filesystems.json",
        "root_listing": output_dir / "root-listing.json",
        "demo_readiness": output_dir / "demo-readiness.json",
        "selected_file_readiness": output_dir / "selected-file-readiness.json",
        "selected_file_preview": output_dir / "selected-file-preview.json",
        "selected_file_analysis": output_dir / "selected-file-analysis.json",
        "selected_file_export": output_dir / "selected-file-export.json",
        "audit": output_dir / "audit.json",
        "unsupported_sections": output_dir / "unsupported-sections.json",
    }


def _unsupported_sections() -> dict[str, object]:
    rows = [
        (
            "file_list_json_csv_output",
            "S4.5-IMP05",
            "File-list JSON/CSV output is not implemented in S4.5-IMP04.",
        ),
        (
            "static_html_summary",
            "S4.5-IMP05",
            "Static HTML summary output is not implemented in S4.5-IMP04.",
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


def _filesystem_demo_artifacts(
    *,
    selected_path: Path,
    intake_result: Mapping[str, object],
    adapter_name: str,
) -> dict[str, dict[str, object]]:
    if adapter_name == "stub":
        return _demo_not_run_artifacts(
            selected_path=selected_path,
            status="not_run",
            message="Real EWF stream/filesystem demo is not run when --adapter stub is selected.",
            parser_backing="stub_adapter",
        )

    stream_kwargs: dict[str, object] = {}
    adapter = _as_mapping(intake_result.get("adapter"))
    dependency = _as_mapping(adapter.get("dependency"))
    if dependency.get("name") == "pyewf" and dependency.get("available") is False:
        stream_kwargs["pyewf_module"] = None
        stream_kwargs["import_error"] = ImportError(str(dependency.get("message") or "pyewf unavailable"))

    segment_paths = _segment_paths_from_intake(intake_result)
    stream = EwfImageByteStream(
        selected_path,
        segment_paths=segment_paths,
        **stream_kwargs,
    )
    stream_info = stream.describe()
    ewf_stream = {
        "schema_version": "stage4_5.first_testing_ewf_stream.v1",
        "status": stream_info.status.code,
        "logical_media_size": stream_info.size,
        "source_path": stream_info.source_path,
        "segment_count": len(segment_paths),
        "stream": stream_info.to_dict(),
    }

    volumes_result = discover_volumes(stream, strategy="partition_table")
    volumes = {
        "schema_version": "stage4_5.first_testing_volumes.v1",
        "status": volumes_result.status.code,
        "strategy": volumes_result.strategy,
        "volume_count": len(volumes_result.volumes),
        "volume_discovery": volumes_result.to_dict(),
    }

    filesystem_results = []
    root_listing: dict[str, object] | None = None
    if volumes_result.status.ok:
        filesystem_adapter = Pytsk3FilesystemAdapter(image_stream=stream)
        for volume in volumes_result.volumes:
            filesystem_result = filesystem_adapter.inspect_volume(volume)
            filesystem_results.append(filesystem_result.to_dict())
            if filesystem_result.status.ok and filesystem_result.entries:
                root_listing = _root_listing_from_filesystem_result(volume, filesystem_result)
                break

    filesystems = {
        "schema_version": "stage4_5.first_testing_filesystems.v1",
        "status": _filesystem_summary_status(filesystem_results, volumes_result.status.code),
        "filesystem_count": len(filesystem_results),
        "filesystems": filesystem_results,
    }

    if root_listing is None:
        root_listing = _empty_root_listing(
            selected_path=selected_path,
            stream_status=stream_info.status.code,
            volume_status=volumes_result.status.code,
            filesystem_status=filesystems["status"],
        )

    demo_readiness = _demo_readiness(
        ewf_stream=ewf_stream,
        volumes=volumes,
        filesystems=filesystems,
        root_listing=root_listing,
    )
    return {
        "ewf_stream": ewf_stream,
        "volumes": volumes,
        "filesystems": filesystems,
        "root_listing": root_listing,
        "demo_readiness": demo_readiness,
    }


def _demo_not_run_artifacts(
    *,
    selected_path: Path,
    status: str,
    message: str,
    parser_backing: str,
) -> dict[str, dict[str, object]]:
    ewf_stream = {
        "schema_version": "stage4_5.first_testing_ewf_stream.v1",
        "status": status,
        "logical_media_size": None,
        "source_path": str(selected_path),
        "segment_count": 0,
        "message": message,
    }
    volumes = {
        "schema_version": "stage4_5.first_testing_volumes.v1",
        "status": status,
        "strategy": "not_run",
        "volume_count": 0,
        "message": message,
    }
    filesystems = {
        "schema_version": "stage4_5.first_testing_filesystems.v1",
        "status": status,
        "filesystem_count": 0,
        "filesystems": [],
        "message": message,
    }
    root_listing = {
        "schema_version": "stage4_5.first_testing_root_listing.v1",
        "status": status,
        "parser_backing": parser_backing,
        "entry_count": 0,
        "entries": [],
        "message": message,
    }
    return {
        "ewf_stream": ewf_stream,
        "volumes": volumes,
        "filesystems": filesystems,
        "root_listing": root_listing,
        "demo_readiness": _demo_readiness(
            ewf_stream=ewf_stream,
            volumes=volumes,
            filesystems=filesystems,
            root_listing=root_listing,
        ),
    }


def _segment_paths_from_intake(intake_result: Mapping[str, object]) -> tuple[str, ...]:
    discovery = _as_mapping(intake_result.get("segment_discovery"))
    segments = discovery.get("segments", [])
    if isinstance(segments, list):
        paths = [
            str(segment.get("path"))
            for segment in segments
            if isinstance(segment, Mapping) and segment.get("path")
        ]
        if paths:
            return tuple(paths)
    selected = intake_result.get("selected_path") or intake_result.get("source_path")
    return (str(selected),) if selected else ()


class _PrecomputedFilesystemAdapter:
    def __init__(self, filesystem_result: object) -> None:
        self._filesystem_result = filesystem_result
        self.name = filesystem_result.adapter_name
        self.read_only = filesystem_result.read_only

    @property
    def is_available(self) -> bool:
        return self._filesystem_result.adapter_available

    def dependency_status(self):
        return self._filesystem_result.dependency

    def inspect_volume(self, _volume):
        return self._filesystem_result


def _root_listing_from_filesystem_result(volume, filesystem_result) -> dict[str, object]:
    listing = list_directory(
        volume,
        "/",
        _PrecomputedFilesystemAdapter(filesystem_result),
    )
    return {
        "schema_version": "stage4_5.first_testing_root_listing.v1",
        "status": listing["status"]["code"],
        "parser_backing": "real_parser_backed",
        "entry_count": listing["entry_count"],
        "directory_listing": listing,
        "entries": listing["entries"],
    }


def _empty_root_listing(
    *,
    selected_path: Path,
    stream_status: str,
    volume_status: str,
    filesystem_status: str,
) -> dict[str, object]:
    if stream_status == "dependency_unavailable":
        parser_backing = "dependency_blocked"
    elif filesystem_status == "dependency_unavailable":
        parser_backing = "dependency_blocked"
    else:
        parser_backing = "unavailable"
    return {
        "schema_version": "stage4_5.first_testing_root_listing.v1",
        "status": "not_available",
        "parser_backing": parser_backing,
        "entry_count": 0,
        "entries": [],
        "source_path": str(selected_path),
        "stream_status": stream_status,
        "volume_status": volume_status,
        "filesystem_status": filesystem_status,
    }


def _filesystem_summary_status(
    filesystem_results: list[dict[str, object]],
    volume_status: str,
) -> str:
    if not filesystem_results:
        return "not_run" if volume_status != "ok" else "not_available"
    for result in filesystem_results:
        status = _as_mapping(result.get("status")).get("code")
        if status == "ok":
            return "ok"
    first_status = _as_mapping(filesystem_results[0].get("status")).get("code")
    return str(first_status or "not_available")


def _demo_readiness(
    *,
    ewf_stream: Mapping[str, object],
    volumes: Mapping[str, object],
    filesystems: Mapping[str, object],
    root_listing: Mapping[str, object],
) -> dict[str, object]:
    parser_backing = root_listing.get("parser_backing")
    entry_count = int(root_listing.get("entry_count") or 0)
    if parser_backing == "real_parser_backed" and entry_count > 0:
        status = "real_parser_backed_root_listing_available"
        message = "S4.5-IMP03 demo gate produced real-parser-backed root entries."
    elif parser_backing == "dependency_blocked":
        status = "dependency_blocked"
        message = "S4.5-IMP03 demo gate is blocked by dependency availability."
    else:
        status = "not_ready"
        message = "S4.5-IMP03 demo gate did not produce real-parser-backed root entries."
    return {
        "schema_version": "stage4_5.first_testing_demo_readiness.v1",
        "status": status,
        "message": message,
        "ewf_stream_status": ewf_stream.get("status"),
        "logical_media_size": ewf_stream.get("logical_media_size"),
        "volume_strategy": volumes.get("strategy"),
        "volume_status": volumes.get("status"),
        "volume_count": volumes.get("volume_count"),
        "filesystem_status": filesystems.get("status"),
        "root_listing_status": root_listing.get("status"),
        "root_listing_parser_backing": parser_backing,
        "root_entry_count": entry_count,
    }


def _selection_request(
    *,
    selected_file_id: str | None,
    selected_file_path: str | None,
    export_dir: str | Path | None,
    export_name: str | None,
    preview_mode: str,
    max_bytes: int,
) -> dict[str, object]:
    return {
        "requested": bool(selected_file_id or selected_file_path),
        "file_id": selected_file_id,
        "file_path": _normalize_file_path(selected_file_path) if selected_file_path else None,
        "export_dir": str(export_dir) if export_dir is not None else None,
        "export_name": export_name,
        "preview_mode": preview_mode,
        "preview_max_bytes": DEFAULT_PREVIEW_MAX_LENGTH,
        "signature_max_bytes": DEFAULT_SIGNATURE_MAX_BYTES,
        "in_memory_max_bytes": max_bytes,
    }


def _selected_file_artifacts(
    *,
    selected_path: Path,
    intake_result: Mapping[str, object],
    adapter_name: str,
    demo_artifacts: Mapping[str, Mapping[str, object]],
    selection: Mapping[str, object],
    case_id: str,
    evidence_id: str,
) -> dict[str, dict[str, object]]:
    if not selection.get("requested"):
        return _selected_file_not_run_artifacts(
            selection=selection,
            status="not_run",
            message="No selected file was requested; selected-file content operations were not run.",
        )

    root_listing = _as_mapping(demo_artifacts.get("root_listing"))
    if root_listing.get("parser_backing") != "real_parser_backed":
        return _selected_file_not_run_artifacts(
            selection=selection,
            status="content_source_unavailable",
            message="Root listing is not real-parser-backed; selected-file content was not run.",
        )

    entry = _find_selected_entry(
        root_listing.get("entries"),
        file_id=_optional_str(selection.get("file_id")),
        file_path=_optional_str(selection.get("file_path")),
    )
    if entry is None:
        return _selected_file_not_run_artifacts(
            selection=selection,
            status="path_not_found",
            message="Explicitly selected file was not found in the root listing.",
        )

    volume = _volume_for_entry(demo_artifacts, entry)
    if volume is None:
        return _selected_file_not_run_artifacts(
            selection=selection,
            status="content_source_unavailable",
            message="Could not recover the selected file volume context.",
            entry=entry,
        )

    stream_kwargs: dict[str, object] = {}
    adapter = _as_mapping(intake_result.get("adapter"))
    dependency = _as_mapping(adapter.get("dependency"))
    if dependency.get("name") == "pyewf" and dependency.get("available") is False:
        stream_kwargs["pyewf_module"] = None
        stream_kwargs["import_error"] = ImportError(str(dependency.get("message") or "pyewf unavailable"))

    stream = EwfImageByteStream(
        selected_path,
        segment_paths=_segment_paths_from_intake(intake_result),
        **stream_kwargs,
    )
    reader = E01SelectedFileContentReader(stream, volume, entry)
    readiness = reader.check().to_dict()
    readiness.update(
        {
            "selection": dict(selection),
            "case_id": case_id,
            "evidence_id": evidence_id,
            "policy": _selected_file_policy(selection),
        }
    )

    preview = _selected_file_preview_artifact(
        entry=entry,
        reader=reader,
        selection=selection,
    )
    analysis = _selected_file_analysis_artifact(
        entry=entry,
        reader=reader,
        selection=selection,
        case_id=case_id,
        evidence_id=evidence_id,
    )
    export = _selected_file_export_artifact(
        entry=entry,
        reader=reader,
        selection=selection,
    )
    return {
        "readiness": readiness,
        "preview": preview,
        "analysis": analysis,
        "export": export,
    }


def _selected_file_not_run_artifacts(
    *,
    selection: Mapping[str, object],
    status: str,
    message: str,
    entry: Mapping[str, object] | None = None,
) -> dict[str, dict[str, object]]:
    readiness = {
        "schema_version": "stage4_5.selected_file_readiness.v1",
        "status": {
            "code": status,
            "ok": False,
            "message": message,
        },
        "selection": dict(selection),
        "entry": dict(entry or {}),
        "policy": _selected_file_policy(selection),
        "source_kind": "metadata_only",
    }
    return {
        "readiness": readiness,
        "preview": _operation_not_run_artifact(
            schema_version="stage4_5.selected_file_preview.v1",
            operation="preview",
            status=status,
            message=message,
            selection=selection,
            entry=entry,
        ),
        "analysis": {
            "schema_version": "stage4_5.selected_file_analysis.v1",
            "status": status,
            "message": message,
            "selection": dict(selection),
            "entry": dict(entry or {}),
            "hash": _analysis_not_run_result(status, message, "hash"),
            "signature": _analysis_not_run_result(status, message, "signature"),
            "extension_mismatch": _analysis_not_run_result(status, message, "extension_mismatch"),
        },
        "export": _operation_not_run_artifact(
            schema_version="stage4_5.selected_file_export.v1",
            operation="export",
            status=status,
            message=message,
            selection=selection,
            entry=entry,
        ),
    }


def _selected_file_preview_artifact(
    *,
    entry: Mapping[str, object],
    reader: E01SelectedFileContentReader,
    selection: Mapping[str, object],
) -> dict[str, object]:
    provider = E01PreviewContentProvider(
        reader,
        max_preview_bytes=int(selection.get("preview_max_bytes") or DEFAULT_PREVIEW_MAX_LENGTH),
    )
    result = preview_file(
        entry,
        mode=str(selection.get("preview_mode") or "hex"),
        provider=provider,
        max_length=int(selection.get("preview_max_bytes") or DEFAULT_PREVIEW_MAX_LENGTH),
    )
    return {
        "schema_version": "stage4_5.selected_file_preview.v1",
        "status": _as_mapping(result.get("status")).get("code"),
        "selection": dict(selection),
        "content_read": provider.last_result.to_dict() if provider.last_result else None,
        "preview": result,
    }


def _selected_file_analysis_artifact(
    *,
    entry: Mapping[str, object],
    reader: E01SelectedFileContentReader,
    selection: Mapping[str, object],
    case_id: str,
    evidence_id: str,
) -> dict[str, object]:
    signature_provider = E01AnalysisContentProvider(
        reader,
        read_mode="bounded",
        max_bytes=int(selection.get("signature_max_bytes") or DEFAULT_SIGNATURE_MAX_BYTES),
    )
    signature = detect_file_signature(
        entry,
        provider=signature_provider,
        max_bytes=int(selection.get("signature_max_bytes") or DEFAULT_SIGNATURE_MAX_BYTES),
        case_id=case_id,
        evidence_id=evidence_id,
    )
    extension = evaluate_extension_mismatch(signature)

    max_bytes = int(selection.get("in_memory_max_bytes") or DEFAULT_SELECTED_FILE_IN_MEMORY_LIMIT)
    if _entry_size(entry) is not None and int(_entry_size(entry) or 0) > max_bytes:
        hash_result: object = _analysis_not_run_result(
            "file_too_large_for_in_memory_provider",
            "Selected file exceeds the in-memory first-testing limit; hash was not run.",
            "hash",
        )
        hash_status = "file_too_large_for_in_memory_provider"
        hash_content_read = None
    else:
        hash_provider = E01AnalysisContentProvider(
            reader,
            read_mode="full",
            max_bytes=max_bytes,
        )
        hash_object = hash_file_content(
            entry,
            provider=hash_provider,
            case_id=case_id,
            evidence_id=evidence_id,
        )
        hash_result = hash_object.to_dict()
        hash_status = hash_object.status.code
        hash_content_read = hash_provider.last_result.to_dict() if hash_provider.last_result else None

    return {
        "schema_version": "stage4_5.selected_file_analysis.v1",
        "status": _selected_analysis_status(hash_status, signature.status.code),
        "selection": dict(selection),
        "hash": hash_result,
        "hash_content_read": hash_content_read,
        "signature": signature.to_dict(),
        "signature_content_read": (
            signature_provider.last_result.to_dict() if signature_provider.last_result else None
        ),
        "extension_mismatch": extension.to_dict(),
    }


def _selected_file_export_artifact(
    *,
    entry: Mapping[str, object],
    reader: E01SelectedFileContentReader,
    selection: Mapping[str, object],
) -> dict[str, object]:
    export_dir = _optional_str(selection.get("export_dir"))
    if not export_dir:
        return _operation_not_run_artifact(
            schema_version="stage4_5.selected_file_export.v1",
            operation="export",
            status="not_run",
            message="No explicit selected-file export directory was supplied.",
            selection=selection,
            entry=entry,
        )

    max_bytes = int(selection.get("in_memory_max_bytes") or DEFAULT_SELECTED_FILE_IN_MEMORY_LIMIT)
    if _entry_size(entry) is not None and int(_entry_size(entry) or 0) > max_bytes:
        return _operation_not_run_artifact(
            schema_version="stage4_5.selected_file_export.v1",
            operation="export",
            status="file_too_large_for_in_memory_provider",
            message="Selected file exceeds the in-memory first-testing limit; export was refused.",
            selection=selection,
            entry=entry,
        )

    provider = E01ExportContentProvider(reader, max_bytes=max_bytes)
    result = export_file(
        entry,
        export_dir,
        provider=provider,
        output_name=_optional_str(selection.get("export_name")),
    )
    return {
        "schema_version": "stage4_5.selected_file_export.v1",
        "status": result.status.code,
        "selection": dict(selection),
        "content_read": provider.last_result.to_dict() if provider.last_result else None,
        "export": result.to_dict(),
    }


def _operation_not_run_artifact(
    *,
    schema_version: str,
    operation: str,
    status: str,
    message: str,
    selection: Mapping[str, object],
    entry: Mapping[str, object] | None,
) -> dict[str, object]:
    return {
        "schema_version": schema_version,
        "operation": operation,
        "status": status,
        "message": message,
        "selection": dict(selection),
        "entry": dict(entry or {}),
    }


def _analysis_not_run_result(status: str, message: str, operation: str) -> dict[str, object]:
    return {
        "analysis_type": operation,
        "status": {
            "code": status,
            "ok": False,
            "message": message,
        },
    }


def _selected_file_policy(selection: Mapping[str, object]) -> dict[str, object]:
    return {
        "preview_max_bytes": selection.get("preview_max_bytes"),
        "signature_max_bytes": selection.get("signature_max_bytes"),
        "in_memory_max_bytes": selection.get("in_memory_max_bytes"),
        "hash_export_policy": "full-file only at or below in-memory max bytes",
        "preview_signature_policy": "bounded-prefix only",
    }


def _find_selected_entry(
    entries: object,
    *,
    file_id: str | None,
    file_path: str | None,
) -> Mapping[str, object] | None:
    if not isinstance(entries, list):
        return None
    for entry in entries:
        if not isinstance(entry, Mapping):
            continue
        if file_id and str(entry.get("file_id") or "") == file_id:
            return entry
        if file_path and _normalize_file_path(str(entry.get("path") or "")) == file_path:
            return entry
    return None


def _volume_for_entry(
    demo_artifacts: Mapping[str, Mapping[str, object]],
    entry: Mapping[str, object],
) -> VolumeInfo | None:
    volumes_artifact = _as_mapping(demo_artifacts.get("volumes"))
    discovery = _as_mapping(volumes_artifact.get("volume_discovery"))
    raw_volumes = discovery.get("volumes")
    if not isinstance(raw_volumes, list):
        return None
    entry_volume_id = str(entry.get("volume_id") or "")
    for raw_volume in raw_volumes:
        if not isinstance(raw_volume, Mapping):
            continue
        if str(raw_volume.get("volume_id") or "") != entry_volume_id:
            continue
        return VolumeInfo(
            volume_id=str(raw_volume.get("volume_id") or ""),
            volume_index=int(raw_volume.get("volume_index") or 0),
            source_path=str(raw_volume.get("source_path") or entry.get("source_path") or ""),
            stream_type=str(raw_volume.get("stream_type") or "ewf"),
            source_size=int(raw_volume.get("source_size") or 0),
            offset=int(raw_volume.get("offset") or 0),
            length=int(raw_volume.get("length") or 0),
            volume_type=str(raw_volume.get("volume_type") or "partition"),
            description=str(raw_volume.get("description") or "Partition volume."),
            read_only=bool(raw_volume.get("read_only", True)),
            status=VolumeDiscoveryStatus(
                code=_as_mapping(raw_volume.get("status")).get("code", "ok"),
                message=_as_mapping(raw_volume.get("status")).get("message", "Volume context restored."),
            ),
        )
    return None


def _selected_analysis_status(hash_status: str, signature_status: str) -> str:
    if hash_status == "ok" and signature_status in {"ok", "unknown_signature", "insufficient_signature_bytes"}:
        return "ok"
    if hash_status == "file_too_large_for_in_memory_provider" and signature_status in {
        "ok",
        "unknown_signature",
        "insufficient_signature_bytes",
    }:
        return "partial"
    if hash_status == "not_run" and signature_status == "not_run":
        return "not_run"
    return "partial"


def _selected_hash_status(selected_analysis: Mapping[str, object]) -> str | None:
    hash_result = _as_mapping(selected_analysis.get("hash"))
    return _as_mapping(hash_result.get("status")).get("code")


def _selected_signature_status(selected_analysis: Mapping[str, object]) -> str | None:
    signature_result = _as_mapping(selected_analysis.get("signature"))
    return _as_mapping(signature_result.get("status")).get("code")


def _entry_size(entry: Mapping[str, object]) -> int | None:
    value = entry.get("size")
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _normalize_file_path(value: str | None) -> str | None:
    if value is None:
        return None
    text = value.strip().replace("\\", "/")
    if not text:
        return None
    if not text.startswith("/"):
        text = f"/{text}"
    while "//" in text:
        text = text.replace("//", "/")
    return text.rstrip("/") if len(text) > 1 else text


def _optional_str(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


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
    demo_artifacts: Mapping[str, Mapping[str, object]],
    selected_file_artifacts: Mapping[str, Mapping[str, object]],
    audit_artifact: Mapping[str, object],
    artifact_paths: Mapping[str, Path],
    adapter_name: str,
    actor: str | None,
    redact_paths: bool,
) -> dict[str, object]:
    adapter = _as_mapping(intake_result.get("adapter"))
    verification = _as_mapping(intake_result.get("verification"))
    demo_readiness = _as_mapping(demo_artifacts.get("demo_readiness"))
    selected_readiness = _as_mapping(selected_file_artifacts.get("readiness"))
    selected_preview = _as_mapping(selected_file_artifacts.get("preview"))
    selected_analysis = _as_mapping(selected_file_artifacts.get("analysis"))
    selected_export = _as_mapping(selected_file_artifacts.get("export"))
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
        "ewf_stream": {
            "status": _as_mapping(demo_artifacts.get("ewf_stream")).get("status"),
            "logical_media_size": _as_mapping(demo_artifacts.get("ewf_stream")).get("logical_media_size"),
            "artifact_path": str(artifact_paths["ewf_stream"]),
        },
        "volumes": {
            "status": _as_mapping(demo_artifacts.get("volumes")).get("status"),
            "strategy": _as_mapping(demo_artifacts.get("volumes")).get("strategy"),
            "volume_count": _as_mapping(demo_artifacts.get("volumes")).get("volume_count"),
            "artifact_path": str(artifact_paths["volumes"]),
        },
        "filesystem": {
            "status": _as_mapping(demo_artifacts.get("filesystems")).get("status"),
            "filesystem_count": _as_mapping(demo_artifacts.get("filesystems")).get("filesystem_count"),
            "artifact_path": str(artifact_paths["filesystems"]),
        },
        "root_listing": {
            "status": _as_mapping(demo_artifacts.get("root_listing")).get("status"),
            "parser_backing": _as_mapping(demo_artifacts.get("root_listing")).get("parser_backing"),
            "entry_count": _as_mapping(demo_artifacts.get("root_listing")).get("entry_count"),
            "artifact_path": str(artifact_paths["root_listing"]),
        },
        "demo_readiness": {
            **dict(demo_readiness),
            "artifact_path": str(artifact_paths["demo_readiness"]),
        },
        "selected_file": {
            "requested": bool(_as_mapping(selected_readiness.get("selection")).get("requested")),
            "selection_status": _as_mapping(selected_readiness.get("status")).get("code")
            or selected_readiness.get("status"),
            "policy": _as_mapping(selected_readiness.get("policy")),
            "readiness": {
                "status": _as_mapping(selected_readiness.get("status")).get("code")
                or selected_readiness.get("status"),
                "source_kind": selected_readiness.get("source_kind"),
                "artifact_path": str(artifact_paths["selected_file_readiness"]),
            },
            "preview": {
                "status": selected_preview.get("status"),
                "artifact_path": str(artifact_paths["selected_file_preview"]),
            },
            "analysis": {
                "status": selected_analysis.get("status"),
                "hash_status": _selected_hash_status(selected_analysis),
                "signature_status": _selected_signature_status(selected_analysis),
                "artifact_path": str(artifact_paths["selected_file_analysis"]),
            },
            "export": {
                "status": selected_export.get("status"),
                "artifact_path": str(artifact_paths["selected_file_export"]),
            },
        },
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
