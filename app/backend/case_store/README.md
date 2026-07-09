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
