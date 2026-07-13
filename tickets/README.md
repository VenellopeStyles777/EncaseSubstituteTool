# Ticketing Workflow

Purpose: this folder stores small, reviewable development tickets for the VS Code implementation agent.

The goal is to make each development slice clear enough that the implementation agent can work independently, while the research/review agent can verify results without guessing what "done" means.

## Ticket States

Use these exact status labels:

- `Draft`: ticket is being written.
- `Ready`: ticket can be given to the VS Code agent.
- `In Progress`: implementation agent is working on it.
- `Review`: implementation is ready for review.
- `Changes Requested`: review found issues that should be fixed before merge/push.
- `Done`: accepted and recorded in project docs.
- `Blocked`: cannot continue without user input, dependency setup, or a design decision.

## Ticket Format

Each ticket should include:

- Objective.
- Context files to read.
- Target files or folders.
- Required work.
- Acceptance criteria.
- Test expectations.
- Documentation updates.
- Review checklist.
- Handoff prompt.

## Development Loop

1. Research/review agent writes or updates a ticket.
2. User approves the ticket scope.
3. Research/review agent gives the ticket prompt to the VS Code agent.
4. VS Code agent implements the ticket and updates docs.
5. Research/review agent reviews the diff, test output, and docs.
6. Ticket is marked `Done`, `Changes Requested`, or `Blocked`.
7. After approved tickets are done, user approves branch/commit/push.

## Branch Guidance

Use a branch per stage or small cluster of tickets:

```text
stage-1-e01-intake
```

For very small fixes during the same stage, keep using the same branch unless the user wants separate branches.

Current ticket folders:

- `stage-1/`: E01 intake spike. Status: complete.
- `stage-2/`: volume/filesystem browsing MVP. Status: complete at Stage 2 handoff.
- `stage-3/`: export/recovery foundation. Status: S3-T01 ready; later tickets are Draft pending review before implementation.

## Approval Buffer

No agent should push to GitHub automatically.

Expected Git approval checkpoints:

1. Show changed files and test result.
2. Propose commit message.
3. Wait for user approval to commit.
4. Show branch and remote target.
5. Wait for user approval to push.
