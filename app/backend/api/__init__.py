"""Local backend API and command boundary package."""

from importlib import import_module

__all__ = [
    "DIRECTORY_LISTING_SCHEMA_VERSION",
    "FILE_PREVIEW_SCHEMA_VERSION",
    "INTAKE_SCHEMA_VERSION",
    "DEFAULT_MANIFEST_SUFFIX",
    "DirectoryBrowserSession",
    "ExportAuditContext",
    "ExportContent",
    "FIRST_TESTING_RUN_SCHEMA_VERSION",
    "StubExportContentProvider",
    "StubPreviewProvider",
    "directory_listing_to_json",
    "build_directory_browser_session",
    "directory_browser_to_summary",
    "export_file",
    "export_file_to_json",
    "first_testing_to_json",
    "format_first_testing_summary",
    "intake_to_json",
    "list_directory",
    "main",
    "preview_file",
    "preview_file_to_json",
    "run_e01_intake",
    "run_first_testing",
]


def __getattr__(name: str):
    if name in {"INTAKE_SCHEMA_VERSION", "intake_to_json", "main", "run_e01_intake"}:
        intake_module = import_module("app.backend.api.intake")
        return getattr(intake_module, name)

    if name in {
        "FIRST_TESTING_RUN_SCHEMA_VERSION",
        "first_testing_to_json",
        "format_first_testing_summary",
        "run_first_testing",
    }:
        first_testing_module = import_module("app.backend.api.first_testing")
        return getattr(first_testing_module, name)

    if name in {
        "DIRECTORY_LISTING_SCHEMA_VERSION",
        "directory_listing_to_json",
        "list_directory",
    }:
        listing_module = import_module("app.backend.api.directory_listing")
        return getattr(listing_module, name)

    if name in {
        "DirectoryBrowserSession",
        "build_directory_browser_session",
        "directory_browser_to_summary",
    }:
        browser_module = import_module("app.backend.api.directory_browser")
        return getattr(browser_module, name)

    if name in {
        "FILE_PREVIEW_SCHEMA_VERSION",
        "StubPreviewProvider",
        "preview_file",
        "preview_file_to_json",
    }:
        preview_module = import_module("app.backend.api.file_preview")
        return getattr(preview_module, name)

    if name in {
        "DEFAULT_MANIFEST_SUFFIX",
        "ExportAuditContext",
        "ExportContent",
        "StubExportContentProvider",
        "export_file",
        "export_file_to_json",
    }:
        export_module = import_module("app.backend.api.file_export")
        return getattr(export_module, name)

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
