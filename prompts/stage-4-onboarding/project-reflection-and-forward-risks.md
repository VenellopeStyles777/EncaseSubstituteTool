# Project Reflection And Forward Risks

Date: 2026-07-14

Author: Stage 3 research/review agent

Scope: review-agent reflection only. This is not the coding-agent predecessor handoff. It should be kept separate from `prompts/vscode-agent/` because the coding agent's reflection can focus on implementation mechanics, while this memo focuses on review risk, forensic soundness, and future-stage guardrails.

## Short Version

The project's strongest trait is disciplined boundaries: read-only assumptions, provenance-rich result shapes, explicit providers, dependency-safe stubs, and staged review.

The weakest point is that the project still has no real evidence-backed content path. Most behavior is correct as scaffolding, but it is scaffolding: metadata stubs, synthetic preview/export bytes, whole-image volume placeholders, and dependency-unavailable parser skeletons.

That is fine through Stage 3. It becomes dangerous if Stage 4 through Stage 6 build impressive-looking hash, signature, search, timeline, report, or UI workflows that still only exercise synthetic bytes.

## What Needs Improvement Most

The project needs a reality anchor.

A reality anchor means at least one tiny, known, non-private, repeatable path where bytes and metadata come from something closer to real evidence than hard-coded stub providers. This could be:

- a tiny generated raw fixture with known bytes and provenance;
- a tiny generated filesystem image if safe tooling is available;
- an optional local-only pytsk3/libewf integration check;
- a reviewed adapter-backed content provider that reads from `ImageByteStream` ranges rather than from an in-memory stub map.

The key is not "add big forensic dependencies now." The key is to prevent later stages from mistaking synthetic provider behavior for forensic capability.

## Strategic Risk

If the project keeps adding features on top of synthetic providers only, the apparent product surface will grow faster than its forensic truth. That creates several risks:

- hashes may look authoritative while only proving synthetic fixtures;
- signatures may classify provider bytes that were never extracted from a filesystem;
- reports may imply stronger evidence provenance than the parser layer can support;
- UI work may hide unsupported parsing states behind polished workflows;
- deleted recovery and carving may become marketing words rather than adapter-backed capabilities;
- case-store records may preserve results without enough source/adapter uncertainty.

## Review-Agent Guidance

Every future stage should ask:

- What bytes are being analyzed?
- Who provided those bytes?
- Are they synthetic, generated fixture, local raw stream, or real parser output?
- Does the result preserve source path, volume id, file id/path, offsets/ranges where known, provider identity, read-only status, parser/source status, byte count, warnings, and timestamp?
- Does the UI or report show uncertainty and unsupported states?
- Does the default test suite remain dependency-safe?

## Stage 4 Implications

Stage 4 should still start with contracts and provider-backed hashing/signature analysis. That is the right next slice.

But Stage 4 should include an explicit early review gate for the reality-anchor problem:

- Do not hash preview-rendered text or hex.
- Do not treat metadata-only filesystem entries as byte-bearing objects.
- Do not claim whole-image verification.
- Do not add native dependencies to default tests.
- Do design hash/signature results so future real adapter bytes can be identified clearly.
- Do consider a tiny generated or optional fixture-backed content provider before Stage 5 search/timeline begins.

## Later Stage Warnings

Stage 5 search/timeline should not become a search engine over fake data only. It needs either a reality anchor or brutally clear labels that results are stub/provider-backed.

Stage 6 reporting/workflow must preserve uncertainty. Reports should not flatten dependency-unavailable, parser-not-implemented, synthetic-provider, unsupported-recovery, or partial-result statuses into polished "evidence found" language.

Stage 7 advanced features should stay deferred until real parsing, fixture strategy, and manual workflows are mature. Carving, artifact parsing, shadow copies, encryption detection, OCR, and AI triage would be premature before real evidence-backed byte paths exist.

## Recommended Next Step

Before handing S4-T01 to the coding agent, the Stage 4 review agent should complete a whole-project familiarization and risk memo. If that memo confirms the current assessment, add or prioritize an early Stage 4 ticket for a hash/signature content-source contract that explicitly distinguishes synthetic, generated-fixture, local-stream, and future real-parser bytes.
