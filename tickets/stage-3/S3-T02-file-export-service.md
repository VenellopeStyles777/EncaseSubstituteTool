# S3-T02 - Fixture/Stub File Export Service

Status: Draft

Stage: Stage 3 - Export and recovery foundation

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Export a selected fixture/stub file to an examiner-selected output directory without modifying source/evidence paths.

## Acceptance Criteria

- Tests export small fixture/stub content.
- Export refuses or warns if destination overlaps source/evidence directory.
- Export result includes manifest path and provenance.

## Handoff Prompt

```text
Implement S3-T02: Fixture/Stub File Export Service. Keep source paths read-only and do not add recovery yet.
```
