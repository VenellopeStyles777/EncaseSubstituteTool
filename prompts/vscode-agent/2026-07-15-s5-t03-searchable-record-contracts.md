# 2026-07-15 - S5-T03 Searchable Record Contracts Prompt

Use this prompt only after S5-T02 is accepted.

```text
Implement ticket S5-T03: Searchable Record Contracts.

This is a contract-only implementation ticket. Add searchable-record structures and tests, but do not implement query matching, filters, persistence, indexing, UI, reporting, parser work, timeline behavior, or full-text search.

Before editing, read:
- tickets/stage-5/README.md
- tickets/stage-5/S5-T01-readiness-and-stage-4.5-completion-gate.md
- tickets/stage-5/S5-T02-input-inventory-and-provenance-audit.md
- tickets/stage-5/S5-T03-searchable-record-contracts.md
- app/backend/api/directory_listing.py
- app/backend/forensic_core/filesystem_adapter.py
- app/backend/forensic_core/content_analysis.py
- app/backend/forensic_core/export_manifest.py
- app/backend/forensic_core/README.md
- app/tests/test_directory_listing.py
- app/tests/test_content_analysis_contracts.py
- Goal.md
- plan.md
- functionality.md
- progression.md
- review.md
- workflow.md

Before implementing:
- Confirm the S5-T01 gate passed.
- Summarize the input families from S5-T02.
- List files you expect to create or modify.
- State how this ticket preserves source kind, status, warnings, and provenance.

Your task:
- Add Stage 5 search schema/version constants.
- Add search status and warning structures.
- Add source/provenance structures for case/evidence/source/volume/file/parser/provider/source-kind fields.
- Add SearchableRecord or equivalent for file metadata, analysis results, export records, audit events, and future text records.
- Carry raw timestamp fields without normalizing them.
- Add to_dict/JSON-safe helpers.
- Add focused dependency-free tests.
- Update docs and ticket status.
- Run python -m pytest and report the exact result.

Scope boundaries:
- Do not implement matching, filters, sorting, pagination, timeline, API wrapper, persistence, parser behavior, UI, reporting, full-text search, commit, or push.
- Do not put file bytes or preview text into searchable records.
- Do not mark metadata-only records as content-bearing.

Final handoff:
- Summarize files changed.
- Summarize contracts added.
- Report tests.
- State limitations and next ticket.

Stop after S5-T03 and hand off for review.
```
