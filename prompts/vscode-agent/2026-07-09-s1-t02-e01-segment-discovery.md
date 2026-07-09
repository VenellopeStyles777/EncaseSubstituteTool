# 2026-07-09 - S1-T02 E01 Segment Discovery Prompt

Use this prompt to hand the next ticket to the VS Code implementation agent.

```text
Implement ticket S1-T02: E01 Segment Discovery.

Before coding, read these files:
- tickets/stage-1/S1-T02-e01-segment-discovery.md
- tickets/stage-1/README.md
- research/02-e01-ewf-image-format.md
- research/05-development-stages.md
- app/backend/forensic_core/README.md
- app/fixtures/README.md
- progression.md
- review.md

Context:
- S1-T01 and S1-T01A are complete, reviewed, committed, and pushed on branch stage-1-e01-intake.
- Current focus is only S1-T02.
- Do not begin S1-T03 adapter work yet.
- Do not require real forensic evidence.
- Use temporary dummy files in tests for names like sample.E01, sample.E02, sample.E03, and missing/gap cases.

Your task:
- Add segment discovery logic under app/backend/forensic_core/.
- Accept a selected .E01 path and discover sibling .E02/.E03/etc. files.
- Validate unsupported/non-E01 inputs with clear behavior.
- Return structured data with ordered present segments and warnings.
- Include tests for:
  - single .E01
  - .E01 + .E02 + .E03
  - missing middle segment, such as .E01 + .E03
  - unsupported extension
  - case-insensitive extension handling if implemented
- Keep all evidence access read-only.
- Update app/backend/forensic_core/README.md and progression.md.
- Run python -m pytest and report the result.

Stop after S1-T02 and hand off for review. Do not start S1-T03 unless the user explicitly approves.
```
