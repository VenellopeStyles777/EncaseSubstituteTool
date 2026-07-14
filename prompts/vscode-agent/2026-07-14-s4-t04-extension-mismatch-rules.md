# 2026-07-14 - S4-T04 Extension Mismatch Rules Prompt

Use this prompt to hand S4-T04 to the Stage 4 VS Code implementation agent.

```text
Implement ticket S4-T04: Extension Mismatch Rules.

Before editing, read these files:
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

Context:
- S4-T01 is reviewed and done. It added hash/signature analysis contracts and provenance/content-source identity structures.
- S4-T02 is reviewed and done. It added provider-backed hashing over explicit Stage 4 analysis content providers.
- S4-T03 is reviewed and done. It added bounded signature detection that returns `SignatureAnalysisResult`.
- S4-T04 should consume reviewed signature results and file metadata only.
- The project still has no real evidence-backed filesystem content extraction. Extension mismatch results must preserve provider/source labels and must not imply real parser evidence when bytes are synthetic or generated.

Before implementing:
- Summarize your understanding of the current true project state.
- List the files you expect to create or modify.
- State that this ticket evaluates existing signature results and metadata only, with no byte reads.
- If you see a conflict between this prompt and the ticket, pause and explain it instead of broadening scope.

Your task:
- Add extension/signature mismatch evaluation in or near `app/backend/forensic_core/content_analysis.py`.
- Consume reviewed S4-T03 `SignatureAnalysisResult` objects and file metadata only.
- Do not accept an analysis provider in the mismatch evaluator.
- Do not call `detect_file_signature()` from the mismatch evaluator.
- Define JSON-safe result/status structures if needed. Prefer names that fit the existing module, such as:
  - `ExtensionMismatchResult`;
  - `ExtensionExpectation` or `SignatureExtensionRule`;
  - `SUPPORTED_SIGNATURE_EXTENSIONS` or `SIGNATURE_EXTENSION_RULES`;
  - `check_extension_mismatch()` or `evaluate_extension_mismatch()`;
  - `extension_mismatch_result_to_json()`.
- Normalize the observed extension from `signature_result.source.file_name` first, falling back to `signature_result.source.file_path` if needed. Use a dot-prefixed lowercase extension such as `.pdf`. Rightmost suffix handling is enough for S4-T04.
- Evaluate only when the source is a file entry, the signature result status is `ok`, `detected_type` is present, the detected type has an explicit extension rule, and file metadata includes an extension.
- Include an explicit `mismatch` field with values `True`, `False`, or `None`.
- Preserve source provenance, content-source identity, signature status, detected type/signature/MIME fields, provider/source warnings, timestamps, observed extension, expected extensions, and any new mismatch warning.
- Return structured not-evaluated states rather than false mismatch flags when required inputs are missing.

Conservative extension rules:
- `pdf`: `.pdf`
- `png`: `.png`
- `jpeg`: `.jpg`, `.jpeg`, `.jpe`
- `gif`: `.gif`
- `zip`: `.zip`, `.jar`, `.docx`, `.xlsx`, `.pptx`, `.odt`, `.ods`, `.odp`, `.apk`
- `elf`: `.elf`, `.so`, `.bin`, `.run`
- `mz_executable_candidate`: `.exe`, `.dll`, `.sys`, `.scr`, `.com`, `.ocx`, `.cpl`, `.drv`

Suggested status and warning names:
- `extension_not_checked`
- `extension_match`
- `extension_mismatch`
- `extension_missing`
- `file_name_unavailable`
- `signature_not_available`
- `unsupported_signature_type`
- `path_not_file`

Test expectations:
- `.PDF` with `pdf` detected type as a case-insensitive match.
- `.txt` with `pdf` detected type as a mismatch.
- `.jpg`, `.jpeg`, and `.jpe` with `jpeg` as matches.
- A ZIP-based allow-listed extension such as `.docx` as a match.
- An MZ executable candidate with `.exe` as a match and `.jpg` as a mismatch.
- A file without an extension as not evaluated, not mismatched.
- Missing file name/path metadata as not evaluated.
- Unknown signature status as not evaluated.
- Insufficient signature status as not evaluated.
- Unsupported detected type as not evaluated.
- Directory/non-file source as not evaluated.
- Provenance, content-source identity, signature warnings, new mismatch warnings, and JSON serialization.
- No regression to S4-T03 signature behavior and S4-T02 hash behavior.

Likely files to create or modify:
- app/backend/forensic_core/content_analysis.py
- app/backend/forensic_core/__init__.py
- app/tests/test_content_analysis_extension_mismatch.py
- app/tests/test_content_analysis_contracts.py if small contract coverage changes are needed
- app/backend/forensic_core/README.md
- app/backend/api/README.md if boundary notes need clarification
- app/fixtures/README.md if fixture/provider guidance needs clarification
- functionality.md
- plan.md
- progression.md
- review.md
- tickets/stage-4/README.md
- tickets/stage-4/S4-T04-extension-mismatch-rules.md

Scope boundaries:
- Do not change S4-T03 signature detection behavior.
- Do not change S4-T02 hash behavior.
- Do not add known-file matching.
- Do not add case-store persistence or schema migrations.
- Do not use preview-rendered text/hex, preview providers, export providers, written export artifacts, or filesystem metadata as byte sources.
- Do not claim whole-image verification.
- Do not add search, timeline, reporting, UI, real EWF parsing, real partition parsing, real filesystem parsing, deleted recovery, carving, native dependencies, commit, or push.

Documentation:
- Update `app/backend/forensic_core/README.md` with S4-T04 behavior and limits.
- Update `app/fixtures/README.md` only if fixture/provider guidance needs clarification.
- Update `functionality.md`, `plan.md`, `progression.md`, and `review.md`.
- Update `tickets/stage-4/README.md` and `tickets/stage-4/S4-T04-extension-mismatch-rules.md` to `Review` when implementation is complete.

Verification:
- Run `python -m pytest`.
- Report the exact command and result.

Final handoff:
- Summarize files changed.
- Summarize extension mismatch behavior added.
- Report the exact pytest command and result.
- State limitations and deferred work.
- Confirm you did not begin S4-T05 or any Stage 5 work.

Stop after S4-T04 and hand off for review.
```
