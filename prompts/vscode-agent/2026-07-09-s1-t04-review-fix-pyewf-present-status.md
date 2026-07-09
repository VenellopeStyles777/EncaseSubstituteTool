# 2026-07-09 - S1-T04 Review Fix Prompt

Use this prompt to ask the VS Code implementation agent to fix the S1-T04 review finding.

```text
Fix S1-T04 review finding: intake status is misleading when pyewf is importable but real metadata extraction is not implemented.

Read first:
- app/backend/api/intake.py
- app/backend/forensic_core/ewf_reader.py
- app/tests/test_intake_command.py
- review.md
- tickets/stage-1/S1-T04-intake-command-json.md

Problem:
- run_e01_intake() currently sets status to "ok" whenever adapter_available is true.
- PyewfEwfReaderAdapter can be available/importable while still returning empty metadata and a "real_reader_not_implemented" warning.
- In that case, intake output says status "ok", which is misleading.

Required fix:
- Adjust run_e01_intake() so an importable-but-not-implemented pyewf adapter does not produce status "ok".
- Use a clear status such as "metadata_unavailable" or "reader_not_implemented".
- Add a regression test that injects a fake pyewf module into PyewfEwfReaderAdapter, runs intake against a dummy .E01, and asserts:
  - status is not "ok"
  - metadata is empty
  - warning code includes "real_reader_not_implemented"
- Keep stub-backed intake success returning status "ok".
- Keep pyewf-missing dependency behavior unchanged.
- Run python -m pytest.
- Update progression.md with the fix result.

Stay within S1-T04. Do not begin S1-T05.
```
