"""Stage 1 evidence intake command boundary."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from app.backend.forensic_core import (
    EwfReaderAdapter,
    EwfReaderWarning,
    PyewfEwfReaderAdapter,
    SegmentWarning,
    StubEwfReaderAdapter,
    VerificationStatus,
    discover_e01_segments,
)


INTAKE_SCHEMA_VERSION = "stage1.intake.v1"


def run_e01_intake(
    selected_path: str | Path,
    adapter: EwfReaderAdapter | None = None,
) -> dict[str, object]:
    """Run dependency-safe Stage 1 E01 intake and return JSON-ready data."""

    reader = adapter or PyewfEwfReaderAdapter()
    discovery = discover_e01_segments(selected_path)
    dependency = reader.dependency_status()
    segment_paths = tuple(segment.path for segment in discovery.segments)

    if not discovery.is_valid_input:
        verification = VerificationStatus(
            status="not_run",
            supported=False,
            message="Metadata and verification were skipped because segment discovery did not produce a valid .E01 input.",
            details={"segment_count": len(segment_paths)},
        )
        adapter_available = reader.is_available
        adapter_read_only = reader.read_only
        metadata: dict[str, object] = {}
        reader_warnings: tuple[EwfReaderWarning, ...] = ()
        intake_warnings = (
            {
                "source": "intake",
                "code": "metadata_skipped",
                "message": "Metadata read skipped for invalid or missing selected .E01 input.",
                "path": discovery.selected_path,
            },
        )
        status = "invalid_input"
    else:
        try:
            metadata_result = reader.read_metadata(segment_paths)
        except Exception as error:  # pragma: no cover - defensive command boundary
            verification = VerificationStatus(
                status="error",
                supported=False,
                message=f"Reader adapter failed during metadata read: {error}",
                details={"segment_count": len(segment_paths)},
            )
            adapter_available = reader.is_available
            adapter_read_only = reader.read_only
            metadata = {}
            reader_warnings = (
                EwfReaderWarning(
                    code="reader_error",
                    message="Reader adapter raised an unexpected error during metadata read.",
                ),
            )
            intake_warnings = ()
            status = "reader_error"
        else:
            verification = metadata_result.verification
            dependency = metadata_result.dependency
            adapter_available = metadata_result.adapter_available
            adapter_read_only = metadata_result.read_only
            metadata = metadata_result.metadata
            reader_warnings = metadata_result.warnings
            intake_warnings = ()
            reader_warning_codes = {warning.code for warning in reader_warnings}
            if "reader_open_failed" in reader_warning_codes:
                status = "reader_error"
            elif "real_reader_not_implemented" in reader_warning_codes:
                status = "reader_not_implemented"
            elif adapter_available:
                status = "ok"
            else:
                status = "metadata_unavailable"

    warnings = (
        _segment_warnings(discovery.warnings)
        + _reader_warnings(reader_warnings)
        + list(intake_warnings)
    )
    read_only = bool(discovery.read_only and adapter_read_only)

    return {
        "schema_version": INTAKE_SCHEMA_VERSION,
        "status": status,
        "source_path": discovery.selected_path,
        "selected_path": discovery.selected_path,
        "read_only": read_only,
        "segment_count": len(discovery.segments),
        "segment_discovery": discovery.to_dict(),
        "adapter": {
            "name": reader.name,
            "available": adapter_available,
            "read_only": adapter_read_only,
            "dependency": dependency.to_dict(),
        },
        "metadata": dict(metadata),
        "verification": verification.to_dict(),
        "warnings": warnings,
    }


def intake_to_json(
    selected_path: str | Path,
    adapter: EwfReaderAdapter | None = None,
    *,
    indent: int | None = 2,
) -> str:
    """Run intake and serialize the result as stable JSON."""

    return json.dumps(run_e01_intake(selected_path, adapter), indent=indent, sort_keys=True)


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point for `python -m app.backend.api.intake`."""

    parser = argparse.ArgumentParser(description="Run Stage 1 E01 intake and print JSON.")
    parser.add_argument("path", help="Path to the selected .E01 segment.")
    parser.add_argument(
        "--adapter",
        choices=("pyewf", "stub"),
        default="pyewf",
        help="Reader adapter to use. Defaults to pyewf with graceful dependency-unavailable output.",
    )
    args = parser.parse_args(argv)

    adapter: EwfReaderAdapter
    if args.adapter == "stub":
        adapter = StubEwfReaderAdapter()
    else:
        adapter = PyewfEwfReaderAdapter()

    result = run_e01_intake(args.path, adapter)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 2 if result["status"] == "invalid_input" else 0


def _segment_warnings(warnings: Sequence[SegmentWarning]) -> list[dict[str, object]]:
    return [
        {"source": "segment_discovery", **warning.to_dict()}
        for warning in warnings
    ]


def _reader_warnings(warnings: Sequence[EwfReaderWarning]) -> list[dict[str, object]]:
    return [
        {"source": "reader", **warning.to_dict()}
        for warning in warnings
    ]


if __name__ == "__main__":
    raise SystemExit(main())
