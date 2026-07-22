# 2026-07-15 - S5-T13 Analysis Export Audit Timeline Adapters Prompt

Use this prompt only after S5-T12 is accepted.

```text
Implement ticket S5-T13: Analysis, Export, And Audit Timeline Adapters.

Adapt explicit analysis, export, and audit records into timeline events. Do not run analysis, export files, or query SQLite automatically.

Before editing, read:
- tickets/stage-5/S5-T11-timeline-event-contracts.md
- tickets/stage-5/S5-T12-file-metadata-timeline-assembly.md
- tickets/stage-5/S5-T13-analysis-export-audit-timeline-adapters.md
- app/backend/forensic_core/timeline.py
- app/backend/forensic_core/content_analysis.py
- app/backend/forensic_core/export_manifest.py
- app/backend/case_store/schema.py
- app/tests/test_content_analysis_contracts.py
- app/tests/test_file_export.py
- app/tests/test_case_store_schema.py
- Goal.md
- plan.md
- functionality.md
- progression.md
- review.md
- workflow.md

Before implementing:
- Summarize evidence event vs case activity event distinction.
- List which explicit record shapes will be adapted.
- List files you expect to modify.

Your task:
- Add adapters for Stage 4 analysis timestamps, Stage 3 export result/manifest timestamps, and case-store audit event rows/dicts.
- Label analysis/export timestamps as tool activity or analysis events unless clearly evidence-derived.
- Label audit rows as case activity events.
- Preserve identifiers, statuses, source kind, warnings, synthetic/generated flags, and read-only assertions.
- Handle missing/invalid timestamps using S5-T10 rules.
- Add dependency-free tests.
- Update docs and ticket status.
- Run python -m pytest and report the exact result.

Scope boundaries:
- Do not call analysis functions, export functions, or case-store query functions from adapters.
- Do not persist events, add automatic database reads, UI, reporting, parser behavior, search behavior, full-text search, commit, or push.

Final handoff:
- Summarize files changed.
- Summarize adapters added.
- Report tests.
- State limitations and next ticket.

Stop after S5-T13 and hand off for review.
```
