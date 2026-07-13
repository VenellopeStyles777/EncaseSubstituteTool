# Review - Code and Architecture Review Notes

Purpose: use this file for findings from research/review agents. Keep reviews focused on defects, forensic-soundness risks, data-integrity risks, missing tests, and architecture drift.

Review priorities for this project:

- Evidence must be opened read-only unless an explicit export/write operation targets a separate output path.
- Every parsed file, exported file, hash, and report item should preserve source provenance.
- Long operations need cancellation, progress, and error recovery.
- Tests should use known tiny forensic images or generated fixtures, not uncontrolled real evidence.
- UI convenience must not hide evidence integrity state, parsing errors, or unsupported filesystem/image features.

## Current Review Queue

## 2026-07-13 - S3-T03 Review

Result: approved for commit.

Findings:

- No blocking issues found.
- `app/backend/api/file_export.py` now verifies successful output writes by reopening the exported artifact, streaming bytes through SHA-256, and counting bytes from disk.
- Returned `ExportResult` and persisted manifest JSON agree on `bytes_requested`, `bytes_written`, `hashes.sha256`, `hashes.status`, final status, and warnings.
- Structured post-write verification failures cover `byte_count_mismatch` and `export_verification_failed`; missing/unreadable output uses hash status `hash_failed`.
- Existing S3-T02 destination safety, exclusive create writes, overwrite refusal, and generic write-failure cleanup behavior remain in place.
- S3-T03 stayed in scope and did not add MD5/SHA-1 production hashing, known-file matching, file signatures, extension mismatch checks, image verification, audit integration, deleted recovery, UI, real parser work, native dependency requirements, or preview-rendered export bytes.

Tests:

- `python -m pytest`: 93 passed in 4.04s.

Residual notes:

- S3-T04 is the next Stage 3 implementation gate and should remain optional/explicit case-store audit integration only.
- Broader hash/signature analysis remains Stage 4.

## 2026-07-13 - S3-T02 Fixture/Stub Export Service Handoff

Result: ready for research/review agent review.

Implemented:

- `app/backend/api/file_export.py` defines a separate raw export content provider protocol, `StubExportContentProvider`, `export_file()`, and `export_file_to_json()`.
- Successful exports require an explicit output directory, use provider-owned raw bytes, write the output file, write a sibling JSON manifest from the S3-T01 result/manifest shape, and return `ExportResult`.
- Destination safety checks run before writing and reject overlap with known source/evidence paths.
- Structured statuses cover `ok`, `path_not_file`, `content_source_unavailable`, `destination_not_selected`, `unsafe_destination`, `invalid_output_name`, `output_exists`, and `export_write_failed`.
- Tests cover successful stub export, manifest JSON, byte equality, result/manifest agreement, missing content, directory entries, missing destination, unsafe destination, traversal/invalid output names, existing output refusal, and provider data non-mutation.

Tests:

- `python -m pytest`: 83 passed.

Scope intentionally not implemented:

- No SHA-256/hash computation; hashes remain `hash_not_computed`.
- No audit integration.
- No deleted-file recovery.
- No UI, search, reporting, real EWF parsing, real partition parsing, real filesystem parsing, required native dependencies, commit, or push.
- No preview-rendered text/hex used as export bytes.

## 2026-07-13 - S3-T02 Review

Result: changes requested.

Findings:

- [P2] `app/backend/api/file_export.py`: `export_file()` checks for existing output/manifest paths, then writes with overwrite-capable `Path.write_bytes()` and `Path.write_text()`. A file appearing between the preflight check and write would be overwritten despite the `output_exists` policy. Use exclusive creation for both output and manifest writes, such as `open("xb")`/`open("x", encoding="utf-8")`, and map `FileExistsError` to structured `output_exists`. Add a regression test that proves an existing output/manifest cannot be overwritten by the write path.
- [P2] `app/backend/api/file_export.py`: if the output file write succeeds and the manifest write fails, `export_file()` returns `export_write_failed` but leaves the exported file behind without a manifest. A failed export should not leave an unmanifested artifact unless the result/warnings explicitly document a partial artifact and the design chooses to retain it. Prefer best-effort cleanup of the just-written output file on manifest-write failure, with a test that simulates manifest-write failure.
- [P2] `app/backend/api/file_export.py`: `ExportRequest.requested_output_path` is captured early but ignored on the success path; the service writes `source.file_name` unless `output_name` is passed. This means an `ExportRequest` asking for `custom.txt` silently writes `hello.txt`, and an unsafe requested path is not validated. Support a safe request-level output name or reject unsupported/unsafe requested paths with `invalid_output_name`; add tests for both safe and traversal-style `ExportRequest.requested_output_path` values.

Tests:

- `python -m pytest`: 83 passed.

Verified good behavior:

- Export content comes from an explicit export provider separate from preview providers.
- The default stub export provider returns raw synthetic bytes and manifests label the content source as stub/synthetic.
- Destination/source overlap, missing destination, non-file entries, missing content, invalid names, and existing outputs are structured in normal preflight paths.
- Result and manifest preserve S3-T01 provenance and keep hashes at `hash_not_computed`.
- S3-T02 did not add SHA-256 computation, audit integration, deleted recovery, UI, real parser work, or native dependency requirements.

Required fix:

- Make overwrite refusal atomic at write time.
- Prevent failed manifest writes from leaving silent unmanifested export artifacts, or explicitly model and test partial-artifact retention if that is the chosen behavior.
- Honor or reject `ExportRequest.requested_output_path` predictably.
- Rerun `python -m pytest`.

## 2026-07-13 - S3-T02 Re-Review

Result: changes requested.

Findings:

- [P2] `app/backend/api/file_export.py`: the write-failure cleanup still misses partial files created by a generic `OSError` inside the exclusive write helpers. `output_created` is set only after `_write_bytes_exclusive()` returns, so if the output helper creates the file and then raises, the `except OSError` path will not clean up the partial output. Likewise, if `_write_text_exclusive()` creates a manifest and then raises, the code cleans up the output but not the partial manifest. For an export workflow, failed writes should not leave silent partial artifacts. In the generic `OSError` path, do best-effort cleanup of both the output path and manifest path, while keeping `FileExistsError` separate so pre-existing files are not removed.

Tests:

- `python -m pytest`: 88 passed.

Verified fixes:

- Output and manifest writes now use exclusive create helpers.
- Write-time `FileExistsError` maps to structured `output_exists`.
- The manifest `FileExistsError` path cleans up the just-written output.
- Safe `ExportRequest.requested_output_path` values are honored, and traversal/path components are rejected with `invalid_output_name`.
- S3-T02 still keeps SHA-256, audit integration, deleted recovery, UI, parser work, and preview-rendered export bytes out of scope.

Required fix:

- In the generic `OSError` branch, best-effort cleanup both output and manifest paths.
- Add regression tests where `_write_bytes_exclusive()` creates a partial output then raises `OSError`, and `_write_text_exclusive()` creates a partial manifest then raises `OSError`.
- Rerun `python -m pytest`.

## 2026-07-13 - S3-T02 Second Re-Review

Result: approved for commit.

Findings:

- No blocking issues found.
- The previous partial-artifact cleanup finding is fixed. Generic `OSError` write failures now best-effort clean up both output and manifest paths.
- `FileExistsError` remains separate, preserving the policy that pre-existing files are reported as `output_exists` and not removed.
- Regression coverage now simulates partial output creation followed by `OSError` and partial manifest creation followed by `OSError`; both paths return structured `export_write_failed` and leave no partial artifact behind.
- Earlier fixes remain in place: exclusive write helpers, write-time `output_exists`, safe `ExportRequest.requested_output_path` support, traversal rejection, and manifest-write failure cleanup.
- S3-T02 stayed in scope and did not add SHA-256 computation, audit integration, deleted recovery, UI, real parser work, native dependency requirements, or preview-rendered export bytes.

Tests:

- `python -m pytest`: 90 passed.

Residual notes:

- S3-T03 should build directly on this accepted write path and add SHA-256 plus byte-count verification only.

## S3-T02 Review Expectations

- Export must use an explicit export content provider/source, separate from preview providers.
- Export must not use rendered preview text/hex as output bytes.
- Destination safety checks must run before writing output or manifest files.
- Source/evidence paths must not be modified.
- Successful S3-T02 exports should write only the expected exported file and manifest JSON under an explicit output directory.
- Result and manifest should preserve S3-T01 provenance and content-source identity.
- SHA-256 must remain `hash_not_computed`; S3-T03 owns hashing.
- S3-T02 should not add audit integration, deleted recovery, UI, real parsers, required native dependencies, or Stage 4 hash/signature scope.

## 2026-07-13 - S3-T01 Export Manifest Contract Handoff

Result: ready for research/review agent review.

Implemented:

- `app/backend/forensic_core/export_manifest.py` defines Stage 3 export contract structures for request, result, manifest, status, warning, source provenance, content-source identity, and hash placeholders.
- Export source provenance preserves Stage 2-style fields including source path, volume id/offset/length, file id/path/name, filesystem type, adapter name, read-only assertion, allocation/deleted state, optional case/evidence ids, and timestamps.
- Content-source identity explicitly records provider name, source kind, read-only assertion, synthetic flag, content size, parser fields, and source status.
- Result/manifest structures include nullable destination/output/manifest paths, nullable byte counts, SHA-256 placeholder fields, destination safety status, UTC timestamps, warnings, and stable JSON serialization helpers.
- Tests cover serialization, JSON dumping, provenance, synthetic content-source labeling, placeholder hash/byte-count fields, warning serialization, non-ok statuses, and UTC timestamp format.

Tests:

- `python -m pytest`: 73 passed.

Scope intentionally not implemented:

- No file export or manifest file writing.
- No hash computation.
- No destination-overlap or source-path safety enforcement beyond placeholder/status fields.
- No case-store audit integration.
- No deleted-file recovery.
- No preview-rendered text/hex used as export bytes.
- No UI, search, reporting, real EWF parsing, real partition parsing, real filesystem parsing, native dependency requirement, commit, or push.

## 2026-07-13 - S3-T01 Review

Result: changes requested.

Findings:

- [P2] `app/backend/forensic_core/export_manifest.py`: `ExportResult.source_read_only` and `ExportManifest.source_read_only` default to `True` independently of `ExportSourceProvenance.read_only`. A caller can construct a result/manifest from a non-read-only source and accidentally serialize `"source_read_only": true` by omission. Because read-only source handling is a forensic integrity assertion, the contract should derive this field from `source.read_only` or default it to a non-assertive value instead of optimistic `True`. Add regression coverage for a source entry with `read_only=False`.

Tests:

- `python -m pytest`: 73 passed.

Verified good behavior:

- S3-T01 stayed contract-only and did not write files or manifests.
- Export content source identity is explicit and distinct from preview rendering.
- Result/manifest structures preserve Stage 2 source provenance and JSON serialization.
- Hash, byte-count, output path, manifest path, and destination-safety fields remain placeholders.
- No audit integration, deleted recovery, UI, real parser work, native dependency requirement, or S3-T02 work was introduced.

Required fix:

- Make `source_read_only` impossible to overstate by default. Prefer deriving the serialized value from `source.read_only` in both result and manifest shapes.
- Add a test proving a non-read-only source serializes as `source_read_only: false`.
- Rerun `python -m pytest`.

## 2026-07-13 - S3-T01 Re-Review

Result: approved for commit.

Findings:

- No blocking issues found.
- The previous read-only assertion finding is fixed. `ExportResult` and `ExportManifest` now serialize `source_read_only` from `source.read_only` when no explicit override is supplied.
- Regression coverage verifies that a source entry with `read_only=False` serializes `source.read_only` and `source_read_only` as false in both result and manifest shapes.
- S3-T01 remains contract-only and did not add file export, manifest writing, hash computation, destination safety enforcement, audit integration, deleted recovery, UI, or parser work.

Tests:

- `python -m pytest`: 74 passed.

Residual notes:

- S3-T02 should build on this contract by adding a separate export content provider/source and destination safety checks before any write.

## 2026-07-13 - Stage 3 Ticket Readiness Review

Result: S3-T01 ready for implementation handoff; later Stage 3 tickets remain Draft.

Findings:

- No code issues reviewed in this pass; this was onboarding/ticketing review only.
- The Stage 3 ticket files existed but were too high-level compared with the Stage 2 ticket prompts.
- Leaving the tickets marked `Ready` risked sending the implementation agent into export work without enough contract detail, status names, test expectations, or scope boundaries.
- The Stage 3 tickets are now marked `Draft` until each ticket is expanded.
- A Stage 3 VS Code familiarization prompt was added at `prompts/vscode-agent/2026-07-13-stage-3-familiarization.md`.
- Follow-up update: S3-T01 is now expanded and marked `Ready`, with a paste-ready implementation prompt at `prompts/vscode-agent/2026-07-13-s3-t01-export-manifest-contract.md`.
- S3-T02 through S3-T06 are expanded as detailed stage plans, but remain `Draft` pending review after each preceding ticket.

Recommended next action:

- Hand S3-T01 to the coding agent using the dedicated prompt.
- S3-T01 should define export request/result/manifest/status/warning/content-source structures and serialization tests.
- S3-T01 should not write files, compute real hashes, add audit events, implement deleted recovery, add UI, add real parsers, or require native dependencies.

Review stance for Stage 3:

- Export bytes must come from an explicit content-source/provider boundary.
- Preview-rendered text/hex must not be used as export bytes.
- Stage 2 filesystem metadata entries must not be treated as byte-bearing objects.
- Destination safety checks must be centralized and heavily tested once file writing begins.
- Manifests must identify whether bytes are stubbed, generated fixture bytes, provider-backed, or later real parser bytes.

## S2-T07 Review Expectations

- Documentation should accurately describe completed Stage 2 behavior and test commands.
- Docs should clearly separate real behavior from stubbed/synthetic/provider-backed behavior.
- Docs should not claim real EWF byte parsing, real partition parsing, real filesystem parsing, UI work, export/recovery, hashing, search, or reporting.
- `Goal.md`, `readme.md`, `plan.md`, `functionality.md`, `progression.md`, `tickets/stage-2/`, and backend docs should agree on Stage 2 status.
- S2-T07 should not add new app behavior or begin Stage 3.

## 2026-07-09 - Stage 2 Final Review Handoff

Result: ready for final Stage 2 review.

Implemented in Stage 2:

- Fixture/dependency strategy for pure stubs, tiny generated files, and optional local-only forensic fixtures.
- Read-only `LocalFileImageStream` for tiny local files and bounded byte reads.
- Whole-image volume discovery boundary.
- Filesystem adapter boundary with deterministic stub entries and dependency-safe `pytsk3` skeleton behavior.
- Backend directory listing/file metadata callable over adapter entries.
- Bounded raw/text/hex preview callable over explicit provider bytes.
- Documentation updates that separate real local-file behavior, stubbed filesystem/listing behavior, and synthetic preview-provider content.

Final review checklist:

- Confirm docs do not claim real EWF byte parsing, real image verification, real partition parsing, real filesystem parsing, or real file extraction.
- Confirm `pyewf`, libewf, `pytsk3`, and The Sleuth Kit remain optional for default tests.
- Confirm Stage 2 API results are not described as automatically persisted to the case store.
- Confirm no export/recovery, hashing/signature analysis, search/timeline, reporting, UI, executable packaging, S2-T08, or Stage 3 work was introduced.
- Confirm manual-test fields remain `Untested` until the user explicitly reports manual testing.

Tests:

- `python -m pytest`: 67 passed.

## 2026-07-09 - Stage 2 Final Review

Result: Stage 2 approved for commit.

Findings:

- No blocking issues found.
- Documentation accurately describes Stage 2 as a backend browsing/preview foundation using real local-file byte-stream behavior, stubbed volume/filesystem/listing behavior, and synthetic preview-provider bytes.
- Docs clearly state that real EWF byte parsing, image verification, partition parsing, filesystem parsing, real file extraction, UI, export/recovery, hashing/signatures, search/timeline, reporting, executable packaging, and automatic Stage 2 result persistence are not implemented.
- Dependency notes keep `pyewf`, libewf, `pytsk3`, and The Sleuth Kit optional for default tests.
- Manual-test fields remain `Untested`, as expected.
- S2-T07 stayed docs/status-only and did not begin Stage 3.

Tests:

- `python -m pytest`: 67 passed.

Residual notes:

- `tickets/README.md` had one stale Stage 2 status line saying "planned next"; this review corrected it to Stage 2 complete at handoff and Stage 3 planned next.

## S2-T06 Review Expectations

- Preview code should use bounded, read-only reads from a stub or tiny generated preview source.
- Preview results should be JSON-friendly and preserve source, volume, file id/path, offset, requested length, returned length, mode, truncation, status, and warnings.
- Text preview should handle decoding errors visibly and safely; hex preview should be deterministic.
- Missing files, directories, invalid ranges, unsupported modes, and size-limit truncation should return structured statuses or warnings.
- S2-T06 should not add export/recovery, hashing, UI work, real filesystem parsing, required native dependencies, persistence, or real evidence fixtures.

## 2026-07-09 - S2-T06 Review

Result: changes requested.

Findings:

- [P2] `app/backend/api/file_preview.py`: `preview_file()` reports `status.code == "ok"` when `offset` is beyond the available preview content and `length` is omitted. Example: `/hello.txt` has 13 stub bytes, but `preview_file(entry, mode="text", offset=99)` returns `ok`, zero bytes, empty text, and no truncation warning. A preview offset outside the content should be a structured non-ok status or warning, such as `preview_truncated`, `content_unavailable`, or a dedicated range status. This matters because a forensic preview boundary should not quietly report success for a range that cannot exist.

Tests:

- `python -m pytest`: 66 passed.

Verified good behavior:

- Text, hex, and raw preview outputs are JSON-friendly.
- Stub preview content is clearly labeled as synthetic, not parsed evidence.
- Negative offset/length, unsupported mode, directory entry, missing content, max-length truncation, content-size truncation with an explicit length, decode replacement, and provenance/read-only fields are covered.
- S2-T06 stayed in scope and did not add export/recovery, hashing, UI, persistence, native dependency requirements, real parsing, S2-T07, or Stage 3 work.

Required fix:

- Add a regression test for `offset > source_content_size` with omitted `length`.
- Return a structured non-ok status/warning for that case.
- Keep the change inside S2-T06 and rerun `python -m pytest`.

## 2026-07-09 - S2-T06 Review Fix Handoff

Result: ready for re-review.

Implemented:

- `preview_file()` now returns structured `content_unavailable` status when the requested offset is beyond provider content size.
- Added regression coverage for `offset > source_content_size` with omitted `length`, preserving provenance, read-only fields, zero returned bytes, and JSON-friendly shape.

Tests:

- `python -m pytest`: 67 passed.

Scope intentionally not implemented:

- No S2-T07 or Stage 3 work.
- No export/recovery, hashing, UI, persistence, native dependency requirement, real filesystem parsing, or real evidence fixture.

## 2026-07-09 - S2-T06 Re-Review

Result: approved for commit.

Findings:

- No blocking issues found.
- The previous offset-boundary finding is fixed: `preview_file(..., offset=99)` for the 13-byte stub file now returns structured `content_unavailable` instead of `ok`.
- Regression coverage verifies non-ok status, zero returned bytes, no preview payload, preserved source size, read-only provenance, and a `content_unavailable` warning.
- Existing text, hex, raw serialization, truncation, missing content, directory/non-file, unsupported mode, invalid range, decode replacement, and provenance tests still pass.
- S2-T06 stayed in scope and did not add S2-T07, Stage 3, export/recovery, hashing, UI, persistence, native dependencies, real filesystem parsing, or real evidence fixtures.

Tests:

- `python -m pytest`: 67 passed.

## 2026-07-09 - S2-T06 Preview Foundation Handoff

Result: ready for research/review agent review.

Implemented:

- `preview_file()` backend API callable for provider-backed raw/text/hex previews.
- `preview_file_to_json()` serialization helper.
- `StubPreviewProvider` with synthetic bytes for `stub-file-hello` (`/hello.txt`).
- JSON-friendly preview result shape with source path, volume id/offset/length, file id/path/name/type, requested offset/length, returned bytes, source content size, truncation flag, read-only assertion, provider details, mode, status, preview data, and warnings.
- Tests for text, hex, raw JSON serialization, bounded offset/length, max-length truncation, content-size truncation, missing content, directory entry rejection, unsupported mode, invalid ranges, decode replacement warning, and provenance/read-only fields.

Scope intentionally not implemented:

- No real filesystem byte extraction.
- No real EWF, partition, or filesystem parsing.
- No export/recovery or hashing.
- No UI, persistence, background jobs, or case-store writes.
- No required native dependency or real evidence fixture.

Suggested review command:

```powershell
python -m pytest
```

## S2-T05 Review Expectations

- Directory listing view should consume the filesystem adapter boundary instead of parsing real filesystems directly.
- Root listing should return deterministic JSON-friendly entries from the stub adapter.
- Unsupported, missing, file, or nested paths should return structured status/warning results unless explicitly supported.
- Adapter dependency-unavailable or real-parser-not-implemented states should be visible in the listing response.
- S2-T05 should not add raw/text/hex preview, export/recovery, hashing, UI work, real filesystem parsing, or required native dependencies.

## 2026-07-09 - S2-T05 Review

Result: approved for commit.

Findings:

- No blocking issues found.
- `list_directory()` consumes `FilesystemAdapter.inspect_volume()` and returns a JSON-friendly directory listing response without parsing real filesystems directly.
- Stub root listing returns deterministic `/Documents` and `/hello.txt` metadata entries with source, volume, adapter, filesystem, status, timestamp, allocation/deleted, and read-only provenance preserved.
- Unsupported nested paths, file paths, unknown paths, dependency-unavailable adapters, importable-but-not-implemented pytsk3, and defensive adapter exceptions are represented as structured statuses.
- Tests do not require `pytsk3`, The Sleuth Kit, real filesystems, real evidence, private fixtures, or network access.
- S2-T05 stayed in scope and did not add file-content preview, export/recovery, hashing, UI work, persistence, case-store writes, real filesystem parsing, or required native dependencies.

Tests:

- `python -m pytest`: 53 passed.

Residual notes:

- The default adapter path is dependency-safe but normally returns `filesystem_unavailable` until real pytsk3 parsing exists. For current smoke/manual checks, callers should pass `StubFilesystemAdapter`.

## 2026-07-09 - S2-T05 Directory Listing Handoff

Result: ready for research/review agent review.

Implemented:

- `list_directory()` backend API callable over `FilesystemAdapter.inspect_volume()`.
- `directory_listing_to_json()` serialization helper.
- Root listing for `StubFilesystemAdapter` returning `/Documents` and `/hello.txt`.
- Structured statuses for `ok`, `path_not_found`, `path_not_directory`, `path_unsupported`, `filesystem_unavailable`, and defensive `filesystem_error`.
- Tests for root listing, JSON shape, provenance/read-only fields, unsupported nested path, file path, unknown path, path normalization, and pytsk3 dependency-unavailable/not-implemented states.

Scope intentionally not implemented:

- No file-content reads or raw/text/hex preview.
- No export/recovery or hashing.
- No UI, persistence, background jobs, or case-store writes.
- No real filesystem parsing or required native dependency.
- No real evidence or filesystem images.

Suggested review command:

```powershell
python -m pytest
```

## S2-T04 Review Expectations

- Filesystem adapter boundary should expose stable result/status/entry shapes.
- Tests must pass without `pytsk3`, The Sleuth Kit, real filesystems, or evidence images.
- Stub adapter should provide deterministic entries for later directory listing work.
- Dependency-unavailable behavior should be structured, not an import crash.
- S2-T04 should not add directory-listing CLI/workflow, preview rendering, export/recovery, or required native dependencies.

## 2026-07-09 - S2-T04 Review

Result: approved for commit.

Findings:

- No blocking issues found.
- `filesystem_adapter.py` defines stable JSON-friendly adapter, dependency, result, status, warning, and entry shapes.
- `StubFilesystemAdapter` returns deterministic root entries for `/Documents` and `/hello.txt`.
- `Pytsk3FilesystemAdapter` reports `dependency_unavailable` when `pytsk3` is missing and `real_parser_not_implemented` when a pytsk3 module is importable but real parsing is still deferred.
- Tests do not require `pytsk3`, The Sleuth Kit, real filesystems, real evidence, or private fixtures.
- S2-T04 stayed in scope and did not add directory-listing workflow, preview rendering, export/recovery, hashing, UI work, or required native dependencies.

Tests:

- `python -m pytest`: 44 passed.

Residual notes:

- Stub entry `/hello.txt` is metadata-only for now. S2-T05/S2-T06 should not assume file content exists until a listing/preview content boundary is explicitly added.

## 2026-07-09 - S2-T04 Filesystem Adapter Handoff

Result: ready for research/review agent review.

Implemented:

- `FilesystemAdapter` protocol and JSON-friendly result/status/warning/dependency/entry structures.
- `StubFilesystemAdapter` with deterministic root entries for `/Documents` and `/hello.txt`.
- `Pytsk3FilesystemAdapter` skeleton that reports `dependency_unavailable` when `pytsk3` is missing and `real_parser_not_implemented` when injected/importable but still deferred.
- Entry provenance fields for source path, volume id, volume offset/length, filesystem type, adapter name, read-only assertion, allocation/deleted state, timestamps, status, and warnings.
- Tests for stub metadata/result shape, root entries, read-only provenance, pytsk3 dependency-unavailable behavior, JSON serialization, and importable-but-unimplemented pytsk3 status.

Scope intentionally not implemented:

- No directory-listing CLI/workflow.
- No real filesystem parsing.
- No preview rendering.
- No export/recovery, hashing, or native dependency requirement.
- No real evidence or filesystem images.

Suggested review command:

```powershell
python -m pytest
```

## S2-T03 Review Expectations

- Volume discovery should produce structured JSON-friendly results with provenance.
- Whole-image/single-volume behavior is acceptable for S2-T03.
- Missing, unreadable, or zero-byte sources should be handled predictably.
- S2-T03 should not introduce filesystem parsing, pytsk3/TSK requirements, preview rendering, export/recovery, or real evidence fixtures.

## 2026-07-09 - S2-T03 Review

Result: approved for commit.

Findings:

- No blocking issues found.
- `discover_volumes()` defines a JSON-friendly volume discovery boundary over `ImageByteStream`.
- Whole-image/single-volume behavior works for readable non-empty streams.
- Missing/unavailable streams, zero-byte sources, and unsupported partition strategies return structured statuses and warnings.
- Tests use tiny generated files and do not require real evidence or native forensic dependencies.
- S2-T03 stayed in scope and did not add filesystem parsing, preview rendering, export/recovery, hashing, UI work, or real partition parsing.

Tests:

- `python -m pytest`: 38 passed.

Residual notes:

- Volume id is currently the stable placeholder `volume-0` for whole-image strategy. Future real partition parsing should define deterministic ids from source/evidence id plus partition metadata.

## 2026-07-09 - S2-T03 Volume Discovery Handoff

Result: ready for research/review agent review.

Implemented:

- `discover_volumes()` volume discovery boundary over `ImageByteStream`.
- Whole-image/single-volume behavior for readable non-empty streams.
- Structured statuses for successful discovery, unavailable image stream, zero-byte image, and unsupported partition parsing strategies.
- JSON-friendly result objects with source path, stream type, source size, read-only assertion, volume id/index, offset, length, type, description, status, and warnings.
- Generated-file tests for non-empty local source, zero-byte source, missing source, serialization shape, read-only provenance, and unsupported partition strategy.

Scope intentionally not implemented:

- No real partition table parsing.
- No filesystem adapter or directory listing.
- No preview rendering.
- No export/recovery, hashing, or native forensic dependencies.
- No real evidence or binary forensic fixtures.

Suggested review command:

```powershell
python -m pytest
```

## S2-T02 Review Expectations

- Byte stream implementation must be read-only and bounded by offset/length.
- Tests should use tiny generated files under ignored paths, not evidence images.
- Missing paths, directories, and invalid ranges should return structured errors or documented exceptions.
- S2-T02 should not introduce volume parsing, filesystem parsing, preview rendering, export/recovery, or native forensic dependencies.

## 2026-07-09 - S2-T02 Review

Result: approved for commit.

Findings:

- No blocking issues found.
- `LocalFileImageStream` provides read-only local file metadata and bounded `read_at(offset, length)` behavior.
- Structured statuses cover missing paths, directories, unreadable/non-regular files, invalid ranges, reads beyond EOF, and successful reads.
- Tests use tiny generated files under ignored workspace paths and do not require real evidence or native forensic dependencies.
- S2-T02 stayed in scope and did not add volume discovery, filesystem parsing, preview rendering, export/recovery, hashing, or UI work.

Tests:

- `python -m pytest`: 32 passed.

Residual notes:

- Offset exactly at EOF with a nonzero length currently returns status `ok` with zero bytes and a `read_truncated_at_eof` warning. This is acceptable for now; later preview/volume callers should treat `bytes_read` and warnings as authoritative.

## 2026-07-09 - S2-T02 Image Byte-Stream Handoff

Result: ready for research/review agent review.

Implemented:

- `LocalFileImageStream` read-only local file-backed stream.
- Structured stream metadata, read result, status, and warning objects.
- Bounded `read_at(offset, length)` reads with source path, stream type, size, read-only assertion, status, and warning provenance.
- Generated-file tests for metadata, normal ranges, offset zero, EOF truncation, read beyond EOF, missing paths, directory paths, negative offset/length, and zero-length reads.

Scope intentionally not implemented:

- No volume discovery.
- No filesystem adapter.
- No directory listing.
- No raw/text/hex preview renderer.
- No export/recovery, hashing, or native forensic dependencies.

Suggested review command:

```powershell
python -m pytest
```

## S2-T01 Review Expectations

- Confirm `app/fixtures/README.md` defines a clear Stage 2 fixture strategy.
- Confirm default Stage 2 tests remain free of private evidence, large images, `pyewf`, libewf, `pytsk3`, and The Sleuth Kit.
- Confirm optional real raw/EWF/TSK fixtures are documented as local-only and opt-in.
- Confirm S2-T01 does not add byte-stream, volume-discovery, filesystem-adapter, preview, export, hash, or UI implementation.
- Confirm missing native dependencies are expected to become structured status results, not raw crashes or default test blockers.

## 2026-07-09 - S2-T01 Review

Result: approved for commit.

Findings:

- No blocking issues found.
- Stage 2 fixture tiers are clear: pure stubs, tiny generated files, and optional local-only forensic fixtures.
- Default tests remain free of private evidence, large images, `pyewf`, libewf, `pytsk3`, and The Sleuth Kit.
- Optional real raw/EWF/TSK fixtures are documented as local-only and opt-in.
- S2-T01 stayed documentation-only and did not add byte-stream, volume, filesystem, preview, export, hash, or UI implementation.

Tests:

- `python -m pytest`: 22 passed.

Residual notes:

- S2-T02 should use this strategy to define read-only byte-stream tests around tiny generated files and structured missing/unreadable path behavior.

## 2026-07-09 - S2-T01 Fixture/Dependency Strategy Handoff

Result: ready for research/review agent review.

Implemented documentation:

- Stage 2 fixture tiers: pure stubs, tiny generated files, and optional local-only forensic fixtures.
- Guidance for S2-T02 through S2-T06 on which tests should use stubs versus generated bytes.
- Later real-fixture rules for legal training images, regeneration notes, expected hashes/sizes, and opt-in integration tests.
- Stage 2 dependency policy making `pytsk3`, The Sleuth Kit, `pyewf`, and libewf optional for default tests.

Scope intentionally not implemented:

- No image/byte-stream abstraction.
- No volume discovery.
- No filesystem adapter.
- No pytsk3 dependency addition.
- No real evidence or binary fixtures.

Suggested review command:

```powershell
python -m pytest
```

## S1-T06 Review Expectations

- Docs should accurately describe current Stage 1 behavior and limitations.
- Test commands should be current and runnable.
- The handoff should not claim real EWF parsing, filesystem parsing, UI, or automatic persistence.
- The final Stage 1 review section should make it clear what is ready for Stage 2 planning.

## 2026-07-09 - Stage 1 Final Review

Result: Stage 1 complete at the planning/review level.

Verified Stage 1 scope:

- Backend skeleton exists and imports.
- E01 segment discovery is implemented and tested without real evidence.
- EWF reader adapter boundary is implemented with stub and pyewf-unavailable behavior.
- Intake JSON callable/CLI exists and handles invalid input/dependency states.
- SQLite case-store schema exists for cases, evidence sources, audit events, and schema migration marker.
- Documentation clearly states that real EWF byte parsing, filesystem parsing, UI, and automatic intake persistence are not implemented yet.

Stage 2 readiness:

- Stage 2 tickets exist under `tickets/stage-2/`.
- Stage 2 should begin with fixture/dependency strategy before implementing byte streams or filesystem adapters.
- Review should continue enforcing read-only source handling, structured unsupported-dependency behavior, and no private evidence in tests.

Stage 3 readiness:

- Stage 3 tickets exist under `tickets/stage-3/`.
- Stage 3 should not begin until Stage 2 provides a stable file/metadata source.

## 2026-07-09 - Stage 1 Final Review Handoff

Result: ready for research/review agent final Stage 1 review.

Implemented capabilities to verify:

- Backend Python package skeleton and pytest configuration.
- E01 segment discovery with ordered segments and structured warnings.
- EWF reader adapter boundary with stub metadata, verification status shape, and pyewf dependency-unavailable behavior.
- Intake JSON command/callable through `python -m app.backend.api.intake path\to\sample.E01`.
- SQLite schema/helpers for `cases`, `evidence_sources`, `audit_events`, and `schema_migrations`.

Current limitations to keep visible:

- No real EWF byte parsing or real image verification yet.
- No partition/filesystem parsing yet.
- No UI yet.
- No automatic persistence from intake command to SQLite yet.
- `pyewf`/libewf is optional and not required for tests.
- No real forensic evidence is required for tests.

Review commands:

```powershell
python -m pytest
python -m app.backend.api.intake path\to\sample.E01 --adapter stub
```

Expected S1-T06 test result:

- `python -m pytest`: 22 passed.

Suggested final review checklist:

- Confirm documentation does not overclaim Stage 1 behavior.
- Confirm test and intake commands are accurate on Windows.
- Confirm no Stage 2 filesystem/UI work was introduced.
- Confirm `plan.md`, `progression.md`, ticket status, and backend docs agree.

## 2026-07-09 - S1-T05 Review

Result: approved for commit.

Findings:

- No blocking issues found.
- Schema includes `cases`, `evidence_sources`, `audit_events`, and `schema_migrations`.
- Evidence source rows preserve S1-T04 intake provenance through source paths, segment discovery JSON, adapter/dependency JSON, metadata JSON, verification JSON/status, warnings JSON, read-only assertion, and timestamps.
- Audit events link to cases and optionally evidence sources.
- Tests use in-memory SQLite and do not require real evidence or persistent user data.
- The implementation stayed in scope and did not wire automatic intake persistence, UI, filesystem parsing, or real EWF parsing.

Tests:

- `python -m pytest`: 22 passed.

Residual notes:

- Audit timestamps currently use second precision. This is acceptable for the Stage 1 foundation, but later audit-heavy workflows may want higher precision or an explicit monotonic sequence.

## S1-T05 Review Expectations

- Schema should include cases, evidence_sources, and audit_events.
- Evidence source records should preserve enough provenance for S1-T04 intake output.
- Tests should use in-memory or temporary SQLite databases, not persistent user data.
- The implementation should not broaden into UI, filesystem parsing, or automatic full case workflow.
- Audit events should be generic enough to record future actions without schema churn.

## 2026-07-09 - S1-T04 Re-Review

Result: approved for commit.

Findings:

- No blocking issues found.
- The previous status-contract issue is fixed: importable-but-unimplemented pyewf now returns `reader_not_implemented` instead of `ok`.
- Stub-backed intake still returns `ok`.
- Missing-pyewf intake still returns `metadata_unavailable`.
- The intake command remains scoped to S1-T04 and does not add SQLite, UI, filesystem parsing, or real EWF parsing.

Tests:

- `python -m pytest`: 18 passed.

Residual notes:

- The CLI currently returns nonzero only for `invalid_input`; future stages may decide whether `reader_not_implemented` or `metadata_unavailable` should also have nonzero CLI exit codes.

## 2026-07-09 - S1-T04 Review

Result: changes requested.

Findings:

- [P2] `app/backend/api/intake.py`: `run_e01_intake()` reports `status: "ok"` whenever `adapter_available` is true. If `PyewfEwfReaderAdapter` is importable but real metadata extraction is still deferred, it returns empty metadata plus `real_reader_not_implemented`, yet intake status is `"ok"`. That would mislead future users who install `pyewf` before real parsing is implemented.

Tests:

- `python -m pytest`: 17 passed.

Good notes:

- The intake layer correctly composes segment discovery and EWF adapter output.
- Invalid input returns structured JSON-style data rather than a traceback.
- CLI behavior for invalid input is tested.
- No SQLite, filesystem parsing, UI work, real evidence, or native dependency requirement was added.

## S1-T04 Review Expectations

- Intake command should compose segment discovery and reader adapter output without duplicating their logic.
- Output should be JSON-serializable and stable enough for future UI use.
- Tests must pass without real evidence or native forensic dependencies.
- Invalid input should not produce raw tracebacks for expected user mistakes.
- S1-T04 must not add case storage, filesystem parsing, or UI work.

## 2026-07-09 - S1-T03 Review

Result: approved for commit.

Findings:

- No blocking issues found.
- The adapter boundary is separate from segment discovery.
- The stub adapter returns predictable synthetic metadata and verification shape for tests.
- The pyewf adapter skeleton handles missing `pyewf` as structured dependency-unavailable data, not a raw import crash.
- Tests do not require real evidence, pyewf, or libewf.

Tests:

- `python -m pytest`: 12 passed.

Residual notes:

- Real pyewf metadata extraction is intentionally deferred beyond S1-T03.
- Result dataclasses contain normal dictionaries; this is acceptable for the current boundary, but later evidence-facing code should avoid mutating returned result objects in place.

## S1-T03 Review Expectations

- Adapter interface should be separate from segment discovery.
- Tests must pass without `pyewf`, libewf, or real E01 evidence.
- Stub adapter should return predictable metadata and verification status.
- Missing dependency behavior should be structured and visible, not a raw import crash.
- Real pyewf adapter code, if added, should be optional and read-only by design.

## 2026-07-09 - S1-T02 Re-Review

Result: approved for commit.

Findings:

- No blocking issues found.
- The previous `.E00` issue is fixed: `.E00` is treated as an unsupported sibling segment and is not included in discovered segments.
- Regression coverage was added for `.E00`.
- Segment discovery remains dependency-free and read-only; it only inspects path names and directory entries.

Tests:

- `python -m pytest`: 8 passed.

Residual notes:

- Old ignored scratch/cache folders from earlier temp-directory experiments may remain locally, but they do not affect tests or Git-tracked files.

## S1-T02 Review Expectations

- Segment discovery must use temporary dummy files or mocks, not real E01 evidence.
- The code should not parse EWF content yet; that belongs to S1-T03 and later.
- Results should be structured and stable enough for the later intake JSON command.
- Missing/gap behavior should be visible through warnings or a documented exception/result.
- Tests should cover valid chains, invalid input, and gaps.

## 2026-07-09 - S1-T02 Initial Review

Result: changes requested.

Findings:

- [P2] `app/backend/forensic_core/segment_discovery.py`: `_parse_segment_number()` accepts `.E00` as segment number `0`. When `sample.E00` sits next to `sample.E01`, discovery includes `.E00` in `segments`, emits no warning, and marks the set complete. Stage 1 discovery should treat `.E00` as unsupported/invalid because the selected evidence chain starts at `.E01`.

Tests:

- `python -m pytest`: 7 passed.

Good notes:

- The implementation stays dependency-free and does not parse evidence bytes.
- The result shape is clear and future JSON-friendly.
- Tests use dummy workspace-local files, not real evidence.
- The pytest temp/cache mitigation is working; the latest test run completed without warnings.

## 2026-07-09 - S1-T01/S1-T01A Review

Result: approved for commit.

Findings:

- No blocking issues found.
- The backend package skeleton is intentionally minimal and stays within S1-T01 scope.
- Smoke tests cover package import and backend subpackage import.
- `.gitignore` covers Python cache/test artifacts, virtual environments, and common build outputs.
- `python -m pytest` passed: 2 tests passed, 1 warning.

Residual notes:

- Pytest still reports a non-blocking cache warning under `.pytest_cache`; tests pass.
- No E01 logic is expected in S1-T01. Segment discovery should begin in S1-T02.
