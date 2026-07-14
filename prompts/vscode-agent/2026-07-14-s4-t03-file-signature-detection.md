# 2026-07-14 - S4-T03 File Signature Detection Prompt

Use this prompt to hand S4-T03 to the Stage 4 VS Code implementation agent.

```text
Implement ticket S4-T03: File Signature Detection.

Before editing, read these files:
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

Context:
- S4-T01 is reviewed and done. It added hash/signature analysis contracts and provenance/content-source identity structures.
- S4-T02 is reviewed and done. It added `AnalysisContent`, `AnalysisContentProvider`, `StubAnalysisContentProvider`, `hash_file_content()`, and `calculate_hashes()`.
- Stage 3 export SHA-256 verifies written export artifacts only. It is not per-file analysis hashing or signature detection.
- Preview bytes are not analysis source content.
- Filesystem entries are metadata-only and are not byte-bearing by themselves.
- The project still has no real evidence-backed filesystem content extraction. S4-T03 must label synthetic/generated provider bytes honestly.

Before implementing:
- Summarize your understanding of the current true project state.
- List the files you expect to create or modify.
- State what bytes this ticket will inspect and why those bytes are legitimate for S4-T03.
- If you see a conflict between this prompt and the ticket, pause and explain it instead of broadening scope.

Your task:
- Add provider-backed file signature detection using explicit Stage 4 analysis content providers only.
- Reuse the S4-T02 `AnalysisContentProvider` / `AnalysisContent` boundary.
- Add signature detection in or near `app/backend/forensic_core/content_analysis.py`. Prefer names that fit the existing module, such as:
  - `FileSignatureDefinition`;
  - `SUPPORTED_FILE_SIGNATURES`;
  - `detect_file_signature()`;
  - `analyze_file_signature()`.
- Inspect only a bounded prefix of provider bytes. Honor `SignatureAnalysisRequest.max_bytes_requested` and allow an explicit `max_bytes` or equivalent argument for direct callable use.
- Validate `max_bytes_requested` before reading provider content. Invalid or non-positive limits must return structured non-ok results and must not read provider bytes.
- Preserve S4-T01 source provenance, provider identity, source kind, source status, byte count inspected, max bytes requested, read-only assertion, timestamp, and warnings in `SignatureAnalysisResult`.
- Detect a small dependency-free set of magic bytes:
  - PDF: `%PDF-`
  - PNG: `\x89PNG\r\n\x1a\n`
  - JPEG: `\xff\xd8\xff`
  - GIF: `GIF87a` and `GIF89a`
  - ZIP: `PK\x03\x04`, `PK\x05\x06`, and `PK\x07\x08`
  - ELF: `\x7fELF`
  - MZ executable candidate: `MZ`; do not claim a fully validated PE unless you actually check the PE header within the bounded bytes.
- Keep detection conservative. Unknown bytes should return structured unknown status, not guessed type.
- Return structured non-ok results for invalid requests, directory/non-file entries, metadata-only sources without provider bytes, unavailable provider content, provider exceptions, insufficient bytes, and unknown signatures.
- Add dependency-free tests for known, unknown, insufficient, invalid, failure, provenance, and source-labeling behavior.
- Update requested docs and ticket status.
- Run `python -m pytest` and report the exact result.

Suggested status and warning names:
- `ok`
- `signature_not_checked`
- `invalid_analysis_request`
- `path_not_file`
- `metadata_only_source`
- `content_source_unavailable`
- `content_provider_error`
- `unknown_signature`
- `insufficient_signature_bytes`
- `synthetic_content`
- `generated_fixture_content`

Likely files to create or modify:
- app/backend/forensic_core/content_analysis.py
- app/backend/forensic_core/__init__.py
- app/tests/test_content_analysis_signatures.py
- app/tests/test_content_analysis_contracts.py if small contract coverage changes are needed
- app/backend/forensic_core/README.md
- app/backend/api/README.md if API boundary notes need clarification
- app/fixtures/README.md
- functionality.md
- plan.md
- progression.md
- review.md
- tickets/stage-4/README.md
- tickets/stage-4/S4-T03-file-signature-detection.md

Test expectations:
- PDF, PNG, JPEG, GIF, ZIP, ELF, and MZ executable-candidate detections.
- Unknown signature behavior.
- Insufficient bytes behavior.
- Bounded inspection behavior.
- Invalid max-byte request behavior before provider read.
- Missing provider content.
- Directory/non-file entry behavior before provider read.
- Metadata-only behavior with no provider.
- Provider exception behavior.
- Provenance and content-source identity preservation.
- Synthetic/generated content warnings and labels.
- JSON serialization of successful and failed results.
- No regression to S4-T02 hash behavior.

Scope boundaries:
- Do not add extension mismatch checks.
- Do not add known-file matching.
- Do not add case-store persistence or schema migrations.
- Do not use preview-rendered text/hex or preview providers as analysis content.
- Do not use Stage 3 exported artifacts or export providers as implicit analysis content.
- Do not change S4-T02 hash behavior.
- Do not change Stage 3 export-output SHA-256 verification.
- Do not claim whole-image verification.
- Do not add search, timeline, reporting, UI, real EWF parsing, real partition parsing, real filesystem parsing, deleted recovery, carving, native dependencies, commit, or push.

Final handoff:
- Summarize files changed.
- Summarize signature detection behavior added.
- Report the exact pytest command and result.
- State limitations and deferred work.
- Confirm you did not begin S4-T04 or any later Stage 4/Stage 5 work.

Stop after S4-T03 and hand off for review.
```
