# Functionality - Feature Inventory

Purpose: use this file as the living feature checklist. Each feature should eventually have acceptance criteria, test cases, and a status.

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
