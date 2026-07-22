# App Skeleton

Purpose: application source root.

Initial layout:

- `backend/`: forensic logic, case storage, workers, and local API.
- `ui/`: future desktop/web interface.
- `fixtures/`: tiny legal fixtures and fixture-generation notes.
- `tests/`: automated tests.
- `scripts/`: setup and developer utility scripts.
- `docs/`: app-specific technical documentation.

Stage 4.5 first-testing support:

- `fixtures/user-provided-e01/`: notes for real E01 inputs supplied by the user, not committed to Git.
- `backend/api/first_testing.py`: current first-testing command shell for user-provided E01 paths and safe local artifacts.
- `scripts/first_testing/`: notes for future helper scripts; the active command currently lives in the backend API module.
- `docs/manual-testing/`: human-run backend workflow checks before a UI exists.

S4.5-IMP01 through S4.5-IMP07 are reviewed and done. Stage 5 search/timeline still must wait for S5-T01 to rerun and accept the completed Stage 4.5 runway.
