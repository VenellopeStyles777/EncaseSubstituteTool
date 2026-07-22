# 2026-07-15 - S5-T02 Input Inventory And Provenance Audit Prompt

Use this prompt only after S5-T01 has passed.

```text
Implement ticket S5-T02: Input Inventory And Provenance Audit.

This is documentation/design only. Do not implement search, filters, timeline assembly, indexing, persistence, UI, reporting, parser behavior, or new evidence handling.

Before editing, read:
- tickets/stage-5/README.md
- tickets/stage-5/S5-T01-readiness-and-stage-4.5-completion-gate.md
- tickets/stage-5/S5-T02-input-inventory-and-provenance-audit.md
- tickets/stage-4.5/README.md
- app/backend/api/directory_listing.py
- app/backend/forensic_core/filesystem_adapter.py
- app/backend/forensic_core/content_analysis.py
- app/backend/api/file_export.py
- app/backend/forensic_core/export_manifest.py
- app/backend/case_store/schema.py
- Goal.md
- readme.md
- plan.md
- functionality.md
- progression.md
- review.md
- workflow.md

Before changing files:
- Confirm S5-T01 gate passed.
- Summarize which Stage 4.5 outputs are implemented and reviewed.
- List the docs you expect to edit.

Your task:
- Inventory the record families Stage 5 can consume.
- For each record family, document schema version, status shape, warning shape, source path/private-path concerns, case/evidence/volume/file ids, parser/provider/source-kind fields, timestamps, and real/stub/synthetic/dependency states.
- Define the minimum provenance fields Stage 5 must preserve in search and timeline results.
- Identify which record families feed search tickets and which feed timeline tickets.
- Identify missing fields that later contracts must copy through, not invent.
- Update docs/logs with the audit decision.
- Run python -m pytest and report the exact result.

Scope boundaries:
- Do not create search.py or timeline.py in this ticket.
- Do not implement matching, filters, sorting, API wrappers, timeline events, persistence, parser behavior, UI, reports, commit, or push.
- Do not describe plans as reviewed behavior.

Final handoff:
- Summarize files changed.
- Summarize allowed input families.
- Summarize blocked or missing inputs.
- Report pytest result.
- State the next recommended ticket.

Stop after S5-T02 and hand off for review.
```
