# S2-T05 - Directory Listing And File Metadata View

Status: Done

Stage: Stage 2 - Volume and filesystem browsing MVP

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Expose a backend directory listing/file metadata view using the Stage 2 filesystem adapter boundary.

## Required Work

- Add a backend callable, and a small command if it fits the existing API style, that lists a directory from the stub or fixture-backed filesystem adapter.
- Return file entries with path, name, type, size, timestamps when available, allocation/deleted state when available, and provenance.
- Keep output JSON-serializable.
- Report unsupported, missing, or non-directory paths as structured statuses instead of tracebacks.
- Keep file content preview and byte reads out of scope for S2-T06.

## Acceptance Criteria

- Tests cover root listing, nested path behavior if supported, and unsupported path behavior.
- Tests cover adapter-unavailable or not-implemented filesystem results.
- No UI is added.
- No private evidence is required.

## Handoff Prompt

```text
Implement S2-T05: Directory Listing And File Metadata View. Use adapter outputs and keep everything backend/JSON-friendly.
```
