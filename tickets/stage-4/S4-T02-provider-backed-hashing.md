# S4-T02 - Provider-Backed Hashing

Status: Done

Stage: Stage 4 - Hash and signature foundations

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Compute per-file hashes only from explicit Stage 4 analysis content providers.

This ticket depends on reviewed S4-T01 contracts. It must keep analysis hashing separate from Stage 3 export-output verification, separate from Stage 2 preview rendering, and separate from future whole-image verification.

## Context To Read First

- `prompts/vscode-agent/2026-07-14-stage-4-familiarization.md`
- `tickets/stage-4/README.md`
- `tickets/stage-4/S4-T00-review-agent-risk-audit.md`
- `tickets/stage-4/S4-T01-hash-signature-contracts.md`
- `tickets/stage-4/S4-T02-provider-backed-hashing.md`
- `Goal.md`
- `readme.md`
- `plan.md`
- `functionality.md`
- `progression.md`
- `review.md`
- `workflow.md`
- `app/backend/forensic_core/content_analysis.py`
- `app/backend/api/file_preview.py`
- `app/backend/api/file_export.py`
- `app/tests/test_content_analysis_contracts.py`
- `app/tests/test_file_preview.py`
- `app/tests/test_file_export.py`
- `app/fixtures/README.md`

## Target Files/Folders

Likely files to create or modify:

- `app/backend/forensic_core/content_analysis.py`
- `app/backend/forensic_core/__init__.py`
- `app/tests/test_content_analysis_hashing.py`
- `app/tests/test_content_analysis_contracts.py` if small contract coverage changes are needed
- `app/backend/forensic_core/README.md`
- `app/backend/api/README.md` if API boundary notes need clarification
- `app/fixtures/README.md`
- `functionality.md`
- `plan.md`
- `progression.md`
- `review.md`
- `tickets/stage-4/README.md`
- `tickets/stage-4/S4-T02-provider-backed-hashing.md`

Do not modify Stage 2 preview behavior, Stage 3 export behavior, filesystem parsing, or case-store schema in this ticket unless a small import/export list update is needed.

## Required Work

- Add an explicit Stage 4 analysis content provider boundary. Prefer names that fit `content_analysis.py`, such as:
  - `AnalysisContent`;
  - `AnalysisContentProvider`;
  - `StubAnalysisContentProvider`;
  - `hash_file_content()` or `calculate_hashes()`.
- Keep this provider separate from `StubPreviewProvider` and `StubExportContentProvider`. S4-T02 may use the same tiny `Hello, world!` bytes for tests, but it must expose them through a Stage 4 analysis provider with its own identity and warnings.
- The provider should return raw bytes plus source identity fields that can populate `AnalysisContentSourceIdentity`.
- Compute SHA-256 by default from provider bytes.
- Support optional MD5 and SHA-1 when explicitly requested. Frame them as forensic comparison hashes, not stronger integrity indicators than SHA-256.
- Normalize algorithm names predictably, such as case-insensitive `sha256`, `md5`, and `sha1`.
- Validate requested algorithms before reading provider content. Unsupported algorithms should return structured non-ok results and should not read provider bytes.
- Preserve source provenance, provider identity, source kind, source status, byte count, read-only assertion, timestamp, and warnings in the returned `HashAnalysisResult`.
- Return structured non-ok results for:
  - unsupported algorithms;
  - empty or invalid algorithm requests;
  - directory/non-file entries;
  - metadata-only sources without provider bytes;
  - provider content unavailable;
  - provider exceptions.
- Keep hash result output JSON-friendly and compatible with S4-T01 contracts.

## Suggested Status And Warning Names

Use existing S4-T01 names where possible:

- `ok`
- `content_source_unavailable`
- `metadata_only_source`
- `invalid_analysis_request`
- `unsupported_algorithm`
- `hash_not_computed`
- `synthetic_content`
- `generated_fixture_content`

Add only if useful:

- `content_provider_error`
- `path_not_file`

## Acceptance Criteria

- SHA-256 is computed from explicit analysis provider bytes.
- MD5 and SHA-1 are computed only when requested.
- Unsupported algorithm requests are structured non-ok results and do not cause provider reads.
- Directory/non-file entries are not hashed.
- Metadata-only entries are not treated as byte-bearing.
- Missing provider content returns structured non-ok status without hashes.
- Provider exceptions return structured non-ok status without raw tracebacks.
- Results preserve source provenance and analysis content-source identity.
- Synthetic/generated provider bytes are labeled honestly.
- No preview-rendered text/hex or Stage 3 export-output artifacts are used as source analysis bytes.
- Default tests pass without real evidence, native dependencies, network access, or large fixtures.

## Test Expectations

Add focused tests under `app/tests/`.

Tests should cover:

- default SHA-256 computed from explicit provider bytes;
- optional MD5 and SHA-1 computed only when requested;
- algorithm normalization;
- unsupported algorithm behavior before provider read;
- empty/invalid algorithm request behavior;
- missing provider content;
- directory/non-file entry behavior;
- provider exception behavior;
- provenance and content-source identity preservation;
- synthetic/generated content warnings and labels;
- JSON serialization of successful and failed results.

Run:

```powershell
python -m pytest
```

## Documentation Updates

- Update `app/backend/forensic_core/README.md` with S4-T02 behavior and limits.
- Update `app/fixtures/README.md` with analysis-provider fixture guidance if needed.
- Update `functionality.md`, `plan.md`, `progression.md`, and `review.md`.
- Update this ticket and `tickets/stage-4/README.md` to `Review` when implementation is complete.

## Review Checklist

- Hashes come from explicit Stage 4 analysis provider bytes only.
- Preview output, preview providers, export output, and export providers are not silently reused as analysis source content.
- Result shape remains compatible with S4-T01 contracts.
- SHA-256 is present by default; MD5/SHA-1 are optional and clearly framed.
- No file signature detection, extension mismatch, known-file matching, persistence, search/timeline, UI, real parser work, deleted recovery, carving, or native dependency work was added.
- Default tests remain dependency-free.

## Implementation Handoff - 2026-07-14

- Added `AnalysisContent`, `AnalysisContentProvider`, `StubAnalysisContentProvider`, `hash_file_content()`, and `calculate_hashes()` in `app/backend/forensic_core/content_analysis.py`.
- Hashing now computes SHA-256 by default from explicit Stage 4 analysis-provider bytes. MD5 and SHA-1 are computed only when explicitly requested.
- Algorithm names are normalized case-insensitively, including hyphen/underscore variants for SHA names.
- Unsupported, empty, malformed, directory/non-file, metadata-only, missing-content, and provider-exception paths return structured non-ok `HashAnalysisResult` objects without treating filesystem metadata as bytes.
- Unsupported and invalid algorithm requests are validated before provider reads.
- Successful and failed results preserve S4-T01 source provenance, content-source identity, source kind, read-only assertion, source status, byte count when available, timestamps, and warnings.
- Added dependency-free tests in `app/tests/test_content_analysis_hashing.py`.
- No file signature detection, extension mismatch checks, known-file matching, persistence, search/timeline, UI, parser work, deleted recovery, carving, native dependencies, export-output behavior changes, or Stage 5 work were added.
- Final test run: `python -m pytest` reported 116 passed in 3.38s.

## Review Result - 2026-07-14

- Approved and marked done.
- No blocking findings found.
- Reviewer confirmed hashes come from explicit Stage 4 analysis-provider bytes, not preview/export providers, written export artifacts, or filesystem metadata.
- Reviewer confirmed unsupported and malformed algorithm requests are rejected before provider reads.
- Reviewer confirmed non-file, metadata-only, unavailable-content, and provider-exception paths return structured non-ok results without broadening scope.
- Reviewer confirmed S4-T02 did not add signature detection, extension mismatch checks, known-file matching, persistence, search/timeline, UI, parser work, deleted recovery, carving, native dependencies, export-output behavior changes, or Stage 5 work.
- Reviewer verification: `python -m pytest` reported 116 passed in 4.21s.

## Handoff Prompt

```text
Implement ticket S4-T02: Provider-Backed Hashing.

Before editing, read:
- prompts/vscode-agent/2026-07-14-stage-4-familiarization.md
- tickets/stage-4/README.md
- tickets/stage-4/S4-T00-review-agent-risk-audit.md
- tickets/stage-4/S4-T01-hash-signature-contracts.md
- tickets/stage-4/S4-T02-provider-backed-hashing.md
- Goal.md
- readme.md
- plan.md
- functionality.md
- progression.md
- review.md
- workflow.md
- app/backend/forensic_core/content_analysis.py
- app/backend/api/file_preview.py
- app/backend/api/file_export.py
- app/tests/test_content_analysis_contracts.py
- app/tests/test_file_preview.py
- app/tests/test_file_export.py
- app/fixtures/README.md

Task:
- Add provider-backed per-file hash calculation using explicit Stage 4 analysis content providers only.
- Compute SHA-256 by default.
- Support MD5 and SHA-1 only when requested.
- Preserve S4-T01 provenance and content-source identity in every result.
- Add dependency-free tests for success, failure, provenance, and source-labeling behavior.
- Update requested docs and ticket status.
- Run python -m pytest and report the exact result.

Scope boundaries:
- Do not detect file signatures.
- Do not add extension mismatch checks.
- Do not add known-file matching.
- Do not add case-store persistence or schema migrations.
- Do not use preview-rendered text/hex or preview providers as analysis content.
- Do not use Stage 3 exported artifacts or export providers as implicit analysis content.
- Do not change Stage 3 export-output SHA-256 verification.
- Do not claim whole-image verification.
- Do not add search, timeline, reporting, UI, real EWF parsing, real partition parsing, real filesystem parsing, deleted recovery, carving, native dependencies, commit, or push.

Stop after S4-T02 and hand off for review.
```
