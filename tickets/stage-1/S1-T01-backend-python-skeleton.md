# S1-T01 - Backend Python Skeleton

Status: Ready

Stage: Stage 1 - E01 intake spike

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Create the first runnable Python backend skeleton so later E01 intake work has a stable place to live.

## Context To Read First

- `Goal.md`
- `research/05-development-stages.md`
- `research/08-stack-direction.md`
- `workflow.md`
- `app/README.md`
- `app/backend/README.md`

## Target Files/Folders

- `app/backend/`
- `app/backend/forensic_core/`
- `app/backend/case_store/`
- `app/tests/`
- Project-level dependency/test config files if needed.

## Required Work

- Create a minimal Python package/module structure under `app/backend`.
- Add enough package files so imports work cleanly.
- Add a minimal test setup.
- Add one smoke test that proves the backend package can be imported.
- Add a simple documented command for running tests.
- Avoid adding E01 logic in this ticket unless it is only a placeholder interface.

## Acceptance Criteria

- The backend package imports successfully.
- A test command is documented.
- At least one smoke test passes.
- No real evidence files are required.
- The folder structure still matches the architecture docs.

## Test Expectations

- Run the chosen test command.
- If dependencies are missing, document the exact setup step.

## Documentation Updates

- Update `app/backend/README.md` with package/test command notes.
- Update `progression.md` with completed setup and blockers.

## Review Checklist

- Is the skeleton small and easy to understand?
- Did it avoid premature UI work?
- Are commands clear for Windows?
- Are generated/cache files ignored or absent?

## Handoff Prompt

```text
Implement ticket S1-T01: Backend Python Skeleton.

Read Goal.md, workflow.md, research/05-development-stages.md, research/08-stack-direction.md, app/README.md, and app/backend/README.md first.

Create a minimal Python backend package under app/backend with a test setup and one smoke test proving the package imports. Keep this ticket small: do not implement E01 segment discovery yet except for placeholder package structure if useful.

Update app/backend/README.md and progression.md with the test command, what changed, and any blockers. Run the tests if possible and report the exact result.
```
