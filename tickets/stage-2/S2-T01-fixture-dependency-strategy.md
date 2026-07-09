# S2-T01 - Fixture And Dependency Strategy

Status: Done

Stage: Stage 2 - Volume and filesystem browsing MVP

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Define how Stage 2 will test image, volume, and filesystem behavior without private evidence or large committed files.

## Context To Read First

- `Goal.md`
- `plan.md`
- `research/08-stack-direction.md`
- `app/fixtures/README.md`
- `app/docs/environment-readiness.md`
- `tickets/stage-2/README.md`

## Required Work

- Document fixture choices for Stage 2.
- Decide which tests use pure stubs and which may use tiny generated files.
- Document optional dependency expectations for `pytsk3` and any EWF reader dependency.
- Add or update fixture-generation notes if needed.
- Do not commit real evidence.

## Acceptance Criteria

- Stage 2 fixture policy is documented.
- Tests can proceed without private evidence.
- Native dependency absence is not a blocker for early Stage 2 tickets.

## Handoff Prompt

```text
Implement S2-T01: Fixture And Dependency Strategy. Keep this documentation-focused and do not start filesystem parsing implementation yet.
```
