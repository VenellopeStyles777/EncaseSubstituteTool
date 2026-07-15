# Future Ticket Roadmap

Purpose: preserve cross-stage risks and rough ticket direction beyond the current implementation stage.

This file is intentionally higher level than the stage ticket folders. Before each stage starts, the research/review agent should turn the relevant notes into detailed stage tickets and VS Code implementation prompts.

## Cross-Stage Weakest Point

The project's weakest point after Stage 3 is the missing real evidence-backed content path.

The code has good contracts and safe stubs, but the default flow still does not parse real EWF bytes, partitions, filesystems, deleted entries, or file content. Preview and export bytes come from explicit providers, and the default providers are synthetic.

Future stages must avoid building confidence-heavy features over synthetic data without clear labels.

## Priority Improvement

Add a reality anchor before the project becomes UI/report heavy.

This is now reframed as Stage 4.5 first testing under `tickets/stage-4.5/`. The immediate priority is user-provided E01 manual testing and honest command-line output before search/timeline continues. The current Stage 4.5 goal overrides the older Stage 5 search/timeline priority. The earlier candidate shape is preserved here as a later possible fixture direction:

```text
Reality Anchor Fixture And Content Provider

Goal: introduce a tiny, non-private, repeatable content path that is closer to real evidence than hard-coded synthetic stub bytes.

Options:
- generated raw fixture with known bytes and offsets;
- generated tiny filesystem fixture if safe tooling is available;
- optional local-only pytsk3/libewf integration fixture;
- adapter-backed provider that reads from ImageByteStream ranges.

Acceptance:
- default tests remain dependency-safe;
- provenance identifies fixture/provider/source kind honestly;
- unsupported native dependencies produce structured statuses;
- no private evidence or large images are required.
```

## Stage 4 - Hash And Signature Analysis

Detailed tickets now live in `tickets/stage-4/`.

Main risk: hashes/signatures over synthetic bytes may look more forensic than they are. Every result must expose provider identity and source status.

## Stage 5 - Documentation Cleanup, Search, And Timeline

Rough tickets now live in `tickets/stage-5/`.

First gate: S5-T00 should clean up documentation organization and duplication before search/timeline starts. It should reconcile `functionality.md`, `progression.md`, `log/`, `tickets/`, and `prompts/vscode-agent/`, and remove or document unused/confusing markdown structures only after preserving unique information.

Main feature risk: search/timeline can become misleading if unsupported parser states are hidden. Results must carry source/provenance/status/warnings. Stage 5 is deferred behind Stage 4.5 and should consume the first-testing handoff, if implemented, without treating stub, synthetic, or dependency-unavailable states as real EWF/filesystem parser output.

## Stage 6 - Reporting And Workflow

Likely tickets:

- bookmark/note result and persistence contracts;
- report item model with provenance and hashes;
- HTML report generation from reviewed result shapes;
- audit-log presentation;
- manual workflow documentation;
- docs and review handoff.

Main risk: reports can overstate findings. Reports must visibly distinguish real parser output, generated fixtures, synthetic providers, unsupported results, partial results, and failed analysis.

## Stage 7 - Advanced Features

Possible later tickets:

- real EWF byte stream integration;
- real partition parsing;
- real filesystem parsing;
- deleted-file recovery from adapter-supported recoverable bytes;
- carving/unallocated-space recovery;
- artifact parsers;
- archive expansion;
- shadow copies;
- encryption detection;
- OCR;
- optional AI triage.

Main risk: these are dependency-heavy and forensic-soundness-heavy. They should not start until the project has stronger real-fixture strategy, optional integration-test policy, and manual workflows.
