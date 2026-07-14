# 2026-07-14 - S3-T06 Stage 3 Docs And Review Handoff Prompt

Use this prompt to hand S3-T06 to the Stage 3 VS Code implementation agent.

```text
Implement ticket S3-T06: Stage 3 Docs And Review Handoff.

Before editing, read these files:
- prompts/vscode-agent/2026-07-13-stage-3-familiarization.md
- tickets/stage-3/README.md
- tickets/stage-3/S3-T01-export-manifest-contract.md
- tickets/stage-3/S3-T02-file-export-service.md
- tickets/stage-3/S3-T03-export-hashing.md
- tickets/stage-3/S3-T04-export-audit-integration.md
- tickets/stage-3/S3-T05-deleted-recovery-plan.md
- tickets/stage-3/S3-T06-docs-review-handoff.md
- Goal.md
- readme.md
- plan.md
- functionality.md
- progression.md
- review.md
- workflow.md
- tickets/README.md
- app/backend/README.md
- app/backend/api/README.md
- app/backend/forensic_core/README.md
- app/backend/case_store/README.md
- app/fixtures/README.md
- app/docs/environment-readiness.md
- log/documentation.md
- app/backend/forensic_core/export_manifest.py
- app/backend/api/file_export.py
- app/tests/test_export_manifest.py
- app/tests/test_file_export.py

Context:
- S3-T01 through S3-T05 are reviewed, committed, and pushed.
- S3-T01 added export result/manifest/content-source/provenance/hash contract structures.
- S3-T02 added fixture/stub export writing to examiner-selected output directories through an explicit export content provider.
- S3-T03 verifies exported artifacts by reading the written output, counting bytes, and computing SHA-256 from disk.
- S3-T04 adds optional export audit events only when explicit `ExportAuditContext` is supplied.
- S3-T05 documents deleted-file recovery as unsupported/deferred because current adapters expose metadata only and no recoverable deleted-file bytes.
- This ticket is the final Stage 3 documentation/review handoff. It should reconcile docs and prepare Stage 4 notes. It should not add new behavior.

Before implementing:
- Summarize your understanding of the final Stage 3 behavior and limitations.
- List the documentation files you expect to modify.
- If you believe a code change is necessary, pause and explain why before making it.

Your task:
- Reconcile all docs so they agree on the final Stage 3 state.
- Update stale wording, especially any text saying Stage 2 is the current project state or Stage 3 is merely ready to begin.
- Document the current Stage 3 backend export workflow:
  - selected file metadata comes from Stage 2-style entries;
  - export bytes come only from an explicit export content provider;
  - the default provider is synthetic/stub-backed for `stub-file-hello`;
  - output goes to an examiner/test-selected directory separate from source/evidence paths;
  - output and manifest writes refuse overwrite;
  - SHA-256 and byte count are verified from the written output artifact;
  - optional audit rows require explicit `ExportAuditContext`.
- Document callable-level usage where appropriate:
  - `export_file(...)`;
  - `export_file_to_json(...)`;
  - `ExportAuditContext`;
  - `StubExportContentProvider`;
  - S3-T01 result/manifest helpers if useful.
- Clearly separate:
  - export writes from real evidence parsing;
  - provider-backed synthetic bytes from filesystem extraction;
  - export-output SHA-256 verification from broader Stage 4 hash/signature analysis;
  - active allocated export from deleted-file recovery;
  - deleted-file recovery from carving/unallocated-space recovery.
- Keep manual-test fields `Untested` unless the user explicitly reports a manual run.
- Add final Stage 3 handoff notes for Stage 4:
  - Stage 4 should build hash/signature contracts on explicit content providers;
  - do not hash preview text/hex as source content;
  - do not claim whole-image verification without adapter support;
  - keep known-file matching and persistence optional until result contracts are reviewed.
- Search for stale phrases such as:
  - `Stage 2 is complete at the documentation/review-handoff level`;
  - `Stage 3 export/recovery foundation is ready to begin`;
  - `S3-T01 ready`;
  - `S3-T06 Draft`;
  - `S3-T05 implemented for review`.

Likely documentation files to update:
- Goal.md
- readme.md
- plan.md
- functionality.md
- progression.md
- review.md
- tickets/README.md
- tickets/stage-3/README.md
- tickets/stage-3/S3-T06-docs-review-handoff.md
- app/backend/README.md
- app/backend/api/README.md
- app/backend/forensic_core/README.md
- app/backend/case_store/README.md
- app/fixtures/README.md
- app/docs/environment-readiness.md
- log/documentation.md

Scope boundaries:
- Do not change backend behavior.
- Do not add or change export APIs.
- Do not add Stage 4 hash/signature code.
- Do not add MD5/SHA-1 production hashing, known-file matching, file signature detection, extension mismatch checks, or image verification.
- Do not add real EWF parsing, real partition parsing, real filesystem parsing, real filesystem extraction, deleted recovery, carving, unallocated-space scanning, UI, search, timeline, reporting, bookmarks, notes, or packaging.
- Do not add native dependency requirements or real evidence fixtures.
- Do not mark manual testing as complete unless the user explicitly reports it.
- Do not commit or push.

Tests:
- Run `python -m pytest`.
- Record the exact result in `progression.md`, `review.md`, and the S3-T06 ticket/handoff notes.

Final handoff:
- Summarize files changed.
- Summarize the final Stage 3 behavior documented.
- Report the exact pytest command and result.
- Confirm no code behavior changed.
- Mark S3-T06 as `Review`, then stop. Do not begin Stage 4.
```
