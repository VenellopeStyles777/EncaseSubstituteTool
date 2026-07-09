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
from app.backend.forensic_core.filesystem_adapter import (
    FILESYSTEM_ADAPTER_SCHEMA_VERSION,
    FilesystemAdapter,
    FilesystemDependencyStatus,
    FilesystemEntry,
    FilesystemResult,
    FilesystemStatus,
    FilesystemWarning,
    Pytsk3FilesystemAdapter,
    StubFilesystemAdapter,
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
    "FILESYSTEM_ADAPTER_SCHEMA_VERSION",
    "FilesystemAdapter",
    "FilesystemDependencyStatus",
    "FilesystemEntry",
    "FilesystemResult",
    "FilesystemStatus",
    "FilesystemWarning",
    "ImageByteStream",
    "ImageReadResult",
    "ImageStreamInfo",
    "ImageStreamStatus",
    "ImageStreamWarning",
    "LocalFileImageStream",
    "PyewfEwfReaderAdapter",
    "Pytsk3FilesystemAdapter",
    "ReaderDependencyStatus",
    "SegmentDiscoveryResult",
    "SegmentInfo",
    "SegmentWarning",
    "StubFilesystemAdapter",
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
