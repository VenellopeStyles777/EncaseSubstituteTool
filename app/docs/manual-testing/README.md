# Manual Testing

Purpose: human-run checks for backend workflows that are useful before a UI exists.

Manual checks should:

- use explicit local paths;
- avoid private evidence unless a later optional integration guide says otherwise;
- write generated outputs under ignored workspace paths or examiner-selected output directories;
- preserve the distinction between real local bytes, generated fixtures, synthetic providers, and future parser-derived evidence.

Current manual-test guides:

- `stage-4.5-first-testing.md`: planned first-testing workflow with user-provided E01 files.
- `stage-4.5-command-line-testing-guide.md`: reviewed S4.5-IMP07 PowerShell guide for the current first-testing command, artifacts, proof boundaries, reviewer transcript, S4.5-IMP08 `--hash-image` path, S4.5-IMP09/S4.5-IMP09A nested directory listing artifacts, and S4.5-IMP09B live terminal browser command. S4.5-IMP10 will refresh it for the final Stage 5 gate handoff.
