"""Local backend API and command boundary package."""

from importlib import import_module

__all__ = ["INTAKE_SCHEMA_VERSION", "intake_to_json", "main", "run_e01_intake"]


def __getattr__(name: str):
    if name in __all__:
        intake_module = import_module("app.backend.api.intake")
        return getattr(intake_module, name)

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
