# Functionality - Feature Inventory

Purpose: use this file as the living feature checklist. Each feature should eventually have acceptance criteria, test cases, and a status.

Status labels:

- `Done`: implemented, reviewed, and committed or ready to commit.
- `In Progress`: active ticket work.
- `Review`: implementation is complete and waiting for research/review acceptance.
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
| Filesystem adapter boundary | 2 | Done | Untested | S2-T04; stub entries and pytsk3 dependency-safe skeleton. |
| Directory listing and file metadata | 2 | Done | Untested | S2-T05; backend root listing over filesystem adapter entries. |
| Raw/text/hex preview foundation | 2 | Done | Untested | S2-T06; bounded stub-provider raw/text/hex previews. |
| Stage 2 documentation handoff | 2 | Done | Untested | S2-T07; documentation/review wrap-up only. Stage 2 final review handoff is ready. |
| Export manifest contract | 3 | Done | Untested | S3-T01 contract structures and tests are reviewed; no file export yet. |
| Fixture/stub file export service | 3 | Done | Untested | S3-T02 reviewed; exports explicit stub/provider bytes only. |
| Export hashing and byte-count verification | 3 | Done | Untested | S3-T03 reviewed; verifies written export artifacts with SHA-256 and on-disk byte counts. Broader hash analysis remains Stage 4. |
| Export audit integration | 3 | Done | Untested | S3-T04 reviewed; audit is explicit opt-in through `ExportAuditContext`. |
| Deleted-file recovery | 3 | Deferred | Untested | S3-T05 reviewed; recovery remains unsupported/deferred until a real adapter exposes recoverable deleted-file bytes. |
| Stage 3 documentation handoff | 3 | Done | Untested | S3-T06 reviewed; documentation/review handoff only, no new behavior. |
| Reality-anchor content path | 4/Future | Planned | Untested | S4-T00 risk audit recorded the gap; S4-T01 must preserve source-kind/provider fields for synthetic, generated fixture, local-stream, and future real-parser bytes. |
| Hash/signature analysis contracts | 4 | Done | Untested | S4-T01 reviewed; request/result/provenance/content-source placeholder contracts only. No hashes are computed and no signatures are detected. |
| Provider-backed hash behavior | 4 | Done | Untested | S4-T02 reviewed; hashes are computed only from explicit Stage 4 analysis content providers. SHA-256 is default, while MD5/SHA-1 are optional comparison hashes. |
| Provider-backed signature behavior | 4 | Done | Untested | S4-T03 reviewed; magic-byte detection uses bounded explicit Stage 4 analysis provider bytes only. |
| Extension mismatch rules | 4 | Done | Untested | S4-T04 reviewed; mismatch evaluation consumes reviewed signature results and file metadata only, with no provider byte reads. |
| Known-file matching | 4 | Done | Untested | S4-T05 reviewed; matching consumes reviewed hash results and caller-supplied in-memory records only, with no external datasets, persistence, byte reads, or implicit hash calculation. |
| Analysis-result persistence plan | 4 | Done | Untested | S4-T06 reviewed; it defers schema/behavior changes while documenting explicit opt-in future persistence requirements. |
| Stage 4 documentation handoff | 4 | Done | Untested | S4-T07 reviewed; it reconciled Stage 4 docs and prepared Stage 5 readiness notes without code or behavior changes. |
| First manual E01 testing workflow | 4.5 | Review/Partial | Partial | S4.5-IMP01, S4.5-IMP02, S4.5-IMP02A, S4.5-IMP03, S4.5-IMP04, S4.5-IMP05, and S4.5-IMP06 are reviewed and done. S4.5-IMP03 portable-runtime smoke against the local E01 set produced EWF stream, partition-table volume, filesystem, root-listing, and demo-readiness artifacts with a real-parser-backed root listing. S4.5-IMP04 adds explicit selected-file content providers and selected-file readiness/preview/analysis/export artifacts, with real selected-file extraction still requiring an approved explicit file selection. S4.5-IMP05 adds root-listing-derived file-list JSON/CSV and a static local HTML summary; its real-image no-selection smoke produced file-list/HTML outputs without auto-selecting files. S4.5-IMP06 adds guardrail/review handoff reconciliation, and S4.5-IMP07 remains drafted for the command-line testing guide. Full recursive traversal, broad crawl, and final manual E01 workflow guide still do not exist. |
| Documentation organization cleanup | 5 | Done | Untested | S5-T00 reduced duplicate status narratives, clarified source-of-truth ownership, and reviewed unused/confusing markdown structures before search/timeline work. |
| Search/timeline | 5 | Deferred | Untested | S5-T01 is done with a failed-gate result; S5-T01A hardened older Stage 4.5 wording; S5-T02 through S5-T16 remain drafted behind the Stage 4.5 substantial-test requirement. Search/timeline implementation must wait until the Stage 4.5 implementation runway is completed and reviewed. |
| Reporting/workflow | 6 | Planned | Untested | Not started. |
| Desktop UI/executable packaging | Later | Deferred | Untested | CLI/manual testing comes first. |

Manual testing note: Stage 1 through Stage 4 have automated tests but have not been manually exercised by the user as an app workflow. S4.5-IMP01 through S4.5-IMP03 now have reviewer-run real-image smoke coverage for intake, metadata, EWF stream, partition-table discovery, and root listing. S4.5-IMP04 has automated fake-parser coverage for selected-file content providers and a real-image no-selection smoke showing selected-file artifacts stay `not_run` until an explicit safe file is selected. S4.5-IMP05 has automated file-list/HTML coverage and a real-image no-selection smoke showing root-listing-derived file-list JSON/CSV plus static HTML output. Keep full selected-file real-E01 extraction, recursive traversal, broad crawl, and final guide workflow untested until those behaviors are exercised with approved selections.
