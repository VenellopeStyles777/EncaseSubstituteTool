# Plan - Sprint and Task Breakdown

Purpose: use this file for the working implementation plan once coding begins. Keep it practical: task, owner/agent, status, blockers, and verification.

Suggested first planning format:

| Stage | Task | Status | Notes |
| --- | --- | --- | --- |
| 0 | Decide stack and create app skeleton | In progress | Planning docs and skeleton folders created; implementation stack still to be confirmed. |
| 1 | Build E01 evidence intake spike | Not started | Open segmented evidence read-only and show metadata. Detailed targets below. |
| 2 | Add filesystem browsing | Not started | Start with one filesystem type and one known test image. |
| 3 | Add hashing and signature checks | Not started | Make this reproducible and testable early. |

## Stage 1 Work Targets

Specific implementation tasks:

Stage 1 is now divided into tickets under `tickets/stage-1/`:

- S1-T01: backend Python skeleton.
- S1-T02: E01 segment discovery.
- S1-T03: EWF reader adapter interface.
- S1-T04: intake command JSON output.
- S1-T05: minimal case-store schema.
- S1-T06: documentation and review handoff.

Definition of done:

- Stage 1 command/API runs.
- Tests cover segment discovery and adapter failure behavior.
- No real evidence file is required for tests.
- Read-only evidence handling is documented.
- Review agent has enough structure to inspect the implementation.
