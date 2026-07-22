# 2026-07-15 - S5-T15 Full-Text Search Reality Check Prompt

Use this prompt after S5-T09 and after S4.5 content-provider work has been reviewed.

```text
Implement ticket S5-T15: Full-Text Search Reality Check.

This ticket decides the honest full-text boundary. It is documentation-only unless the reviewer explicitly accepts a contract-only text-record addition.

Before editing, read:
- tickets/stage-5/S5-T02-input-inventory-and-provenance-audit.md
- tickets/stage-5/S5-T03-searchable-record-contracts.md
- tickets/stage-5/S5-T05-file-metadata-search-engine.md
- tickets/stage-5/S5-T15-full-text-search-reality-check.md
- tickets/stage-4.5/S4.5-T05-e01-file-content-provider-plan.md
- app/backend/api/file_preview.py
- app/backend/api/file_export.py
- app/backend/forensic_core/content_analysis.py
- app/backend/forensic_core/search.py
- Goal.md
- plan.md
- functionality.md
- progression.md
- review.md
- workflow.md

Before implementing:
- Confirm whether S4.5-IMP04 produced reviewed E01-backed selected-file content providers.
- State whether full-text search should be deferred, contract-only, or provider-backed text only.
- If the answer is not clear, choose deferred and document why.
- List files you expect to modify.

Your task:
- Decide and document the full-text boundary.
- Confirm preview text, hex/raw previews, file names, export manifests, and stub strings are not automatically full-text evidence indexes.
- If deferred, update docs and logs only.
- If contract-only is approved, define explicit text record provenance/status/warning fields and tests, without extraction.
- If provider-backed text-only is approved, require caller-supplied text records, size limits, source labels, and no automatic file reads.
- Update functionality/plan/progression/review/log docs.
- Run python -m pytest and report the exact result.

Scope boundaries:
- Do not implement automatic text extraction.
- Do not index evidence files.
- Do not use preview-rendered text as a full-text index.
- Do not add persistence, UI, reports, parser behavior, background jobs, commit, or push.

Final handoff:
- Summarize the decision.
- List files changed.
- Report tests.
- State whether any code was added.
- State limitations and next ticket.

Stop after S5-T15 and hand off for review.
```
