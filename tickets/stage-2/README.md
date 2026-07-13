# Stage 2 Tickets - Volume And Filesystem Browsing MVP

Purpose: track the Stage 2 work for moving from E01 intake metadata to backend volume/filesystem browsing.

Stage 2 should stay backend-first. Do not build a polished UI in this stage.

## Ticket Order

| Ticket | Status | Purpose |
| --- | --- | --- |
| S2-T01 | Done | Fixture and dependency strategy |
| S2-T02 | Done | Image/byte-stream abstraction |
| S2-T03 | Done | Volume discovery boundary |
| S2-T04 | Done | Filesystem adapter boundary |
| S2-T05 | Done | Directory listing and file metadata view |
| S2-T06 | Done | Raw/text/hex preview foundation |
| S2-T07 | Done | Stage 2 docs and review handoff |

## Stage 2 Definition Of Done

- Backend can return structured volume/filesystem data from a safe fixture or stubbed adapter.
- Tests do not require private evidence, large images, or native forensic dependencies.
- Missing native dependencies are reported as structured status.
- File metadata includes provenance fields needed by later export and reporting stages.
- Docs clearly state what is fixture-backed, stubbed, unsupported, and deferred.
