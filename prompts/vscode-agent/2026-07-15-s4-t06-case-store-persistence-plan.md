# 2026-07-15 - S4-T06 Case-Store Persistence Plan Prompt

Use this prompt to hand S4-T06 to the Stage 4 VS Code implementation agent.

```text
Implement ticket S4-T06: Case-Store Persistence Plan.

Before editing, read these files:
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

Context:
- S4-T01 through S4-T05 are reviewed and done.
- Stage 4 analysis result shapes are stable enough to plan persistence, but there is still no reviewed analysis workflow/API/job layer that should own persistence.
- The current SQLite case store has only `cases`, `evidence_sources`, `audit_events`, and `schema_migrations`.
- Stage 3 export auditing writes only when explicit `ExportAuditContext` is supplied.
- S4-T06 is planning/documentation-only. Do not implement schema or behavior.

Before implementing:
- Summarize your understanding of the current true project state.
- List the files you expect to modify.
- State that this ticket documents a persistence decision and future requirements only.
- If you believe a schema/code change is needed, pause and explain it instead of implementing it.

Task:
- Keep S4-T06 planning/documentation-only.
- Review the existing case-store schema and Stage 3 explicit export audit pattern.
- Document that actual analysis-result persistence is deferred beyond S4-T06.
- Document why future persistence should be explicit opt-in, similar to `ExportAuditContext`.
- Document future persistence context, likely including:
  - SQLite connection;
  - explicit case id;
  - optional evidence id;
  - optional actor/examiner;
  - optional analysis job id;
  - policy for failed/partial/not-evaluated results;
  - caller intent to persist.
- Document future table requirements:
  - stable result id;
  - case id and evidence id;
  - analysis type;
  - source provenance JSON;
  - content-source identity JSON;
  - source kind and synthetic/generated flags;
  - status code and status JSON;
  - full result JSON with `schema_version`;
  - warnings JSON;
  - created/completed/persisted timestamps;
  - parser/provider name and version fields where available.
- Document future index/query needs for case/evidence id, file id/path, analysis type, status, source kind, hash digests, detected signatures, mismatch values, and known-file categories.
- Document recommended future schema direction:
  - parent `analysis_results` table for shared provenance/status/result JSON;
  - optional child/index tables for hash digests, signature detections, extension mismatch flags, and known-file matches.
- State clearly that embedded `case_id` or `evidence_id` in analysis provenance must not cause automatic writes.
- State clearly that standalone `hash_file_content()`, `detect_file_signature()`, `evaluate_extension_mismatch()`, and `match_known_file_hashes()` calls must remain non-persistent.
- Update requested docs and ticket status to Review.
- Run python -m pytest and report the exact result.

Likely files to modify:
- tickets/stage-4/S4-T06-case-store-persistence-plan.md
- tickets/stage-4/README.md
- app/backend/case_store/README.md
- app/backend/api/README.md
- app/backend/forensic_core/README.md
- functionality.md
- plan.md
- progression.md
- review.md
- readme.md
- Goal.md

Scope boundaries:
- Do not modify `app/backend/case_store/schema.py`.
- Do not modify `app/backend/case_store/__init__.py`.
- Do not modify `app/backend/forensic_core/content_analysis.py`.
- Do not modify `app/backend/api/file_export.py`.
- Do not modify tests unless a docs-only reference truly requires it.
- Do not add migrations, tables, case-store helper functions, API wrappers, automatic persistence, background jobs, search/timeline/reporting/UI, external known-file dataset storage, real parser work, native dependencies, commit, or push.
- Do not change S4-T01 through S4-T05 behavior.

Verification:
- Run `python -m pytest`.
- Report the exact command and result.

Final handoff:
- Summarize documentation files changed.
- Summarize the persistence decision and future requirements.
- Report the exact pytest command and result.
- State limitations and deferred work.
- Confirm you did not implement schema or persistence and did not begin S4-T07 or Stage 5 work.

Stop after S4-T06 and hand off for review.
```
