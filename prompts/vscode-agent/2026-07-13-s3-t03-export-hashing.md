# 2026-07-13 - S3-T03 Export Hashing And Byte-Count Verification Prompt

Use this prompt to hand S3-T03 to the Stage 3 VS Code implementation agent.

```text
Implement ticket S3-T03: Export Hashing And Byte-Count Verification.

Before editing, read these files:
- prompts/vscode-agent/2026-07-13-stage-3-familiarization.md
- tickets/stage-3/S3-T01-export-manifest-contract.md
- tickets/stage-3/S3-T02-file-export-service.md
- tickets/stage-3/S3-T03-export-hashing.md
- tickets/stage-3/README.md
- Goal.md
- plan.md
- functionality.md
- progression.md
- review.md
- workflow.md
- app/backend/api/file_export.py
- app/backend/forensic_core/export_manifest.py
- app/tests/test_file_export.py
- app/tests/test_export_manifest.py
- app/backend/api/README.md
- app/backend/forensic_core/README.md

Context:
- S3-T01 and S3-T02 are reviewed and done.
- S3-T02 writes explicit provider-backed export bytes and a manifest using S3-T01 shapes.
- S3-T03 verifies the exported artifact after writing.
- Hashing in this ticket is only for exported output verification. Broader file hash analysis, known-file matching, signatures, extension mismatch checks, and image verification are Stage 4 or later.

Before implementing:
- Summarize your understanding of S3-T03.
- List the files you expect to create or modify.
- If you see a conflict between this prompt and the ticket, pause and explain it instead of broadening scope.

Your task:
- Compute SHA-256 from the written output file after a successful S3-T02 export write.
- Record byte count from the written output file after writing, not only provider byte length.
- Compare written byte count with expected/provider byte count when known.
- Update returned `ExportResult` and persisted manifest JSON so they agree on:
  - `bytes_requested`;
  - `bytes_written`;
  - `hashes.sha256`;
  - `hashes.status`;
  - final export status/warnings.
- Use the existing `ExportHashSummary` contract unless a tiny S3-T01-compatible extension is clearly needed.
- Keep existing S3-T02 destination safety, exclusive write, overwrite refusal, and cleanup behavior intact.

Use these status names unless the local design strongly suggests better names:
- `ok`
- `export_verification_failed`
- `byte_count_mismatch`
- `hash_failed`
- Existing S3-T02 statuses such as `path_not_file`, `content_source_unavailable`, `destination_not_selected`, `unsafe_destination`, `invalid_output_name`, `output_exists`, and `export_write_failed` should keep their meaning.

Tests to add or update:
- successful stub export records the known SHA-256 for `b"Hello, world!"`;
- hash is calculated from exported file bytes;
- returned result and manifest JSON agree on SHA-256 and byte counts;
- hash/byte-count fields are JSON-serializable;
- byte-count mismatch or unreadable/missing output after write returns structured non-ok status/warning;
- pre-write failures such as missing content or unsafe destination do not compute SHA-256;
- existing S3-T02 overwrite and partial-cleanup tests still pass.

Scope boundaries:
- Do not add MD5 or SHA-1 unless it is only a harmless placeholder already supported by the contract.
- Do not add known-file matching, file signatures, extension mismatch checks, image verification, audit integration, deleted recovery, UI, real EWF parsing, real partition parsing, real filesystem parsing, or required native dependencies.
- Do not hash preview-rendered text or hex.
- Do not commit or push.

Documentation updates:
- app/backend/api/README.md
- app/backend/forensic_core/README.md
- functionality.md
- plan.md
- progression.md
- review.md
- tickets/stage-3/README.md
- tickets/stage-3/S3-T03-export-hashing.md

Run:
- `python -m pytest`

Final handoff:
- Summarize files changed.
- Summarize hashing/byte-count verification behavior.
- Report the exact pytest command and result.
- State limitations and deferred work.
- Confirm you did not begin S3-T04 or Stage 4 hash/signature analysis.

Stop after S3-T03 and hand off for review.
```
