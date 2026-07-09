# 2026-07-09 - S1-T02 Review Guardrails

Use these guardrails if the VS Code agent asks how far to take segment discovery.

```text
S1-T02 should only discover segment files by path/name and return structured results.

Do not:
- parse real EWF bytes
- add pyewf/libewf dependency logic
- implement metadata extraction
- implement verification
- build a UI
- commit real evidence files

Do:
- use temporary dummy files in tests
- keep output stable for later JSON conversion
- document behavior for gaps and unsupported inputs
- keep adapter work for S1-T03
```
