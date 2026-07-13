# Stage 3 Tickets - Export And Recovery Foundation

Purpose: track the Stage 3 work for safely exporting selected file-like items with provenance.

Stage 3 should build on Stage 2 filesystem/file metadata results. Deleted-file recovery remains conditional on filesystem adapter support.

## Ticket Order

| Ticket | Status | Purpose |
| --- | --- | --- |
| S3-T01 | Done | Export result and manifest contract |
| S3-T02 | Done | Fixture/stub file export service |
| S3-T03 | Done | Export hashing and byte-count verification |
| S3-T04 | Draft | Case-store audit integration for exports |
| S3-T05 | Draft | Deleted-file recovery research and conditional plan |
| S3-T06 | Draft | Stage 3 docs and review handoff |

## Stage 3 Definition Of Done

- Backend can export a selected fixture/stub file to a separate output directory.
- Export output includes a manifest with provenance, hash, byte count, and timestamp.
- Tests prove source/evidence paths are not modified.
- Audit events can record export actions when case/evidence ids are provided.
- Deleted-file recovery support is documented as available, unsupported, or deferred based on adapter capability.

## 2026-07-13 Ticket Readiness Review

The Stage 3 ticket set is a useful outline, but the tickets are not yet implementation-ready. They need the same level of detail as the Stage 2 prompts before being handed to the VS Code implementation agent.

Recommended sequence:

1. Expand S3-T01 into a contract-only implementation ticket.
2. After S3-T01 review, expand S3-T02 around a first-class export content-source/provider boundary and destination safety checks.
3. Keep S3-T03 focused on SHA-256 and byte-count verification for already-written exports.
4. Keep S3-T04 audit integration explicit and optional.
5. Keep S3-T05 documentation/planning-only unless real adapter support exists.
6. Use S3-T06 as the final Stage 3 documentation and review handoff.

Do not hand any Stage 3 ticket after S3-T03 to the implementation agent until its individual ticket file and prompt are reviewed for the current code state. S3-T01 through S3-T03 are reviewed and done; S3-T04 is the next ticket to prepare.
