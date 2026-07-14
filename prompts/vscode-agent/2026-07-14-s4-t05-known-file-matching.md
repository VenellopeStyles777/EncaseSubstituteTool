# 2026-07-14 - S4-T05 Fixture-Sized Known-File Matching Prompt

Use this prompt to hand S4-T05 to the Stage 4 VS Code implementation agent.

```text
Implement ticket S4-T05: Fixture-Sized Known-File Matching.

Before editing, read these files:
- prompts/vscode-agent/2026-07-14-stage-4-familiarization.md
- tickets/stage-4/README.md
- tickets/stage-4/S4-T00-review-agent-risk-audit.md
- tickets/stage-4/S4-T01-hash-signature-contracts.md
- tickets/stage-4/S4-T02-provider-backed-hashing.md
- tickets/stage-4/S4-T03-file-signature-detection.md
- tickets/stage-4/S4-T04-extension-mismatch-rules.md
- tickets/stage-4/S4-T05-known-file-matching.md
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
- app/tests/test_content_analysis_extension_mismatch.py

Context:
- S4-T01 is reviewed and done. It added hash/signature analysis contracts and provenance/content-source identity structures.
- S4-T02 is reviewed and done. It added provider-backed hash calculation over explicit Stage 4 analysis content providers.
- S4-T03 is reviewed and done. It added bounded provider-backed signature detection.
- S4-T04 is reviewed and done. It added extension mismatch evaluation over reviewed signature results and metadata only.
- S4-T05 should consume reviewed hash results and caller-supplied known-file records only.
- The project still has no real evidence-backed filesystem content extraction. A known-file match against synthetic/generated provider bytes must keep those source labels visible and must not imply real parser evidence.

Before implementing:
- Summarize your understanding of the current true project state.
- List the files you expect to create or modify.
- State that this ticket matches existing hash results and in-memory known-file records only, with no byte reads or hash calculation.
- If you see a conflict between this prompt and the ticket, pause and explain it instead of broadening scope.

Your task:
- Add a minimal fixture-sized known-file matching foundation in or near `app/backend/forensic_core/content_analysis.py`.
- Consume existing S4-T02 `HashAnalysisResult` objects and a tiny caller-supplied in-memory sequence of known-file records.
- Do not accept an analysis provider in the matcher.
- Do not read bytes.
- Do not call `hash_file_content()` or `calculate_hashes()` from the matcher.
- Do not read known-file lists from disk or network.
- Define JSON-safe structures if needed. Prefer names that fit the existing module, such as:
  - `KnownFileRecord`;
  - `KnownFileMatchResult`;
  - `match_known_file_hashes()` or `match_known_files()`;
  - `known_file_match_result_to_json()`.
- Preserve hash result source provenance, content-source identity, source kind/status, bytes analyzed, hash status, digest statuses, timestamps, and warnings.
- Match only computed digest values already present on the `HashAnalysisResult`.
- Normalize algorithms the same way S4-T02 does for hash calculation: case-insensitive, with `sha-256`/`sha_256` style inputs normalized to `sha256`.
- Normalize digest values case-insensitively and preserve the original record metadata in JSON-safe form.
- Support SHA-256, MD5, and SHA-1 digest matching because S4-T02 supports those algorithms.
- Prefer SHA-256 matches when multiple digest algorithms are present, but preserve all matched records if multiple records match the available digests.
- Include explicit result fields such as:
  - `matched`: `True`, `False`, or `None`;
  - `match_category`: for simple single-category matches;
  - `matched_algorithm`;
  - `matched_digest`;
  - `matched_records`;
  - `dataset_name` / `dataset_version` through each matched record;
  - timestamps and warnings.
- Preserve only a small caller-supplied category set:
  - `known_good`;
  - `known_bad`;
  - `known_unknown`.
- Treat conflicting categories for the same matched digest as a structured non-ok or warning state, not as a silent match. A structured `conflicting_known_file_records` status is preferred.
- Keep result wording honest: matching a synthetic/provider-backed hash means the provider bytes match a caller-supplied digest record; it does not prove real evidence-derived content.

Suggested status and warning names:
- `known_file_not_checked`
- `known_file_match`
- `known_file_no_match`
- `hash_not_available`
- `hash_digest_unavailable`
- `invalid_known_file_record`
- `conflicting_known_file_records`
- `synthetic_hash_match_context`
- `generated_fixture_hash_match_context`

Test expectations:
- SHA-256 match from a reviewed `HashAnalysisResult`.
- MD5/SHA-1 matching when those digests are explicitly present.
- No-match behavior.
- Non-ok hash result behavior.
- Hash result with no computed digest behavior.
- Invalid known-file records, including unsupported algorithm, missing digest, and invalid category.
- Duplicate same-category records.
- Conflicting category records for the same algorithm/digest.
- Preservation of source provenance, content-source identity, source labels, hash warnings, matched record metadata, timestamps, and JSON safety.
- No provider argument, no byte reads, and no internal call to `hash_file_content()` or `calculate_hashes()` in the matcher.
- No regression to S4-T02 hashing, S4-T03 signature detection, and S4-T04 extension mismatch behavior.

Likely files to create or modify:
- app/backend/forensic_core/content_analysis.py
- app/backend/forensic_core/__init__.py
- app/tests/test_content_analysis_known_files.py
- app/tests/test_content_analysis_contracts.py if small contract coverage changes are needed
- app/backend/forensic_core/README.md
- app/backend/api/README.md if boundary notes need clarification
- app/fixtures/README.md
- functionality.md
- plan.md
- progression.md
- review.md
- tickets/stage-4/README.md
- tickets/stage-4/S4-T05-known-file-matching.md

Scope boundaries:
- Do not change S4-T02 hash calculation behavior.
- Do not change S4-T03 signature detection behavior.
- Do not change S4-T04 extension mismatch behavior.
- Do not add case-store persistence or schema migrations.
- Do not import NSRL or any large/external known-file dataset.
- Do not add file readers for known-file lists.
- Do not add network access.
- Do not add search, timeline, reporting, UI, real EWF parsing, real partition parsing, real filesystem parsing, deleted recovery, carving, native dependencies, commit, or push.

Documentation:
- Update `app/backend/forensic_core/README.md` with S4-T05 behavior and limits.
- Update `app/backend/api/README.md` if API boundary notes need clarification.
- Update `app/fixtures/README.md` with the fixture-sized in-memory known-file policy.
- Update `functionality.md`, `plan.md`, `progression.md`, and `review.md`.
- Update `tickets/stage-4/README.md` and `tickets/stage-4/S4-T05-known-file-matching.md` to `Review` when implementation is complete.

Verification:
- Run `python -m pytest`.
- Report the exact command and result.

Final handoff:
- Summarize files changed.
- Summarize known-file matching behavior added.
- Report the exact pytest command and result.
- State limitations and deferred work.
- Confirm you did not begin S4-T06 or any Stage 5 work.

Stop after S4-T05 and hand off for review.
```
