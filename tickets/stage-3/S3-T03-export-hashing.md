# S3-T03 - Export Hashing And Byte-Count Verification

Status: Draft

Stage: Stage 3 - Export and recovery foundation

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Compute export hashes and verify byte counts for exported files.

## Acceptance Criteria

- SHA-256 is recorded for exported output.
- Byte count matches the written content.
- Tests cover hash and mismatch/error behavior.

## Handoff Prompt

```text
Implement S3-T03: Export Hashing And Byte-Count Verification. Keep broader hash analysis for Stage 4.
```
