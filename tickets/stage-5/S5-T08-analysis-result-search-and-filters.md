# S5-T08 - Analysis Result Search And Filters

Status: Draft

Stage: Stage 5 - search foundations

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Implement search and filters over Stage 5 searchable records produced from reviewed Stage 4 analysis results.

This ticket searches already-produced result records. It must not calculate hashes, detect signatures, run known-file matching, import external datasets, read file bytes, or persist analysis results.

## Entry Requirements

- S5-T07 accepted.

## Context To Read First

- `tickets/stage-5/S5-T05-file-metadata-search-engine.md`
- `tickets/stage-5/S5-T06-search-result-sorting-and-pagination.md`
- `tickets/stage-5/S5-T07-analysis-result-record-adapters.md`
- `app/backend/forensic_core/search.py`
- `app/backend/forensic_core/content_analysis.py`
- `app/tests/test_analysis_search_adapters.py`
- `Goal.md`
- `plan.md`
- `functionality.md`
- `progression.md`
- `review.md`
- `workflow.md`

## Target Files/Folders

Likely files to modify:

- `app/backend/forensic_core/search.py`
- `app/tests/test_analysis_result_search.py`
- `app/backend/forensic_core/README.md`
- `functionality.md`
- `plan.md`
- `progression.md`
- `review.md`
- `tickets/stage-5/README.md`
- `tickets/stage-5/S5-T08-analysis-result-search-and-filters.md`

## Required Work

- Extend the in-memory search/filter engine to support analysis result record fields:
  - hash digest exact search;
  - hash algorithm filter;
  - signature detected type filter;
  - MIME type filter;
  - extension mismatch true/false filter;
  - known-file match category filter;
  - known-file dataset name/version filters;
  - analysis status code filters;
  - source kind and synthetic/generated filters.
- Preserve result provenance and content-source identity in every result.
- Return structured warnings when searching synthetic/generated/provider-backed analysis results.
- Treat absent digests/signatures/matches as explicit no-match or filtered-out states, not errors unless the request is invalid.
- Keep invalid filter values structured and tested.
- Do not read external known-file lists or any file content.

## Acceptance Criteria

- Existing search engine can match/filter Stage 4 analysis result records.
- Hash digest searches are exact by default.
- Signature, mismatch, and known-file filters work over explicit records.
- Non-ok analysis statuses remain searchable/filterable.
- Synthetic/generated/provider-backed labels remain visible.
- No new analysis calculation, persistence, parser behavior, external dataset import, UI, timeline, or full-text search is added.

## Test Expectations

Add tests for:

- exact hash digest lookup;
- unsupported or missing digest behavior;
- signature type filter;
- mismatch filter;
- known-file category filter;
- analysis status filter;
- source-kind synthetic/generated warnings;
- sorting/pagination still works with analysis records;
- invalid filter values.

Run:

```powershell
python -m pytest
```

## Documentation Updates

- Update forensic-core docs with analysis-result search behavior and limits.
- Update `functionality.md`, `plan.md`, `progression.md`, and `review.md`.
- Update ticket and Stage 5 README status.

## Review Checklist

- Does search consume only existing analysis records?
- Does it avoid recomputing hashes or signatures?
- Does it avoid external known-file datasets?
- Are non-ok and synthetic/generated states preserved?
- Did no timeline or full-text behavior sneak in?

## Handoff Prompt

Use `prompts/vscode-agent/2026-07-15-s5-t08-analysis-result-search-and-filters.md`.
