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

Stage 1 added the E01 intake foundation. Stage 2 added the first volume/filesystem browsing boundaries and backend API callables. Stage 3 added the fixture/stub export foundation with manifests, SHA-256/byte-count verification, optional explicit audit logging, and deleted-recovery limitations. The project remains backend-first and has no UI/executable packaging yet.

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

Current Stage 3 verification:

- `python -m pytest`: 99 passed in 4.42s for the final S3-T06 review run.
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
- Deleted-file recovery, carving, Stage 4 hash/signature analysis, search, reporting, UI, or executable packaging workflows.
- Automatic persistence from intake JSON or Stage 2 API results into SQLite.
- Required native forensic dependencies; `pyewf`, libewf, `pytsk3`, and The Sleuth Kit remain optional.

## Stage 3 Export Foundation

Implemented:

- Export result, manifest, content-source, source-provenance, status, warning, and hash-summary contract structures.
- `export_file(...)` for writing explicit export-provider bytes for Stage 2-style file entries or `ExportRequest` objects.
- `export_file_to_json(...)` for running export and serializing the returned result.
- `StubExportContentProvider`, which supplies synthetic `Hello, world!` bytes for `stub-file-hello`.
- Destination checks that require an explicit output directory, reject source/evidence overlap when known, reject unsafe output names, and refuse output/manifest overwrites.
- Manifest writing beside the exported artifact.
- SHA-256 and byte-count verification by reading the written output file after export.
- Optional `ExportAuditContext` for explicit case-store audit rows with `action="file_export"`.
- Deleted-file recovery documentation that keeps recovery unsupported/deferred until a real adapter exposes recoverable deleted-file bytes.

Current Stage 3 limits:

- Export bytes come only from explicit providers, not from filesystem metadata and not from preview-rendered text/hex.
- The default export provider is synthetic/stub-backed and does not prove real filesystem extraction.
- Export-output SHA-256 verifies the written artifact only; broader file hash/signature analysis remains Stage 4.
- No real EWF, partition, or filesystem parser is implemented.
- No real filesystem byte extraction, deleted-file recovery, carving, unallocated-space scanning, UI, search, timeline, reporting, bookmarks, notes, or packaging is implemented.
- Export audit rows require explicit `ExportAuditContext`; source provenance ids alone do not create case-store writes.

Stage 4 should build hash/signature contracts on explicit content providers, avoid hashing preview text/hex as source content, avoid whole-image verification claims without adapter support, and keep known-file matching plus persistence optional until result contracts are reviewed.
