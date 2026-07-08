# Development Stages

Purpose: define the roadmap and make Stage 1 specific enough for another Codex agent to start safely.

Stage 0 - Repository and planning foundation:

- Initialize Git.
- Create planning documents.
- Add app skeleton folders.
- Choose an initial stack direction.
- Define agent workflow and review process.

Stage 1 - E01 intake spike:

- Build the first backend package/module under `app/backend/forensic_core`.
- Implement segment discovery for `.E01`, `.E02`, `.E03`, ... evidence sets.
- Define a reader adapter interface for EWF metadata and verification.
- Add a real adapter target for libewf/pyewf if available.
- Add a stub/mock adapter so tests run without native forensic dependencies.
- Return structured metadata and warning objects.
- Add a command/API entry point that accepts an `.E01` path and prints or returns JSON metadata.
- Create or sketch SQLite tables for cases, evidence sources, and audit events.
- Add tests for segment discovery, unsupported extensions, missing segment reporting, adapter-unavailable behavior, and metadata response shape.
- Document Windows dependency requirements and known blockers.

Stage 1 completion criteria:

- A developer can run one documented command from the repository and receive a structured response for a mock or real `.E01` input.
- Tests do not require a large real evidence file.
- Evidence paths are opened read-only or mocked.
- Missing dependencies produce clear messages.
- `plan.md`, `progression.md`, and `review.md` explain what is ready for review.

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
