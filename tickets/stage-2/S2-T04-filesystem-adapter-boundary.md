# S2-T04 - Filesystem Adapter Boundary

Status: Done

Stage: Stage 2 - Volume and filesystem browsing MVP

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Create the filesystem adapter boundary for listing files from a volume, with dependency-safe behavior for missing `pytsk3`.

## Required Work

- Define filesystem adapter protocol/result structures.
- Add a stub filesystem adapter for deterministic tests.
- Add optional pytsk3 adapter skeleton that reports dependency-unavailable when missing.
- Include filesystem type/status/warnings and read-only assertion.

## Acceptance Criteria

- Tests pass without `pytsk3`.
- Stub adapter returns predictable root directory data.
- Missing dependency behavior is structured, not a raw import crash.

## Handoff Prompt

```text
Implement S2-T04: Filesystem Adapter Boundary. Add stub and pytsk3-unavailable behavior only; do not build full browser workflows yet.
```
