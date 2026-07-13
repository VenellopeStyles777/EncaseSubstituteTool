# Fixtures

Purpose: tiny legal fixtures and fixture-generation notes for tests.

Rules:

- Do not commit private or real case evidence.
- Prefer generated dummy files and mocked EWF adapters for Stage 1.
- Keep fixtures small enough for Git.
- Treat any fixture that represents evidence as read-only in tests.
- Keep generated scratch fixtures under ignored workspace paths such as `.test-artifacts/`.
- Document the generator and intent before committing any binary fixture.

Stage 1 fixture policy:

- S1-T02 should use temporary dummy segment files created during tests, such as `sample.E01`, `sample.E02`, and `sample.E04`.
- Dummy segment files do not need real EWF bytes for segment-discovery tests.
- Do not commit large E01 files.
- Do not commit real evidence.
- If a stable mock fixture becomes necessary, keep it tiny, clearly fake, and document why it is committed.

## Stage 2 Fixture Strategy

Stage 2 should let image, volume, filesystem, directory-listing, and preview code develop without private evidence, large images, or native forensic dependencies. Use three fixture tiers:

1. Pure stubs.
2. Tiny generated files.
3. Optional local-only forensic fixtures.

Pure stubs are the default for adapter boundaries. Use them when testing result shapes, dependency-unavailable behavior, provenance fields, parser status values, directory entry metadata, deleted/allocation flags, warnings, and API serialization. Stub tests must not require `pyewf`, libewf, `pytsk3`, The Sleuth Kit, real E01 files, or real filesystems.

Tiny generated files are appropriate for byte-stream and preview behavior. They may include small raw binary/text files created during tests under `.test-artifacts/`, with known bytes and offsets. These files should test read-only open modes, bounded reads, offset/length validation, text decoding, and hex rendering. They do not need to contain a valid partition table or filesystem unless a later ticket explicitly adds a safe generator.

Optional local-only forensic fixtures are for developer experiments and later integration checks. These can include known-good raw images, EWF images, or filesystem images created outside the repository, but they must stay untracked and must never be required by default tests. Any optional test that uses them should be skipped unless the developer opts in with an explicit environment variable or local path configuration. Those tests should report structured "fixture unavailable" or pytest skip output, not failures.

## Stage 2 Test Guidance

- S2-T02 image/byte-stream abstraction: use tiny generated raw files for real byte reads; use stubs for EWF-backed streams until the EWF reader can expose bytes safely.
- S2-T03 volume discovery boundary: use stubs for partitioned images; allow a whole-image/single-volume result for tiny raw fixtures.
- S2-T04 filesystem adapter boundary: use stubs for filesystem trees and dependency statuses; `pytsk3` absence must produce structured unavailable status.
- S2-T05 directory listing and metadata: use stubbed directory trees with stable provenance fields, file ids/paths, sizes, timestamps where meaningful, and allocation/deleted status where supported.
- S2-T06 preview foundation: use explicit provider content with known raw/text/hex output. The default `StubPreviewProvider` content is synthetic and must not be described as real bytes extracted from the stub filesystem entry.

## Later Real-Fixture Handling

When the project is ready for real raw/EWF/TSK-style integration fixtures:

- Generate or source only legal, non-sensitive training images.
- Prefer tiny images that can be regenerated from scripts or documented commands.
- Store committed fixture generators or manifests, not private evidence.
- Keep large or private fixtures outside Git and list their expected local path through ignored configuration.
- Mark optional integration tests clearly so normal `python -m pytest` remains dependency-free.
- Record fixture provenance: how it was generated, expected size/hash, filesystem type, volume layout, and whether deleted-file artifacts are intentionally present.

## Stage 3 Export Content-Source Guidance

S3-T01 introduces export contract structures only. Tests should continue to use Stage 2-style stub metadata dictionaries and explicit synthetic content-source identities instead of real export files.

For later Stage 3 tickets:

- Export bytes must come from an explicit export content source/provider.
- Filesystem metadata entries are not byte-bearing objects by themselves.
- Preview-rendered text or hex is not an export byte source.
- Stub/provider/generated-fixture exports must be labeled as synthetic, generated, or provider-backed in the result and manifest.
- Real raw/EWF/filesystem fixtures remain optional local-only inputs until a reviewed ticket explicitly adds safe integration behavior.
