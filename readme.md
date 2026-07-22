# README - Project Orientation

Purpose: the front door for the project. Use this file for a short explanation of what the app is, what it is not, how to run it, and links to the more detailed planning documents.

Current project idea: build an EnCase-like forensic analysis application focused first on opening segmented EWF/E01 evidence images (`.E01`, `.E02`, `.E03`, ...), viewing filesystems, recovering/exporting files, hashing evidence, checking file signatures, indexing/searching content, and producing defensible investigation notes or reports.

## Current Status

Stages 1 through 4 are reviewed backend foundations. The current code can discover `.E01/.E02/...` sibling segment filenames, run the intake JSON command, maintain a minimal SQLite case/evidence/audit schema, use stubbed volume/filesystem/listing/preview/export boundaries, verify written export artifacts, and run provider-backed hash/signature/mismatch/known-file helpers over explicit provider bytes.

Stage 4.5 is complete through S4.5-IMP07 as the prerequisite first-testing workflow with user-provided E01 files before Stage 5 search/timeline implementation. The project now has the first command shell and case-workspace bundle, best-effort `pyewf` metadata with separate verification status, an EWF-backed stream, partition-table volume result, real-parser-backed root filesystem listing from the local E01 set, explicit selected-file content providers for preview/export/hash/signature, root-listing-derived file-list JSON/CSV, static local HTML summary, guardrail/review handoff reconciliation, and the command-line testing guide. Stage 5 has detailed future tickets; S5-T01 recorded an older incomplete-runway failed gate, S5-T01A hardened older active wording, and S5-T02+ remain blocked until S5-T01 is rerun.

Run tests from the repository root:

```powershell
python -m pytest
```

Run the current intake command:

```powershell
python -m app.backend.api.intake path\to\sample.E01
```

Use `--adapter stub` for dependency-free synthetic metadata checks.

Run the S4.5-IMP01 first-testing command shell:

```powershell
python -m app.backend.api.first_testing path\to\sample.E01 --case .test-artifacts\first-testing\case-a
```

Use `--adapter stub` for dependency-free smoke checks, `--json-only` for a parseable manifest on stdout, and `--redact-paths` to redact the evidence root in console/summary text.

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
- Real-E01 limit: the project can discover E01 segment filenames, can attempt best-effort `pyewf` metadata/verification when the optional dependency exposes safe APIs, can produce a real-parser-backed root filesystem listing in the portable runtime, can write root-listing-derived file-list JSON/CSV and a static local HTML summary, and can run preview/export/hash/signature only for an explicitly selected parser-backed root entry through S4.5-IMP04 provider wrappers. It does not yet create recursive/nested traversal workflows, broad evidence crawls, or a complete manual testing guide.

Current limitations: the S4.5 first-testing command shell creates a workspace and honest artifacts; S4.5-IMP02 adds metadata/verification artifacts; S4.5-IMP03 adds stream, volume, filesystem, root-listing, and demo-readiness artifacts; S4.5-IMP04 adds selected-file readiness/preview/analysis/export artifacts only when the caller explicitly selects a parser-backed root entry; S4.5-IMP05 adds file-list JSON/CSV plus a static local HTML summary from the current root listing only; and S4.5-IMP07 documents the repeatable command-line workflow. Real verification runs only if a safe `pyewf` verification API is available, and stored hash metadata is not verification success. The project still does not crawl or export arbitrary files, provide nested selected-file traversal, or create a dynamic UI/report system. No search/timeline implementation exists; no UI/executable/reporting system, deleted recovery, carving, external known-file dataset import, automatic analysis persistence, or required native forensic dependency setup exists. Real forensic libraries are optional and not required for default tests.

Current handoff: S3-T01 through S3-T06, S4-T01 through S4-T07, and the Stage 4.5 planning package S4.5-T00 through S4.5-T08 are in review/done as documentation work. S4.5-IMP01 through S4.5-IMP07 are reviewed and done. The first-testing command now creates file-list JSON/CSV and a static local HTML summary from the current root listing, and the command-line testing guide is accepted. S5-T01 failed an older readiness gate, so S5-T02 through S5-T16 stay Draft until S5-T01 is rerun against the completed Stage 4.5 runway.

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
