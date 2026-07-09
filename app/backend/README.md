# Backend

Purpose: backend source root for forensic operations and local app services.

Subfolders:

- `forensic_core/`: evidence image adapters, segment discovery, read-only streams, hashing, signatures, filesystem interfaces.
- `case_store/`: SQLite schema, migrations, case metadata, evidence registry, audit events.
- `analysis_workers/`: background jobs for long-running forensic analysis.
- `api/`: local API or command boundary used by the UI.

## Python Package Skeleton

The backend package can be imported cleanly:

- `app.backend`
- `app.backend.forensic_core`
- `app.backend.case_store`
- `app.backend.analysis_workers`
- `app.backend.api`

Stage 1 added the E01 intake foundation. Stage 2 added the first volume/filesystem browsing boundaries and backend API callables. The project remains backend-first and has no UI/executable packaging yet.

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

Current Stage 2 verification on 2026-07-09:

- `python -m pytest`: 67 passed.
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

## Stage 2 Capabilities And Limits

Implemented:

- E01 segment discovery by filename and directory entry.
- EWF reader adapter contract, stub adapter, and pyewf dependency-unavailable result path.
- JSON intake command/callable.
- SQLite schema helpers for cases, evidence sources, and audit events.
- Read-only `LocalFileImageStream` for tiny local files and bounded byte reads.
- Whole-image volume discovery boundary for readable non-empty streams.
- Filesystem adapter contract, deterministic stub adapter entries, and `pytsk3` dependency-safe skeleton behavior.
- JSON-friendly directory listing/file metadata callable over adapter entries.
- JSON-friendly raw/text/hex preview callable over explicit provider bytes.

Current Stage 2 behavior categories:

- Real local-file backed: local byte-stream metadata and bounded reads from tiny generated files.
- Stubbed: filesystem entries and directory listing via `StubFilesystemAdapter`; `Pytsk3FilesystemAdapter` only reports dependency/unimplemented status.
- Synthetic preview-provider content: `StubPreviewProvider` supplies bytes for `/hello.txt`; preview does not extract bytes from a real filesystem.

Not implemented yet:

- Real EWF byte parsing or image verification.
- Real partition table parsing.
- Real filesystem parsing or real file extraction.
- Export/recovery, hashing, signature, search, reporting, UI, or executable packaging workflows.
- Automatic persistence from intake JSON or Stage 2 API results into SQLite.
- Required native forensic dependencies; `pyewf`, libewf, `pytsk3`, and The Sleuth Kit remain optional.
