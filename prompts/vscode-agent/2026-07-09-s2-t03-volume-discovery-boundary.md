# 2026-07-09 - S2-T03 Volume Discovery Boundary Prompt

Use this prompt to hand S2-T03 to the Stage 2 VS Code implementation agent.

```text
Implement ticket S2-T03: Volume Discovery Boundary.

Before editing, read these files:
- tickets/stage-2/S2-T03-volume-discovery-boundary.md
- tickets/stage-2/README.md
- app/backend/forensic_core/image_stream.py
- app/backend/forensic_core/README.md
- app/fixtures/README.md
- app/docs/environment-readiness.md
- functionality.md
- plan.md
- progression.md
- review.md
- workflow.md

Context:
- Stage 1 is complete.
- S2-T01 fixture/dependency strategy is complete.
- S2-T02 read-only image byte-stream abstraction is complete.
- Current focus is only S2-T03.
- Do not implement filesystem adapters yet; that is S2-T04.
- Do not implement directory listing or preview yet; those are S2-T05/S2-T06.
- Do not add pytsk3, The Sleuth Kit, pyewf, or libewf as required dependencies.
- Do not commit real evidence or binary forensic images.

Your task:
- Add a volume discovery boundary under app/backend/forensic_core/ or another clearly documented backend module.
- Define JSON-serializable volume result structures.
- Support a simple whole-image volume discovery path for LocalFileImageStream or a tiny generated file fixture.
- Include provenance fields such as source path, stream type, source size, volume id, volume index, offset, length/size, description/type/status, read-only assertion, and warnings.
- Add structured status for:
  - successful whole-image volume result;
  - missing/unreadable image stream;
  - empty image/zero-byte source;
  - unsupported real partition parsing if represented.
- Do not parse real partition tables yet unless it can be done safely without broadening scope. A whole-image/single-volume result is sufficient for S2-T03.
- Add tests using tiny generated files and/or stream stubs.
- Tests should cover:
  - whole-image volume result for a non-empty local file;
  - zero-byte source behavior;
  - missing source behavior;
  - JSON/dict serialization shape;
  - read-only assertion/provenance.
- Update app/backend/forensic_core/README.md.
- Update functionality.md for S2-T03 status.
- Update progression.md.
- Add review handoff notes in review.md if useful.
- Run python -m pytest and report the result.

Deliverable:
- A small, tested volume discovery boundary that later filesystem adapter tickets can consume.

Stop after S2-T03 and hand off for review. Do not begin S2-T04.
```
