# S3-T02 - Fixture/Stub File Export Service

Status: Done

Stage: Stage 3 - Export and recovery foundation

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Implement the first safe export service for explicit fixture/stub/provider-backed bytes.

This ticket should write selected file-like content to an examiner-selected output directory and emit a manifest using the S3-T01 contract. It must not parse real filesystems or recover deleted files.

## Context To Read First

- `prompts/vscode-agent/2026-07-13-stage-3-familiarization.md`
- `prompts/vscode-agent/2026-07-13-s3-t02-file-export-service.md`
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
- Use the reviewed S3-T01 structures rather than inventing parallel result shapes:
  - `ExportSourceProvenance`;
  - `ExportContentSourceIdentity`;
  - `ExportStatus`;
  - `ExportWarning`;
  - `ExportHashSummary`;
  - `ExportResult`;
  - `ExportManifest`.
- Keep SHA-256 as not computed in S3-T02. The result and manifest should continue to use `ExportHashSummary(status=ExportStatus(code="hash_not_computed", ...))` unless S3-T03 has landed.
- Write the manifest JSON from `ExportResult.to_manifest()` or an equivalent S3-T01 manifest object.
- Prefer deterministic output naming based on the file entry's `name`, after rejecting unsafe path components.

## Suggested Status Names

Use these names unless a clearer local pattern emerges:

- `ok`: export file and manifest were written successfully.
- `invalid_export_request`: required file/source/destination fields were invalid.
- `path_not_file`: caller tried to export a directory or non-file entry.
- `content_source_unavailable`: explicit export provider has no bytes for the requested file.
- `destination_not_selected`: caller did not supply an explicit output directory.
- `unsafe_destination`: destination overlaps source/evidence path or fails safety checks.
- `invalid_output_name`: file name or requested output path contains traversal or unsafe path components.
- `output_exists`: output or manifest path already exists and overwrite is not enabled.
- `export_write_failed`: output or manifest write failed.

Keep these statuses structured in `ExportStatus` and `ExportWarning`; do not raise raw exceptions for expected user mistakes.

## Acceptance Criteria

- A known stub/provider-backed file can be exported to a workspace-local test output directory.
- Export writes only expected output file and manifest files.
- Export refuses unsafe destinations near the source/evidence path.
- Export refuses missing content, directory entries, invalid destinations, and path traversal attempts with structured statuses.
- Export result and manifest preserve source provenance and content-source identity.
- Export does not compute SHA-256 unless S3-T03 has already been merged; before S3-T03, hash fields remain `hash_not_computed`.
- `bytes_requested` and `bytes_written` reflect provider bytes and written output length for successful exports.
- Manifest JSON and result JSON agree on output path, manifest path, byte count, source provenance, content-source identity, and hash-not-computed status.
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
- manifest content agrees with result content;
- successful export keeps `hashes.status.code == "hash_not_computed"`.

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
Implement S3-T02 only after S3-T01 is reviewed and accepted. Build the first safe fixture/stub/provider-backed export service using the S3-T01 contracts. Do not implement SHA-256 hashing, audit integration, deleted recovery, UI, or real parser work. Stop after S3-T02 and hand off for review.
```
