# Stage 1 Tickets - E01 Intake Spike

Purpose: track the diced-up Stage 1 work for proving E01 evidence intake.

Stage 1 should stay backend-first. Do not build a polished UI in this stage.

## Ticket Order

| Ticket | Status | Purpose |
| --- | --- | --- |
| S1-T01 | Done | Backend Python skeleton and project commands |
| S1-T01A | Done | Finish S1-T01 after Python environment fix |
| S1-T02 | Done | E01 segment discovery |
| S1-T03 | Done | EWF reader adapter interface and stub adapter |
| S1-T04 | Done | Intake command returning structured JSON |
| S1-T05 | Ready | Minimal SQLite case-store schema |
| S1-T06 | Ready | Documentation, dependency notes, and review handoff |

## Stage 1 Definition Of Done

- A documented command performs an E01 intake check.
- Tests run without real forensic evidence.
- Evidence access is read-only or mocked.
- Missing native dependencies produce clear messages.
- Case/evidence/audit schema direction is documented or implemented.
- `plan.md`, `progression.md`, and `review.md` are updated.
