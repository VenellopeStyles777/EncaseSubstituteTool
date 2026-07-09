# 2026-07-09 - S1-T06 Docs And Review Handoff Prompt

Use this prompt to hand S1-T06 to the VS Code implementation agent.

```text
Implement ticket S1-T06: Docs And Review Handoff.

Before editing, read these files:
- tickets/stage-1/S1-T06-docs-review-handoff.md
- tickets/stage-1/README.md
- Goal.md
- readme.md
- plan.md
- progression.md
- review.md
- workflow.md
- app/backend/README.md
- app/backend/api/README.md
- app/backend/forensic_core/README.md
- app/backend/case_store/README.md
- app/docs/environment-readiness.md

Context:
- S1-T01/S1-T01A through S1-T05 are implemented, reviewed, committed, pushed, and reported merged.
- Current focus is only S1-T06.
- This is documentation and final Stage 1 handoff, not new feature work.
- Do not add new backend features unless fixing a documentation/test-command issue absolutely requires a tiny code adjustment.
- Do not start Stage 2.

Your task:
- Ensure setup/test commands are documented and current.
- Ensure Stage 1 capabilities are described honestly:
  - backend Python skeleton
  - E01 segment discovery
  - EWF reader adapter boundary
  - intake JSON command/callable
  - SQLite case-store schema
- Ensure current limitations are clear:
  - no real EWF byte parsing yet
  - no filesystem parsing yet
  - no UI yet
  - no automatic persistence from intake yet
  - pyewf/libewf optional and not required for tests
  - no real evidence required
- Update plan.md and/or tickets/stage-1/README.md if statuses are stale.
- Update progression.md with an S1-T06 handoff entry.
- Update review.md with a concise Stage 1 final review checklist/handoff section.
- Run python -m pytest and report the result.

Deliverable:
- Documentation is ready for the research/review agent to perform final Stage 1 review.
- Include a short handoff summary listing changed docs, test result, and any remaining known limitations.

Stop after S1-T06 and hand off for review. Do not begin Stage 2.
```
