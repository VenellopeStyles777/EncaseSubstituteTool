# Manual Testing

Purpose: human-run checks for backend workflows that are useful before a UI exists.

Manual checks should:

- use explicit local paths;
- avoid private evidence unless a later optional integration guide says otherwise;
- write generated outputs under ignored workspace paths or examiner-selected output directories;
- preserve the distinction between real local bytes, generated fixtures, synthetic providers, and future parser-derived evidence.

Current manual-test guides:

- `stage-4.5-first-testing.md`: planned first-testing workflow with user-provided E01 files.
- `stage-4.5-command-line-testing-guide.md`: reviewed S4.5-IMP10 PowerShell guide for the current first-testing command, artifacts, proof boundaries, reviewer transcript, S4.5-IMP08 `--hash-image` path, S4.5-IMP09/S4.5-IMP09A nested directory listing artifacts, S4.5-IMP09B live terminal browser command, S4.5-IMP11 identity/logical-image labels, and S4.5-IMP12 hash progress/interrupted-status notes.
- `stage-4.5-demo-showcase.md`: presentable short walkthrough for demonstrating the real-E01 Stage 4.5 command-line workflow, visual summary, live browser, optional image hash, S4.5-IMP11 identity/logical-image labels, privacy-safe talking points, and S4.5-IMP12 hash progress/interrupted-status notes.
