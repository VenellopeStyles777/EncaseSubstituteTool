"""Filesystem adapter boundary for Stage 2."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from app.backend.forensic_core.volume_discovery import VolumeInfo


FILESYSTEM_ADAPTER_SCHEMA_VERSION = "stage2.filesystem_adapter.v1"


@dataclass(frozen=True)
class FilesystemDependencyStatus:
    """Structured dependency status for filesystem adapters."""

    name: str
    available: bool
    message: str
    version: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "available": self.available,
            "message": self.message,
            "version": self.version,
        }


@dataclass(frozen=True)
class FilesystemStatus:
    """Structured status for filesystem adapter operations."""

    code: str
    message: str

    @property
    def ok(self) -> bool:
        return self.code == "ok"

    def to_dict(self) -> dict[str, object]:
        return {
            "code": self.code,
            "ok": self.ok,
            "message": self.message,
        }


@dataclass(frozen=True)
class FilesystemWarning:
    """Structured non-fatal filesystem adapter warning."""

    code: str
    message: str
    path: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "code": self.code,
            "message": self.message,
            "path": self.path,
        }


@dataclass(frozen=True)
class FilesystemEntry:
    """File or directory metadata shape for later listing workflows."""

    file_id: str
    path: str
    name: str
    entry_type: str
    size: int | None
    allocated: bool | None
    deleted: bool | None
    source_path: str
    volume_id: str
    volume_offset: int
    volume_length: int
    filesystem_type: str
    adapter_name: str
    read_only: bool
    status: FilesystemStatus
    warnings: tuple[FilesystemWarning, ...] = field(default_factory=tuple)
    timestamps: dict[str, str | None] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return {
            "file_id": self.file_id,
            "path": self.path,
            "name": self.name,
            "entry_type": self.entry_type,
            "size": self.size,
            "allocated": self.allocated,
            "deleted": self.deleted,
            "source_path": self.source_path,
            "volume_id": self.volume_id,
            "volume_offset": self.volume_offset,
            "volume_length": self.volume_length,
            "filesystem_type": self.filesystem_type,
            "adapter_name": self.adapter_name,
            "read_only": self.read_only,
            "status": self.status.to_dict(),
            "warnings": [warning.to_dict() for warning in self.warnings],
            "timestamps": dict(self.timestamps),
        }


@dataclass(frozen=True)
class FilesystemResult:
    """JSON-friendly filesystem adapter result for one volume."""

    schema_version: str
    adapter_name: str
    adapter_available: bool
    dependency: FilesystemDependencyStatus
    source_path: str
    volume_id: str
    volume_offset: int
    volume_length: int
    filesystem_type: str
    read_only: bool
    status: FilesystemStatus
    root_path: str
    entries: tuple[FilesystemEntry, ...] = field(default_factory=tuple)
    warnings: tuple[FilesystemWarning, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "adapter_name": self.adapter_name,
            "adapter_available": self.adapter_available,
            "dependency": self.dependency.to_dict(),
            "source_path": self.source_path,
            "volume_id": self.volume_id,
            "volume_offset": self.volume_offset,
            "volume_length": self.volume_length,
            "filesystem_type": self.filesystem_type,
            "read_only": self.read_only,
            "status": self.status.to_dict(),
            "root_path": self.root_path,
            "entries": [entry.to_dict() for entry in self.entries],
            "warnings": [warning.to_dict() for warning in self.warnings],
        }


class FilesystemAdapter(Protocol):
    """Protocol for read-only filesystem metadata adapters."""

    name: str
    read_only: bool

    @property
    def is_available(self) -> bool:
        """Whether the adapter can parse real filesystems in this environment."""

    def dependency_status(self) -> FilesystemDependencyStatus:
        """Return structured dependency availability information."""

    def inspect_volume(self, volume: VolumeInfo) -> FilesystemResult:
        """Return filesystem metadata and root entries for a volume."""


class StubFilesystemAdapter:
    """Dependency-free deterministic filesystem adapter for tests."""

    name = "stub-filesystem-adapter"
    read_only = True
    filesystem_type = "stubfs"

    @property
    def is_available(self) -> bool:
        return True

    def dependency_status(self) -> FilesystemDependencyStatus:
        return FilesystemDependencyStatus(
            name="stub",
            available=True,
            message="Stub filesystem adapter is available for dependency-free tests.",
        )

    def inspect_volume(self, volume: VolumeInfo) -> FilesystemResult:
        status = FilesystemStatus(
            code="ok",
            message="Stub filesystem root entries returned.",
        )
        entries = (
            self._entry(
                volume,
                file_id="stub-dir-documents",
                path="/Documents",
                name="Documents",
                entry_type="directory",
                size=0,
                status=status,
            ),
            self._entry(
                volume,
                file_id="stub-file-hello",
                path="/hello.txt",
                name="hello.txt",
                entry_type="file",
                size=13,
                status=status,
            ),
        )

        return FilesystemResult(
            schema_version=FILESYSTEM_ADAPTER_SCHEMA_VERSION,
            adapter_name=self.name,
            adapter_available=self.is_available,
            dependency=self.dependency_status(),
            source_path=volume.source_path,
            volume_id=volume.volume_id,
            volume_offset=volume.offset,
            volume_length=volume.length,
            filesystem_type=self.filesystem_type,
            read_only=self.read_only and volume.read_only,
            status=status,
            root_path="/",
            entries=entries,
            warnings=(
                FilesystemWarning(
                    code="stub_filesystem",
                    message="Stub filesystem entries are synthetic and not parsed from evidence.",
                ),
            ),
        )

    def _entry(
        self,
        volume: VolumeInfo,
        *,
        file_id: str,
        path: str,
        name: str,
        entry_type: str,
        size: int,
        status: FilesystemStatus,
    ) -> FilesystemEntry:
        return FilesystemEntry(
            file_id=file_id,
            path=path,
            name=name,
            entry_type=entry_type,
            size=size,
            allocated=True,
            deleted=False,
            source_path=volume.source_path,
            volume_id=volume.volume_id,
            volume_offset=volume.offset,
            volume_length=volume.length,
            filesystem_type=self.filesystem_type,
            adapter_name=self.name,
            read_only=self.read_only and volume.read_only,
            status=status,
            timestamps={
                "created": None,
                "modified": None,
                "accessed": None,
                "metadata_changed": None,
            },
        )


_AUTO_IMPORT = object()


class Pytsk3FilesystemAdapter:
    """Optional pytsk3 adapter skeleton with graceful dependency handling."""

    name = "pytsk3-filesystem-adapter"
    read_only = True

    def __init__(
        self,
        pytsk3_module: object | None = _AUTO_IMPORT,
        import_error: BaseException | None = None,
    ) -> None:
        if pytsk3_module is _AUTO_IMPORT:
            try:
                import pytsk3  # type: ignore[import-not-found]
            except ImportError as error:
                self._pytsk3 = None
                self._import_error = error
            else:
                self._pytsk3 = pytsk3
                self._import_error = None
        else:
            self._pytsk3 = pytsk3_module
            self._import_error = import_error

    @property
    def is_available(self) -> bool:
        return self._pytsk3 is not None

    def dependency_status(self) -> FilesystemDependencyStatus:
        if not self.is_available:
            message = "pytsk3 is not installed; real filesystem parsing is unavailable."
            if self._import_error is not None:
                message = f"{message} Import error: {self._import_error}"
            return FilesystemDependencyStatus(
                name="pytsk3",
                available=False,
                message=message,
            )

        return FilesystemDependencyStatus(
            name="pytsk3",
            available=True,
            message="pytsk3 is available; real filesystem parsing is not implemented in S2-T04.",
            version=getattr(self._pytsk3, "__version__", None),
        )

    def inspect_volume(self, volume: VolumeInfo) -> FilesystemResult:
        dependency = self.dependency_status()
        if not dependency.available:
            return FilesystemResult(
                schema_version=FILESYSTEM_ADAPTER_SCHEMA_VERSION,
                adapter_name=self.name,
                adapter_available=False,
                dependency=dependency,
                source_path=volume.source_path,
                volume_id=volume.volume_id,
                volume_offset=volume.offset,
                volume_length=volume.length,
                filesystem_type="unknown",
                read_only=self.read_only and volume.read_only,
                status=FilesystemStatus(
                    code="dependency_unavailable",
                    message="pytsk3/The Sleuth Kit dependency is unavailable; filesystem was not parsed.",
                ),
                root_path="/",
                warnings=(
                    FilesystemWarning(
                        code="dependency_unavailable",
                        message="pytsk3 is unavailable; returning no filesystem entries.",
                    ),
                ),
            )

        return FilesystemResult(
            schema_version=FILESYSTEM_ADAPTER_SCHEMA_VERSION,
            adapter_name=self.name,
            adapter_available=True,
            dependency=dependency,
            source_path=volume.source_path,
            volume_id=volume.volume_id,
            volume_offset=volume.offset,
            volume_length=volume.length,
            filesystem_type="unknown",
            read_only=self.read_only and volume.read_only,
            status=FilesystemStatus(
                code="real_parser_not_implemented",
                message="pytsk3 is importable, but real filesystem parsing is deferred beyond S2-T04.",
            ),
            root_path="/",
            warnings=(
                FilesystemWarning(
                    code="real_parser_not_implemented",
                    message="pytsk3 adapter skeleton did not parse filesystem entries.",
                ),
            ),
        )
