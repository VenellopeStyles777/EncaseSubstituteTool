# Goal - EnCase-Like Forensic Analysis App

Purpose: this file defines the product goal, current scope, staged development path, and the starter prompt for the VS Code Codex agent.

## Product Goal

Build a desktop forensic analysis application that can open segmented EWF/EnCase evidence images (`.E01`, `.E02`, `.E03`, ...), preserve forensic integrity, and help an examiner inspect filesystems, recover/export files, run hash analysis, detect file signatures, search evidence, bookmark findings, and generate reports.

This project should be inspired by EnCase/OpenText Forensic workflows, but scoped as an independent forensic workstation MVP. The first version should prioritize correctness, transparency, and testability over breadth.

## Non-Negotiable Principles

- Evidence files are read-only.
- Every result must keep provenance: evidence id, volume id, file id/path, offsets when available, parser/job version, and timestamp.
- Long analysis should run in background jobs with status and recoverable errors.
- Unsupported formats and parsing failures must be visible to the examiner.
- Generated exports and reports must include hashes and enough metadata to explain where each item came from.

## Initial MVP Scope

MVP target:

- Create/open a case.
- Add an E01 evidence set.
- Show image metadata and verification status where available.
- Detect partitions/volumes.
- Browse at least one filesystem from the image.
- Show file metadata and preview raw/text/hex where reasonable.
- Export selected files with hashes and provenance.
- Run per-file hash jobs.
- Run file signature detection and extension mismatch checks.
- Record bookmarks/notes.
- Generate a basic HTML report.

Out of initial scope:

- Live acquisition from devices.
- Mobile/cloud acquisition.
- Password cracking.
- AI image classification.
- Full artifact parsing library.
- Court-ready parity with commercial EnCase.

## Development Stages

1. Foundation: initialize Git, choose stack, create skeleton, add test/lint commands, define docs structure.
2. Evidence intake: prove segmented E01 discovery, metadata reading, read-only evidence stream, verification status, and error handling.
3. Volume/filesystem view: parse partitions and browse one filesystem with metadata.
4. Export/recovery: export selected files and later recover deleted files where supported.
5. Hash/signature analysis: add file hashing, known-file matching, file type detection, and mismatch flags.
6. Search/timeline: add filename search, metadata filters, full-text search, and timestamp timeline.
7. Reporting/workflow: bookmarks, examiner notes, audit log, and report generation.
8. Advanced features: carving, artifact parsers, archive expansion, shadow copies, encryption detection, OCR, and optional AI triage.

## Recommended First Technical Direction

Start with a narrow backend proof before building a polished UI:

- Use a small local service/module for forensic operations.
- Investigate `pyewf`/libewf for E01 access and `pytsk3`/The Sleuth Kit for filesystem parsing.
- Store case and analysis state in SQLite.
- Keep UI/backend boundaries clean so native dependency choices can change later.

## VS Code Codex Agent Starter Prompt

```text
You are working in this project to begin an EnCase-like forensic analysis app focused first on segmented EWF/EnCase images (.E01, .E02, .E03...). Read readme.md, Goal.md, research.md, functionality.md, plan.md, progression.md, and review.md before coding.

Your first job is to create the initial project skeleton and a narrow evidence-intake proof of concept. Do not attempt the full forensic UI yet.

Requirements:
- Initialize a sensible app structure under app/.
- Prefer a backend-first spike that can later connect to a desktop UI.
- Implement segment discovery for an E01 evidence set: given a path to .E01, identify expected sibling segments (.E02, .E03, etc.) and report missing/available segments safely.
- Add an evidence metadata interface. If libewf/pyewf is available, use it to read real EWF metadata and verification information. If it is not available, create a clean adapter interface plus a documented stub/fallback so the project can still run and tests can pass.
- Keep all evidence access read-only.
- Add a SQLite-oriented case storage plan or minimal schema for cases, evidence sources, and audit events.
- Add tests for segment discovery, unsupported input handling, metadata response shape, and read-only assumptions.
- Update plan.md and progression.md with what you changed, what worked, and what remains blocked.

Engineering priorities:
- Do not hard-code real evidence paths.
- Do not require large forensic images for tests.
- Use tiny generated fixtures where possible.
- Make native dependency requirements explicit, especially for Windows.
- Keep functions small and reviewable because a separate research/review agent will inspect the code.

Deliverable:
- A runnable first skeleton with clear commands.
- Tests that pass locally or a clear note explaining exactly why they cannot run yet.
- Documentation updates in the existing Markdown files.
```
