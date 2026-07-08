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

- Create backend package/module structure under `app/backend/forensic_core`.
- Create segment discovery logic for E01 chains.
- Create EWF reader adapter interface.
- Add pyewf/libewf adapter if dependency is available.
- Add stub/mock adapter for tests and dependency-free development.
- Create structured metadata response model.
- Create basic case-store schema draft under `app/backend/case_store`.
- Add an intake command/API entry point.
- Add tests under `app/tests`.
- Update documentation after implementation.

Definition of done:

- Stage 1 command/API runs.
- Tests cover segment discovery and adapter failure behavior.
- No real evidence file is required for tests.
- Read-only evidence handling is documented.
- Review agent has enough structure to inspect the implementation.
