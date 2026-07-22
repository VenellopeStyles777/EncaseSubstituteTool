# VS Code Agent Prompts

Purpose: prompt history for the VS Code Codex implementation agent.

Use this folder when:

- Starting a new implementation session.
- Assigning a ticket.
- Asking the VS Code agent to fix review findings.
- Preparing a branch for commit/push.

Current handoff:

- S3-T01 through S3-T06 are reviewed and done.
- S4-T01 through S4-T07 are reviewed and done.
- Stage 4.5 planning prompts S4.5-T01 through S4.5-T08 are present; S4.5-IMP01 through S4.5-IMP07 have been implemented, reviewed, and marked done.
- `2026-07-15-stage-4.5-first-testing-familiarization.md` is the added Stage 4.5 coding-agent onboarding prompt.
- `2026-07-15-s5-t00-documentation-organization-cleanup.md` is the Stage 5 S5-T00 documentation cleanup prompt; S5-T00 is done.
- S5-T01 is done with an older failed-gate/blocker result from before the Stage 4.5 runway was complete; S4.5-IMP01 through S4.5-IMP07 are now done, so S5-T01 is the next gate to rerun.
- S5-T01A is done after documentation hardening. Do not feed S5-T02 or later until S5-T01 is rerun and accepted.
- Keep this coding-agent handoff separate from the Stage 4 research/review-agent packet in `prompts/stage-4-onboarding/`.
- The coding-agent reflection may focus on implementation mechanics; the review-agent reflection focuses on review risk, forensic soundness, and future-stage guardrails.

Current major onboarding prompts:

- `2026-07-09-stage-1-ticketing-start.md`: Stage 1 implementation onboarding.
- `2026-07-09-stage-2-familiarization.md`: Stage 2 implementation onboarding.
- `2026-07-13-stage-3-familiarization.md`: Stage 3 implementation onboarding.
- `2026-07-14-stage-4-familiarization.md`: Stage 4 implementation onboarding.
- `2026-07-15-stage-4.5-first-testing-familiarization.md`: added Stage 4.5 first-testing onboarding.
- `2026-07-15-s4.5-t01-user-e01-handling-plan.md`: Stage 4.5 S4.5-T01 documentation-only handoff prompt.
- `2026-07-15-s4.5-t02-case-workspace-first-testing-command-plan.md`: Stage 4.5 S4.5-T02 documentation-only handoff prompt.
- `2026-07-15-s4.5-t03-pyewf-real-metadata-verification-plan.md`: Stage 4.5 S4.5-T03 documentation-only handoff prompt.
- `2026-07-15-s4.5-t04-ewf-stream-partition-filesystem-plan.md`: Stage 4.5 S4.5-T04 documentation-only handoff prompt.
- `2026-07-15-s4.5-t05-e01-file-content-provider-plan.md`: Stage 4.5 S4.5-T05 documentation-only handoff prompt.
- `2026-07-15-s4.5-t06-file-list-output-plan.md`: Stage 4.5 S4.5-T06 documentation-only handoff prompt.
- `2026-07-15-s4.5-t07-workflow-guardrail-review-optimization.md`: Stage 4.5 S4.5-T07 documentation-only handoff prompt.
- `2026-07-15-s4.5-t08-documentation-review-handoff.md`: Stage 4.5 S4.5-T08 documentation-only handoff prompt.
- `2026-07-16-s4.5-imp01-first-testing-command-shell.md`: Stage 4.5 S4.5-IMP01 first-testing command shell implementation prompt.
- `2026-07-16-s4.5-imp02-real-ewf-metadata-verification.md`: Stage 4.5 S4.5-IMP02 real EWF metadata and verification implementation prompt.
- `2026-07-17-s4.5-imp02a-metadata-warning-semantics.md`: Stage 4.5 S4.5-IMP02A metadata warning semantics correction prompt.
- `2026-07-16-s4.5-imp03-ewf-stream-partition-filesystem.md`: Stage 4.5 S4.5-IMP03 EWF stream, partition, and filesystem implementation prompt.
- `2026-07-16-s4.5-imp04-e01-file-content-providers.md`: Stage 4.5 S4.5-IMP04 E01-backed selected-file content providers prompt.
- `2026-07-16-s4.5-imp05-file-list-output-visual-summary.md`: Stage 4.5 S4.5-IMP05 file-list, output bundle, and visual summary prompt.
- `2026-07-16-s4.5-imp06-final-guardrail-review-handoff.md`: Stage 4.5 S4.5-IMP06 final guardrail review and Stage 5 handoff prompt.
- `2026-07-16-s4.5-imp07-command-line-testing-guide.md`: Stage 4.5 S4.5-IMP07 command-line testing guide prompt.
- `2026-07-15-s5-t00-documentation-organization-cleanup.md`: Stage 5 S5-T00 documentation organization cleanup prompt.
- `2026-07-15-s5-t01-readiness-and-stage-4.5-completion-gate.md`: Stage 5 S5-T01 readiness and Stage 4.5 completion gate prompt.
- `2026-07-16-s5-t01a-stage-4.5-gate-language-hardening.md`: Stage 5 S5-T01A documentation-hardening prompt.
- `2026-07-15-s5-t02-input-inventory-and-provenance-audit.md`: Stage 5 S5-T02 input inventory and provenance audit prompt.
- `2026-07-15-s5-t03-searchable-record-contracts.md`: Stage 5 S5-T03 searchable record contracts prompt.
- `2026-07-15-s5-t04-search-query-filter-sort-contracts.md`: Stage 5 S5-T04 search query, filter, and sort contracts prompt.
- `2026-07-15-s5-t05-file-metadata-search-engine.md`: Stage 5 S5-T05 file metadata search engine prompt.
- `2026-07-15-s5-t06-search-result-sorting-and-pagination.md`: Stage 5 S5-T06 search result sorting and pagination prompt.
- `2026-07-15-s5-t07-analysis-result-record-adapters.md`: Stage 5 S5-T07 analysis result record adapters prompt.
- `2026-07-15-s5-t08-analysis-result-search-and-filters.md`: Stage 5 S5-T08 analysis result search and filters prompt.
- `2026-07-15-s5-t09-search-api-wrapper-and-json-output.md`: Stage 5 S5-T09 search API wrapper and JSON output prompt.
- `2026-07-15-s5-t10-timestamp-normalization-contracts.md`: Stage 5 S5-T10 timestamp normalization contracts prompt.
- `2026-07-15-s5-t11-timeline-event-contracts.md`: Stage 5 S5-T11 timeline event contracts prompt.
- `2026-07-15-s5-t12-file-metadata-timeline-assembly.md`: Stage 5 S5-T12 file metadata timeline assembly prompt.
- `2026-07-15-s5-t13-analysis-export-audit-timeline-adapters.md`: Stage 5 S5-T13 analysis, export, and audit timeline adapters prompt.
- `2026-07-15-s5-t14-timeline-query-sorting-and-json-api.md`: Stage 5 S5-T14 timeline query, sorting, and JSON API prompt.
- `2026-07-15-s5-t15-full-text-search-reality-check.md`: Stage 5 S5-T15 full-text search reality check prompt.
- `2026-07-15-s5-t16-stage-5-documentation-review-handoff.md`: Stage 5 S5-T16 documentation and review handoff prompt.
- `2026-07-14-s4-t01-hash-signature-contracts.md`: Stage 4 S4-T01 implementation prompt.
- `2026-07-14-s4-t02-provider-backed-hashing.md`: Stage 4 S4-T02 implementation prompt.
- `2026-07-14-s4-t03-file-signature-detection.md`: Stage 4 S4-T03 implementation prompt.
- `2026-07-14-s4-t04-extension-mismatch-rules.md`: Stage 4 S4-T04 implementation prompt.
- `2026-07-14-s4-t05-known-file-matching.md`: Stage 4 S4-T05 implementation prompt.
- `2026-07-15-s4-t06-case-store-persistence-plan.md`: Stage 4 S4-T06 implementation prompt.
- `2026-07-15-s4-t07-stage-4-docs-review-handoff.md`: Stage 4 S4-T07 implementation prompt.
- `2026-07-13-s3-t01-export-manifest-contract.md`: Stage 3 S3-T01 implementation prompt.
- `2026-07-13-s3-t02-file-export-service.md`: Stage 3 S3-T02 implementation prompt.
- `2026-07-13-s3-t03-export-hashing.md`: Stage 3 S3-T03 implementation prompt.
- `2026-07-13-s3-t04-export-audit-integration.md`: Stage 3 S3-T04 implementation prompt.
- `2026-07-13-s3-t05-deleted-recovery-plan.md`: Stage 3 S3-T05 implementation prompt.
- `2026-07-14-s3-t06-stage-3-docs-review-handoff.md`: Stage 3 S3-T06 implementation prompt.

Each prompt should name:

- Current ticket or stage.
- Required files to read first.
- Allowed scope.
- Deliverables.
- Tests.
- Documentation updates.
