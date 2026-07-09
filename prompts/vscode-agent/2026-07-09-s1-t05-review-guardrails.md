# 2026-07-09 - S1-T05 Review Guardrails

Use these guardrails if the VS Code implementation agent asks how far to take the case store.

```text
S1-T05 is the minimal SQLite schema foundation.

Do:
- use sqlite3 unless there is a strong reason not to
- create tables for cases, evidence_sources, and audit_events
- keep provenance fields visible
- support basic setup/initialization
- test table creation and basic insert/query behavior
- document schema intent

Do not:
- build a full ORM layer
- add migrations beyond a simple initial schema unless needed
- persist intake automatically if it complicates the ticket
- build UI
- parse real evidence
- add filesystem analysis
- commit real evidence files
```
