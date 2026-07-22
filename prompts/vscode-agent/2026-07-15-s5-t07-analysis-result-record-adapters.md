# 2026-07-15 - S5-T07 Analysis Result Record Adapters Prompt

Use this prompt only after S5-T06 is accepted.

```text
Implement ticket S5-T07: Analysis Result Record Adapters.

Adapt reviewed Stage 4 analysis results into SearchableRecord values. Do not search those records yet.

Before editing, read:
- tickets/stage-4/README.md
- tickets/stage-4/S4-T01-hash-signature-contracts.md
- tickets/stage-4/S4-T02-provider-backed-hashing.md
- tickets/stage-4/S4-T03-file-signature-detection.md
- tickets/stage-4/S4-T04-extension-mismatch-rules.md
- tickets/stage-4/S4-T05-known-file-matching.md
- tickets/stage-5/S5-T03-searchable-record-contracts.md
- tickets/stage-5/S5-T07-analysis-result-record-adapters.md
- app/backend/forensic_core/content_analysis.py
- app/backend/forensic_core/search.py
- app/tests/test_content_analysis_contracts.py
- app/tests/test_content_analysis_hashing.py
- app/tests/test_content_analysis_signatures.py
- app/tests/test_content_analysis_extension_mismatch.py
- app/tests/test_content_analysis_known_files.py
- Goal.md
- plan.md
- functionality.md
- progression.md
- review.md
- workflow.md

Before implementing:
- Confirm S4-T01 through S4-T05 are reviewed/done.
- Summarize which analysis result classes will be adapted.
- State that no analysis will be recomputed.
- List files you expect to modify.

Your task:
- Add explicit adapters for hash, signature, extension mismatch, and known-file match results.
- Map analysis fields into searchable fields.
- Preserve source provenance, content-source identity, source kind, synthetic/generated flags, statuses, warnings, timestamps, and parser/provider names.
- Carry timestamps raw; do not normalize them.
- Add dependency-free tests using Stage 4 fixture-style results.
- Update docs and ticket status.
- Run python -m pytest and report the exact result.

Scope boundaries:
- Do not call hash_file_content, detect_file_signature, evaluate_extension_mismatch, or match_known_file_hashes from adapters.
- Do not read bytes, import datasets, implement search matching, timeline, persistence, UI, reporting, parser behavior, full-text search, commit, or push.

Final handoff:
- Summarize files changed.
- Summarize adapters added.
- Report tests.
- State limitations and next ticket.

Stop after S5-T07 and hand off for review.
```
