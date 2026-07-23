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

S4.5-IMP01 through S4.5-IMP08 are reviewed and done. S4.5-IMP09 nested directory navigation and the S4.5-IMP09A file-visible correction are in review, and S4.5-IMP10 guide/gate refresh remains required before Stage 5 search/timeline can resume.
