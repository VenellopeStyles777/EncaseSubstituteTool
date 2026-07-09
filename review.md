# Review - Code and Architecture Review Notes

Purpose: use this file for findings from research/review agents. Keep reviews focused on defects, forensic-soundness risks, data-integrity risks, missing tests, and architecture drift.

Review priorities for this project:

- Evidence must be opened read-only unless an explicit export/write operation targets a separate output path.
- Every parsed file, exported file, hash, and report item should preserve source provenance.
- Long operations need cancellation, progress, and error recovery.
- Tests should use known tiny forensic images or generated fixtures, not uncontrolled real evidence.
- UI convenience must not hide evidence integrity state, parsing errors, or unsupported filesystem/image features.

## Current Review Queue

- Confirm S1-T05 case-store schema records evidence provenance and audit events.

## 2026-07-09 - S1-T04 Re-Review

Result: approved for commit.

Findings:

- No blocking issues found.
- The previous status-contract issue is fixed: importable-but-unimplemented pyewf now returns `reader_not_implemented` instead of `ok`.
- Stub-backed intake still returns `ok`.
- Missing-pyewf intake still returns `metadata_unavailable`.
- The intake command remains scoped to S1-T04 and does not add SQLite, UI, filesystem parsing, or real EWF parsing.

Tests:

- `python -m pytest`: 18 passed.

Residual notes:

- The CLI currently returns nonzero only for `invalid_input`; future stages may decide whether `reader_not_implemented` or `metadata_unavailable` should also have nonzero CLI exit codes.

## 2026-07-09 - S1-T04 Review

Result: changes requested.

Findings:

- [P2] `app/backend/api/intake.py`: `run_e01_intake()` reports `status: "ok"` whenever `adapter_available` is true. If `PyewfEwfReaderAdapter` is importable but real metadata extraction is still deferred, it returns empty metadata plus `real_reader_not_implemented`, yet intake status is `"ok"`. That would mislead future users who install `pyewf` before real parsing is implemented.

Tests:

- `python -m pytest`: 17 passed.

Good notes:

- The intake layer correctly composes segment discovery and EWF adapter output.
- Invalid input returns structured JSON-style data rather than a traceback.
- CLI behavior for invalid input is tested.
- No SQLite, filesystem parsing, UI work, real evidence, or native dependency requirement was added.

## S1-T04 Review Expectations

- Intake command should compose segment discovery and reader adapter output without duplicating their logic.
- Output should be JSON-serializable and stable enough for future UI use.
- Tests must pass without real evidence or native forensic dependencies.
- Invalid input should not produce raw tracebacks for expected user mistakes.
- S1-T04 must not add case storage, filesystem parsing, or UI work.

## 2026-07-09 - S1-T03 Review

Result: approved for commit.

Findings:

- No blocking issues found.
- The adapter boundary is separate from segment discovery.
- The stub adapter returns predictable synthetic metadata and verification shape for tests.
- The pyewf adapter skeleton handles missing `pyewf` as structured dependency-unavailable data, not a raw import crash.
- Tests do not require real evidence, pyewf, or libewf.

Tests:

- `python -m pytest`: 12 passed.

Residual notes:

- Real pyewf metadata extraction is intentionally deferred beyond S1-T03.
- Result dataclasses contain normal dictionaries; this is acceptable for the current boundary, but later evidence-facing code should avoid mutating returned result objects in place.

## S1-T03 Review Expectations

- Adapter interface should be separate from segment discovery.
- Tests must pass without `pyewf`, libewf, or real E01 evidence.
- Stub adapter should return predictable metadata and verification status.
- Missing dependency behavior should be structured and visible, not a raw import crash.
- Real pyewf adapter code, if added, should be optional and read-only by design.

## 2026-07-09 - S1-T02 Re-Review

Result: approved for commit.

Findings:

- No blocking issues found.
- The previous `.E00` issue is fixed: `.E00` is treated as an unsupported sibling segment and is not included in discovered segments.
- Regression coverage was added for `.E00`.
- Segment discovery remains dependency-free and read-only; it only inspects path names and directory entries.

Tests:

- `python -m pytest`: 8 passed.

Residual notes:

- Old ignored scratch/cache folders from earlier temp-directory experiments may remain locally, but they do not affect tests or Git-tracked files.

## S1-T02 Review Expectations

- Segment discovery must use temporary dummy files or mocks, not real E01 evidence.
- The code should not parse EWF content yet; that belongs to S1-T03 and later.
- Results should be structured and stable enough for the later intake JSON command.
- Missing/gap behavior should be visible through warnings or a documented exception/result.
- Tests should cover valid chains, invalid input, and gaps.

## 2026-07-09 - S1-T02 Initial Review

Result: changes requested.

Findings:

- [P2] `app/backend/forensic_core/segment_discovery.py`: `_parse_segment_number()` accepts `.E00` as segment number `0`. When `sample.E00` sits next to `sample.E01`, discovery includes `.E00` in `segments`, emits no warning, and marks the set complete. Stage 1 discovery should treat `.E00` as unsupported/invalid because the selected evidence chain starts at `.E01`.

Tests:

- `python -m pytest`: 7 passed.

Good notes:

- The implementation stays dependency-free and does not parse evidence bytes.
- The result shape is clear and future JSON-friendly.
- Tests use dummy workspace-local files, not real evidence.
- The pytest temp/cache mitigation is working; the latest test run completed without warnings.

## 2026-07-09 - S1-T01/S1-T01A Review

Result: approved for commit.

Findings:

- No blocking issues found.
- The backend package skeleton is intentionally minimal and stays within S1-T01 scope.
- Smoke tests cover package import and backend subpackage import.
- `.gitignore` covers Python cache/test artifacts, virtual environments, and common build outputs.
- `python -m pytest` passed: 2 tests passed, 1 warning.

Residual notes:

- Pytest still reports a non-blocking cache warning under `.pytest_cache`; tests pass.
- No E01 logic is expected in S1-T01. Segment discovery should begin in S1-T02.
