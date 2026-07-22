# 2026-07-15 - S5-T05 File Metadata Search Engine Prompt

Use this prompt only after S5-T04 is accepted.

```text
Implement ticket S5-T05: File Metadata Search Engine.

Implement dependency-free in-memory search over explicit file metadata SearchableRecord inputs only.

Before editing, read:
- tickets/stage-5/S5-T03-searchable-record-contracts.md
- tickets/stage-5/S5-T04-search-query-filter-sort-contracts.md
- tickets/stage-5/S5-T05-file-metadata-search-engine.md
- app/backend/forensic_core/search.py
- app/tests/test_search_contracts.py
- app/tests/test_search_query_contracts.py
- app/backend/api/directory_listing.py
- app/backend/forensic_core/filesystem_adapter.py
- Goal.md
- plan.md
- functionality.md
- progression.md
- review.md
- workflow.md

Before implementing:
- Confirm S5-T01 gate is still valid.
- Summarize what records this ticket searches and why they are explicit inputs.
- List files you expect to modify.

Your task:
- Add in-memory search over caller-supplied SearchableRecord sequences.
- Support filename/path/display/extension matching as specified in the ticket.
- Support contains/exact/prefix modes if present in S5-T04.
- Apply field selection, case sensitivity, and metadata filters.
- Preserve provenance, status, warnings, source kind, synthetic/generated labels, and read-only fields.
- Add matched-field summaries without exposing file content.
- Return no_matches as a successful zero-result search.
- Add dependency-free tests.
- Update docs and ticket status.
- Run python -m pytest and report the exact result.

Scope boundaries:
- Do not read directories, evidence files, file content, preview text, exported files, or case databases.
- Do not implement analysis-result search, timeline, persistence, indexing, API wrappers, UI, reporting, parser behavior, full-text search, commit, or push.

Final handoff:
- Summarize files changed.
- Summarize metadata search behavior.
- Report tests.
- State limitations and next ticket.

Stop after S5-T05 and hand off for review.
```
