"""Segment discovery for EWF/EnCase-style E01 evidence sets."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Iterable


EWF_SEGMENT_EXTENSION_PATTERN = re.compile(r"^\.E(?P<number>\d{2})$", re.IGNORECASE)


@dataclass(frozen=True)
class SegmentWarning:
    """Structured warning emitted during segment discovery."""

    code: str
    message: str
    path: str | None = None
    segment_number: int | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "code": self.code,
            "message": self.message,
            "path": self.path,
            "segment_number": self.segment_number,
        }


@dataclass(frozen=True)
class SegmentInfo:
    """One discovered EWF segment file."""

    segment_number: int
    path: str
    filename: str
    extension: str
    is_selected: bool = False

    def to_dict(self) -> dict[str, object]:
        return {
            "segment_number": self.segment_number,
            "path": self.path,
            "filename": self.filename,
            "extension": self.extension,
            "is_selected": self.is_selected,
        }


@dataclass(frozen=True)
class SegmentDiscoveryResult:
    """Stable result shape for E01 segment discovery."""

    selected_path: str
    base_name: str
    is_valid_input: bool
    is_complete: bool
    read_only: bool
    segments: tuple[SegmentInfo, ...] = field(default_factory=tuple)
    warnings: tuple[SegmentWarning, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        return {
            "selected_path": self.selected_path,
            "base_name": self.base_name,
            "is_valid_input": self.is_valid_input,
            "is_complete": self.is_complete,
            "read_only": self.read_only,
            "segments": [segment.to_dict() for segment in self.segments],
            "warnings": [warning.to_dict() for warning in self.warnings],
        }


def discover_e01_segments(selected_path: str | Path) -> SegmentDiscoveryResult:
    """Discover sibling EWF segments for a selected first `.E01` segment.

    This function only inspects paths and directory entries. It does not open or
    parse evidence file content.
    """

    path = Path(selected_path).expanduser().resolve(strict=False)
    selected_segment_number = _parse_segment_number(path.suffix)
    warnings: list[SegmentWarning] = []

    if selected_segment_number != 1:
        return SegmentDiscoveryResult(
            selected_path=str(path),
            base_name=path.stem,
            is_valid_input=False,
            is_complete=False,
            read_only=True,
            warnings=(
                SegmentWarning(
                    code="unsupported_input_extension",
                    message="Selected path must be the first EWF segment with extension .E01.",
                    path=str(path),
                ),
            ),
        )

    if not path.parent.exists():
        return SegmentDiscoveryResult(
            selected_path=str(path),
            base_name=path.stem,
            is_valid_input=False,
            is_complete=False,
            read_only=True,
            warnings=(
                SegmentWarning(
                    code="parent_directory_not_found",
                    message="Selected path parent directory does not exist.",
                    path=str(path.parent),
                ),
            ),
        )

    try:
        sibling_paths = list(path.parent.iterdir())
    except OSError as error:
        return SegmentDiscoveryResult(
            selected_path=str(path),
            base_name=path.stem,
            is_valid_input=False,
            is_complete=False,
            read_only=True,
            warnings=(
                SegmentWarning(
                    code="parent_directory_unreadable",
                    message=f"Could not list selected path parent directory: {error}",
                    path=str(path.parent),
                ),
            ),
        )

    segment_paths = _matching_segment_paths(path, sibling_paths, warnings)
    selected_exists = path.exists()
    if not selected_exists:
        warnings.append(
            SegmentWarning(
                code="selected_segment_not_found",
                message="Selected .E01 segment path does not exist.",
                path=str(path),
                segment_number=1,
            )
        )

    segments = tuple(
        SegmentInfo(
            segment_number=number,
            path=str(segment_path.resolve(strict=False)),
            filename=segment_path.name,
            extension=segment_path.suffix,
            is_selected=segment_path.resolve(strict=False) == path,
        )
        for number, segment_path in sorted(segment_paths.items())
    )

    warnings.extend(_missing_segment_warnings(path, segment_paths.keys()))

    return SegmentDiscoveryResult(
        selected_path=str(path),
        base_name=path.stem,
        is_valid_input=selected_exists,
        is_complete=selected_exists
        and not any(warning.code == "missing_segment" for warning in warnings),
        read_only=True,
        segments=segments,
        warnings=tuple(warnings),
    )


def _matching_segment_paths(
    selected_path: Path,
    sibling_paths: Iterable[Path],
    warnings: list[SegmentWarning],
) -> dict[int, Path]:
    segment_paths: dict[int, Path] = {}

    for sibling in sibling_paths:
        if sibling.stem != selected_path.stem:
            continue

        segment_number = _parse_segment_number(sibling.suffix)
        if segment_number is None:
            if sibling.suffix.upper().startswith(".E"):
                warnings.append(
                    SegmentWarning(
                        code="unsupported_segment_extension",
                        message="Sibling file uses an unsupported EWF segment extension pattern.",
                        path=str(sibling.resolve(strict=False)),
                    )
                )
            continue

        if segment_number in segment_paths:
            warnings.append(
                SegmentWarning(
                    code="duplicate_segment_number",
                    message="Multiple sibling files appear to use the same EWF segment number.",
                    path=str(sibling.resolve(strict=False)),
                    segment_number=segment_number,
                )
            )
            continue

        segment_paths[segment_number] = sibling

    return segment_paths


def _missing_segment_warnings(
    selected_path: Path,
    present_segment_numbers: Iterable[int],
) -> list[SegmentWarning]:
    present_numbers = sorted(present_segment_numbers)
    if not present_numbers:
        return []

    warnings: list[SegmentWarning] = []
    for segment_number in range(1, present_numbers[-1] + 1):
        if segment_number not in present_numbers:
            expected_path = selected_path.with_suffix(f".E{segment_number:02d}")
            warnings.append(
                SegmentWarning(
                    code="missing_segment",
                    message=f"Expected segment .E{segment_number:02d} is missing before a later segment.",
                    path=str(expected_path.resolve(strict=False)),
                    segment_number=segment_number,
                )
            )

    return warnings


def _parse_segment_number(extension: str) -> int | None:
    match = EWF_SEGMENT_EXTENSION_PATTERN.match(extension)
    if not match:
        return None

    segment_number = int(match.group("number"))
    if segment_number < 1:
        return None

    return segment_number
