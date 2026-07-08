# EnCase-Style Functionality

Purpose: describe the functionality this app should eventually provide, with the MVP kept realistic.

Source notes:

- OpenText Forensic, formerly EnCase Forensic, is positioned for collecting, triaging, analyzing, and reporting on digital evidence while maintaining evidential integrity. Source: https://www.opentext.com/products/encase-forensic
- OpenText lists capabilities such as evidence acquisition, triage, AI-assisted review, reporting, artifact workflows, broad device/filesystem support, encrypted filesystem acquisition, automation, indexing, timeline view, Volume Shadow Copy analysis, E01/L01 formats, hashing, action logging, deleted-file recovery, unallocated-space analysis, artifact parsing, and chain of custody. Source: https://www.opentext.com/products/encase-forensic

Core functions for this project:

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

Later-stage functions:

- Data carving from unallocated space.
- Artifact parsing for browser history, registry, email, chat databases, thumbnails, recycle bin, link files, jump lists, event logs, and mobile backups.
- Volume Shadow Copy handling.
- Archive expansion and nested container handling.
- Encryption detection and handoff workflows.
- OCR, image classification, and AI-assisted triage only after core forensic correctness is stable.
