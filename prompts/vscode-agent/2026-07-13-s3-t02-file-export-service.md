# 2026-07-13 - S3-T02 Fixture/Stub File Export Service Prompt

Use this prompt to hand S3-T02 to the Stage 3 VS Code implementation agent.

```text
Implement ticket S3-T02: Fixture/Stub File Export Service.

Before editing, read these files:
- prompts/vscode-agent/2026-07-13-stage-3-familiarization.md
- tickets/stage-3/S3-T01-export-manifest-contract.md
- tickets/stage-3/S3-T02-file-export-service.md
- tickets/stage-3/README.md
- Goal.md
- plan.md
- functionality.md
- progression.md
- review.md
- workflow.md
- app/backend/forensic_core/export_manifest.py
- app/tests/test_export_manifest.py
- app/backend/api/file_preview.py
- app/backend/api/directory_listing.py
- app/backend/forensic_core/filesystem_adapter.py
- app/backend/api/README.md
- app/backend/forensic_core/README.md
- app/fixtures/README.md

Context:
- S3-T01 is reviewed and done.
- S3-T01 defines export request/result/manifest/status/warning/source-provenance/content-source/hash-placeholder contracts.
- S3-T02 is the first ticket allowed to write export files and manifest JSON.
- Export bytes must come from an explicit export content provider/source.
- Do not use Stage 2 preview-rendered text or hex as export bytes.
- Do not treat Stage 2 filesystem entries as byte-bearing objects.
- Keep real parser work and deleted recovery deferred.

Before implementing:
- Summarize your understanding of S3-T02.
- List the files you expect to create or modify.
- If you see a conflict between this prompt and the ticket, pause and explain it instead of broadening scope.

Your task:
- Add a backend export service/callable, likely under `app/backend/api/file_export.py`.
- Define an explicit export content provider/source protocol separate from preview providers.
- Add a dependency-free `StubExportContentProvider` or similarly named provider for tests, mapping `stub-file-hello` to raw `b"Hello, world!"`.
- Implement a callable such as `export_file(...)` that:
  - accepts a Stage 2-style file entry or S3-T01 request;
  - accepts an explicit examiner/test-selected output directory;
  - gets raw bytes from the export content provider;
  - performs destination safety checks before writing;
  - writes the exported file;
  - writes a JSON manifest using the S3-T01 `ExportResult.to_manifest()` or equivalent `ExportManifest`;
  - returns an `ExportResult`.
- Add a JSON helper if useful, following existing API patterns.
- Export API names from `app/backend/api/__init__.py` if that fits existing package style.

Destination safety requirements:
- Output directory must be explicit.
- Output directory must not be the same as, inside, or overlapping a known source/evidence path when that can be determined.
- Reject path traversal and unsafe path components from file names or requested output names.
- Existing output or manifest files must be refused unless you intentionally add an explicit overwrite flag. Prefer refusal for S3-T02.
- Expected user mistakes should return structured `ExportStatus`/`ExportWarning` values, not raw tracebacks.

Use these status names unless the local design strongly suggests better names:
- `ok`
- `invalid_export_request`
- `path_not_file`
- `content_source_unavailable`
- `destination_not_selected`
- `unsafe_destination`
- `invalid_output_name`
- `output_exists`
- `export_write_failed`

Keep S3-T02 narrow:
- Do not compute SHA-256. Keep hashes as `hash_not_computed`.
- Do not add audit integration.
- Do not implement deleted-file recovery.
- Do not add UI, search, reporting, real EWF parsing, real partition parsing, real filesystem parsing, or required native dependencies.
- Do not commit or push.

Tests to add:
- successful stub/provider-backed export;
- manifest JSON exists and is JSON-serializable;
- exported bytes equal provider bytes;
- result and manifest agree on output path, manifest path, byte count, source provenance, content-source identity, and hash-not-computed status;
- missing provider content returns structured `content_source_unavailable`;
- directory/non-file entry returns structured `path_not_file`;
- missing output directory returns structured `destination_not_selected`;
- unsafe destination overlapping source/evidence path returns structured `unsafe_destination`;
- invalid output name or traversal returns structured `invalid_output_name`;
- existing output file behavior is predictable, preferably `output_exists`;
- provider/source data is not mutated;
- no real evidence, native dependency, network access, UI, or parser work is required.

Documentation updates:
- app/backend/api/README.md
- app/backend/forensic_core/README.md
- app/fixtures/README.md if fixture/export-source guidance changes
- functionality.md
- plan.md
- progression.md
- review.md
- tickets/stage-3/README.md
- tickets/stage-3/S3-T02-file-export-service.md

Run:
- `python -m pytest`

Final handoff:
- Summarize files changed.
- Summarize export behavior added.
- Report the exact pytest command and result.
- State limitations and deferred work.
- Confirm you did not begin S3-T03.

Stop after S3-T02 and hand off for review.
```
