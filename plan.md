# Plan - Sprint and Task Breakdown

Purpose: use this file for the working implementation plan once coding begins. Keep it practical: task, owner/agent, status, blockers, and verification.

Suggested first planning format:

| Stage | Task | Status | Notes |
| --- | --- | --- | --- |
| 0 | Decide stack and create app skeleton | Done | Python backend-first direction selected; planning docs and skeleton folders exist. |
| 1 | Build E01 evidence intake spike | Done | S1-T01 through S1-T06 complete. Stage 1 is a backend intake foundation, not real EWF/filesystem parsing. |
| 2 | Add volume/filesystem browsing MVP | Done | S2-T01 through S2-T07 complete. Stage 2 is a backend fixture/stub browsing foundation, not real EWF/partition/filesystem parsing. |
| 3 | Add export/recovery foundation | Done | S3-T01 through S3-T06 complete. Stage 3 is a backend fixture/stub export foundation, not real extraction or recovery. |
| 4 | Add hashing and signature checks | Done | S4-T01 through S4-T07 are reviewed/done. Stage 4 remains provider-backed and does not prove real filesystem extraction. |
| 4.5 | First testing with user-provided E01 files | Active | Planning package S4.5-T00 through S4.5-T08 is in review. S4.5-IMP01, S4.5-IMP02, S4.5-IMP02A, S4.5-IMP03, S4.5-IMP04, and S4.5-IMP05 are done. S4.5-IMP03 produced an EWF-backed stream, partition-table volume result, and real-parser-backed root filesystem listing from the local E01 set. S4.5-IMP04 added explicit selected-file content providers for preview/export/hash/signature. S4.5-IMP05 added root-listing-derived file-list JSON/CSV, command summary/artifact inventory updates, and static local HTML. S4.5-IMP06 and S4.5-IMP07 remain drafted before Stage 5 search/timeline implementation. |
| 5 | Add search and timeline foundations | Deferred | Detailed tickets S5-T00 through S5-T16 exist under `tickets/stage-5/`; S5-T00 documentation cleanup is done, S5-T01 is done with a failed gate, and S5-T01A is done. |

## Completed Foundation Stages

Detailed completed-ticket histories live under `tickets/stage-1/` through `tickets/stage-4/`, with implementation prompt history under `prompts/vscode-agent/` and review outcomes in `review.md`. This plan keeps only the current stage order and forward runway.

| Stage | Completed scope | Important remaining limit |
| --- | --- | --- |
| 1 | E01 segment filename discovery, EWF adapter boundary, JSON intake, SQLite case/evidence/audit schema | No real EWF metadata or verification |
| 2 | Local byte stream, whole-image volume boundary, filesystem adapter/stub, directory listing, bounded preview provider | No real partition/filesystem parsing or file extraction |
| 3 | Export contracts/service, manifests, SHA-256 and byte-count verification of written exports, optional audit | Export bytes are explicit provider bytes, not E01-extracted files |
| 4 | Provider-backed hash/signature/extension mismatch/known-file matching over explicit providers | Stage 4 analysis does not prove real E01 filesystem file-content extraction |

Current real-E01 truth:

- The project can discover `.E01/.E02/...` segment filenames.
- The S4.5-IMP01 first-testing command shell can create a case workspace, persist the existing intake snapshot, and write manifest/audit/unsupported-section artifacts.
- The project can attempt best-effort real EWF metadata through `pyewf` when available, while preserving dependency-unavailable status when it is missing.
- The project can run only explicit safe `pyewf` verification APIs when available; stored EWF hash metadata is not treated as verification success.
- S4.5-IMP03 can open the EWF-backed logical image, discover partition-table volumes, and produce a real-parser-backed root filesystem listing from the local E01 set in the portable runtime.
- The project can extract bytes only for an explicitly selected parser-backed root file within S4.5-IMP04's documented first-testing limits.
- S4.5-IMP05 can write root-listing-derived `file-list.json`, `file-list.csv`, and static local `outputs/reports/summary.html`; arbitrary export/crawl, nested traversal, search/timeline, UI, and report-system behavior remain unimplemented.

## Stage 4.5 First Testing Ticket Plan

Stage 4.5 is an added planning/workflow stage before Stage 5 search/timeline. Its goal is to make current progress demonstrable with user-provided E01 files and to improve the manual-testing/review workflow before broader features continue.

Current first-testing truth:

- The current code can run E01 filename/segment discovery against actual user-provided `.E01` paths.
- The S4.5-IMP01 command shell can run the existing intake path through a safe case workspace and output bundle.
- The current code can return structured adapter dependency status.
- The current `pyewf` adapter attempts best-effort metadata and explicit verification when importable, and otherwise reports dependency-unavailable or unsupported verification states.
- The current backend can produce a real-parser-backed root listing through the S4.5-IMP03 portable-runtime path.
- The current backend can run selected-file preview/export/hash/signature only when an explicit root entry is selected and the file fits the documented in-memory policy.
- The current backend can write file-list JSON/CSV and a static local HTML summary from the current root listing only.
- Stage 4 hash/signature behavior is provider-backed and does not yet analyze E01-extracted files.

Updated Stage 4.5 ticket sequence:

- S4.5-T00: current functionality summary, current-code utilization map, and first-testing scope. Status: Review.
- S4.5-T01: user-provided E01 handling, privacy, and evidence safety plan. Status: Review.
- S4.5-T02: first-testing case workspace and orchestration command plan. Status: Review.
- S4.5-T03: real `pyewf` metadata and verification investigation plan. Status: Review.
- S4.5-T04: EWF-backed byte stream, partition, and filesystem parser plan. Status: Review.
- S4.5-T05: E01-backed file-content provider plan for preview/export/hash/signature. Status: Review.
- S4.5-T06: file-list export, command prompt summary, and optional static HTML output plan. Status: Review.
- S4.5-T07: workflow, guardrail, and review optimization for manual testing. Status: Review.
- S4.5-T08: Stage 4.5 documentation and review handoff. Status: Review.
- S4.5-IMP01: first-testing command shell, case workspace, intake persistence, manifest, and unsupported-section output. Status: Done.

Stage 4.5 implementation runway:

- S4.5-IMP01 implements the first-testing command shell, case workspace, intake persistence, manifest, and unsupported-section output from S4.5-T01/T02. Status: Done.
- S4.5-IMP02 implements the real `pyewf` metadata attempt and verification status from S4.5-T03. Status: Done.
- S4.5-IMP02A corrects metadata warning semantics so stored hash metadata does not imply partial metadata by itself. Status: Done.
- S4.5-IMP03 implements the real-E01 filesystem demo gate from S4.5-T04: EWF-backed stream, partition/volume boundary, and root filesystem metadata/listing. Status: Done; use `.\.python312-embed\python.exe` for real-E01 smoke because `pyewf` and `pytsk3` are available there.
- S4.5-IMP04 implements E01-backed selected-file content providers for preview/export/hash/signature from S4.5-T05. Status: Done.
- S4.5-IMP05 implements file-list JSON/CSV, command summary, artifact inventory, and static local HTML from S4.5-T06. Status: Done.
- S4.5-IMP06 should reconcile manual-test guardrails and review handoff from S4.5-T07/T08. Status: Draft.
- S4.5-IMP07 should create the command-line testing guide with exact PowerShell commands, artifact inspection steps, troubleshooting, and proof boundaries. Status: Draft.
- Stage 5 search/timeline implementation should stay deferred until this first-testing implementation runway is reviewed complete. S5-T00 documentation cleanup is done, and S5-T01 has recorded the incomplete runway as a blocker.
- The next practical implementation step is S4.5-IMP06 for final guardrail review, documentation reconciliation, and Stage 5 handoff preparation.

Current code utilization for Stage 4.5:

- E01 command input now reuses `run_e01_intake()` and `discover_e01_segments()` through `run_first_testing()`.
- Case creation now reuses `connect()`, `initialize_schema()`, `insert_case()`, `insert_evidence_source()`, and `insert_audit_event()` in S4.5-IMP01.
- Real EWF metadata/verification now extends `EwfReaderAdapter`, `PyewfEwfReaderAdapter`, `EwfMetadataResult`, and `VerificationStatus`.
- EWF stream and root-listing work now extends `ImageByteStream`, `EwfImageByteStream`, `discover_volumes()`, `VolumeInfo`, `FilesystemAdapter`, `FilesystemEntry`, and `list_directory()` shapes.
- Preview/export/analysis now reuse `preview_file()`, `export_file()`, `hash_file_content()`, `detect_file_signature()`, and `evaluate_extension_mismatch()` through S4.5-IMP04 selected-file provider wrappers.
- File-list export now starts from `FilesystemEntry.to_dict()` / directory listing dictionaries and writes S4.5-IMP05 JSON/CSV plus a static local summary.

Stage 4.5 guardrails:

- Do not commit user-provided E01 files or derived sensitive output.
- Treat evidence inputs as read-only and write outputs only to explicit non-evidence directories.
- Do not claim real metadata, verification, volume parsing, filesystem parsing, or file extraction until reviewed implementation exists.
- Keep unsupported dependencies and not-implemented parser paths visible.
- Optimize handoffs to include automated test results, manual command attempts, skipped manual tests, evidence privacy notes, and review outcomes.
- Keep search/timeline, reports, UI, analysis persistence, deleted recovery, carving, and real parser work out of scope unless a later reviewed Stage 4.5 implementation ticket explicitly asks for a narrow piece.

## Stage 5 Detailed Ticket Plan

Stage 5 remains deferred as the next feature stage and is superseded as the immediate priority by Stage 4.5 first testing. When Stage 5 begins, it should first clean up documentation organization and duplication so the later search/timeline tickets start from a clear source of truth. Its later job is to define search and timeline foundations over explicit, provenance-rich records without hiding parser/source uncertainty.

S5-T01 is a hard gate: it must confirm the Stage 4.5 substantial-test implementation runway is complete and reviewed before S5-T02 or later search/timeline implementation proceeds. The 2026-07-16 S5-T01 pass failed this gate because S4.5-IMP01 through S4.5-IMP06 were not complete and reviewed; the runway now also includes S4.5-IMP07 for the command-line testing guide. S4.5-IMP01 through S4.5-IMP05 are done, but Stage 5 search/timeline remains blocked until the full runway through S4.5-IMP07 is completed and reviewed.

Detailed Stage 5 ticket sequence:

- S5-T00: documentation organization, duplication cleanup, and unused/confusing structure review. Status: Done.
- S5-T01: readiness and Stage 4.5 completion gate. Status: Done; failed gate/blocker because the S4.5-IMP01 through S4.5-IMP06 runway is incomplete.
- S5-T01A: Stage 4.5 gate language hardening. Status: Done.
- S5-T02: input inventory and provenance audit. Status: Draft.
- S5-T03: searchable record contracts. Status: Draft.
- S5-T04: search query, filter, and sort contracts. Status: Draft.
- S5-T05: file metadata search engine. Status: Draft.
- S5-T06: search result sorting and pagination. Status: Draft.
- S5-T07: analysis result record adapters. Status: Draft.
- S5-T08: analysis result search and filters. Status: Draft.
- S5-T09: search API wrapper and JSON output. Status: Draft.
- S5-T10: timestamp normalization contracts. Status: Draft.
- S5-T11: timeline event contracts. Status: Draft.
- S5-T12: file metadata timeline assembly. Status: Draft.
- S5-T13: analysis, export, and audit timeline adapters. Status: Draft.
- S5-T14: timeline query, sorting, and JSON API. Status: Draft.
- S5-T15: full-text search reality check. Status: Draft.
- S5-T16: Stage 5 documentation and review handoff. Status: Draft.

Stage 5 guardrails:

- S5-T00 is documentation-only and must not change app behavior, tests, schema, parser behavior, native dependency setup, UI, reporting, or search/timeline implementation.
- S5-T00 should reconcile `functionality.md`, `progression.md`, `log/`, `tickets/`, and `prompts/vscode-agent/`, and should remove or document unused/confusing markdown structure only after preserving unique information.
- Do not implement full-text search until text extraction is explicit, provider-backed, and honestly labeled.
- Do not hide dependency-unavailable, parser-not-implemented, synthetic-provider, partial, unsupported, or failed states.
- Do not imply real filesystem coverage when searching stub metadata.
- Preserve source path, evidence id when available, volume id, file id/path, provider/source identity, source kind, parser/source status, warnings, dependency/not-implemented states, and timestamp context in results.
- Keep UI/reporting, real parser work, deleted recovery, carving, and required native dependencies out of Stage 5 unless a later reviewed ticket changes scope.

## Forward Stage Risks

- Stage 5 search/timeline should not become search over synthetic provider data only. Results need source/provenance/status/warnings, and full-text search should wait for real text extraction or explicit provider-backed text with clear synthetic/generated labels.
- Stage 6 reporting/workflow must preserve uncertainty. Reports should distinguish real parser output, generated fixtures, synthetic providers, unsupported results, partial results, and failed analysis.
- Stage 7 advanced features such as carving, artifact parsing, shadow copies, encryption detection, OCR, and AI triage should remain deferred until real fixture strategy, optional integration tests, and manual workflows are stronger.

## Manual Testing And Executable Timing

Current manual testing level:

- Stage 1 has backend commands and automated tests, but no user-facing executable.
- Stage 1 manual command testing is possible through PowerShell, but it is not a packaged app workflow.

Recommended timing:

- End of Stage 2: first useful manual-test CLI flow. The user should be able to run intake, inspect fixture/stub volume information, list a directory/tree, and preview small text/hex content.
- End of Stage 3: first meaningful examiner-style backend workflow. The user should be able to intake, browse fixture/stub files, export a selected file, and inspect manifest/hash/provenance/audit output.
- Stage 4 or Stage 5: consider packaging a Windows executable once hashing/signatures or search/timeline make the tool useful enough to package.

Packaging guidance:

- Do not prioritize `.exe` packaging during Stage 2.
- Keep Stage 2 and Stage 3 as Python CLI/manual commands.
- Revisit packaging after backend contracts stabilize, native dependency direction is clearer, and at least one meaningful backend workflow has been manually tested.
