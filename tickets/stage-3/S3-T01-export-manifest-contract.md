# S3-T01 - Export Result And Manifest Contract

Status: Done

Stage: Stage 3 - Export and recovery foundation

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Define Stage 3 export contract structures before any export file writing exists.

This ticket should establish JSON-friendly request/result/manifest/status/warning/content-source shapes that later tickets can use for safe fixture/stub/provider-backed exports. It must keep export content separate from Stage 2 preview rendering and from metadata-only filesystem entries.

## Context To Read First

- `prompts/vscode-agent/2026-07-13-stage-3-familiarization.md`
- `prompts/stage-3-onboarding/stage-2-conclusion-and-stage-3-needs.md`
- `prompts/stage-3-onboarding/project-review-agent-memo.md`
- `Goal.md`
- `plan.md`
- `functionality.md`
- `progression.md`
- `review.md`
- `workflow.md`
- `tickets/README.md`
- `tickets/stage-3/README.md`
- `app/backend/api/file_preview.py`
- `app/backend/api/directory_listing.py`
- `app/backend/forensic_core/filesystem_adapter.py`
- `app/backend/forensic_core/README.md`
- `app/backend/api/README.md`
- `app/fixtures/README.md`

## Target Files/Folders

Likely files to create or modify:

- `app/backend/forensic_core/export_manifest.py`
- `app/backend/forensic_core/__init__.py`
- `app/tests/test_export_manifest.py`
- `app/backend/forensic_core/README.md`
- `app/backend/api/README.md` if API boundary notes need clarification
- `app/fixtures/README.md` if content-source wording needs clarification
- `functionality.md`
- `plan.md`
- `progression.md`
- `review.md`
- `tickets/stage-3/README.md`
- `tickets/stage-3/S3-T01-export-manifest-contract.md`

Do not create an export service yet. Do not create output files.

## Required Work

- Add a Stage 3 export manifest/core contract module that follows the existing backend style: small dataclasses, structured statuses/warnings, and `to_dict()` methods.
- Define a schema version such as `stage3.export_manifest.v1`.
- Define an export request shape for later service use. It should include, at minimum:
  - source path;
  - destination directory or requested destination path;
  - file id;
  - file path;
  - file name;
  - volume id;
  - volume offset/length when known;
  - filesystem type and adapter/source name when known;
  - evidence id and case id as optional context fields;
  - requested export mode or source kind if useful;
  - read-only source assertion;
  - caller/examiner-selected destination assertion or equivalent field.
- Define an explicit export content-source/provider identity shape. It should record:
  - provider name;
  - provider type/source kind, for example `stub`, `generated_fixture`, `provider`, or later `real_parser`;
  - read-only assertion;
  - whether bytes are synthetic;
  - source content size when known;
  - parser/adapter/source status when known.
- Define an export status shape with `code`, `ok`, and `message`.
- Define export warnings with `code`, `message`, optional path, and optional source/component.
- Define an export result shape that can represent future success and failure without writing files in this ticket. It should include:
  - schema version;
  - status;
  - source provenance;
  - destination/output path fields;
  - manifest path field, nullable for S3-T01;
  - content-source/provider identity;
  - byte count fields, initially nullable or placeholder-ready;
  - hash fields, initially empty/nullable placeholders;
  - UTC timestamp;
  - read-only/source-safety assertions;
  - warnings.
- Define an export manifest shape that mirrors the result fields needed to explain an exported artifact later. It should be JSON-serializable and honest about synthetic/provider-backed bytes.
- Provide helper methods or functions for stable dictionary/JSON serialization. Keep this simple and consistent with existing code.
- Use UTC ISO timestamps ending in `Z`, consistent with the case-store helper style.
- Add exports to `app/backend/forensic_core/__init__.py` if that matches existing package style.

## Status Names

Use these names unless a clearer local pattern emerges:

- `planned`: contract/result created before any write attempt.
- `ok`: reserved for later successful export service tickets; S3-T01 may use it only in a pure serialization fixture if no write is implied.
- `export_not_started`: no export write was attempted.
- `content_source_unavailable`: no raw export bytes are available from an explicit provider/source.
- `invalid_export_request`: required request/provenance fields are missing or invalid.
- `destination_not_checked`: destination safety has not been evaluated yet.
- `hash_not_computed`: hash placeholders exist but hashing is deferred.

S3-T01 should not introduce destination-overlap enforcement, real hashing, audit persistence, or file writes. Those belong to later tickets.

## Acceptance Criteria

- Export request/result/manifest/content-source/status/warning structures exist and are importable.
- Structures serialize to JSON-friendly dictionaries without bytes objects or non-serializable values.
- Result and manifest structures preserve source provenance from a Stage 2-style filesystem entry.
- Content-source/provider identity can clearly label synthetic stub/provider-backed bytes versus future real parser bytes.
- Hash and byte-count fields are present but do not imply hashing or file writing has occurred.
- UTC timestamp fields are present and deterministic enough for tests.
- Tests prove that a manifest/result can represent `export_not_started`, `content_source_unavailable`, and placeholder hash/byte-count state.
- No files are exported or written by the contract module.

## Test Expectations

Add focused tests under `app/tests/`.

Tests should cover:

- result/manifest dictionary serialization;
- JSON serialization through `json.dumps`;
- source provenance copied from a Stage 2-style file entry;
- content-source identity for synthetic stub/provider content;
- nullable output/manifest/hash/byte-count fields before export exists;
- warning serialization;
- `ok` property behavior for status objects;
- UTC timestamp format, or injectable timestamp if that keeps tests deterministic.

Run:

```powershell
python -m pytest
```

Default tests must not require native dependencies, real evidence, binary fixtures, network access, or output directories outside the workspace.

## Documentation Updates

- Update `app/backend/forensic_core/README.md` with the new export contract and its limits.
- Update `functionality.md`: keep `Export manifest contract` as Stage 3, move status to `In Progress` or `Done` as appropriate, and keep Manual Test as `Untested`.
- Update `plan.md` if S3-T01 status changes.
- Update `progression.md` with completed/learned/blocked/next notes.
- Add a handoff or review note to `review.md`.
- Update `tickets/stage-3/README.md` and this ticket status to `Review` when implementation is complete.

## Review Checklist

- S3-T01 did not write export files or manifests to disk.
- S3-T01 did not use preview-rendered text/hex as export bytes.
- S3-T01 did not treat filesystem metadata entries as byte-bearing objects.
- S3-T01 did not implement hashing, audit integration, deleted recovery, UI, search, reporting, real EWF parsing, real partition parsing, or real filesystem parsing.
- Result and manifest shapes make source provenance and synthetic/provider-backed content explicit.
- Default tests pass without native dependencies or real evidence.

## Handoff Prompt

```text
Implement ticket S3-T01: Export Result And Manifest Contract.

Before editing, read these files:
- prompts/vscode-agent/2026-07-13-stage-3-familiarization.md
- prompts/stage-3-onboarding/stage-2-conclusion-and-stage-3-needs.md
- prompts/stage-3-onboarding/project-review-agent-memo.md
- tickets/stage-3/S3-T01-export-manifest-contract.md
- tickets/stage-3/README.md
- Goal.md
- plan.md
- functionality.md
- progression.md
- review.md
- workflow.md
- app/backend/api/file_preview.py
- app/backend/api/directory_listing.py
- app/backend/forensic_core/filesystem_adapter.py
- app/backend/forensic_core/README.md
- app/backend/api/README.md
- app/fixtures/README.md

Context:
- Stage 2 is complete as a backend foundation.
- Stage 2 filesystem entries are metadata-only.
- Stage 2 preview bytes are synthetic/provider-backed and are not real filesystem extraction.
- Stage 3 must begin with export contracts/manifests before any file writing.
- Export bytes must eventually come from an explicit export content-source/provider boundary, not preview-rendered text/hex and not metadata alone.

Your task:
- Add contract structures for Stage 3 export request/result/manifest/status/warning/content-source identity.
- Keep the implementation dependency-free and JSON-friendly.
- Preserve source provenance fields used by Stage 2 entries: source path, volume id, volume offset/length, file id/path/name, filesystem type, adapter/source name, read-only assertion, allocation/deleted state where relevant.
- Include destination/output/manifest path fields, but keep them nullable or placeholder-ready because this ticket must not write files.
- Include byte count and hash fields, but treat them as not computed placeholders.
- Include UTC timestamp fields.
- Add tests for serialization, provenance, warnings, content-source identity, placeholder byte/hash fields, and non-ok statuses such as export_not_started or content_source_unavailable.
- Update docs and ticket status as requested in the ticket.
- Run python -m pytest and report the exact result.

Scope boundaries:
- Do not implement file export or write manifests.
- Do not compute hashes.
- Do not add destination safety logic beyond placeholder/status fields.
- Do not add case-store audit integration.
- Do not implement deleted-file recovery.
- Do not use preview-rendered text or hex as export bytes.
- Do not add UI, search, reporting, real EWF parsing, real partition parsing, real filesystem parsing, or required native dependencies.
- Do not commit or push.

Final handoff:
- Summarize files changed.
- Summarize structures added.
- Report the exact pytest command and result.
- State limitations and deferred work.
- Confirm you did not begin S3-T02.

Stop after S3-T01 and hand off for review.
```
