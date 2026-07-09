# Functionality - Feature Inventory

Purpose: use this file as the living feature checklist. Each feature should eventually have acceptance criteria, test cases, and a status.

Status labels:

- `Done`: implemented, reviewed, and committed or ready to commit.
- `In Progress`: active ticket work.
- `Planned`: planned but not started.
- `Untested`: not manually tested by the user yet. Automated tests may still exist.
- `Deferred`: intentionally out of current scope.

Initial feature groups to track:

- Evidence image intake: detect segmented `.E01/.E02/...` sets, read metadata, verify integrity, expose a read-only byte stream.
- Case management: create/open cases, attach evidence sources, record examiner notes, preserve an audit log.
- Filesystem viewing: partition/volume discovery, filesystem tree, file metadata, raw preview, hex preview, text preview.
- File recovery/export: export active files, deleted files when supported, and carved files with provenance metadata.
- Hash analysis: MD5/SHA-1/SHA-256 calculation, image verification, file hash database matching, known-good filtering.
- File signature analysis: magic-byte detection, extension mismatch detection, MIME/category classification.
- Search and indexing: filename search, metadata search, keyword/full-text search, filters, saved queries.
- Timeline: file MACB timestamps, sortable events, filters by source/path/type/time.
- Reporting: bookmarks, tagged evidence, exportable report, chain-of-custody/audit information.

## Stage 1 Feature Targets

- E01 path validation.
- Segment chain discovery.
- Segment gap/missing-file reporting.
- Reader adapter interface.
- Dependency-unavailable fallback behavior.
- Evidence metadata response.
- Verification status field, even if verification is not implemented yet.
- Read-only access guarantee.
- Basic case/evidence/audit schema draft.
- Automated tests for the above.

## Feature Status

| Feature | Stage | Status | Manual Test | Notes |
| --- | --- | --- | --- | --- |
| Python backend package skeleton | 1 | Done | Untested | Automated import tests pass. |
| E01 segment discovery by sibling filenames | 1 | Done | Untested | Does not parse EWF bytes. |
| Segment warnings for gaps/unsupported names | 1 | Done | Untested | Includes `.E00` regression coverage. |
| EWF reader adapter boundary | 1 | Done | Untested | Stub and pyewf-unavailable paths only. |
| JSON intake callable/CLI | 1 | Done | Untested | `python -m app.backend.api.intake path\to\sample.E01`; no real EWF parsing yet. |
| SQLite case/evidence/audit schema | 1 | Done | Untested | No automatic intake persistence yet. |
| Stage 1 documentation handoff | 1 | Done | Untested | Stage 1 limitations documented. |
| Fixture/dependency strategy | 2 | Done | Untested | S2-T01; documentation/strategy only. |
| Read-only image/byte-stream abstraction | 2 | Done | Untested | S2-T02; local file-backed read-only stream with tiny generated test files. |
| Volume discovery boundary | 2 | Done | Untested | S2-T03; whole-image volume result for readable non-empty streams. |
| Filesystem adapter boundary | 2 | Planned | Untested | S2-T04. |
| Directory listing and file metadata | 2 | Planned | Untested | S2-T05. |
| Raw/text/hex preview foundation | 2 | Planned | Untested | S2-T06. |
| Export manifest contract | 3 | Planned | Untested | S3-T01. |
| Fixture/stub file export service | 3 | Planned | Untested | S3-T02. |
| Export hashing and byte-count verification | 3 | Planned | Untested | S3-T03. |
| Export audit integration | 3 | Planned | Untested | S3-T04. |
| Deleted-file recovery | 3 | Planned | Untested | Conditional on filesystem adapter support. |
| Hash/signature analysis | 4 | Planned | Untested | Broader analysis stage; not Stage 3. |
| Search/timeline | 5 | Planned | Untested | Not started. |
| Reporting/workflow | 6 | Planned | Untested | Not started. |
| Desktop UI/executable packaging | Later | Deferred | Untested | CLI/manual testing comes first. |

Manual testing note: Stage 1 has automated tests but has not been manually exercised by the user as an app workflow. Keep the manual-test column at `Untested` until the user confirms a manual run.
