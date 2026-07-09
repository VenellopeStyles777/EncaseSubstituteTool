# Forensic Core

Purpose: core forensic logic.

Stage 1 target:

- E01 segment discovery.
- EWF reader adapter interface.
- Real libewf/pyewf adapter target when available.
- Stub/mock adapter for tests.
- Read-only evidence access assumptions.

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
