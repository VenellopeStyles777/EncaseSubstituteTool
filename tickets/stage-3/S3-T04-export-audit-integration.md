# S3-T04 - Case-Store Audit Integration For Exports

Status: Draft

Stage: Stage 3 - Export and recovery foundation

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Record export actions in the case-store audit log when case/evidence context is available.

## Acceptance Criteria

- Export actions can create `audit_events`.
- Tests verify audit event details include export status, source, destination, hash, and byte count.
- Export still works without case-store context when used as a standalone service.

## Handoff Prompt

```text
Implement S3-T04: Case-Store Audit Integration For Exports. Keep it optional and test with in-memory SQLite.
```
