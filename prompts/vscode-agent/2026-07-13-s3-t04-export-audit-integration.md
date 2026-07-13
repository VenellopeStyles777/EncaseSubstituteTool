# 2026-07-13 - S3-T04 Export Audit Integration Prompt

Use this prompt to hand S3-T04 to the Stage 3 VS Code implementation agent.

```text
Implement ticket S3-T04: Case-Store Audit Integration For Exports.

Before editing, read these files:
- prompts/vscode-agent/2026-07-13-stage-3-familiarization.md
- tickets/stage-3/S3-T01-export-manifest-contract.md
- tickets/stage-3/S3-T02-file-export-service.md
- tickets/stage-3/S3-T03-export-hashing.md
- tickets/stage-3/S3-T04-export-audit-integration.md
- tickets/stage-3/README.md
- Goal.md
- plan.md
- functionality.md
- progression.md
- review.md
- workflow.md
- app/backend/api/file_export.py
- app/backend/forensic_core/export_manifest.py
- app/backend/case_store/schema.py
- app/backend/case_store/README.md
- app/tests/test_file_export.py
- app/tests/test_case_store_schema.py
- app/backend/api/README.md

Context:
- S3-T01 through S3-T03 are reviewed and done.
- S3-T02 writes explicit provider-backed export bytes and a sibling manifest.
- S3-T03 verifies the written export artifact with SHA-256 and on-disk byte count.
- The case store already has `audit_events`, `insert_audit_event()`, and `list_audit_events()`.
- S3-T04 is audit integration only. It is not deleted recovery, reporting, UI, real parser work, automatic persistence for other API calls, or Stage 4 hash/signature analysis.

Before implementing:
- Summarize your understanding of S3-T04.
- List the files you expect to create or modify.
- If you see a conflict between this prompt and the ticket, pause and explain it instead of broadening scope.

Your task:
- Add optional case-store audit logging for export attempts.
- Audit must run only when the caller explicitly supplies audit context. Do not treat `source.case_id` or `source.evidence_id` alone as permission to write to the case store.
- Prefer a small explicit audit context object or equivalent explicit parameters. A recommended shape is:
  - database connection or audit callback/helper;
  - required `case_id`;
  - optional `evidence_id`;
  - optional `actor`;
  - optional `audit_failed_exports`, defaulting to false.
- Use the existing `insert_audit_event()` helper unless a small wrapper is clearly useful.
- Prefer no schema migration. The existing `audit_events` table should be enough for `action="file_export"` plus structured `details_json`.
- `export_file()` should keep working exactly as a standalone export when no audit context is supplied.
- `export_file_to_json()` should either pass through the same explicit audit context or be deliberately documented as unaudited. Prefer pass-through consistency.

Audit details should include:
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

Failed export behavior:
- By default, do not audit failed exports unless the explicit audit context requests it.
- When failed exports are audited, the audit details must clearly show a non-ok status and must not look like a completed export.
- Do not delete successful export artifacts just because audit logging was requested.
- If audit persistence itself fails, do not silently claim that auditing succeeded. Either let the database exception surface or return a clearly structured audit warning/status; keep this choice small, documented, and tested if implemented.

Tests to add or update:
- successful stub export with explicit audit context creates one `audit_events` row;
- audit row uses action `file_export` and preserves case/evidence ids;
- audit details JSON includes provenance, destination, output path, manifest path, byte counts, SHA-256/hash status, export status, provider/content-source identity, and warnings;
- standalone export without audit context creates no audit row;
- source provenance `case_id`/`evidence_id` without explicit audit context does not create an audit row;
- failed export is not audited by default;
- failed export is audited when explicitly requested and details are clearly non-success;
- existing S3-T02/S3-T03 overwrite, cleanup, hash, byte-count, manifest, and destination-safety tests still pass;
- use in-memory SQLite only.

Scope boundaries:
- Do not add automatic case creation.
- Do not insert evidence sources automatically.
- Do not persist intake, directory listing, preview, or hash-analysis actions.
- Do not add deleted-file recovery, UI, reporting, bookmarks, notes, known-file matching, file signatures, extension mismatch checks, image verification, real EWF parsing, real partition parsing, real filesystem parsing, or required native dependencies.
- Do not hash preview-rendered text or hex.
- Do not commit or push.

Documentation updates:
- app/backend/case_store/README.md
- app/backend/api/README.md
- functionality.md
- plan.md
- progression.md
- review.md
- tickets/stage-3/README.md
- tickets/stage-3/S3-T04-export-audit-integration.md

Run:
- python -m pytest

Stop after S3-T04 and hand off for review. Do not begin S3-T05.
```
