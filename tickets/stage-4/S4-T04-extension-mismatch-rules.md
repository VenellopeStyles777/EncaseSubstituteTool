# S4-T04 - Extension Mismatch Rules

Status: Done

Stage: Stage 4 - Hash and signature foundations

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Flag extension/signature mismatches only when both file metadata and reviewed S4-T03 signature information are available.

This ticket consumes `SignatureAnalysisResult` output and Stage 2-style file metadata. It must not read bytes, call providers, infer signatures, or re-run signature detection as part of mismatch evaluation.

## Context To Read First

- `prompts/vscode-agent/2026-07-14-stage-4-familiarization.md`
- `tickets/stage-4/README.md`
- `tickets/stage-4/S4-T00-review-agent-risk-audit.md`
- `tickets/stage-4/S4-T01-hash-signature-contracts.md`
- `tickets/stage-4/S4-T02-provider-backed-hashing.md`
- `tickets/stage-4/S4-T03-file-signature-detection.md`
- `tickets/stage-4/S4-T04-extension-mismatch-rules.md`
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
- `app/tests/test_content_analysis_signatures.py`

## Target Files/Folders

Likely files to create or modify:

- `app/backend/forensic_core/content_analysis.py`
- `app/backend/forensic_core/__init__.py`
- `app/tests/test_content_analysis_extension_mismatch.py`
- `app/tests/test_content_analysis_contracts.py` if small contract coverage changes are needed
- `app/backend/forensic_core/README.md`
- `app/backend/api/README.md` if boundary notes need clarification
- `app/fixtures/README.md` if fixture/provider guidance needs clarification
- `functionality.md`
- `plan.md`
- `progression.md`
- `review.md`
- `tickets/stage-4/README.md`
- `tickets/stage-4/S4-T04-extension-mismatch-rules.md`

Do not modify Stage 2 preview behavior, Stage 3 export behavior, S4-T02 hash behavior, S4-T03 signature detection behavior, filesystem parsing, or case-store schema in this ticket unless a small import/export list update is needed.

## Required Work

- Define extension mismatch result/status structures if they do not already exist. Prefer names that fit the existing module, such as:
  - `ExtensionMismatchResult`;
  - `ExtensionExpectation` or `SignatureExtensionRule`;
  - `SUPPORTED_SIGNATURE_EXTENSIONS` or `SIGNATURE_EXTENSION_RULES`;
  - `check_extension_mismatch()` or `evaluate_extension_mismatch()`;
  - `extension_mismatch_result_to_json()`.
- Accept a reviewed `SignatureAnalysisResult` as the primary input. A helper may also accept a Stage 2-style file entry plus a signature result if that keeps call sites ergonomic.
- Do not accept an analysis provider in the mismatch evaluator. Do not call `detect_file_signature()` from the evaluator.
- Normalize the observed extension from `signature_result.source.file_name` first, falling back to `signature_result.source.file_path` if needed. Use a dot-prefixed lowercase extension such as `.pdf`. Rightmost suffix handling is enough for S4-T04.
- Evaluate only when:
  - the source is a file entry;
  - the signature result status is `ok`;
  - `detected_type` is present;
  - the detected type has an explicit extension rule;
  - the file metadata includes an extension.
- Return structured non-match states rather than false mismatch flags when required inputs are missing:
  - non-file source;
  - missing file name/path metadata;
  - no extension;
  - signature status is not `ok`;
  - detected type is unknown or unsupported for mismatch rules.
- Preserve source provenance, signature status, detected type/signature/MIME fields, content-source identity, timestamps, provider/source warnings, and any new mismatch warnings.
- Include an explicit `mismatch` field with values `True`, `False`, or `None`. Do not make callers infer mismatch solely from `AnalysisStatus.ok`.
- Keep result output JSON-friendly and compatible with S4-T01/S4-T03 contracts.

## Conservative Extension Rules

Start with a small deterministic mapping. Keep it dependency-free and document the choices in code/tests:

- `pdf`: `.pdf`
- `png`: `.png`
- `jpeg`: `.jpg`, `.jpeg`, `.jpe`
- `gif`: `.gif`
- `zip`: `.zip`, `.jar`, `.docx`, `.xlsx`, `.pptx`, `.odt`, `.ods`, `.odp`, `.apk`
- `elf`: `.elf`, `.so`, `.bin`, `.run`
- `mz_executable_candidate`: `.exe`, `.dll`, `.sys`, `.scr`, `.com`, `.ocx`, `.cpl`, `.drv`

Files with no extension should return an unknown/not-evaluated style state, not a mismatch. ZIP-based office/archive containers should not be flagged when their extension is in the documented allow-list.

## Suggested Status And Warning Names

Use existing S4-T01/S4-T03 names where possible. Suggested new status codes:

- `extension_not_checked`
- `extension_match`
- `extension_mismatch`
- `extension_missing`
- `file_name_unavailable`
- `signature_not_available`
- `unsupported_signature_type`
- `path_not_file`

Suggested warning codes:

- `extension_mismatch`
- `extension_missing`
- `signature_not_available`
- `unsupported_signature_type`

## Acceptance Criteria

- Extension mismatch evaluation consumes existing signature results and metadata only.
- No provider bytes are read and no signature detection is run by the mismatch evaluator.
- Matching extension/signature pairs return a structured non-mismatch result.
- Mismatched extension/signature pairs return a structured mismatch result with observed extension and expected extensions.
- Case-insensitive extensions are handled correctly.
- Missing extension/name/path metadata returns a structured unknown/not-evaluated result, not a mismatch.
- Unknown, insufficient, failed, or otherwise non-ok signature results return structured not-evaluated results, not mismatches.
- Unsupported detected signature types return structured not-evaluated results, not mismatches.
- Directory/non-file sources return structured non-ok/not-evaluated results.
- S4-T03 provenance, content-source identity, detected fields, source labels, and warnings are preserved.
- Default tests pass without real evidence, native dependencies, network access, MIME database packages, or large fixtures.

## Test Expectations

Add focused tests under `app/tests/`.

Tests should cover:

- `.PDF` with `pdf` detected type as a case-insensitive match;
- `.txt` with `pdf` detected type as a mismatch;
- `.jpg`, `.jpeg`, and `.jpe` with `jpeg` as matches;
- a ZIP-based allow-listed extension such as `.docx` as a match;
- an MZ executable candidate with `.exe` as a match and `.jpg` as a mismatch;
- a file without an extension as not evaluated, not mismatched;
- missing file name/path metadata as not evaluated;
- unknown signature status as not evaluated;
- insufficient signature status as not evaluated;
- unsupported detected type as not evaluated;
- directory/non-file source as not evaluated;
- provenance, content-source identity, signature warnings, new mismatch warnings, and JSON serialization;
- no regression to S4-T03 signature behavior and S4-T02 hash behavior.

Run:

```powershell
python -m pytest
```

## Documentation Updates

- Update `app/backend/forensic_core/README.md` with S4-T04 behavior and limits.
- Update `app/fixtures/README.md` only if fixture/provider guidance needs clarification.
- Update `functionality.md`, `plan.md`, `progression.md`, and `review.md`.
- Update this ticket and `tickets/stage-4/README.md` to `Review` when implementation is complete.

## Review Checklist

- Mismatch logic does not run when required inputs are missing.
- The evaluator consumes a reviewed `SignatureAnalysisResult`; it does not read provider bytes or call signature detection internally.
- Unknown, insufficient, failed, unsupported, or missing signature states are not reported as mismatches.
- Files without extensions are not reported as mismatches.
- Result wording does not imply real parser evidence if provider bytes are synthetic or generated.
- Result shape preserves S4-T03 provenance, content-source identity, source labels, detected fields, and warnings.
- Existing S4-T02 hashing and S4-T03 signature detection behavior remain unchanged.
- No known-file matching, persistence, search/timeline, UI/reporting, real parser work, deleted recovery, carving, native dependency, or Stage 5 work was added.

## Implementation Handoff - 2026-07-14

- Added `SignatureExtensionRule`, `SIGNATURE_EXTENSION_RULES`, `SUPPORTED_SIGNATURE_EXTENSIONS`, `ExtensionMismatchResult`, `evaluate_extension_mismatch()`, `check_extension_mismatch()`, and `extension_mismatch_result_to_json()` in `app/backend/forensic_core/content_analysis.py`.
- Extension mismatch evaluation consumes an existing `SignatureAnalysisResult` and source file name/path metadata only. It does not accept a provider, read bytes, or call `detect_file_signature()`.
- Rules cover PDF, PNG, JPEG extension variants, GIF, ZIP/container allow-list extensions, ELF, and conservative MZ executable candidates.
- Evaluated results use explicit `mismatch=True` or `False`; missing metadata, no extension, non-file source, non-ok signature results, missing detected type, and unsupported detected types return structured not-evaluated results with `mismatch=None`.
- Results preserve S4-T03 source provenance, content-source identity, signature status, detected type/signature/MIME fields, signature timestamps, source/provider warnings, and new mismatch warnings.
- Added dependency-free tests in `app/tests/test_content_analysis_extension_mismatch.py`.
- Final verification: `python -m pytest` reported 140 passed in 4.99s.
- No S4-T02 hash behavior, S4-T03 signature detection behavior, known-file matching, persistence, search/timeline, UI/reporting, real parser work, deleted recovery, carving, native dependency, export-output behavior, or Stage 5 work was added.

## Review Result - 2026-07-14

- Approved and marked done.
- No blocking findings found.
- Reviewer confirmed extension mismatch evaluation consumes existing S4-T03 `SignatureAnalysisResult` objects and file name/path metadata only.
- Reviewer confirmed `evaluate_extension_mismatch()` and `check_extension_mismatch()` do not accept providers, read bytes, or call `detect_file_signature()` internally.
- Reviewer confirmed match/mismatch results include explicit `mismatch=False` or `True`, while missing metadata, no extension, non-file sources, unknown/insufficient/non-ok signatures, missing detected type, and unsupported detected types return not-evaluated results with `mismatch=None`.
- Reviewer confirmed source provenance, content-source identity, signature status, detected fields, signature timestamps, source/provider warnings, and mismatch warnings are preserved.
- Reviewer confirmed S4-T04 did not add known-file matching, case-store persistence, search/timeline, UI/reporting, real parser work, deleted recovery, carving, native dependencies, S4-T02/S4-T03 behavior changes, export-output behavior changes, or Stage 5 work.
- Reviewer verification: `python -m pytest` reported 140 passed in 3.14s.

## Handoff Prompt

```text
Implement ticket S4-T04: Extension Mismatch Rules.

Before editing, read:
- prompts/vscode-agent/2026-07-14-stage-4-familiarization.md
- tickets/stage-4/README.md
- tickets/stage-4/S4-T00-review-agent-risk-audit.md
- tickets/stage-4/S4-T01-hash-signature-contracts.md
- tickets/stage-4/S4-T02-provider-backed-hashing.md
- tickets/stage-4/S4-T03-file-signature-detection.md
- tickets/stage-4/S4-T04-extension-mismatch-rules.md
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
- app/tests/test_content_analysis_signatures.py

Task:
- Add extension/signature mismatch evaluation that consumes reviewed S4-T03 `SignatureAnalysisResult` objects and file metadata only.
- Do not read provider bytes, accept an analysis provider, or call `detect_file_signature()` from the mismatch evaluator.
- Define a JSON-safe result shape with source provenance, content-source identity, signature status/detected fields, observed extension, expected extensions, explicit `mismatch` value, timestamps, and warnings.
- Add conservative extension rules for PDF, PNG, JPEG, GIF, ZIP containers, ELF, and MZ executable candidates.
- Return structured not-evaluated states for missing metadata, no extension, non-file sources, non-ok signature results, unknown/insufficient signature results, and unsupported detected types.
- Add dependency-free tests for match, mismatch, no-extension, missing metadata, unknown/insufficient signatures, unsupported types, non-file entries, provenance/warnings, JSON safety, and regression coverage.
- Update requested docs and ticket status.
- Run python -m pytest and report the exact result.

Scope boundaries:
- Do not change S4-T03 signature detection behavior.
- Do not change S4-T02 hash behavior.
- Do not add known-file matching.
- Do not add case-store persistence or schema migrations.
- Do not use preview-rendered text/hex, preview providers, export providers, written export artifacts, or filesystem metadata as byte sources.
- Do not claim whole-image verification.
- Do not add search, timeline, reporting, UI, real EWF parsing, real partition parsing, real filesystem parsing, deleted recovery, carving, native dependencies, commit, or push.

Stop after S4-T04 and hand off for review.
```
