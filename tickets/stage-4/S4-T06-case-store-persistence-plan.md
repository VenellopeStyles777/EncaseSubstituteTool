# S4-T06 - Case-Store Persistence Plan

Status: Done

Stage: Stage 4 - Hash and signature foundations

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Document the Stage 4 decision for case-store persistence of hash, signature, extension mismatch, and known-file matching results.

S4-T06 is planning/documentation-only. Do not implement SQLite schema migrations, persistence helpers, API wrappers, background jobs, or automatic writes in this ticket.

## Decision Direction

Defer analysis-result persistence implementation beyond S4-T06.

Reasoning:

- The existing case store is still the minimal Stage 1 schema: `cases`, `evidence_sources`, `audit_events`, and `schema_migrations`.
- Stage 3 export audit integration deliberately writes only when an explicit `ExportAuditContext` is supplied.
- Stage 4 result contracts are now reviewed, but there is no reviewed analysis job/workflow/API layer that should own persistence context, retries, deduplication, or examiner intent.
- The project still lacks real evidence-backed filesystem file-content extraction, so persisted analysis rows must not make synthetic/provider-backed results look stronger than they are.

This ticket should record the future persistence requirements and blockers so S4-T07 can close Stage 4 honestly, and so Stage 5/6 can build search/timeline/reporting on provenance-rich records later.

## Context To Read First

- `prompts/vscode-agent/2026-07-14-stage-4-familiarization.md`
- `tickets/stage-4/README.md`
- `tickets/stage-4/S4-T00-review-agent-risk-audit.md`
- `tickets/stage-4/S4-T01-hash-signature-contracts.md`
- `tickets/stage-4/S4-T02-provider-backed-hashing.md`
- `tickets/stage-4/S4-T03-file-signature-detection.md`
- `tickets/stage-4/S4-T04-extension-mismatch-rules.md`
- `tickets/stage-4/S4-T05-known-file-matching.md`
- `tickets/stage-4/S4-T06-case-store-persistence-plan.md`
- `Goal.md`
- `readme.md`
- `plan.md`
- `functionality.md`
- `progression.md`
- `review.md`
- `workflow.md`
- `app/backend/README.md`
- `app/backend/api/README.md`
- `app/backend/case_store/README.md`
- `app/backend/case_store/schema.py`
- `app/backend/api/file_export.py`
- `app/backend/forensic_core/README.md`
- `app/backend/forensic_core/content_analysis.py`
- `app/tests/test_case_store_schema.py`
- `app/tests/test_file_export.py`
- `app/tests/test_content_analysis_hashing.py`
- `app/tests/test_content_analysis_signatures.py`
- `app/tests/test_content_analysis_extension_mismatch.py`
- `app/tests/test_content_analysis_known_files.py`

## Target Files/Folders

Likely files to modify:

- `tickets/stage-4/S4-T06-case-store-persistence-plan.md`
- `tickets/stage-4/README.md`
- `app/backend/case_store/README.md`
- `app/backend/api/README.md`
- `app/backend/forensic_core/README.md`
- `functionality.md`
- `plan.md`
- `progression.md`
- `review.md`
- `readme.md`
- `Goal.md`

Do not modify these files for behavior in this ticket:

- `app/backend/case_store/schema.py`
- `app/backend/case_store/__init__.py`
- `app/backend/api/file_export.py`
- `app/backend/forensic_core/content_analysis.py`
- `app/tests/`

If you believe code or schema changes are necessary, pause and explain the proposed change instead of implementing it.

## Required Work

- Review the existing case-store schema and Stage 3 export audit pattern.
- Document that S4-T06 defers actual analysis-result persistence implementation.
- Document why persistence should remain explicit opt-in in a later ticket, similar to `ExportAuditContext`.
- Document the minimum future persistence context, likely including:
  - SQLite connection;
  - explicit case id;
  - optional evidence id;
  - optional actor/examiner;
  - optional analysis job id;
  - a policy for failed/partial/not-evaluated results;
  - caller intent to persist.
- Document future table requirements for result persistence, including:
  - stable result id;
  - case id and evidence id;
  - analysis type: hash, signature, extension mismatch, known-file match;
  - source provenance JSON;
  - content-source identity JSON;
  - source kind and synthetic/generated flags;
  - status code and status JSON;
  - full result JSON with `schema_version`;
  - warnings JSON;
  - created/completed/persisted timestamps;
  - parser/provider name and version fields where available.
- Document future index/query needs without implementing search:
  - case/evidence id;
  - file id/path;
  - analysis type;
  - status code;
  - source kind;
  - hash algorithm/digest;
  - detected type/signature;
  - extension mismatch value;
  - known-file matched/category.
- Document the recommended future schema direction:
  - a parent `analysis_results` table for shared provenance/status/result JSON;
  - optional child/index tables for hash digests, signature detections, extension mismatch flags, and known-file matches when search/timeline work needs efficient queries.
- Document explicit constraints:
  - no automatic writes from `case_id`/`evidence_id` embedded in source provenance;
  - no persistence from standalone `hash_file_content()`, `detect_file_signature()`, `evaluate_extension_mismatch()`, or `match_known_file_hashes()` calls;
  - no persistence of external known-file datasets or NSRL-scale data;
  - persisted rows must preserve synthetic/generated/provider-backed labels.
- Update Stage 4 planning/status docs and this ticket to `Review` when complete.

## Out Of Scope

- SQLite schema migrations.
- New tables.
- New case-store helper functions.
- New API wrappers.
- Automatic persistence from analysis functions.
- Background jobs or queues.
- Search/timeline/reporting/UI.
- External known-file dataset storage.
- Real parser work or native dependencies.
- Stage 5 work.

## Acceptance Criteria

- S4-T06 is explicitly planning/documentation-only.
- Docs state that analysis-result persistence is deferred beyond S4-T06.
- Future persistence requirements preserve source provenance, content-source identity, source kind, synthetic/generated labels, statuses, warnings, and timestamps.
- Future persistence is explicit opt-in and cannot happen merely because result provenance contains `case_id` or `evidence_id`.
- Future schema direction is clear enough for a later persistence implementation ticket.
- Existing case-store schema and backend behavior are unchanged.
- Default tests still pass.

## Test Expectations

Run:

```powershell
python -m pytest
```

No new tests are expected for this planning-only ticket. If code changes become necessary, stop first and explain why.

## Review Checklist

- No behavior/schema changes were made.
- S4-T06 does not create analysis persistence tables or helpers.
- S4-T06 does not add automatic persistence from analysis APIs.
- The future plan preserves uncertainty around synthetic/generated/provider-backed bytes.
- The future plan keeps search/timeline/reporting out of Stage 4.
- The future plan is compatible with S4-T01 through S4-T05 result shapes.

## Implementation Notes

- S4-T06 remains planning/documentation-only. No SQLite schema, migration, helper, API wrapper, analysis behavior, or test file was changed.
- The persistence decision is to defer actual analysis-result persistence until a later reviewed workflow/job/API layer can supply explicit caller intent and persistence context.
- Future persistence should follow the Stage 3 `ExportAuditContext` precedent: writes require an explicit SQLite connection, case id, optional evidence id, optional actor/examiner, optional analysis job id, policy for failed/partial/not-evaluated results, and an explicit intent to persist.
- Future persistence must preserve the full Stage 4 result JSON with `schema_version`, source provenance JSON, content-source identity JSON, source kind, synthetic/generated flags, status JSON, warnings JSON, timestamps, and provider/parser name/version fields.
- Recommended future schema direction is a parent `analysis_results` table plus optional child/index tables for hash digests, signature detections, extension mismatch flags, and known-file matches.
- Embedded `case_id` or `evidence_id` in analysis provenance must not cause automatic writes. Standalone calls to `hash_file_content()`, `detect_file_signature()`, `evaluate_extension_mismatch()`, and `match_known_file_hashes()` must remain non-persistent.
- External known-file datasets, NSRL-scale storage, search/timeline/reporting, UI, background jobs, real parser work, and Stage 5 work remain deferred.

## Review Result - 2026-07-15

- Approved and marked done.
- No blocking findings found.
- Reviewer confirmed S4-T06 stayed planning/documentation-only.
- Reviewer confirmed no SQLite schema migration, new table, persistence helper, API wrapper, automatic persistence path, background job, analysis behavior change, or test change was added.
- Reviewer confirmed the future persistence plan is explicit opt-in and follows the Stage 3 `ExportAuditContext` precedent.
- Reviewer confirmed embedded `case_id` or `evidence_id` values in analysis provenance do not trigger writes, and standalone Stage 4 helper calls remain non-persistent.
- Reviewer confirmed future persistence requirements preserve source provenance, content-source identity, source kind, synthetic/generated labels, statuses, warnings, timestamps, full result JSON with `schema_version`, and provider/parser names and versions.
- Reviewer confirmed search/timeline/reporting, UI, external known-file dataset storage, real parser work, native dependencies, S4-T07, and Stage 5 work remain deferred.
- Reviewer verification: `python -m pytest` passed with 152 tests.

## Handoff Prompt

```text
Implement ticket S4-T06: Case-Store Persistence Plan.

Before editing, read:
- prompts/vscode-agent/2026-07-14-stage-4-familiarization.md
- tickets/stage-4/README.md
- tickets/stage-4/S4-T00-review-agent-risk-audit.md
- tickets/stage-4/S4-T01-hash-signature-contracts.md
- tickets/stage-4/S4-T02-provider-backed-hashing.md
- tickets/stage-4/S4-T03-file-signature-detection.md
- tickets/stage-4/S4-T04-extension-mismatch-rules.md
- tickets/stage-4/S4-T05-known-file-matching.md
- tickets/stage-4/S4-T06-case-store-persistence-plan.md
- Goal.md
- readme.md
- plan.md
- functionality.md
- progression.md
- review.md
- workflow.md
- app/backend/README.md
- app/backend/api/README.md
- app/backend/case_store/README.md
- app/backend/case_store/schema.py
- app/backend/api/file_export.py
- app/backend/forensic_core/README.md
- app/backend/forensic_core/content_analysis.py
- app/tests/test_case_store_schema.py
- app/tests/test_file_export.py
- app/tests/test_content_analysis_hashing.py
- app/tests/test_content_analysis_signatures.py
- app/tests/test_content_analysis_extension_mismatch.py
- app/tests/test_content_analysis_known_files.py

Task:
- Keep S4-T06 planning/documentation-only.
- Review the existing case-store schema and Stage 3 explicit export audit pattern.
- Document that actual analysis-result persistence is deferred beyond S4-T06.
- Document future explicit opt-in persistence context, future table requirements, future index/query needs, and the recommended parent/child table direction.
- Preserve the key forensic guardrail: persisted analysis results must retain source provenance, content-source identity, source kind, synthetic/generated labels, statuses, warnings, timestamps, and full result JSON.
- State clearly that embedded `case_id` or `evidence_id` in analysis provenance must not cause automatic writes.
- Update requested docs and ticket status to Review.
- Run python -m pytest and report the exact result.

Scope boundaries:
- Do not modify `app/backend/case_store/schema.py`.
- Do not add migrations, tables, case-store helper functions, API wrappers, automatic persistence, background jobs, search/timeline/reporting/UI, external known-file dataset storage, real parser work, native dependencies, commit, or push.
- Do not change S4-T01 through S4-T05 behavior.

Stop after S4-T06 and hand off for review.
```
