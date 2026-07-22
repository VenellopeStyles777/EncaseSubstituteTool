# 2026-07-15 - S5-T11 Timeline Event Contracts Prompt

Use this prompt only after S5-T10 is accepted.

```text
Implement ticket S5-T11: Timeline Event Contracts.

Define timeline event and result structures. Do not assemble events from records yet.

Before editing, read:
- tickets/stage-5/S5-T10-timestamp-normalization-contracts.md
- tickets/stage-5/S5-T11-timeline-event-contracts.md
- app/backend/forensic_core/timeline.py
- app/backend/forensic_core/search.py
- app/backend/forensic_core/filesystem_adapter.py
- app/backend/forensic_core/content_analysis.py
- app/backend/forensic_core/export_manifest.py
- Goal.md
- plan.md
- functionality.md
- progression.md
- review.md
- workflow.md

Before implementing:
- Summarize timestamp contracts from S5-T10.
- List files you expect to modify.
- State how events will preserve evidence vs case activity distinctions.

Your task:
- Add TimelineEvent or equivalent with event id, type, timestamp, label, provenance, source record type/status/kind, synthetic/generated flags, read-only assertion, and warnings.
- Add timeline result containers.
- Preserve case/evidence/volume/file identifiers.
- Keep evidence-derived events separate from examiner/case activity events.
- Add to_dict/JSON-safe helpers and tests.
- Update docs and ticket status.
- Run python -m pytest and report the exact result.

Scope boundaries:
- Do not assemble events from metadata, analysis, export, or audit records yet.
- Do not sort/filter timelines.
- Do not add API wrappers, persistence, UI, reporting, parser behavior, full-text search, commit, or push.

Final handoff:
- Summarize files changed.
- Summarize event contracts.
- Report tests.
- State limitations and next ticket.

Stop after S5-T11 and hand off for review.
```
