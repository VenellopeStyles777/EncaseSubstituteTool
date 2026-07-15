# 2026-07-15 - S5-T08 Analysis Result Search And Filters Prompt

Use this prompt only after S5-T07 is accepted.

```text
Implement ticket S5-T08: Analysis Result Search And Filters.

Search already-produced analysis records. Do not calculate hashes, detect signatures, run known-file matching, read bytes, or import datasets.

Before editing, read:
- tickets/stage-5/S5-T05-file-metadata-search-engine.md
- tickets/stage-5/S5-T06-search-result-sorting-and-pagination.md
- tickets/stage-5/S5-T07-analysis-result-record-adapters.md
- tickets/stage-5/S5-T08-analysis-result-search-and-filters.md
- app/backend/forensic_core/search.py
- app/backend/forensic_core/content_analysis.py
- app/tests/test_analysis_search_adapters.py
- app/tests/test_file_metadata_search.py
- Goal.md
- plan.md
- functionality.md
- progression.md
- review.md
- workflow.md

Before implementing:
- Summarize existing search behavior and analysis record adapter behavior.
- List fields you will support for analysis filters.
- List files you expect to modify.

Your task:
- Add analysis-result search/filter support for hash digest, hash algorithm, signature type, MIME type, mismatch, known-file category, dataset metadata, analysis status, source kind, and synthetic/generated flags.
- Preserve source provenance and content-source identity.
- Return warnings when searching synthetic/generated/provider-backed analysis records.
- Treat absent digests/signatures/matches as no-match or filtered-out states, not crashes.
- Add dependency-free tests.
- Update docs and ticket status.
- Run python -m pytest and report the exact result.

Scope boundaries:
- Do not recalculate analysis.
- Do not read providers, file content, external known-file data, evidence files, exports, or databases.
- Do not add timeline, persistence, indexing, UI, reporting, parser behavior, full-text search, commit, or push.

Final handoff:
- Summarize files changed.
- Summarize analysis search/filter behavior.
- Report tests.
- State limitations and next ticket.

Stop after S5-T08 and hand off for review.
```
