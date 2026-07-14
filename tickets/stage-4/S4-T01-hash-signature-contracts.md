# S4-T01 - Hash And Signature Contracts

Status: Done

Stage: Stage 4 - Hash and signature foundations

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Define Stage 4 hash/signature analysis request, result, provenance, provider identity, status, and warning contracts before implementing broad calculation behavior.

This ticket is contract-only. It may add serialization helpers and focused tests, but it must not compute production hashes, detect file signatures, write persistence rows, or start search/timeline work.

## Context To Read First

- `prompts/vscode-agent/2026-07-14-stage-4-familiarization.md`
- `prompts/stage-4-onboarding/stage-4-review-agent-familiarization-prompt.md`
- `tickets/stage-4/README.md`
- `tickets/stage-4/S4-T00-review-agent-risk-audit.md`
- `Goal.md`
- `plan.md`
- `functionality.md`
- `progression.md`
- `review.md`
- `workflow.md`
- `app/backend/forensic_core/export_manifest.py`
- `app/backend/api/file_export.py`
- `app/backend/api/file_preview.py`
- `app/backend/forensic_core/filesystem_adapter.py`
- `app/tests/test_export_manifest.py`
- `app/tests/test_file_export.py`
- `app/tests/test_file_preview.py`
- `app/fixtures/README.md`

## Target Files/Folders

Likely files to create or modify:

- `app/backend/forensic_core/content_analysis.py` or another clearly named Stage 4 analysis contract module.
- `app/backend/forensic_core/__init__.py`
- `app/tests/test_content_analysis_contracts.py`
- `app/backend/forensic_core/README.md`
- `app/backend/api/README.md` if API boundary notes need clarification.
- `app/fixtures/README.md` if content-source terminology needs clarification.
- `functionality.md`
- `plan.md`
- `progression.md`
- `review.md`
- `tickets/stage-4/README.md`
- `tickets/stage-4/S4-T01-hash-signature-contracts.md`

Do not modify export behavior, preview behavior, filesystem parsing, or case-store schema in this ticket unless a small import/export list update is needed.

## Required Work

- Define a Stage 4 schema version such as `stage4.content_analysis.v1`.
- Define source provenance for per-file analysis. It should preserve:
  - source path;
  - evidence id and case id when available;
  - volume id, volume offset, and volume length when known;
  - file id, file path, file name, entry type, allocation/deleted state, filesystem type, adapter name, read-only assertion, and timestamps when available.
- Define explicit content-source/provider identity for analysis bytes. It should record:
  - provider name;
  - source kind, such as `synthetic`, `generated_fixture`, `local_stream`, `export_provider`, or future `real_parser`;
  - read-only assertion;
  - synthetic/generated flags or equivalent fields;
  - source content size when known;
  - parser/source status;
  - parser/source name and version when known.
- Define structured status and warning objects with stable `code`, `ok`, and `message` fields for statuses.
- Define request/result contracts for hash analysis without doing real calculation yet. Include:
  - requested algorithms;
  - bytes analyzed as nullable placeholder;
  - per-algorithm digest placeholders;
  - status and warnings;
  - timestamp.
- Define request/result contracts for signature analysis without doing real detection yet. Include:
  - max bytes requested;
  - bytes inspected as nullable placeholder;
  - detected type/signature fields as nullable placeholders;
  - status and warnings;
  - timestamp.
- Define a top-level combined analysis result only if it reduces duplication. Keep hash and signature concepts separable.
- Provide `to_dict()` and JSON serialization helpers consistent with existing project style.
- Use UTC ISO timestamps ending in `Z`.

## Suggested Status And Warning Names

Use these names unless the implementation discovers a clearer local pattern:

- `analysis_not_started`
- `ok`
- `content_source_unavailable`
- `metadata_only_source`
- `preview_rendering_not_allowed`
- `invalid_analysis_request`
- `hash_not_computed`
- `signature_not_checked`
- `unsupported_algorithm`
- `insufficient_bytes`
- `unknown_signature`
- `synthetic_content`
- `generated_fixture_content`

S4-T01 should mainly define names and placeholder states. Later tickets can add additional statuses when behavior requires them.

## Acceptance Criteria

- Contract structures are importable and JSON-serializable.
- Source provenance can be built from a Stage 2-style file entry without mutating it.
- Content-source identity can honestly label synthetic, generated fixture, local-stream, and future real-parser bytes.
- Hash result placeholders do not imply hashes were computed.
- Signature result placeholders do not imply type detection occurred.
- Contracts keep preview rendering, export-output verification, per-file analysis, and whole-image verification separate.
- Default tests pass without real evidence, native dependencies, network access, or large fixtures.

## Test Expectations

Add focused tests under `app/tests/`.

Tests should cover:

- status and warning serialization;
- source provenance copied from a Stage 2-style file entry;
- content-source identity for synthetic and generated/local fixture examples;
- hash request/result placeholder serialization;
- signature request/result placeholder serialization;
- UTC timestamp format;
- no bytes objects or non-JSON values in `to_dict()` output.

Run:

```powershell
python -m pytest
```

## Documentation Updates

- Update `app/backend/forensic_core/README.md` with the Stage 4 contract boundary.
- Update `functionality.md` if feature status text changes.
- Update `plan.md`, `progression.md`, and `review.md`.
- Update this ticket and `tickets/stage-4/README.md` to `Review` when implementation is complete.

## Review Checklist

- No production hash calculation was added.
- No file signature detection was added.
- No preview-rendered text/hex is used as source content.
- No metadata-only filesystem entry is treated as byte-bearing.
- No export-output hash verification behavior was changed.
- No whole-image verification claim was added.
- No case-store persistence, known-file matching, search, timeline, UI, real parser work, deleted recovery, or carving was added.
- Tests prove contract serialization and provenance honesty.

## Implementation Handoff - 2026-07-14

- Added `app/backend/forensic_core/content_analysis.py` with Stage 4 contract-only status, warning, source-provenance, content-source identity, hash request/result, digest placeholder, signature request/result, and JSON helper structures.
- Added exports from `app.backend.forensic_core`.
- Added `app/tests/test_content_analysis_contracts.py` covering status/warning serialization, Stage 2 file-entry provenance copying without mutation, synthetic/generated/future-real content-source labels, hash placeholders, signature placeholders, UTC timestamp format, and JSON-safe output.
- Updated backend, fixture, planning, review, progression, and ticket docs to mark S4-T01 ready for review.
- No hashes are computed, no signatures are detected, no preview-rendered output is analyzed, no metadata-only entry is treated as byte-bearing, and Stage 3 export verification behavior is unchanged.
- Final test run: `python -m pytest` reported 106 passed in 4.51s.

## Review - 2026-07-14

Result: approved.

Findings:

- No blocking issues found.
- The implementation stayed contract-only and did not compute hashes, detect signatures, read provider bytes, use preview output as source content, treat metadata as byte-bearing, change export verification, add persistence, start search/timeline, or add parser/native dependency work.
- Contract structures are JSON-friendly and preserve Stage 2-style source provenance plus explicit analysis content-source identity.
- Tests cover status/warning serialization, file-entry provenance copying without mutation, synthetic/generated/future-real source labels, hash placeholders, signature placeholders, UTC timestamp format, and JSON-safe output.

Review verification:

- `python -m pytest`: 106 passed in 4.82s.

## Handoff Prompt

```text
Implement ticket S4-T01: Hash And Signature Contracts.

Before editing, read:
- prompts/vscode-agent/2026-07-14-stage-4-familiarization.md
- tickets/stage-4/README.md
- tickets/stage-4/S4-T00-review-agent-risk-audit.md
- tickets/stage-4/S4-T01-hash-signature-contracts.md
- Goal.md
- plan.md
- functionality.md
- progression.md
- review.md
- workflow.md
- app/backend/forensic_core/export_manifest.py
- app/backend/api/file_export.py
- app/backend/api/file_preview.py
- app/backend/forensic_core/filesystem_adapter.py
- app/fixtures/README.md

Task:
- Add Stage 4 hash/signature analysis contract structures only.
- Preserve source provenance and explicit analysis content-source identity.
- Add JSON-friendly status, warning, request, and result shapes.
- Add focused dependency-free tests.
- Update requested docs and ticket status.
- Run python -m pytest and report the exact result.

Scope boundaries:
- Do not compute hashes yet.
- Do not detect signatures yet.
- Do not use preview-rendered text or hex as source content.
- Do not treat filesystem metadata as byte-bearing.
- Do not change export verification.
- Do not add known-file matching, persistence, search, timeline, UI, real parser work, deleted recovery, carving, native dependencies, commit, or push.

Stop after S4-T01 and hand off for review.
```
