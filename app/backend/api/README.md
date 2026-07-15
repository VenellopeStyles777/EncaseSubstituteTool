# Backend API

Purpose: local command/API boundary between backend logic and the future UI.

Current Stage 2 API surface:

- E01 intake command/callable from Stage 1.
- Directory listing/file metadata callable over the Stage 2 filesystem adapter boundary.
- Raw/text/hex preview callable over explicit preview-provider bytes.
- Fixture/stub file export callable over an explicit export content provider.

These callables are backend-only and JSON-friendly. They do not provide UI, executable packaging, broader hash/signature analysis, search, reporting, real EWF byte parsing, real partition parsing, real filesystem parsing, deleted recovery, or automatic case-store persistence.

Stage 3 note: S3-T04 can optionally record export attempts in the case-store audit log when the caller supplies explicit audit context. It does not recover deleted files, parse real filesystems, run broader hash/signature analysis, or use preview-rendered text/hex as export bytes.

Stage 4 note: S4-T01 adds hash/signature analysis contracts in `app.backend.forensic_core.content_analysis`, S4-T02 adds provider-backed hash calculation in that core module, S4-T03 adds bounded provider-backed file signature detection there, S4-T04 adds extension mismatch evaluation over reviewed signature results plus file metadata, and S4-T05 adds fixture-sized known-file matching over reviewed hash results plus caller-supplied in-memory records. S4-T06 documents that analysis-result persistence is deferred and must be explicit opt-in in a later workflow/API/job layer. S4-T07 is a documentation/review handoff only. There is still no API callable/wrapper for hash, signature, mismatch, known-file, or analysis-result persistence. Preview-rendered text/hex, preview providers, export providers, written export artifacts, and external known-file lists remain disallowed as implicit source analysis content.

## S1-T04 Intake Command

Callable usage from Python:

```python
from app.backend.api import run_e01_intake
from app.backend.forensic_core import StubEwfReaderAdapter

result = run_e01_intake("sample.E01", StubEwfReaderAdapter())
```

Command-line usage from the repository root:

```powershell
python -m app.backend.api.intake path\to\sample.E01
```

By default, the CLI uses the optional `pyewf` adapter and returns structured dependency-unavailable JSON if `pyewf` is not installed. For dependency-free smoke checks with synthetic metadata:

```powershell
python -m app.backend.api.intake path\to\sample.E01 --adapter stub
```

Normal invalid input, such as selecting a non-`.E01` path, prints structured JSON and exits with code `2` rather than a raw traceback.

Current status values include:

- `ok`: stub-backed intake completed with synthetic metadata.
- `metadata_unavailable`: adapter dependency is unavailable, such as missing `pyewf`.
- `reader_not_implemented`: adapter dependency is importable, but real metadata extraction is not implemented yet.
- `invalid_input`: selected path is missing or not a valid `.E01` first segment.
- `reader_error`: unexpected adapter exception caught at the command boundary.

S1-T04 does not persist results automatically. Use the case-store helpers explicitly when a case workflow is ready.

## S2-T05 Directory Listing Callable

Callable usage from Python:

```python
from app.backend.api import list_directory
from app.backend.forensic_core import StubFilesystemAdapter

result = list_directory(volume, "/", StubFilesystemAdapter())
```

`list_directory()` consumes a `VolumeInfo` and a filesystem adapter. It returns a JSON-friendly dictionary with:

- schema version and structured listing status;
- directory path;
- source path, volume id, volume offset/length, filesystem type, adapter/dependency details, and read-only assertion;
- file/directory entries from the filesystem adapter, including file id, path, name, type, size, timestamps, allocation/deleted state, status/warnings, and provenance;
- adapter/listing warnings.

Current S2-T05 behavior:

- root listing with `StubFilesystemAdapter` returns deterministic entries for `/Documents` and `/hello.txt`;
- empty path normalizes to `/`, and paths without a leading slash are normalized with one;
- nested directory paths such as `/Documents` return `path_unsupported`;
- file paths such as `/hello.txt` return `path_not_directory`;
- missing paths return `path_not_found`;
- dependency-unavailable or not-implemented adapters return `filesystem_unavailable`.

S2-T05 does not read file content, render raw/text/hex preview, export files, hash files, persist case-store data, parse real filesystems, or require `pytsk3`/The Sleuth Kit.

## S2-T06 Raw/Text/Hex Preview Callable

Callable usage from Python:

```python
from app.backend.api import preview_file

result = preview_file(entry, mode="text")
```

`preview_file()` consumes a file-entry metadata dictionary and an explicit preview content provider. The default `StubPreviewProvider` provides synthetic bytes for the S2-T04/S2-T05 stub file `stub-file-hello` (`/hello.txt`) only. This is not real evidence byte extraction.

The response is JSON-friendly and includes:

- schema version and structured preview status;
- mode: `raw`, `text`, or `hex`;
- source path, volume id, volume offset/length, file id/path/name/type, and read-only assertion;
- requested offset/length, returned byte count, source content size, truncation flag, and warnings;
- provider name/read-only assertion;
- preview data as byte values for raw mode, decoded text for text mode, or lowercase hex for hex mode.

Current S2-T06 behavior:

- enforces bounded previews through `max_length`;
- returns `preview_truncated` when the request exceeds the configured limit or available content;
- returns `content_unavailable` when the requested offset is beyond available provider content;
- returns structured statuses for missing content, non-file entries, unsupported modes, and invalid ranges;
- uses UTF-8 text decoding with visible replacement warnings for undecodable bytes.

S2-T06 does not perform real filesystem byte extraction, parse evidence/filesystems, export files, hash files, write output, persist case-store data, or require native forensic dependencies.

## S3-T01 Export Contract Note

Export contracts now exist in `app.backend.forensic_core.export_manifest` for later service/API work. They preserve Stage 2 source provenance and identify the explicit export content source/provider, but all output path, manifest path, byte-count, destination-safety, and hash fields are placeholder-ready until later Stage 3 tickets implement actual export behavior.

Stage 2 preview output remains a preview surface only; rendered text or hex must not be treated as export bytes.

## S3-T02 Fixture/Stub Export Callable

Callable usage from Python:

```python
from app.backend.api import export_file

result = export_file(entry, r"C:\case-exports")
```

`export_file()` consumes a Stage 2-style file-entry dictionary or S3-T01 `ExportRequest`, an explicit output directory, and an explicit export content provider. The default `StubExportContentProvider` maps `stub-file-hello` (`/hello.txt`) to raw synthetic `Hello, world!` bytes for dependency-free tests and smoke checks.

Current S3-T02 behavior:

- writes the exported file and a sibling JSON manifest when the destination is explicit and safe;
- preserves S3-T01 source provenance and content-source identity in the returned `ExportResult` and manifest;
- records provider byte counts before S3-T03 verification;
- refuses missing content, non-file entries, missing destinations, source/destination overlap, unsafe output names, and existing output/manifest files through structured statuses.

S3-T02 does not add audit persistence, recover deleted files, add UI/export commands, parse real evidence/filesystems, or require native forensic dependencies.

## S3-T03 Export Hashing And Byte-Count Verification

`export_file()` now verifies a successful write by reopening the exported output file, streaming its bytes through SHA-256, and recording the byte count observed on disk. The returned `ExportResult` and persisted manifest agree on `bytes_requested`, `bytes_written`, `hashes.sha256`, `hashes.status`, final status, and warnings.

Current S3-T03 behavior:

- computes SHA-256 from the written output file, not from provider bytes alone and not from preview text/hex;
- compares the written byte count with the provider byte count when known;
- returns structured `byte_count_mismatch` when the written size differs from expected provider bytes;
- returns structured `export_verification_failed` with hash status `hash_failed` when the output cannot be read back after writing;
- preserves S3-T02 destination safety, exclusive write, overwrite refusal, and partial-artifact cleanup behavior.

S3-T03 does not add MD5/SHA-1 production hashing, known-file matching, file signature analysis, extension mismatch checks, image verification, audit integration, deleted recovery, UI, real parser work, or required native dependencies.

## S3-T04 Optional Export Audit Integration

Callable usage from Python:

```python
from app.backend.api import ExportAuditContext, export_file
from app.backend.case_store import connect, initialize_schema

connection = connect(":memory:")
initialize_schema(connection)

result = export_file(
    entry,
    r"C:\case-exports",
    audit_context=ExportAuditContext(
        connection=connection,
        case_id="case-123",
        evidence_id="evidence-123",
        actor="examiner",
    ),
)
```

`ExportAuditContext` is explicit opt-in audit context. Supplying `source.case_id` or `source.evidence_id` in export provenance does not write to the case store by itself.

Current S3-T04 behavior:

- successful exports with `ExportAuditContext` insert one `audit_events` row with `action="file_export"`;
- audit details JSON records export status, source provenance, audit context ids, destination/output/manifest paths, byte counts, SHA-256/hash status, destination status, content-source identity, and warnings;
- failed exports are not audited by default;
- failed exports are audited only when `audit_failed_exports=True`, and details keep the non-ok export status;
- `export_file_to_json()` accepts the same audit context and passes it through.

S3-T04 uses the existing case-store schema and does not create cases or evidence sources automatically. Audit persistence errors are allowed to surface to the caller rather than being hidden as a successful audit.

## S4-T06 Analysis Persistence Boundary

Stage 4 analysis results are not persisted by the API layer yet. Standalone calls to `hash_file_content()`, `detect_file_signature()`, `evaluate_extension_mismatch()`, or `match_known_file_hashes()` remain JSON-friendly in-memory operations even when their source provenance contains `case_id` or `evidence_id`.

Future analysis persistence should mirror the explicitness of `ExportAuditContext`: callers must provide a SQLite connection, explicit case id, optional evidence id, optional actor/examiner, optional analysis job id, and an explicit intent to persist. The future API/workflow owner must also decide whether successful, failed, partial, and not-evaluated results should be stored.

S4-T06 and S4-T07 do not add API wrappers, background jobs, automatic persistence, schema migrations, search/timeline/reporting, UI, external known-file dataset storage, or real parser behavior.

## S3-T05 Deleted-File Recovery Boundary

The current export API does not perform deleted-file recovery. It exports bytes only from an explicit export content provider. A file entry with metadata such as `deleted=True` would still need a recovery-capable content source before export could proceed honestly.

Current API truth:

- `export_file()` is active provider-backed export, not deleted recovery.
- Stage 2 filesystem entries are metadata-only.
- Stub filesystem entries are allocated and not deleted.
- Preview-rendered text/hex and filesystem metadata are not export or recovery bytes.
- No API currently scans unallocated space, carves files, parses real filesystems, or recovers deleted content.

Future deleted-recovery API work should return structured statuses such as `deleted_recovery_unsupported`, `deleted_entry_metadata_only`, `recovery_content_unavailable`, `recovery_partial`, `recovery_not_attempted`, and `carving_deferred` instead of treating unsupported recovery as success. Any recovered bytes should reuse the existing export result, manifest, SHA-256/byte-count verification, destination safety, and optional audit behavior.
