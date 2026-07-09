# S1-T05 - Minimal Case Store Schema

Status: Ready

Stage: Stage 1 - E01 intake spike

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Create a minimal SQLite-oriented schema direction for cases, evidence sources, and audit events.

## Context To Read First

- `research/03-forensic-processes.md`
- `research/04-architecture-components.md`
- `app/backend/case_store/README.md`

## Target Files/Folders

- `app/backend/case_store/`
- `app/tests/`
- `app/docs/`

## Required Work

- Define minimal tables or a schema document for:
  - cases
  - evidence_sources
  - audit_events
- Include fields needed for provenance and read-only source tracking.
- Add migration/setup structure if implementation already has enough shape.
- Add tests if schema is executable.

## Acceptance Criteria

- Case/evidence/audit concepts are represented clearly.
- Evidence source records can store original path, segment metadata, adapter status, verification status, and timestamps.
- Audit events can record who/what/when/action/details at a basic level.
- Schema is documented even if not fully wired into the intake command yet.

## Test Expectations

- If executable schema exists, test creating tables in an in-memory or temporary SQLite database.
- If only a design doc exists, explain why implementation was deferred.

## Documentation Updates

- Update `app/backend/case_store/README.md`.
- Update `app/docs/` if a schema design file is created.
- Update `progression.md`.

## Review Checklist

- Does the schema preserve provenance?
- Does it avoid storing only UI-friendly data while losing forensic context?
- Is future migration/versioning considered?
- Are timestamp fields clear?

## Handoff Prompt

```text
Implement ticket S1-T05: Minimal Case Store Schema.

Read research/03-forensic-processes.md, research/04-architecture-components.md, and app/backend/case_store/README.md first.

Create a minimal SQLite-oriented schema or schema implementation for cases, evidence_sources, and audit_events. Include provenance fields needed for E01 intake results. Add tests if the schema is executable.

Update app/backend/case_store/README.md, any schema docs, and progression.md. Run tests if applicable and report results.
```
