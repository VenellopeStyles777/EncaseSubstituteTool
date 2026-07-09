# Stage 3 Tickets - Export And Recovery Foundation

Purpose: track the Stage 3 work for safely exporting selected file-like items with provenance.

Stage 3 should build on Stage 2 filesystem/file metadata results. Deleted-file recovery remains conditional on filesystem adapter support.

## Ticket Order

| Ticket | Status | Purpose |
| --- | --- | --- |
| S3-T01 | Ready | Export result and manifest contract |
| S3-T02 | Ready | Fixture/stub file export service |
| S3-T03 | Ready | Export hashing and byte-count verification |
| S3-T04 | Ready | Case-store audit integration for exports |
| S3-T05 | Ready | Deleted-file recovery research and conditional plan |
| S3-T06 | Ready | Stage 3 docs and review handoff |

## Stage 3 Definition Of Done

- Backend can export a selected fixture/stub file to a separate output directory.
- Export output includes a manifest with provenance, hash, byte count, and timestamp.
- Tests prove source/evidence paths are not modified.
- Audit events can record export actions when case/evidence ids are provided.
- Deleted-file recovery support is documented as available, unsupported, or deferred based on adapter capability.
