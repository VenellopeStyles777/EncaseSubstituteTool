# Research - EnCase-Style Forensic Analysis App

Purpose: use this file for research notes, source links, architecture reasoning, and technical recommendations. This should stay implementation-facing rather than becoming a generic essay.

Last updated: 2026-07-08

## Source Notes

- OpenText Forensic, formerly EnCase Forensic, is described by OpenText as software for collecting, triaging, analyzing, and reporting on digital evidence while maintaining evidential integrity. Source: https://www.opentext.com/products/encase-forensic
- OpenText lists current EnCase/OpenText Forensic use cases and features including evidence acquisition, triage, AI-assisted review, reporting, artifact workflows, broad device/filesystem support, encrypted filesystem acquisition, automation, indexing, timeline view, volume shadow copy analysis, E01/L01 formats, hashing, action logging, deleted-file recovery, unallocated-space analysis, artifact parsing, and chain of custody. Source: https://www.opentext.com/products/encase-forensic
- libewf is an open-source library for the Expert Witness Compression Format. It supports EnCase `.E01` and `.Ex01`, provides tools such as `ewfinfo`, `ewfexport`, `ewfmount`, and `ewfverify`, and can expose EWF evidence data for other tooling. Source: https://github.com/libyal/libewf
- The Sleuth Kit is a library and command-line toolkit for investigating disk images, especially volume and filesystem data, and can be incorporated into larger forensic tools. Source: https://www.sleuthkit.org/sleuthkit/
- NIST NSRL provides a Reference Data Set of file profiles and digital signatures that investigators can use to match known files and reduce review effort. Source: https://www.nist.gov/itl/csd/secure-systems-and-applications/national-software-reference-library-nsrl

## Essential EnCase-Like Functionality

For this project, "EnCase-like" should mean a defensible forensic workstation for offline evidence analysis, not a full commercial replacement on day one.

Core functions:

- Case workspace: create a case, add evidence, store examiner notes, preserve an audit trail, and keep generated analysis separate from original evidence.
- Evidence image intake: detect segmented EWF sets (`.E01`, `.E02`, `.E03`, ...), read metadata, verify image checksums/hashes, and expose a read-only logical byte stream.
- Volume and partition discovery: parse partition tables, list volumes, show offsets, sizes, filesystem types, and unsupported regions.
- Filesystem browsing: show directory trees, file metadata, timestamps, permissions/attributes, deleted-file state when supported, alternate data streams where supported, and raw path provenance.
- File preview and export: preview text, images, hex, and metadata; export files without altering evidence; recover deleted files when filesystem metadata permits.
- Hash analysis: compute file hashes and evidence hashes; support MD5, SHA-1, and SHA-256; match against known-good or known-bad hash sets such as NSRL-style data.
- File signature analysis: detect file type from magic bytes, compare detected type to extension, flag mismatches, and categorize files for filtering.
- Search and indexing: support filename/path search first, then metadata and full-text indexing, then advanced queries and saved filters.
- Timeline: collect filesystem timestamps and later artifact timestamps into a sortable/filterable event view.
- Bookmarks/tags: allow examiners to mark important files, add notes, and include items in reports.
- Reporting: export case summary, evidence metadata, hashes, tagged files, search hits, timeline items, and audit log.

Important later-stage functions:

- Data carving from unallocated space.
- Artifact parsing for browser history, registry, email, chat databases, thumbnails, recycle bin, link files, jump lists, event logs, and mobile backups.
- Volume Shadow Copy handling.
- Archive expansion and nested container handling.
- Encryption detection and handoff workflows.
- OCR, image classification, and AI-assisted triage only after core forensic correctness is stable.

## Processes Needed For It To Function

Evidence intake process:

1. User selects the first segment, normally `.E01`.
2. App discovers the related segment chain and validates ordering.
3. App reads image metadata: examiner, case number, acquisition notes, media size, compression, sector size, internal hashes/checksums when available.
4. App verifies the evidence stream where possible and records the result.
5. App registers the evidence source in the case database without modifying source files.

Analysis process:

1. Open the evidence stream read-only.
2. Detect partition table and volumes.
3. For each supported volume, mount/parse filesystem metadata through a forensic library rather than the operating system.
4. Build a file index: path, inode/MFT record or equivalent id, allocation state, size, timestamps, attributes, source offsets.
5. Queue long-running analysis jobs: hashing, signature identification, text extraction, thumbnail generation, search indexing.
6. Store derived results in the case database with status, errors, and provenance.

Recovery/export process:

1. Examiner selects files, directories, or carved candidates.
2. App reads bytes from evidence source through the forensic abstraction.
3. App writes to an examiner-selected export directory, never back into evidence.
4. App computes output hashes and records source path, source offset/id, export path, and time.

Reporting process:

1. Examiner bookmarks/tag items during analysis.
2. App gathers selected evidence metadata, hashes, notes, search hits, timeline entries, and export records.
3. App generates a human-readable report and a machine-readable manifest.
4. App includes warnings for unsupported sources, parse errors, incomplete jobs, or unverifiable evidence.

## Components And Development Separation

Recommended separation:

- `forensic-core`: image abstraction, read-only byte stream, EWF adapter, partition parsing, filesystem adapter interfaces, hashing, file signature detection, export/recovery logic.
- `case-store`: SQLite database schema, migrations, case metadata, evidence registry, analysis results, bookmarks, notes, audit log.
- `analysis-workers`: background jobs for hashing, signature scans, indexing, thumbnails, text extraction, and later carving/artifacts.
- `api`: local application API between UI and backend; should stream large reads/previews safely.
- `ui`: case dashboard, evidence list, filesystem tree, file table, preview pane, search, timeline, reports.
- `fixtures-tests`: tiny legal test images, generated filesystems, known hash/signature fixtures, regression tests.
- `docs`: developer notes, user guide, forensic assumptions, supported formats matrix.

Design principles:

- Treat evidence as immutable.
- Keep every derived result tied to evidence id, volume id, file id/path, and parser version.
- Prefer established forensic libraries for EWF and filesystem parsing.
- Make unsupported or partially parsed evidence visible instead of silently ignoring it.
- Design for large images: streaming reads, pagination, background work, cancellation, resumable jobs.

## Development Stages

Stage 0 - Repository and stack foundation:

- Initialize Git.
- Choose stack.
- Create app skeleton.
- Add formatting, linting, test runner, and CI-style local commands.
- Create a tiny sample fixture strategy.

Stage 1 - E01 intake spike:

- Open a segmented EWF set from `.E01`.
- Show evidence metadata.
- Verify image data where supported.
- Expose a read-only stream and basic sector/hex preview.

Stage 2 - Filesystem browser MVP:

- Detect partitions/volumes.
- Browse one supported filesystem first, preferably NTFS or FAT/exFAT depending on library support and available fixtures.
- Show directory tree, file list, metadata, and raw/hex preview.

Stage 3 - Export and recovery:

- Export selected active files.
- Preserve hashes and provenance.
- Add deleted-file listing/recovery where the filesystem library supports it.

Stage 4 - Hash and signature analysis:

- Add per-file MD5/SHA-1/SHA-256 jobs.
- Add file signature/magic-byte detection.
- Add extension mismatch flags.
- Add NSRL-style known-file import and matching.

Stage 5 - Search, filters, and timeline:

- Add path/name search and metadata filters.
- Add full-text extraction/indexing for common text/document types.
- Add timeline from filesystem timestamps.

Stage 6 - Reporting and examiner workflow:

- Add bookmarks/tags/notes.
- Add report export.
- Add audit log viewer.

Stage 7 - Advanced forensic features:

- Data carving.
- Artifact parsers.
- Archive/container expansion.
- Volume Shadow Copy support.
- Encryption detection/handoff.
- OCR and AI-assisted triage.

## Suggested Stack Direction

Good first choice: Tauri or Electron-style desktop UI with a backend that can call mature native forensic libraries.

Backend options:

- Rust: strong for desktop apps, streaming, hashing, and safety; can integrate with native libraries, but EWF/TSK bindings may require more setup.
- Python: fastest research/MVP path with `pyewf`, `pytsk3`, `python-magic`, SQLite, and worker queues, but packaging native dependencies on Windows can be painful.
- C++/Qt: strong native library fit, heavier development load.

Practical recommendation for this project:

- Start with a Python forensic-service spike to prove E01 + filesystem access.
- Wrap it behind a clean local API so the UI/backend can later be hardened or moved to Rust/C++ if needed.
- Use SQLite for case storage from the start.

## Helpful Plugins, Skills, And Tools

Codex-side skills/plugins:

- Browser control skill: useful for checking the app UI once a local dev server or desktop web UI exists.
- PDF skill: useful later for verifying generated forensic reports.
- Documents skill: useful if reports need Word-compatible exports.
- Spreadsheets skill: useful if hash lists, exports, or triage tables need `.xlsx` output.
- OpenAI docs skill: useful only if adding OpenAI-powered triage later.

Development libraries/tools to investigate:

- libewf / pyewf for `.E01/.E02/...` support.
- The Sleuth Kit / pytsk3 for volume and filesystem analysis.
- SQLite for case database.
- libmagic or pure signature table for file type detection.
- Hash libraries built into the chosen language.
- Full-text indexing: SQLite FTS5 for early MVP; Tantivy/Lucene/Solr later if needed.
- Report generation: HTML plus PDF export first.

## Immediate Risks

- Native forensic libraries can be difficult to install on Windows, especially Python bindings.
- E01 support alone is not enough; the app must bridge image reading into volume/filesystem parsing.
- Deleted-file recovery behavior varies heavily by filesystem.
- Forensic correctness depends on audit logs, immutability, provenance, and visible error states from the beginning.
- Large images will expose performance problems unless indexing and previews are streamed/paginated.

## First Agent Task Recommendation

The first coding task should not be the full UI. It should be a technical spike that proves the evidence pipeline:

1. Create the project skeleton.
2. Add a small backend module that can identify an E01 segment set.
3. Read EWF metadata through libewf/pyewf or a clearly documented fallback.
4. Expose a minimal command/API returning evidence metadata.
5. Add tests around segment discovery, unsupported-file handling, and metadata response shape.
6. Document exactly what library setup is required on Windows.
