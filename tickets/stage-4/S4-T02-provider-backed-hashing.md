# S4-T02 - Provider-Backed Hashing

Status: Draft

Stage: Stage 4 - Hash and signature foundations

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Compute per-file hashes only from explicit analysis content providers.

This ticket depends on reviewed S4-T01 contracts. It must keep analysis hashing separate from Stage 3 export-output verification and future whole-image verification.

## Expected Scope

- Add an explicit analysis content provider protocol or equivalent boundary.
- Add a dependency-free provider for tests that labels content as synthetic or generated fixture content.
- Compute SHA-256 by default.
- Add MD5 and SHA-1 only as optional forensic comparison hashes, not as stronger integrity signals than SHA-256.
- Preserve provider identity, source kind, source status, byte count, read-only status, timestamp, and warnings in every result.
- Return structured non-ok results for missing provider content, directory entries, unsupported algorithms, invalid requests, or provider read errors.

## Out Of Scope

- File signature detection.
- Extension mismatch.
- Known-file matching.
- Case-store persistence.
- Export-output hash verification changes.
- Whole-image verification.
- Preview-rendered bytes.
- Real EWF, partition, filesystem, deleted recovery, carving, search, timeline, UI, or native dependencies.

## Test Expectations

Tests should prove:

- SHA-256 is computed from provider bytes.
- Optional MD5/SHA-1 are computed only when requested.
- Unsupported algorithms return structured status/warnings.
- Missing content returns `content_source_unavailable` or the reviewed S4-T01 equivalent.
- Directory/metadata-only entries are not hashed.
- Results preserve provenance and content-source identity.
- Synthetic/generated content is labeled honestly.

Run `python -m pytest`.

## Review Checklist

- Hashes come from explicit provider bytes only.
- Preview output and exported artifacts are not silently reused as analysis source content.
- Result shape remains compatible with S4-T01 contracts.
- Default tests remain dependency-free.
