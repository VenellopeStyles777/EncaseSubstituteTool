# README - Project Orientation

Purpose: the front door for the project. Use this file for a short explanation of what the app is, what it is not, how to run it, and links to the more detailed planning documents.

Current project idea: build an EnCase-like forensic analysis application focused first on opening segmented EWF/E01 evidence images (`.E01`, `.E02`, `.E03`, ...), viewing filesystems, recovering/exporting files, hashing evidence, checking file signatures, indexing/searching content, and producing defensible investigation notes or reports.

## Current Status

Stages 1 through 4 are reviewed backend foundations. The current code can discover `.E01/.E02/...` sibling segment filenames, run the intake JSON command, maintain a minimal SQLite case/evidence/audit schema, use stubbed volume/filesystem/listing/preview/export boundaries, verify written export artifacts, and run provider-backed hash/signature/mismatch/known-file helpers over explicit provider bytes.

Stage 4.5 is the active prerequisite direction: build a substantial first-testing workflow with user-provided E01 files before Stage 5 search/timeline implementation. Stage 5 has detailed future tickets, but S5-T01 must block S5-T02+ until the Stage 4.5 implementation runway is completed and reviewed.

Run tests from the repository root:

```powershell
python -m pytest
```

Run the current intake command:

```powershell
python -m app.backend.api.intake path\to\sample.E01
```

Use `--adapter stub` for dependency-free synthetic metadata checks.

Use the current backend callables from Python:

```python
from app.backend.api import (
    ExportAuditContext,
    StubExportContentProvider,
    export_file,
    export_file_to_json,
    list_directory,
    preview_file,
    run_e01_intake,
)
from app.backend.forensic_core import (
    LocalFileImageStream,
    StubAnalysisContentProvider,
    StubFilesystemAdapter,
    detect_file_signature,
    discover_volumes,
    evaluate_extension_mismatch,
    hash_file_content,
    match_known_file_hashes,
)
```

What is real versus stubbed today:

- Real local-file behavior: `LocalFileImageStream` can describe and bounded-read tiny local files in read-only binary mode.
- Stub/provider behavior: volume, filesystem listing, preview, export, and analysis surfaces currently rely on explicit stubs/providers unless a future adapter supplies real parser-backed data.
- Real-E01 limit: the project can discover E01 segment filenames, but it does not yet read real EWF metadata, verify real EWF images, parse real partitions/filesystems, or extract E01-backed file content.

Current limitations: no Stage 4.5 first-testing command exists yet; no search/timeline implementation exists; no UI/executable/reporting, deleted recovery, carving, external known-file dataset import, automatic analysis persistence, or required native forensic dependency setup exists. Real forensic libraries are optional and not required for tests.

Current handoff: S3-T01 through S3-T06, S4-T01 through S4-T07, and the Stage 4.5 planning package S4.5-T00 through S4.5-T08 are in review/done as documentation work. No analysis-result schema, first-testing command, parser behavior, or manual E01 workflow has been added. The next practical implementation slice should be S4.5-IMP01. Stage 5 is deferred; detailed tickets S5-T00 through S5-T16 now exist, with S5-T00 documentation cleanup done and S5-T01 as the hard gate that must confirm the Stage 4.5 substantial-test implementation runway is completed and reviewed before search/timeline implementation proceeds. The main carryover risk is that the project can discover E01 segments today, but does not yet read real EWF metadata, verify real EWF images, parse partitions/filesystems, or extract file content from E01 files.

Primary planning files:

- [Goal.md](Goal.md): product vision, scope, development stages, and initial VS Code agent prompt.
- [research.md](research.md): research notes, references, functionality map, architecture outline, and plugin/tooling recommendations.
- [functionality.md](functionality.md): current feature/status/manual-test matrix.
- [plan.md](plan.md): stage order, ticket sequence, implementation runway, and guardrails.
- [tickets/](tickets): ticket scope, acceptance criteria, and status.
- [prompts/](prompts): implementation prompt history and onboarding packets.
- [progression.md](progression.md): concise chronological development journal and next action.
- [review.md](review.md): review findings, approvals, risks, and verification notes.
- [log/](log): documentation-change and decision logs.
