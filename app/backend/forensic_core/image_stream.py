"""Read-only image byte-stream abstractions for Stage 2."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol


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
