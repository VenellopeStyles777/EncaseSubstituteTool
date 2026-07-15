# S5-T07 - Analysis Result Record Adapters

Status: Draft

Stage: Stage 5 - search foundations

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Adapt reviewed Stage 4 analysis results into Stage 5 `SearchableRecord` values without recalculating hashes, rereading providers, or changing analysis behavior.

This ticket creates adapters/contracts only. Search/filter behavior over those records belongs to S5-T08.

## Entry Requirements

- S5-T06 accepted.
- S4-T01 through S4-T05 remain reviewed/done.
- If Stage 4.5 added real parser-backed analysis providers, their source kind and warnings must remain visible.

## Context To Read First

- `tickets/stage-4/README.md`
- `tickets/stage-4/S4-T01-hash-signature-contracts.md`
- `tickets/stage-4/S4-T02-provider-backed-hashing.md`
- `tickets/stage-4/S4-T03-file-signature-detection.md`
- `tickets/stage-4/S4-T04-extension-mismatch-rules.md`
- `tickets/stage-4/S4-T05-known-file-matching.md`
- `tickets/stage-5/S5-T03-searchable-record-contracts.md`
- `app/backend/forensic_core/content_analysis.py`
- `app/backend/forensic_core/search.py`
- `app/tests/test_content_analysis_*.py`
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
- `app/tests/test_analysis_search_adapters.py`
- `app/backend/forensic_core/README.md`
- `functionality.md`
- `plan.md`
- `progression.md`
- `review.md`
- `tickets/stage-5/README.md`
- `tickets/stage-5/S5-T07-analysis-result-record-adapters.md`

## Required Work

- Add explicit adapter helpers for:
  - `HashAnalysisResult`;
  - `SignatureAnalysisResult`;
  - `ExtensionMismatchResult`;
  - `KnownFileMatchResult`.
- Do not call `hash_file_content()`, `detect_file_signature()`, `evaluate_extension_mismatch()`, or `match_known_file_hashes()` inside these adapters.
- Map analysis fields into searchable fields:
  - hash algorithms and digests;
  - signature type, signature label, MIME type;
  - observed extension and expected extensions;
  - mismatch boolean;
  - known-file category and dataset metadata;
  - analysis status codes;
  - bytes analyzed/inspected counts.
- Preserve source provenance, content-source identity, source kind, synthetic/generated flags, status, warnings, timestamps, and parser/provider names.
- Carry analysis timestamps as raw strings. Timeline normalization is not part of this ticket.
- Return structured non-ok records or validation warnings for unsupported input shapes.

## Acceptance Criteria

- Stage 4 analysis results can be represented as `SearchableRecord` values.
- Adapters never read bytes or recompute analysis.
- Synthetic/generated/provider-backed/real-parser source labels remain visible.
- Warnings from analysis results survive in the searchable record.
- Tests use dependency-free Stage 4 fixture-style results.
- No analysis behavior, search matching, timeline behavior, persistence, UI, parser work, or full-text search is added.

## Test Expectations

Add tests for:

- hash result adapter;
- signature result adapter;
- extension mismatch adapter;
- known-file match adapter;
- non-ok/partial analysis result preservation;
- synthetic/generated source label preservation;
- JSON-safe output;
- no recomputation behavior, using fakes if useful.

Run:

```powershell
python -m pytest
```

## Documentation Updates

- Update forensic-core docs with analysis-result search adapter boundaries.
- Update `functionality.md`, `plan.md`, `progression.md`, and `review.md`.
- Update ticket and Stage 5 README status.

## Review Checklist

- Were Stage 4 results adapted without recomputation?
- Are content-source labels and warnings retained?
- Does the implementation avoid external known-file datasets?
- Did this ticket avoid actual search/filter behavior?

## Handoff Prompt

Use `prompts/vscode-agent/2026-07-15-s5-t07-analysis-result-record-adapters.md`.
