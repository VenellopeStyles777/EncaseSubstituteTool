"""Tests for the S2-T06 raw/text/hex preview foundation."""

import json

from app.backend.api.file_preview import (
    FILE_PREVIEW_SCHEMA_VERSION,
    StubPreviewProvider,
    preview_file,
    preview_file_to_json,
)


def _stub_file_entry() -> dict[str, object]:
    return {
        "file_id": "stub-file-hello",
        "path": "/hello.txt",
        "name": "hello.txt",
        "entry_type": "file",
        "size": 13,
        "allocated": True,
        "deleted": False,
        "source_path": "C:/fixtures/tiny.raw",
        "volume_id": "volume-0",
        "volume_offset": 0,
        "volume_length": 1024,
        "filesystem_type": "stubfs",
        "adapter_name": "stub-filesystem-adapter",
        "read_only": True,
        "timestamps": {
            "created": None,
            "modified": None,
            "accessed": None,
            "metadata_changed": None,
        },
    }


def _stub_directory_entry() -> dict[str, object]:
    entry = _stub_file_entry()
    entry.update(
        {
            "file_id": "stub-dir-documents",
            "path": "/Documents",
            "name": "Documents",
            "entry_type": "directory",
            "size": 0,
        }
    )
    return entry


def test_text_preview_for_known_stub_content():
    result = preview_file(_stub_file_entry(), mode="text")

    assert result["schema_version"] == FILE_PREVIEW_SCHEMA_VERSION
    assert result["status"]["code"] == "ok"
    assert result["mode"] == "text"
    assert result["preview"]["text"] == "Hello, world!"
    assert result["returned_bytes"] == 13
    assert result["source_content_size"] == 13
    assert result["truncated"] is False


def test_hex_preview_for_known_stub_content():
    result = preview_file(_stub_file_entry(), mode="hex")

    assert result["status"]["code"] == "ok"
    assert result["preview"]["hex"] == "48656c6c6f2c20776f726c6421"
    assert result["returned_bytes"] == 13


def test_raw_preview_is_json_serializable():
    parsed = json.loads(preview_file_to_json(_stub_file_entry(), mode="raw"))

    assert parsed["schema_version"] == FILE_PREVIEW_SCHEMA_VERSION
    assert parsed["status"]["code"] == "ok"
    assert parsed["preview"]["byte_values"] == [
        72,
        101,
        108,
        108,
        111,
        44,
        32,
        119,
        111,
        114,
        108,
        100,
        33,
    ]


def test_preview_offset_and_length_are_bounded():
    result = preview_file(_stub_file_entry(), mode="text", offset=7, length=5)

    assert result["status"]["code"] == "ok"
    assert result["requested_offset"] == 7
    assert result["requested_length"] == 5
    assert result["returned_bytes"] == 5
    assert result["preview"]["text"] == "world"


def test_preview_truncates_when_request_exceeds_max_length():
    result = preview_file(
        _stub_file_entry(),
        mode="text",
        offset=0,
        length=13,
        max_length=5,
    )

    assert result["status"]["code"] == "preview_truncated"
    assert result["truncated"] is True
    assert result["returned_bytes"] == 5
    assert result["preview"]["text"] == "Hello"
    assert "preview_truncated" in [warning["code"] for warning in result["warnings"]]


def test_preview_truncates_when_request_exceeds_content_size():
    result = preview_file(_stub_file_entry(), mode="text", offset=7, length=20)

    assert result["status"]["code"] == "preview_truncated"
    assert result["truncated"] is True
    assert result["returned_bytes"] == 6
    assert result["preview"]["text"] == "world!"


def test_preview_offset_beyond_content_size_returns_structured_status():
    result = preview_file(_stub_file_entry(), mode="text", offset=99)

    assert result["status"]["code"] == "content_unavailable"
    assert result["status"]["ok"] is False
    assert result["requested_offset"] == 99
    assert result["requested_length"] is None
    assert result["source_content_size"] == 13
    assert result["returned_bytes"] == 0
    assert result["truncated"] is False
    assert result["preview"] is None
    assert result["read_only"] is True
    assert "content_unavailable" in [
        warning["code"] for warning in result["warnings"]
    ]


def test_missing_file_content_returns_structured_status():
    entry = _stub_file_entry()
    entry["file_id"] = "missing-file"
    entry["path"] = "/missing.txt"

    result = preview_file(entry, mode="text")

    assert result["status"]["code"] == "file_not_found"
    assert result["preview"] is None
    assert result["returned_bytes"] == 0
    assert result["warnings"][0]["code"] == "file_not_found"


def test_directory_entry_returns_path_not_file():
    result = preview_file(_stub_directory_entry(), mode="text")

    assert result["status"]["code"] == "path_not_file"
    assert result["preview"] is None
    assert result["warnings"][0]["code"] == "path_not_file"


def test_unsupported_preview_mode_returns_structured_status():
    result = preview_file(_stub_file_entry(), mode="html")

    assert result["status"]["code"] == "unsupported_preview_mode"
    assert result["preview"] is None
    assert result["warnings"][0]["code"] == "unsupported_preview_mode"


def test_invalid_negative_offset_returns_structured_status():
    result = preview_file(_stub_file_entry(), mode="text", offset=-1)

    assert result["status"]["code"] == "invalid_range"
    assert result["preview"] is None
    assert result["warnings"][0]["code"] == "invalid_range"


def test_invalid_negative_length_returns_structured_status():
    result = preview_file(_stub_file_entry(), mode="text", length=-1)

    assert result["status"]["code"] == "invalid_range"
    assert result["preview"] is None
    assert result["warnings"][0]["code"] == "invalid_range"


def test_text_preview_decode_replacement_is_visible():
    provider = StubPreviewProvider({"stub-file-hello": b"bad:\xff"})

    result = preview_file(_stub_file_entry(), mode="text", provider=provider)

    assert result["status"]["code"] == "ok"
    assert result["preview"]["text"] == "bad:\ufffd"
    assert "text_decode_replacement" in [
        warning["code"] for warning in result["warnings"]
    ]


def test_preview_preserves_provenance_and_read_only_fields():
    entry = _stub_file_entry()

    result = preview_file(entry, mode="text")

    assert result["source_path"] == entry["source_path"]
    assert result["volume_id"] == entry["volume_id"]
    assert result["volume_offset"] == entry["volume_offset"]
    assert result["volume_length"] == entry["volume_length"]
    assert result["file_id"] == entry["file_id"]
    assert result["file_path"] == entry["path"]
    assert result["file_name"] == entry["name"]
    assert result["entry_type"] == "file"
    assert result["read_only"] is True
    assert result["provider"]["name"] == "stub-preview-provider"
    assert result["provider"]["read_only"] is True
    assert "stub_preview_content" in [
        warning["code"] for warning in result["warnings"]
    ]
