"""Filesystem adapter boundary for Stage 2."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Protocol

from app.backend.forensic_core.image_stream import ImageByteStream
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

    def list_directory(self, volume: VolumeInfo, directory_path: str) -> FilesystemResult:
        """Return direct child metadata for one directory path."""


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
        image_stream: ImageByteStream | None = None,
    ) -> None:
        self._image_stream = image_stream
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
        return self._inspect_directory(volume, directory_path="/")

    def list_directory(self, volume: VolumeInfo, directory_path: str) -> FilesystemResult:
        return self._inspect_directory(volume, directory_path=directory_path)

    def _inspect_directory(
        self,
        volume: VolumeInfo,
        *,
        directory_path: str,
    ) -> FilesystemResult:
        normalized_directory_path = _normalize_filesystem_path(directory_path)
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
                root_path=normalized_directory_path,
                warnings=(
                    FilesystemWarning(
                        code="dependency_unavailable",
                        message="pytsk3 is unavailable; returning no filesystem entries.",
                    ),
                ),
            )

        if self._image_stream is None:
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
                    message="pytsk3 is importable, but no image stream was supplied for filesystem parsing.",
                ),
                root_path=normalized_directory_path,
                warnings=(
                    FilesystemWarning(
                        code="real_parser_not_implemented",
                        message="pytsk3 adapter could not parse without an image stream.",
                    ),
                ),
            )

        image_info = _Pytsk3ImageInfo(self._image_stream, self._pytsk3)
        filesystem = None
        try:
            try:
                filesystem = self._pytsk3.FS_Info(image_info, offset=volume.offset)
                directory = filesystem.open_dir(path=normalized_directory_path)
                entries = tuple(
                    entry
                    for entry in (
                        _filesystem_entry(
                            self._pytsk3,
                            filesystem,
                            volume,
                            raw_entry,
                            parent_path=normalized_directory_path,
                        )
                        for raw_entry in directory
                    )
                    if entry is not None
                )
            except Exception as error:
                if normalized_directory_path == "/":
                    status_code = "filesystem_parse_error"
                    warning_message = "pytsk3 could not parse filesystem root entries."
                elif filesystem is not None and _path_exists_as_non_directory(
                    self._pytsk3,
                    filesystem,
                    normalized_directory_path,
                ):
                    status_code = "path_not_directory"
                    warning_message = "pytsk3 found the requested path, but it is not a directory."
                else:
                    status_code = "path_not_found"
                    warning_message = "pytsk3 could not open the requested directory."
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
                        code=status_code,
                        message=f"{warning_message} {error}",
                    ),
                    root_path=normalized_directory_path,
                    warnings=(
                        FilesystemWarning(
                            code=status_code,
                            message=warning_message,
                            path=normalized_directory_path,
                        ),
                    ),
                )
        finally:
            image_info.close()

        filesystem_type = _filesystem_type(self._pytsk3, filesystem)
        message = (
            "pytsk3 parsed root filesystem entries."
            if normalized_directory_path == "/"
            else "pytsk3 parsed requested directory entries."
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
            filesystem_type=filesystem_type,
            read_only=self.read_only and volume.read_only,
            status=FilesystemStatus(
                code="ok",
                message=message,
            ),
            root_path=normalized_directory_path,
            entries=entries,
            warnings=(
                FilesystemWarning(
                    code="real_parser_backed",
                    message="Directory entries were parsed from the supplied image stream with pytsk3.",
                    path=normalized_directory_path,
                ),
            ),
        )


class _Pytsk3ImageInfo:
    def __new__(cls, image_stream: ImageByteStream, pytsk3_module: object):
        base = getattr(pytsk3_module, "Img_Info")

        class ImageInfo(base):
            def __init__(self, stream: ImageByteStream, module: object) -> None:
                self._image_stream = stream
                self._native_handle = _open_native_handle(stream)
                image_type = getattr(module, "TSK_IMG_TYPE_EXTERNAL", 0)
                super().__init__(url="", type=image_type)

            def close(self) -> None:
                handle = getattr(self, "_native_handle", None)
                if handle is not None:
                    close = getattr(handle, "close", None)
                    if callable(close):
                        close()
                    self._native_handle = None

            def read(self, offset: int, size: int) -> bytes:
                handle = getattr(self, "_native_handle", None)
                if handle is not None:
                    read_at = getattr(handle, "read_buffer_at_offset", None)
                    if callable(read_at):
                        return read_at(size, offset)

                result = self._image_stream.read_at(offset, size)
                if not result.status.ok:
                    return b""
                return result.data

            def get_size(self) -> int:
                info = self._image_stream.describe()
                return int(info.size or 0)

        return ImageInfo(image_stream, pytsk3_module)


def _open_native_handle(image_stream: ImageByteStream) -> object | None:
    open_handle = getattr(image_stream, "_open_native_handle", None)
    if callable(open_handle):
        return open_handle()
    return None


def _path_exists_as_non_directory(
    pytsk3_module: object,
    filesystem: object,
    path: str,
) -> bool:
    open_path = getattr(filesystem, "open", None)
    if not callable(open_path):
        return False
    try:
        raw_entry = open_path(path=path)
    except TypeError:
        try:
            raw_entry = open_path(path)
        except Exception:
            return False
    except Exception:
        return False

    info = getattr(raw_entry, "info", None)
    meta = getattr(info, "meta", None)
    return _entry_type(pytsk3_module, meta) != "directory"


def _filesystem_entry(
    pytsk3_module: object,
    filesystem: object,
    volume: VolumeInfo,
    raw_entry: object,
    *,
    parent_path: str = "/",
) -> FilesystemEntry | None:
    info = getattr(raw_entry, "info", None)
    name_info = getattr(info, "name", None)
    raw_name = getattr(name_info, "name", None)
    name = _decode_name(raw_name)
    if name in {"", ".", ".."}:
        return None

    meta = getattr(info, "meta", None)
    entry_type = _entry_type(pytsk3_module, meta)
    size = getattr(meta, "size", None) if meta is not None else None
    name_flags = int(getattr(name_info, "flags", 0) or 0)
    unallocated_flag = int(getattr(pytsk3_module, "TSK_FS_NAME_FLAG_UNALLOC", 0) or 0)
    allocated_flag = int(getattr(pytsk3_module, "TSK_FS_NAME_FLAG_ALLOC", 0) or 0)
    deleted = bool(name_flags & unallocated_flag) if unallocated_flag else None
    allocated = bool(name_flags & allocated_flag) if allocated_flag else None
    if deleted is not None and allocated is None:
        allocated = not deleted

    path = _join_filesystem_path(parent_path, name)
    file_id = _file_id(volume, meta, name_info, path)
    status = FilesystemStatus(
        code="ok",
        message="Parser-backed root entry.",
    )
    return FilesystemEntry(
        file_id=file_id,
        path=path,
        name=name,
        entry_type=entry_type,
        size=int(size) if size is not None else None,
        allocated=allocated,
        deleted=deleted,
        source_path=volume.source_path,
        volume_id=volume.volume_id,
        volume_offset=volume.offset,
        volume_length=volume.length,
        filesystem_type=_filesystem_type(pytsk3_module, filesystem),
        adapter_name=Pytsk3FilesystemAdapter.name,
        read_only=volume.read_only,
        status=status,
        timestamps=_timestamps(meta),
    )


def _normalize_filesystem_path(value: str | None) -> str:
    text = (value or "/").strip().replace("\\", "/")
    if not text:
        return "/"
    if not text.startswith("/"):
        text = f"/{text}"
    while "//" in text:
        text = text.replace("//", "/")
    return text.rstrip("/") if len(text) > 1 else text


def _join_filesystem_path(parent_path: str, name: str) -> str:
    parent = _normalize_filesystem_path(parent_path)
    if parent == "/":
        return f"/{name}".replace("//", "/")
    return f"{parent}/{name}".replace("//", "/")


def _decode_name(value: object) -> str:
    if isinstance(value, bytes):
        return value.decode("utf-8", "replace")
    if value is None:
        return ""
    return str(value)


def _entry_type(pytsk3_module: object, meta: object | None) -> str:
    meta_type = getattr(meta, "type", None) if meta is not None else None
    if meta_type == getattr(pytsk3_module, "TSK_FS_META_TYPE_DIR", object()):
        return "directory"
    if meta_type == getattr(pytsk3_module, "TSK_FS_META_TYPE_REG", object()):
        return "file"
    if meta_type == getattr(pytsk3_module, "TSK_FS_META_TYPE_LNK", object()):
        return "symlink"
    if meta_type is None:
        return "unknown"
    return "special"


def _file_id(
    volume: VolumeInfo,
    meta: object | None,
    name_info: object | None,
    path: str,
) -> str:
    meta_addr = getattr(meta, "addr", None) if meta is not None else None
    name_meta_addr = getattr(name_info, "meta_addr", None) if name_info is not None else None
    identifier = meta_addr if meta_addr is not None else name_meta_addr
    if identifier is None:
        identifier = path
    return f"{volume.volume_id}:{identifier}"


def _filesystem_type(pytsk3_module: object, filesystem: object) -> str:
    info = getattr(filesystem, "info", None)
    ftype = getattr(info, "ftype", None)
    if ftype is None:
        return "unknown"
    for name in dir(pytsk3_module):
        if name.startswith("TSK_FS_TYPE_") and getattr(pytsk3_module, name) == ftype:
            return name.removeprefix("TSK_FS_TYPE_").lower()
    return f"pytsk3_type_{ftype}"


def _timestamps(meta: object | None) -> dict[str, str | None]:
    return {
        "created": _timestamp(getattr(meta, "crtime", None) if meta is not None else None),
        "modified": _timestamp(getattr(meta, "mtime", None) if meta is not None else None),
        "accessed": _timestamp(getattr(meta, "atime", None) if meta is not None else None),
        "metadata_changed": _timestamp(getattr(meta, "ctime", None) if meta is not None else None),
    }


def _timestamp(value: object) -> str | None:
    if value in {None, 0}:
        return None
    try:
        return datetime.fromtimestamp(int(value), timezone.utc).isoformat().replace("+00:00", "Z")
    except (OSError, OverflowError, ValueError, TypeError):
        return None
