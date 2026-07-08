# Risks And Assumptions

Purpose: keep the main technical and forensic risks visible.

Immediate risks:

- Native forensic libraries can be difficult to install on Windows, especially Python bindings.
- E01 support alone is not enough; the app must bridge image reading into volume/filesystem parsing.
- Deleted-file recovery behavior varies heavily by filesystem.
- Forensic correctness depends on audit logs, immutability, provenance, and visible error states from the beginning.
- Large images will expose performance problems unless indexing and previews are streamed/paginated.

Assumptions:

- The first app target is an offline desktop/workstation workflow.
- The first evidence target is EWF/E01, not live acquisition.
- Tests should avoid real evidence and use tiny fixtures or mocks.
- A separate review agent will inspect code for correctness and forensic-soundness risks.

Review focus:

- Read-only evidence handling.
- Provenance for every derived result.
- Clear dependency failure modes.
- No hard-coded private evidence paths.
- No hidden parse errors.
