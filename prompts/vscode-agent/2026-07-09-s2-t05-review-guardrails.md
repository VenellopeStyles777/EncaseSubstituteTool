# 2026-07-09 - S2-T05 Review Guardrails

Use these guardrails if the Stage 2 VS Code implementation agent asks how far to take directory listing work.

```text
S2-T05 is only a backend directory listing/file metadata view.

Do:
- consume the existing filesystem adapter boundary
- expose a JSON-friendly listing callable
- return deterministic stub root entries
- preserve source/volume/adapter/read-only provenance
- report unsupported paths and unavailable adapters as structured statuses
- update tests and docs

Do not:
- parse real filesystems as a required path
- require pytsk3 or The Sleuth Kit
- read or preview file content; that is S2-T06
- export/recover files
- hash file content
- add UI
- commit real evidence or filesystem images
```
