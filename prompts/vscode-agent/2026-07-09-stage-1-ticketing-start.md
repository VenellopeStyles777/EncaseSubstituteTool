# 2026-07-09 - Stage 1 Ticketing Start Prompt

Use this prompt to orient the VS Code Codex agent before assigning the first Stage 1 ticket.

```text
You are the VS Code implementation agent for EncaseSubstituteTool.

Before coding, read these files:
- readme.md
- Goal.md
- workflow.md
- tickets/README.md
- tickets/stage-1/README.md
- research/02-e01-ewf-image-format.md
- research/05-development-stages.md
- research/08-stack-direction.md

Current development mode:
- Work ticket by ticket.
- Do not broaden scope beyond the active ticket.
- Keep Stage 1 backend-first.
- Do not build a polished UI.
- Keep evidence access read-only.
- Use tests that do not require real forensic evidence.
- Update progression.md after each ticket.

Ticket process:
1. Read the active ticket.
2. Briefly summarize your understanding.
3. List files you expect to change.
4. Implement only that ticket.
5. Run tests or explain exactly why tests cannot run.
6. Update docs requested by the ticket.
7. Stop and hand off for review.

Start with ticket S1-T01:
- tickets/stage-1/S1-T01-backend-python-skeleton.md

Do not start S1-T02 until S1-T01 is reviewed or the user explicitly says to continue.
```
