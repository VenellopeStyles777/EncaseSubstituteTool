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
| 5 | Add search and timeline foundations | Rough | Rough ticket plan exists under `tickets/stage-5/`; start with S5-T00 readiness review before any implementation. |

## Stage 1 Work Targets

Specific implementation tasks:

Stage 1 is now divided into tickets under `tickets/stage-1/`:

- S1-T01: backend Python skeleton.
- S1-T02: E01 segment discovery.
- S1-T03: EWF reader adapter interface.
- S1-T04: intake command JSON output.
- S1-T05: minimal case-store schema.
- S1-T06: documentation and review handoff.

## Stage 1 Implemented Capabilities

- Backend package imports and tests run through `python -m pytest`.
- E01 segment discovery reports ordered present segments and structured warnings.
- EWF reader adapters expose metadata, dependency, warning, and verification result shapes.
- Intake command prints JSON from segment discovery plus adapter output:

```powershell
python -m app.backend.api.intake path\to\sample.E01
```

- SQLite schema can create and insert/query `cases`, `evidence_sources`, and `audit_events`.

## Stage 1 Current Limitations

- No real EWF byte parsing yet.
- No filesystem or partition parsing yet.
- No UI yet.
- No automatic persistence from the intake command to SQLite yet.
- `pyewf`/libewf is optional; tests use stub/fallback behavior and do not require native forensic dependencies.
- Tests do not require real forensic evidence.

Definition of done:

- Stage 1 command/API runs.
- Tests cover segment discovery and adapter failure behavior.
- No real evidence file is required for tests.
- Read-only evidence handling is documented.
- Review agent has enough structure to inspect the implementation.

Status: complete.

## Stage 2 Ticket Outline

Tickets live under `tickets/stage-2/`:

- S2-T01: fixture and dependency strategy.
- S2-T02: image/byte-stream abstraction.
- S2-T03: volume discovery boundary.
- S2-T04: filesystem adapter boundary.
- S2-T05: directory listing and file metadata view.
- S2-T06: raw/text/hex preview foundation.
- S2-T07: Stage 2 documentation and review handoff.

S2-T01 fixture/dependency direction:

- Default tests should use pure stubs for adapter boundaries and structured status/error shapes.
- Tiny generated files under ignored workspace paths may be used for raw byte-stream and preview tests.
- Real raw, EWF, or pytsk3/The Sleuth Kit integration fixtures must remain optional, local-only, and skipped unless explicitly configured.
- `pytsk3`, The Sleuth Kit, `pyewf`, and libewf remain optional for Stage 2; missing dependencies should produce structured unavailable status instead of failing default tests.

Stage 2 definition of done:

- Backend can produce structured volume/filesystem data from a fixture or stub path.
- Tests do not require private or large evidence.
- Missing native dependencies are visible and structured.
- No UI is required.
- Docs honestly separate real fixture-backed behavior from stubbed behavior.

Stage 2 handoff status:

- Real local-file backed behavior: `LocalFileImageStream` describes and reads tiny local files in read-only mode with bounded offset/length handling.
- Stubbed behavior: volume discovery currently supports whole-image volume results; filesystem metadata and directory listing use deterministic adapter entries unless a later real adapter is added.
- Synthetic preview-provider behavior: raw/text/hex preview renders bytes supplied by an explicit provider, with the default stub provider serving synthetic `/hello.txt` content.
- Deferred: real EWF byte streams, image verification, partition parsing, real filesystem parsing, real file extraction, export/recovery, hashing/signatures, search/timeline, reporting, UI, executable packaging, and automatic case-store persistence for Stage 2 API results.
- Dependency policy: `pyewf`, libewf, `pytsk3`, and The Sleuth Kit remain optional; default tests must continue to pass without them.

## Stage 3 Ticket Outline

Tickets live under `tickets/stage-3/`:

- S3-T01: export result and manifest contract.
- S3-T02: fixture/stub file export service.
- S3-T03: export hashing and byte-count verification.
- S3-T04: case-store audit integration for exports.
- S3-T05: deleted-file recovery research and conditional plan.
- S3-T06: Stage 3 documentation and review handoff.

Stage 3 ticket readiness review, 2026-07-13:

- S3-T01 through S3-T06 are reviewed and done. S3-T06 stayed documentation/review-handoff only.
- A Stage 3 VS Code familiarization prompt now exists at `prompts/vscode-agent/2026-07-13-stage-3-familiarization.md`.
- The S3-T01 implementation prompt now exists at `prompts/vscode-agent/2026-07-13-s3-t01-export-manifest-contract.md`.
- The S3-T06 implementation prompt now exists at `prompts/vscode-agent/2026-07-14-s3-t06-stage-3-docs-review-handoff.md`.
- S3-T01 is contract-only: export request/result/manifest/status/warning/content-source structures and serialization tests, with no export file writes.
- S3-T02 should introduce the actual fixture/stub/provider-backed export service and destination safety checks.
- S3-T03 adds SHA-256 and byte-count verification after the write path exists.
- S3-T04 adds optional case-store audit hooks only when explicit audit context is supplied.
- S3-T05 documents why deleted-file recovery remains unsupported/deferred because current adapters do not expose deleted entries plus recoverable bytes.
- S3-T06 reconciles docs and prepares Stage 4 handoff notes without changing backend behavior.

Stage 3 definition of done:

- Backend can export a selected fixture/stub file to an output directory.
- Export results include manifest/provenance and hash information.
- Tests prove source/evidence paths are not modified.
- Deleted-file recovery remains clearly scoped to filesystem support.

## Stage 4 Detailed Ticket Plan

Stage 4 should begin only after Stage 3 has a reviewed export result/manifest shape and at least one safe fixture/stub/provider-backed export workflow.

Stage 4 starts with familiarization and risk review, not implementation. The review-agent audit is recorded in `tickets/stage-4/S4-T00-review-agent-risk-audit.md` and `review.md`. Use `prompts/vscode-agent/2026-07-14-stage-4-familiarization.md` for the coding agent before S4-T01.

Weakest-point carryover: the project has strong contracts and safe stubs, but no real evidence-backed content path. Stage 4 must keep provider identity explicit and should decide whether to add a tiny generated or optional fixture-backed reality anchor before Stage 5 search/timeline.

Detailed Stage 4 ticket sequence:

- S4-T00: review-agent familiarization and reality-anchor risk audit. Status: Done.
- S4-T01: hash/signature request/result/status/warning contracts and provenance model. Status: Done.
- S4-T02: provider-backed SHA-256 plus optional MD5/SHA-1 calculation for explicit content sources. Status: Done.
- S4-T03: file signature/magic-byte detection over bounded provider bytes. Status: Done.
- S4-T04: extension mismatch result rules where metadata and reviewed signature results both exist. Status: Done.
- S4-T05: fixture-sized known-file matching over caller-supplied in-memory records. Status: Done.
- S4-T06: planning-only case-store persistence decision for analysis results. Status: Done.
- S4-T07: Stage 4 documentation and review handoff. Status: Done.

Stage 4 guardrails:

- Do not require real EWF/filesystem parsers or native dependencies for default tests.
- Do not hash preview-rendered text/hex as if it were source file content.
- Do not claim whole-evidence verification unless the image/adapter layer actually exposes verified evidence bytes and expected hashes.
- Keep long-running/background job orchestration minimal until the result contracts are stable.

## Stage 5 Rough Ticket Plan

Stage 5 remains rough/draft and should start with S5-T00 readiness review. Its job is to define search and timeline foundations over explicit, provenance-rich records without hiding parser/source uncertainty.

Rough Stage 5 ticket sequence:

- S5-T00: Stage 5 readiness review and search/timeline risk audit.
- S5-T01: search result and filter contract model.
- S5-T02: filename and metadata search over existing listing/result shapes.
- S5-T03: hash/signature result search and filtering.
- S5-T04: timestamp normalization and timeline event contracts.
- S5-T05: timeline assembly from metadata and analysis result timestamps.
- S5-T06: full-text search reality check and deferred extraction plan.
- S5-T07: Stage 5 documentation and review handoff.

Stage 5 guardrails:

- Do not implement full-text search until text extraction is explicit, provider-backed, and honestly labeled.
- Do not hide dependency-unavailable, parser-not-implemented, synthetic-provider, partial, unsupported, or failed states.
- Do not imply real filesystem coverage when searching stub metadata.
- Preserve source path, evidence id when available, volume id, file id/path, provider/source identity, source kind, parser/source status, warnings, synthetic/generated labels, and timestamp context in results.
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
