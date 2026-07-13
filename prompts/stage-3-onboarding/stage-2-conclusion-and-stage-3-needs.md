# Stage 2 Conclusion And Stage 3 Needs

Date: 2026-07-13

Purpose: archive the Stage 2 review-agent conclusion for the Stage 3 implementation/review agents.

## Stage 2 Outcome

Stage 2 is complete at the backend foundation and documentation handoff level. It moved the project from Stage 1's E01 intake boundary into a dependency-safe volume/filesystem browsing and preview foundation.

Implemented capabilities:

- Fixture and dependency strategy for pure stubs, tiny generated files, and optional local-only forensic fixtures.
- Read-only image byte-stream boundary through `LocalFileImageStream`.
- Bounded byte reads with structured metadata, warnings, and status for missing paths, directories, invalid ranges, EOF truncation, and read-beyond-EOF behavior.
- Whole-image volume discovery boundary through `discover_volumes()`.
- Filesystem adapter boundary with JSON-friendly result, warning, dependency, and entry metadata shapes.
- `StubFilesystemAdapter` with deterministic entries for `/Documents` and `/hello.txt`.
- `Pytsk3FilesystemAdapter` dependency-status skeleton that does not require `pytsk3` or The Sleuth Kit.
- Backend directory listing/file metadata callable through `list_directory()`.
- Backend raw/text/hex preview callable through `preview_file()`.
- `StubPreviewProvider` synthetic bytes for the stub `/hello.txt` entry.
- Regression fix for preview offsets beyond available provider content, now returning `content_unavailable`.
- Documentation handoff that separates real local-file behavior, stubbed filesystem/listing behavior, and synthetic provider-backed preview content.

Final Stage 2 test result recorded during handoff:

```powershell
python -m pytest
```

Result: 67 passed.

## What Is Real Today

Real local behavior is deliberately narrow:

- `LocalFileImageStream` can describe and read tiny local files in read-only binary mode.
- Tests use generated tiny files or in-memory/stub data.
- Stage 2 APIs return JSON-friendly dictionaries that preserve provenance fields.

This is a useful foundation, but it is not a real evidence browser yet.

## What Is Stubbed Or Synthetic

Stubbed behavior:

- Volume discovery can report a single whole-image volume; it does not parse partition tables.
- Filesystem metadata and directory listing are backed by deterministic stub adapter entries unless a caller supplies a different adapter.
- The `pytsk3` adapter is only a dependency/unimplemented-status boundary.

Synthetic behavior:

- Preview content comes from an explicit provider.
- The default provider maps `stub-file-hello` (`/hello.txt`) to synthetic `Hello, world!` bytes.
- Current filesystem entries are metadata-only and do not expose real byte offsets or real file content.

## What Stage 2 Did Not Implement

Deferred items:

- Real EWF byte parsing.
- Real image verification.
- Real partition table parsing.
- Real filesystem parsing.
- Real file extraction from a filesystem.
- Export/recovery.
- Hashing/signature analysis beyond future placeholders.
- Search, timeline, reporting, bookmarks, notes, UI, executable packaging.
- Automatic case-store persistence for Stage 2 API results.
- Required native dependencies such as `pyewf`, libewf, `pytsk3`, or The Sleuth Kit.

## Plan Changes And Scope Adjustments During Stage 2

The original Stage 2 target mentioned browsing one filesystem path/tree from a tiny fixture or stub adapter. The implementation chose the conservative side of that target:

- It did not create or commit a tiny filesystem image.
- It did not parse a real raw filesystem.
- It used deterministic stubs for filesystem entries and synthetic provider bytes for preview.

This was the right trade for early correctness. It kept tests fast, legal, dependency-free, and reviewable. The cost is that Stage 3 cannot honestly claim to export real evidence bytes yet. It can export fixture/stub/provider bytes first, but must keep that label visible in every result and manifest.

Another important adjustment: preview was kept separate from filesystem entries. The stub `/hello.txt` listing entry does not itself contain content offsets. Stage 3 must not assume listed entries can be exported unless an explicit export content provider or fixture source supplies bytes.

## Stage 3 Starting Point

Stage 3 should build a safe export/recovery foundation without pretending real recovery exists.

Recommended sequence:

1. Define export request/result/manifest structures.
2. Define an explicit export content source/provider boundary.
3. Implement fixture/stub export only, writing to examiner-selected output paths.
4. Add SHA-256 and byte-count verification for exported output.
5. Add case-store audit integration only when case/evidence identifiers are provided.
6. Document deleted-file recovery as unsupported/deferred unless a future real filesystem adapter exposes deleted entries and recoverable byte ranges.

## Stage 3 Ticket Readiness Note

Stage 3 ticket files already exist under `tickets/stage-3/`, but they are still high-level starter tickets. Before the Stage 3 coding agent begins implementation, the Stage 3 review agent should inspect and likely expand them in the same style used during Stage 2:

- more precise context files to read;
- explicit scope boundaries;
- expected files to create or modify;
- status values and result shapes;
- tests to add;
- documentation updates;
- stop conditions and no-push reminders.

The first ticket, S3-T01, should probably stay documentation/contract-only: define export request/result/manifest structures and tests, but do not write export files yet. S3-T02 should then implement actual fixture/stub export using the explicit content-provider boundary.

## Stage 3 Must Preserve These Boundaries

- Never write to source/evidence paths.
- Do not export from the Stage 2 metadata entry alone; require explicit bytes from a provider or fixture source.
- Do not add real EWF, partition, or filesystem parsing as a side effect of export work.
- Do not make `pyewf`, libewf, `pytsk3`, or The Sleuth Kit required for default tests.
- Do not commit real evidence, real disk images, or large binary fixtures.
- Keep export manifests honest about whether bytes came from stubs, generated fixtures, or later real parsers.

## Files Stage 3 Agents Should Read First

- `Goal.md`
- `plan.md`
- `functionality.md`
- `progression.md`
- `review.md`
- `workflow.md`
- `tickets/stage-3/README.md`
- `tickets/stage-3/S3-T01-export-manifest-contract.md`
- `app/backend/api/README.md`
- `app/backend/forensic_core/README.md`
- `app/backend/case_store/README.md`
- `app/fixtures/README.md`
- `app/docs/environment-readiness.md`
