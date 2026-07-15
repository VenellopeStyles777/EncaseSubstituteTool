# 2026-07-15 - S5-T14 Timeline Query Sorting And JSON API Prompt

Use this prompt only after S5-T13 is accepted.

```text
Implement ticket S5-T14: Timeline Query, Sorting, And JSON API.

Add deterministic timeline sorting, filtering, pagination if useful, and a backend JSON API wrapper over caller-supplied timeline events.

Before editing, read:
- tickets/stage-5/S5-T10-timestamp-normalization-contracts.md
- tickets/stage-5/S5-T11-timeline-event-contracts.md
- tickets/stage-5/S5-T12-file-metadata-timeline-assembly.md
- tickets/stage-5/S5-T13-analysis-export-audit-timeline-adapters.md
- tickets/stage-5/S5-T14-timeline-query-sorting-and-json-api.md
- app/backend/forensic_core/timeline.py
- app/backend/api/README.md
- Goal.md
- plan.md
- functionality.md
- progression.md
- review.md
- workflow.md

Before implementing:
- Summarize current timeline event/adapters behavior.
- State unknown/invalid timestamp ordering policy.
- State that the API consumes caller-supplied events only.
- List files you expect to create or modify.

Your task:
- Add timeline query/filter helpers for date bounds, event type, source category, status, source kind, and ids.
- Implement deterministic chronological sorting with explicit unknown/invalid handling.
- Add pagination/limit if useful and already specified.
- Add app.backend.api.timeline or equivalent JSON API wrapper over explicit events.
- Add stable JSON helper output.
- Add dependency-free tests.
- Update docs and ticket status.
- Run python -m pytest and report the exact result.

Scope boundaries:
- Do not automatically assemble events from files, databases, evidence paths, or analysis providers inside the API.
- Do not add persistent storage, UI, reports, parser behavior, full-text search, search-index behavior, commit, or push.

Final handoff:
- Summarize files changed.
- Summarize timeline query/API behavior.
- Report tests.
- State limitations and next ticket.

Stop after S5-T14 and hand off for review.
```
