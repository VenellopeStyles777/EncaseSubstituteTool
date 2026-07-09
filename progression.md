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
