# Stage 4 Tickets - Hash And Signature Foundations

Purpose: track the Stage 4 work for reproducible per-file hash and signature analysis.

Stage 4 builds on Stage 3 export/content-provider boundaries, but it must remain separate from export-output verification. It must not treat preview-rendered text/hex or metadata-only filesystem entries as source bytes.

## Stage 4 Status

Status: In Progress. S4-T01 contract implementation, S4-T02 provider-backed hashing, S4-T03 file signature detection, S4-T04 extension mismatch rules, S4-T05 fixture-sized known-file matching, and S4-T06 case-store persistence planning are reviewed and done; S4-T07 documentation/review handoff is next.

The Stage 4 review-agent familiarization and risk audit is complete. Continue one reviewed ticket at a time so hash, signature, known-file, and persistence work do not blur together.

Baseline verification before ticket expansion:

```powershell
python -m pytest
```

Result recorded by the Stage 4 review agent: `99 passed in 6.46s`.

## Current Truth

Real today:

- `LocalFileImageStream` can read tiny local files in read-only mode.
- Stage 3 export can write explicit provider bytes to an examiner/test-selected destination, refuse overwrites, clean up failed writes, write a manifest, compute SHA-256 from the written artifact, and optionally audit through explicit `ExportAuditContext`.
- SQLite case-store helpers can persist cases, evidence-source intake snapshots, and audit events when explicitly called.

Stubbed or synthetic today:

- EWF metadata and verification are stubbed or dependency-unavailable.
- Whole-image volume discovery is a boundary, not real partition parsing.
- Filesystem entries are deterministic stub metadata or pytsk3 dependency-status skeletons.
- Preview bytes come from explicit preview providers; the default provider is synthetic.
- Export bytes come from explicit export providers; the default provider is synthetic.

Not proved today:

- Real EWF byte streams.
- Real image verification.
- Real partition or filesystem parsing.
- Real filesystem file-content extraction.
- Deleted-file recovery or carving.
- Hash/signature analysis over evidence-derived file bytes.

## Detailed Ticket Order

| Ticket | Status | Purpose |
| --- | --- | --- |
| [S4-T00](S4-T00-review-agent-risk-audit.md) | Done | Stage 4 review-agent familiarization and reality-anchor risk audit |
| [S4-T01](S4-T01-hash-signature-contracts.md) | Done | Hash/signature request/result/status/warning contracts and provenance model |
| [S4-T02](S4-T02-provider-backed-hashing.md) | Done | Provider-backed SHA-256 plus optional MD5/SHA-1 calculation for explicit content sources |
| [S4-T03](S4-T03-file-signature-detection.md) | Done | File signature/magic-byte detection over bounded provider bytes |
| [S4-T04](S4-T04-extension-mismatch-rules.md) | Done | Extension mismatch result rules where metadata and signature both exist |
| [S4-T05](S4-T05-known-file-matching.md) | Done | Fixture-sized known-file matching over caller-supplied in-memory records |
| [S4-T06](S4-T06-case-store-persistence-plan.md) | Done | Planning-only case-store persistence decision for analysis results |
| [S4-T07](S4-T07-docs-review-handoff.md) | Draft | Stage 4 documentation and review handoff |

## Stage 4 Guardrails

- Hash explicit content provider bytes only.
- Preserve provenance: source path, evidence id when available, volume id, file id/path, provider identity, byte count, parser/source status, read-only status, warnings, and timestamp.
- Keep export-output verification separate from analysis hashing.
- Keep whole-image verification separate unless the image/adapter layer exposes verified evidence bytes and expected verification values.
- Keep MD5/SHA-1 framed as forensic comparison hashes, not stronger integrity signals than SHA-256.
- Keep known-file matching small and optional; do not require NSRL-scale datasets or network access for default tests.
- Keep analysis-result persistence explicit and deferred until a later reviewed workflow/API/job layer owns write intent and persistence context.
- Do not require `pyewf`, libewf, `pytsk3`, The Sleuth Kit, `python-magic`, Node, UI tooling, or real evidence for default tests.
- Do not add search, timeline, reporting, UI, deleted recovery, carving, real EWF parsing, partition parsing, or real filesystem parsing in Stage 4 unless a later reviewed ticket explicitly changes scope.

## Reality-Anchor Decision

Stage 4 can begin with explicit provider-backed contracts and analysis because the current code already has provider identity patterns from Stage 3. However, Stage 4 should not wait until Stage 5 to think about reality anchoring.

Recommended handling:

- S4-T01 must define source-kind/provider fields that can distinguish `synthetic`, `generated_fixture`, `local_stream`, and future `real_parser` bytes.
- S4-T02 may use a dependency-free stub/generated provider for default tests, but the result must label those bytes honestly.
- Before Stage 5 search/timeline begins, add either an optional generated/local-stream provider ticket or a dedicated Stage 5 readiness check that blocks confidence-heavy search over synthetic-only results.

## Stage 4 Definition Of Done

- Hash/signature result contracts are reviewed before calculation behavior broadens.
- Provider-backed hash calculation works for dependency-free explicit content and labels synthetic/generated bytes honestly.
- Signature detection uses bounded provider bytes and structured statuses for detected, unknown, unsupported, and insufficient content.
- Extension mismatch logic only runs when both file metadata and detected signature information are available.
- Known-file matching remains fixture-sized, optional, in-memory, and reviewed before persistence or search/timeline work builds on it.
- Case-store persistence is planned only after standalone result shapes are stable; S4-T06 defers implementation and documents future explicit opt-in requirements.
- Documentation clearly separates per-file provider-backed analysis from export-output verification and whole-image verification.
