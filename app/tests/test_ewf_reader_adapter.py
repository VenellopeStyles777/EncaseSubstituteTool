"""Tests for the S1-T03 EWF reader adapter boundary."""

from app.backend.forensic_core import (
    PyewfEwfReaderAdapter,
    StubEwfReaderAdapter,
)


class FakePyewf:
    __version__ = "fake-pyewf-1.0"

    def __init__(self, handle):
        self._handle = handle

    def handle(self):
        return self._handle


class FakeMetadataHandle:
    def __init__(self, *, verify_result=None, verify_error=None):
        self.opened_paths = None
        self.closed = False
        self._verify_result = verify_result
        self._verify_error = verify_error

    def open(self, paths):
        self.opened_paths = list(paths)

    def close(self):
        self.closed = True

    def get_media_size(self):
        return 4096

    def get_bytes_per_sector(self):
        return 512

    def get_header_values(self):
        return {
            "case_number": "CASE-001",
            "description": "Training image",
            "examiner": "Examiner",
            "evidence_number": "EV-7",
        }

    def get_acquiry_date(self):
        return "2026-07-01T01:02:03Z"

    def get_system_date(self):
        return "2026-07-01T04:05:06Z"

    def get_hash_values(self):
        return {"md5": "stored-md5"}

    def verify(self):
        if self._verify_error is not None:
            raise self._verify_error
        return self._verify_result


class PartialMetadataHandle(FakeMetadataHandle):
    def get_bytes_per_sector(self):
        raise RuntimeError("sector size unavailable")

    def get_header_values(self):
        raise RuntimeError("headers unavailable")


class OpenFailureHandle(FakeMetadataHandle):
    def open(self, paths):
        self.opened_paths = list(paths)
        raise RuntimeError("open failed")


class UnsupportedVerificationHandle(FakeMetadataHandle):
    verify = None


def test_stub_metadata_response_shape_without_real_evidence():
    adapter = StubEwfReaderAdapter()

    result = adapter.read_metadata(["missing-sample.E01", "missing-sample.E02"])
    result_dict = result.to_dict()

    assert result.adapter_name == "stub-ewf-reader"
    assert result.adapter_available is True
    assert result.read_only is True
    assert result.metadata["format"] == "EWF"
    assert result.metadata["reader"] == "stub"
    assert result.metadata["segment_count"] == 2
    assert result.verification.status == "not_supported"
    assert result.dependency.available is True
    assert result.warnings[0].code == "stub_metadata"
    assert result_dict["verification"]["status"] == "not_supported"
    assert result_dict["dependency"]["name"] == "stub"


def test_stub_verification_status_field_shape():
    status = StubEwfReaderAdapter().verify(["sample.E01"])
    status_dict = status.to_dict()

    assert status.status == "not_supported"
    assert status.supported is False
    assert status.message
    assert status.details["segment_count"] == 1
    assert set(status_dict) == {"status", "supported", "message", "details"}


def test_pyewf_dependency_unavailable_response_is_structured():
    adapter = PyewfEwfReaderAdapter(
        pyewf_module=None,
        import_error=ImportError("No module named 'pyewf'"),
    )

    result = adapter.read_metadata(["sample.E01"])

    assert adapter.is_available is False
    assert result.adapter_name == "pyewf-reader"
    assert result.adapter_available is False
    assert result.read_only is True
    assert result.metadata == {}
    assert result.dependency.name == "pyewf"
    assert result.dependency.available is False
    assert "pyewf is not installed" in result.dependency.message
    assert result.verification.status == "not_run"
    assert result.verification.supported is False
    assert result.warnings[0].code == "dependency_unavailable"


def test_pyewf_unavailable_path_does_not_require_real_evidence():
    adapter = PyewfEwfReaderAdapter(pyewf_module=None)

    result = adapter.read_metadata(["does-not-exist.E01"])

    assert result.source_paths[0].endswith("does-not-exist.E01")
    assert result.metadata == {}
    assert result.verification.details["segment_count"] == 1


def test_fake_pyewf_returns_normalized_metadata_and_closes_handle():
    handle = FakeMetadataHandle(verify_result=True)
    adapter = PyewfEwfReaderAdapter(pyewf_module=FakePyewf(handle))

    result = adapter.read_metadata(["sample.E01", "sample.E02"])

    assert result.adapter_available is True
    assert handle.closed is True
    assert result.metadata["format"] == "EWF"
    assert result.metadata["segment_count"] == 2
    assert result.metadata["media_size"] == 4096
    assert result.metadata["bytes_per_sector"] == 512
    assert result.metadata["case_number"] == "CASE-001"
    assert result.metadata["description"] == "Training image"
    assert result.metadata["examiner"] == "Examiner"
    assert result.metadata["evidence_number"] == "EV-7"
    assert result.metadata["acquired_date"] == "2026-07-01T01:02:03Z"
    assert result.metadata["system_date"] == "2026-07-01T04:05:06Z"
    assert result.metadata["hashes"]["md5"] == "stored-md5"
    assert result.metadata["reader"]["version"] == "fake-pyewf-1.0"
    assert result.verification.status == "verification_ok"
    assert "stored_hash_not_verified" in _warning_codes(result)
    assert "metadata_partial" not in _warning_codes(result)


def test_fake_pyewf_partial_metadata_returns_warnings_and_metadata():
    handle = PartialMetadataHandle(verify_result=True)
    adapter = PyewfEwfReaderAdapter(pyewf_module=FakePyewf(handle))

    result = adapter.read_metadata(["sample.E01"])

    assert result.metadata["media_size"] == 4096
    assert "bytes_per_sector" not in result.metadata
    assert result.verification.status == "verification_ok"
    assert "metadata_field_unavailable" in _warning_codes(result)
    assert "metadata_partial" in _warning_codes(result)


def test_fake_pyewf_open_failure_is_structured_and_closes_handle():
    handle = OpenFailureHandle(verify_result=True)
    adapter = PyewfEwfReaderAdapter(pyewf_module=FakePyewf(handle))

    result = adapter.read_metadata(["sample.E01"])

    assert handle.closed is True
    assert result.metadata == {}
    assert result.verification.status == "not_run"
    assert "reader_open_failed" in _warning_codes(result)


def test_stored_hash_metadata_does_not_verify_evidence():
    handle = UnsupportedVerificationHandle()
    adapter = PyewfEwfReaderAdapter(pyewf_module=FakePyewf(handle))

    result = adapter.read_metadata(["sample.E01"])

    assert result.metadata["hashes"]["md5"] == "stored-md5"
    assert result.verification.status == "not_supported"
    assert result.verification.status != "verification_ok"
    assert "stored_hash_not_verified" in _warning_codes(result)
    assert "verification_not_supported" in _warning_codes(result)
    assert "metadata_partial" not in _warning_codes(result)


def test_fake_pyewf_verification_success_failure_exception_and_unsupported():
    success = PyewfEwfReaderAdapter(
        pyewf_module=FakePyewf(FakeMetadataHandle(verify_result=True))
    ).read_metadata(["sample.E01"])
    failure = PyewfEwfReaderAdapter(
        pyewf_module=FakePyewf(FakeMetadataHandle(verify_result=False))
    ).read_metadata(["sample.E01"])
    exception = PyewfEwfReaderAdapter(
        pyewf_module=FakePyewf(
            FakeMetadataHandle(verify_error=RuntimeError("verify broke"))
        )
    ).read_metadata(["sample.E01"])
    unsupported = PyewfEwfReaderAdapter(
        pyewf_module=FakePyewf(UnsupportedVerificationHandle())
    ).read_metadata(["sample.E01"])

    assert success.verification.status == "verification_ok"
    assert failure.verification.status == "verification_failed"
    assert "verification_failed" in _warning_codes(failure)
    assert exception.verification.status == "verification_error"
    assert "verification_error" in _warning_codes(exception)
    assert unsupported.verification.status == "not_supported"
    assert "verification_not_supported" in _warning_codes(unsupported)


def _warning_codes(result):
    return [warning.code for warning in result.warnings]
