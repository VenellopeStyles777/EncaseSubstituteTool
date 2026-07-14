# 2026-07-14 - Stage 4 Familiarization Prompt

Use this prompt when starting a fresh VS Code Codex implementation chat for Stage 4.

This is the coding-agent succession/onboarding prompt. Keep it separate from the Stage 4 research/review-agent packet in `prompts/stage-4-onboarding/`; the two agents should carry different reflections and responsibilities.

```text
You are joining the EncaseSubstituteTool project as the Stage 4 implementation agent.

Before editing code, familiarize yourself with the whole project. This is not a quick skim: read the planning docs, ticket history, backend code, tests, fixtures/dependency notes, and review findings so you understand both what exists and what is still fake, stubbed, deferred, or risky.

Read these files first:
1. readme.md
2. Goal.md
3. plan.md
4. functionality.md
5. progression.md
6. review.md
7. workflow.md
8. tickets/README.md
9. tickets/stage-1/README.md
10. tickets/stage-2/README.md
11. tickets/stage-3/README.md
12. tickets/stage-4/README.md
13. app/backend/README.md
14. app/backend/api/README.md
15. app/backend/forensic_core/README.md
16. app/backend/case_store/README.md
17. app/fixtures/README.md
18. app/docs/environment-readiness.md
19. log/documentation.md

Then inspect the backend implementation and tests:
- app/backend/forensic_core/
- app/backend/api/
- app/backend/case_store/
- app/tests/

Use `rg --files app tickets prompts research log` or the equivalent file explorer view to make sure you understand the project shape. Pay special attention to:
- tests that define current behavior;
- status/warning names already in use;
- places where docs explicitly say behavior is synthetic, stubbed, unsupported, deferred, or not real evidence parsing;
- review findings that were fixed, especially around read-only assertions, destination overwrite refusal, SHA-256 from written output, audit opt-in, and deleted recovery being unsupported.

Current project state:
- Stage 1 is complete: segmented E01 discovery, EWF reader adapter boundary, JSON intake command/callable, and case-store schema.
- Stage 2 is complete: read-only local byte-stream abstraction, whole-image volume discovery boundary, filesystem adapter boundary, directory listing, and raw/text/hex preview through explicit preview providers.
- Stage 3 is complete: export contracts, fixture/stub export service, SHA-256 and byte-count verification from written artifacts, optional explicit export audit events, and deleted-file recovery documentation as unsupported/deferred.
- Default tests are dependency-free and should pass with `python -m pytest`.

The most important project weakness to keep in mind:
- The project is still mostly contract/stub/provider-backed beyond tiny local file reads. There is no real EWF byte stream, no real partition parser, no real filesystem parser, and no real filesystem file-content extraction. Stage 4 must not accidentally make synthetic provider bytes look like real evidence analysis.

Stage 4 goal:
- Add hash/signature analysis foundations, but only over explicit content providers with honest provenance and status.
- Define contracts before building broad analysis behavior.
- Keep per-file hash/signature analysis separate from export-output verification and separate from whole-image verification.

Stage 4 guardrails:
- Do not hash preview-rendered text or hex as source content.
- Do not treat filesystem metadata entries as byte-bearing objects.
- Do not claim real file hashing from evidence unless an explicit content provider can supply those bytes and identify its source.
- Do not claim whole-image verification unless an image/EWF adapter exposes the necessary bytes and expected verification data.
- Keep MD5/SHA-1, known-file matching, case-store persistence, and background job orchestration optional until result contracts are reviewed.
- Do not add real EWF parsing, real partition parsing, real filesystem parsing, deleted recovery, carving, UI, search, timeline, reporting, bookmarks, packaging, or required native dependencies unless a reviewed ticket explicitly asks for that scope.

Recommended first Stage 4 direction:
1. Start with a Stage 4 fixture/content-source reality check. Decide what bytes Stage 4 is allowed to hash/signature-test by default.
2. Define hash/signature request/result/status/warning contracts with source provenance and provider identity.
3. Add dependency-free tests using explicit provider-backed bytes, while labeling synthetic bytes honestly.
4. Only after contracts are reviewed, add calculation behavior such as SHA-256 and optional MD5/SHA-1 for provider-backed content.
5. Keep known-file matching and case-store persistence separate later tickets.

Before implementing any Stage 4 ticket:
- Summarize your understanding of the true current project state.
- List the files you expect to modify.
- State what bytes your ticket will analyze and why those bytes are legitimate for that ticket.
- If the ticket would require real parser support or real evidence extraction that does not exist, pause and explain instead of inventing fake support.

Run `python -m pytest` after any change and report the exact result.

Stop after the active ticket and hand off for review. Do not broaden into later stages.
```
