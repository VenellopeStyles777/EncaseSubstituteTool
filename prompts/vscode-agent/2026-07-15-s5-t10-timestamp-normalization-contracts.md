# 2026-07-15 - S5-T10 Timestamp Normalization Contracts Prompt

Use this prompt only after S5-T09 is accepted, unless the reviewer explicitly starts timeline contracts earlier.

```text
Implement ticket S5-T10: Timestamp Normalization Contracts.

Define timestamp normalization structures and tests. Do not assemble timelines yet.

Before editing, read:
- tickets/stage-5/S5-T02-input-inventory-and-provenance-audit.md
- tickets/stage-5/S5-T03-searchable-record-contracts.md
- tickets/stage-5/S5-T10-timestamp-normalization-contracts.md
- app/backend/forensic_core/filesystem_adapter.py
- app/backend/forensic_core/content_analysis.py
- app/backend/forensic_core/export_manifest.py
- app/backend/case_store/schema.py
- Goal.md
- plan.md
- functionality.md
- progression.md
- review.md
- workflow.md

Before implementing:
- Confirm S5-T01 gate is still valid.
- Summarize timestamp fields discovered in S5-T02.
- List files you expect to create or modify.

Your task:
- Add Stage 5 timeline schema/version constants.
- Add timestamp status and warning structures.
- Add TimelineTimestamp or equivalent with raw value, normalized UTC value when safe, timestamp kind, timezone policy, precision, status, and warnings.
- Safely parse project UTC timestamps ending in Z.
- Preserve missing, unknown, invalid, and source-local timestamps distinctly.
- Avoid guessing time zones.
- Add dependency-free tests.
- Update docs and ticket status.
- Run python -m pytest and report the exact result.

Scope boundaries:
- Do not assemble timeline events.
- Do not sort/filter timelines.
- Do not parse filesystem-specific timestamp formats unless explicitly reviewed in this ticket.
- Do not add search behavior, parser behavior, persistence, UI, reports, commit, or push.

Final handoff:
- Summarize files changed.
- Summarize timestamp policy.
- Report tests.
- State limitations and next ticket.

Stop after S5-T10 and hand off for review.
```
