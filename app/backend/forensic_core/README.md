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
