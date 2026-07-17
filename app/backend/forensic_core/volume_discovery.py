"""Volume discovery boundaries for Stage 2."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.backend.forensic_core.image_stream import ImageByteStream


VOLUME_DISCOVERY_SCHEMA_VERSION = "stage2.volume_discovery.v1"
_AUTO_IMPORT = object()


@dataclass(frozen=True)
class VolumeDiscoveryStatus:
    """Structured status for volume discovery operations."""

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
class VolumeDiscoveryWarning:
    """Structured non-fatal warning for volume discovery."""

    code: str
    message: str

    def to_dict(self) -> dict[str, object]:
        return {
            "code": self.code,
            "message": self.message,
        }


@dataclass(frozen=True)
class VolumeInfo:
    """One discovered volume-like range within an image stream."""

    volume_id: str
    volume_index: int
    source_path: str
    stream_type: str
    source_size: int
    offset: int
    length: int
    volume_type: str
    description: str
    read_only: bool
    status: VolumeDiscoveryStatus
    warnings: tuple[VolumeDiscoveryWarning, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        return {
            "volume_id": self.volume_id,
            "volume_index": self.volume_index,
            "source_path": self.source_path,
            "stream_type": self.stream_type,
            "source_size": self.source_size,
            "offset": self.offset,
            "length": self.length,
            "volume_type": self.volume_type,
            "description": self.description,
            "read_only": self.read_only,
            "status": self.status.to_dict(),
            "warnings": [warning.to_dict() for warning in self.warnings],
        }


@dataclass(frozen=True)
class VolumeDiscoveryResult:
    """JSON-friendly volume discovery result for one image stream."""

    schema_version: str
    source_path: str
    stream_type: str
    source_size: int | None
    read_only: bool
    strategy: str
    status: VolumeDiscoveryStatus
    volumes: tuple[VolumeInfo, ...] = field(default_factory=tuple)
    warnings: tuple[VolumeDiscoveryWarning, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "source_path": self.source_path,
            "stream_type": self.stream_type,
            "source_size": self.source_size,
            "read_only": self.read_only,
            "strategy": self.strategy,
            "status": self.status.to_dict(),
            "volumes": [volume.to_dict() for volume in self.volumes],
            "warnings": [warning.to_dict() for warning in self.warnings],
        }


def discover_volumes(
    image_stream: ImageByteStream,
    *,
    strategy: str = "whole_image",
    pytsk3_module: object | None = _AUTO_IMPORT,
    import_error: BaseException | None = None,
) -> VolumeDiscoveryResult:
    """Discover volumes for a read-only image stream.

    Stage 2 supports a whole-image/single-volume strategy only. Real partition
    table parsing is represented by structured unsupported status for now.
    """

    stream_info = image_stream.describe()

    if strategy not in {"whole_image", "partition_table", "auto"}:
        return _unsupported_strategy_result(stream_info, strategy)

    if not stream_info.status.ok:
        return VolumeDiscoveryResult(
            schema_version=VOLUME_DISCOVERY_SCHEMA_VERSION,
            source_path=stream_info.source_path,
            stream_type=stream_info.stream_type,
            source_size=stream_info.size,
            read_only=stream_info.read_only,
            strategy=strategy,
            status=VolumeDiscoveryStatus(
                code="image_stream_unavailable",
                message=f"Image stream is unavailable: {stream_info.status.message}",
            ),
            warnings=(
                VolumeDiscoveryWarning(
                    code=stream_info.status.code,
                    message=stream_info.status.message,
                ),
            ),
        )

    if strategy in {"partition_table", "auto"}:
        partition_result = _discover_partition_table_volumes(
            image_stream,
            stream_info=stream_info,
            strategy=strategy,
            pytsk3_module=pytsk3_module,
            import_error=import_error,
        )
        if partition_result.status.ok or strategy == "partition_table":
            return partition_result

        if strategy == "auto":
            fallback = _whole_image_result(image_stream, stream_info, strategy="whole_image")
            return VolumeDiscoveryResult(
                schema_version=fallback.schema_version,
                source_path=fallback.source_path,
                stream_type=fallback.stream_type,
                source_size=fallback.source_size,
                read_only=fallback.read_only,
                strategy="auto",
                status=fallback.status,
                volumes=fallback.volumes,
                warnings=partition_result.warnings
                + (
                    VolumeDiscoveryWarning(
                        code="whole_image_fallback",
                        message="Partition parsing did not produce volumes; emitted whole-image fallback.",
                    ),
                ),
            )

    if stream_info.size == 0:
        return VolumeDiscoveryResult(
            schema_version=VOLUME_DISCOVERY_SCHEMA_VERSION,
            source_path=stream_info.source_path,
            stream_type=stream_info.stream_type,
            source_size=0,
            read_only=stream_info.read_only,
            strategy=strategy,
            status=VolumeDiscoveryStatus(
                code="empty_image",
                message="Image stream is readable but contains zero bytes.",
            ),
            warnings=(
                VolumeDiscoveryWarning(
                    code="empty_image",
                    message="No whole-image volume was emitted for a zero-byte source.",
                ),
            ),
        )

    return _whole_image_result(image_stream, stream_info, strategy=strategy)


def _whole_image_result(
    image_stream: ImageByteStream,
    stream_info,
    *,
    strategy: str,
) -> VolumeDiscoveryResult:
    source_size = stream_info.size or 0
    volume = VolumeInfo(
        volume_id="volume-0",
        volume_index=0,
        source_path=stream_info.source_path,
        stream_type=stream_info.stream_type,
        source_size=source_size,
        offset=0,
        length=source_size,
        volume_type="whole_image",
        description="Whole image exposed as a single volume-like range.",
        read_only=stream_info.read_only,
        status=VolumeDiscoveryStatus(
            code="ok",
            message="Whole-image volume discovered.",
        ),
    )

    return VolumeDiscoveryResult(
        schema_version=VOLUME_DISCOVERY_SCHEMA_VERSION,
        source_path=stream_info.source_path,
        stream_type=stream_info.stream_type,
        source_size=source_size,
        read_only=stream_info.read_only,
        strategy=strategy,
        status=VolumeDiscoveryStatus(
            code="ok",
            message="Volume discovery completed using whole-image strategy.",
        ),
        volumes=(volume,),
    )


def _unsupported_strategy_result(stream_info, strategy: str) -> VolumeDiscoveryResult:
    return VolumeDiscoveryResult(
        schema_version=VOLUME_DISCOVERY_SCHEMA_VERSION,
        source_path=stream_info.source_path,
        stream_type=stream_info.stream_type,
        source_size=stream_info.size,
        read_only=stream_info.read_only,
        strategy=strategy,
        status=VolumeDiscoveryStatus(
            code="partition_parsing_unsupported",
            message="Requested volume discovery strategy is not implemented.",
        ),
        warnings=(
            VolumeDiscoveryWarning(
                code="partition_parsing_deferred",
                message="Use whole_image, partition_table, or auto.",
            ),
        ),
    )


def _discover_partition_table_volumes(
    image_stream: ImageByteStream,
    *,
    stream_info,
    strategy: str,
    pytsk3_module: object | None,
    import_error: BaseException | None,
) -> VolumeDiscoveryResult:
    pytsk3 = _resolve_pytsk3(pytsk3_module)
    if pytsk3 is None:
        message = "pytsk3/The Sleuth Kit dependency is unavailable; partition table was not parsed."
        if import_error is not None:
            message = f"{message} Import error: {import_error}"
        return VolumeDiscoveryResult(
            schema_version=VOLUME_DISCOVERY_SCHEMA_VERSION,
            source_path=stream_info.source_path,
            stream_type=stream_info.stream_type,
            source_size=stream_info.size,
            read_only=stream_info.read_only,
            strategy=strategy,
            status=VolumeDiscoveryStatus(
                code="partition_dependency_unavailable",
                message=message,
            ),
            warnings=(
                VolumeDiscoveryWarning(
                    code="partition_dependency_unavailable",
                    message="pytsk3 is unavailable; no partition records were emitted.",
                ),
            ),
        )

    image_info = _Pytsk3ImageInfo(image_stream, pytsk3)
    try:
        try:
            raw_volumes = list(pytsk3.Volume_Info(image_info))
        except Exception as error:
            return VolumeDiscoveryResult(
                schema_version=VOLUME_DISCOVERY_SCHEMA_VERSION,
                source_path=stream_info.source_path,
                stream_type=stream_info.stream_type,
                source_size=stream_info.size,
                read_only=stream_info.read_only,
                strategy=strategy,
                status=VolumeDiscoveryStatus(
                    code="partition_parse_error",
                    message=f"Partition table parsing failed: {error}",
                ),
                warnings=(
                    VolumeDiscoveryWarning(
                        code="partition_parse_error",
                        message="pytsk3 could not parse a partition table from the image stream.",
                    ),
                ),
            )
    finally:
        image_info.close()

    sector_size = _sector_size(image_stream)
    if sector_size is None:
        return VolumeDiscoveryResult(
            schema_version=VOLUME_DISCOVERY_SCHEMA_VERSION,
            source_path=stream_info.source_path,
            stream_type=stream_info.stream_type,
            source_size=stream_info.size,
            read_only=stream_info.read_only,
            strategy=strategy,
            status=VolumeDiscoveryStatus(
                code="partition_parse_error",
                message="Partition parser produced sector units, but sector size is unavailable.",
            ),
            warnings=(
                VolumeDiscoveryWarning(
                    code="sector_size_unavailable",
                    message="Could not convert partition sector offsets to bytes.",
                ),
            ),
        )

    allocated_flag = int(getattr(pytsk3, "TSK_VS_PART_FLAG_ALLOC", 1))
    volumes: list[VolumeInfo] = []
    skipped = 0
    for raw_index, part in enumerate(raw_volumes):
        flags = int(getattr(part, "flags", 0) or 0)
        start = int(getattr(part, "start", 0) or 0)
        length = int(getattr(part, "len", 0) or 0)
        if length <= 0 or not flags & allocated_flag:
            skipped += 1
            continue

        offset = start * sector_size
        byte_length = length * sector_size
        description = _partition_description(part)
        volume = VolumeInfo(
            volume_id=f"volume-{len(volumes)}",
            volume_index=len(volumes),
            source_path=stream_info.source_path,
            stream_type=stream_info.stream_type,
            source_size=stream_info.size or 0,
            offset=offset,
            length=byte_length,
            volume_type=description or "partition",
            description=description or f"Partition {raw_index}",
            read_only=stream_info.read_only,
            status=VolumeDiscoveryStatus(
                code="ok",
                message="Partition volume discovered.",
            ),
        )
        volumes.append(volume)

    if not volumes:
        return VolumeDiscoveryResult(
            schema_version=VOLUME_DISCOVERY_SCHEMA_VERSION,
            source_path=stream_info.source_path,
            stream_type=stream_info.stream_type,
            source_size=stream_info.size,
            read_only=stream_info.read_only,
            strategy=strategy,
            status=VolumeDiscoveryStatus(
                code="partition_table_not_found",
                message="Partition parser ran but emitted no allocated partition volumes.",
            ),
            warnings=(
                VolumeDiscoveryWarning(
                    code="partition_table_not_found",
                    message="No allocated partition entries were available for filesystem parsing.",
                ),
            ),
        )

    warnings: tuple[VolumeDiscoveryWarning, ...] = ()
    if skipped:
        warnings = (
            VolumeDiscoveryWarning(
                code="partition_entries_skipped",
                message=f"Skipped {skipped} metadata, safety, unallocated, or zero-length partition entries.",
            ),
        )

    return VolumeDiscoveryResult(
        schema_version=VOLUME_DISCOVERY_SCHEMA_VERSION,
        source_path=stream_info.source_path,
        stream_type=stream_info.stream_type,
        source_size=stream_info.size,
        read_only=stream_info.read_only,
        strategy=strategy,
        status=VolumeDiscoveryStatus(
            code="ok",
            message="Partition table parsing completed.",
        ),
        volumes=tuple(volumes),
        warnings=warnings,
    )


def _resolve_pytsk3(pytsk3_module: object | None) -> object | None:
    if pytsk3_module is not _AUTO_IMPORT:
        return pytsk3_module
    try:
        import pytsk3  # type: ignore[import-not-found]
    except ImportError:
        return None
    return pytsk3


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


def _sector_size(image_stream: ImageByteStream) -> int | None:
    bytes_per_sector = getattr(image_stream, "bytes_per_sector", None)
    if callable(bytes_per_sector):
        value = bytes_per_sector()
        if value:
            return int(value)
    return 512


def _partition_description(part: object) -> str:
    raw = getattr(part, "desc", "")
    if isinstance(raw, bytes):
        return raw.decode("utf-8", "replace").strip()
    return str(raw).strip()
