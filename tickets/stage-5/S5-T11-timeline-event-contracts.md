# S5-T11 - Timeline Event Contracts

Status: Draft

Stage: Stage 5 - timeline foundations

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Define timeline event contracts that preserve event provenance, timestamp kind, source status, warnings, and uncertainty.

This ticket may add event/result structures and tests, but it must not assemble timelines from records yet.

## Entry Requirements

- S5-T10 accepted.

## Context To Read First

- `tickets/stage-5/S5-T10-timestamp-normalization-contracts.md`
- `app/backend/forensic_core/timeline.py`
- `app/backend/forensic_core/search.py`
- `app/backend/forensic_core/filesystem_adapter.py`
- `app/backend/forensic_core/content_analysis.py`
- `app/backend/forensic_core/export_manifest.py`
- `Goal.md`
- `plan.md`
- `functionality.md`
- `progression.md`
- `review.md`
- `workflow.md`

## Target Files/Folders

Likely files to modify:

- `app/backend/forensic_core/timeline.py`
- `app/backend/forensic_core/__init__.py`
- `app/tests/test_timeline_event_contracts.py`
- `app/backend/forensic_core/README.md`
- `functionality.md`
- `plan.md`
- `progression.md`
- `review.md`
- `tickets/stage-5/README.md`
- `tickets/stage-5/S5-T11-timeline-event-contracts.md`

## Required Work

- Define `TimelineEvent` or equivalent with:
  - event id;
  - event type;
  - timestamp object from S5-T10;
  - label/title;
  - source/provenance fields;
  - source record type;
  - source status;
  - source kind;
  - synthetic/generated flags;
  - read-only assertion;
  - warnings.
- Define timeline result containers for future assembly:
  - status;
  - warnings;
  - event count;
  - events.
- Preserve case/evidence/volume/file identifiers when available.
- Keep evidence timeline events separate from examiner/case activity events through explicit event type or source category.
- Provide `to_dict()` and JSON helper behavior.
- Do not create adapters from file metadata or analysis records yet.

## Acceptance Criteria

- Timeline event structures are JSON-serializable.
- Events can carry known, unknown, invalid, and missing timestamp statuses.
- Events preserve provenance and source uncertainty.
- Event type distinguishes evidence-derived events from case activity events.
- No timeline assembly, sorting, filtering, UI, reports, parser work, or persistence is added.
- Tests are dependency-free.

## Test Expectations

Add tests for:

- event serialization;
- unknown timestamp event;
- invalid timestamp event;
- source kind/synthetic/generated preservation;
- evidence event vs case activity event labeling;
- timeline result container serialization.

Run:

```powershell
python -m pytest
```

## Documentation Updates

- Update forensic-core docs with timeline event contract boundary.
- Update `functionality.md`, `plan.md`, `progression.md`, and `review.md`.
- Update ticket and Stage 5 README status.

## Review Checklist

- Do events preserve source provenance and uncertainty?
- Are case activity events clearly distinct from evidence events?
- Did this avoid assembly/sorting/filtering behavior?

## Handoff Prompt

Use `prompts/vscode-agent/2026-07-15-s5-t11-timeline-event-contracts.md`.
