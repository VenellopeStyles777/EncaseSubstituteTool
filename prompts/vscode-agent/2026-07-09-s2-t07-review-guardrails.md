# 2026-07-09 - S2-T07 Review Guardrails

Use these guardrails if the Stage 2 VS Code implementation agent asks how far to take the documentation handoff.

```text
S2-T07 is docs and review handoff only.

Do:
- update stale Stage 1 wording in top-level/backend docs
- mark Stage 2 status accurately
- separate real local-file behavior, stubs, and synthetic preview-provider content
- document dependency policy and default test expectations
- update progression/review/ticket status
- run python -m pytest

Do not:
- add new Stage 3 code
- implement export/recovery
- add hashing/signature analysis
- add UI or executable packaging
- claim real EWF, partition, or filesystem parsing
- require pyewf/libewf/pytsk3/TSK
- commit real evidence or filesystem images
```
