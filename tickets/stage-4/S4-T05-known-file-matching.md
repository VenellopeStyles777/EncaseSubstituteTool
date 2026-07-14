# S4-T05 - Fixture-Sized Known-File Matching

Status: Draft

Stage: Stage 4 - Hash and signature foundations

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Plan or add a very small known-file matching foundation after hash result contracts and provider-backed hashing are reviewed.

Known-file matching must remain fixture-sized for default tests. Do not introduce NSRL-scale data, downloads, network access, or required external databases.

## Expected Scope Options

Choose one after S4-T02 review:

- Documentation/planning only, if result contracts need more settling.
- Minimal in-memory matching against a tiny caller-supplied list of digest records.

If implemented, preserve:

- digest algorithm and digest value;
- match category such as known-good, known-bad, or unknown;
- dataset/provider identity;
- dataset version or label when supplied;
- source hash result id/provenance;
- warnings and timestamp.

## Out Of Scope

- NSRL import.
- Database-scale matching.
- Case-store persistence unless S4-T06 explicitly approves it.
- Network downloads.
- UI filtering.
- Search/timeline/reporting.

## Test Expectations

If implementation proceeds, tests should cover:

- match and no-match cases;
- unsupported or missing hash algorithm;
- duplicate/conflicting known-file entries as warnings or structured non-ok status;
- JSON serialization;
- no network or external files.

Run `python -m pytest`.

## Review Checklist

- Known-file data is tiny, explicit, and dependency-free.
- Matching does not overstate synthetic/provider-backed hash results.
- Persistence and large imports remain deferred.
