# 2026-07-09 - S1-T03 EWF Reader Adapter Prompt

Use this prompt to hand S1-T03 to the VS Code implementation agent.

```text
Implement ticket S1-T03: EWF Reader Adapter Interface.

Before coding, read these files:
- tickets/stage-1/S1-T03-ewf-reader-adapter.md
- tickets/stage-1/README.md
- research/02-e01-ewf-image-format.md
- research/06-tools-plugins-skills.md
- research/08-stack-direction.md
- app/backend/forensic_core/README.md
- app/backend/forensic_core/segment_discovery.py
- app/tests/test_segment_discovery.py
- progression.md
- review.md

Context:
- S1-T01/S1-T01A are complete.
- S1-T02 segment discovery is complete and reviewed.
- Current focus is only S1-T03.
- Do not implement the S1-T04 intake JSON command yet.
- Do not require real E01 evidence.
- Do not require pyewf/libewf to be installed for tests.

Your task:
- Define a clean EWF reader adapter boundary under app/backend/forensic_core/.
- Add stable structured result/data objects for metadata and verification status.
- Add a stub adapter that returns predictable fake metadata for tests.
- Add a graceful pyewf/libewf unavailable path, such as a dependency-unavailable adapter/result/status.
- If you add a real pyewf adapter skeleton, it must fail gracefully when pyewf is not installed.
- Keep segment discovery separate from reader adapter logic.
- Ensure adapter behavior is read-only by design.
- Add tests for:
  - stub metadata response shape
  - verification status field shape
  - dependency-unavailable behavior when pyewf is missing
  - no real evidence required
- Update app/backend/forensic_core/README.md and progression.md.
- Run python -m pytest and report the result.

Stay within S1-T03. Stop after S1-T03 and hand off for review before S1-T04.
```
