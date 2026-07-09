# 2026-07-09 - Stage 2 Familiarization Prompt

Use this prompt when starting a fresh VS Code Codex chat for Stage 2.

```text
You are joining the EncaseSubstituteTool project as the Stage 2 implementation agent.

Before editing code, familiarize yourself with the project. Read these files in order:
1. readme.md
2. Goal.md
3. plan.md
4. progression.md
5. review.md
6. workflow.md
7. tickets/README.md
8. tickets/stage-1/README.md
9. tickets/stage-2/README.md
10. research/02-e01-ewf-image-format.md
11. research/03-forensic-processes.md
12. research/04-architecture-components.md
13. research/05-development-stages.md
14. research/08-stack-direction.md
15. app/backend/README.md
16. app/backend/api/README.md
17. app/backend/forensic_core/README.md
18. app/backend/case_store/README.md
19. app/fixtures/README.md
20. app/docs/environment-readiness.md

Project context:
- This app is an EnCase-like forensic analysis tool.
- Stage 1 is complete.
- Stage 1 created the backend skeleton, E01 segment discovery, EWF reader adapter boundary, JSON intake command/callable, and SQLite case-store schema.
- Stage 1 intentionally does not parse real EWF bytes, parse partitions/filesystems, provide a UI, or automatically persist intake results.
- Tests currently do not require real evidence or native forensic dependencies.

Current Stage 2 goal:
- Build the backend foundation for volume/filesystem browsing.
- Stay backend-first.
- Do not build UI.
- Do not start export/recovery work; that is Stage 3.
- Do not start hashing/signature analysis; that is Stage 4.
- Do not require private evidence or large images.

Stage 2 should aim to add:
- fixture and dependency strategy;
- read-only image/byte-stream abstraction;
- volume discovery boundary;
- filesystem adapter boundary with dependency-safe behavior;
- directory listing and file metadata result shapes;
- raw/text/hex preview foundation;
- documentation and review handoff.

Important principles:
- Treat all source/evidence paths as read-only.
- Keep every result tied to provenance: source path, evidence/source id when available, volume id, file path/id, offsets when available, parser/adapter status, warnings, and timestamps where relevant.
- Missing native dependencies such as pytsk3 must produce structured status, not raw crashes.
- Use stubs or tiny generated fixtures for tests.
- Do not commit real forensic evidence.
- Keep each ticket small and reviewable.

Workflow:
- Work ticket by ticket.
- Start with S2-T01 only:
  tickets/stage-2/S2-T01-fixture-dependency-strategy.md
- Before implementing, summarize your understanding of Stage 2 and list the files you expect to modify.
- Implement only the active ticket.
- Run python -m pytest if code changes are made.
- Update progression.md and any docs requested by the ticket.
- Stop after the ticket and hand off for review.

Do not start S2-T02 until S2-T01 is reviewed or the user explicitly says to continue.
```
