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

Stage 1 added the E01 intake foundation. Stage 2 added the first volume/filesystem browsing boundaries and backend API callables. Stage 3 added the fixture/stub export foundation with manifests, SHA-256/byte-count verification, optional explicit audit logging, and deleted-recovery limitations. Stage 4 now has hash/signature analysis result contracts, provider-backed hash calculation, bounded provider-backed file signature detection over explicit analysis content providers, and extension mismatch evaluation over reviewed signature results plus file metadata. The project remains backend-first and has no UI/executable packaging yet.

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

Current verification snapshot:

- `python -m pytest`: 140 passed in 4.99s after the S4-T04 extension mismatch implementation handoff.
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
- Deleted-file recovery, carving, search, reporting, UI, or executable packaging workflows.
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

## Stage 4 Hash And Signature Analysis Foundation

Implemented so far:

- `app.backend.forensic_core.content_analysis` defines contract-only hash/signature analysis request/result/status/warning/source-provenance/content-source structures.
- The contracts distinguish source kinds such as `synthetic`, `generated_fixture`, `local_stream`, `export_provider`, and future `real_parser`.
- `hash_file_content(...)` and `calculate_hashes(...)` compute hashes from explicit Stage 4 analysis-provider bytes only.
- `StubAnalysisContentProvider` supplies dependency-free synthetic/generated test bytes through a Stage 4 analysis provider that is separate from preview and export providers.
- SHA-256 is computed by default; MD5 and SHA-1 are computed only when explicitly requested as comparison hashes.
- Unsupported, empty, malformed, directory/non-file, metadata-only, missing-content, and provider-exception paths return structured non-ok `HashAnalysisResult` objects.
- `detect_file_signature(...)` and `analyze_file_signature(...)` inspect bounded prefixes from explicit Stage 4 analysis-provider bytes only.
- The supported dependency-free signature table covers PDF, PNG, JPEG, GIF87a/GIF89a, ZIP header variants, ELF, and conservative MZ executable candidates.
- Invalid max-byte, directory/non-file, metadata-only, missing-content, provider-exception, insufficient partial-signature, and unknown-signature paths return structured non-ok `SignatureAnalysisResult` objects.
- `evaluate_extension_mismatch(...)` and `check_extension_mismatch(...)` compare reviewed `SignatureAnalysisResult` fields with file name/path metadata only.
- Extension mismatch results preserve source provenance, content-source identity, signature status and detected fields, observed and expected extensions, explicit `mismatch` values, timestamps, and warnings.
- Unknown, insufficient, failed, unsupported, missing-name, no-extension, and non-file states return structured not-evaluated results with `mismatch=None`.

Stage 4 must continue to analyze only explicit content providers for hashing/signature detection, avoid hashing or signature-checking preview text/hex or export artifacts as source analysis content, avoid whole-image verification claims without adapter support, and keep known-file matching, persistence, search/timeline, and UI work for later reviewed tickets.
