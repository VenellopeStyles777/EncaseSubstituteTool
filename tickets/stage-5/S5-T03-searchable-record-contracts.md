# S5-T03 - Searchable Record Contracts

Status: Draft

Stage: Stage 5 - search foundations

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Add Stage 5 searchable-record contracts that can represent file metadata, analysis results, export records, and future parser-backed records without losing provenance or source uncertainty.

This is a contract ticket. It may add a new module and focused tests, but it must not implement query matching, filters, persistence, indexing, UI, reporting, parser work, or full-text search.

## Entry Requirements

- S5-T01 gate passed.
- S5-T02 input inventory accepted.

## Context To Read First

- `tickets/stage-5/README.md`
- `tickets/stage-5/S5-T01-readiness-and-stage-4.5-completion-gate.md`
- `tickets/stage-5/S5-T02-input-inventory-and-provenance-audit.md`
- `app/backend/api/directory_listing.py`
- `app/backend/forensic_core/filesystem_adapter.py`
- `app/backend/forensic_core/content_analysis.py`
- `app/backend/forensic_core/export_manifest.py`
- `app/backend/forensic_core/README.md`
- `app/tests/test_directory_listing.py`
- `app/tests/test_content_analysis_contracts.py`
- `Goal.md`
- `plan.md`
- `functionality.md`
- `progression.md`
- `review.md`
- `workflow.md`

## Target Files/Folders

Likely files to create or modify:

- `app/backend/forensic_core/search.py`
- `app/backend/forensic_core/__init__.py`
- `app/tests/test_search_contracts.py`
- `app/backend/forensic_core/README.md`
- `functionality.md`
- `plan.md`
- `progression.md`
- `review.md`
- `tickets/stage-5/README.md`
- `tickets/stage-5/S5-T03-searchable-record-contracts.md`

## Required Work

- Define a Stage 5 search schema version, such as `stage5.search.v1`.
- Define JSON-friendly status and warning structures for search.
- Define a source/provenance structure that preserves:
  - case id;
  - evidence id;
  - source path;
  - selected path when available;
  - volume id, offset, and length;
  - file id/path/name;
  - filesystem type;
  - adapter/provider/parser name and version;
  - source kind;
  - read-only assertion;
  - synthetic/generated flags;
  - parser/source status;
  - source warnings.
- Define `SearchableRecord` or equivalent with:
  - stable record id;
  - record type, such as `file_metadata`, `hash_result`, `signature_result`, `extension_mismatch`, `known_file_match`, `export_result`, `audit_event`, or future `text_content`;
  - display name and path fields;
  - searchable string fields;
  - exact-match fields;
  - numeric fields;
  - timestamp fields as raw values only;
  - status and warnings;
  - source/provenance.
- Provide constructors/helpers from generic mappings only where safe and explicit.
- Preserve raw timestamps as strings without normalizing them yet. Timestamp normalization belongs to S5-T10.
- Provide `to_dict()` and JSON serialization helpers.

## Acceptance Criteria

- Searchable-record contracts are importable and JSON-serializable.
- Contracts can represent a Stage 2/4.5 file metadata entry without mutation.
- Contracts can represent Stage 4 analysis result metadata without reading bytes.
- Contracts preserve source kind, synthetic/generated flags, status, warnings, and read-only assertions.
- No query matching or timeline behavior is implemented.
- Default tests pass without real evidence, native dependencies, network access, or large fixtures.

## Test Expectations

Add focused tests under `app/tests/`.

Tests should cover:

- status/warning serialization;
- file-metadata record creation from a mapping;
- analysis-result-shaped record creation from explicit fields;
- preservation of source kind and warnings;
- JSON-safe output;
- no byte content in record JSON;
- raw timestamp fields carried without normalization.

Run:

```powershell
python -m pytest
```

## Documentation Updates

- Update backend forensic-core docs with the Stage 5 search contract boundary.
- Update `functionality.md`, `plan.md`, `progression.md`, and `review.md`.
- Update this ticket and `tickets/stage-5/README.md` to `Review` when implementation is complete.

## Review Checklist

- Does the contract preserve provenance and uncertainty?
- Does it avoid treating metadata-only entries as file content?
- Does it avoid full-text search?
- Does it avoid persistence/indexing?
- Are synthetic/generated/provider-backed records labeled honestly?
- Are tests dependency-free?

## Handoff Prompt

Use `prompts/vscode-agent/2026-07-15-s5-t03-searchable-record-contracts.md`.
