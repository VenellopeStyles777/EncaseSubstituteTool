# Stage 5 Review Agent Handoff Prompt

You are inheriting the EnCase substitute project as the Stage 5 research/review agent.

Your role is to review, plan, and hand off work. Do not directly change app source code when implementation is needed. If app coding is needed, write a precise coding-agent prompt instead and wait for user approval or direction.

## Immediate Orientation

Read these first:

- `Goal.md`
- `readme.md`
- `plan.md`
- `functionality.md`
- `progression.md`
- `review.md`
- `workflow.md`
- `log/documentation.md`
- `tickets/README.md`
- `tickets/stage-4.5/README.md`
- `tickets/stage-4.5/S4.5-T00-current-functionality-and-scope.md`
- `tickets/stage-4.5/S4.5-T01-user-e01-handling-plan.md`
- `tickets/stage-4.5/S4.5-T02-manual-e01-intake-demo-plan.md`
- `tickets/stage-4.5/S4.5-T03-pyewf-real-metadata-investigation.md`
- `tickets/stage-4.5/S4.5-T04-ewf-stream-partition-filesystem-plan.md`
- `tickets/stage-4.5/S4.5-T05-e01-file-content-provider-plan.md`
- `tickets/stage-4.5/S4.5-T06-file-list-and-output-plan.md`
- `tickets/stage-4.5/S4.5-T07-workflow-guardrail-review-optimization.md`
- `tickets/stage-4.5/S4.5-T08-documentation-review-handoff.md`
- `tickets/stage-5/README.md`
- `tickets/stage-5/S5-T00-documentation-organization-cleanup.md`
- `tickets/stage-5/S5-T01-readiness-and-stage-4.5-completion-gate.md`
- `tickets/stage-5/S5-T02-input-inventory-and-provenance-audit.md`
- `tickets/stage-5/S5-T03-searchable-record-contracts.md`
- `tickets/stage-5/S5-T04-search-query-filter-sort-contracts.md`
- `tickets/stage-5/S5-T05-file-metadata-search-engine.md`
- `tickets/stage-5/S5-T06-search-result-sorting-and-pagination.md`
- `tickets/stage-5/S5-T07-analysis-result-record-adapters.md`
- `tickets/stage-5/S5-T08-analysis-result-search-and-filters.md`
- `tickets/stage-5/S5-T09-search-api-wrapper-and-json-output.md`
- `tickets/stage-5/S5-T10-timestamp-normalization-contracts.md`
- `tickets/stage-5/S5-T11-timeline-event-contracts.md`
- `tickets/stage-5/S5-T12-file-metadata-timeline-assembly.md`
- `tickets/stage-5/S5-T13-analysis-export-audit-timeline-adapters.md`
- `tickets/stage-5/S5-T14-timeline-query-sorting-and-json-api.md`
- `tickets/stage-5/S5-T15-full-text-search-reality-check.md`
- `tickets/stage-5/S5-T16-stage-5-documentation-review-handoff.md`
- `prompts/vscode-agent/README.md`
- `prompts/vscode-agent/2026-07-15-s5-t00-documentation-organization-cleanup.md`
- `prompts/stage-5-onboarding/README.md`

## Current Project Truth

Stages 1 through 4 are reviewed backend foundations:

- Stage 1: E01 filename segment discovery, EWF adapter boundary, intake JSON command, SQLite case/evidence/audit schema.
- Stage 2: local byte stream, whole-image volume boundary, filesystem adapter/stub, listing, bounded preview provider.
- Stage 3: export contracts/service, export manifests, SHA-256 and byte-count verification of written exports, optional audit.
- Stage 4: provider-backed hash/signature/extension mismatch/known-file matching. These operate on explicit providers, not real E01-extracted filesystem bytes.

The current real-E01 truth is still limited:

- The project can discover `.E01/.E02/...` segment filenames.
- The project does not yet read real EWF metadata.
- The project does not yet verify real EWF images.
- The project does not yet parse real partitions or filesystems from E01 files.
- The project does not yet extract real file content from E01 files.
- Preview, export, hash, signature, and known-file behavior remain provider-backed, fixture/stub/synthetic, or planned unless a later reviewed implementation proves otherwise.

## Stage 4.5 State To Inherit

Stage 4.5 was added before Stage 5 because the user wants something testable and demonstrable with actual E01 files.

Stage 4.5 remains planning-only at handoff time. S4.5-T00 through S4.5-T08 are in review. S4.5-T08 completed the documentation/review handoff and did not implement behavior.

Before starting Stage 5, review S4.5-T08 as a normal review item. Confirm:

- no Python source behavior changed;
- no dependencies were installed;
- no E01 files or private outputs were added;
- Stage 4.5 remains planning-only;
- manual E01 test status remains `Untested`;
- the next practical implementation slice is S4.5-IMP01, and Stage 5 search/timeline implementation should not push the Stage 4.5 substantial-test runway back.

The Stage 4.5 implementation runway is:

- S4.5-IMP01: first-testing command shell, safe case workspace, intake persistence, manifest, unsupported-section output.
- S4.5-IMP02: real `pyewf` metadata and verification status.
- S4.5-IMP03: EWF-backed stream, partition boundary, root filesystem metadata/listing.
- S4.5-IMP04: E01-backed selected-file content providers for preview/export/hash/signature.
- S4.5-IMP05: file-list JSON/CSV, command summary, artifact inventory, optional static HTML.
- S4.5-IMP06: manual-test guardrails, documentation reconciliation, and review handoff.

## Stage 5 Entry Rule

Do not start Stage 5 search/timeline first.

The first Stage 5 ticket is:

- `S5-T00`: documentation organization, duplication cleanup, and unused/confusing markdown structure review.

The older readiness/risk audit is now the hard gate:

- `S5-T01`: readiness and Stage 4.5 completion gate.

Search/timeline work starts only after:

- Stage 4.5 first-testing implementation runway S4.5-IMP01 through S4.5-IMP06 is completed and reviewed;
- S5-T00 documentation cleanup is accepted;
- S5-T01 confirms what data search/timeline can honestly operate on.

S5-T01 should block S5-T02 and later if the Stage 4.5 substantial-test runway is incomplete. It should name the missing Stage 4.5 implementation ticket(s), not push that work back.

## Detailed Stage 5 Ticket Queue

- S5-T00: documentation organization, duplication cleanup, and unused/confusing structure review. Status: Ready.
- S5-T01: readiness and Stage 4.5 completion gate. Status: Draft.
- S5-T02: input inventory and provenance audit. Status: Draft.
- S5-T03: searchable record contracts. Status: Draft.
- S5-T04: search query, filter, and sort contracts. Status: Draft.
- S5-T05: file metadata search engine. Status: Draft.
- S5-T06: search result sorting and pagination. Status: Draft.
- S5-T07: analysis result record adapters. Status: Draft.
- S5-T08: analysis result search and filters. Status: Draft.
- S5-T09: search API wrapper and JSON output. Status: Draft.
- S5-T10: timestamp normalization contracts. Status: Draft.
- S5-T11: timeline event contracts. Status: Draft.
- S5-T12: file metadata timeline assembly. Status: Draft.
- S5-T13: analysis, export, and audit timeline adapters. Status: Draft.
- S5-T14: timeline query, sorting, and JSON API. Status: Draft.
- S5-T15: full-text search reality check. Status: Draft.
- S5-T16: Stage 5 documentation and review handoff. Status: Draft.

## S5-T00 Review Intent

S5-T00 is documentation-only. It should organize and de-duplicate documentation before feature work continues.

Main cleanup areas:

- `functionality.md`, `progression.md`, and `log/`
- `tickets/` and `prompts/vscode-agent/`
- unused or confusing markdown files/folders

Known cleanup candidates to inspect:

- empty `tickets/stage-5a/`
- empty `prompts/stage-5a-onboarding/`

Do not delete or move markdown files until unique information has been preserved and references have been checked.

Use the source-of-truth split from `workflow.md` and `tickets/stage-5/S5-T00-documentation-organization-cleanup.md`:

- `functionality.md`: current feature/status/manual-test matrix.
- `progression.md`: concise chronological development journal and next action.
- `log/documentation.md`: documentation-change log and decision trace.
- `review.md`: review findings, approvals, risks, and verification notes.
- `plan.md`: stage order, ticket sequence, implementation runway, and guardrails.
- `tickets/`: executable work slices, ticket status, acceptance criteria, and handoff scope.
- `prompts/vscode-agent/`: paste-ready implementation prompts and prompt history.
- `workflow.md`: process rules, handoff rules, review gates, and Git expectations.

## Review Posture

Default to a review stance:

- Findings first, ordered by severity, with file references.
- Confirm test output yourself when feasible.
- Preserve user or coding-agent changes; do not revert unrelated work.
- Keep manual-test status at `Untested` unless the user confirms a reviewed manual run against an approved local E01/manual input.
- Treat real local E01 paths and outputs as private. Redact paths in summaries unless the user says otherwise.
- Do not allow docs to claim real metadata, verification, partition parsing, filesystem parsing, file-content extraction, preview/export/hash/signature, file-list output, or visual output before reviewed implementation exists.

## Latest Verification Known At Handoff

The latest recorded verification in `review.md` for S4.5-T08:

```powershell
python -m pytest
# 152 passed in 10.64s
```

Run the suite again after any new edits or before final review acceptance.

## Next Likely Moves

1. Review S4.5-T08 and decide whether it can move from `Review` to `Done`.
2. Ask the user whether to begin S4.5-IMP01 implementation planning or to start Stage 5 S5-T00 documentation cleanup.
3. If Stage 5 starts, feed or review `prompts/vscode-agent/2026-07-15-s5-t00-documentation-organization-cleanup.md`.
4. Do not proceed to Stage 5 search/timeline tickets until S5-T00 is accepted and S5-T01 confirms the Stage 4.5 substantial-test runway is completed and reviewed.
