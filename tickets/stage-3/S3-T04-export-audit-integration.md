# S3-T04 - Case-Store Audit Integration For Exports

Status: Done

Stage: Stage 3 - Export and recovery foundation

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Record export actions in the case-store audit log only when explicit case/evidence context is supplied.

Standalone exports must continue to work without a database connection.

## Context To Read First

- `prompts/vscode-agent/2026-07-13-stage-3-familiarization.md`
- `prompts/vscode-agent/2026-07-13-s3-t04-export-audit-integration.md`
- `tickets/stage-3/S3-T01-export-manifest-contract.md`
- `tickets/stage-3/S3-T02-file-export-service.md`
- `tickets/stage-3/S3-T03-export-hashing.md`
- `tickets/stage-3/S3-T04-export-audit-integration.md`
- S3-T01 through S3-T03 reviewed implementation
- `app/backend/case_store/schema.py`
- `app/tests/test_case_store_schema.py`
- `app/backend/api/file_export.py`
- `app/tests/test_file_export.py`
- `app/backend/forensic_core/export_manifest.py`
- `app/backend/api/README.md`
- `app/backend/case_store/README.md`
- `Goal.md`
- `plan.md`
- `functionality.md`
- `progression.md`
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
- Prefer a small explicit audit context object or equivalent explicit parameters. A recommended shape is:
  - database connection or audit callback/helper;
  - required `case_id`;
  - optional `evidence_id`;
  - optional `actor`;
  - optional `audit_failed_exports` flag, defaulting to false.
- Audit integration must run only when the caller explicitly supplies audit context. Do not treat `source.case_id` or `source.evidence_id` alone as permission to write to the case store.
- Use the existing `insert_audit_event()` helper unless a small wrapper is clearly useful. Do not add a schema migration unless the current schema cannot support the required audit event.
- Recommended audit action name: `file_export`.
- Record audit details that include:
  - a schema/version label for export audit details;
  - export status code, ok flag, and message;
  - source path;
  - source file id/path/name;
  - source case/evidence ids when present in provenance;
  - audit context case/evidence ids;
  - volume id;
  - destination directory;
  - requested output path;
  - output path;
  - manifest path;
  - bytes requested;
  - bytes written;
  - SHA-256 and hash status when available;
  - destination status;
  - content-source/provider identity;
  - warnings.
- Failed exports may be audited only when explicitly requested, such as with `audit_failed_exports=True`. The action/details must clearly identify failure and must not look like a completed export.
- Standalone export without audit context must not write to the case store.
- `export_file_to_json()` should either accept the same audit context or deliberately remain unaudited with documentation. Prefer passing through the same explicit audit context for consistency.
- Audit integration must not change S3-T02/S3-T03 export safety: no output into evidence/source paths, no overwrite, no preview-rendered export bytes, no deleted recovery, and no broader hash/signature analysis.

## Acceptance Criteria

- Successful export can create an `audit_events` row when explicit context is provided.
- Standalone export creates no audit row.
- Failed export audit details are clearly non-success when failure auditing is enabled.
- Audit details include S3-T03 hash/byte-count verification fields for completed exports.
- `source.case_id`/`source.evidence_id` alone do not cause case-store writes without explicit audit context.
- Existing export result and manifest behavior remains unchanged except for optional audit side effects.
- Tests use in-memory SQLite.
- Existing case-store schema remains backward-compatible unless a deliberate migration is documented.

## Test Expectations

Tests should cover:

- audit row created for successful export with case/evidence context;
- no audit row without explicit audit context;
- audit details JSON includes provenance, destination, hash, byte count, status, and provider identity;
- failed export is not audited by default;
- failed export is audited when explicitly requested;
- failed export audit does not claim success;
- source provenance ids alone do not trigger auditing;
- standalone export still works without importing or initializing a database;
- existing S3-T02/S3-T03 export safety, overwrite, cleanup, hash, and manifest tests still pass;
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
- Audit details preserve source provenance and the S3-T03 export verification fields.
- Standalone exports do not require a database connection and do not write audit rows.
- The current case-store schema remains compatible unless a migration is deliberately documented and tested.
- No automatic intake/listing/preview persistence was added.
- No UI, reporting, real parser, deleted recovery, or Stage 4 analysis scope was added.

## Implementation Handoff - 2026-07-13

- Added explicit `ExportAuditContext` for opt-in export audit logging.
- Successful audited exports insert one `audit_events` row using the existing `insert_audit_event()` helper and `action="file_export"`.
- Audit details include export status, source provenance, audit context ids, destination/output/manifest paths, byte counts, SHA-256/hash status, destination status, content-source identity, and warnings.
- Standalone exports and source provenance ids alone do not create audit rows.
- Failed exports are not audited by default; `audit_failed_exports=True` records clearly non-ok details.
- No schema migration, automatic case/evidence creation, deleted recovery, UI, reporting, real parser work, or Stage 4 hash/signature analysis was added.

## Review Result - 2026-07-13

- Approved for commit.
- Review found no blocking issues.
- `python -m pytest` reported 99 passed in 3.19s.
- S3-T05 remains the next Stage 3 gate and should stay planning/research-focused unless real adapter support exists.

## Research/Review Handoff - 2026-07-13

- S3-T01 through S3-T03 are reviewed and done.
- `app/backend/case_store/schema.py` already has `insert_audit_event()`, `list_audit_events()`, and in-memory SQLite test coverage.
- S3-T04 should likely need no schema migration. The existing `audit_events` table can record `action="file_export"` with structured JSON details.
- The export service currently accepts `file_entry_or_request`, `output_directory`, optional provider, and optional output name. S3-T04 should add only explicit audit context and pass-through JSON behavior as needed.
- Source provenance may already carry optional `case_id` and `evidence_id`, but those fields alone are not permission to persist audit events.

## Handoff Prompt

```text
Implement S3-T04 only after S3-T03 is reviewed and accepted. Add optional case-store audit logging for exports when explicit audit context is supplied. Standalone exports must still work without database writes. Stop after S3-T04 and hand off for review.
```
