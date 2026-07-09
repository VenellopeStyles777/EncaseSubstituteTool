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
from app.backend.forensic_core.segment_discovery import (
    SegmentDiscoveryResult,
    SegmentInfo,
    SegmentWarning,
    discover_e01_segments,
)

__all__ = [
    "EwfMetadataResult",
    "EwfReaderAdapter",
    "EwfReaderWarning",
    "PyewfEwfReaderAdapter",
    "ReaderDependencyStatus",
    "SegmentDiscoveryResult",
    "SegmentInfo",
    "SegmentWarning",
    "StubEwfReaderAdapter",
    "VerificationStatus",
    "discover_e01_segments",
]
