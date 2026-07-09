# 2026-07-09 - S2-T06 Review Fix: Offset Beyond Content

Use this prompt to hand the S2-T06 review fix to the Stage 2 VS Code implementation agent.

```text
Fix the S2-T06 review finding only. Do not begin S2-T07 or Stage 3.

Before editing, read:
- review.md, especially `2026-07-09 - S2-T06 Review`
- app/backend/api/file_preview.py
- app/tests/test_file_preview.py
- tickets/stage-2/S2-T06-preview-foundation.md
- progression.md

Finding:
- `preview_file()` currently reports `status.code == "ok"` when `offset` is beyond the available preview content and `length` is omitted.
- Example: `/hello.txt` has 13 stub bytes, but `preview_file(entry, mode="text", offset=99)` returns `ok`, zero bytes, empty text, and no truncation warning.
- A preview offset outside the content should be a structured non-ok status or warning, such as `preview_truncated`, `content_unavailable`, or a dedicated range status. Pick the status that best matches the existing S2-T06 status style and document it through the test.

Required work:
- Add a regression test for `offset > source_content_size` with omitted `length`.
- Update `preview_file()` so this case no longer reports `ok`.
- Preserve JSON-friendly output, provenance fields, read-only fields, and existing behavior for valid ranges.
- Keep the fix scoped to S2-T06.
- Update progression.md with the fix result.
- Update review.md with a brief handoff note if useful.
- Run `python -m pytest` and report the result.

Stop after this fix and hand off for re-review. Do not commit, push, begin S2-T07, or begin Stage 3.
```
