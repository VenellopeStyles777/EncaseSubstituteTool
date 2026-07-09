# S1-T03 - EWF Reader Adapter Interface

Status: Ready

Stage: Stage 1 - E01 intake spike

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Define a clean EWF reader adapter boundary so Stage 1 can support real libewf/pyewf later while tests remain dependency-free.

## Context To Read First

- `research/02-e01-ewf-image-format.md`
- `research/06-tools-plugins-skills.md`
- `research/08-stack-direction.md`
- `app/backend/forensic_core/README.md`

## Target Files/Folders

- `app/backend/forensic_core/`
- `app/tests/`

## Required Work

- Define an EWF reader adapter protocol/base class/interface.
- Add a stub/mock adapter that returns predictable metadata and dependency status.
- Optionally add a pyewf adapter skeleton that fails gracefully if `pyewf` is unavailable.
- Represent verification status as structured data, even if real verification is not implemented.
- Ensure no adapter writes to evidence files.

## Acceptance Criteria

- Adapter interface has stable methods for metadata and verification status.
- Stub adapter works in tests.
- Missing `pyewf` does not crash the app.
- Dependency-unavailable behavior is explicit and testable.

## Test Expectations

- Test stub metadata response shape.
- Test dependency-unavailable path.
- Test verification status field shape.

## Documentation Updates

- Update `app/backend/forensic_core/README.md`.
- Update `research/02-e01-ewf-image-format.md` if the adapter contract changes.
- Update `progression.md`.

## Review Checklist

- Is adapter logic separate from segment discovery?
- Can a real pyewf implementation be added without rewriting tests?
- Are dependency errors clear?
- Is read-only behavior documented?

## Handoff Prompt

```text
Implement ticket S1-T03: EWF Reader Adapter Interface.

Read research/02-e01-ewf-image-format.md, research/06-tools-plugins-skills.md, research/08-stack-direction.md, and app/backend/forensic_core/README.md first.

Define an adapter interface for EWF metadata/verification. Add a stub adapter for tests and a graceful dependency-unavailable path for pyewf/libewf. Keep segment discovery separate from reader logic. Ensure the response includes a verification status field even if real verification is not implemented.

Update docs and progression.md. Run tests and report results.
```
