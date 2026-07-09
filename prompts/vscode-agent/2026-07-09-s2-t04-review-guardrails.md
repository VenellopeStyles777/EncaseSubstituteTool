# 2026-07-09 - S2-T04 Review Guardrails

Use these guardrails if the Stage 2 VS Code implementation agent asks how far to take filesystem adapter work.

```text
S2-T04 is only the filesystem adapter boundary.

Do:
- define stable filesystem adapter/result/status structures
- define file/directory entry metadata shape
- add a deterministic stub adapter for tests
- add pytsk3 dependency-unavailable behavior
- include volume/source provenance and read-only assertions

Do not:
- require pytsk3 or TSK
- parse real filesystems as a default path
- add directory-listing CLI/workflow; that is S2-T05
- add preview rendering; that is S2-T06
- export files
- commit real evidence or filesystem images
```
