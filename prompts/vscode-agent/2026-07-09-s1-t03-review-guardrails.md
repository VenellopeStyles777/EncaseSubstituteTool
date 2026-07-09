# 2026-07-09 - S1-T03 Review Guardrails

Use these guardrails if the VS Code implementation agent asks how far to take the EWF reader adapter.

```text
S1-T03 is about the adapter boundary, not full E01 parsing.

Do:
- define stable metadata/verification result structures
- add a stub adapter for deterministic tests
- add dependency-unavailable behavior for pyewf/libewf
- keep tests free of real evidence files
- keep segment discovery separate

Do not:
- require pyewf/libewf installation
- parse real EWF bytes as a requirement
- add the S1-T04 JSON command
- add filesystem parsing or pytsk3
- build UI
- commit real evidence
```
