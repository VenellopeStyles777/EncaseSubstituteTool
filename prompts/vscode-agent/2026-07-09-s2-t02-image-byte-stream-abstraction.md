# 2026-07-09 - S2-T02 Image Byte-Stream Abstraction Prompt

Use this prompt to hand S2-T02 to the Stage 2 VS Code implementation agent.

```text
Implement ticket S2-T02: Image Byte-Stream Abstraction.

Before editing, read these files:
- tickets/stage-2/S2-T02-image-byte-stream-abstraction.md
- tickets/stage-2/README.md
- app/fixtures/README.md
- app/docs/environment-readiness.md
- app/backend/forensic_core/README.md
- app/backend/api/README.md
- functionality.md
- plan.md
- progression.md
- review.md
- workflow.md

Context:
- Stage 1 is complete.
- S2-T01 fixture/dependency strategy is complete.
- Current focus is only S2-T02.
- This is the first Stage 2 code ticket.
- Do not implement volume discovery yet; that is S2-T03.
- Do not implement filesystem adapters yet; that is S2-T04.
- Do not implement directory listing or preview yet; those are S2-T05/S2-T06.
- Do not add pytsk3, The Sleuth Kit, pyewf, or libewf as required dependencies.
- Do not commit real evidence or binary forensic images.

Your task:
- Add a read-only image/byte-stream abstraction under app/backend/forensic_core/ or another clearly documented backend module.
- Support a simple local file-backed implementation for tiny generated test files.
- Provide structured result/status/error objects for:
  - opening a readable source;
  - missing path;
  - directory instead of file;
  - invalid read ranges;
  - read beyond end behavior.
- Include provenance fields such as source path, size, stream type, read-only assertion, and warnings/status.
- Ensure reads are bounded by offset and length.
- Ensure source files are opened/read in read-only mode only.
- Add tests using tiny generated files under ignored workspace test paths, not real evidence.
- Tests should cover:
  - source metadata/size;
  - reading a byte range;
  - reading at offset zero;
  - read beyond EOF behavior;
  - missing path;
  - directory path;
  - invalid negative offset or length;
  - read-only assertion/status.
- Update app/backend/forensic_core/README.md.
- Update functionality.md for S2-T02 status.
- Update progression.md.
- Add review handoff notes in review.md if useful.
- Run python -m pytest and report the result.

Deliverable:
- A small, tested, read-only byte-stream foundation that later tickets can use for volume discovery and previews.

Stop after S2-T02 and hand off for review. Do not begin S2-T03.
```
