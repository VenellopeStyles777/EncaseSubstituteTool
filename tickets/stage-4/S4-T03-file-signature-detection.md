# S4-T03 - File Signature Detection

Status: Draft

Stage: Stage 4 - Hash and signature foundations

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Detect basic file signatures from bounded bytes supplied by an explicit analysis content provider.

This ticket depends on reviewed S4-T01 contracts and should build beside S4-T02 provider-backed content handling without requiring native libraries such as `python-magic`.

## Expected Scope

- Inspect only a bounded prefix of provider bytes.
- Add a small dependency-free magic-byte table suitable for tests, such as PDF, PNG, JPEG, GIF, ZIP, PE/EXE, ELF, and unknown.
- Return structured statuses for detected signatures, unknown signatures, insufficient bytes, missing content, unsupported source, and invalid requests.
- Preserve source provenance, provider identity, source kind, byte count inspected, max bytes requested, read-only status, timestamp, and warnings.
- Keep detected type/category fields JSON-friendly and conservative.

## Out Of Scope

- MIME database dependency.
- Deep file parsing.
- Extension mismatch checks.
- Known-file matching.
- Whole-file hashing unless already provided by S4-T02.
- Real filesystem extraction, search, timeline, reporting, UI, deleted recovery, carving, or native dependencies.

## Test Expectations

Tests should cover:

- Known magic-byte detections.
- Unknown type.
- Insufficient bytes.
- Missing provider content.
- Directory/metadata-only entries.
- Bounded reads that do not require loading large content.
- Provenance and provider identity preservation.

Run `python -m pytest`.

## Review Checklist

- Signature detection uses provider bytes, not preview-rendered text/hex.
- Detection is conservative and structured when unknown.
- Default tests remain dependency-free.
