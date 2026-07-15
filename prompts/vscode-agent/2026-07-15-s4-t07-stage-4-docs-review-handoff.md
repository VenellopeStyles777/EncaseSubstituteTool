# 2026-07-15 - S4-T07 Stage 4 Documentation And Review Handoff Prompt

Use this prompt to hand S4-T07 to the Stage 4 VS Code implementation agent.

```text
Implement ticket S4-T07: Stage 4 Documentation And Review Handoff.

Before editing, read:
- prompts/vscode-agent/2026-07-14-stage-4-familiarization.md
- tickets/stage-4/README.md
- tickets/stage-4/S4-T00-review-agent-risk-audit.md
- tickets/stage-4/S4-T01-hash-signature-contracts.md
- tickets/stage-4/S4-T02-provider-backed-hashing.md
- tickets/stage-4/S4-T03-file-signature-detection.md
- tickets/stage-4/S4-T04-extension-mismatch-rules.md
- tickets/stage-4/S4-T05-known-file-matching.md
- tickets/stage-4/S4-T06-case-store-persistence-plan.md
- tickets/stage-4/S4-T07-docs-review-handoff.md
- tickets/stage-5/README.md
- Goal.md
- readme.md
- plan.md
- functionality.md
- progression.md
- review.md
- workflow.md
- tickets/README.md
- app/backend/README.md
- app/backend/api/README.md
- app/backend/case_store/README.md
- app/backend/forensic_core/README.md
- app/fixtures/README.md
- app/backend/forensic_core/content_analysis.py
- app/backend/api/file_export.py
- app/backend/case_store/schema.py
- Stage 4 tests under app/tests/test_content_analysis_*.py

Context:
- S4-T01 through S4-T06 are reviewed and done.
- S4-T07 is the Stage 4 documentation/review handoff.
- Stage 4 behavior exists in `app.backend.forensic_core.content_analysis`, not in API wrappers or background jobs.
- Stage 4 analysis bytes must come from explicit Stage 4 analysis content providers.
- The project still has no real EWF byte parsing, real partition parsing, real filesystem parsing, real filesystem file-content extraction, whole-image verification, analysis persistence implementation, search/timeline, reporting/UI, deleted recovery, carving, or required native dependencies.
- Stage 5 remains rough/draft and must not start in this ticket.

Before implementing:
- Summarize your understanding of the current true project state.
- List the files you expect to modify.
- State that S4-T07 is documentation/status reconciliation only.
- If you believe a code/schema/test change is needed, pause and explain it instead of implementing it.

Task:
- Keep S4-T07 documentation/review-handoff only.
- Reconcile top-level docs, backend docs, fixture notes, ticket indexes, progression, review, and documentation logs for the final reviewed Stage 4 state.
- Clearly document final Stage 4 behavior:
  - S4-T01 contracts;
  - S4-T02 provider-backed hashing;
  - S4-T03 bounded file signature detection;
  - S4-T04 extension mismatch evaluation over existing signature results plus metadata;
  - S4-T05 fixture-sized known-file matching over existing hash results plus caller-supplied in-memory records;
  - S4-T06 persistence planning only.
- Clearly document Stage 4 limits:
  - no real EWF/partition/filesystem parsing;
  - no real filesystem file-content extraction;
  - no whole-image verification;
  - no analysis-result persistence implementation;
  - no Stage 4 API wrappers;
  - no search/timeline/reporting/UI;
  - no external known-file datasets or NSRL import;
  - no deleted recovery/carving;
  - no required native dependencies.
- Keep Stage 3 export-output verification separate from Stage 4 per-file analysis hashing.
- Keep synthetic/generated/provider-backed analysis labels visible and warn that Stage 5 search/timeline must preserve source/provenance/status/warning/source-kind uncertainty.
- Keep Stage 5 rough/draft. Do not mark any Stage 5 ticket ready and do not start S5-T00.
- Keep manual-test status as Untested unless the user explicitly reported a manual run.
- Update S4-T07 and Stage 4 status docs to Review when complete.
- Run python -m pytest and report the exact result.

Likely files to modify:
- tickets/stage-4/S4-T07-docs-review-handoff.md
- tickets/stage-4/README.md
- tickets/stage-5/README.md
- tickets/README.md
- Goal.md
- readme.md
- plan.md
- functionality.md
- progression.md
- review.md
- log/documentation.md
- app/backend/README.md
- app/backend/api/README.md
- app/backend/case_store/README.md
- app/backend/forensic_core/README.md
- app/fixtures/README.md

Scope boundaries:
- Do not modify Python source files, schema files, tests, API behavior, persistence behavior, search/timeline code, UI, parser code, native dependency configuration, commit, or push.
- Do not create Stage 5 implementation tickets beyond rough/readiness wording.
- If a code/schema defect is discovered, pause and explain it instead of fixing it in S4-T07.

Verification:
- Run `python -m pytest`.
- Report the exact command and result.

Final handoff:
- Summarize documentation files changed.
- Summarize the final Stage 4 truth and Stage 5 readiness note.
- Report the exact pytest command and result.
- Confirm no behavior/schema/test changes and no Stage 5 implementation.

Stop after S4-T07 and hand off for review.
```
