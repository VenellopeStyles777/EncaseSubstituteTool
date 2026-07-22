# S5-T14 - Timeline Query, Sorting, And JSON API

Status: Draft

Stage: Stage 5 - timeline foundations

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Add deterministic timeline sorting, range filtering, event filtering, and a small backend JSON API wrapper over caller-supplied timeline events.

This ticket should not add UI, reports, persistence, automatic case-store reads, parser work, search-index behavior, or full-text search.

## Entry Requirements

- S5-T13 accepted.

## Context To Read First

- `tickets/stage-5/S5-T10-timestamp-normalization-contracts.md`
- `tickets/stage-5/S5-T11-timeline-event-contracts.md`
- `tickets/stage-5/S5-T12-file-metadata-timeline-assembly.md`
- `tickets/stage-5/S5-T13-analysis-export-audit-timeline-adapters.md`
- `app/backend/forensic_core/timeline.py`
- `app/backend/api/README.md`
- `Goal.md`
- `plan.md`
- `functionality.md`
- `progression.md`
- `review.md`
- `workflow.md`

## Target Files/Folders

Likely files to create or modify:

- `app/backend/forensic_core/timeline.py`
- `app/backend/api/timeline.py`
- `app/backend/api/__init__.py`
- `app/tests/test_timeline_query_api.py`
- `app/backend/forensic_core/README.md`
- `app/backend/api/README.md`
- `functionality.md`
- `plan.md`
- `progression.md`
- `review.md`
- `tickets/stage-5/README.md`
- `tickets/stage-5/S5-T14-timeline-query-sorting-and-json-api.md`

## Required Work

- Add timeline query/filter contracts or helpers if not already present:
  - start/end timestamp bounds;
  - event type filter;
  - source category filter;
  - status code filter;
  - source kind filter;
  - case/evidence/volume/file id filters;
  - include/exclude unknown or invalid timestamps.
- Implement deterministic sorting:
  - known normalized timestamps sort chronologically;
  - unknown/missing/invalid timestamp policy is explicit;
  - tie-breaking is stable and deterministic.
- Add pagination/limit support if useful.
- Add a backend API callable over caller-supplied events.
- Add stable JSON output helper.
- Do not automatically assemble events from files, databases, or evidence paths inside the API wrapper.

## Acceptance Criteria

- Timeline events can be sorted chronologically with explicit handling of unknown/invalid timestamps.
- Range and source filters work over explicit events.
- JSON API wrapper returns stable output over caller-supplied events.
- Provenance and source uncertainty survive query/sort/filter.
- No automatic database reads, persistence, UI, report generation, parser behavior, or file-content work is added.
- Tests are dependency-free.

## Test Expectations

Add tests for:

- chronological sort;
- unknown/invalid timestamp ordering policy;
- date range filtering;
- event type/source category filters;
- source kind/status filters;
- pagination if implemented;
- API JSON helper output;
- provenance preservation.

Run:

```powershell
python -m pytest
```

## Documentation Updates

- Update forensic-core and API docs with timeline query/API scope.
- Update `functionality.md`, `plan.md`, `progression.md`, and `review.md`.
- Update ticket and Stage 5 README status.

## Review Checklist

- Are unknown/invalid timestamps handled honestly?
- Does API consume caller-supplied events only?
- Are evidence and case activity events still distinct?
- Did no UI/report/persistence/parser behavior sneak in?

## Handoff Prompt

Use `prompts/vscode-agent/2026-07-15-s5-t14-timeline-query-sorting-and-json-api.md`.
