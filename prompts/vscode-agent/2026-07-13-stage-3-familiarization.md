# 2026-07-13 - Stage 3 Familiarization Prompt

Use this prompt when starting a fresh VS Code Codex chat for Stage 3.

```text
You are joining the EncaseSubstituteTool project as the Stage 3 implementation agent.

Before editing code, familiarize yourself with the project. Read these files in order:
1. prompts/stage-3-onboarding/stage-2-conclusion-and-stage-3-needs.md
2. prompts/stage-3-onboarding/project-review-agent-memo.md
3. Goal.md
4. readme.md
5. plan.md
6. functionality.md
7. progression.md
8. review.md
9. workflow.md
10. tickets/README.md
11. tickets/stage-2/README.md
12. tickets/stage-3/README.md
13. app/backend/README.md
14. app/backend/api/README.md
15. app/backend/forensic_core/README.md
16. app/backend/case_store/README.md
17. app/fixtures/README.md
18. app/docs/environment-readiness.md

Then inspect these Stage 2 code/test files so you understand what Stage 3 can safely build on:
- app/backend/api/file_preview.py
- app/backend/api/directory_listing.py
- app/backend/api/intake.py
- app/backend/forensic_core/filesystem_adapter.py
- app/backend/forensic_core/volume_discovery.py
- app/backend/forensic_core/image_stream.py
- app/backend/case_store/schema.py
- app/tests/test_file_preview.py
- app/tests/test_directory_listing.py
- app/tests/test_case_store_schema.py

Project context:
- This app is an EnCase-like forensic analysis tool.
- Stage 1 is complete.
- Stage 2 is complete at the backend foundation and documentation handoff level.
- Stage 2 provides dependency-safe intake, read-only local byte-stream behavior, whole-image volume results, stub filesystem metadata/listing, and provider-backed raw/text/hex preview.
- Stage 2 does not parse real EWF bytes, verify real images, parse real partition tables, parse real filesystems, extract real file content, or provide a UI/executable.
- Preview bytes are synthetic/provider-backed. They are not extracted from a real filesystem.
- Native forensic dependencies such as pyewf, libewf, pytsk3, and The Sleuth Kit remain optional and must not be required for default tests.

Current Stage 3 goal:
- Build safe export/recovery foundations.
- Start with contracts and manifests before writing exported files.
- Export only fixture/stub/provider-backed content until a real filesystem/content adapter exists.
- Preserve source provenance and source mutability assumptions in every export result and manifest.
- Write only to examiner-selected output directories, never source/evidence paths.
- Compute export byte counts and at least SHA-256 during Stage 3, after the export contract exists.
- Add optional case-store audit events only when case/evidence context is explicitly supplied.
- Keep deleted-file recovery documented as unsupported/deferred unless a future real adapter exposes recoverable deleted-file bytes.

Important Stage 3 risks:
- Do not let exported artifacts look more authoritative than their source.
- Do not use rendered preview text or hex as export bytes.
- Do not treat Stage 2 filesystem entries as byte-bearing objects.
- Do not write anywhere near source/evidence paths without explicit destination safety checks.
- Do not claim deleted-file recovery is implemented without a real adapter exposing recoverable content.
- Do not add UI, search, reporting, broad hash analysis, real parser work, or required native dependencies under Stage 3 export tickets.
- Do not commit real evidence, disk images, large binary fixtures, or private fixtures.

Ticket readiness note:
- The current Stage 3 tickets are starter placeholders.
- Do not begin S3-T01 implementation until the research/review agent expands the S3-T01 ticket and gives you a ticket-specific prompt.
- Your first task in this chat is familiarization only unless the user explicitly gives you an expanded Stage 3 ticket prompt.

Workflow:
- Work ticket by ticket.
- Before implementing any ticket, summarize your understanding and list the files you expect to create or modify.
- Implement only the active ticket.
- Run python -m pytest after code changes and report the exact result.
- Update progression.md and any docs requested by the active ticket.
- Keep manual-test status as Untested unless the user explicitly reports a manual workflow run.
- Stop after each ticket and hand off for review.
- Do not commit or push.

For this onboarding pass:
- Read the files above.
- Summarize Stage 2's true state.
- Summarize the Stage 3 export/recovery boundary.
- Identify any confusing or stale docs you notice.
- Wait for the expanded S3-T01 prompt before editing code.
```
