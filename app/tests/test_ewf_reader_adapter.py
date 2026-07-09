"""Tests for the S1-T03 EWF reader adapter boundary."""

from app.backend.forensic_core import (
    PyewfEwfReaderAdapter,
    StubEwfReaderAdapter,
)


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
