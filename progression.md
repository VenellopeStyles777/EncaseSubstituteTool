# Progression - Development Journal

Purpose: track what actually changed over time. This is the narrative counterpart to `plan.md`: decisions made, features completed, tests added, and what should happen next.

Recommended entry format:

```text
YYYY-MM-DD
- Completed:
- Learned:
- Blocked by:
- Next:
```

2026-07-08
- Completed: expanded Stage 1 targets, created app skeleton folders, split research into topic files, added VS Code agent prompt, and added agent workflow documentation.
- Learned: Git is initialized on `main` with `origin` configured, but this sandbox has read-only access to `.git` and cannot stage/commit.
- Blocked by: remote GitHub check failed because the environment attempted to connect through an unavailable local proxy; push was not attempted.
- Next: from VS Code or a normal terminal, set the remote to the proper GitHub repository URL if needed, stage the intended files, commit, and push to `origin main`.

2026-07-09
- Completed: created ticketing workflow, Stage 1 ticket set, and VS Code agent prompt history folder.
- Learned: Stage 1 should be handled as six small tickets so implementation and review stay clean.
- Blocked by: nothing for ticket planning.
- Next: give the VS Code agent the Stage 1 ticketing start prompt, then begin S1-T01.

2026-07-09
- Completed: checked local environment readiness for Stage 1 and documented findings in `app/docs/environment-readiness.md`.
- Learned: Git is healthy, but the normal shell does not have a real Python/pip setup yet; `python` is only the Microsoft Store alias.
- Blocked by: Stage 1 tests need Python 3.11+ and pytest installed in a real project environment.
- Next: install/configure Python, create `.venv`, install pytest, and rerun S1-T01 smoke tests.

2026-07-09
- Completed: implemented ticket S1-T01 by adding the minimal Python backend package skeleton, pytest configuration, and smoke tests for backend package imports.
- Learned: the Stage 1 ticket workflow is active, and S1-T01 should stop at importable package structure without adding E01 discovery logic yet.
- Blocked by: no remaining S1-T01 blocker after the S1-T01A Python environment fix; the earlier missing-Python issue is resolved.
- Next: submit S1-T01/S1-T01A for review before starting S1-T02 segment discovery.

2026-07-09
- Completed: rechecked Python after environment fix; `python --version` reports Python 3.14.6, pip is available, and `python -m pytest` passed 2 tests.
- Learned: the remaining warning is a non-failing pytest cache warning under `.pytest_cache`.
- Blocked by: nothing blocking S1-T01 smoke tests now.
- Next: VS Code agent should complete supplementary ticket S1-T01A, update S1-T01 docs/progression, then stop for review before S1-T02.

2026-07-09
- Completed: implemented supplementary ticket S1-T01A by rerunning `python -m pytest`, confirming the S1-T01 smoke tests pass, and updating backend/environment documentation.
- Learned: tests pass with Python 3.14.6 and pytest 9.1.1; the `.pytest_cache` warning persists because the local cache directory is permission-denied, but it does not fail the test run.
- Blocked by: nothing for S1-T01A; `.gitignore` already covers `__pycache__/`, `.pytest_cache/`, `.venv/`, and common Python build/test artifacts.
- Next: hand S1-T01A off for review and do not begin S1-T02 until review approval or explicit user instruction.

2026-07-09
- Completed: reviewed S1-T01/S1-T01A and marked both tickets done.
- Learned: the ticket-review-commit workflow is working as intended.
- Blocked by: nothing for this commit.
- Next: commit the reviewed S1-T01/S1-T01A work, then start a new branch or ticket handoff for S1-T02.

2026-07-09
- Completed: confirmed S1-T01/S1-T01A work was committed and pushed on branch `stage-1-e01-intake` at commit `e224e21`.
- Learned: the branch workflow is active: implementation, review, commit, then separate push approval.
- Blocked by: nothing for S1-T02 planning.
- Next: hand S1-T02 to the VS Code agent for E01 segment discovery.

2026-07-09
- Completed: implemented S1-T02 E01 segment discovery with structured result objects and tests for single segments, ordered chains, missing middle segments, unsupported input, and case-insensitive extensions.
- Learned: filename-level segment discovery can stay dependency-free and read-only by inspecting only directory entries, leaving EWF metadata parsing for S1-T03 and later. Tests pass with workspace-local dummy files because this shell cannot access pytest's default temp directory and Python-created `TemporaryDirectory` folders became permission-denied.
- Blocked by: nothing for S1-T02 implementation.
- Next: hand S1-T02 off for review before beginning S1-T03 adapter work. Final test run: `python -m pytest` reported 7 passed, 1 non-failing `.pytest_cache` warning.

2026-07-09
- Completed: mitigated local pytest temp/cache permission issues by configuring pytest to use `.test-artifacts/pytest-temp` and disabling pytest's optional cache provider.
- Learned: Python itself is suitable for Stage 1; the problem was local temporary/cache directory permissions, not the segment discovery implementation.
- Blocked by: old permission-denied scratch folders remain from failed temp-directory experiments, but they are ignored and do not block tests.
- Next: optionally clean old scratch folders from Windows Explorer or after reboot; continue S1-T02 review with `python -m pytest` now reporting 7 passed.

2026-07-09
- Completed: reviewed S1-T02 segment discovery.
- Learned: main behavior is good, but `.E00` is incorrectly accepted as segment number 0.
- Blocked by: S1-T02 needs a small correction and regression test before approval.
- Next: give the VS Code agent the S1-T02 review fix prompt for `.E00` handling.

2026-07-09
- Completed: fixed the S1-T02 review finding so `.E00` is treated as an unsupported sibling segment instead of discovered segment number 0.
- Learned: with pytest cache disabled and tests using deterministic `.test-artifacts` scratch folders, `python -m pytest` now runs without the earlier cache warning in this environment.
- Blocked by: nothing for the S1-T02 review fix.
- Next: return S1-T02 for review before starting S1-T03 adapter work. Final test run: `python -m pytest` reported 8 passed.

2026-07-09
- Completed: re-reviewed S1-T02 after the `.E00` fix and approved it for commit.
- Learned: the segment discovery behavior is now good enough for the later S1-T04 JSON intake command.
- Blocked by: nothing for S1-T02.
- Next: commit S1-T02 after user approval, then prepare the S1-T03 adapter-interface ticket.

2026-07-09
- Completed: implemented and reviewed S1-T03 EWF reader adapter boundary with stub metadata, verification status shape, and structured pyewf dependency-unavailable behavior.
- Learned: the project now has a clean split between segment discovery and metadata-reader adapters, which sets up S1-T04's intake JSON command.
- Blocked by: nothing for S1-T03.
- Next: commit S1-T03 after user approval, then prepare S1-T04 intake command JSON output.

2026-07-09
- Completed: confirmed S1-T03 is committed locally as `4166b02 stage 1: EWF reader adapter` and the working tree is clean before S1-T04 prep.
- Learned: S1-T04 should compose existing segment discovery and EWF adapter result shapes rather than inventing new parsing logic.
- Blocked by: local Git view did not yet show S1-T03 on `origin/stage-1-e01-intake`; push can happen as a separate checkpoint.
- Next: hand S1-T04 to the VS Code agent for intake command JSON output.

2026-07-09
- Completed: confirmed S1-T02 commit `5a5f90e stage 1: E01 segment discovery` is visible locally on `stage-1-e01-intake`; user reported it was pushed and merged.
- Learned: the branch remains clean and ready for the next ticket handoff.
- Blocked by: nothing for S1-T03 planning.
- Next: hand S1-T03 to the VS Code agent for EWF reader adapter interface and stub behavior.

2026-07-09
- Completed: implemented S1-T03 EWF reader adapter boundary with structured dependency, metadata, warning, and verification result objects; added a dependency-free stub adapter and pyewf-unavailable adapter path.
- Learned: the reader adapter can remain separate from segment discovery and tests can cover metadata shape without real E01 evidence or native libraries.
- Blocked by: nothing for S1-T03 implementation.
- Next: hand S1-T03 off for review before beginning S1-T04 intake JSON command work. Final test run: `python -m pytest` reported 12 passed.

2026-07-09
- Completed: implemented S1-T04 intake JSON command/callable that composes E01 segment discovery with the EWF reader adapter boundary and handles invalid input as structured output.
- Learned: the intake layer can stay thin by reusing `discover_e01_segments()` and adapter result objects instead of duplicating their logic.
- Blocked by: nothing for S1-T04 implementation.
- Next: hand S1-T04 off for review before beginning S1-T05 SQLite case-store work. Final test run: `python -m pytest` reported 17 passed.

2026-07-09
- Completed: reviewed S1-T04 intake command/callable.
- Learned: main structure is good, but intake status is misleading if `pyewf` is importable while real metadata extraction remains unimplemented.
- Blocked by: S1-T04 needs a small status-contract fix and regression test before approval.
- Next: give the VS Code agent the S1-T04 review fix prompt for importable-but-not-implemented pyewf status handling.

2026-07-09
- Completed: fixed the S1-T04 review finding so an importable-but-unimplemented pyewf adapter returns `reader_not_implemented` instead of `ok`.
- Learned: intake status needs to consider adapter warning codes, not just whether the adapter dependency is importable.
- Blocked by: nothing for the S1-T04 review fix.
- Next: return S1-T04 for review before starting S1-T05 SQLite case-store work. Final test run: `python -m pytest` reported 18 passed.

2026-07-09
- Completed: re-reviewed S1-T04 after the status-contract fix and approved it for commit.
- Learned: the VS Code agent handoff summary is useful context, but review should still verify files and rerun tests.
- Blocked by: nothing for S1-T04.
- Next: commit S1-T04 after user approval, then prepare S1-T05 minimal SQLite case-store schema.
