# 2026-07-14 - S4-T01 Hash And Signature Contracts Prompt

Use this prompt to hand S4-T01 to the Stage 4 VS Code implementation agent.

```text
Implement ticket S4-T01: Hash And Signature Contracts.

Before editing, read these files:
- prompts/vscode-agent/2026-07-14-stage-4-familiarization.md
- tickets/stage-4/README.md
- tickets/stage-4/S4-T00-review-agent-risk-audit.md
- tickets/stage-4/S4-T01-hash-signature-contracts.md
- Goal.md
- readme.md
- plan.md
- functionality.md
- progression.md
- review.md
- workflow.md
- app/backend/README.md
- app/backend/api/README.md
- app/backend/forensic_core/README.md
- app/fixtures/README.md
- app/backend/forensic_core/export_manifest.py
- app/backend/api/file_export.py
- app/backend/api/file_preview.py
- app/backend/forensic_core/filesystem_adapter.py
- app/tests/test_export_manifest.py
- app/tests/test_file_export.py
- app/tests/test_file_preview.py

Context:
- Stage 1 is complete as a backend intake foundation, not real EWF parsing.
- Stage 2 is complete as a backend volume/filesystem browsing foundation, not real partition or filesystem parsing.
- Stage 3 is complete as a backend fixture/stub export foundation, not real filesystem extraction or deleted recovery.
- Stage 3 export SHA-256 verifies written export artifacts only. It is separate from Stage 4 per-file analysis hashing.
- Preview bytes are separate from export bytes and must not be treated as source content for hashing.
- Current filesystem entries are metadata-only. A filesystem entry by itself is not a byte-bearing object.
- The project still lacks a real evidence-backed file-content path. Stage 4 must not make synthetic provider bytes look like real evidence analysis.

Before implementing:
- Summarize your understanding of the current true project state.
- List the files you expect to create or modify.
- State what bytes this ticket will analyze. For S4-T01 the answer should be: none; this is contract-only.
- If you see a conflict between this prompt and the ticket, pause and explain it instead of broadening scope.

Your task:
- Add Stage 4 hash/signature analysis contract structures only.
- Keep the implementation dependency-free and JSON-friendly.
- Define a Stage 4 schema version such as `stage4.content_analysis.v1`.
- Define structured status and warning objects using stable fields such as `code`, `ok`, and `message` for statuses.
- Define per-file analysis source provenance that can be built from a Stage 2-style file entry and preserves:
  - source path;
  - case id and evidence id when available;
  - volume id, volume offset, and volume length when known;
  - file id, file path, file name, entry type, allocation/deleted state, filesystem type, adapter name, read-only assertion, and timestamps when available.
- Define explicit analysis content-source/provider identity that records:
  - provider name;
  - source kind, such as `synthetic`, `generated_fixture`, `local_stream`, `export_provider`, or future `real_parser`;
  - read-only assertion;
  - synthetic/generated flags or equivalent fields;
  - source content size when known;
  - parser/source status;
  - parser/source name and version when known.
- Define hash analysis request/result contracts without computing hashes yet. Include requested algorithms, nullable bytes-analyzed placeholder, per-algorithm digest placeholders, status, warnings, and timestamp.
- Define signature analysis request/result contracts without detecting signatures yet. Include max bytes requested, nullable bytes-inspected placeholder, detected type/signature placeholders, status, warnings, and timestamp.
- Keep hash and signature concepts separable. Add a combined/top-level result only if it removes real duplication.
- Provide `to_dict()` methods and JSON serialization helpers consistent with the existing dataclass style.
- Use UTC ISO timestamps ending in `Z`, consistent with existing project conventions.
- Add focused tests for contract serialization and provenance honesty.
- Update docs and ticket status as requested in the ticket.
- Run `python -m pytest` and report the exact result.

Suggested status and warning names:
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

Likely files to create or modify:
- app/backend/forensic_core/content_analysis.py
- app/backend/forensic_core/__init__.py
- app/tests/test_content_analysis_contracts.py
- app/backend/forensic_core/README.md
- app/backend/api/README.md if API boundary notes need clarification
- app/fixtures/README.md if content-source terminology needs clarification
- functionality.md
- plan.md
- progression.md
- review.md
- tickets/stage-4/README.md
- tickets/stage-4/S4-T01-hash-signature-contracts.md

Test expectations:
- Status and warning serialization.
- Source provenance copied from a Stage 2-style file entry without mutating the entry.
- Content-source identity for synthetic and generated/local fixture examples.
- Hash request/result placeholder serialization.
- Signature request/result placeholder serialization.
- UTC timestamp format.
- No bytes objects or non-JSON values in `to_dict()` output.

Scope boundaries:
- Do not compute hashes yet.
- Do not detect file signatures yet.
- Do not use preview-rendered text or hex as source content.
- Do not treat filesystem metadata entries as byte-bearing objects.
- Do not change Stage 3 export behavior or export-output SHA-256 verification.
- Do not claim whole-image verification.
- Do not add known-file matching.
- Do not add case-store persistence or schema migrations.
- Do not add search, timeline, reporting, UI, real EWF parsing, real partition parsing, real filesystem parsing, deleted recovery, carving, native dependencies, commit, or push.

Final handoff:
- Summarize files changed.
- Summarize contract structures added.
- Report the exact pytest command and result.
- State limitations and deferred work.
- Confirm you did not begin S4-T02 or any later Stage 4/Stage 5 work.

Stop after S4-T01 and hand off for review.
```
