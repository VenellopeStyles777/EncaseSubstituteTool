# VS Code Agent Prompt - S5-T00 Documentation Organization And Duplication Cleanup

You are working on S5-T00 for the EnCase substitute project.

This is documentation-only cleanup. Do not change app source code, tests, parser behavior, native dependency setup, evidence handling behavior, UI/reporting, or Stage 5 search/timeline implementation.

## Read First

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
- `tickets/stage-5/S5-T00-documentation-organization-cleanup.md`
- `prompts/README.md`
- `prompts/vscode-agent/README.md`

## Goal

Make the documentation easier to navigate before Stage 5 search/timeline work starts.

Focus on organization and duplication around:

- `functionality.md`, `progression.md`, and `log/`
- `tickets/` and `prompts/vscode-agent/`
- unused or confusing markdown files/folders, including empty or stale stage folders if present.

## Required Work

- Apply the source-of-truth model from `tickets/stage-5/S5-T00-documentation-organization-cleanup.md`.
- Reduce repeated long status narratives where they appear in multiple docs.
- Keep `functionality.md` as the feature/status/manual-test matrix.
- Keep `progression.md` as the concise chronological journal and next-action tracker.
- Keep `log/documentation.md` as the documentation-change and decision trace.
- Keep `tickets/` as the source of ticket scope and `prompts/vscode-agent/` as the prompt history/index.
- Update README/index files so a future agent knows where to start.
- Preserve unique historical information before deleting, moving, or archiving any markdown file/folder.
- Keep the current real-E01 limitation visible: segment filename discovery exists, but real EWF metadata, verification, partition/filesystem parsing, and E01-backed file content extraction are not implemented yet.

## Guardrails

- Do not implement search/timeline.
- Do not implement Stage 4.5 first-testing behavior.
- Do not install dependencies.
- Do not add E01 files, fixtures, or private evidence outputs.
- Do not remove historical review information unless its unique content is preserved somewhere appropriate.
- Do not mark manual E01 testing as complete unless the user has actually confirmed a reviewed manual run.

## Deliverables

- Updated documentation files that clearly separate source-of-truth responsibilities.
- Updated `tickets/stage-5/README.md` or S5-T00 status if appropriate.
- Updated `prompts/vscode-agent/README.md` if prompt indexing changes.
- Updated `progression.md` and `log/documentation.md` with a concise S5-T00 entry.
- A final handoff summary listing changed files, cleanup decisions, removed/archived structures, skipped cleanup candidates, and test results.

## Tests

Run:

```powershell
python -m pytest
```

If you remove or rename markdown files/folders, also use repository search to check for stale references and include the result in your handoff.
