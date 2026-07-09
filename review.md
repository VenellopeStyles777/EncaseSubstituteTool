# Review - Code and Architecture Review Notes

Purpose: use this file for findings from research/review agents. Keep reviews focused on defects, forensic-soundness risks, data-integrity risks, missing tests, and architecture drift.

Review priorities for this project:

- Evidence must be opened read-only unless an explicit export/write operation targets a separate output path.
- Every parsed file, exported file, hash, and report item should preserve source provenance.
- Long operations need cancellation, progress, and error recovery.
- Tests should use known tiny forensic images or generated fixtures, not uncontrolled real evidence.
- UI convenience must not hide evidence integrity state, parsing errors, or unsupported filesystem/image features.

## Current Review Queue

## S1-T06 Review Expectations

- Docs should accurately describe current Stage 1 behavior and limitations.
- Test commands should be current and runnable.
- The handoff should not claim real EWF parsing, filesystem parsing, UI, or automatic persistence.
- The final Stage 1 review section should make it clear what is ready for Stage 2 planning.

## 2026-07-09 - Stage 1 Final Review

Result: Stage 1 complete at the planning/review level.

Verified Stage 1 scope:

- Backend skeleton exists and imports.
- E01 segment discovery is implemented and tested without real evidence.
- EWF reader adapter boundary is implemented with stub and pyewf-unavailable behavior.
- Intake JSON callable/CLI exists and handles invalid input/dependency states.
- SQLite case-store schema exists for cases, evidence sources, audit events, and schema migration marker.
- Documentation clearly states that real EWF byte parsing, filesystem parsing, UI, and automatic intake persistence are not implemented yet.

Stage 2 readiness:

- Stage 2 tickets exist under `tickets/stage-2/`.
- Stage 2 should begin with fixture/dependency strategy before implementing byte streams or filesystem adapters.
- Review should continue enforcing read-only source handling, structured unsupported-dependency behavior, and no private evidence in tests.

Stage 3 readiness:

- Stage 3 tickets exist under `tickets/stage-3/`.
- Stage 3 should not begin until Stage 2 provides a stable file/metadata source.

## 2026-07-09 - Stage 1 Final Review Handoff

Result: ready for research/review agent final Stage 1 review.

Implemented capabilities to verify:

- Backend Python package skeleton and pytest configuration.
- E01 segment discovery with ordered segments and structured warnings.
- EWF reader adapter boundary with stub metadata, verification status shape, and pyewf dependency-unavailable behavior.
- Intake JSON command/callable through `python -m app.backend.api.intake path\to\sample.E01`.
- SQLite schema/helpers for `cases`, `evidence_sources`, `audit_events`, and `schema_migrations`.

Current limitations to keep visible:

- No real EWF byte parsing or real image verification yet.
- No partition/filesystem parsing yet.
- No UI yet.
- No automatic persistence from intake command to SQLite yet.
- `pyewf`/libewf is optional and not required for tests.
- No real forensic evidence is required for tests.

Review commands:

```powershell
python -m pytest
python -m app.backend.api.intake path\to\sample.E01 --adapter stub
```

Expected S1-T06 test result:

- `python -m pytest`: 22 passed.

Suggested final review checklist:

- Confirm documentation does not overclaim Stage 1 behavior.
- Confirm test and intake commands are accurate on Windows.
- Confirm no Stage 2 filesystem/UI work was introduced.
- Confirm `plan.md`, `progression.md`, ticket status, and backend docs agree.

## 2026-07-09 - S1-T05 Review

Result: approved for commit.

Findings:

- No blocking issues found.
- Schema includes `cases`, `evidence_sources`, `audit_events`, and `schema_migrations`.
- Evidence source rows preserve S1-T04 intake provenance through source paths, segment discovery JSON, adapter/dependency JSON, metadata JSON, verification JSON/status, warnings JSON, read-only assertion, and timestamps.
- Audit events link to cases and optionally evidence sources.
- Tests use in-memory SQLite and do not require real evidence or persistent user data.
- The implementation stayed in scope and did not wire automatic intake persistence, UI, filesystem parsing, or real EWF parsing.

Tests:

- `python -m pytest`: 22 passed.

Residual notes:

- Audit timestamps currently use second precision. This is acceptable for the Stage 1 foundation, but later audit-heavy workflows may want higher precision or an explicit monotonic sequence.

## S1-T05 Review Expectations

- Schema should include cases, evidence_sources, and audit_events.
- Evidence source records should preserve enough provenance for S1-T04 intake output.
- Tests should use in-memory or temporary SQLite databases, not persistent user data.
- The implementation should not broaden into UI, filesystem parsing, or automatic full case workflow.
- Audit events should be generic enough to record future actions without schema churn.

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
