# 2026-07-09 - S2-T04 Filesystem Adapter Boundary Prompt

Use this prompt to hand S2-T04 to the Stage 2 VS Code implementation agent.

```text
Implement ticket S2-T04: Filesystem Adapter Boundary.

Before editing, read these files:
- tickets/stage-2/S2-T04-filesystem-adapter-boundary.md
- tickets/stage-2/README.md
- app/backend/forensic_core/image_stream.py
- app/backend/forensic_core/volume_discovery.py
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
- S2-T03 volume discovery boundary is complete.
- Current focus is only S2-T04.
- Do not implement directory listing workflows beyond adapter boundary behavior; S2-T05 is the directory listing/file metadata view.
- Do not implement raw/text/hex preview; that is S2-T06.
- Do not add pytsk3 or The Sleuth Kit as required dependencies.
- Do not parse real filesystems as a required path.
- Do not commit real evidence or filesystem images.

Your task:
- Add a filesystem adapter boundary under app/backend/forensic_core/ or another clearly documented backend module.
- Define JSON-serializable filesystem result/status/warning structures.
- Define a file/directory entry metadata shape suitable for later S2-T05 listing.
- Add a deterministic stub filesystem adapter that can return a root directory tree or root entries for tests.
- Add an optional pytsk3 adapter skeleton or dependency-status path that reports `dependency_unavailable` when pytsk3 is missing.
- Include provenance fields such as source path, volume id, volume offset/length, filesystem type, adapter name, read-only assertion, file id/path/name/type/size, allocation/deleted status when available, and warnings/status.
- Keep the adapter boundary separate from S2-T05 command/workflow.
- Add tests for:
  - stub adapter metadata/result shape;
  - stub root entries;
  - read-only assertions;
  - dependency-unavailable behavior for pytsk3;
  - JSON/dict serialization shape;
  - no real evidence/native dependency requirement.
- Update app/backend/forensic_core/README.md.
- Update functionality.md for S2-T04 status.
- Update progression.md.
- Add review handoff notes in review.md if useful.
- Run python -m pytest and report the result.

Deliverable:
- A dependency-safe filesystem adapter boundary that later S2-T05 directory listing work can consume.

Stop after S2-T04 and hand off for review. Do not begin S2-T05.
```
