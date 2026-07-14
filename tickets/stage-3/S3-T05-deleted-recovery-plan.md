# S3-T05 - Deleted-File Recovery Research And Conditional Plan

Status: Done

Stage: Stage 3 - Export and recovery foundation

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Document what deleted-file recovery can and cannot mean with the current adapter capabilities, and define a conditional implementation plan for later real filesystem adapters.

This ticket is documentation/planning unless a reviewed real adapter already exposes recoverable deleted-file bytes. Current Stage 2 stubs do not.

## Context To Read First

- `prompts/vscode-agent/2026-07-13-stage-3-familiarization.md`
- `prompts/vscode-agent/2026-07-13-s3-t05-deleted-recovery-plan.md`
- `tickets/stage-3/S3-T01-export-manifest-contract.md`
- `tickets/stage-3/S3-T02-file-export-service.md`
- `tickets/stage-3/S3-T03-export-hashing.md`
- `tickets/stage-3/S3-T04-export-audit-integration.md`
- `tickets/stage-3/S3-T05-deleted-recovery-plan.md`
- `tickets/stage-3/README.md`
- `Goal.md`
- `plan.md`
- `functionality.md`
- `progression.md`
- `review.md`
- `workflow.md`
- `app/backend/forensic_core/filesystem_adapter.py`
- `app/backend/forensic_core/README.md`
- `app/backend/api/README.md`
- `app/fixtures/README.md`
- `app/docs/environment-readiness.md`
- S3-T01 through S3-T04 reviewed state

## Target Files/Folders

Likely files to modify:

- `app/backend/forensic_core/README.md`
- `app/backend/api/README.md`
- `app/fixtures/README.md`
- `app/docs/environment-readiness.md`
- `Goal.md`
- `plan.md`
- `functionality.md`
- `progression.md`
- `review.md`
- `tickets/README.md`
- `tickets/stage-3/README.md`
- `tickets/stage-3/S3-T05-deleted-recovery-plan.md`
- possibly a new doc under `app/docs/` if the plan becomes large

## Required Work

- Confirm and document current adapter capability. Current expected truth is:
  - `StubFilesystemAdapter` returns only allocated, non-deleted synthetic entries;
  - `Pytsk3FilesystemAdapter` is dependency/status scaffolding and does not parse filesystems;
  - current filesystem entries are metadata, not byte-bearing recovery objects;
  - `StubPreviewProvider` and `StubExportContentProvider` provide synthetic bytes only for explicitly registered file ids;
  - no reviewed adapter exposes deleted entries plus recoverable deleted-file bytes.
- Explain the difference between:
  - active allocated file export;
  - deleted entry metadata;
  - deleted file recovery;
  - carving/unallocated-space recovery;
  - unsupported/unrecoverable entries.
- State the current project truth:
  - `StubFilesystemAdapter` marks entries allocated and not deleted;
  - current entries are metadata-only;
  - current providers can supply synthetic bytes only when explicitly registered;
  - no real deleted-file recovery exists.
- Define future adapter requirements for deleted-file recovery, such as:
  - allocation/deleted status;
  - recoverable content ranges or provider source;
  - completeness/confidence status;
  - overwritten/sparse/unavailable range warnings;
  - filesystem-specific provenance.
- Define statuses/warnings that future code should use for unsupported deleted recovery.
- Suggested future status/warning names:
  - `deleted_recovery_unsupported`;
  - `deleted_entry_metadata_only`;
  - `recovery_content_unavailable`;
  - `recovery_partial`;
  - `recovery_not_attempted`;
  - `carving_deferred`.
- Explain that normal active-file export through S3-T02/S3-T04 is not deleted-file recovery, even when the result preserves `deleted=False`.
- Keep carving and advanced recovery deferred unless a later stage explicitly starts it.
- Do not add recovery APIs, fake deleted entries, fake recoverable deleted bytes, pytsk3 parsing, carving, unallocated-space scanning, UI, or new native dependencies.

## Acceptance Criteria

- Docs clearly state deleted-file recovery is unsupported/deferred in the current implementation.
- Docs tie future recovery to real adapter capability.
- No code claims deleted-file recovery exists.
- `functionality.md` keeps deleted recovery manual-test status `Untested`.
- Stage 3 final scope remains export foundation, not carving or advanced recovery.
- S3-T05 is documentation/planning-only unless the implementation agent can point to a reviewed adapter already exposing deleted entries and recoverable bytes. The current code does not.

## Test Expectations

This is expected to be documentation-only.

Run:

```powershell
python -m pytest
```

Record the result. If only docs changed and tests are not run, explain why.

## Documentation Updates

Update the docs listed above and ticket statuses.

## Review Checklist

- No unsupported deleted recovery claims were introduced.
- No fake deleted-byte recovery was implemented through the stub adapter.
- No carving, unallocated-space scanning, real parser work, UI, or Stage 4 analysis was introduced.
- The docs do not imply that preview bytes or stub export bytes prove real filesystem recovery.
- Future requirements preserve provenance, read-only source handling, content-source identity, and uncertainty/partial-recovery status.

## Implementation Handoff - 2026-07-13

- Confirmed S3-T05 remains documentation/planning-only: no reviewed adapter exposes deleted entries plus recoverable bytes.
- Documented active allocated export, deleted entry metadata, deleted-file recovery, carving/unallocated-space recovery, and unsupported/unrecoverable entries as separate concepts.
- Recorded current truth: stub entries are allocated and not deleted; filesystem entries are metadata-only; preview/export providers are explicit synthetic content sources; current export is not deleted recovery; no real deleted-file recovery exists.
- Defined future adapter requirements for allocation/deleted state, recoverable ranges or recovery content providers, completeness/confidence, warnings, filesystem-specific provenance, read-only handling, and compatibility with the S3 export/manifest/hash/audit workflow.
- Kept carving and unallocated-space scanning deferred.
- No recovery APIs, fake deleted entries, fake deleted bytes, parser work, UI, reporting, Stage 4 analysis, native dependencies, commits, or pushes were added.

## Review Result - 2026-07-13

- Approved for commit.
- Confirmed the changes are documentation/planning only.
- Confirmed current docs state deleted-file recovery is unsupported/deferred with the present adapters.
- Confirmed no recovery APIs, fake deleted entries, fake recoverable deleted bytes, parser work, carving, unallocated-space scanning, UI, reporting, or Stage 4 analysis were introduced.
- Verification: `python -m pytest` reported 99 passed in 6.72s during review.

## Research/Review Handoff - 2026-07-13

- S3-T01 through S3-T04 are reviewed and done.
- The current Stage 2 filesystem adapter only exposes metadata entries. `FilesystemEntry` has `allocated` and `deleted` fields, but no recoverable content ranges or deleted-entry byte provider.
- The default `StubFilesystemAdapter` returns `/Documents` and `/hello.txt` as allocated and not deleted.
- `Pytsk3FilesystemAdapter` reports dependency availability and `real_parser_not_implemented`; it does not expose deleted entries or file content.
- S3-T05 should therefore be documentation/planning only.

## Handoff Prompt

```text
Implement S3-T05 only after S3-T04 is reviewed and accepted, unless the research/review agent explicitly asks for this documentation earlier. This is documentation/planning: explain active export versus deleted-file recovery, current unsupported status, and future adapter requirements. Do not implement recovery code unless a reviewed real adapter already exposes recoverable deleted-file bytes. Stop after S3-T05 and hand off for review.
```
