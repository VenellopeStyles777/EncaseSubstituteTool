# Stage 4.5 First Testing Plan

Purpose: track how the project moves from automated tests only to direct manual testing with user-provided E01 files.

Stage 4.5 is not Stage 5 search/timeline. S4.5-IMP01 is reviewed and done as the first command-shell slice. S4.5-IMP02 and S4.5-IMP02A are reviewed and done as the best-effort metadata/verification slice plus warning-semantics correction. S4.5-IMP03 is reviewed and done after the project-local portable Python 3.12 runtime produced EWF stream, partition-table volume, filesystem, root-listing, and demo-readiness artifacts from the local E01 set. S4.5-IMP04 is reviewed and done after adding explicit selected-file content providers and selected-file artifacts. S4.5-IMP05 is reviewed and done after adding root-listing-derived file-list JSON/CSV and a static local HTML summary. Final handoff and testing-guide work remain incomplete.

## What Is Implemented Now

The current backend can:

- discover `.E01/.E02/.E03...` sibling segment names;
- report missing or unsupported segment patterns;
- run a JSON intake callable/CLI;
- run the S4.5-IMP01 first-testing command shell to create a case workspace, persist the existing intake snapshot, write a run manifest, write command summary text, write audit JSON, and write unsupported-section JSON;
- attempt best-effort real EWF metadata through `pyewf` when it is importable, while preserving dependency-unavailable output when it is missing;
- keep verification separate from metadata and report `verification_ok`, `verification_failed`, `verification_error`, `verification_partial`, `not_supported`, or `not_run`;
- open an EWF-backed logical image stream with `EwfImageByteStream` when `pyewf` is available;
- discover partition-table volume candidates with `pytsk3` when available;
- map a real-parser-backed root filesystem listing into existing directory-listing result shapes;
- run selected-file preview/export/hash/signature only when an explicit parser-backed root entry is selected and the operation fits the documented first-testing policy;
- write `file-list.json`, `file-list.csv`, and `outputs/reports/summary.html` from the current root listing only;
- create a minimal SQLite case/evidence/audit schema when called explicitly;
- run stubbed volume/filesystem/listing/preview/export workflows;
- run provider-backed hash/signature/mismatch/known-file helpers over explicit provider bytes.

The current backend cannot yet:

- guarantee real EWF metadata when `pyewf` is missing or metadata fields are unavailable;
- guarantee real EWF verification when no safe `pyewf` verification API is exposed;
- hash/export selected files above the documented in-memory limit without future streaming support;
- recursively crawl, enumerate all nested directories, or auto-select files from the E01 image;
- show a UI or packaged executable.

## Current Manual E01 Workflow

S4.5-IMP01 adds this command target:

```powershell
python -m app.backend.api.first_testing path\to\sample.E01 --case .test-artifacts\first-testing\case-001 --output .test-artifacts\first-testing\case-001\outputs
```

For dependency-free smoke checks, add `--adapter stub`. For a parseable stdout manifest, add `--json-only`. For shared console/summary text, add `--redact-paths`; local JSON artifacts keep original paths for examiner-owned review.

S4.5-IMP04 selected-file options are explicit and opt-in:

```powershell
.\.python312-embed\python.exe -m app.backend.api.first_testing --evidence-dir ".\ Test Image" --first-segment "C16242-1-RL1-E003.E01" --case .test-artifacts\first-testing\case-selected --selected-file-id "<root-entry-file-id>" --selected-file-export-dir .test-artifacts\first-testing\case-selected\exports --redact-paths
```

Use either `--selected-file-id` or `--selected-file-path`, not both. Do not choose arbitrary evidence files for shared testing; select only a reviewed safe, regular, allocated root entry. If no explicit file is selected, the command writes selected-file artifacts with `not_run` statuses.

Current first-testing sections:

- input evidence path;
- case workspace path and case/evidence identifiers;
- discovered segment chain;
- missing/unsupported segment warnings;
- adapter and dependency status;
- metadata and verification status from the existing intake adapter boundary, including S4.5-IMP02 `metadata.json` and `verification.json`;
- EWF stream, volume, filesystem, root-listing, and demo-readiness status artifacts from S4.5-IMP03 when the portable runtime can use `pyewf` and `pytsk3`;
- selected-file readiness, preview, analysis, and export status when a file is explicitly selected, or `not_run` when no file is selected;
- file-list JSON/CSV status and entry count from the current root listing;
- static local `outputs/reports/summary.html` artifact inventory and status summary;
- explicit current limitations;
- output paths for JSON artifacts.

Later sections for final handoff and command-line testing guidance remain future S4.5-IMP06 through S4.5-IMP07 work.

## Planned Case Workspace

The first command uses a case workspace rather than loose output files:

```text
.test-artifacts/first-testing/local-runs/case-a/
  case.db
  run-manifest.json
  command-summary.txt
  outputs/
    intake.json
    case.json
    metadata.json
    verification.json
    segment-discovery.json
    ewf-stream.json
    volumes.json
    filesystems.json
    root-listing.json
    demo-readiness.json
    selected-file-readiness.json
    selected-file-preview.json
    selected-file-analysis.json
    selected-file-export.json
    file-list.json
    file-list.csv
    reports/
      summary.html
    audit.json
    unsupported-sections.json
```

The command creates the SQLite case database with existing case-store helpers, persists the intake result as an evidence source, and records audit rows for the run. S4.5-IMP02 writes metadata and verification artifacts. S4.5-IMP03 writes stream, volume, filesystem, root-listing, and demo-readiness artifacts when the parser stack is available. S4.5-IMP04 writes selected-file artifacts and runs selected-file preview/export/hash/signature only for an explicit parser-backed root-entry selection. S4.5-IMP05 writes file-list JSON/CSV and a static local HTML summary from the current root listing while keeping recursive crawl, broad enumeration, search/timeline, and UI/reporting deferred.

## Current EWF Metadata And Verification Check

S4.5-IMP02 implements the first `pyewf` metadata/verification attempt. The metadata target is best-effort and read-only: media size, bytes per sector, segment count, reader version, and clearly exposed acquisition metadata. Sensitive fields such as case number, examiner, evidence number, description, and acquisition notes must be redacted from shared summaries unless the user approves.

Verification is separate from metadata. Reading stored EWF hash values is not the same as verifying the image. Verification runs only when the installed or injected `pyewf` API exposes an explicit safe method; otherwise the first-testing command shows `not_run` or `not_supported`.

## Current Stream, Volume, And Filesystem Bridge

S4.5-IMP03 implements the first path from E01 container bytes to navigable root filesystem metadata:

```text
selected .E01 -> EWF-backed image stream -> volume records -> filesystem entries -> directory listing
```

Use `.\.python312-embed\python.exe` for this path because that local runtime has `pyewf` and `pytsk3` available. The stream implements the existing `ImageByteStream` protocol instead of treating `.E01` as a raw local file. Partition parsing emits `VolumeInfo` records, and filesystem parsing emits `FilesystemResult` and `FilesystemEntry` records so `list_directory()` keeps its current response shape.

## Current File-Content Provider Bridge

S4.5-IMP04 implements the first selected-file content bridge:

- `E01SelectedFileContentReader` validates that a selected root entry is parser-backed, allocated, regular, and readable through the EWF stream plus parser APIs.
- Thin preview/export/analysis providers feed existing `preview_file()`, `export_file()`, `hash_file_content()`, `detect_file_signature()`, and `evaluate_extension_mismatch()` behavior.
- Preview and signature use bounded bytes.
- Hash and export are full-file only at or below the documented in-memory limit.
- The command must not fall back to stub providers while claiming E01-backed output.
- If parser-backed content is unavailable, selected-file artifacts say so directly with structured statuses.

## Current File List And Output Bundle

S4.5-IMP05 adds the output bundle that makes first testing inspectable without relying on automated tests alone. The command writes a local run manifest, command summary, JSON artifacts, CSV file list, selected-file export manifests when explicitly requested, and a single static local HTML summary.

The file list starts from the current root listing only. It preserves source path, volume id, file id/path/name, entry type, size, timestamps, allocation/deleted state, parser status, read-only assertion, and warnings. JSON remains authoritative; CSV is for quick review. The HTML summary is a local static artifact, not a UI/search/timeline feature, and it contains statuses, counts, and artifact inventory rather than evidence content.

The implementation lineup is now: command shell and case workspace, real metadata/verification, EWF stream plus filesystem listing, selected-file content providers, output bundle, guardrail/review handoff, then command-line testing guide. Stage 5 search/timeline must wait until S4.5-IMP01 through S4.5-IMP07 are completed and reviewed.

S4.5-IMP05 is reviewed and done. The real-E01 no-selection smoke discovered 53 segments, produced `metadata_available`, verification `not_supported`, EWF stream status `ok`, partition-table volume status `ok` with 5 volumes, filesystem status `ok`, a `real_parser_backed` root listing with 11 entries, file-list JSON/CSV `ok` with 11 entries, and a static HTML summary; selected-file readiness/preview/hash/signature/export were all `not_run` because no explicit safe file was selected. The next practical implementation slice is S4.5-IMP06 for guardrail/review handoff work. S5-T02 or later search/timeline implementation cannot proceed until the full Stage 4.5 implementation runway through S4.5-IMP07 is complete and reviewed.

## Minimum Demonstration Goal

At the bare minimum, the first-testing workflow should eventually show:

- case creation/opening with basic information;
- evidence intake from a user-provided E01 path;
- segment information;
- verification status;
- file-structure navigation;
- file metadata;
- basic analysis: file hash and signature for an explicitly selected root file;
- raw/text/hex preview for an explicitly selected root file;
- selected file export for an explicit, size-limited root file and explicit export destination;
- root file-list export.

Current code has foundations for several of these, S4.5-IMP04 adds the first explicit selected-file content path, and S4.5-IMP05 adds root file-list export plus static HTML summary output. Nested traversal, broad crawl, and a final command-line testing guide require additional implementation.

## Current Code To Reuse

| Demonstration area | Current code | Planned use |
| --- | --- | --- |
| E01 intake and segments | `run_e01_intake()`, `discover_e01_segments()` | First command section and saved intake JSON |
| Case workspace | `connect()`, `initialize_schema()`, `insert_case()`, `insert_evidence_source()`, `insert_audit_event()` | Create/open case database and record manual-test actions |
| EWF metadata/verification | `EwfReaderAdapter`, `PyewfEwfReaderAdapter`, `EwfMetadataResult`, `VerificationStatus` | S4.5-IMP02 attempts best-effort metadata/verification when available |
| Volumes/filesystem entries | `ImageByteStream`, `discover_volumes()`, `VolumeInfo`, `FilesystemAdapter`, `FilesystemEntry`, `list_directory()` | Preserve shapes while adding EWF/TSK-backed implementations |
| Preview | `preview_file()` | S4.5-IMP04 reuses raw/text/hex rendering for explicit selected-file bytes |
| Export | `export_file()`, `ExportAuditContext` | S4.5-IMP04 reuses destination safety, manifest, SHA-256 verification, and audit hook for explicit selected-file bytes |
| Analysis | `hash_file_content()`, `detect_file_signature()`, `evaluate_extension_mismatch()` | S4.5-IMP04 reuses existing provider-backed analysis over explicit selected-file bytes |
| File list | Directory listing dictionaries and `FilesystemEntry.to_dict()` | S4.5-IMP05 writes root-listing-derived JSON/CSV file-list export |

## Ticket Ownership

- S4.5-T01: user-provided E01 handling and privacy.
- S4.5-T02: case workspace and first-testing command plan.
- S4.5-T03: real `pyewf` metadata/verification plan.
- S4.5-T04: EWF-backed stream, partition, and filesystem parser plan.
- S4.5-T05: E01-backed file-content provider plan.
- S4.5-T06: file-list export, command prompt summary, and optional static HTML plan.
- S4.5-T07: workflow and review guardrails.
- S4.5-T08: final documentation/review handoff.

## Additional Basic EnCase-Like Output

For a useful first command-line MVP, the output should also include:

- an audit log of the manual run;
- dependency and parser capability summary;
- JSON run manifest with schema/tool versions and warnings;
- file-list export in JSON and CSV;
- export manifests with hashes and provenance;
- optional static HTML summary for visual review;
- timestamp handling notes for missing or normalized timestamps.

## Evidence Safety

- Source E01 files must be opened read-only.
- Output folders must not overlap source evidence folders.
- User-provided E01 files and generated summaries containing sensitive paths must not be committed.
- Shared review notes should redact private source paths unless the user explicitly allows them.
- Selecting `.E02` or later as the primary evidence input should be rejected with guidance to select `.E01`.
- Local run configs may contain private paths and must stay under ignored locations such as `.test-artifacts/first-testing/`.

## Planned Input And Output Policy

Accepted input forms:

- direct selected `.E01` path;
- evidence directory plus explicit first-segment filename;
- ignored local run configuration for repeat manual checks.

Output policy:

- case database, run manifest, command summary, file lists, exports, and reports should be written under the explicit case/output directory;
- output paths must not be inside the evidence directory;
- evidence paths must not be inside the output directory;
- shared summaries should redact private source roots as `<EVIDENCE_ROOT>`.

## Review Expectations

Every Stage 4.5 implementation handoff should include:

- automated test command and result;
- manual command attempted, if any;
- whether a real E01 file was used;
- what output files were produced;
- what was skipped and why;
- confirmation that no evidence file was modified;
- any redactions made in shared summaries.

Manual-test status in `functionality.md` can remain partial, because local real-E01 smokes have produced reviewed intake, metadata, stream, volume, filesystem, root-listing, and no-selection selected-file artifacts. Mocked dependency tests, stub providers, generated dummy filenames, dependency-unavailable output, and no-selection selected-file output do not count as full selected-file real-E01 testing; later output/guide slices and any selected-file real-content run remain untested until those behaviors are exercised with approved selections.

Shared transcripts, screenshots, HTML summaries, and file-list excerpts should redact evidence roots, user profile paths, case/client names, examiner names, evidence numbers, serial numbers, acquisition notes, and sensitive file paths unless the user explicitly approves disclosure.
