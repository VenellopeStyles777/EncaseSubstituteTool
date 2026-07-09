# README - Project Orientation

Purpose: the front door for the project. Use this file for a short explanation of what the app is, what it is not, how to run it, and links to the more detailed planning documents.

Current project idea: build an EnCase-like forensic analysis application focused first on opening segmented EWF/E01 evidence images (`.E01`, `.E02`, `.E03`, ...), viewing filesystems, recovering/exporting files, hashing evidence, checking file signatures, indexing/searching content, and producing defensible investigation notes or reports.

## Current Status

Stage 2 is complete at the documentation/review-handoff level. The project currently provides a backend-first forensic browsing foundation:

- Python backend package skeleton.
- E01 segment discovery for `.E01/.E02/.E03...` sibling files.
- EWF reader adapter boundary with a dependency-free stub adapter.
- Structured dependency-unavailable behavior for missing `pyewf`/libewf.
- JSON intake command/callable.
- Minimal SQLite schema for cases, evidence sources, and audit events.
- Read-only local file byte-stream abstraction for tiny generated files.
- Whole-image volume discovery boundary.
- Filesystem adapter boundary with deterministic stub entries and dependency-safe `pytsk3` skeleton behavior.
- Backend directory listing/file metadata callable over adapter entries.
- Bounded raw/text/hex preview callable over explicit preview-provider bytes.

Run tests from the repository root:

```powershell
python -m pytest
```

Run the current intake command:

```powershell
python -m app.backend.api.intake path\to\sample.E01
```

Use `--adapter stub` for dependency-free synthetic metadata checks.

Use the Stage 2 backend callables from Python:

```python
from app.backend.api import list_directory, preview_file, run_e01_intake
from app.backend.forensic_core import (
    LocalFileImageStream,
    StubFilesystemAdapter,
    discover_volumes,
)
```

What is real versus stubbed today:

- Real local-file behavior: `LocalFileImageStream` can describe and bounded-read tiny local files in read-only binary mode.
- Stubbed behavior: whole-image volume discovery can wrap a readable non-empty stream as one volume; filesystem listing uses the deterministic `StubFilesystemAdapter` unless a future adapter supplies real entries.
- Synthetic preview-provider content: `preview_file()` does not extract bytes from real filesystems. The default `StubPreviewProvider` maps the stub `/hello.txt` entry to synthetic `Hello, world!` bytes.

Current limitations: Stage 2 does not parse real EWF bytes, verify real images, parse real partition tables, parse real filesystems, extract real file content, provide a UI/executable, export/recover files, hash files, search, report, or automatically persist Stage 2 results to the case store. Real forensic libraries are optional and not required for tests.

Next planned stage: Stage 3 export/recovery foundation. It should add safe fixture/stub export contracts, manifests, hashes, provenance, and audit hooks without assuming real deleted-file recovery is available.

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
