# S4-T06 - Case-Store Persistence Plan

Status: Draft

Stage: Stage 4 - Hash and signature foundations

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Decide whether Stage 4 hash/signature results should persist to the SQLite case store now or remain standalone JSON-friendly results until a later workflow stage.

This ticket should be documentation/planning-first unless S4-T01 through S4-T05 produce stable result shapes and the reviewer explicitly approves schema work.

## Expected Scope

- Review existing `case_store/schema.py` and Stage 3 audit behavior.
- Decide whether persistence belongs in Stage 4 or later reporting/workflow stages.
- If persistence is deferred, document the future table requirements.
- If persistence is approved, propose or implement a minimal migration/table plan only after review.

Future persistence requirements should include:

- case id and evidence id;
- source provenance;
- provider identity and source kind;
- hash/signature status and warnings;
- algorithm/digest values;
- signature and mismatch fields;
- synthetic/generated/real-parser labels;
- timestamps;
- schema version.

## Out Of Scope

- Automatic persistence from analysis APIs without explicit caller context.
- Background job orchestration.
- UI/report integration.
- Large known-file database persistence.
- Real parser work.

## Test Expectations

If planning-only, run `python -m pytest` to ensure no backend regression.

If schema work is approved later, tests must use in-memory SQLite and cover explicit opt-in persistence only.

## Review Checklist

- Persistence is not automatic or surprising.
- Source provenance and provider uncertainty are preserved.
- Synthetic/provider-backed results cannot be mistaken for real parser output.
