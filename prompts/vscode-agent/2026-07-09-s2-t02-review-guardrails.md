# 2026-07-09 - S2-T02 Review Guardrails

Use these guardrails if the Stage 2 VS Code implementation agent asks how far to take the byte-stream abstraction.

```text
S2-T02 is only the read-only image/byte-stream abstraction.

Do:
- support tiny generated local files
- read bounded byte ranges
- return structured status/errors
- include source provenance and read-only assertion
- test missing path, directory path, invalid ranges, and EOF behavior

Do not:
- parse partitions or volumes
- parse filesystems
- add pytsk3 or TSK
- add EWF byte reading unless it is a dependency-safe stub boundary
- add preview rendering
- add export/recovery
- commit real evidence or binary forensic images
```
