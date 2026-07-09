# Tests

Purpose: automated tests for the app.

Stage 1 tests should cover:

- E01 segment discovery.
- Unsupported input handling.
- Missing segment warnings.
- Dependency-unavailable behavior.
- Metadata response shape.

## Temporary Test Files

Pytest is configured in `pyproject.toml` to use `.test-artifacts/pytest-temp` as its base temporary directory and to disable pytest's optional cache provider. This avoids local Windows temp-directory and pytest cache permission issues observed during S1-T02.

`.test-artifacts/` is ignored by Git and may be deleted at any time.
