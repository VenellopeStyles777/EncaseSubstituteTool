# S5-T12 - File Metadata Timeline Assembly

Status: Draft

Stage: Stage 5 - timeline foundations

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Assemble timeline events from explicit file metadata records, including MACB-style timestamp fields where present, without parsing evidence or inventing missing timestamps.

This ticket consumes caller-supplied file metadata records only.

## Entry Requirements

- S5-T11 accepted.

## Context To Read First

- `tickets/stage-5/S5-T10-timestamp-normalization-contracts.md`
- `tickets/stage-5/S5-T11-timeline-event-contracts.md`
- `app/backend/forensic_core/timeline.py`
- `app/backend/forensic_core/search.py`
- `app/backend/forensic_core/filesystem_adapter.py`
- `app/tests/test_timeline_event_contracts.py`
- `Goal.md`
- `plan.md`
- `functionality.md`
- `progression.md`
- `review.md`
- `workflow.md`

## Target Files/Folders

Likely files to modify:

- `app/backend/forensic_core/timeline.py`
- `app/backend/forensic_core/__init__.py`
- `app/tests/test_file_metadata_timeline.py`
- `app/backend/forensic_core/README.md`
- `functionality.md`
- `plan.md`
- `progression.md`
- `review.md`
- `tickets/stage-5/README.md`
- `tickets/stage-5/S5-T12-file-metadata-timeline-assembly.md`

## Required Work

- Add a function that accepts explicit file metadata mappings or searchable records.
- Produce timeline events for available file timestamp fields:
  - created;
  - modified;
  - accessed;
  - metadata_changed.
- Preserve missing timestamp fields as either omitted events with summary warnings or explicit unknown events, choosing one policy and documenting it.
- Preserve invalid timestamp fields as visible invalid timestamp events or warnings.
- Carry file provenance, source kind, parser status, source warnings, synthetic/generated flags, and read-only assertion into every event.
- Keep event labels concise and deterministic.
- Return a timeline result container from S5-T11.
- Do not read directories, parse filesystems, extract content, run search, or persist events.

## Acceptance Criteria

- File metadata records produce timeline events from available timestamp fields.
- Missing and invalid timestamps are visible according to the documented policy.
- Events preserve source provenance and source uncertainty.
- Synthetic/stub/provider-backed records remain labeled.
- No parser, search, persistence, UI, report, or case-store behavior is added.
- Tests are dependency-free.

## Test Expectations

Add tests for:

- event generation for all four file timestamp kinds;
- missing timestamp policy;
- invalid timestamp policy;
- synthetic/stub provenance preservation;
- file id/path/name preservation;
- result container counts/warnings;
- no mutation of input records.

Run:

```powershell
python -m pytest
```

## Documentation Updates

- Update forensic-core docs with file metadata timeline behavior and limits.
- Update `functionality.md`, `plan.md`, `progression.md`, and `review.md`.
- Update ticket and Stage 5 README status.

## Review Checklist

- Does timeline assembly consume explicit records only?
- Does it avoid inventing timestamps?
- Are unsupported/synthetic/parser status fields preserved?
- Did no search/UI/reporting/persistence behavior sneak in?

## Handoff Prompt

Use `prompts/vscode-agent/2026-07-15-s5-t12-file-metadata-timeline-assembly.md`.
