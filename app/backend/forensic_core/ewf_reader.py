"""EWF reader adapter contracts and dependency-free implementations."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol, Sequence


class EwfReaderAdapter(Protocol):
    """Protocol for read-only EWF metadata and verification adapters."""

    name: str
    read_only: bool

    @property
    def is_available(self) -> bool:
        """Whether the adapter can read real EWF evidence in this environment."""

    def dependency_status(self) -> "ReaderDependencyStatus":
        """Return structured dependency availability information."""

    def read_metadata(self, segment_paths: Sequence[str | Path]) -> "EwfMetadataResult":
        """Return metadata for an EWF segment set without modifying evidence."""

    def verify(self, segment_paths: Sequence[str | Path]) -> "VerificationStatus":
        """Return verification status for an EWF segment set."""


@dataclass(frozen=True)
class ReaderDependencyStatus:
    """Structured dependency status for an adapter."""

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
class EwfReaderWarning:
    """Structured warning emitted by an EWF reader adapter."""

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
class VerificationStatus:
    """Stable verification status shape for EWF evidence."""

    status: str
    supported: bool
    message: str
    details: dict[str, object] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return {
            "status": self.status,
            "supported": self.supported,
            "message": self.message,
            "details": dict(self.details),
        }


@dataclass(frozen=True)
class EwfMetadataResult:
    """Stable metadata result returned by EWF reader adapters."""

    adapter_name: str
    adapter_available: bool
    read_only: bool
    source_paths: tuple[str, ...]
    metadata: dict[str, object]
    verification: VerificationStatus
    dependency: ReaderDependencyStatus
    warnings: tuple[EwfReaderWarning, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        return {
            "adapter_name": self.adapter_name,
            "adapter_available": self.adapter_available,
            "read_only": self.read_only,
            "source_paths": list(self.source_paths),
            "metadata": dict(self.metadata),
            "verification": self.verification.to_dict(),
            "dependency": self.dependency.to_dict(),
            "warnings": [warning.to_dict() for warning in self.warnings],
        }


class StubEwfReaderAdapter:
    """Dependency-free EWF reader for tests and early integration."""

    name = "stub-ewf-reader"
    read_only = True

    @property
    def is_available(self) -> bool:
        return True

    def dependency_status(self) -> ReaderDependencyStatus:
        return ReaderDependencyStatus(
            name="stub",
            available=True,
            message="Stub EWF reader is available for dependency-free tests.",
        )

    def read_metadata(self, segment_paths: Sequence[str | Path]) -> EwfMetadataResult:
        paths = _normalize_paths(segment_paths)
        return EwfMetadataResult(
            adapter_name=self.name,
            adapter_available=self.is_available,
            read_only=self.read_only,
            source_paths=paths,
            metadata={
                "format": "EWF",
                "reader": "stub",
                "segment_count": len(paths),
                "case_number": "STUB-CASE",
                "examiner": "Stub Examiner",
                "notes": "Predictable fake metadata for tests; not forensic evidence.",
            },
            verification=self.verify(segment_paths),
            dependency=self.dependency_status(),
            warnings=(
                EwfReaderWarning(
                    code="stub_metadata",
                    message="Stub metadata is synthetic and must not be used as forensic fact.",
                ),
            ),
        )

    def verify(self, segment_paths: Sequence[str | Path]) -> VerificationStatus:
        paths = _normalize_paths(segment_paths)
        return VerificationStatus(
            status="not_supported",
            supported=False,
            message="Stub EWF reader does not verify evidence integrity.",
            details={"segment_count": len(paths)},
        )


_AUTO_IMPORT = object()


class PyewfEwfReaderAdapter:
    """Optional pyewf adapter skeleton with graceful dependency handling."""

    name = "pyewf-reader"
    read_only = True

    def __init__(
        self,
        pyewf_module: object | None = _AUTO_IMPORT,
        import_error: BaseException | None = None,
    ) -> None:
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
    def is_available(self) -> bool:
        return self._pyewf is not None

    def dependency_status(self) -> ReaderDependencyStatus:
        if not self.is_available:
            message = "pyewf is not installed; real EWF metadata reading is unavailable."
            if self._import_error is not None:
                message = f"{message} Import error: {self._import_error}"
            return ReaderDependencyStatus(
                name="pyewf",
                available=False,
                message=message,
            )

        return ReaderDependencyStatus(
            name="pyewf",
            available=True,
            message="pyewf is available; real metadata reading is not implemented in S1-T03.",
            version=getattr(self._pyewf, "__version__", None),
        )

    def read_metadata(self, segment_paths: Sequence[str | Path]) -> EwfMetadataResult:
        paths = _normalize_paths(segment_paths)
        dependency = self.dependency_status()
        if not dependency.available:
            return EwfMetadataResult(
                adapter_name=self.name,
                adapter_available=False,
                read_only=self.read_only,
                source_paths=paths,
                metadata={},
                verification=self.verify(segment_paths),
                dependency=dependency,
                warnings=(
                    EwfReaderWarning(
                        code="dependency_unavailable",
                        message="pyewf/libewf dependency is unavailable; metadata was not read.",
                    ),
                ),
            )

        return EwfMetadataResult(
            adapter_name=self.name,
            adapter_available=True,
            read_only=self.read_only,
            source_paths=paths,
            metadata={},
            verification=self.verify(segment_paths),
            dependency=dependency,
            warnings=(
                EwfReaderWarning(
                    code="real_reader_not_implemented",
                    message="pyewf is importable, but real metadata extraction is deferred beyond S1-T03.",
                ),
            ),
        )

    def verify(self, segment_paths: Sequence[str | Path]) -> VerificationStatus:
        paths = _normalize_paths(segment_paths)
        if not self.is_available:
            return VerificationStatus(
                status="not_run",
                supported=False,
                message="Verification was not run because pyewf is unavailable.",
                details={"segment_count": len(paths)},
            )

        return VerificationStatus(
            status="not_run",
            supported=False,
            message="Verification is not implemented in the S1-T03 pyewf adapter skeleton.",
            details={"segment_count": len(paths)},
        )


def _normalize_paths(segment_paths: Sequence[str | Path]) -> tuple[str, ...]:
    return tuple(str(Path(path).expanduser().resolve(strict=False)) for path in segment_paths)
