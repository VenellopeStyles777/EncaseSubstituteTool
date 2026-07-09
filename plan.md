# Plan - Sprint and Task Breakdown

Purpose: use this file for the working implementation plan once coding begins. Keep it practical: task, owner/agent, status, blockers, and verification.

Suggested first planning format:

| Stage | Task | Status | Notes |
| --- | --- | --- | --- |
| 0 | Decide stack and create app skeleton | Done | Python backend-first direction selected; planning docs and skeleton folders exist. |
| 1 | Build E01 evidence intake spike | Done | S1-T01 through S1-T06 complete. Stage 1 is a backend intake foundation, not real EWF/filesystem parsing. |
| 2 | Add volume/filesystem browsing MVP | In Progress | S2-T06 adds a bounded raw/text/hex preview foundation over stub or tiny generated content. Stage 2 docs handoff remains upcoming. |
| 3 | Add export/recovery foundation | Planned | Export selected fixture/stub files with manifest, hashes, provenance, and audit hooks. Deleted recovery remains conditional. |
| 4 | Add hashing and signature checks | Not started | Make this reproducible and testable after export/filesystem foundations exist. |

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
- `pytsk3`, The Sleuth Kit, `pyewf`, and libewf remain optional for early Stage 2; missing dependencies should produce structured unavailable status instead of failing default tests.

Stage 2 definition of done:

- Backend can produce structured volume/filesystem data from a fixture or stub path.
- Tests do not require private or large evidence.
- Missing native dependencies are visible and structured.
- No UI is required.
- Docs honestly separate real fixture-backed behavior from stubbed behavior.

## Stage 3 Ticket Outline

Tickets live under `tickets/stage-3/`:

- S3-T01: export result and manifest contract.
- S3-T02: fixture/stub file export service.
- S3-T03: export hashing and byte-count verification.
- S3-T04: case-store audit integration for exports.
- S3-T05: deleted-file recovery research and conditional plan.
- S3-T06: Stage 3 documentation and review handoff.

Stage 3 definition of done:

- Backend can export a selected fixture/stub file to an output directory.
- Export results include manifest/provenance and hash information.
- Tests prove source/evidence paths are not modified.
- Deleted-file recovery remains clearly scoped to filesystem support.

## Manual Testing And Executable Timing

Current manual testing level:

- Stage 1 has backend commands and automated tests, but no user-facing executable.
- Stage 1 manual command testing is possible through PowerShell, but it is not a packaged app workflow.

Recommended timing:

- End of Stage 2: first useful manual-test CLI flow. The user should be able to run intake, inspect fixture/stub volume information, list a directory/tree, and preview small text/hex content.
- End of Stage 3: first meaningful examiner-style backend workflow. The user should be able to intake, browse fixture/stub files, export a selected file, and inspect manifest/hash/provenance/audit output.
- Stage 4 or Stage 5: consider packaging a Windows executable once hashing/signatures or search/timeline make the tool useful enough to package.

Packaging guidance:

- Do not prioritize `.exe` packaging during early Stage 2.
- Keep Stage 2 and Stage 3 as Python CLI/manual commands.
- Revisit packaging after backend contracts stabilize and native dependency direction is clearer.
