# Stage 4.5 Tickets - First Testing

Purpose: Stage 4.5 is a planning and workflow stage after Stage 4 and before any Stage 5 search/timeline work. Its job is to make the current project testable and demonstrable with user-provided E01 files, while documenting exactly what the current implementation can and cannot prove.

Stage 4.5 is not search/timeline. It should not implement broad new forensic features. It should create a careful plan for direct manual testing, command prompt output, optional simple visual output, and review guardrails around real E01 files supplied by the user.

## Stage 4.5 Status

Status: T00 through T08 are planning in review. Stage 4.5 remains planning-only work; no behavior has been implemented.

## Current Implemented Functionality Summary

The project currently implements these backend foundations:

- Stage 1 evidence intake foundation:
  - segmented `.E01/.E02/.E03...` sibling discovery by filename;
  - structured warnings for missing or unsupported segment patterns;
  - EWF reader adapter boundary;
  - dependency-free stub reader;
  - `pyewf` adapter skeleton with structured dependency-unavailable or real-reader-not-implemented status;
  - JSON intake callable/CLI;
  - minimal SQLite case/evidence/audit schema.
- Stage 2 browsing foundation:
  - read-only local file byte-stream abstraction for tiny local files;
  - whole-image volume boundary for readable non-empty streams;
  - filesystem adapter boundary with deterministic stub entries;
  - dependency-safe `pytsk3` skeleton;
  - directory listing/file metadata callable over adapter entries;
  - raw/text/hex preview over explicit preview-provider bytes.
- Stage 3 export foundation:
  - export request/result/manifest/provenance contracts;
  - explicit provider-backed export service;
  - output/manifest overwrite refusal and destination safety checks;
  - SHA-256 and byte-count verification of written export artifacts;
  - optional explicit export audit events;
  - deleted-file recovery documented as unsupported/deferred.
- Stage 4 analysis foundation:
  - hash/signature analysis contracts with provenance and content-source identity;
  - provider-backed SHA-256, MD5, and SHA-1 hashing;
  - bounded file signature detection for a small magic-byte table;
  - extension mismatch evaluation over reviewed signature results plus metadata;
  - fixture-sized known-file matching over caller-supplied in-memory records;
  - planning-only analysis-result persistence notes.

Current real-E01 truth:

- The current CLI can run E01 segment discovery against a real user-provided `.E01` path.
- The current `pyewf` adapter does not yet read real EWF metadata or verify real EWF images.
- The current backend does not parse real partitions, real filesystems, or real file content from E01 files.
- Stage 4 hash/signature behavior operates on explicit provider bytes, not E01-extracted filesystem bytes.

## Current Code Utilization Plan

This is the working map from the desired bare-minimum command-line workflow to the current codebase.

| Intended functionality | Current code to reuse | How it fits | Missing work |
| --- | --- | --- | --- |
| Accept E01 path in command prompt | `app.backend.api.intake.main()`, `run_e01_intake()`, `discover_e01_segments()` | Existing intake CLI proves path-in to JSON-out for segment discovery and adapter status | New `first_testing` orchestration command with `--case`, `--output`, summary mode, and artifact writes |
| Create/open case file/workspace | `connect()`, `initialize_schema()`, `insert_case()`, `insert_evidence_source()`, `insert_audit_event()` in `app.backend.case_store` | SQLite foundation can store cases, evidence intake snapshots, and audit events when explicitly called | Case workspace folder layout, database path policy, CLI create/open behavior, automatic evidence registration |
| Basic case/evidence info | `insert_case()`, `insert_evidence_source()`, intake result dicts | Intake JSON can become the saved evidence-source snapshot | Case naming/description arguments, evidence id policy, run manifest |
| Segment info | `discover_e01_segments()` and `SegmentDiscoveryResult.to_dict()` | Already works against real filenames without parsing evidence bytes | Human-readable summary and persisted run artifact |
| EWF metadata | `EwfReaderAdapter`, `StubEwfReaderAdapter`, `PyewfEwfReaderAdapter.read_metadata()` | Adapter boundary exists and reports dependency/not-implemented states | Real `pyewf` metadata extraction, dependency install notes, structured partial/failure statuses |
| Verification | `EwfReaderAdapter.verify()`, `VerificationStatus` | Result shape exists | Real EWF verification or clear unsupported/not-run reporting through libewf/pyewf |
| Volume discovery | `discover_volumes()`, `VolumeInfo` | Current whole-image boundary can represent volume results | EWF-backed image stream and real partition parser strategy |
| Navigate file structure | `FilesystemAdapter`, `Pytsk3FilesystemAdapter`, `list_directory()` | Adapter/listing/result shapes exist | Real `pytsk3` filesystem parsing over EWF-backed image/volume bytes, path traversal/listing |
| File metadata | `FilesystemEntry`, directory-listing result entries | Metadata shape exists | Populate entries from real filesystem parser instead of stub entries |
| Preview raw/text/hex | `preview_file()`, `PreviewContentProvider` | Preview rendering and bounds exist | E01/filesystem-backed preview content provider for real file bytes |
| File hash/signature | `hash_file_content()`, `detect_file_signature()`, `evaluate_extension_mismatch()` | Analysis behavior exists for explicit provider bytes | E01/filesystem-backed analysis content provider for selected files |
| Export selected file | `export_file()`, `ExportContentProvider`, `ExportAuditContext` | Export, manifest, SHA-256 verification, destination safety, and optional audit exist | E01/filesystem-backed export content provider and real source provenance |
| Export file list | `list_directory()` result dictionaries | Directory/listing output is JSON-friendly | Dedicated file-list export to JSON and CSV, with parser status and provenance |
| Audit/review trail | `insert_audit_event()`, export audit details | Audit table and export audit pattern exist | First-testing audit actions for case creation, intake, verification, listing, preview, analysis, and exports |
| Command/visual output | Existing JSON serializers and result `to_dict()` methods | Most result shapes are already JSON-friendly | Summary printer, run manifest bundle, optional static HTML summary |

## Updated Ticket Direction

The old Stage 5 search/timeline path is deferred. The next tickets should move toward the first-testing command-line E01 workflow.

Recommended Stage 4.5 ticket sequence:

| Ticket | Status | Purpose |
| --- | --- | --- |
| S4.5-T00 | Review | Current functionality summary, current-code utilization map, and first-testing scope |
| S4.5-T01 | Review | User-provided E01 handling, privacy, and evidence safety plan |
| S4.5-T02 | Review | First-testing case workspace and orchestration command plan |
| S4.5-T03 | Review | Real `pyewf` metadata and verification investigation plan |
| S4.5-T04 | Review | EWF-backed byte stream, partition, and filesystem parser plan |
| S4.5-T05 | Review | E01-backed file-content provider plan for preview/export/hash/signature |
| S4.5-T06 | Review | File-list export, command prompt summary, and optional static HTML output plan |
| S4.5-T07 | Review | Workflow, guardrail, and review optimization for manual testing |
| S4.5-T08 | Review | Stage 4.5 documentation and review handoff |

## Implementation Runway

These planning tickets are intended to line up into implementation slices before Stage 5 search/timeline unless the user explicitly changes priority.

| Future implementation slice | Planning source | Deliverable |
| --- | --- | --- |
| S4.5-IMP01 | S4.5-T01 and S4.5-T02 | First-testing command shell, safe case workspace, intake persistence, manifest, and unsupported-section output |
| S4.5-IMP02 | S4.5-T03 | Real `pyewf` metadata attempt and verification status while preserving dependency-free tests |
| S4.5-IMP03 | S4.5-T04 | EWF-backed stream, partition discovery boundary, and root filesystem metadata/listing |
| S4.5-IMP04 | S4.5-T05 | E01-backed selected-file content providers for preview/export/hash/signature under explicit size or streaming policy |
| S4.5-IMP05 | S4.5-T06 | File-list JSON/CSV, command summary, artifact inventory, and optional static HTML |
| S4.5-IMP06 | S4.5-T07 and S4.5-T08 | Manual-test guardrails, documentation reconciliation, and review handoff |

The next practical implementation ticket should be S4.5-IMP01 unless the user changes priority. Do not add that implementation prompt until the user explicitly asks for it.

## Stage 4.5 Guardrails

- Do not commit user-provided E01 files, segment sets, or derived sensitive output.
- Treat user-provided evidence paths as read-only.
- Keep local evidence path configuration ignored or supplied at command time.
- Separate real E01 segment discovery from stub metadata and synthetic/provider-backed analysis.
- Do not claim real EWF metadata, verification, partition parsing, filesystem parsing, or file-content extraction until a reviewed ticket actually implements it.
- Make unsupported dependencies and not-implemented parser paths visible in command output.
- Require both automated tests and at least one documented manual command transcript when behavior changes.
- Keep Stage 5 search/timeline out of scope.

## Rough Stage 4.5 Definition Of Done

- The project has a written current-functionality summary suitable for explaining progress to a tester.
- The project has a detailed plan for user-provided E01 manual testing.
- The planned manual workflow shows what will appear in command prompt output and, if feasible, a simple HTML or JSON summary artifact.
- The plan identifies exact implementation tickets needed to move from current structured intake output to useful real-E01 demonstration output.
- The workflow/review guardrails explain how to handle real local evidence files without committing them or overstating support.
