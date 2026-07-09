# 2026-07-09 - S2-T03 Review Guardrails

Use these guardrails if the Stage 2 VS Code implementation agent asks how far to take volume discovery.

```text
S2-T03 is only the volume discovery boundary.

Do:
- define stable volume result/status structures
- support a whole-image volume result for tiny generated local files
- include provenance and read-only assertions
- report unsupported partition parsing as structured status if needed
- test missing and zero-byte sources

Do not:
- parse filesystems
- add pytsk3 or TSK
- add real partition parsing unless explicitly small and safe
- add preview rendering
- add export/recovery
- commit evidence images
```
