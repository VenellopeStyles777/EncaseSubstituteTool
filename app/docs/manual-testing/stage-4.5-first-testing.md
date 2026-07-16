# Stage 4.5 First Testing Plan

Purpose: track how the project moves from automated tests only to direct manual testing with user-provided E01 files.

Stage 4.5 is not Stage 5 search/timeline. S4.5-IMP01 is reviewed and done as the first command-shell slice; it has a reviewer-run smoke test against the local ` Test Image` E01 set, while the broader parser/content/output workflow remains incomplete.

## What Is Implemented Now

The current backend can:

- discover `.E01/.E02/.E03...` sibling segment names;
- report missing or unsupported segment patterns;
- run a JSON intake callable/CLI;
- run the S4.5-IMP01 first-testing command shell to create a case workspace, persist the existing intake snapshot, write a run manifest, write command summary text, write audit JSON, and write unsupported-section JSON;
- report whether the EWF reader dependency is unavailable or not implemented;
- create a minimal SQLite case/evidence/audit schema when called explicitly;
- run stubbed volume/filesystem/listing/preview/export workflows;
- run provider-backed hash/signature/mismatch/known-file helpers over explicit provider bytes.

The current backend cannot yet:

- read real EWF metadata from user-provided E01 files;
- verify real EWF images;
- parse real partition tables;
- parse real filesystems;
- extract real file content from E01 images;
- hash or signature-check files extracted from E01 images;
- show a UI or packaged executable.

## Current Manual E01 Workflow

S4.5-IMP01 adds this command target:

```powershell
python -m app.backend.api.first_testing path\to\sample.E01 --case .test-artifacts\first-testing\case-001 --output .test-artifacts\first-testing\case-001\outputs
```

For dependency-free smoke checks, add `--adapter stub`. For a parseable stdout manifest, add `--json-only`. For shared console/summary text, add `--redact-paths`; local JSON artifacts keep original paths for examiner-owned review.

Current S4.5-IMP01 sections:

- input evidence path;
- case workspace path and case/evidence identifiers;
- discovered segment chain;
- missing/unsupported segment warnings;
- adapter and dependency status;
- metadata and verification status from the existing intake adapter boundary;
- explicit current limitations;
- output paths for JSON artifacts.

Later sections for volume/filesystem parser status, file listing, selected file metadata, preview, hash, signature, export results, CSV, and static HTML remain future S4.5-IMP02 through S4.5-IMP06 work.

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
    audit.json
    unsupported-sections.json
```

The command creates the SQLite case database with existing case-store helpers, persists the intake result as an evidence source, and records audit rows for the run. Until later tickets add real parsers, the summary and unsupported-section JSON label real metadata, verification, filesystem navigation, preview, export, hash/signature, file-list export, and static HTML as unsupported or not yet implemented.

## Planned EWF Metadata And Verification Check

S4.5-T03 keeps real `pyewf` work as an investigation plan before implementation. The first metadata target should be best-effort and read-only: media size, bytes per sector, segment count, reader version, and clearly exposed acquisition metadata. Sensitive fields such as case number, examiner, evidence number, description, and acquisition notes must be redacted from shared summaries unless the user approves.

Verification is separate from metadata. Reading stored EWF hash values is not the same as verifying the image. Until a real verification path is implemented and reviewed, the first-testing command should show verification as `not_run`, `not_supported`, or another explicit non-success status.

## Planned Stream, Volume, And Filesystem Bridge

S4.5-T04 plans the missing path from E01 container bytes to navigable filesystem metadata:

```text
selected .E01 -> EWF-backed image stream -> volume records -> filesystem entries -> directory listing
```

This remains unimplemented. The future stream should implement the existing `ImageByteStream` protocol instead of treating `.E01` as a raw local file. Partition parsing should continue to emit `VolumeInfo` records, and filesystem parsing should continue to emit `FilesystemResult` and `FilesystemEntry` records so `list_directory()` can keep its current response shape. File byte extraction for preview/export/hash/signature remains a later S4.5-T05 concern.

## Planned File-Content Provider Bridge

S4.5-T05 plans how a real parser-backed file entry should supply bytes to the existing preview, export, and analysis functions. The intended shape is a shared selected-file content reader with thin wrappers for preview, export, and analysis provider protocols.

The command must not fall back to stub providers while claiming E01-backed output. If parser-backed content is unavailable, preview/export/hash/signature sections should say so directly. Large-file behavior also needs an explicit policy: either refuse full-file export/hash above a documented first-testing limit or add streaming support before claiming large real-file operations.

## Planned File List And Output Bundle

S4.5-T06 plans the output bundle that makes first testing inspectable without relying on automated tests alone. The command should write a local run manifest, command summary, JSON artifacts, CSV file list, export manifests when available, and optionally a single static HTML summary.

The file list should start from `FilesystemEntry` records and preserve source path, volume id, file id/path/name, entry type, size, timestamps, allocation/deleted state, parser status, read-only assertion, and warnings. JSON should remain authoritative; CSV is for quick review. The optional HTML summary is a local artifact, not a UI/search/timeline feature.

The implementation lineup is now: command shell and case workspace, real metadata/verification, EWF stream plus filesystem listing, selected-file content providers, output bundle, then guardrail/review handoff. Stage 5 search/timeline must wait until S4.5-IMP01 through S4.5-IMP06 are completed and reviewed.

The next practical implementation ticket is S4.5-IMP02. The user may pause or choose when to start it, but S5-T02 or later search/timeline implementation cannot proceed until the full Stage 4.5 implementation runway is complete and reviewed. S4.5-IMP01 creates only the first-testing command shell, safe case workspace, intake persistence, manifest, and unsupported-section output; real parser work and Stage 5 search/timeline remain later work.

## Minimum Demonstration Goal

At the bare minimum, the first-testing workflow should eventually show:

- case creation/opening with basic information;
- evidence intake from a user-provided E01 path;
- segment information;
- verification status;
- file-structure navigation;
- file metadata;
- basic analysis: file hash and signature;
- raw/text/hex preview;
- selected file export;
- file-list export.

Current code has foundations for several of these, but the real E01-backed path is still missing. Segment discovery can run against an actual E01 path now. Real metadata, verification, volume parsing, filesystem parsing, file-content preview, file-content hash/signature analysis, and real file export require additional implementation.

## Current Code To Reuse

| Demonstration area | Current code | Planned use |
| --- | --- | --- |
| E01 intake and segments | `run_e01_intake()`, `discover_e01_segments()` | First command section and saved intake JSON |
| Case workspace | `connect()`, `initialize_schema()`, `insert_case()`, `insert_evidence_source()`, `insert_audit_event()` | Create/open case database and record manual-test actions |
| EWF metadata/verification | `EwfReaderAdapter`, `PyewfEwfReaderAdapter`, `EwfMetadataResult`, `VerificationStatus` | Extend adapter to read real metadata/verification when available |
| Volumes/filesystem entries | `ImageByteStream`, `discover_volumes()`, `VolumeInfo`, `FilesystemAdapter`, `FilesystemEntry`, `list_directory()` | Preserve shapes while adding EWF/TSK-backed implementations |
| Preview | `preview_file()` | Reuse raw/text/hex rendering once real file bytes are provided |
| Export | `export_file()`, `ExportAuditContext` | Reuse destination safety, manifest, SHA-256 verification, and audit hook |
| Analysis | `hash_file_content()`, `detect_file_signature()`, `evaluate_extension_mismatch()` | Reuse existing provider-backed analysis over E01-backed file bytes |
| File list | Directory listing dictionaries and `FilesystemEntry.to_dict()` | Add JSON/CSV file-list export |

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

Manual-test status in `functionality.md` can record the S4.5-IMP01 command-shell smoke run as partial, because it used an approved local E01 set and produced reviewed artifacts. Mocked dependency tests, stub providers, generated dummy filenames, and dependency-unavailable output alone do not count as full manual E01 testing; later parser/content/output slices remain untested until those behaviors exist and are exercised.

Shared transcripts, screenshots, HTML summaries, and file-list excerpts should redact evidence roots, user profile paths, case/client names, examiner names, evidence numbers, serial numbers, acquisition notes, and sensitive file paths unless the user explicitly approves disclosure.
