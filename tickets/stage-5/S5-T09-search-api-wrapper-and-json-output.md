# S5-T09 - Search API Wrapper And JSON Output

Status: Draft

Stage: Stage 5 - search foundations

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Expose Stage 5 search behavior through a small backend API wrapper and stable JSON helper over caller-supplied records.

This ticket should make search easier to call from future workflows, but it must not add UI, persistent indexes, background jobs, file readers, parser work, full-text search, or automatic case-store persistence.

## Entry Requirements

- S5-T08 accepted.

## Context To Read First

- `tickets/stage-5/S5-T03-searchable-record-contracts.md`
- `tickets/stage-5/S5-T04-search-query-filter-sort-contracts.md`
- `tickets/stage-5/S5-T05-file-metadata-search-engine.md`
- `tickets/stage-5/S5-T08-analysis-result-search-and-filters.md`
- `app/backend/forensic_core/search.py`
- `app/backend/api/README.md`
- `app/backend/api/directory_listing.py`
- `app/backend/api/file_export.py`
- `app/tests/test_file_metadata_search.py`
- `app/tests/test_analysis_result_search.py`
- `Goal.md`
- `plan.md`
- `functionality.md`
- `progression.md`
- `review.md`
- `workflow.md`

## Target Files/Folders

Likely files to create or modify:

- `app/backend/api/search.py`
- `app/backend/api/__init__.py`
- `app/tests/test_search_api.py`
- `app/backend/api/README.md`
- `app/backend/forensic_core/README.md`
- `functionality.md`
- `plan.md`
- `progression.md`
- `review.md`
- `tickets/stage-5/README.md`
- `tickets/stage-5/S5-T09-search-api-wrapper-and-json-output.md`

## Required Work

- Add a backend API callable that accepts explicit `SearchableRecord` inputs and a query/request object or mapping.
- Add a stable JSON helper similar to existing `*_to_json()` helpers.
- Keep input records caller-supplied. Do not automatically read case databases, file lists, evidence paths, exported artifacts, or analysis providers.
- Validate mapping inputs into the S5-T04 query contract.
- Return JSON-serializable result sets preserving provenance.
- Export the callable from `app.backend.api` if consistent with existing API style.
- Add structured error handling for invalid requests.

## Acceptance Criteria

- Search can be called through a backend API wrapper over explicit records.
- JSON output is stable and sorted where practical.
- Invalid request mappings return structured errors.
- No automatic persistence, indexing, file reading, parser work, UI, CLI, full-text search, timeline, or report behavior is added.
- Tests are dependency-free.

## Test Expectations

Add tests for:

- successful API search over explicit metadata records;
- successful API search over explicit analysis records;
- JSON helper output;
- invalid query mapping;
- provenance preservation;
- no mutation of caller records.

Run:

```powershell
python -m pytest
```

## Documentation Updates

- Update `app/backend/api/README.md` with search API scope.
- Update `functionality.md`, `plan.md`, `progression.md`, and `review.md`.
- Update ticket and Stage 5 README status.

## Review Checklist

- Does the API wrapper require caller-supplied records?
- Does it avoid case-store auto-reads and persistent indexing?
- Are invalid requests structured?
- Does JSON preserve provenance and source uncertainty?

## Handoff Prompt

Use `prompts/vscode-agent/2026-07-15-s5-t09-search-api-wrapper-and-json-output.md`.
