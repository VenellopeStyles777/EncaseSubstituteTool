# First Testing Scripts

Purpose: future Stage 4.5 scripts or commands that make current progress directly testable with user-provided E01 files.

Planned responsibilities:

- run E01 intake checks from an explicit user-provided `.E01` path;
- write JSON output under `.test-artifacts/first-testing/` or another explicit output directory;
- print a concise command prompt summary;
- optionally generate a simple local HTML summary;
- never write beside source evidence files;
- keep unsupported or not-implemented parser states visible.

Current status: the active first-testing command is `python -m app.backend.api.first_testing`. S4.5-IMP01 through S4.5-IMP06 are reviewed and done. This folder remains documentation/planning space for future helper scripts; do not add generated evidence output or private run artifacts here.
