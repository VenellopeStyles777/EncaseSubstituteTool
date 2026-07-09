# README - Project Orientation

Purpose: the front door for the project. Use this file for a short explanation of what the app is, what it is not, how to run it, and links to the more detailed planning documents.

Current project idea: build an EnCase-like forensic analysis application focused first on opening segmented EWF/E01 evidence images (`.E01`, `.E02`, `.E03`, ...), viewing filesystems, recovering/exporting files, hashing evidence, checking file signatures, indexing/searching content, and producing defensible investigation notes or reports.

## Current Status

Stage 1 is complete. It provides a backend-first E01 intake foundation:

- Python backend package skeleton.
- E01 segment discovery for `.E01/.E02/.E03...` sibling files.
- EWF reader adapter boundary with a dependency-free stub adapter.
- Structured dependency-unavailable behavior for missing `pyewf`/libewf.
- JSON intake command/callable.
- Minimal SQLite schema for cases, evidence sources, and audit events.

Run tests from the repository root:

```powershell
python -m pytest
```

Run the current intake command:

```powershell
python -m app.backend.api.intake path\to\sample.E01
```

Use `--adapter stub` for dependency-free synthetic metadata checks.

Current limitations: Stage 1 does not parse real EWF bytes, parse filesystems, provide a UI, or automatically persist intake results to the case store. Real forensic libraries are optional and not required for tests.

Next planned stage: Stage 2 volume/filesystem browsing MVP. Stage 2 should add fixture strategy, image/byte-stream abstractions, volume discovery, filesystem adapter boundaries, and one backend browsable tree or stubbed equivalent. It should still avoid UI and private evidence.

Primary planning files:

- [Goal.md](Goal.md): product vision, scope, development stages, and initial VS Code agent prompt.
- [research.md](research.md): research notes, references, functionality map, architecture outline, and plugin/tooling recommendations.
- [tickets/](tickets): ticketing workflow and stage-by-stage implementation tickets.
- [prompts/](prompts): history of prompts sent to implementation agents.
- [functionality.md](functionality.md): future feature checklist and acceptance criteria.
- [plan.md](plan.md): future sprint-level implementation plan.
- [progression.md](progression.md): future progress tracker.
- [review.md](review.md): future code-review findings and architectural review notes.
- [log/](log): working logs for documentation, errors, general notes, and Git activity.
