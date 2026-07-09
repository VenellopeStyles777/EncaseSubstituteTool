# Agent Workflow

Purpose: define how the VS Code implementation agent, this research/review agent, and optional subagents should work together.

## Agent Roles

Implementation agent:

- Works primarily in `app/`.
- Implements the current stage from `Goal.md` and `plan.md`.
- Updates `progression.md` after meaningful changes.
- Updates `functionality.md` when a ticket adds, completes, defers, or changes user-visible behavior.
- Adds tests with each implementation step.
- Does not push until review notes are addressed or explicitly deferred.

Research/review agent:

- Maintains `research/`, `Goal.md`, `plan.md`, and review guidance.
- Reviews implementation for bugs, forensic-soundness risks, missing tests, and architecture drift.
- Writes findings in `review.md`.
- Can generate prompts for the implementation agent.
- Can prepare commits/pushes when requested and when the repo is clean.

Subagents:

- Use only for bounded tasks such as dependency research, fixture strategy, UI comparison, or test-plan drafting.
- Subagents should not make broad architecture decisions.
- Subagent outputs should be summarized into the main docs before they affect implementation.

## Normal Development Loop

1. Research/review agent updates goals and generates an implementation prompt.
2. Implementation agent reads the docs and works on the current stage.
3. Implementation agent runs tests and updates `progression.md`.
4. Research/review agent reviews the diff and records findings in `review.md`.
5. Implementation agent fixes accepted findings.
6. Research/review agent verifies status, prepares a commit, and pushes only after the user approves or explicitly requests it.

## Implementation Handoff Summary

When the VS Code implementation agent finishes a ticket or review fix, paste its summary into the research/review chat when practical.

Useful handoff summaries include:

- What ticket was completed.
- What files changed.
- What behavior was added or fixed.
- What tests were added or changed.
- Exact test command and result.
- Any blockers, assumptions, skipped work, or scope boundaries.

This summary is helpful but does not replace review. The research/review agent still checks the actual files and reruns tests.

## Ticketing Workflow

Tickets live in `tickets/`.

Prompt history lives in `prompts/vscode-agent/`.

Use the ticketing workflow when development begins:

1. Research/review agent creates or updates a ticket and marks it `Ready`.
2. User approves the ticket if the scope is significant.
3. Research/review agent creates a VS Code agent prompt and stores it in prompt history.
4. VS Code agent implements only the active ticket.
5. VS Code agent updates `progression.md` and requested docs.
6. User shares the VS Code agent's handoff summary when available.
7. Research/review agent reviews the result and updates ticket status.
8. User approves commit and push separately.

Do not let one prompt cover too much work. A good ticket should usually be reviewable in one sitting.

## Review Checklist Before Commit

- Does the change match the current stage?
- Are evidence paths treated read-only?
- Are errors and unsupported dependencies visible?
- Are tests present and runnable without large private files?
- Are docs updated where behavior changed?
- Is `functionality.md` updated for user-visible feature status and manual-test status?
- Is `git status` clean except intended changes?

## Git Workflow

- Main branch: `main`.
- Commit style: small, descriptive commits.
- Suggested commit message format: `stage N: short summary`.
- Push target: `origin main`.
- The remote should use the repository URL, not the GitHub settings page URL.
- Current intended repository: `https://github.com/VenellopeStyles777/EncaseSubstituteTool`.

Before pushing:

1. Run tests or document why tests cannot run.
2. Run `git status`.
3. Review staged files.
4. Commit only intended files.
5. Push to `origin main`.

Preferred branch flow for stage work:

1. Create or use a branch named for the stage, such as `stage-1-e01-intake`.
2. Complete and review one or more tickets on that branch.
3. Commit after user approval.
4. Push branch after separate user approval.
5. Merge to `main` only after review.

After implementation and review, do not push automatically. Show me git status, changed files, test results, and proposed commit message. Wait for my approval before committing. After commit, wait for separate approval before pushing to origin main.

## Prompt Handoff Rules

- Prompts should name the exact stage.
- Prompts should name the exact ticket when one exists.
- Prompts should list required docs to read first.
- Prompts should specify files/folders to work in.
- Prompts should define deliverables and tests.
- Prompts should ask the implementation agent to update `progression.md`, `plan.md` when relevant, and `functionality.md` when user-visible behavior/status changes.
- Prompts should tell the implementation agent to stop after the active ticket unless the user explicitly says to continue.

## Conflict Handling

- If the implementation agent changes planning docs, the research/review agent should preserve useful changes and clarify conflicts.
- If code and docs disagree, stop and update the docs or implementation before pushing.
- If a native dependency blocks progress, add a fallback path and document the blocker.
