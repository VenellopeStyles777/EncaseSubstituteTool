# Project Review Agent Memo Before Stage 3

Date: 2026-07-13

Purpose: candid review-agent notes for the next Stage 3 review agent before this Stage 2 thread is archived.

## Overall Assessment

The project is in a healthy early-stage shape. The strongest decision so far has been to build narrow backend boundaries with structured status objects before attempting real forensic parsing or UI. That discipline is paying off: tests run without private evidence, native dependency absence is visible, and most results carry useful provenance.

The project is still mostly scaffolding, not yet a forensic tool an examiner can rely on. That is not a failure; it is the honest stage of the work. The main danger going forward is overclaiming. Stage 3 export will feel more "real" because it writes files, so the next agents need to be extra careful about provenance, source mutability, and whether exported bytes are synthetic, generated, or eventually parsed from evidence.

## Main Weaknesses

1. Real parser gap.
   The project does not yet parse real EWF bytes, partition tables, or filesystems. Stage 2 has adapter boundaries but no real evidence traversal. Future docs and manifests must not blur this.

2. Metadata/content gap.
   The stub filesystem entry for `/hello.txt` and the preview provider's `Hello, world!` bytes are related by convention, not by a real offset/content contract. Stage 3 must introduce an explicit export content provider or source contract instead of treating metadata entries as byte-bearing objects.

3. Manual testing gap.
   Automated tests pass, but manual-test fields remain `Untested`. There has not been an end-to-end human-run workflow for intake, volume discovery, listing, preview, and later export.

4. Case-store integration gap.
   SQLite schema exists, but intake and Stage 2 API results are not automatically persisted. Stage 3 audit integration should be careful and optional; do not quietly create incomplete case histories.

5. Native dependency uncertainty.
   `pyewf`, libewf, `pytsk3`, and The Sleuth Kit are still optional and absent from the default environment. That is correct for default tests, but the project will eventually need a deliberate integration strategy for real forensic parsing.

6. User-facing workflow gap.
   There is no UI, no packaged executable, and limited CLI/manual workflow. That is fine for now, but Stage 3 should be designed so later CLI/UI layers do not need to reinterpret low-level result objects.

## What Needs Testing Next

Stage 3 should add tests for:

- Export manifests are JSON-serializable and preserve source provenance.
- Export refuses or clearly fails when destination overlaps source/evidence paths.
- Export writes only to examiner-selected output directories.
- Export does not mutate source fixture/provider data.
- Export handles missing content, directory entries, unsupported entries, invalid destination paths, and existing output files predictably.
- Export records byte count exactly.
- SHA-256 matches exported bytes.
- Manifest hash and file hash agree.
- Audit events are only written when a case/evidence context is explicitly supplied.
- Failed exports do not leave misleading complete manifests.
- Partial-write or mismatch behavior is structured and testable.

Manual smoke tests should eventually cover:

- Run intake on dummy `.E01` paths with stub adapter.
- Create/read a tiny local byte-stream fixture.
- Discover a whole-image volume.
- List the stub root directory.
- Preview `/hello.txt`.
- Export provider-backed `/hello.txt` to a separate output directory.
- Inspect manifest/hash/provenance.
- Confirm source directories were not written.

## What Needs Improvement

- Add a first-class content-source boundary for export. Do not reuse preview rendering as export content without a clear contract.
- Make provenance fields consistent across intake, volume, filesystem entry, preview, export result, manifest, and audit event.
- Add parser/adapter/source identifiers to export manifests so a later real parser can be distinguished from current stubs.
- Decide how timestamps should be represented consistently. Current structures often use nullable timestamp fields; export/audit should use UTC ISO strings.
- Keep destination safety logic centralized and heavily tested.
- Consider a small manual CLI only after the export service exists. The CLI should demonstrate workflow, not become the architecture.
- Keep docs updated after every ticket; the docs are currently doing important anti-overclaiming work.

## What Stage 3 Should Focus On

Stage 3 should be about safe writing, not real recovery.

Priority order:

1. Contract clarity.
   Define what an export request, export result, manifest, content provider, warning, and status mean before writing files.

2. Source safety.
   Treat source paths as read-only and protect against output paths inside source/evidence directories.

3. Provenance.
   Every output file and manifest should explain where bytes came from, including whether the source was a stub/provider/generated fixture.

4. Verification.
   Record byte count and SHA-256 early. Broader hash workflows can wait for Stage 4.

5. Audit hooks.
   Case-store audit should be explicit and optional. Avoid hidden persistence.

6. Honest deleted-file language.
   Deleted recovery should remain conditional. The current stub metadata can mark allocation/deleted status, but it cannot recover deleted bytes.

## Ticketing Note For The Next Review Agent

The current Stage 3 tickets in `tickets/stage-3/` are useful placeholders, but they are not yet as detailed as the Stage 2 prompts became. Before handing S3-T01 to an implementation agent, expand the ticket/prompt with concrete status names, expected files, test cases, documentation updates, and strict boundaries. The most important early decision is the export content-source contract: exported bytes should come from an explicit provider/source, not from preview-rendered text/hex and not implicitly from filesystem metadata.

## Review Warnings For Stage 3

Reject or request changes if a Stage 3 implementation:

- Writes anywhere near source/evidence paths without explicit destination safety checks.
- Treats Stage 2 stub entries as real filesystem-backed files.
- Uses preview text/hex output as export bytes instead of raw provider bytes.
- Claims deleted-file recovery is implemented without a real adapter exposing recoverable content.
- Adds required native forensic dependencies to default tests.
- Commits binary evidence/image fixtures.
- Adds UI, search, reporting, broad hashing/signature analysis, or real parser work under the export ticket.
- Records an audit event for a failed export as if it succeeded.
- Produces a manifest without enough provenance to distinguish stub bytes from real evidence bytes.

## Personal Read Of The Project

This project has the right bones. It is not rushing into impressive-looking parsing or UI, which is exactly what makes the foundation more trustworthy. The next challenge is emotional as much as technical: export will make the app feel like it is doing "real forensic work," but the implementation must keep saying what is real and what is synthetic.

If Stage 3 keeps that honesty, the project will have a clean path toward real parser integration later. If Stage 3 blurs the line, future review gets much harder because exported artifacts will look more authoritative than their source warrants.
