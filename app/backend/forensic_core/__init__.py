"""Forensic core package for evidence-facing logic."""

from app.backend.forensic_core.ewf_reader import (
    EwfMetadataResult,
    EwfReaderAdapter,
    EwfReaderWarning,
    PyewfEwfReaderAdapter,
    ReaderDependencyStatus,
    StubEwfReaderAdapter,
    VerificationStatus,
)
from app.backend.forensic_core.image_stream import (
    ImageByteStream,
    ImageReadResult,
    ImageStreamInfo,
    ImageStreamStatus,
    ImageStreamWarning,
    LocalFileImageStream,
)
from app.backend.forensic_core.segment_discovery import (
    SegmentDiscoveryResult,
    SegmentInfo,
    SegmentWarning,
    discover_e01_segments,
)
from app.backend.forensic_core.volume_discovery import (
    VOLUME_DISCOVERY_SCHEMA_VERSION,
    VolumeDiscoveryResult,
    VolumeDiscoveryStatus,
    VolumeDiscoveryWarning,
    VolumeInfo,
    discover_volumes,
)

__all__ = [
    "EwfMetadataResult",
    "EwfReaderAdapter",
    "EwfReaderWarning",
    "ImageByteStream",
    "ImageReadResult",
    "ImageStreamInfo",
    "ImageStreamStatus",
    "ImageStreamWarning",
    "LocalFileImageStream",
    "PyewfEwfReaderAdapter",
    "ReaderDependencyStatus",
    "SegmentDiscoveryResult",
    "SegmentInfo",
    "SegmentWarning",
    "StubEwfReaderAdapter",
    "VOLUME_DISCOVERY_SCHEMA_VERSION",
    "VerificationStatus",
    "VolumeDiscoveryResult",
    "VolumeDiscoveryStatus",
    "VolumeDiscoveryWarning",
    "VolumeInfo",
    "discover_e01_segments",
    "discover_volumes",
]
