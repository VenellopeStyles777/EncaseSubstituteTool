# S3-T03 - Export Hashing And Byte-Count Verification

Status: Done

Stage: Stage 3 - Export and recovery foundation

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Add SHA-256 and byte-count verification for files exported by the S3-T02 service.

This ticket verifies written export artifacts. It is not the broader Stage 4 hash/signature-analysis system.

## Context To Read First

- `prompts/vscode-agent/2026-07-13-stage-3-familiarization.md`
- `prompts/vscode-agent/2026-07-13-s3-t03-export-hashing.md`
- `tickets/stage-3/S3-T01-export-manifest-contract.md`
- `tickets/stage-3/S3-T02-file-export-service.md`
- `tickets/stage-3/S3-T03-export-hashing.md`
- S3-T01 and S3-T02 reviewed implementation
- `app/backend/api/file_export.py`
- `app/backend/forensic_core/export_manifest.py`
- `app/tests/test_file_export.py`
- `app/tests/test_export_manifest.py`
- `Goal.md`
- `plan.md`
- `functionality.md`
- `progression.md`
- `review.md`
- `workflow.md`

## Target Files/Folders

Likely files to modify:

- `app/backend/api/file_export.py`
- `app/backend/forensic_core/export_manifest.py`
- `app/tests/test_file_export.py`
- possibly `app/tests/test_export_manifest.py`
- `app/backend/api/README.md`
- `app/backend/forensic_core/README.md`
- `functionality.md`
- `plan.md`
- `progression.md`
- `review.md`
- `tickets/stage-3/README.md`
- `tickets/stage-3/S3-T03-export-hashing.md`

## Required Work

- Compute SHA-256 over the exported output bytes after writing.
- Record byte count from the written output, not only from provider metadata.
- Compare written byte count with provider/source byte count when known.
- Update result and manifest fields with:
  - `sha256`;
  - exported byte count;
  - expected/source byte count when known;
  - verification status/warnings.
- Use the existing S3-T01 `ExportHashSummary` unless a small contract extension is clearly necessary. Do not invent a parallel hash result object.
- Update manifest JSON after verification so the persisted manifest and returned result agree.
- Verify by reading the written output file after export. Do not hash provider bytes directly as a substitute for exported file verification.
- Add structured mismatch/error handling for:
  - byte-count mismatch;
  - unreadable output after write;
  - hash computation failure;
  - partial write or missing output.
- Keep MD5/SHA-1 optional/deferred unless the S3-T01 contract already supports harmless placeholders. Stage 4 handles broader hash analysis.
- Keep the existing S3-T02 overwrite and cleanup behavior intact.

## Suggested Status Names

Use these names unless a clearer local pattern emerges:

- `ok`: export write, byte-count verification, and SHA-256 verification completed.
- `export_verification_failed`: exported output could not be verified after writing.
- `byte_count_mismatch`: written file size does not match expected/provider byte count.
- `hash_failed`: SHA-256 calculation failed.
- Existing S3-T02 statuses such as `path_not_file`, `content_source_unavailable`, `destination_not_selected`, `unsafe_destination`, `invalid_output_name`, `output_exists`, and `export_write_failed` should keep their meaning.

If a post-write verification failure occurs, return a structured non-ok result and do not leave a misleading successful manifest.

## Acceptance Criteria

- Successful exports include correct SHA-256 and exported byte count.
- Manifest hash and result hash agree.
- Hash is calculated from the exported file bytes.
- Byte-count mismatch or unreadable output produces structured non-ok status/warning.
- Existing S3-T02 failure paths still do not compute hashes and still avoid writing artifacts where appropriate.
- S3-T03 does not add MD5, SHA-1, known-file matching, file signatures, case-store audit integration, deleted recovery, UI, or real parser work.
- Default tests remain dependency-free and use tiny provider-backed bytes.

## Test Expectations

Tests should cover:

- SHA-256 for known stub bytes;
- byte count equals written bytes;
- result and manifest hash agreement;
- hash/byte count fields are JSON-serializable;
- simulated mismatch or post-write verification failure.
- no hash fields are set for pre-write failures such as missing content or unsafe destination;
- S3-T02 overwrite/partial-cleanup tests still pass.

Run:

```powershell
python -m pytest
```

## Documentation Updates

- Document Stage 3 export hashing in backend docs.
- Keep broader Stage 4 hash/signature analysis documented as future work.
- Update `functionality.md`, `plan.md`, `progression.md`, `review.md`, and ticket statuses.

## Review Checklist

- Hashing verifies exported artifacts, not preview-rendered text/hex.
- The implementation does not claim full evidence verification.
- The implementation does not add known-file matching, file signatures, UI, real parsers, or deleted recovery.
- Failure modes are structured and testable.
- Manifest/result cannot report `ok` with missing or mismatched hash/byte-count verification.

## Implementation Handoff - 2026-07-13

- `export_file()` now reads the written output file after export, computes SHA-256 from those bytes, records on-disk `bytes_written`, and compares it with provider `bytes_requested`.
- Successful result and manifest JSON agree on SHA-256, hash status, byte counts, final status, and warnings.
- Structured post-write verification failures include `byte_count_mismatch` and `export_verification_failed` with hash status `hash_failed` when the output cannot be read back.
- Existing S3-T02 destination safety, exclusive write, overwrite refusal, and generic write-failure cleanup behavior remain in place.
- Scope remained limited to S3-T03; S3-T04 and Stage 4 hash/signature analysis were not started.

## Review Result - 2026-07-13

- Approved for commit.
- Review found no blocking issues.
- `python -m pytest` reported 93 passed in 4.04s.
- S3-T04 remains the next Stage 3 gate and should stay limited to optional, explicit case-store audit integration.

## Handoff Prompt

```text
Implement S3-T03 only after S3-T02 is reviewed and accepted. Add SHA-256 and byte-count verification for exported output files and manifests. Keep broader hash/signature analysis for Stage 4. Stop after S3-T03 and hand off for review.
```
