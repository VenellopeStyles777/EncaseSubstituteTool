# Plan - Sprint and Task Breakdown

Purpose: use this file for the working implementation plan once coding begins. Keep it practical: task, owner/agent, status, blockers, and verification.

Suggested first planning format:

| Stage | Task | Status | Notes |
| --- | --- | --- | --- |
| 0 | Decide stack and create app skeleton | Done | Python backend-first direction selected; planning docs and skeleton folders exist. |
| 1 | Build E01 evidence intake spike | Done | S1-T01 through S1-T06 complete. Stage 1 is a backend intake foundation, not real EWF/filesystem parsing. |
| 2 | Add volume/filesystem browsing MVP | Done | S2-T01 through S2-T07 complete. Stage 2 is a backend fixture/stub browsing foundation, not real EWF/partition/filesystem parsing. |
| 3 | Add export/recovery foundation | Done | S3-T01 through S3-T06 complete. Stage 3 is a backend fixture/stub export foundation, not real extraction or recovery. |
| 4 | Add hashing and signature checks | Next | Rough plan recorded below. Make this reproducible and testable after export/content-provider foundations exist. |

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

## Stage 4 Rough Plan

Stage 4 should begin only after Stage 3 has a reviewed export result/manifest shape and at least one safe fixture/stub/provider-backed export workflow.

Likely Stage 4 ticket sequence:

- Define hash job/result contracts for per-file content supplied by explicit content providers, not filesystem metadata alone.
- Add SHA-256/MD5/SHA-1 calculation for provider-backed file bytes, keeping broader evidence-image verification separate.
- Store hash-analysis results in JSON-friendly shapes with source provenance, provider identity, byte count, status, warnings, and timestamps.
- Add file signature/magic-byte detection for bounded provider-backed bytes.
- Add extension mismatch flags only when both file name/extension metadata and detected signature are available.
- Sketch known-file database import/matching as an optional later Stage 4 or Stage 4B task; do not require NSRL-scale data in default tests.
- Add optional case-store persistence only after standalone result shapes are reviewed.

Stage 4 guardrails:

- Do not require real EWF/filesystem parsers or native dependencies for default tests.
- Do not hash preview-rendered text/hex as if it were source file content.
- Do not claim whole-evidence verification unless the image/adapter layer actually exposes verified evidence bytes and expected hashes.
- Keep long-running/background job orchestration minimal until the result contracts are stable.

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
- Revisit packaging after backend contracts stabilize and native dependency direction is clearer.
