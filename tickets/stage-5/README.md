# Stage 5 Tickets - Search And Timeline

Purpose: rough planning for Stage 5 search, filters, and timeline foundations.

Stage 5 must not turn synthetic/provider-backed data into confident forensic findings. It should search and organize reviewed result shapes while preserving source provenance, provider identity, parser/source status, warnings, and uncertainty.

## Stage 5 Status

Status: Rough. Stage 5 has not started, and every Stage 5 ticket remains `Draft`.

Stage 5 should begin with S5-T00 readiness review before implementation. That readiness check should confirm whether the project has a reality anchor or whether search must be explicitly limited to provider-backed/synthetic-labeled data.

## Draft Ticket Order

| Ticket | Status | Purpose |
| --- | --- | --- |
| S5-T00 | Draft | Stage 5 readiness review and search/timeline risk audit |
| S5-T01 | Draft | Search result and filter contract model |
| S5-T02 | Draft | Filename and metadata search over existing listing/result shapes |
| S5-T03 | Draft | Hash/signature result search and filtering |
| S5-T04 | Draft | Timestamp normalization and timeline event contracts |
| S5-T05 | Draft | Timeline assembly from metadata and analysis result timestamps |
| S5-T06 | Draft | Full-text search reality check and deferred extraction plan |
| S5-T07 | Draft | Stage 5 documentation and review handoff |

## Stage 5 Guardrails

- Search results must preserve source path, evidence id when available, volume id, file id/path, source/provider identity, source kind, parser/source status, warning list, and timestamp context.
- Search over synthetic/provider-backed data must be labeled as such.
- Search/timeline must preserve unsupported, failed, partial, dependency-unavailable, synthetic, generated, and provider-backed source states instead of smoothing them into confident findings.
- Filename/metadata search may use existing stub/listing shapes, but it must not imply real filesystem coverage.
- Hash/signature search may use reviewed Stage 4 result shapes only.
- Full-text search should stay deferred or planning-only until there is reviewed text extraction from explicit content providers.
- Timeline results must preserve missing/unknown timestamps instead of inventing values.
- Do not add UI, reporting, real parser work, deleted recovery, carving, background indexing infrastructure, or required native dependencies unless a later reviewed ticket explicitly changes scope.

## Rough Stage 5 Definition Of Done

- Stable search result/filter contracts exist.
- Basic dependency-free filename/metadata search works over explicit input records, if implemented.
- Hash/signature filtering works over reviewed Stage 4 result records, if implemented.
- Timeline event contracts preserve provenance, timestamp kind, source status, and warnings.
- Full-text search is either implemented only over explicit provider text with honest labels or documented as deferred.
- Documentation warns that search/timeline scope is limited by the still-missing real evidence-backed parsing path.
