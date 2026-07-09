"""Volume discovery boundaries for Stage 2."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.backend.forensic_core.image_stream import ImageByteStream


VOLUME_DISCOVERY_SCHEMA_VERSION = "stage2.volume_discovery.v1"


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
) -> VolumeDiscoveryResult:
    """Discover volumes for a read-only image stream.

    Stage 2 supports a whole-image/single-volume strategy only. Real partition
    table parsing is represented by structured unsupported status for now.
    """

    stream_info = image_stream.describe()

    if strategy != "whole_image":
        return VolumeDiscoveryResult(
            schema_version=VOLUME_DISCOVERY_SCHEMA_VERSION,
            source_path=stream_info.source_path,
            stream_type=stream_info.stream_type,
            source_size=stream_info.size,
            read_only=stream_info.read_only,
            strategy=strategy,
            status=VolumeDiscoveryStatus(
                code="partition_parsing_unsupported",
                message="Real partition-table parsing is not implemented in S2-T03.",
            ),
            warnings=(
                VolumeDiscoveryWarning(
                    code="partition_parsing_deferred",
                    message="Use the whole_image strategy for S2-T03 fixture-backed behavior.",
                ),
            ),
        )

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
