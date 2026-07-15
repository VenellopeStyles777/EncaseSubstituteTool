# S5-T06 - Search Result Sorting And Pagination

Status: Draft

Stage: Stage 5 - search foundations

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Add deterministic sorting, pagination, result limits, and result-summary warnings for Stage 5 metadata search.

This ticket builds on S5-T05. It should not broaden into new record adapters, analysis-result search, timeline behavior, persistence, indexing, UI, parser work, or full-text search.

## Entry Requirements

- S5-T05 accepted.

## Context To Read First

- `tickets/stage-5/S5-T03-searchable-record-contracts.md`
- `tickets/stage-5/S5-T04-search-query-filter-sort-contracts.md`
- `tickets/stage-5/S5-T05-file-metadata-search-engine.md`
- `app/backend/forensic_core/search.py`
- `app/tests/test_file_metadata_search.py`
- `Goal.md`
- `plan.md`
- `functionality.md`
- `progression.md`
- `review.md`
- `workflow.md`

## Target Files/Folders

Likely files to modify:

- `app/backend/forensic_core/search.py`
- `app/tests/test_search_sorting_pagination.py`
- `app/backend/forensic_core/README.md`
- `functionality.md`
- `plan.md`
- `progression.md`
- `review.md`
- `tickets/stage-5/README.md`
- `tickets/stage-5/S5-T06-search-result-sorting-and-pagination.md`

## Required Work

- Implement sorting over allowed sort fields from S5-T04, such as:
  - display name;
  - file path;
  - extension;
  - entry type;
  - status code;
  - source kind;
  - selected timestamp strings without timeline normalization.
- Make sort order deterministic when values are missing or equal.
- Preserve original input order as a final tie-breaker where practical.
- Implement limit/offset or equivalent pagination from S5-T04.
- Return total input count, total matched count, returned count, limit, and offset.
- Return structured warnings for truncated results.
- Reject invalid sort fields/directions and invalid pagination values with structured non-ok status.
- Keep unknown/missing values visible rather than inventing values.

## Acceptance Criteria

- Search result ordering is deterministic.
- Pagination metadata is correct.
- Truncated result sets carry a warning.
- Invalid sort/pagination requests are structured and tested.
- Provenance and source labels survive sorting and pagination.
- No new search domain, timeline behavior, persistence, UI, parser behavior, or full-text search is added.

## Test Expectations

Add tests for:

- ascending and descending sort;
- missing sort values;
- stable tie-breaking;
- limit and offset;
- truncated-result warning;
- invalid sort field;
- invalid sort direction;
- invalid limit/offset;
- provenance preservation after pagination.

Run:

```powershell
python -m pytest
```

## Documentation Updates

- Update forensic-core docs with result ordering and pagination behavior.
- Update `progression.md`, `review.md`, `plan.md`, and `functionality.md`.
- Update ticket and Stage 5 README status.

## Review Checklist

- Are sorting and pagination deterministic?
- Does the implementation preserve source uncertainty?
- Are missing values not fabricated?
- Did the ticket stay within search result handling only?

## Handoff Prompt

Use `prompts/vscode-agent/2026-07-15-s5-t06-search-result-sorting-and-pagination.md`.
