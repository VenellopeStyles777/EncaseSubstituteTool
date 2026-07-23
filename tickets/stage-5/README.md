# Stage 5 Tickets - Documentation Cleanup, Then Search And Timeline

Purpose: Stage 5 now starts with a documentation organization and duplication cleanup gate before any search, filters, or timeline foundation work.

After that cleanup gate, Stage 5 must not turn synthetic/provider-backed data into confident forensic findings. It should search and organize reviewed result shapes while preserving source provenance, provider identity, parser/source status, warnings, and uncertainty.

## Stage 5 Status

Status: Deferred. Stage 5 search/timeline implementation has not started. S5-T00 documentation cleanup is done; S5-T01 is done with an older failed-gate/blocker result, S5-T01A is done after hardening older active Stage 4.5 bypass/priority wording, and S5-T02 through S5-T16 remain detailed draft tickets with matching prompt files. Stage 4.5 has been extended after hands-on demo feedback; S4.5-IMP08 through S4.5-IMP09B are reviewed/done, and S4.5-IMP10 remains drafted.

Current override: Stage 4.5 first testing remains the near-term prerequisite goal. S4.5-IMP01 through S4.5-IMP09B are reviewed and done, including the corrected nested-navigation demo that shows regular files when available and the live command-line browser. S4.5-IMP10 still needs the final guide/gate refresh. S5-T02 and later search/timeline implementation tickets stay blocked until S4.5-IMP10 is reviewed and S5-T01 is rerun.

## Hard Stage 4.5 Gate

S5-T01 must verify the Stage 4.5 runway before any search/timeline implementation begins:

| Stage 4.5 slice | Required result before S5-T02+ |
| --- | --- |
| S4.5-IMP01 | First-testing command shell, safe case workspace, intake persistence, manifest, unsupported-section output reviewed |
| S4.5-IMP02 | Real `pyewf` metadata attempt and verification status reviewed, including dependency-unavailable behavior |
| S4.5-IMP03 | EWF-backed stream, partition boundary, and root filesystem metadata/listing reviewed |
| S4.5-IMP04 | E01-backed selected-file content providers for preview/export/hash/signature reviewed |
| S4.5-IMP05 | File-list JSON/CSV, command summary, artifact inventory, optional static HTML reviewed |
| S4.5-IMP06 | Manual-test guardrails, documentation reconciliation, and review handoff reviewed |
| S4.5-IMP07 | Command-line testing guide with exact commands, artifact inspection steps, troubleshooting, and proof boundaries reviewed |
| S4.5-IMP08 | Independent full logical-image hash artifact reviewed |
| S4.5-IMP09 | Nested directory navigation into actual filesystem entries reviewed, including S4.5-IMP09A file-visible correction |
| S4.5-IMP09B | Live command-line directory browser reviewed |
| S4.5-IMP10 | Command-line guide and Stage 5 gate refresh reviewed after hash/navigation/browser |

If S5-T01 finds any of these incomplete, it should record Stage 5 as blocked and name the exact Stage 4.5 ticket(s) still needed. It should not continue into S5-T02.

## Detailed Ticket Order

| Ticket | Status | Purpose |
| --- | --- | --- |
| S5-T00 | Done | Documentation organization, duplication cleanup, and unused/confusing structure review |
| S5-T01 | Done | Readiness and Stage 4.5 completion gate; older failed gate, rerun blocked until S4.5-IMP10 is reviewed |
| S5-T01A | Done | Stage 4.5 gate language hardening for older active bypass/priority wording |
| S5-T02 | Draft | Input inventory and provenance audit |
| S5-T03 | Draft | Searchable record contracts |
| S5-T04 | Draft | Search query, filter, and sort contracts |
| S5-T05 | Draft | File metadata search engine |
| S5-T06 | Draft | Search result sorting and pagination |
| S5-T07 | Draft | Analysis result record adapters |
| S5-T08 | Draft | Analysis result search and filters |
| S5-T09 | Draft | Search API wrapper and JSON output |
| S5-T10 | Draft | Timestamp normalization contracts |
| S5-T11 | Draft | Timeline event contracts |
| S5-T12 | Draft | File metadata timeline assembly |
| S5-T13 | Draft | Analysis, export, and audit timeline adapters |
| S5-T14 | Draft | Timeline query, sorting, and JSON API |
| S5-T15 | Draft | Full-text search reality check |
| S5-T16 | Draft | Stage 5 documentation and review handoff |

## Stage 5 Guardrails

- S5-T00 is documentation organization only. It must not implement search/timeline behavior, parser behavior, native dependency setup, UI, reporting, or app source changes.
- S5-T01 is a gate. It must block S5-T02 and later if the Stage 4.5 substantial-test implementation runway is incomplete, including the remaining S4.5-IMP10 guide/gate refresh.
- Before deleting or moving any markdown file or folder, preserve unique information in the correct source-of-truth document and update references.
- Documentation cleanup must make the project easier to follow without erasing important review history.
- Search results must preserve source path, evidence id when available, volume id, file id/path, source/provider identity, source kind, parser/source status, warning list, and timestamp context.
- Search over synthetic/provider-backed data must be labeled as such.
- Search/timeline must preserve unsupported, failed, partial, dependency-unavailable, synthetic, generated, and provider-backed source states instead of smoothing them into confident findings.
- Filename/metadata search may use existing stub/listing shapes, but it must not imply real filesystem coverage.
- Hash/signature search may use reviewed Stage 4 result shapes only.
- Full-text search should stay deferred or planning-only until there is reviewed text extraction from explicit content providers.
- Timeline results must preserve missing/unknown timestamps instead of inventing values.
- Do not add UI, reporting, real parser work, deleted recovery, carving, background indexing infrastructure, or required native dependencies unless a later reviewed ticket explicitly changes scope.
- Do not consume Stage 4.5 demo outputs as real EWF/filesystem parser evidence unless the corresponding parser behavior was actually implemented and reviewed.

## Draft Stage 5 Definition Of Done

- Stable search result/filter contracts exist.
- Basic dependency-free filename/metadata search works over explicit input records, if implemented.
- Hash/signature filtering works over reviewed Stage 4 result records, if implemented.
- Timeline event contracts preserve provenance, timestamp kind, source status, and warnings.
- Full-text search is either implemented only over explicit provider text with honest labels or documented as deferred.
- Documentation warns that search/timeline scope is limited by whatever Stage 4.5 actually reviewed, and does not smooth over missing real evidence-backed parsing or content extraction.
