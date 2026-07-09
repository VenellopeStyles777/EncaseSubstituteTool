"""Smoke tests for the Stage 1 backend package skeleton."""


def test_backend_package_imports():
    import app.backend as backend

    assert backend.PACKAGE_NAME == "encase_substitute_backend"
    assert backend.__version__ == "0.1.0"


def test_backend_subpackages_import():
    import app.backend.analysis_workers
    import app.backend.api
    import app.backend.case_store
    import app.backend.forensic_core

