# S4-T00 - Review-Agent Risk Audit

Status: Done

Stage: Stage 4 - Hash and signature foundations

Owner: Research/review agent

Reviewer: User

## Objective

Complete Stage 4 familiarization and produce a risk memo before any implementation ticket is handed to the VS Code coding agent.

This ticket is planning/review work only. It must not change backend behavior or ask the implementation agent to start Stage 4.

## Context Read

- `prompts/stage-4-onboarding/stage-4-review-agent-familiarization-prompt.md`
- `prompts/stage-4-onboarding/project-reflection-and-forward-risks.md`
- `prompts/vscode-agent/2026-07-14-stage-4-familiarization.md`
- `Goal.md`
- `readme.md`
- `plan.md`
- `functionality.md`
- `progression.md`
- `review.md`
- `workflow.md`
- `tickets/`
- `prompts/`
- `app/backend/`
- `app/tests/`
- `app/fixtures/`
- `app/docs/`
- `log/`

## Current Findings

Real today:

- Tiny local files can be read through `LocalFileImageStream` in read-only binary mode.
- Export writes use explicit export-provider bytes, safe destination checks, exclusive create writes, manifests, SHA-256 from the written artifact, and optional explicit audit context.
- Case-store audit rows exist only when called explicitly.

Stubbed or synthetic today:

- EWF adapter behavior is stubbed or dependency-unavailable.
- Whole-image volume discovery is a boundary and not a partition parser.
- Filesystem entries are metadata-only stubs unless a future adapter supplies real entries.
- Preview bytes and export bytes are provider-backed; default providers are synthetic.

What tests prove:

- Current contracts serialize cleanly.
- Current stubs and dependency-unavailable paths behave predictably.
- Source read-only assertions, destination overwrite refusal, partial-write cleanup, export SHA-256 from disk, audit opt-in, and deleted recovery deferral are covered.

What tests do not prove:

- Real EWF parsing.
- Real image verification.
- Real partition/filesystem parsing.
- Real evidence-derived file-content extraction.
- Real deleted recovery or carving.
- Real hash/signature findings from parsed evidence.

## Highest Risks

- Stage 4 could make synthetic provider bytes look like real evidence analysis.
- Hash/signature code could accidentally reuse rendered preview text/hex instead of source bytes.
- Per-file hashing could be confused with Stage 3 export-output verification or future whole-image verification.
- Stage 5 search/timeline could index synthetic-only results and make the product surface look more complete than the evidence pipeline is.

## Decision

Stage 4 can proceed, but only in narrow steps:

1. Contract-first result/provenance design.
2. Provider-backed hashes over explicitly supplied bytes.
3. Bounded signature detection over explicitly supplied bytes.
4. Extension mismatch only when metadata and signature results are both available.
5. Known-file matching and persistence after result shapes are reviewed.

Default tests must remain dependency-free.

## Verification

```powershell
python -m pytest
```

Result: `99 passed in 6.46s`.
