# Architecture Components

Purpose: define component boundaries so agents can work in focused areas.

Recommended separation:

- `app/backend/forensic_core`: image abstraction, read-only byte stream, EWF adapter, partition parsing, filesystem adapter interfaces, hashing, file signature detection, export/recovery logic.
- `app/backend/case_store`: SQLite database schema, migrations, case metadata, evidence registry, analysis results, bookmarks, notes, audit log.
- `app/backend/analysis_workers`: background jobs for hashing, signature scans, indexing, thumbnails, text extraction, and later carving/artifacts.
- `app/backend/api`: local application API between UI and backend; should stream large reads/previews safely.
- `app/ui`: case dashboard, evidence list, filesystem tree, file table, preview pane, search, timeline, reports.
- `app/fixtures`: tiny legal test fixtures and fixture-generation notes.
- `app/tests`: unit and integration tests.
- `app/scripts`: setup, fixture generation, and developer utility scripts.
- `app/docs`: developer notes, user guide, forensic assumptions, supported formats matrix.

Design principles:

- Treat evidence as immutable.
- Keep every derived result tied to evidence id, volume id, file id/path, and parser version.
- Prefer established forensic libraries for EWF and filesystem parsing.
- Make unsupported or partially parsed evidence visible instead of silently ignoring it.
- Design for large images: streaming reads, pagination, background work, cancellation, resumable jobs.

Initial skeleton target:

- Create folders with README files explaining responsibilities.
- Do not invent final implementation details too early.
- Keep the first runnable path backend-focused: E01 segment discovery and metadata adapter.
