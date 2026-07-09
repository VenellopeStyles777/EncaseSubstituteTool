# Backend

Purpose: backend source root for forensic operations and local app services.

Subfolders:

- `forensic_core/`: evidence image adapters, segment discovery, read-only streams, hashing, signatures, filesystem interfaces.
- `case_store/`: SQLite schema, migrations, case metadata, evidence registry, audit events.
- `analysis_workers/`: background jobs for long-running forensic analysis.
- `api/`: local API or command boundary used by the UI.

## Python Package Skeleton

Stage 1 ticket S1-T01 adds minimal Python package files so backend modules can be imported cleanly:

- `app.backend`
- `app.backend.forensic_core`
- `app.backend.case_store`
- `app.backend.analysis_workers`
- `app.backend.api`

No E01 parsing or evidence access is implemented in this ticket.

## Tests

Prerequisite: install Python 3.11 or newer and make sure `python` is available on `PATH`. On Windows, the Microsoft Store app execution alias is not enough for this project because it does not provide a real interpreter.

Run the smoke tests from the repository root:

```powershell
python -m pytest
```

If `pytest` is not installed:

```powershell
python -m pip install pytest
```

Current S1-T01A verification on 2026-07-09:

- `python -m pytest`: 2 passed, 1 warning.
- Warning: pytest could not create/update a path under `.pytest_cache`; this is a non-blocking local cache issue when tests still pass.
