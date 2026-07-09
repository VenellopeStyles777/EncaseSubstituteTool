# S2-T06 - Raw/Text/Hex Preview Foundation

Status: Ready

Stage: Stage 2 - Volume and filesystem browsing MVP

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Add a safe preview foundation for small file content from a fixture/stub file entry.

## Required Work

- Define preview request/result structures.
- Support bounded byte previews and hex/text rendering for tests.
- Enforce size limits and clear truncation status.
- Preserve source provenance in preview results.

## Acceptance Criteria

- Tests cover text preview, hex preview, truncation, and unsupported/missing file behavior.
- Preview reads are bounded and read-only.

## Handoff Prompt

```text
Implement S2-T06: Raw/Text/Hex Preview Foundation. Keep reads bounded, read-only, and fixture/stub based.
```
