# S4-T05 - Fixture-Sized Known-File Matching

Status: Done

Stage: Stage 4 - Hash and signature foundations

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Add a very small known-file matching foundation after reviewed S4-T02 hash results.

Known-file matching must remain fixture-sized for default tests. It should consume existing `HashAnalysisResult` objects and a caller-supplied in-memory list of known-file records only. Do not introduce NSRL-scale data, downloads, network access, required external databases, case-store persistence, or implicit hash calculation.

This ticket depends on reviewed S4-T01 contracts and reviewed S4-T02 provider-backed hashing. S4-T03 and S4-T04 are also reviewed and done, but known-file matching should not depend on signature detection or extension mismatch behavior.

## Context To Read First

- `prompts/vscode-agent/2026-07-14-stage-4-familiarization.md`
- `tickets/stage-4/README.md`
- `tickets/stage-4/S4-T00-review-agent-risk-audit.md`
- `tickets/stage-4/S4-T01-hash-signature-contracts.md`
- `tickets/stage-4/S4-T02-provider-backed-hashing.md`
- `tickets/stage-4/S4-T03-file-signature-detection.md`
- `tickets/stage-4/S4-T04-extension-mismatch-rules.md`
- `tickets/stage-4/S4-T05-known-file-matching.md`
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
- `app/tests/test_content_analysis_extension_mismatch.py`

## Target Files/Folders

Likely files to create or modify:

- `app/backend/forensic_core/content_analysis.py`
- `app/backend/forensic_core/__init__.py`
- `app/tests/test_content_analysis_known_files.py`
- `app/tests/test_content_analysis_contracts.py` if small contract coverage changes are needed
- `app/backend/forensic_core/README.md`
- `app/backend/api/README.md` if boundary notes need clarification
- `app/fixtures/README.md`
- `functionality.md`
- `plan.md`
- `progression.md`
- `review.md`
- `tickets/stage-4/README.md`
- `tickets/stage-4/S4-T05-known-file-matching.md`

Do not modify Stage 2 preview behavior, Stage 3 export behavior, S4-T02 hash calculation behavior, S4-T03 signature detection behavior, S4-T04 extension mismatch behavior, filesystem parsing, or case-store schema in this ticket unless a small import/export list update is needed.

## Required Work

- Add a minimal in-memory known-file matching contract in or near `app/backend/forensic_core/content_analysis.py`.
- Consume an existing `HashAnalysisResult` as the primary input.
- Accept a tiny caller-supplied sequence of known-file records. Do not read known-file data from disk or network.
- Do not accept an analysis provider, read bytes, or call `hash_file_content()` / `calculate_hashes()` from the matcher.
- Define JSON-safe structures if needed. Prefer names that fit the existing module, such as:
  - `KnownFileRecord`;
  - `KnownFileMatchResult`;
  - `match_known_file_hashes()` or `match_known_files()`;
  - `known_file_match_result_to_json()`.
- Preserve hash result source provenance, content-source identity, source kind/status, bytes analyzed, hash status, digest statuses, timestamps, and warnings.
- Match only computed digest values already present on the `HashAnalysisResult`.
- Normalize algorithms the same way S4-T02 does for hash calculation: case-insensitive, with `sha-256`/`sha_256` style inputs normalized to `sha256`.
- Normalize digest values case-insensitively and preserve the original record metadata in JSON-safe form.
- Support at least SHA-256, MD5, and SHA-1 because S4-T02 supports those algorithms.
- Prefer SHA-256 matches when multiple digest algorithms are present, but preserve all matched records if multiple records match the available digests.
- Include explicit result fields such as:
  - `matched`: `True`, `False`, or `None`;
  - `match_category`: for simple single-category matches;
  - `matched_algorithm`;
  - `matched_digest`;
  - `matched_records`;
  - `dataset_name` / `dataset_version` through each matched record;
  - timestamps and warnings.
- Preserve caller-supplied record category values only from a small allowed set:
  - `known_good`;
  - `known_bad`;
  - `known_unknown`.
- Treat conflicting categories for the same matched digest as a structured non-ok or warning state, not as a silent match. A structured `conflicting_known_file_records` status is preferred.
- Keep result wording honest: matching a synthetic/provider-backed hash means the provider bytes match a caller-supplied digest record; it does not prove real evidence-derived content.

## Suggested Status And Warning Names

Use existing S4-T01/S4-T02 names where possible. Suggested new status codes:

- `known_file_not_checked`
- `known_file_match`
- `known_file_no_match`
- `hash_not_available`
- `hash_digest_unavailable`
- `invalid_known_file_record`
- `conflicting_known_file_records`

Suggested warning codes:

- `known_file_match`
- `known_file_no_match`
- `hash_not_available`
- `hash_digest_unavailable`
- `invalid_known_file_record`
- `conflicting_known_file_records`
- `synthetic_hash_match_context`
- `generated_fixture_hash_match_context`

## Acceptance Criteria

- Known-file matching consumes existing `HashAnalysisResult` objects and caller-supplied in-memory records only.
- No provider bytes are read and no hash calculation is run by the matcher.
- A matching digest returns a structured result with `matched=True`, matched algorithm/digest, category, matched record metadata, source provenance, and content-source identity.
- No match returns a structured result with `matched=False`, not a failure.
- Non-ok hash results return structured not-evaluated results with `matched=None`.
- Hash results with no computed digests return structured not-evaluated results with `matched=None`.
- Invalid known-file records are surfaced through structured status/warnings and do not crash.
- Conflicting categories for the same matched digest are surfaced through structured status/warnings and are not silently resolved.
- Synthetic/generated provider labels and warnings from the source hash result remain visible in the match result.
- Result JSON contains no bytes and is stable enough for future search/timeline work.
- Default tests pass without real evidence, native dependencies, network access, external known-file datasets, or large fixtures.

## Out Of Scope

- NSRL import.
- Database-scale matching.
- Case-store persistence or schema migrations.
- Network downloads.
- Reading known-file lists from disk.
- Automatic hash calculation.
- Signature detection or extension mismatch behavior.
- UI filtering.
- Search/timeline/reporting.
- Real parser work or native dependencies.

## Test Expectations

Add focused tests under `app/tests/`.

Tests should cover:

- SHA-256 match from a reviewed `HashAnalysisResult`;
- MD5/SHA-1 matching when those digests are explicitly present;
- no-match behavior;
- non-ok hash result behavior;
- hash result with no computed digest behavior;
- invalid known-file records, including unsupported algorithm, missing digest, and invalid category;
- duplicate same-category records;
- conflicting category records for the same algorithm/digest;
- preservation of source provenance, content-source identity, source labels, hash warnings, matched record metadata, timestamps, and JSON safety;
- no provider argument, no byte reads, and no internal call to `hash_file_content()` or `calculate_hashes()` in the matcher;
- no regression to S4-T02 hashing, S4-T03 signature detection, and S4-T04 extension mismatch behavior.

Run `python -m pytest`.

## Documentation Updates

- Update `app/backend/forensic_core/README.md` with S4-T05 behavior and limits.
- Update `app/backend/api/README.md` if API boundary notes need clarification.
- Update `app/fixtures/README.md` with the fixture-sized in-memory known-file policy.
- Update `functionality.md`, `plan.md`, `progression.md`, and `review.md`.
- Update this ticket and `tickets/stage-4/README.md` to `Review` when implementation is complete.

## Review Checklist

- Known-file data is tiny, explicit, and dependency-free.
- Matching consumes reviewed hash results only and does not compute hashes or read bytes internally.
- Matching does not overstate synthetic/provider-backed hash results as real evidence-backed findings.
- Invalid and conflicting known-file records are structured and tested.
- Source provenance, content-source identity, hash statuses, digest statuses, warnings, and timestamps are preserved.
- Persistence, large imports, network downloads, file readers, search/timeline, UI/reporting, parser work, deleted recovery, carving, native dependencies, and Stage 5 work remain deferred.

## Implementation Notes

- `content_analysis.py` now defines `KnownFileRecord`, `KnownFileMatchResult`, `match_known_file_hashes()`, `match_known_files()`, and `known_file_match_result_to_json()`.
- Matching consumes an existing `HashAnalysisResult` plus caller-supplied in-memory records only. It does not accept an analysis provider, read bytes, read known-file lists from disk/network, or calculate hashes internally.
- Records support normalized SHA-256, MD5, and SHA-1 algorithms plus `known_good`, `known_bad`, and `known_unknown` categories.
- Results preserve the source hash provenance, content-source identity, hash status, digest statuses, bytes analyzed, timestamps, hash warnings, matched record metadata, and synthetic/generated context warnings.
- Invalid records, unavailable hashes, missing digest values, no-match states, duplicate records, and conflicting categories for the same matched digest are covered by dependency-free tests.

## Review Result - 2026-07-14

- Approved and marked done.
- No blocking findings found.
- Reviewer confirmed matching consumes an existing S4-T02 `HashAnalysisResult` plus caller-supplied in-memory known-file records only.
- Reviewer confirmed `match_known_file_hashes()` and `match_known_files()` do not accept providers, read bytes, read known-file lists from disk/network, or calculate hashes internally.
- Reviewer confirmed records support normalized SHA-256, MD5, and SHA-1 algorithms plus `known_good`, `known_bad`, and `known_unknown` categories.
- Reviewer confirmed non-ok hashes, missing computed digests, invalid records, duplicate records, no-match states, and conflicting categories for the same matched digest are structured and tested.
- Reviewer confirmed source provenance, content-source identity, hash status, digest statuses, bytes analyzed, hash timestamps, source hash warnings, matched record metadata, and synthetic/generated context warnings are preserved.
- Reviewer confirmed S4-T05 did not add case-store persistence, schema migrations, external datasets, known-file file readers, network access, search/timeline, UI/reporting, real parser work, deleted recovery, carving, native dependencies, S4-T02/S4-T03/S4-T04 behavior changes, export-output behavior changes, or Stage 5 work.
- Reviewer verification: focused S4-T05 run `python -m pytest app/tests/test_content_analysis_known_files.py` reported 12 passed in 0.19s; full run `python -m pytest` reported 152 passed in 3.47s.

## Handoff Prompt

```text
Implement ticket S4-T05: Fixture-Sized Known-File Matching.

Before editing, read:
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

Task:
- Add a minimal fixture-sized known-file matching foundation that consumes existing S4-T02 `HashAnalysisResult` objects and a tiny caller-supplied in-memory list of known-file records.
- Do not accept an analysis provider, read bytes, read known-file data from disk/network, or call `hash_file_content()` / `calculate_hashes()` from the matcher.
- Define JSON-safe known-file record/result structures with source provenance, content-source identity, hash status, digest statuses, matched record metadata, explicit `matched` value, timestamps, and warnings.
- Support SHA-256, MD5, and SHA-1 digest matching because S4-T02 can compute those algorithms.
- Preserve only a small category set: `known_good`, `known_bad`, and `known_unknown`.
- Surface invalid records and conflicting categories through structured status/warnings.
- Preserve synthetic/generated source labels so a digest match does not imply real evidence-derived content.
- Add dependency-free tests for match, no-match, non-ok hash result, missing digests, invalid records, duplicate/conflicting records, provenance/warnings, JSON safety, and regression coverage.
- Update requested docs and ticket status.
- Run python -m pytest and report the exact result.

Scope boundaries:
- Do not change S4-T02 hash calculation behavior.
- Do not change S4-T03 signature detection behavior.
- Do not change S4-T04 extension mismatch behavior.
- Do not add case-store persistence, schema migrations, NSRL imports, external datasets, file readers for known-file lists, network access, search, timeline, reporting, UI, real EWF parsing, real partition parsing, real filesystem parsing, deleted recovery, carving, native dependencies, commit, or push.

Stop after S4-T05 and hand off for review.
```
