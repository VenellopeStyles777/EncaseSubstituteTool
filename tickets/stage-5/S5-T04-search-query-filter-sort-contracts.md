# S5-T04 - Search Query, Filter, And Sort Contracts

Status: Draft

Stage: Stage 5 - search foundations

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Define search query, filter, sort, pagination, and result-set contracts over explicit `SearchableRecord` inputs.

This ticket should validate request shapes and serialize result containers, but it should not implement actual search matching yet.

## Entry Requirements

- S5-T03 accepted.

## Context To Read First

- `tickets/stage-5/S5-T03-searchable-record-contracts.md`
- `app/backend/forensic_core/search.py`
- `app/tests/test_search_contracts.py`
- `tickets/stage-5/README.md`
- `Goal.md`
- `plan.md`
- `functionality.md`
- `progression.md`
- `review.md`
- `workflow.md`

## Target Files/Folders

Likely files to modify:

- `app/backend/forensic_core/search.py`
- `app/backend/forensic_core/__init__.py`
- `app/tests/test_search_query_contracts.py`
- `app/backend/forensic_core/README.md`
- `functionality.md`
- `plan.md`
- `progression.md`
- `review.md`
- `tickets/stage-5/README.md`
- `tickets/stage-5/S5-T04-search-query-filter-sort-contracts.md`

## Required Work

- Define a search request/query structure with:
  - optional text query;
  - explicit fields to search;
  - match mode, such as `contains`, `exact`, `prefix`, or later `regex`;
  - case-sensitivity flag;
  - filter criteria;
  - sort specs;
  - limit/offset or page/page-size fields.
- Define filter criteria for:
  - record type;
  - status code;
  - source kind;
  - synthetic/generated flags;
  - parser/provider names;
  - file path/name/extension;
  - entry type;
  - hash algorithm/digest;
  - signature type;
  - known-file category;
  - timestamp field presence, without timeline normalization.
- Define sort specs but do not implement sorting yet.
- Define result item/result set contracts with:
  - matched record;
  - matched fields;
  - optional highlight ranges or matched value summaries;
  - status and warnings;
  - total input count;
  - total matched count;
  - returned count;
  - limit/offset.
- Validate malformed request fields into structured non-ok statuses.
- Keep regex either out of scope or validated as a future/deferred match mode. Do not allow a dangerous or unbounded regex implementation in this contract ticket.

## Acceptance Criteria

- Query/filter/sort/result-set structures are JSON-serializable.
- Invalid request shapes return structured statuses or raise documented validation errors covered by tests.
- Contracts do not perform matching yet.
- Contracts preserve uncertainty and source fields from records.
- Default tests pass without real evidence or native dependencies.

## Test Expectations

Add tests for:

- query serialization;
- filter serialization;
- sort serialization;
- pagination fields;
- invalid match mode;
- invalid filter field/operator;
- invalid limit/offset;
- result-set serialization with an existing `SearchableRecord`.

Run:

```powershell
python -m pytest
```

## Documentation Updates

- Update forensic-core docs with query/filter contract boundaries.
- Update `functionality.md`, `plan.md`, `progression.md`, and `review.md`.
- Update this ticket and the Stage 5 README to `Review` when complete.

## Review Checklist

- No actual matching, indexing, persistence, UI, or parser behavior was added.
- Filter fields match the S5-T02 inventory and S5-T03 record contract.
- Result-set contracts retain record provenance.
- Invalid requests are structured and tested.

## Handoff Prompt

Use `prompts/vscode-agent/2026-07-15-s5-t04-search-query-filter-sort-contracts.md`.
