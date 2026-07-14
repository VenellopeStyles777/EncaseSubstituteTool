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

0. Foundation: initialize Git, choose stack, create skeleton, add test/lint commands, define docs structure. Status: complete.
1. Evidence intake: prove segmented E01 discovery, adapter boundaries, JSON intake output, case-store schema, and dependency-safe behavior. Status: complete.
2. Volume/filesystem view: establish image/byte-stream fixtures, discover whole-image volumes, and browse a stubbed filesystem with metadata and bounded preview output. Status: complete as of S2-T07 final review.
3. Export/recovery: export selected files with provenance and lay groundwork for deleted-file recovery where supported. Status: complete as a backend fixture/stub export foundation after S3-T06 final review.
4. Hash/signature analysis: add file hashing, known-file matching, file type detection, and mismatch flags. Status: in progress; S4-T01 contracts, S4-T02 provider-backed hashing, S4-T03 file signature detection, S4-T04 extension mismatch rules, and S4-T05 fixture-sized known-file matching are reviewed and done.
5. Search/timeline: add filename search, metadata filters, full-text search, and timestamp timeline.
6. Reporting/workflow: bookmarks, examiner notes, audit log, and report generation.
7. Advanced features: carving, artifact parsers, archive expansion, shadow copies, encryption detection, OCR, and optional AI triage.

## Stage 1 Detailed Targets

Stage 1 goal: prove the app can safely recognize and describe an E01 evidence set before any full UI or filesystem browser is built.

Targets:

- Create a backend-first skeleton under `app/backend/`.
- Implement segment discovery from a selected `.E01` path.
- Report discovered sibling segments, expected sequence, gaps, and unsupported naming patterns.
- Define a clean EWF reader adapter interface.
- Add a real-reader target for libewf/pyewf if the dependency is available.
- Add a stub/mock adapter so development and tests can continue without native forensic dependencies.
- Return structured metadata as JSON or a Python object/dict with stable fields.
- Add a minimal case-store schema or migration draft for cases, evidence sources, and audit events.
- Add a command-line or local API entry point for the intake spike.
- Add tests for segment discovery, unsupported inputs, missing dependencies, and metadata response shape.
- Update project docs with setup commands, dependency notes, and known limitations.

Stage 1 acceptance criteria:

- The app has one documented command that performs an E01 intake check.
- The command does not modify source evidence files.
- Tests can run without large real forensic images.
- Native dependency absence is handled with a useful message.
- Review notes are captured in `review.md` before any push to GitHub.

Stage 1 status: complete as of 2026-07-09.

Implemented:

- Python backend skeleton and test configuration.
- E01 segment discovery for sibling `.E01/.E02/.E03...` files.
- EWF reader adapter boundary with stub and pyewf-unavailable behavior.
- JSON intake callable/CLI.
- SQLite case-store schema for cases, evidence sources, audit events, and schema migration marker.
- Documentation and review handoff.

Known Stage 1 limits:

- No real EWF byte parsing yet.
- No partition or filesystem parsing yet.
- No UI yet.
- No automatic persistence from intake command to SQLite yet.
- No real evidence needed for tests.

## Stage 2 Detailed Targets

Stage 2 goal: move from "we can identify and describe an evidence source" to "we can discover volumes and browse a small filesystem view through a safe backend boundary."

Targets:

- Decide the Stage 2 fixture strategy for raw images, EWF images, and/or generated tiny filesystems.
- Add an image/byte-stream abstraction that can be backed by a local raw fixture and later by real EWF readers.
- Add a volume discovery boundary that can report partitions/volumes or a single whole-disk/whole-image volume for simple fixtures.
- Add a filesystem adapter boundary, preferably pytsk3-compatible, with stub/fallback behavior when native dependencies are missing.
- Browse one supported filesystem path/tree from a tiny non-sensitive fixture or stub adapter.
- Return structured file metadata: path, type, size, timestamps where available, allocation/deleted state when supported, and source provenance.
- Add tests that do not require private evidence or large images.
- Keep all evidence/image reads read-only.

Stage 2 acceptance criteria:

- A documented backend command/callable can list volume/filesystem information for a test fixture or stubbed filesystem.
- Unsupported or missing native dependencies produce structured status, not raw crashes.
- Tests run without private evidence.
- Stage 2 docs clearly state which behavior is real fixture-backed and which remains stubbed.

Stage 2 status: complete at the documentation/review-handoff level as of 2026-07-09.

Implemented:

- Fixture/dependency strategy for stubs, tiny generated files, and optional local-only forensic fixtures.
- Read-only `LocalFileImageStream` for tiny local files and bounded byte reads.
- Whole-image volume discovery boundary for readable non-empty image streams.
- Filesystem adapter boundary with deterministic stub entries and dependency-safe `pytsk3` skeleton behavior.
- Backend directory listing/file metadata callable over adapter entries.
- Bounded raw/text/hex preview callable over explicit preview-provider bytes.

Known Stage 2 limits:

- No real EWF byte parsing or image verification.
- No real partition table parsing.
- No real filesystem parsing or real file extraction.
- No UI or executable packaging.
- No export/recovery, hashing/signature analysis, search/timeline, or reporting.
- No automatic case-store persistence for Stage 2 API results.
- `pyewf`, libewf, `pytsk3`, and The Sleuth Kit remain optional and are not required for default tests.

Stage 3 builds from the Stage 2 backend result shapes and adds export/recovery foundations without assuming deleted-file recovery is available until a real filesystem adapter exposes it.

## Stage 3 Detailed Targets

Stage 3 goal: add safe file export foundations so a selected file-like item can be written out with provenance, hashes, and audit context.

Targets:

- Define export request/result structures.
- Add an export service that writes to an examiner-selected output directory, never evidence paths.
- Support exporting bytes from a stub or fixture-backed file entry.
- Compute output hashes, at minimum SHA-256, with MD5/SHA-1 deferred to the broader hash-analysis stage if needed.
- Record source provenance in an export manifest.
- Add audit-event integration through the case store when a case/evidence id is provided.
- Document deleted-file recovery as later/conditional behavior unless the Stage 2 filesystem adapter truly exposes deleted entries.

Stage 3 acceptance criteria:

- A documented backend command/callable can export a selected fixture/stub file to an output folder.
- Export output includes a manifest with source path/id, evidence id when available, output path, byte count, hash, and timestamp.
- Tests prove exports do not write into evidence/source fixture directories.
- Deleted-file recovery limitations are explicit.

Stage 3 planning note, 2026-07-13:

- The first Stage 3 VS Code implementation chat should start with `prompts/vscode-agent/2026-07-13-stage-3-familiarization.md`.
- S3-T01 through S3-T06 are reviewed and done.
- The S3-T06 implementation prompt is `prompts/vscode-agent/2026-07-14-s3-t06-stage-3-docs-review-handoff.md`.
- S3-T04 adds optional audit events only when explicit audit context is supplied. Source provenance ids alone must not trigger database writes.
- S3-T05 remains documentation/planning-only because no reviewed adapter exposes deleted entries plus recoverable deleted-file bytes.
- S3-T01 should define export contracts only. It should not write exported files, compute real hashes, add audit persistence, or start deleted recovery.
- S3-T03 verifies written export artifacts with SHA-256 and on-disk byte counts only; broader hash/signature analysis remains Stage 4.
- Stage 3 must keep preview, metadata, and export content separated: rendered preview output is not an export byte source.
- Stage 4 should build hash/signature contracts on explicit content providers, avoid preview text/hex as source content, avoid whole-image verification claims without adapter support, keep known-file matching fixture-sized/in-memory, and defer persistence until result contracts are reviewed.

## Stage 4 Detailed Targets

Stage 4 goal: add reproducible file hash and signature-analysis foundations after Stage 3 has reviewed export/content-source contracts.

Stage 4 must begin from an uncomfortable but useful truth: the project does not yet have real filesystem file-content extraction. Hash/signature results must therefore be explicit about the content provider they analyze and must not imply real evidence-derived bytes unless a reviewed adapter supplies them.

Targets:

- Confirm the allowed Stage 4 content sources and fixture strategy before implementation.
- Define hash/signature request, result, warning, and status structures.
- Calculate per-file hashes from explicit content providers, starting with SHA-256 and adding MD5/SHA-1 where useful for forensic comparison workflows.
- Preserve provenance for every hash/signature result: source path, evidence id when available, volume id, file id/path, content provider, byte count, parser/source status, and timestamp.
- Add file signature/magic-byte detection for bounded bytes.
- Add extension mismatch flags only when metadata and detected signature are both available.
- Keep known-file database matching optional and fixture-sized for default tests.
- Avoid whole-image verification claims unless the evidence adapter exposes the necessary bytes and expected verification values.

Stage 4 acceptance criteria:

- Hash/signature tests run without private evidence, large fixtures, native forensic dependencies, or network access.
- Hash results are JSON-serializable and preserve byte count, algorithm, digest, status, and provenance.
- Signature results distinguish detected type, unknown type, unsupported content, and insufficient bytes through structured statuses.
- Documentation separates per-file provider-backed hashing from real evidence-image verification.

Stage 4 review-agent handoff:

- The Stage 4 coding agent should start with `prompts/vscode-agent/2026-07-14-stage-4-familiarization.md`.
- The Stage 4 review/research side has read the project, inspected tests/code, run `python -m pytest`, and recorded the S4-T00 risk audit.
- Detailed Stage 4 tickets now live under `tickets/stage-4/`; S4-T01 contract-only implementation is reviewed and done.
- S4-T02 provider-backed hashing, S4-T03 file signature detection, S4-T04 extension mismatch rules, and S4-T05 fixture-sized known-file matching are reviewed and done.
- A rough Stage 5 search/timeline ticket plan now lives under `tickets/stage-5/`.
- The main carryover risk is the missing real evidence-backed content path. Stage 4 can build provider-backed hash/signature contracts, but future stages need a reality anchor before search, reports, timeline, or UI work imply real forensic extraction.

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

## VS Code Codex Familiarization Prompt

```text
You are joining the EncaseSubstituteTool project as the implementation agent. Before editing code, familiarize yourself with the project structure and goals.

Read these files first:
- readme.md for orientation.
- Goal.md for product goal, MVP scope, Stage 1 targets, and the starter implementation prompt.
- research.md for the research index.
- research/01-encase-functionality.md through research/07-risks-assumptions.md for topic-specific research.
- functionality.md for feature inventory.
- plan.md for the working task plan.
- progression.md for the development journal.
- review.md for review priorities and findings.
- workflow.md for how the implementation agent, research/review agent, and any subagents should coordinate.

Current expected focus:
- Stage 1 only: E01 intake spike.
- Do not build a full EnCase replacement or a polished UI yet.
- Work inside app/.
- Keep evidence access read-only.
- Make dependency failures clear.
- Add tests that do not require real evidence.

After reading, summarize your understanding briefly, list the first files you plan to create or modify, then begin implementation only if the plan matches Stage 1.
```
