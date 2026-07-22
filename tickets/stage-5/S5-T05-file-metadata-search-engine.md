# S5-T05 - File Metadata Search Engine

Status: Draft

Stage: Stage 5 - search foundations

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Implement dependency-free in-memory search over explicit file metadata `SearchableRecord` inputs.

This ticket covers filename/path/metadata search only. It must not search file content, build persistent indexes, parse real filesystems, read evidence bytes, or imply broader coverage than the records supplied by the caller.

## Entry Requirements

- S5-T04 accepted.
- S5-T01 gate still valid.

## Context To Read First

- `tickets/stage-5/S5-T03-searchable-record-contracts.md`
- `tickets/stage-5/S5-T04-search-query-filter-sort-contracts.md`
- `app/backend/forensic_core/search.py`
- `app/tests/test_search_contracts.py`
- `app/tests/test_search_query_contracts.py`
- `app/backend/api/directory_listing.py`
- `app/backend/forensic_core/filesystem_adapter.py`
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
- `app/tests/test_file_metadata_search.py`
- `app/backend/forensic_core/README.md`
- `functionality.md`
- `plan.md`
- `progression.md`
- `review.md`
- `tickets/stage-5/README.md`
- `tickets/stage-5/S5-T05-file-metadata-search-engine.md`

## Required Work

- Add a pure in-memory search function over a sequence of `SearchableRecord` values.
- Support text matching over explicit fields such as:
  - file name;
  - file path;
  - extension;
  - display name;
  - selected metadata fields from the record contract.
- Support `contains`, `exact`, and `prefix` match modes if they are in S5-T04.
- Apply field selection, case sensitivity, and structured invalid-query behavior.
- Apply metadata filters for:
  - record type `file_metadata`;
  - status code;
  - source kind;
  - synthetic/generated flags;
  - parser/provider/adapter names;
  - entry type;
  - extension.
- Preserve all record provenance in result items.
- Add matched-field summaries without exposing file content.
- Return structured warning(s) when supplied records are synthetic/generated/stub/provider-backed.
- Return `no_matches` as a successful search result with zero records, not as an error.
- Do not recurse into directories or read files. The caller supplies records.

## Acceptance Criteria

- Filename and path searches work over explicit metadata records.
- Metadata filters narrow results predictably.
- Search results preserve provenance/status/warnings/source kind.
- Synthetic/generated/stub records remain labeled.
- The implementation does not read evidence bytes or file content.
- The implementation does not add persistence, indexing, UI, timeline, parser behavior, or full-text search.
- Tests are dependency-free.

## Test Expectations

Add tests for:

- contains/exact/prefix matching;
- case-sensitive and case-insensitive matching;
- field-restricted search;
- extension and entry-type filters;
- status/source-kind filters;
- synthetic/generated warning preservation;
- no-match result;
- invalid query result;
- provenance preservation.

Run:

```powershell
python -m pytest
```

## Documentation Updates

- Update forensic-core docs with file metadata search scope and limits.
- Update `functionality.md`, `plan.md`, `progression.md`, and `review.md`.
- Update ticket status to `Review` when complete.

## Review Checklist

- Search consumes explicit records only.
- Search output does not imply full evidence coverage unless records are real parser-backed and labeled.
- No file-content/full-text search was added.
- No persistent index or background job was added.
- Synthetic/provider-backed labels remain visible.

## Handoff Prompt

Use `prompts/vscode-agent/2026-07-15-s5-t05-file-metadata-search-engine.md`.
