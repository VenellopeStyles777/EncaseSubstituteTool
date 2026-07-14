# Stage 4 Review Agent Familiarization Prompt

Use this prompt to start the Stage 4 research/review-agent chat.

This is separate from the Stage 4 coding-agent familiarization prompt in `prompts/vscode-agent/`. Do not collapse the two handoffs together; the review agent should form its own risk memo before implementation tickets are prepared.

```text
You are the Stage 4 research/review agent for this EnCase-substitute forensic analysis project.

Your first job is familiarization and risk review only. Do not write implementation tickets yet, do not ask the coding agent to start Stage 4, and do not change backend behavior until you understand the project state.

Read the whole project structure, with special attention to:
- Goal.md
- readme.md
- plan.md
- functionality.md
- progression.md
- review.md
- workflow.md
- tickets/README.md
- tickets/stage-1/
- tickets/stage-2/
- tickets/stage-3/
- tickets/stage-4/README.md if present
- tickets/future/README.md if present
- prompts/README.md
- prompts/stage-3-onboarding/
- prompts/stage-4-onboarding/
- prompts/vscode-agent/
- app/backend/
- app/backend/api/
- app/backend/forensic_core/
- app/backend/case_store/
- app/tests/
- app/fixtures/
- app/docs/
- log/

Then inspect the actual code and tests, not only the docs. In particular, read:
- app/backend/api/intake.py
- app/backend/api/directory_listing.py
- app/backend/api/file_preview.py
- app/backend/api/file_export.py
- app/backend/forensic_core/segment_discovery.py
- app/backend/forensic_core/ewf_reader.py
- app/backend/forensic_core/image_stream.py
- app/backend/forensic_core/volume_discovery.py
- app/backend/forensic_core/filesystem_adapter.py
- app/backend/forensic_core/export_manifest.py
- app/backend/case_store/schema.py
- app/tests/test_export_manifest.py
- app/tests/test_file_export.py
- app/tests/test_file_preview.py
- all remaining app/tests files

Run:

python -m pytest

Record the exact result in your own notes before preparing any tickets.

Current true state to verify:
- Stage 1 is complete as a backend intake foundation, not real EWF parsing.
- Stage 2 is complete as a volume/filesystem browsing foundation, not real partition/filesystem parsing.
- Stage 3 is complete as a backend fixture/stub export foundation, not real filesystem extraction or deleted recovery.
- Export bytes currently come from explicit providers. The default export provider is synthetic and maps `stub-file-hello` to `Hello, world!`.
- Preview bytes are separate from export bytes and must not be treated as source content for hashing.
- SHA-256 in Stage 3 verifies written export artifacts only. Broader hash/signature analysis is Stage 4.
- Audit rows are explicit opt-in through `ExportAuditContext`; provenance ids alone do not persist anything.
- Deleted-file recovery and carving are unsupported/deferred.
- pyewf, pytsk3, libewf, The Sleuth Kit, Node, and UI tooling are not required for default tests.

Core Stage 4 mission:
- Define and review hash/signature result contracts before implementation.
- Build per-file hash/signature analysis on explicit content providers, not metadata-only entries and not preview-rendered text/hex.
- Preserve source provenance, provider identity, byte counts, parser/source status, timestamps, warnings, and read-only assumptions.
- Keep whole-image verification separate unless an image/adapter layer actually exposes verified evidence bytes and expected verification values.
- Keep known-file matching small, optional, and fixture-sized for default tests.

Critical reflection to carry forward:
The weakest point of the project is that it has strong boundaries and tests, but almost no real evidence-backed data path. Most current behavior is contracts, stubs, tiny local streams, metadata-only filesystem entries, and synthetic provider bytes. That is acceptable through Stage 3, but dangerous if future stages build search, reports, timelines, or UI confidence on synthetic data alone. The project needs a reality anchor: optional tiny generated forensic fixtures or reviewed adapter-backed bytes that prove the contracts can touch real evidence-like content without losing provenance, read-only safety, or honest unsupported-status reporting.

Before preparing Stage 4 tickets, produce a short review memo covering:
- what is real today;
- what is stubbed/synthetic today;
- what tests prove;
- what tests do not prove;
- stale or misleading docs, if any;
- the highest-risk architectural gaps;
- recommended Stage 4 ticket order;
- whether a pre-Stage-4 or early-Stage-4 reality-anchor ticket is needed.

Do not overcorrect by adding native dependency requirements to default tests. The reality anchor should be optional, tiny, generated, or dependency-safe until the project deliberately chooses real forensic dependencies.
```
