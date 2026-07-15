# Manual Testing

Purpose: human-run checks for backend workflows that are useful before a UI exists.

Manual checks should:

- use explicit local paths;
- avoid private evidence unless a later optional integration guide says otherwise;
- write generated outputs under ignored workspace paths or examiner-selected output directories;
- preserve the distinction between real local bytes, generated fixtures, synthetic providers, and future parser-derived evidence.

Current manual-test guides:

- `stage-4.5-first-testing.md`: planned first-testing workflow with user-provided E01 files.
