"""Read-only image byte-stream abstractions for Stage 2."""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
from pathlib import Path
from typing import Protocol, Sequence

from app.backend.forensic_core.segment_discovery import discover_e01_segments


DEFAULT_IMAGE_HASH_CHUNK_SIZE = 4 * 1024 * 1024
SUPPORTED_IMAGE_HASH_ALGORITHMS = ("sha256",)


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


@dataclass(frozen=True)
class ImageHashStatus:
    """Structured status for full logical-image hash operations."""

    code: str
    message: str
    path: str | None = None

    @property
    def ok(self) -> bool:
        return self.code == "completed"

    def to_dict(self) -> dict[str, object]:
        return {
            "code": self.code,
            "ok": self.ok,
            "message": self.message,
            "path": self.path,
        }


@dataclass(frozen=True)
class ImageHashResult:
    """Computed hash result for a read-only logical image stream."""

    source_path: str
    stream_type: str
    read_only: bool
    algorithm: str
    status: ImageHashStatus
    hexdigest: str | None
    bytes_hashed: int
    logical_media_size: int | None
    byte_count_matches_media_size: bool | None
    warnings: tuple[ImageStreamWarning, ...] = field(default_factory=tuple)

    @property
    def source_kind(self) -> str:
        if self.stream_type == "ewf":
            return "ewf_logical_image"
        return f"{self.stream_type}_image"

    def to_dict(self) -> dict[str, object]:
        return {
            "source_path": self.source_path,
            "stream_type": self.stream_type,
            "source_kind": self.source_kind,
            "read_only": self.read_only,
            "algorithm": self.algorithm,
            "status": self.status.to_dict(),
            "hexdigest": self.hexdigest,
            "bytes_hashed": self.bytes_hashed,
            "logical_media_size": self.logical_media_size,
            "byte_count_matches_media_size": self.byte_count_matches_media_size,
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


def hash_image_stream(
    stream: ImageByteStream,
    *,
    algorithm: str = "sha256",
    chunk_size: int = DEFAULT_IMAGE_HASH_CHUNK_SIZE,
) -> ImageHashResult:
    """Hash a full read-only logical image stream in bounded chunks."""

    normalized_algorithm = _normalize_image_hash_algorithm(algorithm)
    source_path = str(getattr(stream, "source_path", ""))
    stream_type = str(getattr(stream, "stream_type", "unknown"))
    read_only = bool(getattr(stream, "read_only", False))

    if normalized_algorithm not in SUPPORTED_IMAGE_HASH_ALGORITHMS:
        return ImageHashResult(
            source_path=source_path,
            stream_type=stream_type,
            read_only=read_only,
            algorithm=normalized_algorithm,
            status=ImageHashStatus(
                code="failed",
                message="Unsupported image hash algorithm.",
                path=source_path,
            ),
            hexdigest=None,
            bytes_hashed=0,
            logical_media_size=None,
            byte_count_matches_media_size=None,
            warnings=(
                ImageStreamWarning(
                    code="unsupported_image_hash_algorithm",
                    message="Only SHA-256 is currently supported for full logical-image hashing.",
                    path=source_path,
                ),
            ),
        )

    if chunk_size <= 0:
        return ImageHashResult(
            source_path=source_path,
            stream_type=stream_type,
            read_only=read_only,
            algorithm=normalized_algorithm,
            status=ImageHashStatus(
                code="failed",
                message="Image hash chunk size must be greater than zero.",
                path=source_path,
            ),
            hexdigest=None,
            bytes_hashed=0,
            logical_media_size=None,
            byte_count_matches_media_size=None,
            warnings=(
                ImageStreamWarning(
                    code="invalid_image_hash_chunk_size",
                    message="Image hash chunk size must be greater than zero.",
                    path=source_path,
                ),
            ),
        )

    info = stream.describe()
    warnings = list(info.warnings)
    if not info.status.ok:
        status_code = (
            "dependency_unavailable"
            if info.status.code == "dependency_unavailable"
            else "stream_unavailable"
        )
        warnings.append(_image_hash_warning_from_stream_status(info.status))
        return ImageHashResult(
            source_path=info.source_path,
            stream_type=info.stream_type,
            read_only=info.read_only,
            algorithm=normalized_algorithm,
            status=ImageHashStatus(
                code=status_code,
                message="Logical image stream is unavailable for full-image hashing.",
                path=info.source_path,
            ),
            hexdigest=None,
            bytes_hashed=0,
            logical_media_size=info.size,
            byte_count_matches_media_size=None,
            warnings=tuple(warnings),
        )

    if info.size is None:
        return ImageHashResult(
            source_path=info.source_path,
            stream_type=info.stream_type,
            read_only=info.read_only,
            algorithm=normalized_algorithm,
            status=ImageHashStatus(
                code="stream_unavailable",
                message="Logical image media size is unavailable for full-image hashing.",
                path=info.source_path,
            ),
            hexdigest=None,
            bytes_hashed=0,
            logical_media_size=None,
            byte_count_matches_media_size=None,
            warnings=(
                *warnings,
                ImageStreamWarning(
                    code="image_hash_media_size_unavailable",
                    message="Logical image media size is required before hashing the full image.",
                    path=info.source_path,
                ),
            ),
        )

    digest = hashlib.new(normalized_algorithm)
    if isinstance(stream, EwfImageByteStream):
        bytes_hashed, read_warnings, failure = _hash_ewf_stream_native(
            stream,
            digest,
            media_size=info.size,
            chunk_size=chunk_size,
        )
    else:
        bytes_hashed, read_warnings, failure = _hash_generic_stream(
            stream,
            digest,
            media_size=info.size,
            chunk_size=chunk_size,
        )
    warnings.extend(read_warnings)

    if failure is not None:
        return ImageHashResult(
            source_path=info.source_path,
            stream_type=info.stream_type,
            read_only=info.read_only,
            algorithm=normalized_algorithm,
            status=failure,
            hexdigest=None,
            bytes_hashed=bytes_hashed,
            logical_media_size=info.size,
            byte_count_matches_media_size=bytes_hashed == info.size,
            warnings=tuple(warnings),
        )

    byte_count_matches = bytes_hashed == info.size
    status = ImageHashStatus(
        code="completed" if byte_count_matches else "failed",
        message=(
            "Full logical-image hash completed."
            if byte_count_matches
            else "Image hash byte count did not match the logical media size."
        ),
        path=info.source_path,
    )
    if not byte_count_matches:
        warnings.append(
            ImageStreamWarning(
                code="image_hash_byte_count_mismatch",
                message="Bytes hashed did not match the logical media size.",
                path=info.source_path,
            )
        )
    return ImageHashResult(
        source_path=info.source_path,
        stream_type=info.stream_type,
        read_only=info.read_only,
        algorithm=normalized_algorithm,
        status=status,
        hexdigest=digest.hexdigest() if byte_count_matches else None,
        bytes_hashed=bytes_hashed,
        logical_media_size=info.size,
        byte_count_matches_media_size=byte_count_matches,
        warnings=tuple(warnings),
    )


def _hash_generic_stream(
    stream: ImageByteStream,
    digest: object,
    *,
    media_size: int,
    chunk_size: int,
) -> tuple[int, list[ImageStreamWarning], ImageHashStatus | None]:
    offset = 0
    warnings: list[ImageStreamWarning] = []
    while offset < media_size:
        length = min(chunk_size, media_size - offset)
        read_result = stream.read_at(offset, length)
        warnings.extend(read_result.warnings)
        if not read_result.status.ok:
            warnings.append(_image_hash_warning_from_stream_status(read_result.status))
            return (
                offset,
                warnings,
                ImageHashStatus(
                    code=(
                        "dependency_unavailable"
                        if read_result.status.code == "dependency_unavailable"
                        else "failed"
                    ),
                    message="Logical image read failed during hashing.",
                    path=read_result.source_path,
                ),
            )

        data_length = len(read_result.data)
        if data_length == 0 and length > 0:
            warning = ImageStreamWarning(
                code="image_hash_empty_read",
                message="Image stream returned zero bytes before the logical media size was exhausted.",
                path=read_result.source_path,
            )
            warnings.append(warning)
            return (
                offset,
                warnings,
                ImageHashStatus(
                    code="failed",
                    message="Logical image hashing stopped after an empty read.",
                    path=read_result.source_path,
                ),
            )

        digest.update(read_result.data)
        offset += data_length
        if data_length < length and offset < media_size:
            warning = ImageStreamWarning(
                code="image_hash_short_read",
                message="Image stream returned fewer bytes than requested before reaching the logical media size.",
                path=read_result.source_path,
            )
            warnings.append(warning)
            return (
                offset,
                warnings,
                ImageHashStatus(
                    code="failed",
                    message="Logical image hashing stopped after a short read.",
                    path=read_result.source_path,
                ),
            )
    return offset, warnings, None


def _hash_ewf_stream_native(
    stream: EwfImageByteStream,
    digest: object,
    *,
    media_size: int,
    chunk_size: int,
) -> tuple[int, list[ImageStreamWarning], ImageHashStatus | None]:
    offset = 0
    warnings: list[ImageStreamWarning] = []
    handle = None
    try:
        handle = stream._open_native_handle()
        while offset < media_size:
            length = min(chunk_size, media_size - offset)
            data = stream._read_from_handle(handle, offset, length)
            data_length = len(data)
            if data_length == 0 and length > 0:
                warnings.append(
                    ImageStreamWarning(
                        code="image_hash_empty_read",
                        message="EWF stream returned zero bytes before the logical media size was exhausted.",
                        path=stream.source_path,
                    )
                )
                return (
                    offset,
                    warnings,
                    ImageHashStatus(
                        code="failed",
                        message="Logical image hashing stopped after an empty EWF read.",
                        path=stream.source_path,
                    ),
                )

            digest.update(data)
            offset += data_length
            if data_length < length and offset < media_size:
                warnings.append(
                    ImageStreamWarning(
                        code="image_hash_short_read",
                        message="EWF stream returned fewer bytes than requested before reaching the logical media size.",
                        path=stream.source_path,
                    )
                )
                return (
                    offset,
                    warnings,
                    ImageHashStatus(
                        code="failed",
                        message="Logical image hashing stopped after a short EWF read.",
                        path=stream.source_path,
                    ),
                )
    except Exception as error:
        warnings.append(
            ImageStreamWarning(
                code="image_hash_read_failed",
                message=f"Logical image read failed during hashing: {error}",
                path=stream.source_path,
            )
        )
        return (
            offset,
            warnings,
            ImageHashStatus(
                code="failed",
                message="Logical image read failed during hashing.",
                path=stream.source_path,
            ),
        )
    finally:
        stream._close_handle(handle)
    return offset, warnings, None


def _normalize_image_hash_algorithm(algorithm: str) -> str:
    return algorithm.strip().lower().replace("-", "")


def _image_hash_warning_from_stream_status(status: ImageStreamStatus) -> ImageStreamWarning:
    return ImageStreamWarning(
        code=status.code,
        message=status.message,
        path=status.path,
    )
