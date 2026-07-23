"""Tests for the S4.5-IMP09B interactive directory browser."""

from io import StringIO
from pathlib import Path
import shutil

from app.backend.api.directory_browser import DirectoryBrowserSession
from app.backend.forensic_core import (
    FilesystemDependencyStatus,
    FilesystemEntry,
    FilesystemResult,
    FilesystemStatus,
    Pytsk3FilesystemAdapter,
    VolumeDiscoveryStatus,
    VolumeInfo,
)


def _sample_volume() -> VolumeInfo:
    return VolumeInfo(
        volume_id="volume-0",
        volume_index=0,
        source_path="C:/fixtures/tiny.raw",
        stream_type="ewf",
        source_size=1024,
        offset=0,
        length=1024,
        volume_type="ntfs",
        description="Fake parser-backed volume.",
        read_only=True,
        status=VolumeDiscoveryStatus(
            code="ok",
            message="Volume available.",
        ),
    )


class FakeBrowserAdapter:
    name = "pytsk3-filesystem-adapter"
    read_only = True

    @property
    def is_available(self):
        return True

    def dependency_status(self):
        return FilesystemDependencyStatus(
            name="pytsk3",
            available=True,
            message="fake parser available",
        )

    def inspect_volume(self, volume):
        return self._result(
            volume,
            root_path="/",
            entries=(
                self._entry(volume, file_id="volume-0:2", path="/Users", name="Users", entry_type="directory"),
                self._entry(
                    volume,
                    file_id="volume-0:3",
                    path="/Program Files",
                    name="Program Files",
                    entry_type="directory",
                ),
                self._entry(volume, file_id="volume-0:4", path="/note.txt", name="note.txt", entry_type="file"),
            ),
        )

    def list_directory(self, volume, directory_path):
        if directory_path == "/Users":
            return self._result(
                volume,
                root_path="/Users",
                entries=(
                    self._entry(volume, file_id="volume-0:5", path="/Users/Profile", name="Profile", entry_type="directory"),
                    self._entry(volume, file_id="volume-0:6", path="/Users/nested.txt", name="nested.txt", entry_type="file"),
                ),
            )
        if directory_path == "/Users/Profile":
            return self._result(
                volume,
                root_path="/Users/Profile",
                entries=(
                    self._entry(volume, file_id="volume-0:7", path="/Users/Profile/deep.txt", name="deep.txt", entry_type="file"),
                ),
            )
        if directory_path == "/Program Files":
            return self._result(
                volume,
                root_path="/Program Files",
                entries=(
                    self._entry(
                        volume,
                        file_id="volume-0:8",
                        path="/Program Files/app.exe",
                        name="app.exe",
                        entry_type="file",
                    ),
                ),
            )
        if directory_path in {"/note.txt", "/Users/nested.txt", "/Program Files/app.exe"}:
            return self._result(
                volume,
                root_path=directory_path,
                status=FilesystemStatus("path_not_directory", "fake target is a file"),
                entries=(),
            )
        return self._result(
            volume,
            root_path=directory_path,
            status=FilesystemStatus("path_not_found", "fake path not found"),
            entries=(),
        )

    def _result(self, volume, *, root_path, entries, status=None):
        return FilesystemResult(
            schema_version="stage2.filesystem_adapter.v1",
            adapter_name=self.name,
            adapter_available=self.is_available,
            dependency=self.dependency_status(),
            source_path=volume.source_path,
            volume_id=volume.volume_id,
            volume_offset=volume.offset,
            volume_length=volume.length,
            filesystem_type="ntfs",
            read_only=True,
            status=status or FilesystemStatus("ok", "fake listing ok"),
            root_path=root_path,
            entries=entries,
        )

    def _entry(self, volume, *, file_id, path, name, entry_type):
        return FilesystemEntry(
            file_id=file_id,
            path=path,
            name=name,
            entry_type=entry_type,
            size=10 if entry_type == "file" else 0,
            allocated=True,
            deleted=False,
            source_path=volume.source_path,
            volume_id=volume.volume_id,
            volume_offset=volume.offset,
            volume_length=volume.length,
            filesystem_type="ntfs",
            adapter_name=self.name,
            read_only=True,
            status=FilesystemStatus("ok", "fake entry ok"),
            timestamps={
                "created": None,
                "modified": None,
                "accessed": None,
                "metadata_changed": None,
            },
        )


def _run_browser(commands: str, adapter=None):
    output = StringIO()
    session = DirectoryBrowserSession(
        volume=_sample_volume(),
        filesystem_adapter=adapter or FakeBrowserAdapter(),
        input_stream=StringIO(commands),
        output_stream=output,
        segment_count=2,
    )
    summary = session.run()
    return summary, output.getvalue()


def test_browser_accepts_core_commands_and_exits_cleanly():
    summary, output = _run_browser("pwd\nhelp\nls\ndir\nexit\n")

    assert summary["exit_code"] == 0
    assert summary["root_parser_backing"] == "real_parser_backed"
    assert summary["root_entry_count"] == 3
    assert "Current path: /" in output
    assert "Commands:" in output
    assert output.count("Status: ok parser_backing=real_parser_backed") >= 3
    assert "Source modified: false" in output


def test_browser_cd_child_directory_updates_current_path_only_after_ok():
    summary, output = _run_browser("cd Users\npwd\nquit\n")

    assert summary["exit_code"] == 0
    assert summary["current_path"] == "/Users"
    assert summary["last_status"] == "ok"
    assert summary["last_file_count"] == 1
    assert "Current path: /Users" in output


def test_browser_cd_parent_and_root_never_moves_above_root():
    summary, output = _run_browser("cd Users\ncd ..\ncd ..\ncd Users/Profile\ncd /\nroot\npwd\nexit\n")

    assert summary["exit_code"] == 0
    assert summary["current_path"] == "/"
    assert "Current path: /" in output
    assert "Path: /Users/Profile" in output


def test_browser_handles_quoted_names_with_spaces():
    summary, output = _run_browser('cd "Program Files"\npwd\nexit\n')

    assert summary["exit_code"] == 0
    assert summary["current_path"] == "/Program Files"
    assert summary["last_file_count"] == 1
    assert "Current path: /Program Files" in output


def test_browser_cd_file_reports_not_directory_and_keeps_current_path():
    summary, output = _run_browser("cd Users\ncd nested.txt\npwd\nexit\n")

    assert summary["exit_code"] == 0
    assert summary["current_path"] == "/Users"
    assert summary["last_status"] == "path_not_directory"
    assert "Cannot change directory: path_not_directory" in output
    assert "Current path: /Users" in output


def test_browser_missing_path_reports_not_found_without_crashing():
    summary, output = _run_browser("cd missing\npwd\nexit\n")

    assert summary["exit_code"] == 0
    assert summary["current_path"] == "/"
    assert summary["last_status"] == "path_not_found"
    assert "Cannot change directory: path_not_found" in output


def test_browser_dependency_unavailable_is_clean_blocked_status():
    output = StringIO()
    session = DirectoryBrowserSession(
        volume=_sample_volume(),
        filesystem_adapter=Pytsk3FilesystemAdapter(
            pytsk3_module=None,
            import_error=ImportError("No module named 'pytsk3'"),
        ),
        input_stream=StringIO("exit\n"),
        output_stream=output,
    )

    summary = session.run()

    assert summary["exit_code"] == 2
    assert summary["root_status"] == "filesystem_unavailable"
    assert "Browser blocked: root listing is unavailable." in output.getvalue()


def test_browser_does_not_create_artifacts_by_default():
    scratch = Path.cwd() / ".test-artifacts" / "directory-browser-no-artifacts"
    if scratch.exists():
        shutil.rmtree(scratch, ignore_errors=True)
    scratch.mkdir(parents=True)

    summary, _output = _run_browser("dir\nexit\n")

    assert summary["exit_code"] == 0
    assert list(scratch.iterdir()) == []
