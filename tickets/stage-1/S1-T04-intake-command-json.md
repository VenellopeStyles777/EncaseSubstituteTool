# S1-T04 - Intake Command JSON Output

Status: Ready

Stage: Stage 1 - E01 intake spike

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Create a simple command-line entry point that runs the intake flow and returns structured JSON.

## Context To Read First

- `Goal.md`
- `research/02-e01-ewf-image-format.md`
- `tickets/stage-1/S1-T02-e01-segment-discovery.md`
- `tickets/stage-1/S1-T03-ewf-reader-adapter.md`

## Target Files/Folders

- `app/backend/api/`
- `app/backend/forensic_core/`
- `app/tests/`
- `app/backend/README.md`

## Required Work

- Add a command or module entry point that accepts an `.E01` path.
- Compose segment discovery and reader adapter metadata.
- Return JSON with stable fields.
- Return clear non-zero/error behavior for invalid input if using CLI style.
- Keep output suitable for future UI consumption.

## Acceptance Criteria

- A documented command returns JSON for a dummy/stub-backed intake.
- JSON includes source path, segments, warnings, adapter status, metadata, verification status, and read-only assertion.
- Invalid input is handled predictably.
- Tests cover output shape without real evidence.

## Test Expectations

- Test successful JSON shape using temporary files and stub adapter.
- Test invalid path or unsupported extension.
- Test command/module behavior where practical.

## Documentation Updates

- Update `app/backend/README.md` with command usage.
- Update `progression.md`.

## Review Checklist

- Is the JSON contract stable and simple?
- Does command behavior avoid stack traces for normal invalid input?
- Is it future-UI friendly?
- Are tests small and deterministic?

## Handoff Prompt

```text
Implement ticket S1-T04: Intake Command JSON Output.

Read Goal.md, research/02-e01-ewf-image-format.md, and tickets S1-T02/S1-T03 first.

Create a simple backend command or module entry point that accepts a .E01 path, runs segment discovery, uses the EWF adapter boundary, and returns structured JSON. Use the stub adapter for tests so no real forensic evidence is required.

Document the command in app/backend/README.md, update progression.md, run tests, and report the result.
```
