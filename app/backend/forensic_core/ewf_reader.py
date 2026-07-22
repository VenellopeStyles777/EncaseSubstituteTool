"""EWF reader adapter contracts and dependency-free implementations."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Protocol, Sequence


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
    """Optional pyewf adapter with graceful dependency handling."""

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
            message="pyewf is available; real metadata and verification are attempted on a best-effort read-only basis.",
            version=_pyewf_version(self._pyewf),
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

        warnings: list[EwfReaderWarning] = []
        if dependency.version is None:
            warnings.append(
                EwfReaderWarning(
                    code="dependency_version_unknown",
                    message="pyewf is importable, but no version string was exposed.",
                )
            )

        handle: object | None = None
        try:
            handle = self._open_handle(paths)
        except Exception as error:
            return EwfMetadataResult(
                adapter_name=self.name,
                adapter_available=True,
                read_only=self.read_only,
                source_paths=paths,
                metadata={},
                verification=VerificationStatus(
                    status="not_run",
                    supported=False,
                    message="Verification was not run because the EWF reader could not open the segment set.",
                    details={"segment_count": len(paths), "error": str(error)},
                ),
                dependency=dependency,
                warnings=tuple(
                    warnings
                    + [
                        EwfReaderWarning(
                            code="reader_open_failed",
                            message=f"pyewf could not open the supplied segment set: {error}",
                        )
                    ]
                ),
            )

        try:
            metadata, metadata_warnings = _extract_metadata(handle, paths, dependency)
            warnings.extend(metadata_warnings)
            verification, verification_warnings = _verify_with_open_handle(handle, paths)
            warnings.extend(verification_warnings)
            return EwfMetadataResult(
                adapter_name=self.name,
                adapter_available=True,
                read_only=self.read_only,
                source_paths=paths,
                metadata=metadata,
                verification=verification,
                dependency=dependency,
                warnings=tuple(warnings),
            )
        finally:
            _close_handle(handle)

    def verify(self, segment_paths: Sequence[str | Path]) -> VerificationStatus:
        paths = _normalize_paths(segment_paths)
        if not self.is_available:
            return VerificationStatus(
                status="not_run",
                supported=False,
                message="Verification was not run because pyewf is unavailable.",
                details={"segment_count": len(paths)},
            )

        handle: object | None = None
        try:
            handle = self._open_handle(paths)
        except Exception as error:
            return VerificationStatus(
                status="verification_error",
                supported=True,
                message="Verification could not open the EWF segment set.",
                details={"segment_count": len(paths), "error": str(error)},
            )

        try:
            verification, _warnings = _verify_with_open_handle(handle, paths)
            return verification
        finally:
            _close_handle(handle)

    def _open_handle(self, paths: Sequence[str]) -> object:
        handle_factory = getattr(self._pyewf, "handle", None)
        if handle_factory is None or not callable(handle_factory):
            raise RuntimeError("pyewf.handle is unavailable")

        handle = handle_factory()
        open_method = getattr(handle, "open", None)
        if open_method is None or not callable(open_method):
            _close_handle(handle)
            raise RuntimeError("pyewf handle does not expose open()")

        try:
            open_method(list(paths))
        except Exception:
            _close_handle(handle)
            raise
        return handle


def _normalize_paths(segment_paths: Sequence[str | Path]) -> tuple[str, ...]:
    return tuple(str(Path(path).expanduser().resolve(strict=False)) for path in segment_paths)


def _pyewf_version(pyewf_module: object | None) -> str | None:
    if pyewf_module is None:
        return None
    version = getattr(pyewf_module, "__version__", None)
    if version is not None:
        return str(version)
    get_version = getattr(pyewf_module, "get_version", None)
    if callable(get_version):
        try:
            return str(get_version())
        except Exception:
            return None
    return None


def _extract_metadata(
    handle: object,
    paths: Sequence[str],
    dependency: ReaderDependencyStatus,
) -> tuple[dict[str, object], list[EwfReaderWarning]]:
    warnings: list[EwfReaderWarning] = []
    metadata: dict[str, object] = {
        "format": "EWF",
        "segment_count": len(paths),
        "reader": {
            "name": "pyewf",
            "version": dependency.version,
        },
    }

    media_size, media_warning = _optional_value(
        handle,
        "media_size",
        ("get_media_size",),
        ("media_size",),
    )
    if media_warning is not None:
        warnings.append(media_warning)
    elif media_size is not None:
        metadata["media_size"] = media_size

    bytes_per_sector, sector_warning = _optional_value(
        handle,
        "bytes_per_sector",
        ("get_bytes_per_sector",),
        ("bytes_per_sector",),
    )
    if sector_warning is not None:
        warnings.append(sector_warning)
    elif bytes_per_sector is not None:
        metadata["bytes_per_sector"] = bytes_per_sector

    headers, header_warnings = _header_values(handle)
    warnings.extend(header_warnings)
    _copy_header(metadata, headers, "case_number", ("case_number", "case number", "case"))
    _copy_header(metadata, headers, "description", ("description", "description_text", "notes"))
    _copy_header(metadata, headers, "examiner", ("examiner", "examiner_name"))
    _copy_header(metadata, headers, "evidence_number", ("evidence_number", "evidence number"))

    acquired_date, acquired_warning = _optional_value(
        handle,
        "acquired_date",
        ("get_acquiry_date", "get_acquired_date"),
        ("acquired_date", "acquiry_date"),
    )
    if acquired_warning is not None:
        warnings.append(acquired_warning)
    elif acquired_date is not None:
        metadata["acquired_date"] = acquired_date

    system_date, system_warning = _optional_value(
        handle,
        "system_date",
        ("get_system_date",),
        ("system_date",),
    )
    if system_warning is not None:
        warnings.append(system_warning)
    elif system_date is not None:
        metadata["system_date"] = system_date

    hashes, hash_warnings = _hash_values(handle)
    warnings.extend(hash_warnings)
    if hashes:
        metadata["hashes"] = hashes
        warnings.append(
            EwfReaderWarning(
                code="stored_hash_not_verified",
                message="Stored EWF hash values were read as metadata only; they are not verification success.",
            )
        )

    if any(warning.code == "metadata_field_unavailable" for warning in warnings):
        warnings.append(
            EwfReaderWarning(
                code="metadata_partial",
                message="Some optional pyewf metadata fields were unavailable or failed to read.",
            )
        )

    return metadata, warnings


def _optional_value(
    handle: object,
    field_name: str,
    method_names: Sequence[str],
    attribute_names: Sequence[str],
) -> tuple[object | None, EwfReaderWarning | None]:
    for method_name in method_names:
        method = getattr(handle, method_name, None)
        if callable(method):
            try:
                return _json_safe(method()), None
            except Exception as error:
                return None, EwfReaderWarning(
                    code="metadata_field_unavailable",
                    message=f"pyewf metadata field {field_name!r} failed via {method_name}(): {error}",
                )

    for attribute_name in attribute_names:
        if hasattr(handle, attribute_name):
            try:
                return _json_safe(getattr(handle, attribute_name)), None
            except Exception as error:
                return None, EwfReaderWarning(
                    code="metadata_field_unavailable",
                    message=f"pyewf metadata field {field_name!r} failed via attribute {attribute_name!r}: {error}",
                )

    return None, EwfReaderWarning(
        code="metadata_field_unavailable",
        message=f"pyewf metadata field {field_name!r} is not exposed by this reader.",
    )


def _header_values(handle: object) -> tuple[dict[str, object], list[EwfReaderWarning]]:
    get_header_values = getattr(handle, "get_header_values", None)
    if not callable(get_header_values):
        return {}, [
            EwfReaderWarning(
                code="metadata_field_unavailable",
                message="pyewf header metadata is not exposed by this reader.",
            )
        ]

    try:
        raw_headers = get_header_values()
    except Exception as error:
        return {}, [
            EwfReaderWarning(
                code="metadata_field_unavailable",
                message=f"pyewf header metadata failed to read: {error}",
            )
        ]

    if not isinstance(raw_headers, Mapping):
        return {}, [
            EwfReaderWarning(
                code="metadata_field_unavailable",
                message="pyewf header metadata did not return a mapping.",
            )
        ]

    return {
        _normalize_metadata_key(str(key)): _json_safe(value)
        for key, value in raw_headers.items()
    }, []


def _copy_header(
    metadata: dict[str, object],
    headers: Mapping[str, object],
    target_key: str,
    source_keys: Sequence[str],
) -> None:
    for source_key in source_keys:
        normalized = _normalize_metadata_key(source_key)
        value = headers.get(normalized)
        if value is not None and value != "":
            metadata[target_key] = value
            return


def _hash_values(handle: object) -> tuple[dict[str, object], list[EwfReaderWarning]]:
    warnings: list[EwfReaderWarning] = []
    hashes: dict[str, object] = {}

    get_hash_values = getattr(handle, "get_hash_values", None)
    if callable(get_hash_values):
        try:
            raw_hashes = get_hash_values()
        except Exception as error:
            warnings.append(
                EwfReaderWarning(
                    code="metadata_field_unavailable",
                    message=f"pyewf stored hash metadata failed to read: {error}",
                )
            )
        else:
            if isinstance(raw_hashes, Mapping):
                hashes.update(
                    {
                        _normalize_metadata_key(str(key)): _json_safe(value)
                        for key, value in raw_hashes.items()
                    }
                )

    for key, method_name in (
        ("md5", "get_stored_md5_hash"),
        ("sha1", "get_stored_sha1_hash"),
        ("sha256", "get_stored_sha256_hash"),
    ):
        method = getattr(handle, method_name, None)
        if callable(method):
            try:
                value = method()
            except Exception as error:
                warnings.append(
                    EwfReaderWarning(
                        code="metadata_field_unavailable",
                        message=f"pyewf stored {key} hash metadata failed to read: {error}",
                    )
                )
            else:
                if value not in {None, ""}:
                    hashes[key] = _json_safe(value)

    return hashes, warnings


def _verify_with_open_handle(
    handle: object,
    paths: Sequence[str],
) -> tuple[VerificationStatus, list[EwfReaderWarning]]:
    for method_name in ("verify", "verify_media", "check_media", "verify_hashes"):
        method = getattr(handle, method_name, None)
        if not callable(method):
            continue

        try:
            raw_result = method()
        except Exception as error:
            return (
                VerificationStatus(
                    status="verification_error",
                    supported=True,
                    message=f"pyewf verification raised an error via {method_name}().",
                    details={
                        "segment_count": len(paths),
                        "method": method_name,
                        "error": str(error),
                    },
                ),
                [
                    EwfReaderWarning(
                        code="verification_error",
                        message=f"pyewf verification raised an error via {method_name}(): {error}",
                    )
                ],
            )

        status, supported, message, details, warnings = _verification_from_result(
            raw_result,
            method_name=method_name,
            segment_count=len(paths),
        )
        return (
            VerificationStatus(
                status=status,
                supported=supported,
                message=message,
                details=details,
            ),
            warnings,
        )

    return (
        VerificationStatus(
            status="not_supported",
            supported=False,
            message="The available pyewf reader does not expose a supported verification method.",
            details={"segment_count": len(paths)},
        ),
        [
            EwfReaderWarning(
                code="verification_not_supported",
                message="No safe pyewf verification method was exposed by this reader.",
            )
        ],
    )


def _verification_from_result(
    raw_result: object,
    *,
    method_name: str,
    segment_count: int,
) -> tuple[str, bool, str, dict[str, object], list[EwfReaderWarning]]:
    details = {
        "segment_count": segment_count,
        "method": method_name,
        "raw_result": _json_safe(raw_result),
    }
    warnings: list[EwfReaderWarning] = []

    status_value: object = raw_result
    if isinstance(raw_result, Mapping):
        status_value = (
            raw_result.get("status")
            or raw_result.get("result")
            or raw_result.get("verified")
            or raw_result.get("ok")
            or raw_result.get("passed")
        )

    if isinstance(status_value, str):
        normalized = status_value.strip().lower().replace("-", "_").replace(" ", "_")
        if normalized in {"verification_ok", "ok", "true", "passed", "pass", "verified", "success"}:
            return "verification_ok", True, "pyewf verification completed successfully.", details, warnings
        if normalized in {"verification_failed", "failed", "fail", "false", "mismatch"}:
            warnings.append(
                EwfReaderWarning(
                    code="verification_failed",
                    message="pyewf verification ran and reported failure.",
                )
            )
            return "verification_failed", True, "pyewf verification ran and reported failure.", details, warnings
        if normalized in {"verification_partial", "partial", "incomplete"}:
            warnings.append(
                EwfReaderWarning(
                    code="verification_partial",
                    message="pyewf verification returned a partial result.",
                )
            )
            return "verification_partial", True, "pyewf verification returned a partial result.", details, warnings

    if status_value is True:
        return "verification_ok", True, "pyewf verification completed successfully.", details, warnings
    if status_value is False:
        warnings.append(
            EwfReaderWarning(
                code="verification_failed",
                message="pyewf verification ran and reported failure.",
            )
        )
        return "verification_failed", True, "pyewf verification ran and reported failure.", details, warnings

    warnings.append(
        EwfReaderWarning(
            code="verification_error",
            message="pyewf verification returned an unsupported result shape.",
        )
    )
    return (
        "verification_error",
        True,
        "pyewf verification returned an unsupported result shape.",
        details,
        warnings,
    )


def _close_handle(handle: object | None) -> None:
    if handle is None:
        return
    close = getattr(handle, "close", None)
    if callable(close):
        close()


def _normalize_metadata_key(key: str) -> str:
    return key.strip().lower().replace(" ", "_").replace("-", "_")


def _json_safe(value: object) -> object:
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, Mapping):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_safe(item) for item in value]
    return str(value)
