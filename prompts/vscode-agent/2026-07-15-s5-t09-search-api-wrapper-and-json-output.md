# 2026-07-15 - S5-T09 Search API Wrapper And JSON Output Prompt

Use this prompt only after S5-T08 is accepted.

```text
Implement ticket S5-T09: Search API Wrapper And JSON Output.

Expose Stage 5 search through a small backend API callable over caller-supplied records.

Before editing, read:
- tickets/stage-5/S5-T03-searchable-record-contracts.md
- tickets/stage-5/S5-T04-search-query-filter-sort-contracts.md
- tickets/stage-5/S5-T05-file-metadata-search-engine.md
- tickets/stage-5/S5-T08-analysis-result-search-and-filters.md
- tickets/stage-5/S5-T09-search-api-wrapper-and-json-output.md
- app/backend/forensic_core/search.py
- app/backend/api/README.md
- app/backend/api/directory_listing.py
- app/backend/api/file_export.py
- app/tests/test_file_metadata_search.py
- app/tests/test_analysis_result_search.py
- Goal.md
- plan.md
- functionality.md
- progression.md
- review.md
- workflow.md

Before implementing:
- Summarize current search core behavior.
- State that the API will consume caller-supplied records only.
- List files you expect to create or modify.

Your task:
- Add app.backend.api.search or equivalent.
- Add a callable that accepts explicit SearchableRecord inputs and a query/request object or mapping.
- Add stable JSON helper output.
- Validate mapping inputs into the S5-T04 query contract.
- Export the callable from app.backend.api if consistent with local style.
- Add structured error handling for invalid requests.
- Add dependency-free tests.
- Update API/backend docs and ticket status.
- Run python -m pytest and report the exact result.

Scope boundaries:
- Do not automatically read case databases, file lists, evidence paths, exported artifacts, analysis providers, or file content.
- Do not add CLI, UI, timeline, full-text search, parser behavior, persistent indexes, background jobs, automatic persistence, reports, commit, or push.

Final handoff:
- Summarize files changed.
- Summarize API behavior.
- Report tests.
- State limitations and next ticket.

Stop after S5-T09 and hand off for review.
```
