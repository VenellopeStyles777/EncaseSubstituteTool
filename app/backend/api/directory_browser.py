"""Interactive Stage 4.5 directory browser over parser-backed listings."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import shlex
import sys
from typing import Any, Mapping, Sequence, TextIO

from app.backend.api.directory_listing import list_directory
from app.backend.api.intake import run_e01_intake
from app.backend.forensic_core import (
    EwfImageByteStream,
    PyewfEwfReaderAdapter,
    Pytsk3FilesystemAdapter,
    VolumeInfo,
    discover_volumes,
)


@dataclass(frozen=True)
class DirectoryBrowserSetupResult:
    """Setup result for the interactive browser CLI."""

    status: str
    message: str
    session: DirectoryBrowserSession | None = None
    selected_path: Path | None = None
    evidence_root: Path | None = None
    segment_count: int = 0
    root_listing: Mapping[str, object] | None = None
    read_only_asserted: bool = True
    source_modified: bool = False

    @property
    def ok(self) -> bool:
        return self.status == "ok" and self.session is not None


class DirectoryBrowserSession:
    """Stateful command loop around the reviewed directory listing boundary."""

    def __init__(
        self,
        *,
        volume: VolumeInfo,
        filesystem_adapter: object,
        input_stream: TextIO | None = None,
        output_stream: TextIO | None = None,
        segment_count: int | None = None,
        display_label: str | None = None,
        prompt: bool = False,
    ) -> None:
        self.volume = volume
        self.filesystem_adapter = filesystem_adapter
        self.input_stream = input_stream or sys.stdin
        self.output_stream = output_stream or sys.stdout
        self.current_path = "/"
        self.segment_count = segment_count
        self.display_label = _display_label(display_label)
        self.volume_label = _volume_label(volume)
        self.prompt = prompt
        self.last_listing: dict[str, object] | None = None
        self.root_listing: dict[str, object] | None = None
        self.commands_run = 0
        self.source_modified = False

    def run(self) -> dict[str, object]:
        """Run the browser loop until EOF, exit, or quit."""

        self._write_header()
        root_listing = self._list_and_print("/")
        self.root_listing = root_listing
        if _status_code(root_listing) != "ok":
            self._write_line("Browser blocked: root listing is unavailable.")
            self._write_footer()
            return self.summary(exit_code=2)

        exit_code = 0
        while True:
            if self.prompt:
                self.output_stream.write(
                    f"{self.display_label} [{self.volume_label}] {self.current_path}> "
                )
                self.output_stream.flush()
            line = self.input_stream.readline()
            if line == "":
                break
            should_continue = self.execute_line(line)
            if not should_continue:
                break

        self._write_footer()
        return self.summary(exit_code=exit_code)

    def execute_line(self, line: str) -> bool:
        """Execute one browser command. Return False when the loop should exit."""

        text = line.strip()
        if not text:
            return True
        self.commands_run += 1

        try:
            parts = shlex.split(text)
        except ValueError as error:
            self._write_line(f"Invalid command: {error}")
            return True

        if not parts:
            return True

        command = parts[0].lower()
        if command in {"exit", "quit"}:
            self._write_line("Exiting directory browser.")
            return False
        if command in {"help", "?"}:
            self._write_help()
            return True
        if command == "pwd":
            self._write_line(f"Current path: {self.current_path}")
            return True
        if command in {"ls", "dir"}:
            self._list_and_print(self.current_path)
            return True
        if command == "root":
            self._change_directory("/")
            return True
        if command == "cd":
            if len(parts) < 2:
                self._write_line("Usage: cd <path-or-name>")
                return True
            target = " ".join(parts[1:])
            self._change_directory(target)
            return True

        self._write_line(f"Unknown command: {parts[0]}. Type help for commands.")
        return True

    def summary(self, *, exit_code: int) -> dict[str, object]:
        listing = self.last_listing or {}
        root_listing = self.root_listing or {}
        return {
            "exit_code": exit_code,
            "commands_run": self.commands_run,
            "current_path": self.current_path,
            "display_label": self.display_label,
            "volume_label": self.volume_label,
            "segment_count": self.segment_count,
            "root_status": _status_code(root_listing),
            "root_parser_backing": _parser_backing(root_listing),
            "root_entry_count": _entry_count(root_listing),
            "last_status": _status_code(listing),
            "last_parser_backing": _parser_backing(listing),
            "last_entry_count": _entry_count(listing),
            "last_file_count": _entry_type_counts(listing)["file"],
            "last_directory_count": _entry_type_counts(listing)["directory"],
            "last_other_count": _entry_type_counts(listing)["other"],
            "read_only_asserted": _read_only_asserted(listing),
            "source_modified": self.source_modified,
        }

    def _change_directory(self, target: str) -> None:
        requested_path = self._resolve_path(target)
        listing = list_directory(self.volume, requested_path, self.filesystem_adapter)
        if _status_code(listing) == "ok":
            self.current_path = _normalize_path(str(listing.get("directory_path") or requested_path))
            self._print_listing(listing)
            return

        self.last_listing = dict(listing)
        self._write_line(
            f"Cannot change directory: {_status_code(listing)} "
            f"parser_backing={_parser_backing(listing)}"
        )
        self._write_counts(listing)

    def _list_and_print(self, path: str) -> dict[str, object]:
        listing = list_directory(self.volume, path, self.filesystem_adapter)
        self._print_listing(listing)
        return dict(listing)

    def _print_listing(self, listing: Mapping[str, object]) -> None:
        self.last_listing = dict(listing)
        path = str(listing.get("directory_path") or self.current_path)
        self._write_line(f"Path: {path}")
        self._write_line(
            f"Status: {_status_code(listing)} parser_backing={_parser_backing(listing)}"
        )
        self._write_counts(listing)
        entries = listing.get("entries")
        if isinstance(entries, list) and entries:
            self._write_line("Name\tType\tSize\tAllocated\tDeleted\tModified")
            for entry in entries:
                if isinstance(entry, Mapping):
                    timestamps = _as_mapping(entry.get("timestamps"))
                    self._write_line(
                        "\t".join(
                            [
                                str(entry.get("name") or ""),
                                str(entry.get("entry_type") or "unknown"),
                                "" if entry.get("size") is None else str(entry.get("size")),
                                _bool_cell(entry.get("allocated")),
                                _bool_cell(entry.get("deleted")),
                                str(timestamps.get("modified") or ""),
                            ]
                        )
                    )

    def _write_header(self) -> None:
        self._write_line("Stage 4.5 interactive logical-image directory browser")
        self._write_line(f"Image: {self.display_label}")
        self._write_line(f"Volume: {self.volume_label}")
        self._write_line("Read-only browser; no file content, export, hash, search, or crawl.")
        if self.segment_count is not None:
            self._write_line(f"Segment count: {self.segment_count}")

    def _write_footer(self) -> None:
        self._write_line("Source modified: false")
        self._write_line(f"Read-only asserted: {_bool_cell(_read_only_asserted(self.last_listing or {}))}")

    def _write_help(self) -> None:
        self._write_line("Commands:")
        self._write_line("- dir or ls: list direct child entries")
        self._write_line("- cd <path-or-name>: move to a directory")
        self._write_line("- cd ..: move to the parent directory")
        self._write_line("- cd / or root: return to filesystem root")
        self._write_line("- pwd: print the current in-image path")
        self._write_line("- exit or quit: leave the browser")
        self._write_line("Boundaries: no content reads, exports, hashes, recursive crawl, search, or timeline.")

    def _write_counts(self, listing: Mapping[str, object]) -> None:
        counts = _entry_type_counts(listing)
        self._write_line(
            f"Entries: {_entry_count(listing)} "
            f"files={counts['file']} directories={counts['directory']} other={counts['other']}"
        )

    def _resolve_path(self, target: str) -> str:
        text = (target or "").strip().replace("\\", "/")
        if text.lower() == "root":
            return "/"
        if text in {"", "."}:
            return self.current_path
        if text == "..":
            return _parent_path(self.current_path)
        base_parts: list[str]
        if text.startswith("/"):
            base_parts = []
        else:
            base_parts = _path_parts(self.current_path)
        for part in text.split("/"):
            if part in {"", "."}:
                continue
            if part == "..":
                if base_parts:
                    base_parts.pop()
                continue
            base_parts.append(part)
        return "/" + "/".join(base_parts) if base_parts else "/"

    def _write_line(self, text: str) -> None:
        self.output_stream.write(f"{text}\n")


def build_directory_browser_session(
    evidence_path: str | Path | None = None,
    *,
    evidence_dir: str | Path | None = None,
    first_segment: str | Path | None = None,
    input_stream: TextIO | None = None,
    output_stream: TextIO | None = None,
    project_name: str | None = None,
    redact_paths: bool = False,
    prompt: bool = False,
) -> DirectoryBrowserSetupResult:
    """Build a browser session from a direct .E01 path or evidence dir/segment."""

    validation = _resolve_evidence_input(
        evidence_path=evidence_path,
        evidence_dir=evidence_dir,
        first_segment=first_segment,
    )
    if validation["status"] != "ok":
        return DirectoryBrowserSetupResult(
            status=str(validation["status"]),
            message=str(validation["message"]),
            read_only_asserted=True,
            source_modified=False,
        )

    selected_path = validation["selected_path"]
    evidence_root = validation["evidence_root"]
    assert isinstance(selected_path, Path)
    assert isinstance(evidence_root, Path)

    intake_result = run_e01_intake(selected_path, PyewfEwfReaderAdapter())
    segment_count = int(intake_result.get("segment_count") or 0)
    segment_paths = _segment_paths_from_intake(intake_result)
    stream = EwfImageByteStream(
        selected_path,
        segment_paths=segment_paths,
        **_ewf_stream_kwargs_from_intake(intake_result),
    )
    stream_info = stream.describe()
    if not stream_info.status.ok:
        return _setup_failure(
            status=stream_info.status.code,
            message=stream_info.status.message,
            selected_path=selected_path,
            evidence_root=evidence_root,
            segment_count=segment_count,
            redact_paths=redact_paths,
        )

    volumes_result = discover_volumes(stream, strategy="partition_table")
    if not volumes_result.status.ok:
        return _setup_failure(
            status=volumes_result.status.code,
            message=volumes_result.status.message,
            selected_path=selected_path,
            evidence_root=evidence_root,
            segment_count=segment_count,
            redact_paths=redact_paths,
        )

    filesystem_adapter = Pytsk3FilesystemAdapter(image_stream=stream)
    last_listing: Mapping[str, object] | None = None
    for volume in volumes_result.volumes:
        root_listing = list_directory(volume, "/", filesystem_adapter)
        last_listing = root_listing
        if _status_code(root_listing) == "ok":
            display_label = (
                _redact_evidence_root(project_name, str(evidence_root))
                if redact_paths and project_name is not None
                else project_name
            )
            session = DirectoryBrowserSession(
                volume=volume,
                filesystem_adapter=filesystem_adapter,
                input_stream=input_stream,
                output_stream=output_stream,
                segment_count=segment_count,
                display_label=display_label,
                prompt=prompt,
            )
            return DirectoryBrowserSetupResult(
                status="ok",
                message="Directory browser is ready.",
                session=session,
                selected_path=selected_path,
                evidence_root=evidence_root,
                segment_count=segment_count,
                root_listing=root_listing,
                read_only_asserted=_read_only_asserted(root_listing),
                source_modified=False,
            )

    status = _status_code(last_listing or {})
    return _setup_failure(
        status=status or "filesystem_unavailable",
        message="No parser-backed root directory listing was available.",
        selected_path=selected_path,
        evidence_root=evidence_root,
        segment_count=segment_count,
        redact_paths=redact_paths,
        root_listing=last_listing,
    )


def directory_browser_to_summary(
    evidence_path: str | Path | None = None,
    *,
    evidence_dir: str | Path | None = None,
    first_segment: str | Path | None = None,
    commands: str,
    project_name: str | None = None,
) -> dict[str, object]:
    """Run a scripted browser session and return its non-content summary."""

    from io import StringIO

    setup = build_directory_browser_session(
        evidence_path,
        evidence_dir=evidence_dir,
        first_segment=first_segment,
        input_stream=StringIO(commands),
        output_stream=StringIO(),
        project_name=project_name,
    )
    if not setup.ok:
        return {
            "exit_code": 2,
            "setup_status": setup.status,
            "message": setup.message,
            "segment_count": setup.segment_count,
            "read_only_asserted": setup.read_only_asserted,
            "source_modified": setup.source_modified,
        }
    assert setup.session is not None
    summary = setup.session.run()
    summary["setup_status"] = setup.status
    return summary


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Browse a real E01-backed filesystem from the terminal.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        help="Path to the selected .E01 first segment.",
    )
    parser.add_argument("--evidence-dir", help="Evidence directory containing the first segment.")
    parser.add_argument("--first-segment", help="First segment filename when --evidence-dir is used.")
    parser.add_argument("--project-name", help="Project/logical image label for the browser header and prompt.")
    parser.add_argument(
        "--redact-paths",
        action="store_true",
        help="Redact local evidence root paths in setup error output.",
    )
    args = parser.parse_args(argv)

    setup = build_directory_browser_session(
        args.path,
        evidence_dir=args.evidence_dir,
        first_segment=args.first_segment,
        project_name=args.project_name,
        redact_paths=args.redact_paths,
        prompt=sys.stdin.isatty(),
    )
    if not setup.ok:
        message = setup.message
        if args.redact_paths and setup.evidence_root is not None:
            message = _redact_evidence_root(message, str(setup.evidence_root))
        print(f"Directory browser unavailable: {setup.status}")
        print(message)
        print(f"Segment count: {setup.segment_count}")
        print("Source modified: false")
        print(f"Read-only asserted: {_bool_cell(setup.read_only_asserted)}")
        return 2

    assert setup.session is not None
    summary = setup.session.run()
    return int(summary.get("exit_code") or 0)


def _resolve_evidence_input(
    *,
    evidence_path: str | Path | None,
    evidence_dir: str | Path | None,
    first_segment: str | Path | None,
) -> dict[str, object]:
    has_direct_path = evidence_path is not None
    has_evidence_dir = evidence_dir is not None
    has_first_segment = first_segment is not None

    if has_direct_path and (has_evidence_dir or has_first_segment):
        return _input_error("conflicting_input_forms", "Use either a direct .E01 path or --evidence-dir with --first-segment, not both.")
    if not has_direct_path and not has_evidence_dir:
        return _input_error("missing_input", "Provide a direct .E01 path or --evidence-dir with --first-segment.")
    if has_evidence_dir and not has_first_segment:
        return _input_error("missing_first_segment", "--first-segment is required when --evidence-dir is used.")
    if has_first_segment and not has_evidence_dir:
        return _input_error("first_segment_without_evidence_dir", "--first-segment can only be used with --evidence-dir.")

    if has_evidence_dir:
        evidence_root = _resolve(evidence_dir)
        first_segment_path = Path(str(first_segment))
        if first_segment_path.is_absolute() or len(first_segment_path.parts) != 1:
            return _input_error("first_segment_must_be_filename", "--first-segment must be a filename inside --evidence-dir.")
        selected_path = evidence_root / first_segment_path
    else:
        selected_path = _resolve(evidence_path)
        evidence_root = selected_path.parent

    extension_error = _validate_e01_first_segment(selected_path)
    if extension_error is not None:
        return extension_error
    if not selected_path.exists():
        return _input_error("input_not_found", "The selected .E01 path does not exist.")
    if selected_path.is_dir():
        return _input_error("input_is_directory", "The selected evidence path is a directory; select the .E01 file.")

    return {
        "status": "ok",
        "selected_path": _resolve(selected_path),
        "evidence_root": _resolve(evidence_root),
    }


def _validate_e01_first_segment(path: Path) -> dict[str, object] | None:
    suffix = path.suffix.lower()
    if suffix.startswith(".e") and suffix[2:].isdigit() and int(suffix[2:]) > 1:
        return _input_error("select_first_e01_segment", "Select the .E01 first segment as the primary input.")
    if suffix != ".e01":
        return _input_error("unsupported_input_extension", "The browser accepts only a selected .E01 first segment.")
    return None


def _input_error(code: str, message: str) -> dict[str, object]:
    return {
        "status": "invalid_input",
        "code": code,
        "message": message,
    }


def _setup_failure(
    *,
    status: str,
    message: str,
    selected_path: Path,
    evidence_root: Path,
    segment_count: int,
    redact_paths: bool,
    root_listing: Mapping[str, object] | None = None,
) -> DirectoryBrowserSetupResult:
    output_message = _redact_evidence_root(message, str(evidence_root)) if redact_paths else message
    return DirectoryBrowserSetupResult(
        status=status,
        message=output_message,
        selected_path=selected_path,
        evidence_root=evidence_root,
        segment_count=segment_count,
        root_listing=root_listing,
        read_only_asserted=_read_only_asserted(root_listing or {}),
        source_modified=False,
    )


def _segment_paths_from_intake(intake_result: Mapping[str, object]) -> list[str]:
    discovery = _as_mapping(intake_result.get("segment_discovery"))
    raw_segments = discovery.get("segments")
    paths = []
    for segment in raw_segments if isinstance(raw_segments, list) else []:
        if isinstance(segment, Mapping) and segment.get("path") is not None:
            paths.append(str(segment["path"]))
    if not paths and intake_result.get("selected_path") is not None:
        paths.append(str(intake_result["selected_path"]))
    return paths


def _ewf_stream_kwargs_from_intake(intake_result: Mapping[str, object]) -> dict[str, object]:
    adapter = _as_mapping(intake_result.get("adapter"))
    dependency = _as_mapping(adapter.get("dependency"))
    if dependency.get("name") == "pyewf" and dependency.get("available") is False:
        return {
            "pyewf_module": None,
            "import_error": ImportError(str(dependency.get("message") or "pyewf unavailable")),
        }
    return {}


def _status_code(listing: Mapping[str, object]) -> str:
    return str(_as_mapping(listing.get("status")).get("code") or "")


def _entry_count(listing: Mapping[str, object]) -> int:
    try:
        return int(listing.get("entry_count") or 0)
    except (TypeError, ValueError):
        return 0


def _entry_type_counts(listing: Mapping[str, object]) -> dict[str, int]:
    counts = {"file": 0, "directory": 0, "other": 0}
    entries = listing.get("entries")
    for entry in entries if isinstance(entries, list) else []:
        if not isinstance(entry, Mapping):
            continue
        entry_type = str(entry.get("entry_type") or "unknown")
        if entry_type == "file":
            counts["file"] += 1
        elif entry_type == "directory":
            counts["directory"] += 1
        else:
            counts["other"] += 1
    return counts


def _parser_backing(listing: Mapping[str, object]) -> str:
    adapter = _as_mapping(listing.get("adapter"))
    status_code = _status_code(listing)
    if (
        adapter.get("name") == "pytsk3-filesystem-adapter"
        and adapter.get("available") is True
        and status_code in {"ok", "path_not_directory", "path_not_found"}
    ):
        return "real_parser_backed"
    if status_code == "":
        return "not_run"
    return "unavailable"


def _read_only_asserted(listing: Mapping[str, object]) -> bool:
    if "read_only" not in listing:
        return True
    return bool(listing.get("read_only"))


def _normalize_path(path: str) -> str:
    text = (path or "/").strip().replace("\\", "/")
    if not text.startswith("/"):
        text = f"/{text}"
    while "//" in text:
        text = text.replace("//", "/")
    return text.rstrip("/") if len(text) > 1 else "/"


def _path_parts(path: str) -> list[str]:
    normalized = _normalize_path(path)
    if normalized == "/":
        return []
    return [part for part in normalized.strip("/").split("/") if part]


def _parent_path(path: str) -> str:
    parts = _path_parts(path)
    if parts:
        parts.pop()
    return "/" + "/".join(parts) if parts else "/"


def _display_label(value: str | None) -> str:
    text = (value or "").strip()
    return text or "Logical Image"


def _volume_label(volume: VolumeInfo) -> str:
    return str(volume.volume_id or "selected-volume")


def _bool_cell(value: object) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    return ""


def _resolve(path: str | Path | None) -> Path:
    if path is None:
        raise ValueError("Path cannot be None")
    return Path(path).expanduser().resolve(strict=False)


def _as_mapping(value: object) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _redact_evidence_root(text: str, evidence_root: str) -> str:
    if not evidence_root:
        return text
    variants = {
        evidence_root,
        evidence_root.replace("/", "\\"),
    }
    redacted = text
    for variant in sorted(variants, key=len, reverse=True):
        if variant:
            redacted = redacted.replace(variant, "<EVIDENCE_ROOT>")
    return redacted


if __name__ == "__main__":
    raise SystemExit(main())
