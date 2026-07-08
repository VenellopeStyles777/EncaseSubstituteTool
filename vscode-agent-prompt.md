# VS Code Codex Agent Familiarization Prompt

Use this prompt when starting a fresh VS Code Codex chat for this project.

```text
You are joining the EncaseSubstituteTool project as the implementation agent. Your current assignment is Stage 1: E01 evidence intake. The following is for the preparation by helping you understand the scope of the project and stage 1 in particular, do not work on stage 1 yet.

Before editing code, read these files with high priority, while also familiarize with the overall directories:
1. readme.md
2. Goal.md
3. research.md
4. research/01-encase-functionality.md
5. research/02-e01-ewf-image-format.md
6. research/03-forensic-processes.md
7. research/04-architecture-components.md
8. research/05-development-stages.md
9. research/06-tools-plugins-skills.md
10. research/07-risks-assumptions.md
11. functionality.md
12. plan.md
13. progression.md
14. review.md
15. workflow.md

Project context:
- This app is an EnCase-like forensic analysis tool.
- The first supported evidence target is segmented EWF/EnCase image files: .E01, .E02, .E03, etc.
- The app must treat evidence files as read-only.
- The first implementation should prove evidence intake, not build the full UI.

Your Stage 1 deliverables:
- Create or complete the backend skeleton under app/backend/.
- Implement E01 segment discovery from a selected .E01 path.
- Define a clean EWF reader adapter interface.
- Use pyewf/libewf if available, but provide a stub/mock adapter so tests can pass without native dependencies.
- Return structured metadata and warning information.
- Draft or implement minimal SQLite case-store structures for cases, evidence sources, and audit events.
- Add an intake command or local API entry point.
- Add tests that do not require real forensic evidence.
- Update plan.md and progression.md with what changed and what remains blocked.

After reading the docs, briefly summarize your understanding and list the things that you suggest to implement or have that is needed for working on stage 1.
```
