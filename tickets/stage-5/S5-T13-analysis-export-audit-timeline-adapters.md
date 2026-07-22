# S5-T13 - Analysis, Export, And Audit Timeline Adapters

Status: Draft

Stage: Stage 5 - timeline foundations

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Adapt explicit analysis result timestamps, export manifest timestamps, and case-store audit events into timeline events while keeping evidence-derived events separate from examiner/case activity events.

This ticket consumes existing records only. It must not run analysis, export files, query SQLite automatically, or persist timeline events.

## Entry Requirements

- S5-T12 accepted.

## Context To Read First

- `tickets/stage-5/S5-T11-timeline-event-contracts.md`
- `tickets/stage-5/S5-T12-file-metadata-timeline-assembly.md`
- `app/backend/forensic_core/timeline.py`
- `app/backend/forensic_core/content_analysis.py`
- `app/backend/forensic_core/export_manifest.py`
- `app/backend/case_store/schema.py`
- `app/tests/test_content_analysis_*.py`
- `app/tests/test_file_export.py`
- `app/tests/test_case_store_schema.py`
- `Goal.md`
- `plan.md`
- `functionality.md`
- `progression.md`
- `review.md`
- `workflow.md`

## Target Files/Folders

Likely files to modify:

- `app/backend/forensic_core/timeline.py`
- `app/backend/forensic_core/__init__.py`
- `app/tests/test_timeline_record_adapters.py`
- `app/backend/forensic_core/README.md`
- `functionality.md`
- `plan.md`
- `progression.md`
- `review.md`
- `tickets/stage-5/README.md`
- `tickets/stage-5/S5-T13-analysis-export-audit-timeline-adapters.md`

## Required Work

- Add adapter helpers for explicit records:
  - Stage 4 hash/signature/mismatch/known-file result created/completed timestamps;
  - Stage 3 export result or manifest timestamps;
  - case-store audit event rows or dictionaries.
- Do not call analysis functions, export functions, or case-store query functions inside adapters.
- Label analysis/export timestamps as tool activity or analysis events unless clearly evidence-derived.
- Label audit rows as case activity events, not evidence file MACB events.
- Preserve case/evidence/source/file identifiers where available.
- Preserve source status, source kind, synthetic/generated flags, read-only assertions, and warnings.
- Handle missing/invalid timestamps using S5-T10 status rules.

## Acceptance Criteria

- Analysis result records can become timeline events without recomputation.
- Export records can become timeline events without reading exported files.
- Audit event dictionaries/rows can become case activity events.
- Evidence-derived events and case activity events are clearly separated.
- No automatic SQLite reads, persistence, parser behavior, search behavior, UI, or reporting is added.
- Tests are dependency-free.

## Test Expectations

Add tests for:

- hash result timestamp event;
- signature result timestamp event;
- export manifest/result timestamp event;
- audit row/dict timestamp event;
- missing/invalid timestamp handling;
- case activity vs evidence event category;
- provenance and source labels.

Run:

```powershell
python -m pytest
```

## Documentation Updates

- Update forensic-core docs with timeline adapter scope.
- Update `functionality.md`, `plan.md`, `progression.md`, and `review.md`.
- Update ticket and Stage 5 README status.

## Review Checklist

- Are tool/case activity events separated from evidence events?
- Do adapters avoid triggering analysis/export/database reads?
- Are non-ok and synthetic/generated statuses preserved?
- Did the implementation avoid persistence and UI/reporting?

## Handoff Prompt

Use `prompts/vscode-agent/2026-07-15-s5-t13-analysis-export-audit-timeline-adapters.md`.
