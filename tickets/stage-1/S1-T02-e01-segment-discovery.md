# S1-T02 - E01 Segment Discovery

Status: Ready

Stage: Stage 1 - E01 intake spike

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Implement logic that accepts a selected `.E01` path and discovers related segment files such as `.E02`, `.E03`, and later segments.

## Context To Read First

- `research/02-e01-ewf-image-format.md`
- `research/05-development-stages.md`
- `app/backend/forensic_core/README.md`
- `tickets/stage-1/S1-T01-backend-python-skeleton.md`

## Target Files/Folders

- `app/backend/forensic_core/`
- `app/tests/`

## Required Work

- Add segment discovery function/class.
- Validate that the input path looks like an E01 first segment.
- Discover sibling segment files with matching base name and ordered EWF segment extensions.
- Return a structured result with present segments and warnings.
- Include missing/gap warning behavior when appropriate.
- Do not open evidence for writing.

## Acceptance Criteria

- `.E01` input is accepted.
- Non-E01 input returns a clear unsupported/invalid result or raises a documented exception.
- Present sibling segments are returned in order.
- Missing segment/gap warnings are represented in structured data.
- Tests use temporary dummy files, not real evidence.

## Test Expectations

- Test single `.E01`.
- Test `.E01` + `.E02` + `.E03`.
- Test missing middle segment.
- Test unsupported extension.
- Test case-insensitive extension handling if implemented.

## Documentation Updates

- Update `app/backend/forensic_core/README.md`.
- Update `progression.md`.

## Review Checklist

- Does discovery avoid hard-coded evidence paths?
- Is output stable enough for a later JSON command?
- Is behavior clear when the segment set is incomplete?
- Are tests independent and small?

## Handoff Prompt

```text
Implement ticket S1-T02: E01 Segment Discovery.

Read research/02-e01-ewf-image-format.md, research/05-development-stages.md, app/backend/forensic_core/README.md, and the Stage 1 ticket README first.

Add backend logic that accepts a selected .E01 path and discovers related .E02/.E03/etc. sibling segments. Return structured data with ordered present segments and warnings for invalid input or gaps. Use temporary dummy files in tests; do not require real forensic evidence.

Update app/backend/forensic_core/README.md and progression.md. Run tests and report the result.
```
