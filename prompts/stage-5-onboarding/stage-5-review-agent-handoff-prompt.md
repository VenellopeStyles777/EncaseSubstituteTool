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
- S4.5-IMP05 is reviewed and done with root-listing-derived `file-list.json`, `file-list.csv`, and a static local HTML summary.
- S4.5-IMP08 is reviewed and done with an explicit independent logical-image SHA-256 hash command/artifact, but the local 1 TB full-image hash remains a long-running user/reviewer command unless separately completed.
- S4.5-IMP09, S4.5-IMP09A, and S4.5-IMP09B are reviewed and done with bounded parser-backed nested directory navigation, file-visible demo behavior when available, and a live command-line browser over the same listing path.
- The project can extract real file content only for an explicitly selected parser-backed root entry within the S4.5-IMP04 first-testing limits.
- Preview, export, hash, and signature can consume selected E01-backed bytes only through that explicit parser-backed selected-file path. Known-file behavior remains provider-backed over reviewed hash results.

## Stage 4.5 State To Inherit

Stage 4.5 was added before Stage 5 because the user wants something testable and demonstrable with actual E01 files.

Stage 4.5 is no longer planning-only. S4.5-T00 through S4.5-T08 are planning/review records, and S4.5-IMP01 through S4.5-IMP10 are reviewed and done. Hands-on demo feedback extended Stage 4.5 with S4.5-IMP09, S4.5-IMP09B, and S4.5-IMP10 because the user needed real nested directory navigation, a live command-line browser, and a final gate refresh before Stage 5. S4.5-IMP10 is accepted, and the S5-T01 rerun is accepted/done with a passed-gate result.

Before starting Stage 5, confirm the current Stage 4.5 runway state:

- S4.5-IMP01 is done;
- S4.5-IMP02 and S4.5-IMP02A are done;
- S4.5-IMP03, S4.5-IMP04, S4.5-IMP05, S4.5-IMP06, S4.5-IMP07, S4.5-IMP08, S4.5-IMP09, S4.5-IMP09A, S4.5-IMP09B, and S4.5-IMP10 are reviewed and done;
- S4.5-IMP09/S4.5-IMP09A provide bounded nested directory navigation with regular files visible in the corrected local real-E01 smoke and `path_not_directory` for known nested file paths;
- S4.5-IMP09B provides the reviewed live command-line directory browser over the same parser-backed listing path;
- S4.5-IMP10 provides the reviewed final demo guide and Stage 5 gate refresh;
- the portable runtime/dependency setup is project-local and ignored by git;
- no committed E01 files or private outputs were added;
- manual E01 testing is partial for intake, metadata, stream, partition-table discovery, root listing, root-listing-derived file-list/static summary output, bounded nested navigation, and the live browser;
- S5-T01 rerun is accepted; S5-T02 is the next ticket to prepare.

The Stage 4.5 implementation runway is:

- S4.5-IMP01: first-testing command shell, safe case workspace, intake persistence, manifest, unsupported-section output.
- S4.5-IMP02: real `pyewf` metadata and verification status. Status: Done.
- S4.5-IMP03: real-E01 filesystem demo gate for EWF-backed stream, partition/volume boundary, and root filesystem metadata/listing. Status: Done.
- S4.5-IMP04: E01-backed selected-file content providers for preview/export/hash/signature. Status: Done.
- S4.5-IMP05: file-list JSON/CSV, command summary, artifact inventory, static local HTML. Status: Done.
- S4.5-IMP06: manual-test guardrails, documentation reconciliation, and review handoff. Status: Done.
- S4.5-IMP07: command-line testing guide and evidence workflow instructions. Status: Done.
- S4.5-IMP08: independent full logical-image hash artifact. Status: Done.
- S4.5-IMP09: nested directory navigation into actual filesystem entries. Status: Done.
- S4.5-IMP09A: file-visible nested navigation correction. Status: Done.
- S4.5-IMP09B: interactive E01 directory browser. Status: Done.
- S4.5-IMP10: demo guide and Stage 5 gate refresh. Status: Done.

## Stage 5 Entry Rule

Do not start Stage 5 search/timeline first.

The first Stage 5 ticket is:

- `S5-T00`: documentation organization, duplication cleanup, and unused/confusing markdown structure review.

The older readiness/risk audit is now the hard gate:

- `S5-T01`: readiness and Stage 4.5 completion gate.

Search/timeline work starts only after:

- Stage 4.5 first-testing implementation runway S4.5-IMP01 through S4.5-IMP10 is completed and reviewed;
- S5-T00 documentation cleanup is accepted;
- S5-T01 confirms what data search/timeline can honestly operate on.

S5-T01 should block S5-T02 and later if the Stage 4.5 substantial-test runway is incomplete. It should name the missing Stage 4.5 implementation ticket(s), not push that work back.

## Detailed Stage 5 Ticket Queue

- S5-T00: documentation organization, duplication cleanup, and unused/confusing structure review. Status: Done.
- S5-T01: readiness and Stage 4.5 completion gate. Status: Done; older failed gate/blocker remains historical. Rerun accepted after Stage 4.5 completion.
- S5-T01A: Stage 4.5 gate language hardening. Status: Done.
- S5-T02: input inventory and provenance audit. Status: Draft; next ticket to prepare.
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

The latest reviewer verification in `review.md` is S5-T01 rerun acceptance:

```powershell
.\.python312-embed\python.exe -m pytest
# 207 passed in 41.53s
```

Privacy-safe reviewer S5-T01 rerun real-image no-selection/navigation smoke exited 0 with `ok_with_unsupported_sections`, 53 segments, metadata `metadata_available`, verification `not_supported`, EWF stream `ok`, logical media size 1,024,209,543,168 bytes, 5 volumes, filesystem `ok`, a parser-backed root listing with 11 entries, file-list JSON/CSV `ok` with 11 entries, a parser-backed nested listing with 19 regular files visible, static HTML created, image hash `not_run`, selected-file operations `not_run`, `source_modified: false`, and `read_only_asserted: true`.

S5-T02 should be prepared next; do not start S5-T03 or later until earlier Stage 5 tickets are reviewed.

## Next Likely Moves

1. Prepare S5-T02 as the next ticket.
2. Review and feed S5-T02 only after its ticket/prompt are populated and marked ready.
3. Do not proceed to S5-T03 or later search/timeline tickets until earlier Stage 5 tickets are reviewed.
