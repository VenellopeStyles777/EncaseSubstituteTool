# S5-T10 - Timestamp Normalization Contracts

Status: Draft

Stage: Stage 5 - timeline foundations

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Define timestamp normalization contracts for timeline work while preserving unknown, missing, invalid, source-local, and partial timestamp states.

This is a contract ticket. It must not assemble timelines, change search behavior, parse evidence, or invent timestamps.

## Entry Requirements

- S5-T09 accepted, or the reviewer explicitly starts timeline contracts after S5-T04 if search API wrappers are not needed yet.
- S5-T01 gate still valid.

## Context To Read First

- `tickets/stage-5/S5-T02-input-inventory-and-provenance-audit.md`
- `tickets/stage-5/S5-T03-searchable-record-contracts.md`
- `app/backend/forensic_core/filesystem_adapter.py`
- `app/backend/forensic_core/content_analysis.py`
- `app/backend/forensic_core/export_manifest.py`
- `app/backend/case_store/schema.py`
- `Goal.md`
- `plan.md`
- `functionality.md`
- `progression.md`
- `review.md`
- `workflow.md`

## Target Files/Folders

Likely files to create or modify:

- `app/backend/forensic_core/timeline.py`
- `app/backend/forensic_core/__init__.py`
- `app/tests/test_timeline_timestamp_contracts.py`
- `app/backend/forensic_core/README.md`
- `functionality.md`
- `plan.md`
- `progression.md`
- `review.md`
- `tickets/stage-5/README.md`
- `tickets/stage-5/S5-T10-timestamp-normalization-contracts.md`

## Required Work

- Define a Stage 5 timeline schema version, such as `stage5.timeline.v1`.
- Define timestamp status and warning structures.
- Define a `TimelineTimestamp` or equivalent structure with:
  - raw value;
  - normalized UTC value when safely parseable;
  - timestamp kind, such as created/modified/accessed/metadata_changed/exported/analyzed/audit;
  - source timezone policy;
  - precision when known;
  - status and warnings.
- Support safe parsing of ISO-like UTC timestamps already used by this project.
- Preserve values that cannot be parsed as `invalid_timestamp` or equivalent, not as `None` unless missing.
- Preserve missing/unknown timestamps with explicit status.
- Do not guess time zones for source-local filesystem timestamps.
- Do not normalize Windows FILETIME, Unix epoch, or filesystem-specific formats unless the implementation has explicit reviewed inputs and tests.

## Acceptance Criteria

- Timestamp contracts are importable and JSON-serializable.
- UTC project timestamps ending in `Z` normalize predictably.
- Missing, unknown, invalid, and source-local timestamps remain distinguishable.
- No timeline events or timeline assembly are implemented.
- Tests are dependency-free.

## Test Expectations

Add tests for:

- UTC `Z` timestamp parsing;
- timezone offset parsing if supported;
- missing timestamp status;
- unknown timestamp status;
- invalid timestamp status;
- source-local/no-timezone policy;
- JSON-safe output.

Run:

```powershell
python -m pytest
```

## Documentation Updates

- Update forensic-core docs with timestamp normalization policy.
- Update `functionality.md`, `plan.md`, `progression.md`, and `review.md`.
- Update ticket and Stage 5 README status.

## Review Checklist

- Does the contract avoid inventing or guessing timestamps?
- Are invalid and unknown timestamps visible?
- Does the ticket avoid event assembly and UI/reporting behavior?
- Are timezone assumptions documented?

## Handoff Prompt

Use `prompts/vscode-agent/2026-07-15-s5-t10-timestamp-normalization-contracts.md`.
