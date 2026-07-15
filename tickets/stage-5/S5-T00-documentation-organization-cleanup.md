# S5-T00 - Documentation Organization And Duplication Cleanup

Status: Ready

Stage: Stage 5 - documentation cleanup gate before search/timeline

## Objective

Make the project documentation easier to navigate before Stage 5 search/timeline work starts.

This ticket should reduce duplication, clarify which files own which information, reconcile stale status notes, and identify unused or confusing markdown files/folders. It is intentionally documentation-only.

## Context Files To Read First

- `Goal.md`
- `readme.md`
- `plan.md`
- `functionality.md`
- `progression.md`
- `review.md`
- `workflow.md`
- `log/documentation.md`
- `tickets/README.md`
- `tickets/stage-4.5/README.md`
- `tickets/stage-5/README.md`
- `prompts/README.md`
- `prompts/vscode-agent/README.md`

## Source-Of-Truth Model

Use this ownership split while cleaning up:

| File or folder | Owns | Should avoid |
| --- | --- | --- |
| `functionality.md` | Current capability/status matrix and manual-test status | Long chronological history, ticket-by-ticket narrative |
| `progression.md` | Concise chronological development journal and next action | Duplicated feature tables or full documentation logs |
| `log/documentation.md` | Documentation-change log and decision trace | Repeating the full current status every time |
| `review.md` | Review findings, approvals, risks, and verification notes | General project roadmap text that belongs in `plan.md` |
| `plan.md` | Stage order, ticket sequence, implementation runway, guardrails | Detailed prompt text or full review history |
| `tickets/` | Executable work slices, status, acceptance criteria, handoff prompts | Long historical prompt transcripts |
| `prompts/vscode-agent/` | Paste-ready coding-agent prompts and prompt index | Replacing ticket files as source of scope truth |
| `workflow.md` | Process rules, handoff rules, review gates, Git expectations | Ticket-specific implementation detail |

## Required Work

- Inventory top-level markdown files and the main markdown folders:
  - `functionality.md`
  - `progression.md`
  - `log/`
  - `tickets/`
  - `prompts/vscode-agent/`
  - other markdown files or folders that are stale, empty, confusing, or no longer referenced.
- Reconcile `functionality.md`, `progression.md`, and `log/documentation.md` so they no longer repeat the same long status narrative.
- Reconcile `tickets/` and `prompts/vscode-agent/` so ticket scope and prompt history are clearly linked but not duplicated unnecessarily.
- Review unused or confusing structures, including the empty `tickets/stage-5a/` folder if it still exists.
- Remove, rename, archive, or clearly document unused markdown files/folders only after preserving any unique information and updating references.
- Update README/index files so a new agent can find the current source of truth without reading every historical note.
- Keep Stage 4.5 first-testing and Stage 5 search/timeline priorities clearly separated.
- Keep the real-E01 truth visible: current code can discover E01 segment filenames but does not yet read real EWF metadata, verify real EWF images, parse real partitions/filesystems, or extract real file content from E01 files.

## Out Of Scope

- App code changes.
- Parser behavior.
- Search/timeline implementation.
- Stage 4.5 first-testing implementation.
- Native dependency installation.
- Test fixture or evidence-file creation.
- UI, reporting, packaging, deleted recovery, carving, or background indexing.

## Acceptance Criteria

- The documentation has a clear source-of-truth map.
- Stage 5 starts with this documentation cleanup gate before search/timeline tickets.
- `functionality.md`, `progression.md`, and `log/documentation.md` have distinct jobs and reduced duplicate narrative.
- `tickets/` and `prompts/vscode-agent/` clearly show which tickets are current, which prompts are historical, and what should be fed next.
- Unused or confusing markdown files/folders are either removed, archived, or explicitly documented as intentional.
- Cross-links are updated so there are no obvious stale references to removed or renamed docs.
- No behavior, schema, parser, dependency, evidence, UI, report, or test fixture changes are made.

## Test Expectations

- Run `python -m pytest` after the documentation cleanup unless the reviewer explicitly accepts a documentation-only no-test note.
- Optionally run a simple markdown reference check with repository search commands if files or folders are removed or renamed.

## Review Checklist

- Does the cleanup preserve important history while making the current state easier to read?
- Are source-of-truth responsibilities clear enough for a future coding agent?
- Did any deleted/moved file contain unique information that was not preserved?
- Do ticket statuses and prompt indexes agree?
- Does Stage 5 still avoid search/timeline work until S5-T00 is accepted?
- Is the real-E01 limitation still visible and honest?

## Handoff Prompt

Use `prompts/vscode-agent/2026-07-15-s5-t00-documentation-organization-cleanup.md`.
