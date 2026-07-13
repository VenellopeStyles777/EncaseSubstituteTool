# S3-T05 - Deleted-File Recovery Research And Conditional Plan

Status: Draft

Stage: Stage 3 - Export and recovery foundation

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Document what deleted-file recovery can and cannot mean with the current adapter capabilities, and define a conditional implementation plan for later real filesystem adapters.

This ticket is documentation/planning unless a reviewed real adapter already exposes recoverable deleted-file bytes. Current Stage 2 stubs do not.

## Context To Read First

- `Goal.md`
- `plan.md`
- `functionality.md`
- `review.md`
- `app/backend/forensic_core/filesystem_adapter.py`
- `app/backend/forensic_core/README.md`
- `app/backend/api/README.md`
- `app/fixtures/README.md`
- S3-T01 through S3-T04 reviewed state

## Target Files/Folders

Likely files to modify:

- `app/backend/forensic_core/README.md`
- `app/backend/api/README.md`
- `app/fixtures/README.md`
- `Goal.md`
- `plan.md`
- `functionality.md`
- `progression.md`
- `review.md`
- `tickets/stage-3/README.md`
- `tickets/stage-3/S3-T05-deleted-recovery-plan.md`
- possibly a new doc under `app/docs/` if the plan becomes large

## Required Work

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
- Keep carving and advanced recovery deferred unless a later stage explicitly starts it.

## Acceptance Criteria

- Docs clearly state deleted-file recovery is unsupported/deferred in the current implementation.
- Docs tie future recovery to real adapter capability.
- No code claims deleted-file recovery exists.
- `functionality.md` keeps deleted recovery manual-test status `Untested`.
- Stage 3 final scope remains export foundation, not carving or advanced recovery.

## Test Expectations

This is expected to be documentation-only.

Run `python -m pytest` if practical to confirm no existing behavior regressed. If only docs changed and tests are not run, explain why.

## Documentation Updates

Update the docs listed above and ticket statuses.

## Review Checklist

- No unsupported deleted recovery claims were introduced.
- No fake deleted-byte recovery was implemented through the stub adapter.
- No carving, unallocated-space scanning, real parser work, UI, or Stage 4 analysis was introduced.

## Handoff Prompt

```text
Implement S3-T05 only after S3-T04 is reviewed and accepted, unless the research/review agent explicitly asks for this documentation earlier. This is documentation/planning: explain active export versus deleted-file recovery, current unsupported status, and future adapter requirements. Do not implement recovery code unless a reviewed real adapter already exposes recoverable deleted-file bytes. Stop after S3-T05 and hand off for review.
```
