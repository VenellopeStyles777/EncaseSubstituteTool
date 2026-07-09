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

Current Stage 1 verification on 2026-07-09:

- `python -m pytest`: 22 passed.
- The project config routes pytest temporary files to `.test-artifacts/pytest-temp` and disables pytest's optional cache provider.

## Stage 1 Intake Command

Run the current backend intake command from the repository root:

```powershell
python -m app.backend.api.intake path\to\sample.E01
```

The default adapter is dependency-safe: if `pyewf` is unavailable, the command returns JSON describing the unavailable dependency instead of crashing. For tests or synthetic smoke checks, use the stub adapter:

```powershell
python -m app.backend.api.intake path\to\sample.E01 --adapter stub
```

The command does not write to evidence files. It composes segment discovery with the EWF reader adapter boundary and prints JSON for later UI integration.

## Stage 1 Capabilities And Limits

Implemented:

- E01 segment discovery by filename and directory entry.
- EWF reader adapter contract, stub adapter, and pyewf dependency-unavailable result path.
- JSON intake command/callable.
- SQLite schema helpers for cases, evidence sources, and audit events.

Not implemented yet:

- Real EWF byte parsing or image verification.
- Filesystem, partition, export/recovery, hashing, signature, search, reporting, or UI workflows.
- Automatic persistence from intake JSON into SQLite.
