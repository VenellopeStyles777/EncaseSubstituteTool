# S5-T02 - Input Inventory And Provenance Audit

Status: Draft

Stage: Stage 5 - documentation cleanup, then search and timeline

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Inventory the exact record shapes Stage 5 search and timeline may consume, and document the provenance/status fields that must survive every later ticket.

This ticket is documentation and design only. It should not implement search, filters, timeline assembly, indexing, persistence, UI, reporting, parser behavior, or new evidence handling.

## Entry Requirements

- S5-T00 accepted.
- S5-T01 gate passed.
- Stage 4.5 first-testing implementation runway completed and reviewed, unless the user has explicitly rewritten the project order.

## Context To Read First

- `tickets/stage-5/README.md`
- `tickets/stage-5/S5-T01-readiness-and-stage-4.5-completion-gate.md`
- `tickets/stage-4.5/README.md`
- `app/backend/api/directory_listing.py`
- `app/backend/forensic_core/filesystem_adapter.py`
- `app/backend/forensic_core/content_analysis.py`
- `app/backend/api/file_export.py`
- `app/backend/forensic_core/export_manifest.py`
- `app/backend/case_store/schema.py`
- `Goal.md`
- `readme.md`
- `plan.md`
- `functionality.md`
- `progression.md`
- `review.md`
- `workflow.md`

## Target Files/Folders

Likely files to modify:

- `tickets/stage-5/S5-T02-input-inventory-and-provenance-audit.md`
- `tickets/stage-5/README.md`
- `plan.md`
- `progression.md`
- `review.md`
- `log/documentation.md`
- `app/backend/forensic_core/README.md`
- `app/backend/api/README.md`

Do not create Stage 5 search/timeline source modules in this ticket.

## Required Work

- Inventory available record families:
  - directory listing responses;
  - `FilesystemEntry` dictionaries;
  - first-testing file-list JSON records if implemented;
  - Stage 4 hash results;
  - Stage 4 signature results;
  - Stage 4 extension mismatch results;
  - Stage 4 known-file match results;
  - Stage 3 export results/manifests;
  - case-store audit events;
  - first-testing run manifests.
- For each family, document:
  - schema version;
  - status field shape;
  - warning field shape;
  - source path and redaction considerations;
  - case/evidence/volume/file identifiers;
  - parser/provider/source-kind fields;
  - timestamp fields;
  - whether records can be real parser-backed, synthetic, generated, stubbed, dependency-unavailable, partial, unsupported, or failed.
- Define the minimum provenance fields Stage 5 records must preserve.
- Define which record families are allowed as search inputs in S5-T03 through S5-T09.
- Define which record families are allowed as timeline inputs in S5-T10 through S5-T14.
- Identify any missing fields that must be copied into Stage 5 result contracts rather than invented.
- Identify privacy-sensitive fields that should be redacted in shared summaries.

## Acceptance Criteria

- A future coding agent can see exactly what Stage 5 may consume.
- The audit distinguishes real parser-backed records from synthetic/provider-backed/stub records.
- The audit preserves unsupported, dependency-unavailable, partial, failed, skipped, and unknown states.
- The audit does not claim Stage 5 has a persistent index or broad parser support.
- No app source behavior changes.

## Test Expectations

Run:

```powershell
python -m pytest
```

This is documentation/design work, but the suite should still be recorded unless the reviewer accepts a no-test note.

## Documentation Updates

- Update `app/backend/forensic_core/README.md` and/or `app/backend/api/README.md` with Stage 5 input-boundary notes.
- Update `progression.md`, `review.md`, and `log/documentation.md`.
- Update `tickets/stage-5/README.md` if ticket readiness changes.

## Review Checklist

- Are all allowed Stage 5 input record families named?
- Are provenance fields specific enough for later implementation?
- Are synthetic/generated/stub/real-parser distinctions preserved?
- Are missing Stage 4.5 outputs treated as blockers instead of silently ignored?
- Does this ticket avoid implementing search/timeline behavior?

## Handoff Prompt

Use `prompts/vscode-agent/2026-07-15-s5-t02-input-inventory-and-provenance-audit.md`.
