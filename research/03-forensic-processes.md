# Forensic Processes

Purpose: outline the actual processes the app must support so development does not become only UI screens.

Evidence intake process:

1. User selects the first segment, normally `.E01`.
2. App discovers the related segment chain and validates ordering.
3. App reads image metadata: examiner, case number, acquisition notes, media size, compression, sector size, internal hashes/checksums when available.
4. App verifies the evidence stream where possible and records the result.
5. App registers the evidence source in the case database without modifying source files.

Analysis process:

1. Open the evidence stream read-only.
2. Detect partition table and volumes.
3. For each supported volume, parse filesystem metadata through a forensic library rather than the operating system.
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
