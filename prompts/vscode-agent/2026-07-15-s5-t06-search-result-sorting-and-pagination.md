# 2026-07-15 - S5-T06 Search Result Sorting And Pagination Prompt

Use this prompt only after S5-T05 is accepted.

```text
Implement ticket S5-T06: Search Result Sorting And Pagination.

Add deterministic sorting, pagination, result limits, and truncation warnings for Stage 5 search results.

Before editing, read:
- tickets/stage-5/S5-T03-searchable-record-contracts.md
- tickets/stage-5/S5-T04-search-query-filter-sort-contracts.md
- tickets/stage-5/S5-T05-file-metadata-search-engine.md
- tickets/stage-5/S5-T06-search-result-sorting-and-pagination.md
- app/backend/forensic_core/search.py
- app/tests/test_file_metadata_search.py
- Goal.md
- plan.md
- functionality.md
- progression.md
- review.md
- workflow.md

Before implementing:
- Summarize existing search behavior.
- List sort fields and pagination semantics you plan to support.
- List files you expect to modify.

Your task:
- Implement deterministic sort behavior over allowed fields.
- Preserve input order as final tie-breaker where practical.
- Implement limit/offset or the existing pagination fields.
- Return total input, matched, returned, limit, and offset counts.
- Add structured warning(s) for truncated results.
- Reject invalid sort/pagination requests with structured status.
- Add dependency-free tests.
- Update docs and ticket status.
- Run python -m pytest and report the exact result.

Scope boundaries:
- Do not add new search domains, analysis adapters, timeline behavior, API wrappers, persistence, indexing, UI, reporting, parser work, full-text search, commit, or push.
- Do not invent missing values for sorting.

Final handoff:
- Summarize files changed.
- Summarize sorting/pagination behavior.
- Report tests.
- State limitations and next ticket.

Stop after S5-T06 and hand off for review.
```
