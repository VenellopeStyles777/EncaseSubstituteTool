# 2026-07-13 - S3-T05 Deleted-File Recovery Plan Prompt

Use this prompt to hand S3-T05 to the Stage 3 VS Code implementation agent.

```text
Implement ticket S3-T05: Deleted-File Recovery Research And Conditional Plan.

Before editing, read these files:
- prompts/vscode-agent/2026-07-13-stage-3-familiarization.md
- tickets/stage-3/S3-T01-export-manifest-contract.md
- tickets/stage-3/S3-T02-file-export-service.md
- tickets/stage-3/S3-T03-export-hashing.md
- tickets/stage-3/S3-T04-export-audit-integration.md
- tickets/stage-3/S3-T05-deleted-recovery-plan.md
- tickets/stage-3/README.md
- Goal.md
- plan.md
- functionality.md
- progression.md
- review.md
- workflow.md
- app/backend/forensic_core/filesystem_adapter.py
- app/backend/forensic_core/README.md
- app/backend/api/file_export.py
- app/backend/api/README.md
- app/fixtures/README.md
- app/docs/environment-readiness.md
- tickets/README.md

Context:
- S3-T01 through S3-T04 are reviewed and done.
- S3-T02/S3-T04 support active fixture/stub export of explicit provider-backed bytes with manifest, SHA-256, and optional audit events.
- Current filesystem entries are metadata only. Metadata may include `allocated` and `deleted`, but no current adapter exposes recoverable deleted-file byte ranges.
- `StubFilesystemAdapter` returns `/Documents` and `/hello.txt` as allocated and not deleted.
- `Pytsk3FilesystemAdapter` reports dependency availability and `real_parser_not_implemented`; it does not parse real filesystems or deleted entries.
- Therefore S3-T05 is documentation/planning only.

Before implementing:
- Summarize your understanding of why S3-T05 is docs/planning only in the current codebase.
- List the files you expect to modify.
- If you find a reviewed real adapter that exposes deleted entries and recoverable bytes, pause and explain it before adding recovery behavior.

Your task:
- Document the difference between:
  - active allocated file export;
  - deleted entry metadata;
  - deleted-file recovery;
  - carving or unallocated-space recovery;
  - unsupported or unrecoverable entries.
- State the current project truth:
  - stub filesystem entries are allocated and not deleted;
  - current filesystem entries are metadata-only;
  - preview/export providers supply synthetic bytes only when explicitly registered;
  - current export is not deleted-file recovery;
  - no real deleted-file recovery exists.
- Define future adapter requirements for deleted-file recovery:
  - allocation/deleted state;
  - recoverable content ranges or explicit content provider/source;
  - completeness/confidence status;
  - overwritten, sparse, partial, or unavailable range warnings;
  - filesystem-specific provenance;
  - read-only source handling;
  - output/manifest/audit compatibility with the existing export workflow.
- Define future statuses/warnings for unsupported recovery, using names like:
  - `deleted_recovery_unsupported`;
  - `deleted_entry_metadata_only`;
  - `recovery_content_unavailable`;
  - `recovery_partial`;
  - `recovery_not_attempted`;
  - `carving_deferred`.
- Keep carving and unallocated-space scanning deferred.

Likely documentation files to update:
- app/backend/forensic_core/README.md
- app/backend/api/README.md
- app/fixtures/README.md
- app/docs/environment-readiness.md
- Goal.md
- plan.md
- functionality.md
- progression.md
- review.md
- tickets/README.md
- tickets/stage-3/README.md
- tickets/stage-3/S3-T05-deleted-recovery-plan.md

Scope boundaries:
- Do not add recovery APIs.
- Do not add fake deleted entries to `StubFilesystemAdapter`.
- Do not add fake recoverable deleted bytes to preview/export providers.
- Do not add pytsk3 parsing, real EWF parsing, real partition parsing, real filesystem parsing, carving, unallocated-space scanning, UI, reporting, Stage 4 hash/signature analysis, or native dependency requirements.
- Do not change S3-T02/S3-T04 export behavior.
- Do not commit or push.

Tests:
- Run `python -m pytest`.
- Record the exact result in `progression.md` and relevant review/handoff notes.

Stop after S3-T05 and hand off for review. Do not begin S3-T06.
```
