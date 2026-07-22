# S5-T01A - Stage 4.5 Gate Language Hardening

Status: Done

Stage: Stage 5 gate follow-up before Stage 4.5 implementation resumes

Owner: Research/review agent

Reviewer: Research/review agent

## Objective

Remove or clarify active documentation wording that suggests Stage 4.5 first-testing implementation can be bypassed, set aside, or deprioritized before Stage 5 search/timeline implementation.

S5-T01 failed the Stage 5 readiness gate because S4.5-IMP01 through S4.5-IMP06 are not created, implemented, or reviewed. This small follow-up keeps that blocker unambiguous before the project moves to S4.5-IMP01.

## Completion Notes - 2026-07-16

Result: documentation hardening complete; ready for review.

Active bypass wording removed or clarified:

- `tickets/stage-4.5/README.md`: removed the "unless the user explicitly changes priority" escape valve and clarified that the user may pause or choose when to start S4.5-IMP01, but S5-T02+ cannot proceed until S4.5-IMP01 through S4.5-IMP06 are completed and reviewed.
- `tickets/stage-4.5/S4.5-T00-current-functionality-and-scope.md`: replaced "reviewed as complete enough or explicitly set aside by the user" with the hard S4.5-IMP01 through S4.5-IMP06 completion requirement.
- `tickets/stage-4.5/S4.5-T06-file-list-and-output-plan.md`: removed priority-change and set-aside wording from the implementation runway and Stage 5 handoff language.
- `tickets/stage-4.5/S4.5-T07-workflow-guardrail-review-optimization.md`: replaced "explicitly moves on" / "explicitly set aside" wording with the S4.5-IMP01 through S4.5-IMP06 completion rule.
- `tickets/stage-4.5/S4.5-T08-documentation-review-handoff.md`: clarified that S4.5-IMP01 is next, while S5-T02+ must wait for the full Stage 4.5 implementation runway.
- `app/docs/manual-testing/stage-4.5-first-testing.md`: replaced "reviewed or explicitly set aside" and "unless the user changes priority" with the hard gate plus pause/timing language.

Status preserved:

- S5-T01 remains `Done` as the accepted failed-gate/blocker record.
- S5-T02 through S5-T16 remain `Draft`.
- S4.5-IMP01 remains the next practical implementation ticket.

Focused search result: active Stage 4.5 docs no longer contain `set aside`, `priority changes`, `changes priority`, `unless the user changes priority`, or `explicitly sets Stage 4.5 implementation aside` as bypass guidance. The checked Stage 5 indexes show no readiness drift for S5-T02 through S5-T16. Remaining old-wording matches are historical review/log/prompt-history notes, privacy wording unrelated to bypassing, or S5-T01/S5-T01A descriptions of the wording that was hardened.

Verification: `python -m pytest`: 152 passed in 7.64s.

## Review Result - 2026-07-16

- Accepted as documentation-only hardening.
- Confirmed active Stage 4.5 and manual-testing guidance no longer allows Stage 5 search/timeline to proceed by setting aside or bypassing S4.5-IMP01 through S4.5-IMP06.
- Confirmed remaining old-wording matches are confined to S5-T01/S5-T01A descriptions of the hardened wording or historical review/log/prompt-history notes.
- Confirmed S5-T02 through S5-T16 remain `Draft`.
- S4.5-IMP01 remains the next practical implementation ticket.

## Current Truth

- S5-T00 is done.
- S5-T01 is accepted as a completed gate with a failed-gate/blocker result.
- Stage 5 search/timeline remains blocked/deferred.
- S5-T02 through S5-T16 remain `Draft`.
- Stage 4.5 first-testing implementation is required before S5-T02 or later.
- The next practical implementation ticket remains S4.5-IMP01 after this wording hardening.

## Context To Read First

- `tickets/stage-5/S5-T01-readiness-and-stage-4.5-completion-gate.md`
- `tickets/stage-5/README.md`
- `workflow.md`
- `tickets/stage-4.5/README.md`
- `tickets/stage-4.5/S4.5-T00-current-functionality-and-scope.md`
- `tickets/stage-4.5/S4.5-T06-file-list-and-output-plan.md`
- `tickets/stage-4.5/S4.5-T07-workflow-guardrail-review-optimization.md`
- `tickets/stage-4.5/S4.5-T08-documentation-review-handoff.md`
- `app/docs/manual-testing/stage-4.5-first-testing.md`
- `Goal.md`
- `readme.md`
- `plan.md`
- `functionality.md`
- `progression.md`
- `review.md`
- `log/documentation.md`
- `prompts/vscode-agent/README.md`

## Target Files/Folders

Likely files to modify:

- `tickets/stage-4.5/README.md`
- `tickets/stage-4.5/S4.5-T00-current-functionality-and-scope.md`
- `tickets/stage-4.5/S4.5-T06-file-list-and-output-plan.md`
- `tickets/stage-4.5/S4.5-T07-workflow-guardrail-review-optimization.md`
- `tickets/stage-4.5/S4.5-T08-documentation-review-handoff.md`
- `app/docs/manual-testing/stage-4.5-first-testing.md`
- `tickets/stage-5/S5-T01A-stage-4.5-gate-language-hardening.md`
- `tickets/stage-5/README.md`
- `plan.md`
- `functionality.md`
- `progression.md`
- `review.md`
- `log/documentation.md`
- `prompts/vscode-agent/README.md`

Only edit historical prompt files if they are still presented as reusable active instructions. If a prompt is clearly historical prompt history, leave it alone and make the active docs clear instead.

## Required Work

- Search active documentation for wording such as:
  - `set aside`
  - `priority changes`
  - `changes priority`
  - `unless the user changes priority`
  - `explicitly sets Stage 4.5 implementation aside`
- Replace active guidance that implies bypassing Stage 4.5 with the current hard rule:
  - S4.5-IMP01 through S4.5-IMP06 must be completed and reviewed before S5-T02 or later search/timeline implementation.
  - The user may pause work, review documentation, or choose the timing of S4.5-IMP01, but Stage 5 search/timeline cannot proceed until the Stage 4.5 runway is complete and reviewed.
- Preserve historical review/log entries unless they are being used as current guidance.
- Keep S5-T01 as the failed gate/blocker record.
- Keep S5-T02 through S5-T16 as `Draft`.
- Do not create or implement S4.5-IMP01 in this ticket.
- Do not start S5-T02 or later.

## Acceptance Criteria

- Active docs no longer imply Stage 4.5 substantial-test implementation can be bypassed or pushed back to start Stage 5 search/timeline.
- S5-T01 remains accepted as the failed-gate/blocker record.
- S5-T02 through S5-T16 remain `Draft`.
- S4.5-IMP01 remains the next practical implementation ticket after this hardening.
- No app behavior, tests, schema, parser behavior, evidence handling, search, timeline, UI, or report behavior changes.

## Test Expectations

Run:

```powershell
python -m pytest
```

Also run a focused text search for the old bypass wording in active Stage 4.5 and Stage 5 docs. Historical log/review mentions may remain if they are clearly historical.

## Review Checklist

- Did the change remove active `set aside` / `priority changes` escape-valve wording?
- Did it preserve the hard S5-T01 gate?
- Did it avoid changing app behavior?
- Did it leave S5-T02 and later blocked/draft?
- Did it avoid creating S4.5-IMP01?

## Handoff Prompt

Use `prompts/vscode-agent/2026-07-16-s5-t01a-stage-4.5-gate-language-hardening.md`.
