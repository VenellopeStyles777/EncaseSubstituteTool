# S3-T02 - Fixture/Stub File Export Service

Status: Draft

Stage: Stage 3 - Export and recovery foundation

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Implement the first safe export service for explicit fixture/stub/provider-backed bytes.

This ticket should write selected file-like content to an examiner-selected output directory and emit a manifest using the S3-T01 contract. It must not parse real filesystems or recover deleted files.

## Context To Read First

- `prompts/vscode-agent/2026-07-13-stage-3-familiarization.md`
- `tickets/stage-3/S3-T01-export-manifest-contract.md`
- `tickets/stage-3/S3-T02-file-export-service.md`
- S3-T01 implementation and tests after review
- `app/backend/api/file_preview.py`
- `app/backend/forensic_core/filesystem_adapter.py`
- `app/backend/forensic_core/export_manifest.py`
- `app/fixtures/README.md`
- `review.md`
- `workflow.md`

## Target Files/Folders

Likely files to create or modify:

- `app/backend/api/file_export.py`
- `app/backend/api/__init__.py`
- `app/backend/forensic_core/export_manifest.py`
- `app/tests/test_file_export.py`
- `app/backend/api/README.md`
- `app/backend/forensic_core/README.md`
- `functionality.md`
- `plan.md`
- `progression.md`
- `review.md`
- `tickets/stage-3/README.md`
- `tickets/stage-3/S3-T02-file-export-service.md`

## Required Work

- Define an explicit export content provider/source protocol. It may resemble the preview provider, but it must be separate so export never consumes rendered preview output.
- Add a dependency-free stub export provider for tests, likely mapping `stub-file-hello` to raw `b"Hello, world!"` bytes.
- Add an export service/callable that:
  - accepts a Stage 2-style file entry or S3-T01 request;
  - accepts an explicit output directory selected by the examiner/test caller;
  - obtains raw bytes from the export content provider;
  - writes the file to the output directory;
  - writes a JSON manifest beside the export or in a deterministic manifest path;
  - returns the S3-T01 result shape.
- Add destination safety checks before writing:
  - output directory must be explicit;
  - output directory must not be the same as, inside, or overlapping a source/evidence path when that can be determined;
  - path traversal through file names or requested relative paths must be rejected or sanitized predictably;
  - existing files must be handled predictably, either refusal or explicit overwrite flag.
- Keep source/evidence paths read-only and unmodified.

## Acceptance Criteria

- A known stub/provider-backed file can be exported to a workspace-local test output directory.
- Export writes only expected output file and manifest files.
- Export refuses unsafe destinations near the source/evidence path.
- Export refuses missing content, directory entries, invalid destinations, and path traversal attempts with structured statuses.
- Export result and manifest preserve source provenance and content-source identity.
- Export does not compute SHA-256 unless S3-T03 has already been merged; before S3-T03, hash fields remain `hash_not_computed`.
- Tests prove source fixture/provider data is not mutated.

## Test Expectations

Tests should cover:

- successful stub/provider-backed export;
- manifest JSON exists and is JSON-serializable;
- exported bytes equal provider bytes;
- missing provider content;
- directory/non-file entry;
- unsafe destination overlapping source/evidence path;
- invalid destination path;
- path traversal or unsafe file name;
- existing output file behavior;
- no mutation of source path/provider data.

Run:

```powershell
python -m pytest
```

## Documentation Updates

- Document the export callable in `app/backend/api/README.md`.
- Update `app/backend/forensic_core/README.md` to distinguish export content provider bytes from preview provider rendering.
- Update `functionality.md`, `plan.md`, `progression.md`, `review.md`, and ticket statuses.

## Review Checklist

- Export uses an explicit export content provider/source, not preview-rendered text/hex.
- Destination safety checks run before any write.
- Source/evidence paths are not written or modified.
- Manifest says whether bytes are stub/provider-backed.
- No real parsing, deleted recovery, UI, audit persistence, or Stage 4 hash/signature scope was added.

## Handoff Prompt

```text
Implement S3-T02 only after S3-T01 is reviewed and accepted. Build the first safe fixture/stub/provider-backed export service using the S3-T01 contracts. Do not implement hashing, audit integration, deleted recovery, UI, or real parser work. Stop after S3-T02 and hand off for review.
```
