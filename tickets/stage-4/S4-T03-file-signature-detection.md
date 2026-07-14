# S4-T03 - File Signature Detection

Status: Done

Stage: Stage 4 - Hash and signature foundations

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Detect basic file signatures from a bounded prefix of bytes supplied by an explicit Stage 4 analysis content provider.

This ticket depends on reviewed S4-T01 contracts and reviewed S4-T02 provider-backed hashing. It should reuse the S4-T02 `AnalysisContentProvider` boundary and should not add a new preview, export, filesystem, or parser content path.

## Context To Read First

- `prompts/vscode-agent/2026-07-14-stage-4-familiarization.md`
- `tickets/stage-4/README.md`
- `tickets/stage-4/S4-T00-review-agent-risk-audit.md`
- `tickets/stage-4/S4-T01-hash-signature-contracts.md`
- `tickets/stage-4/S4-T02-provider-backed-hashing.md`
- `tickets/stage-4/S4-T03-file-signature-detection.md`
- `Goal.md`
- `readme.md`
- `plan.md`
- `functionality.md`
- `progression.md`
- `review.md`
- `workflow.md`
- `app/backend/README.md`
- `app/backend/api/README.md`
- `app/backend/forensic_core/README.md`
- `app/fixtures/README.md`
- `app/backend/forensic_core/content_analysis.py`
- `app/backend/forensic_core/__init__.py`
- `app/tests/test_content_analysis_contracts.py`
- `app/tests/test_content_analysis_hashing.py`
- `app/tests/test_file_preview.py`
- `app/tests/test_file_export.py`

## Target Files/Folders

Likely files to create or modify:

- `app/backend/forensic_core/content_analysis.py`
- `app/backend/forensic_core/__init__.py`
- `app/tests/test_content_analysis_signatures.py`
- `app/tests/test_content_analysis_contracts.py` if small contract coverage changes are needed
- `app/backend/forensic_core/README.md`
- `app/backend/api/README.md` if API boundary notes need clarification
- `app/fixtures/README.md`
- `functionality.md`
- `plan.md`
- `progression.md`
- `review.md`
- `tickets/stage-4/README.md`
- `tickets/stage-4/S4-T03-file-signature-detection.md`

Do not modify Stage 2 preview behavior, Stage 3 export behavior, S4-T02 hash behavior, filesystem parsing, or case-store schema in this ticket unless a small import/export list update is needed.

## Required Work

- Add provider-backed signature detection in or near `app/backend/forensic_core/content_analysis.py`.
- Prefer names that fit the existing module, such as:
  - `FileSignatureDefinition`;
  - `SUPPORTED_FILE_SIGNATURES`;
  - `detect_file_signature()`;
  - `analyze_file_signature()`.
- Reuse the explicit Stage 4 `AnalysisContentProvider`/`AnalysisContent` boundary from S4-T02.
- Inspect only a bounded prefix of provider bytes. Honor `SignatureAnalysisRequest.max_bytes_requested` and allow an explicit `max_bytes` or equivalent argument for direct callable use.
- Validate `max_bytes_requested` before reading provider content. Invalid or non-positive limits should return structured non-ok results and should not read provider bytes.
- Return `SignatureAnalysisResult` with source provenance, content-source identity, source kind/status, read-only assertion, timestamps, warnings, `bytes_inspected`, `detected_type`, `detected_signature`, and `detected_mime_type`.
- Add a small dependency-free signature table suitable for tests. Use conservative labels:
  - PDF: `%PDF-`
  - PNG: `\x89PNG\r\n\x1a\n`
  - JPEG: `\xff\xd8\xff`
  - GIF: `GIF87a` and `GIF89a`
  - ZIP: `PK\x03\x04`, `PK\x05\x06`, and `PK\x07\x08`
  - ELF: `\x7fELF`
  - MZ executable candidate: `MZ`; do not claim a fully validated PE unless the implementation actually checks the PE header within the bounded bytes.
- Keep detection conservative. Unknown bytes should return a structured unknown status, not a guessed type.
- Return structured non-ok results for:
  - invalid signature requests;
  - directory/non-file entries;
  - metadata-only sources without provider bytes;
  - provider content unavailable;
  - provider exceptions;
  - insufficient bytes for any supported signature decision;
  - unknown signature after enough bytes are inspected.
- Keep result output JSON-friendly and compatible with S4-T01 contracts.

## Suggested Status And Warning Names

Use existing S4-T01/S4-T02 names where possible:

- `ok`
- `signature_not_checked`
- `invalid_analysis_request`
- `path_not_file`
- `metadata_only_source`
- `content_source_unavailable`
- `content_provider_error`
- `synthetic_content`
- `generated_fixture_content`

Add only if useful:

- `unknown_signature`
- `insufficient_signature_bytes`

## Acceptance Criteria

- Signature detection reads only explicit Stage 4 analysis provider bytes.
- Detection inspects no more than the requested bounded prefix.
- Known signatures return structured successful results with conservative detected type, signature label, MIME type where appropriate, byte count inspected, source provenance, and content-source identity.
- Unknown content returns a structured unknown result without guessing.
- Too-few bytes return a structured insufficient-bytes result.
- Invalid max-byte requests return structured non-ok results and do not cause provider reads.
- Directory/non-file entries are not inspected and do not cause provider reads.
- Metadata-only entries are not treated as byte-bearing.
- Missing provider content returns structured non-ok status without detection fields.
- Provider exceptions return structured non-ok status without raw tracebacks.
- Synthetic/generated provider bytes are labeled honestly.
- No preview-rendered text/hex, preview providers, export providers, written export artifacts, or filesystem metadata are used as source analysis bytes.
- Default tests pass without real evidence, native dependencies, network access, MIME database packages, or large fixtures.

## Test Expectations

Add focused tests under `app/tests/`.

Tests should cover:

- PDF, PNG, JPEG, GIF, ZIP, ELF, and MZ executable-candidate detections;
- unknown signature behavior;
- insufficient bytes behavior;
- bounded inspection behavior;
- invalid max-byte request behavior before provider read;
- missing provider content;
- directory/non-file entry behavior before provider read;
- metadata-only behavior with no provider;
- provider exception behavior;
- provenance and content-source identity preservation;
- synthetic/generated content warnings and labels;
- JSON serialization of successful and failed results;
- no regression to S4-T02 hash behavior.

Run:

```powershell
python -m pytest
```

## Documentation Updates

- Update `app/backend/forensic_core/README.md` with S4-T03 behavior and limits.
- Update `app/fixtures/README.md` with signature-test fixture/provider guidance if needed.
- Update `functionality.md`, `plan.md`, `progression.md`, and `review.md`.
- Update this ticket and `tickets/stage-4/README.md` to `Review` when implementation is complete.

## Review Checklist

- Signature detection uses explicit Stage 4 analysis provider bytes only.
- Bounded prefix behavior is clear and tested.
- Detection is conservative and structured when unknown or insufficient.
- Preview output, preview providers, export output, export providers, and metadata-only filesystem entries are not treated as signature source content.
- Result shape remains compatible with S4-T01 contracts.
- Existing S4-T02 hashing behavior remains unchanged.
- No extension mismatch, known-file matching, persistence, search/timeline, UI/reporting, real parser work, deleted recovery, carving, native dependency, or Stage 5 work was added.
- Default tests remain dependency-free.

## Implementation Handoff - 2026-07-14

- Added `FileSignatureDefinition`, `SUPPORTED_FILE_SIGNATURES`, `detect_file_signature()`, and `analyze_file_signature()` in `app/backend/forensic_core/content_analysis.py`.
- Signature detection reuses the S4-T02 `AnalysisContentProvider` / `AnalysisContent` boundary and inspects only `content.data[:max_bytes]`.
- Detection supports dependency-free magic bytes for PDF, PNG, JPEG, GIF87a/GIF89a, ZIP header variants, ELF, and conservative MZ executable candidates.
- Invalid or non-positive max-byte requests are rejected before provider reads.
- Directory/non-file entries, metadata-only sources, unavailable provider content, provider exceptions, insufficient partial known signatures, and unknown signatures return structured non-ok `SignatureAnalysisResult` objects.
- Successful and failed results preserve S4-T01 source provenance, provider identity, source kind/status, max bytes requested, byte count inspected when applicable, read-only assertion, timestamps, and warnings.
- Synthetic/generated provider bytes are labeled through content-source identity and warnings.
- Added dependency-free tests in `app/tests/test_content_analysis_signatures.py`.
- Final verification: `python -m pytest` reported 127 passed in 4.41s.
- No extension mismatch checks, known-file matching, persistence, search/timeline, UI/reporting, real parser work, deleted recovery, carving, native dependencies, S4-T02 hash behavior changes, export-output behavior changes, or Stage 5 work were added.

## Review Result - 2026-07-14

- Approved and marked done.
- No blocking findings found.
- Reviewer confirmed signature detection uses explicit Stage 4 analysis-provider bytes, not preview/export providers, written export artifacts, or filesystem metadata.
- Reviewer confirmed invalid max-byte requests and directory/non-file entries are rejected before provider reads.
- Reviewer confirmed known signatures are conservative, unknown and insufficient-prefix results are structured, and MZ is labeled as an executable candidate rather than a validated PE.
- Reviewer confirmed S4-T03 did not add extension mismatch checks, known-file matching, persistence, search/timeline, UI/reporting, parser work, deleted recovery, carving, native dependencies, S4-T02 hash behavior changes, export-output behavior changes, or Stage 5 work.
- Reviewer verification: `python -m pytest` reported 127 passed in 5.39s.

## Handoff Prompt

```text
Implement ticket S4-T03: File Signature Detection.

Before editing, read:
- prompts/vscode-agent/2026-07-14-stage-4-familiarization.md
- tickets/stage-4/README.md
- tickets/stage-4/S4-T00-review-agent-risk-audit.md
- tickets/stage-4/S4-T01-hash-signature-contracts.md
- tickets/stage-4/S4-T02-provider-backed-hashing.md
- tickets/stage-4/S4-T03-file-signature-detection.md
- Goal.md
- readme.md
- plan.md
- functionality.md
- progression.md
- review.md
- workflow.md
- app/backend/README.md
- app/backend/api/README.md
- app/backend/forensic_core/README.md
- app/fixtures/README.md
- app/backend/forensic_core/content_analysis.py
- app/backend/forensic_core/__init__.py
- app/tests/test_content_analysis_contracts.py
- app/tests/test_content_analysis_hashing.py
- app/tests/test_file_preview.py
- app/tests/test_file_export.py

Task:
- Add provider-backed file signature detection using explicit Stage 4 analysis content providers only.
- Reuse the S4-T02 `AnalysisContentProvider` boundary.
- Inspect only a bounded prefix of provider bytes.
- Detect a small dependency-free set of magic bytes: PDF, PNG, JPEG, GIF, ZIP, ELF, and conservative MZ executable candidate.
- Preserve S4-T01 provenance and content-source identity in every result.
- Add dependency-free tests for known, unknown, insufficient, invalid, failure, provenance, and source-labeling behavior.
- Update requested docs and ticket status.
- Run python -m pytest and report the exact result.

Scope boundaries:
- Do not add extension mismatch checks.
- Do not add known-file matching.
- Do not add case-store persistence or schema migrations.
- Do not use preview-rendered text/hex or preview providers as analysis content.
- Do not use Stage 3 exported artifacts or export providers as implicit analysis content.
- Do not change S4-T02 hash behavior or Stage 3 export-output SHA-256 verification.
- Do not claim whole-image verification.
- Do not add search, timeline, reporting, UI, real EWF parsing, real partition parsing, real filesystem parsing, deleted recovery, carving, native dependencies, commit, or push.

Stop after S4-T03 and hand off for review.
```
