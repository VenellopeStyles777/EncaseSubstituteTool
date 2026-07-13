# S3-T04 - Case-Store Audit Integration For Exports

Status: Draft

Stage: Stage 3 - Export and recovery foundation

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Record export actions in the case-store audit log only when explicit case/evidence context is supplied.

Standalone exports must continue to work without a database connection.

## Context To Read First

- S3-T01 through S3-T03 tickets and reviewed implementation
- `app/backend/case_store/schema.py`
- `app/tests/test_case_store_schema.py`
- `app/backend/api/file_export.py`
- `app/backend/forensic_core/export_manifest.py`
- `app/backend/case_store/README.md`
- `review.md`
- `workflow.md`

## Target Files/Folders

Likely files to modify:

- `app/backend/api/file_export.py`
- `app/backend/case_store/schema.py` only if a helper is truly useful
- `app/tests/test_file_export.py`
- `app/tests/test_case_store_schema.py` if schema/helper changes occur
- `app/backend/case_store/README.md`
- `app/backend/api/README.md`
- `functionality.md`
- `plan.md`
- `progression.md`
- `review.md`
- `tickets/stage-3/README.md`
- `tickets/stage-3/S3-T04-export-audit-integration.md`

## Required Work

- Add optional audit integration to the export workflow.
- Audit integration should run only when the caller explicitly supplies:
  - database connection or audit callback/helper;
  - case id;
  - evidence id when available.
- Record audit details that include:
  - export status;
  - source path;
  - source file id/path/name;
  - volume id;
  - destination/output path;
  - manifest path;
  - byte count;
  - SHA-256 when available;
  - content-source/provider identity;
  - warnings.
- Failed exports may be audited if explicitly requested, but the action/details must clearly identify failure and must not look like a completed export.
- Standalone export without audit context must not write to the case store.

## Acceptance Criteria

- Successful export can create an `audit_events` row when explicit context is provided.
- Standalone export creates no audit row.
- Failed export audit details are clearly non-success when failure auditing is enabled.
- Tests use in-memory SQLite.
- Existing case-store schema remains backward-compatible unless a deliberate migration is documented.

## Test Expectations

Tests should cover:

- audit row created for successful export with case/evidence context;
- no audit row without explicit audit context;
- audit details JSON includes provenance, destination, hash, byte count, status, and provider identity;
- failed export audit does not claim success;
- in-memory SQLite remains sufficient.

Run:

```powershell
python -m pytest
```

## Documentation Updates

- Update `app/backend/case_store/README.md`.
- Update `app/backend/api/README.md`.
- Update `functionality.md`, `plan.md`, `progression.md`, `review.md`, and ticket statuses.

## Review Checklist

- Audit writes are explicit and optional.
- Failed exports are not recorded as successful.
- No automatic intake/listing/preview persistence was added.
- No UI, reporting, real parser, deleted recovery, or Stage 4 analysis scope was added.

## Handoff Prompt

```text
Implement S3-T04 only after S3-T03 is reviewed and accepted. Add optional case-store audit logging for exports when explicit case/evidence context is supplied. Standalone exports must still work without database writes. Stop after S3-T04 and hand off for review.
```
