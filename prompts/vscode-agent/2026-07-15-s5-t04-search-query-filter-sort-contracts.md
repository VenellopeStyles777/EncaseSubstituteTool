# 2026-07-15 - S5-T04 Search Query Filter Sort Contracts Prompt

Use this prompt only after S5-T03 is accepted.

```text
Implement ticket S5-T04: Search Query, Filter, And Sort Contracts.

Define request/result container contracts and validation. Do not implement actual matching yet.

Before editing, read:
- tickets/stage-5/S5-T03-searchable-record-contracts.md
- tickets/stage-5/S5-T04-search-query-filter-sort-contracts.md
- app/backend/forensic_core/search.py
- app/tests/test_search_contracts.py
- tickets/stage-5/README.md
- Goal.md
- plan.md
- functionality.md
- progression.md
- review.md
- workflow.md

Before implementing:
- Confirm S5-T03 is accepted.
- Summarize current search contract objects.
- List files you expect to modify.

Your task:
- Define search request/query structures.
- Define filter criteria for record type, status, source kind, synthetic/generated flags, parser/provider names, paths/extensions, entry type, hash/signature/known-file fields, and timestamp field presence.
- Define sort specs and pagination fields.
- Define result item and result set contracts.
- Validate malformed request fields into structured statuses or documented validation errors.
- Add dependency-free tests for serialization and invalid requests.
- Update docs and ticket status.
- Run python -m pytest and report the exact result.

Scope boundaries:
- Do not implement search matching.
- Do not implement sorting/pagination behavior beyond contract serialization/validation.
- Do not add timeline, API wrapper, persistence, parser work, UI, reporting, full-text search, commit, or push.

Final handoff:
- Summarize files changed.
- Summarize query/filter/sort/result contracts.
- Report tests.
- State limitations and next ticket.

Stop after S5-T04 and hand off for review.
```
