# S5-T15 - Full-Text Search Reality Check

Status: Draft

Stage: Stage 5 - search foundations

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Decide and document the honest full-text search boundary for Stage 5 after Stage 4.5 content-provider work.

This ticket should either keep full-text search deferred, or define a narrow explicit-text-record contract. It must not silently treat file names, preview rendering, hex output, export manifests, or stub strings as full evidence text.

## Entry Requirements

- S5-T09 accepted.
- S4.5-IMP04 reviewed if real E01-backed selected-file content providers are relevant.
- S5-T01 gate still valid.

## Context To Read First

- `tickets/stage-5/S5-T02-input-inventory-and-provenance-audit.md`
- `tickets/stage-5/S5-T03-searchable-record-contracts.md`
- `tickets/stage-5/S5-T05-file-metadata-search-engine.md`
- `tickets/stage-4.5/S4.5-T05-e01-file-content-provider-plan.md`
- `app/backend/api/file_preview.py`
- `app/backend/api/file_export.py`
- `app/backend/forensic_core/content_analysis.py`
- `app/backend/forensic_core/search.py`
- `Goal.md`
- `plan.md`
- `functionality.md`
- `progression.md`
- `review.md`
- `workflow.md`

## Target Files/Folders

Likely files to modify:

- `tickets/stage-5/S5-T15-full-text-search-reality-check.md`
- `tickets/stage-5/README.md`
- `app/backend/forensic_core/README.md`
- `app/backend/api/README.md`
- `functionality.md`
- `plan.md`
- `progression.md`
- `review.md`
- `log/documentation.md`

If the reviewer approves a contract-only explicit text record, likely files may also include:

- `app/backend/forensic_core/search.py`
- `app/tests/test_text_search_contracts.py`

## Required Work

- Review whether Stage 4.5 produced a reviewed, explicit content provider capable of text extraction.
- Decide one of these outcomes:
  - `deferred`: full-text search remains out of scope because text extraction is not implemented/reviewed;
  - `contract_only`: define explicit text search record contracts without implementing extraction;
  - `provider_backed_text_only`: allow search only over caller-supplied explicit text records with provenance and source labels.
- If deferred, update docs and ticket status only.
- If contract-only, define:
  - text record source provenance;
  - text extraction status;
  - encoding/source text warnings;
  - source kind/synthetic/generated flags;
  - text length and truncation fields;
  - no actual extraction.
- If provider-backed text-only is allowed, require:
  - caller-supplied text records;
  - no automatic file reads;
  - size limits;
  - status/warning propagation;
  - clear synthetic/generated/real-parser labeling.
- Confirm preview-rendered text is not automatically a full-text index.
- Confirm hex/raw previews are not full-text search content.

## Acceptance Criteria

- Stage 5 has an honest full-text decision.
- Docs do not imply full evidence keyword search unless reviewed text extraction exists.
- If contracts are added, they are JSON-safe and provenance-rich.
- No automatic text extraction, indexing, parser behavior, UI, reporting, or persistence is added unless a later ticket explicitly allows it.
- Full-text status in `functionality.md` remains accurate.

## Test Expectations

If documentation-only/deferred:

```powershell
python -m pytest
```

If contract code is added, add focused dependency-free tests and run the full suite.

## Documentation Updates

- Update forensic-core/API docs with full-text boundary.
- Update `functionality.md`, `plan.md`, `progression.md`, `review.md`, and `log/documentation.md`.
- Update ticket and Stage 5 README status.

## Review Checklist

- Does the ticket prevent overclaiming keyword/full-text coverage?
- Does it avoid preview-text-as-index behavior?
- Are real-parser, provider-backed, synthetic, and generated text sources distinguishable?
- Did it avoid extraction/indexing/persistence unless explicitly approved?

## Handoff Prompt

Use `prompts/vscode-agent/2026-07-15-s5-t15-full-text-search-reality-check.md`.
