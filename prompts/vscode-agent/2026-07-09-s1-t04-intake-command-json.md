# 2026-07-09 - S1-T04 Intake Command JSON Prompt

Use this prompt to hand S1-T04 to the VS Code implementation agent.

```text
Implement ticket S1-T04: Intake Command JSON Output.

Before coding, read these files:
- tickets/stage-1/S1-T04-intake-command-json.md
- tickets/stage-1/README.md
- research/02-e01-ewf-image-format.md
- app/backend/forensic_core/segment_discovery.py
- app/backend/forensic_core/ewf_reader.py
- app/backend/api/README.md
- app/backend/README.md
- app/tests/test_segment_discovery.py
- app/tests/test_ewf_reader_adapter.py
- progression.md
- review.md

Context:
- S1-T02 segment discovery is complete.
- S1-T03 EWF reader adapter boundary is complete.
- Current focus is only S1-T04.
- Do not implement SQLite case storage yet; that is S1-T05.
- Do not parse real EWF bytes.
- Do not require pyewf/libewf or real E01 evidence.

Your task:
- Add a backend intake command/module under app/backend/api/ or another clearly documented backend command boundary.
- The command/callable should accept a selected .E01 path.
- It should run discover_e01_segments().
- It should use an EWF reader adapter, defaulting to dependency-safe behavior. For tests, use StubEwfReaderAdapter or injectable adapter behavior.
- Return structured JSON or a JSON-serializable dict combining:
  - selected/source path
  - segment discovery result
  - adapter name/availability/dependency status
  - metadata result
  - verification status
  - warnings
  - read-only assertion
- Invalid input should produce predictable structured output or a documented non-zero CLI behavior, not a raw traceback for normal user mistakes.
- Add tests for:
  - successful stub-backed intake output shape
  - unsupported input extension
  - missing selected .E01 path behavior
  - dependency-unavailable adapter output if using PyewfEwfReaderAdapter
- Update app/backend/api/README.md and app/backend/README.md with command/callable usage.
- Update progression.md.
- Run python -m pytest and report the result.

Stay within S1-T04. Stop after S1-T04 and hand off for review before S1-T05.
```
