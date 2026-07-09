# 2026-07-09 - S2-T01 Fixture And Dependency Strategy Prompt

Use this prompt to hand S2-T01 to the Stage 2 VS Code implementation agent.

```text
Implement ticket S2-T01: Fixture And Dependency Strategy.

Before editing, read these files:
- tickets/stage-2/S2-T01-fixture-dependency-strategy.md
- tickets/stage-2/README.md
- Goal.md
- plan.md
- progression.md
- review.md
- workflow.md
- app/fixtures/README.md
- app/docs/environment-readiness.md
- research/08-stack-direction.md
- app/backend/forensic_core/README.md
- app/backend/api/README.md
- app/backend/case_store/README.md

Context:
- Stage 1 is complete.
- Stage 2 is beginning.
- S2-T01 is documentation/strategy only.
- Do not implement image byte streams yet.
- Do not add volume parsing yet.
- Do not add filesystem adapter code yet.
- Do not add pytsk3 as a required dependency.
- Do not commit real forensic images or large binary fixtures.

Your task:
- Document the Stage 2 fixture strategy.
- Clarify what kinds of tests should use pure stubs, tiny generated files, or optional local-only fixtures.
- Document how real/raw/EWF/TSK-style testing should be handled later without committing private evidence.
- Document optional dependency expectations for Stage 2, especially pytsk3/The Sleuth Kit and EWF reader dependencies.
- Clarify that early Stage 2 must keep tests passing without native forensic dependencies.
- Update app/fixtures/README.md.
- Update app/docs/environment-readiness.md if dependency notes need correction.
- Update plan.md only if Stage 2 status/ticket notes are stale.
- Update progression.md with the S2-T01 result.
- Add a review handoff note in review.md if useful.

Testing:
- If you only edit docs, you do not need to add tests.
- Still run python -m pytest if practical, because this confirms the existing Stage 1 foundation remains healthy.
- Report the exact test result or explain why tests were not run.

Deliverable:
- A clear Stage 2 fixture/dependency strategy that lets S2-T02 and later tickets proceed safely.
- A short handoff summary listing changed docs, test result, and remaining decisions.

Stop after S2-T01 and hand off for review. Do not begin S2-T02.
```
