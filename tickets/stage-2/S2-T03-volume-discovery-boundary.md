# S2-T03 - Volume Discovery Boundary

Status: Ready

Stage: Stage 2 - Volume and filesystem browsing MVP

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Define structured volume discovery results for later partition parsing while allowing simple whole-image fixture behavior.

## Required Work

- Add volume result structures.
- Support a stub or whole-image volume discovery path for tests.
- Include offsets, size, volume id, source image id/path, and warnings.
- Leave real partition-table parsing optional/deferred unless a tiny fixture makes it safe.

## Acceptance Criteria

- Tests cover whole-image volume result shape and unsupported parser/dependency behavior.
- Results are JSON-serializable.
- No filesystem browsing is implemented in this ticket.

## Handoff Prompt

```text
Implement S2-T03: Volume Discovery Boundary. Keep it structured and testable; do not implement filesystem listing yet.
```
