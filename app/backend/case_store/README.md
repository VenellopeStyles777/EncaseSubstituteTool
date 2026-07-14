# Case Store

Purpose: case database and persistence layer.

Stage 1 target:

- Draft minimal schema for cases, evidence sources, and audit events.
- Use SQLite unless the implementation agent finds a strong reason to choose differently.

## S1-T05 Minimal SQLite Schema

`schema.py` provides an executable SQLite foundation using Python's built-in `sqlite3`.

Tables:

- `cases`: case id, name, description, created/updated timestamps.
- `evidence_sources`: evidence id, case id, original selected/source path, source type, intake status, segment count, segment discovery JSON, adapter name/dependency JSON, metadata JSON, verification status/JSON, warnings JSON, read-only assertion, timestamps.
- `audit_events`: audit event id, case id, optional evidence id, action, actor, details JSON, timestamp.
- `schema_migrations`: current schema version marker for later migration work.

Basic usage:

```python
from app.backend.case_store import (
    connect,
    initialize_schema,
    insert_case,
    insert_evidence_source,
    insert_audit_event,
)

connection = connect(":memory:")
initialize_schema(connection)
case_id = insert_case(connection, name="Example Case")
```

S1-T05 does not automatically persist S1-T04 intake results. Callers can explicitly pass an intake result dict to `insert_evidence_source()` when a case workflow is ready.

## S3-T04 Export Audit Integration

The Stage 3 export API can optionally write export audit events through the existing `audit_events` table. No schema migration is required.

`app.backend.api.ExportAuditContext` wraps the explicit audit inputs:

- SQLite connection;
- required case id;
- optional evidence id;
- optional actor;
- `audit_failed_exports`, defaulting to false.

When an export is audited, `insert_audit_event()` is called with `action="file_export"` and structured details JSON. Details include export status, source provenance, audit context ids, destination/output/manifest paths, byte counts, SHA-256/hash status, destination status, content-source identity, and warnings.

Standalone exports do not write audit rows. Source provenance `case_id` and `evidence_id` fields are preserved in results and audit details when present, but they do not trigger persistence unless an explicit `ExportAuditContext` is supplied.

Current limits:

- No migration runner beyond the initial `schema_migrations` marker.
- No automatic case creation or intake persistence in the CLI.
- No automatic evidence-source creation from exports.
- No analysis-result, bookmark, note, export-artifact, or report tables yet.
- Audit timestamps use UTC ISO strings with second precision.
