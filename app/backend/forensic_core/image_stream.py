"""Read-only image byte-stream abstractions for Stage 2."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol, Sequence

from app.backend.forensic_core.segment_discovery import discover_e01_segments


@dataclass(frozen=True)
class ImageStreamStatus:
    """Structured status for image stream operations."""

    code: str
    message: str
    path: str | None = None

    @property
    def ok(self) -> bool:
        return self.code == "ok"

    def to_dict(self) -> dict[str, object]:
        return {
            "code": self.code,
            "ok": self.ok,
            "message": self.message,
            "path": self.path,
        }


@dataclass(frozen=True)
class ImageStreamWarning:
    """Structured non-fatal warning for image stream operations."""

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
class ImageStreamInfo:
    """Metadata and provenance for a read-only image stream."""

    source_path: str
    stream_type: str
    size: int | None
    read_only: bool
    status: ImageStreamStatus
    warnings: tuple[ImageStreamWarning, ...] = field(default_factory=tuple)

    @property
    def is_readable(self) -> bool:
        return self.status.ok and self.size is not None

    def to_dict(self) -> dict[str, object]:
        return {
            "source_path": self.source_path,
            "stream_type": self.stream_type,
            "size": self.size,
            "read_only": self.read_only,
            "status": self.status.to_dict(),
            "warnings": [warning.to_dict() for warning in self.warnings],
        }


@dataclass(frozen=True)
class ImageReadResult:
    """Result of a bounded byte-range read."""

    source_path: str
    stream_type: str
    read_only: bool
    offset: int
    length: int
    source_size: int | None
    data: bytes
    status: ImageStreamStatus
    warnings: tuple[ImageStreamWarning, ...] = field(default_factory=tuple)

    @property
    def bytes_read(self) -> int:
        return len(self.data)

    def to_dict(self) -> dict[str, object]:
        return {
            "source_path": self.source_path,
            "stream_type": self.stream_type,
            "read_only": self.read_only,
            "offset": self.offset,
            "length": self.length,
            "source_size": self.source_size,
            "bytes_read": self.bytes_read,
            "status": self.status.to_dict(),
            "warnings": [warning.to_dict() for warning in self.warnings],
        }


class ImageByteStream(Protocol):
    """Protocol for bounded, read-only image byte access."""

    stream_type: str
    read_only: bool

    def describe(self) -> ImageStreamInfo:
        """Return stream metadata and availability without modifying the source."""

    def read_at(self, offset: int, length: int) -> ImageReadResult:
        """Read up to length bytes starting at offset."""


class LocalFileImageStream:
    """Read-only image stream backed by a local file."""

    stream_type = "local-file"
    read_only = True

    def __init__(self, source_path: str | Path) -> None:
        self._path = Path(source_path).expanduser().resolve(strict=False)

    @property
    def source_path(self) -> str:
        return str(self._path)

    def describe(self) -> ImageStreamInfo:
        status = self._source_status()
        size = self._path.stat().st_size if status.ok else None
        return ImageStreamInfo(
            source_path=self.source_path,
            stream_type=self.stream_type,
            size=size,
            read_only=self.read_only,
            status=status,
        )

    def read_at(self, offset: int, length: int) -> ImageReadResult:
        range_status = self._range_status(offset, length)
        if not range_status.ok:
            return self._empty_read(offset, length, None, range_status)

        info = self.describe()
        if not info.status.ok:
            return self._empty_read(offset, length, info.size, info.status)

        source_size = info.size or 0
        if offset > source_size:
            return self._empty_read(
                offset,
                length,
                source_size,
                ImageStreamStatus(
                    code="read_beyond_end",
                    message="Read offset is beyond the end of the source.",
                    path=self.source_path,
                ),
            )

        warnings: tuple[ImageStreamWarning, ...] = ()
        if offset + length > source_size:
            warnings = (
                ImageStreamWarning(
                    code="read_truncated_at_eof",
                    message="Requested range extends beyond the end of the source; returned available bytes only.",
                    path=self.source_path,
                ),
            )

        try:
            with self._path.open("rb") as source:
                source.seek(offset)
                data = source.read(length)
        except OSError as error:
            return self._empty_read(
                offset,
                length,
                source_size,
                ImageStreamStatus(
                    code="source_unreadable",
                    message=f"Could not read source file: {error}",
                    path=self.source_path,
                ),
            )

        return ImageReadResult(
            source_path=self.source_path,
            stream_type=self.stream_type,
            read_only=self.read_only,
            offset=offset,
            length=length,
            source_size=source_size,
            data=data,
            status=ImageStreamStatus(
                code="ok",
                message="Read completed.",
                path=self.source_path,
            ),
            warnings=warnings,
        )

    def _source_status(self) -> ImageStreamStatus:
        if not self._path.exists():
            return ImageStreamStatus(
                code="missing_path",
                message="Source path does not exist.",
                path=self.source_path,
            )

        if self._path.is_dir():
            return ImageStreamStatus(
                code="path_is_directory",
                message="Source path is a directory, not a readable image file.",
                path=self.source_path,
            )

        if not self._path.is_file():
            return ImageStreamStatus(
                code="not_regular_file",
                message="Source path is not a regular file.",
                path=self.source_path,
            )

        try:
            with self._path.open("rb"):
                pass
        except OSError as error:
            return ImageStreamStatus(
                code="source_unreadable",
                message=f"Could not open source file read-only: {error}",
                path=self.source_path,
            )

        return ImageStreamStatus(
            code="ok",
            message="Source file is readable in read-only mode.",
            path=self.source_path,
        )

    def _range_status(self, offset: int, length: int) -> ImageStreamStatus:
        if offset < 0:
            return ImageStreamStatus(
                code="invalid_range",
                message="Read offset must be greater than or equal to zero.",
                path=self.source_path,
            )

        if length < 0:
            return ImageStreamStatus(
                code="invalid_range",
                message="Read length must be greater than or equal to zero.",
                path=self.source_path,
            )

        return ImageStreamStatus(
            code="ok",
            message="Read range is valid.",
            path=self.source_path,
        )

    def _empty_read(
        self,
        offset: int,
        length: int,
        source_size: int | None,
        status: ImageStreamStatus,
    ) -> ImageReadResult:
        return ImageReadResult(
            source_path=self.source_path,
            stream_type=self.stream_type,
            read_only=self.read_only,
            offset=offset,
            length=length,
            source_size=source_size,
            data=b"",
            status=status,
        )


_AUTO_IMPORT = object()


class EwfImageByteStream:
    """Read-only logical image stream backed by an EWF segment set."""

    stream_type = "ewf"
    read_only = True

    def __init__(
        self,
        selected_path: str | Path,
        *,
        segment_paths: Sequence[str | Path] | None = None,
        pyewf_module: object | None = _AUTO_IMPORT,
        import_error: BaseException | None = None,
    ) -> None:
        self._path = Path(selected_path).expanduser().resolve(strict=False)
        self._explicit_segment_paths = (
            tuple(Path(path).expanduser().resolve(strict=False) for path in segment_paths)
            if segment_paths is not None
            else None
        )

        if pyewf_module is _AUTO_IMPORT:
            try:
                import pyewf  # type: ignore[import-not-found]
            except ImportError as error:
                self._pyewf = None
                self._import_error = error
            else:
                self._pyewf = pyewf
                self._import_error = None
        else:
            self._pyewf = pyewf_module
            self._import_error = import_error

    @property
    def source_path(self) -> str:
        return str(self._path)

    @property
    def segment_paths(self) -> tuple[str, ...]:
        return tuple(str(path) for path in self._segment_paths())

    @property
    def is_available(self) -> bool:
        return self._pyewf is not None

    def describe(self) -> ImageStreamInfo:
        dependency_status = self._dependency_status()
        if not dependency_status.ok:
            return ImageStreamInfo(
                source_path=self.source_path,
                stream_type=self.stream_type,
                size=None,
                read_only=self.read_only,
                status=dependency_status,
                warnings=(self._warning_from_status(dependency_status),),
            )

        segment_status = self._segment_status()
        if not segment_status.ok:
            return ImageStreamInfo(
                source_path=self.source_path,
                stream_type=self.stream_type,
                size=None,
                read_only=self.read_only,
                status=segment_status,
                warnings=(self._warning_from_status(segment_status),),
            )

        handle = None
        try:
            handle = self._open_native_handle()
            media_size = self._media_size(handle)
        except Exception as error:
            return ImageStreamInfo(
                source_path=self.source_path,
                stream_type=self.stream_type,
                size=None,
                read_only=self.read_only,
                status=ImageStreamStatus(
                    code="ewf_open_failed",
                    message=f"EWF segment set could not be opened read-only: {error}",
                    path=self.source_path,
                ),
                warnings=(
                    ImageStreamWarning(
                        code="ewf_open_failed",
                        message="EWF segment set could not be opened read-only.",
                        path=self.source_path,
                    ),
                ),
            )
        finally:
            self._close_handle(handle)

        if media_size is None:
            return ImageStreamInfo(
                source_path=self.source_path,
                stream_type=self.stream_type,
                size=None,
                read_only=self.read_only,
                status=ImageStreamStatus(
                    code="ewf_media_size_unavailable",
                    message="EWF logical media size was not exposed by the reader.",
                    path=self.source_path,
                ),
                warnings=(
                    ImageStreamWarning(
                        code="ewf_media_size_unavailable",
                        message="EWF logical media size was not exposed by the reader.",
                        path=self.source_path,
                    ),
                ),
            )

        return ImageStreamInfo(
            source_path=self.source_path,
            stream_type=self.stream_type,
            size=media_size,
            read_only=self.read_only,
            status=ImageStreamStatus(
                code="ok",
                message="EWF logical image stream is readable in read-only mode.",
                path=self.source_path,
            ),
        )

    def read_at(self, offset: int, length: int) -> ImageReadResult:
        range_status = self._range_status(offset, length)
        if not range_status.ok:
            return self._empty_read(offset, length, None, range_status)

        info = self.describe()
        if not info.status.ok:
            return self._empty_read(offset, length, info.size, info.status)

        source_size = info.size or 0
        if offset > source_size:
            return self._empty_read(
                offset,
                length,
                source_size,
                ImageStreamStatus(
                    code="read_beyond_end",
                    message="Read offset is beyond the end of the EWF logical image.",
                    path=self.source_path,
                ),
            )

        read_length = length
        warnings: tuple[ImageStreamWarning, ...] = ()
        if offset + length > source_size:
            read_length = max(0, source_size - offset)
            warnings = (
                ImageStreamWarning(
                    code="read_truncated_at_eof",
                    message="Requested range extends beyond the end of the EWF logical image; returned available bytes only.",
                    path=self.source_path,
                ),
            )

        handle = None
        try:
            handle = self._open_native_handle()
            data = self._read_from_handle(handle, offset, read_length)
        except Exception as error:
            return self._empty_read(
                offset,
                length,
                source_size,
                ImageStreamStatus(
                    code="ewf_read_failed",
                    message=f"EWF logical image read failed: {error}",
                    path=self.source_path,
                ),
            )
        finally:
            self._close_handle(handle)

        return ImageReadResult(
            source_path=self.source_path,
            stream_type=self.stream_type,
            read_only=self.read_only,
            offset=offset,
            length=length,
            source_size=source_size,
            data=data,
            status=ImageStreamStatus(
                code="ok",
                message="Read completed.",
                path=self.source_path,
            ),
            warnings=warnings,
        )

    def _dependency_status(self) -> ImageStreamStatus:
        if self._pyewf is not None:
            return ImageStreamStatus(
                code="ok",
                message="pyewf/libewf is available for EWF logical image reads.",
                path=self.source_path,
            )

        message = "pyewf/libewf dependency is unavailable; EWF logical image reads cannot run."
        if self._import_error is not None:
            message = f"{message} Import error: {self._import_error}"
        return ImageStreamStatus(
            code="dependency_unavailable",
            message=message,
            path=self.source_path,
        )

    def _segment_status(self) -> ImageStreamStatus:
        paths = self._segment_paths()
        if not paths:
            return ImageStreamStatus(
                code="segment_set_unavailable",
                message="No EWF segment paths were available for the selected evidence.",
                path=self.source_path,
            )

        missing = [path for path in paths if not path.exists()]
        if missing:
            return ImageStreamStatus(
                code="segment_set_incomplete",
                message="One or more EWF segment paths are missing.",
                path=str(missing[0]),
            )

        return ImageStreamStatus(
            code="ok",
            message="EWF segment paths are available.",
            path=self.source_path,
        )

    def _segment_paths(self) -> tuple[Path, ...]:
        if self._explicit_segment_paths is not None:
            return self._explicit_segment_paths

        discovery = discover_e01_segments(self._path)
        return tuple(Path(segment.path) for segment in discovery.segments)

    def _open_native_handle(self) -> object:
        if self._pyewf is None:
            raise RuntimeError("pyewf/libewf dependency is unavailable")

        handle_factory = getattr(self._pyewf, "handle", None)
        if handle_factory is None or not callable(handle_factory):
            raise RuntimeError("pyewf.handle is unavailable")

        handle = handle_factory()
        open_method = getattr(handle, "open", None)
        if open_method is None or not callable(open_method):
            self._close_handle(handle)
            raise RuntimeError("pyewf handle does not expose open()")

        try:
            open_method([str(path) for path in self._segment_paths()])
        except Exception:
            self._close_handle(handle)
            raise
        return handle

    def _media_size(self, handle: object) -> int | None:
        get_media_size = getattr(handle, "get_media_size", None)
        if callable(get_media_size):
            value = get_media_size()
        else:
            value = getattr(handle, "media_size", None)

        if value is None:
            return None
        return int(value)

    def bytes_per_sector(self) -> int | None:
        handle = None
        try:
            handle = self._open_native_handle()
            get_bytes_per_sector = getattr(handle, "get_bytes_per_sector", None)
            if callable(get_bytes_per_sector):
                value = get_bytes_per_sector()
            else:
                value = getattr(handle, "bytes_per_sector", None)
            return int(value) if value is not None else None
        except Exception:
            return None
        finally:
            self._close_handle(handle)

    def _read_from_handle(self, handle: object, offset: int, length: int) -> bytes:
        if length == 0:
            return b""

        read_at = getattr(handle, "read_buffer_at_offset", None)
        if callable(read_at):
            return read_at(length, offset)

        seek = getattr(handle, "seek", None) or getattr(handle, "seek_offset", None)
        read = getattr(handle, "read", None) or getattr(handle, "read_buffer", None)
        if callable(seek) and callable(read):
            seek(offset)
            return read(length)

        raise RuntimeError("pyewf handle does not expose a supported read method")

    def _range_status(self, offset: int, length: int) -> ImageStreamStatus:
        if offset < 0:
            return ImageStreamStatus(
                code="invalid_range",
                message="Read offset must be greater than or equal to zero.",
                path=self.source_path,
            )
        if length < 0:
            return ImageStreamStatus(
                code="invalid_range",
                message="Read length must be greater than or equal to zero.",
                path=self.source_path,
            )
        return ImageStreamStatus(
            code="ok",
            message="Read range is valid.",
            path=self.source_path,
        )

    def _empty_read(
        self,
        offset: int,
        length: int,
        source_size: int | None,
        status: ImageStreamStatus,
    ) -> ImageReadResult:
        return ImageReadResult(
            source_path=self.source_path,
            stream_type=self.stream_type,
            read_only=self.read_only,
            offset=offset,
            length=length,
            source_size=source_size,
            data=b"",
            status=status,
        )

    def _warning_from_status(self, status: ImageStreamStatus) -> ImageStreamWarning:
        return ImageStreamWarning(
            code=status.code,
            message=status.message,
            path=status.path,
        )

    def _close_handle(self, handle: object | None) -> None:
        if handle is None:
            return
        close = getattr(handle, "close", None)
        if callable(close):
            close()
