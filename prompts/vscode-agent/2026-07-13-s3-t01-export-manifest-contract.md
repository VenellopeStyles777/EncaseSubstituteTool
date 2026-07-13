# 2026-07-13 - S3-T01 Export Manifest Contract Prompt

Use this prompt to hand S3-T01 to the Stage 3 VS Code implementation agent.

```text
Implement ticket S3-T01: Export Result And Manifest Contract.

Before editing, read these files:
- prompts/vscode-agent/2026-07-13-stage-3-familiarization.md
- prompts/stage-3-onboarding/stage-2-conclusion-and-stage-3-needs.md
- prompts/stage-3-onboarding/project-review-agent-memo.md
- tickets/stage-3/S3-T01-export-manifest-contract.md
- tickets/stage-3/README.md
- Goal.md
- plan.md
- functionality.md
- progression.md
- review.md
- workflow.md
- app/backend/api/file_preview.py
- app/backend/api/directory_listing.py
- app/backend/forensic_core/filesystem_adapter.py
- app/backend/forensic_core/README.md
- app/backend/api/README.md
- app/fixtures/README.md

Context:
- Stage 2 is complete as a backend foundation.
- Stage 2 filesystem entries are metadata-only.
- Stage 2 preview bytes are synthetic/provider-backed and are not real filesystem extraction.
- Stage 3 must begin with export contracts/manifests before any file writing.
- Export bytes must eventually come from an explicit export content-source/provider boundary, not preview-rendered text/hex and not metadata alone.

Before implementing:
- Summarize your understanding of S3-T01.
- List the files you expect to create or modify.
- If you see a conflict between this prompt and the ticket, pause and explain it instead of broadening scope.

Your task:
- Add contract structures for Stage 3 export request/result/manifest/status/warning/content-source identity.
- Keep the implementation dependency-free and JSON-friendly.
- Preserve source provenance fields used by Stage 2 entries: source path, volume id, volume offset/length, file id/path/name, filesystem type, adapter/source name, read-only assertion, allocation/deleted state where relevant.
- Include destination/output/manifest path fields, but keep them nullable or placeholder-ready because this ticket must not write files.
- Include byte count and hash fields, but treat them as not-computed placeholders.
- Include UTC timestamp fields.
- Add tests for serialization, provenance, warnings, content-source identity, placeholder byte/hash fields, and non-ok statuses such as `export_not_started` or `content_source_unavailable`.
- Update docs and ticket status as requested in the ticket.
- Run `python -m pytest` and report the exact result.

Likely files to create or modify:
- app/backend/forensic_core/export_manifest.py
- app/backend/forensic_core/__init__.py
- app/tests/test_export_manifest.py
- app/backend/forensic_core/README.md
- app/backend/api/README.md if API boundary notes need clarification
- app/fixtures/README.md if content-source wording needs clarification
- functionality.md
- plan.md
- progression.md
- review.md
- tickets/stage-3/README.md
- tickets/stage-3/S3-T01-export-manifest-contract.md

Scope boundaries:
- Do not implement file export or write manifests.
- Do not compute hashes.
- Do not add destination safety logic beyond placeholder/status fields.
- Do not add case-store audit integration.
- Do not implement deleted-file recovery.
- Do not use preview-rendered text or hex as export bytes.
- Do not add UI, search, reporting, real EWF parsing, real partition parsing, real filesystem parsing, or required native dependencies.
- Do not commit or push.

Final handoff:
- Summarize files changed.
- Summarize structures added.
- Report the exact pytest command and result.
- State limitations and deferred work.
- Confirm you did not begin S3-T02.

Stop after S3-T01 and hand off for review.
```
