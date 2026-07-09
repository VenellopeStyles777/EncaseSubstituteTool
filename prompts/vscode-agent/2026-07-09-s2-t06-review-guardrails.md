# 2026-07-09 - S2-T06 Review Guardrails

Use these guardrails if the Stage 2 VS Code implementation agent asks how far to take preview work.

```text
S2-T06 is only a bounded raw/text/hex preview foundation.

Do:
- use stub or tiny generated preview bytes
- keep reads bounded and read-only
- return JSON-friendly preview results
- preserve source, volume, file, offset, mode, truncation, status, warning, and provider provenance
- test text, hex, raw serialization, truncation, invalid ranges, missing files, unsupported modes, and directory/non-file paths
- update docs and ticket status

Do not:
- parse real filesystems or EWF data
- pretend stub filesystem entries have real evidence byte offsets
- export or recover files
- hash content
- add UI
- add case-store persistence or audit events
- require pytsk3, The Sleuth Kit, pyewf, or libewf
- commit real evidence or filesystem images
```
