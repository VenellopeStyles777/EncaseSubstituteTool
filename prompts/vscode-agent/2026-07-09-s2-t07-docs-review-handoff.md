# 2026-07-09 - S2-T07 Stage 2 Docs And Review Handoff Prompt

Use this prompt to hand S2-T07 to the Stage 2 VS Code implementation agent.

```text
Implement ticket S2-T07: Stage 2 Docs And Review Handoff.

Before editing, read these files:
- prompts/vscode-agent/2026-07-09-stage-2-familiarization.md
- Goal.md
- readme.md
- plan.md
- functionality.md
- progression.md
- review.md
- workflow.md
- tickets/stage-2/S2-T07-docs-review-handoff.md
- tickets/stage-2/README.md
- app/backend/README.md
- app/backend/api/README.md
- app/backend/forensic_core/README.md
- app/backend/case_store/README.md
- app/fixtures/README.md
- app/docs/environment-readiness.md

Context:
- Stage 1 is complete.
- S2-T01 through S2-T06 are implemented, reviewed, committed, pushed, and reported merged.
- Current focus is only S2-T07.
- S2-T07 is documentation and final Stage 2 review handoff, not new app behavior.
- Do not start Stage 3.
- Do not add export/recovery, hashing, UI, search, reporting, real EWF byte parsing, real partition parsing, real filesystem parsing, or native dependency requirements.
- Do not commit or push. Stop for review after this ticket.

Before editing:
- Briefly summarize your understanding of Stage 2's completed behavior and limitations.
- List the documentation files you expect to modify.
- If docs conflict, reconcile them conservatively and call out the assumption in `progression.md` or `review.md`.

Your task:
- Update docs so Stage 2 is described honestly as a backend browsing/preview foundation.
- Ensure docs describe completed Stage 2 capabilities:
  - fixture/dependency strategy;
  - read-only local image/byte-stream abstraction;
  - whole-image volume discovery boundary;
  - filesystem adapter boundary with stub and pytsk3 dependency-safe skeleton;
  - backend directory listing/file metadata view over adapter entries;
  - bounded raw/text/hex preview foundation over stub/provider content.
- Ensure docs describe current limitations:
  - no real EWF byte parsing;
  - no real image verification;
  - no real partition table parsing;
  - no real filesystem parsing or real file extraction;
  - no UI/executable packaging;
  - no export/recovery;
  - no hashing/signature analysis;
  - no search/timeline/reporting;
  - no automatic case-store persistence for Stage 2 API results;
  - `pyewf`, libewf, `pytsk3`, and The Sleuth Kit remain optional and are not required for default tests.
- Clearly separate what is real local-file backed, what is stubbed, and what is synthetic preview-provider content.
- Update `Goal.md` so Stage 2 status is no longer stale/planned-next and Stage 3 is described as the next planned stage.
- Update `readme.md` so the project front door describes current Stage 2 status, test command, and available backend callables/commands without overclaiming.
- Update `plan.md` so Stage 2 is marked review-ready or complete-at-handoff as appropriate, and Stage 3 remains planned/not started.
- Update `functionality.md` so S2-T07 status is current and all manual-test fields remain `Untested` unless the user has explicitly confirmed a manual test.
- Update `tickets/stage-2/README.md` and `tickets/stage-2/S2-T07-docs-review-handoff.md` to `Review` when implementation is complete.
- Update `progression.md` with the S2-T07 handoff result, what was learned, blockers if any, and the next step.
- Update `review.md` with a concise Stage 2 final review handoff/checklist.
- Update backend docs as needed, especially:
  - app/backend/README.md
  - app/backend/api/README.md
  - app/backend/forensic_core/README.md
  - app/docs/environment-readiness.md if dependency notes are stale.
- Run `python -m pytest` and report the result.

Likely files to modify:
- Goal.md
- readme.md
- plan.md
- functionality.md
- progression.md
- review.md
- tickets/stage-2/README.md
- tickets/stage-2/S2-T07-docs-review-handoff.md
- app/backend/README.md
- app/backend/api/README.md
- app/backend/forensic_core/README.md
- app/docs/environment-readiness.md
- app/fixtures/README.md only if fixture language needs a final Stage 2 clarification.

Scope boundaries:
- Do not add new production code unless fixing a documentation import/example issue absolutely requires a tiny correction.
- Do not add new tests unless documenting a command exposes a broken example that must be fixed.
- Do not start Stage 3.
- Do not implement export/recovery, hashing, UI, search, reporting, real parsing, or native dependency installation.
- Do not commit real evidence, raw disk images, E01 files, or filesystem images.

Deliverable:
- Stage 2 documentation and review handoff are ready for the research/review agent's final Stage 2 review.

Final handoff:
- Summarize docs changed.
- Summarize the final documented Stage 2 capabilities and limitations.
- Report the exact pytest command and result.
- State any remaining risks or docs intentionally left unchanged.
- Confirm you did not begin Stage 3.

Stop after S2-T07 and hand off for review. Do not commit, push, or begin Stage 3.
```
