# S2-T02 - Image Byte-Stream Abstraction

Status: Done

Stage: Stage 2 - Volume and filesystem browsing MVP

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Create a read-only byte-stream abstraction that can be backed by a tiny local fixture now and by real EWF readers later.

## Required Work

- Add an interface or small class for read-only image byte access.
- Support a simple local file-backed implementation for tests.
- Return structured errors for unreadable/missing paths.
- Include provenance fields such as source path, size, and read-only assertion.
- Do not parse partitions or filesystems yet.

## Acceptance Criteria

- Tests cover read ranges, missing files, and read-only behavior.
- No real E01 evidence is required.
- The abstraction is separate from filesystem parsing.

## Handoff Prompt

```text
Implement S2-T02: Image Byte-Stream Abstraction. Add read-only file-backed tests, but do not add volume or filesystem parsing yet.
```
