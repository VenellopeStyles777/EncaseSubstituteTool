# Stage 4.5 Tickets - First Testing

Purpose: Stage 4.5 is a planning and workflow stage after Stage 4 and before any Stage 5 search/timeline work. Its job is to make the current project testable and demonstrable with user-provided E01 files, while documenting exactly what the current implementation can and cannot prove.

Stage 4.5 is not search/timeline. It should not implement broad new forensic features. It should create a careful plan for direct manual testing, command prompt output, optional simple visual output, and review guardrails around real E01 files supplied by the user.

## Stage 4.5 Status

Status: S4.5-IMP01 through S4.5-IMP09A are reviewed and done. S4.5-IMP09 now proves bounded parser-backed nested directory navigation with regular files visible from the local real E01 smoke. S4.5-IMP10 is drafted and required before Stage 5 resumes.

## Current Implemented Functionality Summary

The project currently implements these backend foundations:

- Stage 1 evidence intake foundation:
  - segmented `.E01/.E02/.E03...` sibling discovery by filename;
  - structured warnings for missing or unsupported segment patterns;
  - EWF reader adapter boundary;
  - dependency-free stub reader;
  - `pyewf` adapter skeleton with structured dependency-unavailable or real-reader-not-implemented status;
  - JSON intake callable/CLI;
  - minimal SQLite case/evidence/audit schema;
  - S4.5-IMP01 first-testing command shell that creates a safe case workspace, persists the existing intake snapshot, writes a manifest/summary/audit bundle, and marks later real-E01 sections unsupported.
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

- The current CLIs can run E01 segment discovery against a real user-provided `.E01` path, and S4.5-IMP01 can wrap that intake in a case workspace plus manifest/audit/unsupported-section artifacts.
- The current `pyewf` adapter can attempt best-effort metadata and explicit verification when `pyewf` is importable; if `pyewf` or a safe verification API is unavailable, it reports structured dependency/unsupported statuses.
- S4.5-IMP03 adds a project-local portable-runtime path for EWF-backed stream reads, partition-table volume discovery, and a real-parser-backed root filesystem listing from the local E01 set.
- The current backend can extract bytes only for an explicitly selected parser-backed root file through the S4.5-IMP04 provider path; it does not crawl, auto-select, or export arbitrary evidence files.
- S4.5-IMP05 can turn the current root listing into `file-list.json`, `file-list.csv`, and a static local `outputs/reports/summary.html`; S4.5-IMP09 adds explicit one-directory nested navigation artifacts, and S4.5-IMP09A makes the bounded demo prefer regular-file-visible nested listings when available. These tickets do not add recursive traversal, broad crawl, indexing, search/timeline, UI, or a report system.
- Stage 4 hash/signature behavior operates on explicit provider bytes, not E01-extracted filesystem bytes.

## Current Code Utilization Plan

This is the working map from the desired bare-minimum command-line workflow to the current codebase.

| Intended functionality | Current code to reuse | How it fits | Missing work |
| --- | --- | --- | --- |
| Accept E01 path in command prompt | `python -m app.backend.api.first_testing`, `run_first_testing()`, `run_e01_intake()`, `discover_e01_segments()` | S4.5-IMP01 accepts direct `.E01` and `--evidence-dir` plus `--first-segment`, then writes a case workspace and artifact bundle | Final guardrail handoff and command-line testing guide remain later slices |
| Create/open case file/workspace | `connect()`, `initialize_schema()`, `insert_case()`, `insert_evidence_source()`, `insert_audit_event()` in `app.backend.case_store` | S4.5-IMP01 creates a case database, case row, evidence source row, and first-testing audit events | Reopening/updating existing cases remains outside this first command shell |
| Basic case/evidence info | `insert_case()`, `insert_evidence_source()`, intake result dicts | S4.5-IMP01 saves the intake snapshot and writes `case.json` plus `run-manifest.json` | Later slices can add richer parser-backed evidence/file records |
| Segment info | `discover_e01_segments()` and `SegmentDiscoveryResult.to_dict()` | Already works against real filenames without parsing evidence bytes | Human-readable summary and persisted run artifact |
| EWF metadata | `EwfReaderAdapter`, `StubEwfReaderAdapter`, `PyewfEwfReaderAdapter.read_metadata()` | S4.5-IMP02 attempts best-effort normalized pyewf metadata when the dependency is importable and keeps missing fields as warnings | EWF-backed streams and parser consumers remain later slices |
| Verification | `EwfReaderAdapter.verify()`, `VerificationStatus` | S4.5-IMP02 keeps verification separate from metadata and runs only explicit supported verification APIs | Independent logical-image hash artifact is S4.5-IMP08 |
| Volume discovery | `discover_volumes()`, `VolumeInfo` | S4.5-IMP03 adds a `partition_table` strategy over an EWF-backed stream while preserving whole-image behavior | Deeper partition policy and edge-case handling remain later refinement |
| Navigate file structure | `FilesystemAdapter`, `Pytsk3FilesystemAdapter`, `list_directory()` | S4.5-IMP03 maps real parser-backed root entries into existing listing/result shapes; S4.5-IMP09 lists one explicit or bounded-demo nested directory; S4.5-IMP09A makes demo mode prefer file-visible nested listings when available | Recursive traversal and full-volume enumeration remain later/out of scope |
| File metadata | `FilesystemEntry`, directory-listing result entries | S4.5-IMP03 can populate root entries from a real filesystem parser when dependencies are available; S4.5-IMP05 exports current root entries to JSON/CSV; S4.5-IMP09/S4.5-IMP09A export the selected nested directory listing to JSON/CSV | Broad crawl and all-volume enumeration remain later/out of scope |
| Preview raw/text/hex | `preview_file()`, `PreviewContentProvider` | S4.5-IMP04 adds a selected-file E01 preview provider over explicit parser-backed bytes | Full file-list previews and auto-selection remain out of scope |
| File hash/signature | `hash_file_content()`, `detect_file_signature()`, `evaluate_extension_mismatch()` | S4.5-IMP04 adds a selected-file E01 analysis provider with bounded signature and in-memory hash policy | Broad analysis over all evidence files remains out of scope |
| Export selected file | `export_file()`, `ExportContentProvider`, `ExportAuditContext` | S4.5-IMP04 adds a selected-file E01 export provider for explicit, size-limited selections and explicit export dirs | Broad export/crawl and large-file streaming remain out of scope |
| Export file list | `list_directory()` result dictionaries | S4.5-IMP05 writes root-listing-derived `file-list.json` and `file-list.csv` with parser status, provenance, and honest zero-entry unavailable states | Recursive traversal and full-volume enumeration remain later/out of scope |
| Audit/review trail | `insert_audit_event()`, export audit details | Audit table and export audit pattern exist | First-testing audit actions for case creation, intake, verification, listing, preview, analysis, and exports |
| Command/visual output | Existing JSON serializers and result `to_dict()` methods | S4.5-IMP05 strengthens the command summary/artifact inventory and writes a static local `outputs/reports/summary.html` | Final testing guide remains later |

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
| S4.5-IMP01 | Done | First-testing command shell, safe case workspace, intake persistence, manifest, and unsupported-section output |
| S4.5-IMP02 | Done | Real EWF metadata and verification status while preserving dependency-free tests |
| S4.5-IMP02A | Done | Metadata warning semantics cleanup after S4.5-IMP02 review |
| S4.5-IMP03 | Done | Real E01 filesystem demo gate: EWF-backed stream, partition-table volumes, and real-parser-backed root listing |
| S4.5-IMP04 | Done | E01-backed selected-file content providers for preview/export/hash/signature |
| S4.5-IMP05 | Done | File-list JSON/CSV, command summary, artifact inventory, and static local HTML summary |
| S4.5-IMP06 | Done | Final guardrail review, documentation reconciliation, and Stage 5 handoff |
| S4.5-IMP07 | Done | Command-line testing guide and evidence workflow instructions |
| S4.5-IMP08 | Done | Independent full logical-image hash artifact |
| S4.5-IMP09 | Done | Nested directory navigation into actual filesystem entries |
| S4.5-IMP09A | Done | File-visible nested navigation correction |
| S4.5-IMP10 | Draft | Demo guide and Stage 5 gate refresh after hash/navigation |

## Implementation Runway

These planning tickets line up into implementation slices that must be completed and reviewed before S5-T02 or later search/timeline implementation. The user may pause work, review documentation, or choose when to start the next Stage 4.5 slice, but Stage 5 search/timeline cannot proceed until this runway is complete.

| Future implementation slice | Planning source | Deliverable |
| --- | --- | --- |
| S4.5-IMP01 | S4.5-T01 and S4.5-T02 | First-testing command shell, safe case workspace, intake persistence, manifest, and unsupported-section output; reviewed and done |
| S4.5-IMP02 | S4.5-T03 | Real `pyewf` metadata attempt and verification status while preserving dependency-free tests; reviewed and done |
| S4.5-IMP02A | S4.5-T03 | Narrow warning-semantics correction so `metadata_partial` only means actual metadata incompleteness; reviewed and done |
| S4.5-IMP03 | S4.5-T04 | Real E01 filesystem demo gate: EWF-backed stream, partition/volume boundary, and root filesystem metadata/listing; reviewed and done |
| S4.5-IMP04 | S4.5-T05 | E01-backed selected-file content providers for preview/export/hash/signature under explicit size policy; reviewed and done |
| S4.5-IMP05 | S4.5-T06 | File-list JSON/CSV, command summary, artifact inventory, and static local HTML; reviewed and done |
| S4.5-IMP06 | S4.5-T07 and S4.5-T08 | Manual-test guardrails, documentation reconciliation, and review handoff; reviewed and done |
| S4.5-IMP07 | S4.5-T07 and S4.5-T08 | User-facing command-line testing guide, PowerShell commands, artifact inspection steps, troubleshooting, and proof boundaries; reviewed and done |
| S4.5-IMP08 | User hands-on demo feedback | Independent SHA-256 full logical-image hash artifact over the EWF stream; reviewed/done for capability |
| S4.5-IMP09 | User hands-on demo feedback | Explicit nested directory navigation into actual filesystem entries; reviewed and done after S4.5-IMP09A |
| S4.5-IMP09A | S4.5-IMP09 review | Ensure demo mode reaches regular files and known nested file paths return `path_not_directory`; reviewed and done |
| S4.5-IMP10 | User hands-on demo feedback | Final guide and Stage 5 gate refresh after hash/navigation; drafted |

S4.5-IMP09A is done as the Stage 4.5 slice after S4.5-IMP09 review findings. It still writes bounded command artifacts rather than a live `cd`/`dir` style navigator; a separate future ticket should own that interactive browsing experience if desired. Stage 5 search/timeline remains blocked until S4.5-IMP10 is reviewed and S5-T01 is rerun and accepted.

## Stage 5 Gate Handoff After S4.5-IMP06

S4.5-IMP06 prepared the later S5-T01 rerun, S4.5-IMP07 completed the first command-line testing guide, S4.5-IMP08 added the explicit image-level hash path, and S4.5-IMP09/S4.5-IMP09A are done for explicit nested directory navigation with regular files visible in the corrected demo. S4.5-IMP10 remains the hard remaining Stage 4.5 prerequisite. S5-T02 and later search/timeline work must wait for S4.5-IMP10 review and for S5-T01 to be rerun and accepted.

Allowed future Stage 5 input records should be limited to reviewed, provenance-rich artifacts: intake and segment discovery, case/evidence/audit rows, metadata and verification status, EWF stream status, partition/volume records, filesystem/root-listing entries, root-listing-derived file-list JSON/CSV, reviewed image-level hash records, reviewed nested directory-listing records, and selected-file readiness/preview/analysis/export records only for explicit parser-backed selections. The static HTML summary is a local human-readable review artifact, not an indexing source.

Blocked inputs remain recursive traversal beyond the reviewed one-directory navigation artifact, broad full-volume crawl, arbitrary auto-selected preview/export/hash/signature, full-text E01 content, deleted recovery/carving, UI/report-system records, and verification-success claims when verification is unsupported or only stored hash metadata exists.

Any later search/timeline record must preserve source path, evidence id when available, volume id, file id/path, provider/source identity, source kind, parser/source status, dependency/not-supported/not-run states, warning list, timestamp context, read-only assertion, and source-modified assertion.

Matching implementation prompts now live under `prompts/vscode-agent/`:

- `2026-07-16-s4.5-imp02-real-ewf-metadata-verification.md`
- `2026-07-17-s4.5-imp02a-metadata-warning-semantics.md`
- `2026-07-16-s4.5-imp03-ewf-stream-partition-filesystem.md`
- `2026-07-16-s4.5-imp04-e01-file-content-providers.md`
- `2026-07-16-s4.5-imp05-file-list-output-visual-summary.md`
- `2026-07-16-s4.5-imp06-final-guardrail-review-handoff.md`
- `2026-07-16-s4.5-imp07-command-line-testing-guide.md`
- `2026-07-22-s4.5-imp08-image-level-verification-hash.md`
- `2026-07-22-s4.5-imp09-nested-directory-navigation.md`
- `2026-07-23-s4.5-imp09a-file-visible-navigation-correction.md`
- `2026-07-22-s4.5-imp10-demo-guide-and-stage-5-gate-refresh.md`

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
