"""Local backend API and command boundary package."""

from importlib import import_module

__all__ = [
    "DIRECTORY_LISTING_SCHEMA_VERSION",
    "INTAKE_SCHEMA_VERSION",
    "directory_listing_to_json",
    "intake_to_json",
    "list_directory",
    "main",
    "run_e01_intake",
]


def __getattr__(name: str):
    if name in {"INTAKE_SCHEMA_VERSION", "intake_to_json", "main", "run_e01_intake"}:
        intake_module = import_module("app.backend.api.intake")
        return getattr(intake_module, name)

    if name in {
        "DIRECTORY_LISTING_SCHEMA_VERSION",
        "directory_listing_to_json",
        "list_directory",
    }:
        listing_module = import_module("app.backend.api.directory_listing")
        return getattr(listing_module, name)

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
