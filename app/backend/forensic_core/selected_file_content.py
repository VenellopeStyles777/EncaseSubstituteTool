"""Selected-file content readers and providers for E01-backed parser bytes."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

from app.backend.forensic_core.content_analysis import AnalysisContent, AnalysisWarning
from app.backend.forensic_core.export_manifest import ExportWarning
from app.backend.forensic_core.filesystem_adapter import FilesystemEntry
from app.backend.forensic_core.image_stream import ImageByteStream
from app.backend.forensic_core.volume_discovery import VolumeInfo


SELECTED_FILE_CONTENT_SCHEMA_VERSION = "stage4_5.selected_file_content.v1"
DEFAULT_SELECTED_FILE_IN_MEMORY_LIMIT = 1024 * 1024
DEFAULT_SELECTED_FILE_PREVIEW_BYTES = 64

_AUTO_IMPORT = object()


@dataclass(frozen=True)
class SelectedFileContentStatus:
    """Structured status for selected-file content reads."""

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
class SelectedFileContentWarning:
    """Structured warning for selected-file content reads."""

    code: str
    message: str
    path: str | None = None
    source: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "code": self.code,
            "message": self.message,
            "path": self.path,
            "source": self.source,
        }


@dataclass(frozen=True)
class SelectedFileContentResult:
    """Result for a bounded or full parser-backed selected-file read."""

    status: SelectedFileContentStatus
    file_entry: Mapping[str, object]
    source_path: str | None
    volume_id: str | None
    volume_offset: int | None
    volume_length: int | None
    file_id: str | None
    file_path: str | None
    file_name: str | None
    entry_type: str | None
    filesystem_type: str | None
    adapter_name: str | None
    source_kind: str
    provider_name: str
    parser_name: str | None
    parser_version: str | None
    read_only: bool
    source_content_size: int | None
    requested_offset: int | None = None
    requested_length: int | None = None
    bytes_read: int = 0
    data: bytes = b""
    synthetic: bool = False
    warnings: tuple[SelectedFileContentWarning, ...] = field(default_factory=tuple)

    def to_dict(self, *, include_data: bool = False) -> dict[str, object]:
        result = {
            "schema_version": SELECTED_FILE_CONTENT_SCHEMA_VERSION,
            "status": self.status.to_dict(),
            "source_path": self.source_path,
            "volume_id": self.volume_id,
            "volume_offset": self.volume_offset,
            "volume_length": self.volume_length,
            "file_id": self.file_id,
            "file_path": self.file_path,
            "file_name": self.file_name,
            "entry_type": self.entry_type,
            "filesystem_type": self.filesystem_type,
            "adapter_name": self.adapter_name,
            "source_kind": self.source_kind,
            "provider_name": self.provider_name,
            "parser_name": self.parser_name,
            "parser_version": self.parser_version,
            "read_only": self.read_only,
            "source_content_size": self.source_content_size,
            "requested_offset": self.requested_offset,
            "requested_length": self.requested_length,
            "bytes_read": self.bytes_read,
            "synthetic": self.synthetic,
            "warnings": [warning.to_dict() for warning in self.warnings],
        }
        if include_data:
            result["data_hex"] = self.data.hex()
        return result


class E01SelectedFileContentReader:
    """Read parser-backed selected-file bytes from an EWF image stream."""

    provider_name = "e01-selected-file-content-reader"
    source_kind = "real_parser"
    parser_name = "pytsk3"
    read_only = True
    synthetic = False

    def __init__(
        self,
        image_stream: ImageByteStream,
        volume: VolumeInfo,
        file_entry: Mapping[str, object] | FilesystemEntry,
        *,
        pytsk3_module: object | None = _AUTO_IMPORT,
        import_error: BaseException | None = None,
    ) -> None:
        self._image_stream = image_stream
        self._volume = volume
        self._file_entry = _entry_mapping(file_entry)
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
    def file_entry(self) -> Mapping[str, object]:
        return self._file_entry

    @property
    def parser_version(self) -> str | None:
        return _optional_str(getattr(self._pytsk3, "__version__", None))

    def check(self) -> SelectedFileContentResult:
        """Validate selected-file provenance without reading content bytes."""

        status, warnings = self._preflight(full_read=False)
        return self._result(
            status=status,
            requested_offset=None,
            requested_length=None,
            data=b"",
            warnings=warnings,
        )

    def read_range(self, offset: int, length: int) -> SelectedFileContentResult:
        """Read a bounded selected-file range."""

        if offset < 0 or length < 0:
            return self._result(
                status=SelectedFileContentStatus(
                    code="invalid_range",
                    message="Selected-file read offset and length must be non-negative.",
                ),
                requested_offset=offset,
                requested_length=length,
                data=b"",
                warnings=(
                    SelectedFileContentWarning(
                        code="invalid_range",
                        message="Selected-file read offset and length must be non-negative.",
                        path=_entry_path(self._file_entry),
                        source="selected_file_content_reader",
                    ),
                ),
            )

        status, warnings = self._preflight(full_read=False)
        if not status.ok:
            return self._result(
                status=status,
                requested_offset=offset,
                requested_length=length,
                data=b"",
                warnings=warnings,
            )

        source_size = _entry_size(self._file_entry)
        if source_size is None:
            status = SelectedFileContentStatus(
                code="content_source_unavailable",
                message="Selected-file size is unavailable; content was not read.",
            )
            return self._result(
                status=status,
                requested_offset=offset,
                requested_length=length,
                data=b"",
                warnings=warnings
                + (
                    SelectedFileContentWarning(
                        code="content_source_unavailable",
                        message="Selected-file size is unavailable.",
                        path=_entry_path(self._file_entry),
                        source="selected_file_content_reader",
                    ),
                ),
            )

        if offset > source_size:
            status = SelectedFileContentStatus(
                code="content_source_unavailable",
                message="Selected-file read offset is beyond the file size.",
            )
            return self._result(
                status=status,
                requested_offset=offset,
                requested_length=length,
                data=b"",
                warnings=warnings
                + (
                    SelectedFileContentWarning(
                        code="content_source_unavailable",
                        message="Selected-file read offset is beyond the file size.",
                        path=_entry_path(self._file_entry),
                        source="selected_file_content_reader",
                    ),
                ),
            )

        read_length = min(length, max(0, source_size - offset))
        try:
            data = self._read_from_parser(offset, read_length)
        except Exception:
            status = SelectedFileContentStatus(
                code="file_content_unreadable",
                message="Parser could not read selected-file content.",
            )
            return self._result(
                status=status,
                requested_offset=offset,
                requested_length=length,
                data=b"",
                warnings=warnings
                + (
                    SelectedFileContentWarning(
                        code="parser_content_unreadable",
                        message="Parser could not read selected-file content.",
                        path=_entry_path(self._file_entry),
                        source="selected_file_content_reader",
                    ),
                ),
            )

        status = SelectedFileContentStatus(
            code="ok",
            message="Selected-file content range was read from the real parser.",
        )
        read_warnings = warnings
        if len(data) != read_length:
            status = SelectedFileContentStatus(
                code="file_content_partial",
                message="Parser returned fewer bytes than requested.",
            )
            read_warnings = read_warnings + (
                SelectedFileContentWarning(
                    code="parser_content_partial",
                    message="Parser returned fewer bytes than requested.",
                    path=_entry_path(self._file_entry),
                    source="selected_file_content_reader",
                ),
            )

        return self._result(
            status=status,
            requested_offset=offset,
            requested_length=length,
            data=data,
            warnings=read_warnings,
        )

    def read_full(self, *, max_bytes: int) -> SelectedFileContentResult:
        """Read complete selected-file bytes under an explicit in-memory limit."""

        status, warnings = self._preflight(full_read=True, max_bytes=max_bytes)
        if not status.ok:
            return self._result(
                status=status,
                requested_offset=0,
                requested_length=None,
                data=b"",
                warnings=warnings,
            )

        source_size = _entry_size(self._file_entry)
        if source_size is None:
            status = SelectedFileContentStatus(
                code="content_source_unavailable",
                message="Selected-file size is unavailable; full content was not read.",
            )
            return self._result(
                status=status,
                requested_offset=0,
                requested_length=None,
                data=b"",
                warnings=warnings,
            )

        return self.read_range(0, source_size)

    def _preflight(
        self,
        *,
        full_read: bool,
        max_bytes: int | None = None,
    ) -> tuple[SelectedFileContentStatus, tuple[SelectedFileContentWarning, ...]]:
        path = _entry_path(self._file_entry)
        warnings: list[SelectedFileContentWarning] = []

        if self._pytsk3 is None:
            message = "pytsk3/The Sleuth Kit dependency is unavailable; selected-file content was not read."
            if self._import_error is not None:
                message = f"{message} Import error: {self._import_error}"
            return (
                SelectedFileContentStatus(
                    code="content_source_unavailable",
                    message=message,
                ),
                (
                    SelectedFileContentWarning(
                        code="dependency_unavailable",
                        message="pytsk3 is unavailable for selected-file content reads.",
                        path=path,
                        source="selected_file_content_reader",
                    ),
                ),
            )

        adapter_name = _optional_str(self._file_entry.get("adapter_name"))
        if adapter_name != "pytsk3-filesystem-adapter":
            return (
                SelectedFileContentStatus(
                    code="metadata_only_source",
                    message="Selected entry is not from the parser-backed E01 filesystem adapter.",
                ),
                (
                    SelectedFileContentWarning(
                        code="metadata_only_source",
                        message="Selected entry is metadata-only for this content reader.",
                        path=path,
                        source="selected_file_content_reader",
                    ),
                ),
            )

        if _optional_str(self._file_entry.get("entry_type")) != "file":
            return (
                SelectedFileContentStatus(
                    code="path_not_file",
                    message="Selected-file content requires a regular file entry.",
                ),
                (
                    SelectedFileContentWarning(
                        code="path_not_file",
                        message="Directory or special entries cannot be read as selected-file content.",
                        path=path,
                        source="selected_file_content_reader",
                    ),
                ),
            )

        if _optional_bool(self._file_entry.get("deleted")) is True:
            return (
                SelectedFileContentStatus(
                    code="deleted_recovery_unsupported",
                    message="Deleted-entry recovery is out of scope for selected-file content.",
                ),
                (
                    SelectedFileContentWarning(
                        code="deleted_recovery_deferred",
                        message="Deleted-entry content recovery is deferred.",
                        path=path,
                        source="selected_file_content_reader",
                    ),
                ),
            )

        if _optional_bool(self._file_entry.get("allocated")) is False:
            return (
                SelectedFileContentStatus(
                    code="deleted_entry_metadata_only",
                    message="Unallocated/deleted entry metadata is available, but content is not.",
                ),
                (
                    SelectedFileContentWarning(
                        code="deleted_entry_metadata_only",
                        message="Unallocated/deleted entry content was not read.",
                        path=path,
                        source="selected_file_content_reader",
                    ),
                ),
            )

        source_size = _entry_size(self._file_entry)
        if full_read and source_size is not None and max_bytes is not None and source_size > max_bytes:
            return (
                SelectedFileContentStatus(
                    code="file_too_large_for_in_memory_provider",
                    message="Selected file exceeds the in-memory first-testing limit.",
                ),
                (
                    SelectedFileContentWarning(
                        code="large_file_refused",
                        message="Selected file exceeds the in-memory first-testing limit.",
                        path=path,
                        source="selected_file_content_reader",
                    ),
                ),
            )

        warnings.append(
            SelectedFileContentWarning(
                code="real_parser_content",
                message="Selected-file bytes are read through the parser-backed E01 path.",
                path=path,
                source="selected_file_content_reader",
            )
        )
        warnings.append(
            SelectedFileContentWarning(
                code="read_only_content_source",
                message="Selected-file content source is read-only.",
                path=path,
                source="selected_file_content_reader",
            )
        )
        return (
            SelectedFileContentStatus(
                code="ok",
                message="Selected-file content source is available.",
            ),
            tuple(warnings),
        )

    def _read_from_parser(self, offset: int, length: int) -> bytes:
        image_info = _Pytsk3ImageInfo(self._image_stream, self._pytsk3)
        file_object = None
        try:
            filesystem = self._pytsk3.FS_Info(image_info, offset=self._volume.offset)
            file_object = _open_file(filesystem, self._file_entry)
            read_random = getattr(file_object, "read_random", None)
            if not callable(read_random):
                raise RuntimeError("pytsk3 file object does not expose read_random()")
            return bytes(read_random(offset, length))
        finally:
            close = getattr(file_object, "close", None)
            if callable(close):
                close()
            image_info.close()

    def _result(
        self,
        *,
        status: SelectedFileContentStatus,
        requested_offset: int | None,
        requested_length: int | None,
        data: bytes,
        warnings: tuple[SelectedFileContentWarning, ...],
    ) -> SelectedFileContentResult:
        return SelectedFileContentResult(
            status=status,
            file_entry=self._file_entry,
            source_path=_optional_str(self._file_entry.get("source_path")),
            volume_id=_optional_str(self._file_entry.get("volume_id")),
            volume_offset=_optional_int(self._file_entry.get("volume_offset")),
            volume_length=_optional_int(self._file_entry.get("volume_length")),
            file_id=_optional_str(self._file_entry.get("file_id")),
            file_path=_entry_path(self._file_entry),
            file_name=_optional_str(self._file_entry.get("name")),
            entry_type=_optional_str(self._file_entry.get("entry_type")),
            filesystem_type=_optional_str(self._file_entry.get("filesystem_type")),
            adapter_name=_optional_str(self._file_entry.get("adapter_name")),
            source_kind=self.source_kind if status.ok else "metadata_only",
            provider_name=self.provider_name,
            parser_name=self.parser_name if status.ok else None,
            parser_version=self.parser_version if status.ok else None,
            read_only=self.read_only and bool(self._file_entry.get("read_only", False)),
            source_content_size=_entry_size(self._file_entry),
            requested_offset=requested_offset,
            requested_length=requested_length,
            bytes_read=len(data),
            data=data,
            synthetic=False,
            warnings=warnings,
        )


class E01PreviewContentProvider:
    """Preview provider backed by bounded selected-file parser reads."""

    name = "e01-preview-content-provider"
    read_only = True

    def __init__(
        self,
        reader: E01SelectedFileContentReader,
        *,
        max_preview_bytes: int = DEFAULT_SELECTED_FILE_PREVIEW_BYTES,
    ) -> None:
        self._reader = reader
        self._max_preview_bytes = max_preview_bytes
        self.last_result: SelectedFileContentResult | None = None

    def get_content(self, file_entry: Mapping[str, object]):
        from app.backend.api.file_preview import PreviewContent

        source_size = _entry_size(file_entry) or 0
        length = min(max(source_size, 0), self._max_preview_bytes)
        self.last_result = self._reader.read_range(0, length)
        if not self.last_result.status.ok:
            return None

        return PreviewContent(
            data=self.last_result.data,
            provider_name=self.name,
            source_path=self.last_result.source_path,
            read_only=self.read_only and self.last_result.read_only,
            warnings=tuple(
                _preview_warning(warning) for warning in self.last_result.warnings
            ),
        )


class E01ExportContentProvider:
    """Export provider backed by complete selected-file parser reads."""

    name = "e01-export-content-provider"
    source_kind = "real_parser"
    read_only = True
    synthetic = False

    def __init__(
        self,
        reader: E01SelectedFileContentReader,
        *,
        max_bytes: int = DEFAULT_SELECTED_FILE_IN_MEMORY_LIMIT,
    ) -> None:
        self._reader = reader
        self._max_bytes = max_bytes
        self.last_result: SelectedFileContentResult | None = None

    def get_content(self, source):
        from app.backend.api.file_export import ExportContent

        self.last_result = self._reader.read_full(max_bytes=self._max_bytes)
        if not self.last_result.status.ok:
            return None

        return ExportContent(
            data=self.last_result.data,
            provider_name=self.name,
            source_kind=self.source_kind,
            read_only=self.read_only and self.last_result.read_only,
            synthetic=False,
            parser_name=self.last_result.parser_name,
            parser_version=self.last_result.parser_version,
            warnings=tuple(
                _export_warning(warning) for warning in self.last_result.warnings
            ),
        )


class E01AnalysisContentProvider:
    """Analysis provider backed by selected-file parser reads."""

    name = "e01-analysis-content-provider"
    source_kind = "real_parser"
    read_only = True
    synthetic = False
    generated = False

    def __init__(
        self,
        reader: E01SelectedFileContentReader,
        *,
        read_mode: str = "full",
        max_bytes: int = DEFAULT_SELECTED_FILE_IN_MEMORY_LIMIT,
    ) -> None:
        self._reader = reader
        self._read_mode = read_mode
        self._max_bytes = max_bytes
        self.last_result: SelectedFileContentResult | None = None

    def get_content(self, source) -> AnalysisContent | None:
        if self._read_mode == "bounded":
            source_size = _entry_size(self._reader.file_entry) or 0
            self.last_result = self._reader.read_range(0, min(source_size, self._max_bytes))
        else:
            self.last_result = self._reader.read_full(max_bytes=self._max_bytes)

        if not self.last_result.status.ok:
            return None

        return AnalysisContent(
            data=self.last_result.data,
            provider_name=self.name,
            source_kind=self.source_kind,
            read_only=self.read_only and self.last_result.read_only,
            synthetic=False,
            generated=False,
            parser_name=self.last_result.parser_name,
            parser_version=self.last_result.parser_version,
            warnings=tuple(
                _analysis_warning(warning) for warning in self.last_result.warnings
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


def _open_file(filesystem: object, file_entry: Mapping[str, object]) -> object:
    identifier = _file_identifier(file_entry)
    open_meta = getattr(filesystem, "open_meta", None)
    if identifier is not None and callable(open_meta):
        try:
            return open_meta(inode=identifier)
        except TypeError:
            return open_meta(identifier)

    path = _entry_path(file_entry)
    if path:
        open_path = getattr(filesystem, "open", None)
        if callable(open_path):
            try:
                return open_path(path=path)
            except TypeError:
                return open_path(path)

    raise RuntimeError("No stable parser file handle could be opened for the selected entry")


def _file_identifier(file_entry: Mapping[str, object]) -> int | None:
    file_id = _optional_str(file_entry.get("file_id"))
    if not file_id or ":" not in file_id:
        return None
    _, suffix = file_id.split(":", 1)
    try:
        return int(suffix)
    except ValueError:
        return None


def _entry_mapping(file_entry: Mapping[str, object] | FilesystemEntry) -> Mapping[str, object]:
    if isinstance(file_entry, FilesystemEntry):
        return file_entry.to_dict()
    return dict(file_entry)


def _entry_size(file_entry: Mapping[str, object]) -> int | None:
    return _optional_int(file_entry.get("size"))


def _entry_path(file_entry: Mapping[str, object]) -> str | None:
    return _optional_str(file_entry.get("path"))


def _optional_str(value: object) -> str | None:
    if value is None:
        return None
    text = str(value)
    return text if text else None


def _optional_int(value: object) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _optional_bool(value: object) -> bool | None:
    if value is None:
        return None
    return bool(value)


def _preview_warning(warning: SelectedFileContentWarning):
    from app.backend.api.file_preview import PreviewWarning

    return PreviewWarning(
        code=warning.code,
        message=warning.message,
        path=warning.path,
    )


def _export_warning(warning: SelectedFileContentWarning) -> ExportWarning:
    return ExportWarning(
        code=warning.code,
        message=warning.message,
        path=warning.path,
        source=warning.source,
    )


def _analysis_warning(warning: SelectedFileContentWarning) -> AnalysisWarning:
    return AnalysisWarning(
        code=warning.code,
        message=warning.message,
        path=warning.path,
        source=warning.source,
    )
