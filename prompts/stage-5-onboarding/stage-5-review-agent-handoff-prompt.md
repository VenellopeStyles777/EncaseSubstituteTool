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
- The project can attempt real EWF metadata through optional `pyewf` and can report explicit verification status; stored hash metadata is not treated as verification success.
- S4.5-IMP03 is reviewed and done with EWF-backed stream reads, partition-table volume discovery, and a real-parser-backed root listing from the local E01 set.
- The project can extract real file content only for an explicitly selected parser-backed root entry within the S4.5-IMP04 first-testing limits.
- Preview, export, hash, and signature can consume selected E01-backed bytes only through that explicit parser-backed selected-file path. Known-file behavior remains provider-backed over reviewed hash results.

## Stage 4.5 State To Inherit

Stage 4.5 was added before Stage 5 because the user wants something testable and demonstrable with actual E01 files.

Stage 4.5 is no longer planning-only. S4.5-T00 through S4.5-T08 are planning/review records, and S4.5-IMP01 through S4.5-IMP07 are reviewed and done. The completed runway includes the first command-shell implementation slice, real metadata/verification status path, EWF stream, partition-table volume discovery, real-parser-backed root listing, selected-file E01-backed content providers, root-listing-derived file-list JSON/CSV, static local HTML output, guardrail/Stage 5 gate handoff, and command-line testing guide.

Before starting Stage 5, confirm the current Stage 4.5 runway state:

- S4.5-IMP01 is done;
- S4.5-IMP02 and S4.5-IMP02A are done;
- S4.5-IMP03, S4.5-IMP04, S4.5-IMP05, S4.5-IMP06, and S4.5-IMP07 are reviewed and done;
- the portable runtime/dependency setup is project-local and ignored by git;
- no committed E01 files or private outputs were added;
- manual E01 testing is partial for intake, metadata, stream, partition-table discovery, root listing, and root-listing-derived file-list/static summary output;
- S5-T01 should be rerun before any S5-T02 or later search/timeline implementation.

The Stage 4.5 implementation runway is:

- S4.5-IMP01: first-testing command shell, safe case workspace, intake persistence, manifest, unsupported-section output.
- S4.5-IMP02: real `pyewf` metadata and verification status. Status: Done.
- S4.5-IMP03: real-E01 filesystem demo gate for EWF-backed stream, partition/volume boundary, and root filesystem metadata/listing. Status: Done.
- S4.5-IMP04: E01-backed selected-file content providers for preview/export/hash/signature. Status: Done.
- S4.5-IMP05: file-list JSON/CSV, command summary, artifact inventory, static local HTML. Status: Done.
- S4.5-IMP06: manual-test guardrails, documentation reconciliation, and review handoff. Status: Done.
- S4.5-IMP07: command-line testing guide and evidence workflow instructions. Status: Done.

## Stage 5 Entry Rule

Do not start Stage 5 search/timeline first.

The first Stage 5 ticket is:

- `S5-T00`: documentation organization, duplication cleanup, and unused/confusing markdown structure review.

The older readiness/risk audit is now the hard gate:

- `S5-T01`: readiness and Stage 4.5 completion gate.

Search/timeline work starts only after:

- Stage 4.5 first-testing implementation runway S4.5-IMP01 through S4.5-IMP07 is completed and reviewed;
- S5-T00 documentation cleanup is accepted;
- S5-T01 confirms what data search/timeline can honestly operate on.

S5-T01 should block S5-T02 and later if the Stage 4.5 substantial-test runway is incomplete. It should name the missing Stage 4.5 implementation ticket(s), not push that work back.

## Detailed Stage 5 Ticket Queue

- S5-T00: documentation organization, duplication cleanup, and unused/confusing structure review. Status: Done.
- S5-T01: readiness and Stage 4.5 completion gate. Status: Done; older failed gate/blocker from before Stage 4.5 was complete. Rerun is now the next required gate.
- S5-T01A: Stage 4.5 gate language hardening. Status: Done.
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

## S5-T00 Review Result

S5-T00 is documentation-only and is now accepted. It organized and de-duplicated documentation before feature work continued.

Main cleanup areas:

- `functionality.md`, `progression.md`, and `log/`
- `tickets/` and `prompts/vscode-agent/`
- unused or confusing markdown files/folders

Resolved cleanup candidates:

- `tickets/stage-5a/` was checked and was not present.
- `prompts/stage-5a-onboarding/` was removed after confirming it was empty and had no unique information to preserve.

For any future markdown cleanup, do not delete or move files until unique information has been preserved and references have been checked.

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

The latest recorded reviewer verification in `review.md` for S4.5-IMP07 acceptance:

```powershell
.\.python312-embed\python.exe -m pytest
# 184 passed in 28.38s
```

Run the suite again after any new edits or before the S5-T01 rerun acceptance.

## Next Likely Moves

1. Rerun S5-T01 as the hard Stage 4.5 completion gate.
2. Do not proceed to S5-T02 or later search/timeline tickets until S5-T01 passes after S4.5-IMP07 acceptance.
