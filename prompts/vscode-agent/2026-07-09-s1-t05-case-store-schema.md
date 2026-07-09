# 2026-07-09 - S1-T05 Case Store Schema Prompt

Use this prompt to hand S1-T05 to the VS Code implementation agent.

```text
Implement ticket S1-T05: Minimal Case Store Schema.

Before coding, read these files:
- tickets/stage-1/S1-T05-case-store-schema.md
- tickets/stage-1/README.md
- research/03-forensic-processes.md
- research/04-architecture-components.md
- app/backend/case_store/README.md
- app/backend/api/intake.py
- app/backend/forensic_core/segment_discovery.py
- app/backend/forensic_core/ewf_reader.py
- progression.md
- review.md

Context:
- S1-T02 segment discovery is complete.
- S1-T03 EWF reader adapter boundary is complete.
- S1-T04 intake JSON command is complete and reviewed.
- Current focus is only S1-T05.
- Do not build UI.
- Do not parse real EWF bytes.
- Do not add filesystem parsing.
- Do not require real evidence files.

Your task:
- Create a minimal SQLite-oriented case-store schema under app/backend/case_store/.
- Represent at least:
  - cases
  - evidence_sources
  - audit_events
- Include provenance-oriented fields that can store or reference:
  - case id/name
  - evidence id
  - original selected/source path
  - discovered segment metadata or JSON
  - adapter name and dependency status
  - verification status
  - read-only assertion
  - timestamps
  - audit action/details
- Prefer a small executable schema module if reasonable, using Python's built-in sqlite3.
- Add tests using an in-memory or temporary SQLite database.
- Tests should verify table creation and basic insert/query behavior for cases, evidence_sources, and audit_events.
- Keep this as schema/storage foundation. Do not force S1-T04 intake command to persist automatically unless the ticket can do so cleanly without broadening scope.
- Update app/backend/case_store/README.md and progression.md.
- Run python -m pytest and report the result.

Stay within S1-T05. Stop after S1-T05 and hand off for review before S1-T06.
```
