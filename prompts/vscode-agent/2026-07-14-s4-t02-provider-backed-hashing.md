# 2026-07-14 - S4-T02 Provider-Backed Hashing Prompt

Use this prompt to hand S4-T02 to the Stage 4 VS Code implementation agent.

```text
Implement ticket S4-T02: Provider-Backed Hashing.

Before editing, read these files:
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
- app/backend/README.md
- app/backend/api/README.md
- app/backend/forensic_core/README.md
- app/fixtures/README.md
- app/backend/forensic_core/content_analysis.py
- app/backend/api/file_preview.py
- app/backend/api/file_export.py
- app/tests/test_content_analysis_contracts.py
- app/tests/test_file_preview.py
- app/tests/test_file_export.py

Context:
- S4-T01 is reviewed and done. It added contract-only hash/signature analysis request/result/provenance/content-source structures.
- Stage 3 export SHA-256 verifies written export artifacts only. It is not per-file analysis hashing.
- Preview bytes are not analysis source content.
- Filesystem entries are metadata-only and are not byte-bearing by themselves.
- The project still has no real evidence-backed filesystem content extraction. S4-T02 must label synthetic/generated provider bytes honestly.

Before implementing:
- Summarize your understanding of the current true project state.
- List the files you expect to create or modify.
- State what bytes this ticket will analyze and why those bytes are legitimate for S4-T02.
- If you see a conflict between this prompt and the ticket, pause and explain it instead of broadening scope.

Your task:
- Add provider-backed per-file hash calculation using explicit Stage 4 analysis content providers only.
- Add an analysis content provider boundary in or near `app/backend/forensic_core/content_analysis.py`. Prefer names that fit the existing module, such as:
  - `AnalysisContent`;
  - `AnalysisContentProvider`;
  - `StubAnalysisContentProvider`;
  - `hash_file_content()` or `calculate_hashes()`.
- Keep the Stage 4 analysis provider separate from `StubPreviewProvider` and `StubExportContentProvider`.
- The provider should return raw bytes plus enough source identity fields to populate `AnalysisContentSourceIdentity`.
- Compute SHA-256 by default.
- Support MD5 and SHA-1 only when explicitly requested. Treat them as forensic comparison hashes, not stronger integrity signals than SHA-256.
- Normalize algorithm names predictably, such as case-insensitive `sha256`, `md5`, and `sha1`.
- Validate requested algorithms before reading provider content. Unsupported algorithms must return structured non-ok results and must not read provider bytes.
- Preserve S4-T01 source provenance, provider identity, source kind, source status, byte count, read-only assertion, timestamp, and warnings in `HashAnalysisResult`.
- Return structured non-ok results for unsupported algorithms, empty/invalid algorithm requests, directory/non-file entries, metadata-only sources without provider bytes, unavailable provider content, and provider exceptions.
- Add dependency-free tests for success, failure, provenance, and source-labeling behavior.
- Update requested docs and ticket status.
- Run `python -m pytest` and report the exact result.

Suggested status and warning names:
- `ok`
- `content_source_unavailable`
- `metadata_only_source`
- `invalid_analysis_request`
- `unsupported_algorithm`
- `hash_not_computed`
- `synthetic_content`
- `generated_fixture_content`
- `content_provider_error`
- `path_not_file`

Likely files to create or modify:
- app/backend/forensic_core/content_analysis.py
- app/backend/forensic_core/__init__.py
- app/tests/test_content_analysis_hashing.py
- app/tests/test_content_analysis_contracts.py if small contract coverage changes are needed
- app/backend/forensic_core/README.md
- app/backend/api/README.md if API boundary notes need clarification
- app/fixtures/README.md
- functionality.md
- plan.md
- progression.md
- review.md
- tickets/stage-4/README.md
- tickets/stage-4/S4-T02-provider-backed-hashing.md

Test expectations:
- Default SHA-256 computed from explicit provider bytes.
- Optional MD5 and SHA-1 computed only when requested.
- Algorithm normalization.
- Unsupported algorithm behavior before provider read.
- Empty/invalid algorithm request behavior.
- Missing provider content.
- Directory/non-file entry behavior.
- Provider exception behavior.
- Provenance and content-source identity preservation.
- Synthetic/generated content warnings and labels.
- JSON serialization of successful and failed results.

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

Final handoff:
- Summarize files changed.
- Summarize provider and hashing behavior added.
- Report the exact pytest command and result.
- State limitations and deferred work.
- Confirm you did not begin S4-T03 or any later Stage 4/Stage 5 work.

Stop after S4-T02 and hand off for review.
```
