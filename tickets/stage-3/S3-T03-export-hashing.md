# S3-T03 - Export Hashing And Byte-Count Verification

Status: Draft

Stage: Stage 3 - Export and recovery foundation

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Add SHA-256 and byte-count verification for files exported by the S3-T02 service.

This ticket verifies written export artifacts. It is not the broader Stage 4 hash/signature-analysis system.

## Context To Read First

- S3-T01 and S3-T02 tickets and reviewed implementation
- `app/backend/api/file_export.py`
- `app/backend/forensic_core/export_manifest.py`
- `app/tests/test_file_export.py`
- `Goal.md`
- `plan.md`
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
  - hash algorithm metadata;
  - exported byte count;
  - expected/source byte count when known;
  - verification status/warnings.
- Add structured mismatch/error handling for:
  - byte-count mismatch;
  - unreadable output after write;
  - hash computation failure;
  - partial write or missing output.
- Keep MD5/SHA-1 optional/deferred unless the S3-T01 contract already supports harmless placeholders. Stage 4 handles broader hash analysis.

## Acceptance Criteria

- Successful exports include correct SHA-256 and exported byte count.
- Manifest hash and result hash agree.
- Hash is calculated from the exported file bytes.
- Byte-count mismatch or unreadable output produces structured non-ok status/warning.
- Default tests remain dependency-free and use tiny provider-backed bytes.

## Test Expectations

Tests should cover:

- SHA-256 for known stub bytes;
- byte count equals written bytes;
- result and manifest hash agreement;
- hash/byte count fields are JSON-serializable;
- simulated mismatch or post-write verification failure.

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

## Handoff Prompt

```text
Implement S3-T03 only after S3-T02 is reviewed and accepted. Add SHA-256 and byte-count verification for exported output files and manifests. Keep broader hash/signature analysis for Stage 4. Stop after S3-T03 and hand off for review.
```
