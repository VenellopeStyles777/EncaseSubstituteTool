# Forensic Core

Purpose: core forensic logic.

Stage 1 target:

- E01 segment discovery.
- EWF reader adapter interface.
- Real libewf/pyewf adapter target when available.
- Stub/mock adapter for tests.
- Read-only evidence access assumptions.

Stage 2 target:

- Read-only image/byte-stream abstraction.
- Volume discovery boundary.
- Filesystem adapter boundary.
- Directory metadata and preview foundations.

## S1-T02 Segment Discovery

`discover_e01_segments(path)` accepts a selected first segment path such as `sample.E01` and discovers sibling files with the same base name and `.E##` extensions.

Current behavior:

- accepts `.E01` case-insensitively;
- returns ordered present segments such as `.E01`, `.E02`, `.E03`;
- warns about missing middle segments when a later segment proves a gap;
- returns a structured invalid result for unsupported selected extensions;
- only inspects path names and directory entries, and does not open or parse evidence content.

The result object includes `is_valid_input`, `is_complete`, `read_only`, ordered `segments`, and structured `warnings`. Real EWF metadata reading belongs to a later adapter ticket.

## S1-T03 EWF Reader Adapter

`ewf_reader.py` defines the read-only adapter boundary for EWF metadata and verification:

- `EwfReaderAdapter`: protocol for dependency status, metadata, and verification calls.
- `EwfMetadataResult`: stable metadata result shape with adapter availability, read-only assertion, source paths, metadata, dependency status, verification status, and warnings.
- `VerificationStatus`: stable verification shape using statuses such as `not_supported` and `not_run`.
- `StubEwfReaderAdapter`: dependency-free adapter that returns predictable synthetic metadata for tests.
- `PyewfEwfReaderAdapter`: optional pyewf/libewf adapter skeleton that reports structured dependency-unavailable results when `pyewf` is not installed. If `pyewf` is importable, real metadata extraction is still intentionally unimplemented in Stage 1 and is reported as `real_reader_not_implemented`.

The adapter layer is intentionally separate from segment discovery. Stage 1 does not parse real EWF bytes and does not require real evidence files or native forensic libraries for tests.

## S2-T02 Image Byte-Stream Abstraction

`image_stream.py` defines the first Stage 2 read-only byte access boundary:

- `ImageByteStream`: protocol for stream metadata and bounded byte-range reads.
- `LocalFileImageStream`: local file-backed implementation for tiny generated fixtures and later raw-image experiments.
- `ImageStreamInfo`: source metadata and provenance, including source path, stream type, size, read-only assertion, status, and warnings.
- `ImageReadResult`: bounded read result, including offset, requested length, source size, bytes read, read-only assertion, status, warnings, and raw `bytes` for backend callers.
- `ImageStreamStatus` and `ImageStreamWarning`: structured status/warning objects for normal and error paths.

Current behavior:

- opens local sources only in read-only binary mode;
- supports bounded reads by explicit offset and length;
- reports missing paths, directory paths, unreadable files, invalid negative ranges, and reads beyond the end of the source as structured statuses;
- truncates reads that extend past EOF and emits a `read_truncated_at_eof` warning;
- uses tiny generated files in tests and does not require real evidence, EWF parsing, `pyewf`, libewf, `pytsk3`, or The Sleuth Kit.

S2-T02 does not parse partitions, discover volumes, parse filesystems, list directories, render previews, export files, or hash evidence. Those remain later tickets.

## S2-T03 Volume Discovery Boundary

`volume_discovery.py` defines the first Stage 2 volume result boundary:

- `discover_volumes(stream, strategy="whole_image")`: returns JSON-friendly volume discovery results for an `ImageByteStream`.
- `VolumeDiscoveryResult`: source-level result with schema version, source path, stream type, source size, read-only assertion, strategy, status, volumes, and warnings.
- `VolumeInfo`: one volume-like range with volume id, index, source provenance, offset, length, type, description, read-only assertion, status, and warnings.
- `VolumeDiscoveryStatus` and `VolumeDiscoveryWarning`: structured status/warning objects for normal, unavailable, empty, and unsupported paths.

Current behavior:

- emits one `whole_image` volume for a readable non-empty local file stream;
- returns `empty_image` with no volumes for a zero-byte source;
- returns `image_stream_unavailable` with stream-status warning details for missing, directory, unreadable, or otherwise unavailable image streams;
- returns `partition_parsing_unsupported` for non-`whole_image` strategies so future real partition parsers have a documented boundary.

S2-T03 does not parse real partition tables, parse filesystems, list directories, render previews, export files, hash evidence, or require `pytsk3`, The Sleuth Kit, `pyewf`, libewf, or real forensic images.

## S2-T04 Filesystem Adapter Boundary

`filesystem_adapter.py` defines the Stage 2 filesystem adapter boundary:

- `FilesystemAdapter`: protocol for read-only filesystem metadata adapters.
- `StubFilesystemAdapter`: dependency-free deterministic adapter for tests and later directory-listing integration.
- `Pytsk3FilesystemAdapter`: optional pytsk3 skeleton that reports structured dependency status without requiring `pytsk3`.
- `FilesystemResult`: source/volume-level result with adapter name, dependency status, source path, volume id, volume offset/length, filesystem type, read-only assertion, root path, entries, status, and warnings.
- `FilesystemEntry`: file/directory metadata shape for later S2-T05 listing, including file id, path, name, type, size, allocation/deleted state, timestamps, source provenance, adapter name, read-only assertion, status, and warnings.

Current behavior:

- stub adapter returns deterministic root entries for `/Documents` and `/hello.txt`;
- pytsk3 adapter returns `dependency_unavailable` when `pytsk3` is missing;
- importable pytsk3 remains `real_parser_not_implemented` until a later ticket intentionally adds real parsing;
- tests do not require real evidence, real filesystems, `pytsk3`, or The Sleuth Kit.

S2-T04 does not add a directory-listing command/workflow, parse real filesystems, render previews, export files, hash evidence, or require native forensic dependencies.

## S2-T05 Directory Listing And File Metadata View

The backend API layer in `app/backend/api/directory_listing.py` consumes the S2-T04 filesystem adapter boundary and exposes a JSON-friendly directory listing callable:

- `list_directory(volume, directory_path="/", adapter=None)`: returns a stable dictionary for a directory listing.
- `directory_listing_to_json(...)`: serializes the listing result for command/API consumers.

Current behavior:

- uses adapter-provided `FilesystemEntry` metadata without mutating adapter results;
- preserves source path, volume id, volume offset/length, filesystem type, adapter/dependency information, read-only assertion, entry status/warnings, allocation/deleted state, and timestamps;
- root listing with `StubFilesystemAdapter` returns `/Documents` and `/hello.txt`;
- non-root directories return `path_unsupported`, files return `path_not_directory`, unknown paths return `path_not_found`, and dependency-unavailable/not-implemented adapters return `filesystem_unavailable`.

S2-T05 does not read file content, render previews, parse real filesystems, export/recover files, compute hashes, add UI, or require native forensic dependencies. Raw/text/hex preview remains S2-T06.
