# 2026-07-15 - S5-T12 File Metadata Timeline Assembly Prompt

Use this prompt only after S5-T11 is accepted.

```text
Implement ticket S5-T12: File Metadata Timeline Assembly.

Assemble timeline events from caller-supplied file metadata records only.

Before editing, read:
- tickets/stage-5/S5-T10-timestamp-normalization-contracts.md
- tickets/stage-5/S5-T11-timeline-event-contracts.md
- tickets/stage-5/S5-T12-file-metadata-timeline-assembly.md
- app/backend/forensic_core/timeline.py
- app/backend/forensic_core/search.py
- app/backend/forensic_core/filesystem_adapter.py
- app/tests/test_timeline_event_contracts.py
- Goal.md
- plan.md
- functionality.md
- progression.md
- review.md
- workflow.md

Before implementing:
- Summarize current timeline contracts.
- State the missing/invalid timestamp policy you will implement.
- List files you expect to modify.

Your task:
- Add a function that accepts explicit file metadata mappings or searchable records.
- Produce events for created, modified, accessed, and metadata_changed timestamp fields when available.
- Preserve missing/invalid timestamp states according to the documented policy.
- Carry file provenance, source kind, parser status, source warnings, synthetic/generated flags, and read-only assertion into every event.
- Return a timeline result container.
- Add dependency-free tests.
- Update docs and ticket status.
- Run python -m pytest and report the exact result.

Scope boundaries:
- Do not read directories, parse filesystems, extract content, run search, persist events, add API wrappers, UI, reports, parser behavior, commit, or push.
- Do not invent missing timestamps.

Final handoff:
- Summarize files changed.
- Summarize metadata timeline behavior.
- Report tests.
- State limitations and next ticket.

Stop after S5-T12 and hand off for review.
```
