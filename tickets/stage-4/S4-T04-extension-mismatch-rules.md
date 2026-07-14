# S4-T04 - Extension Mismatch Rules

Status: Draft

Stage: Stage 4 - Hash and signature foundations

Owner: VS Code implementation agent

Reviewer: Research/review agent

## Objective

Flag extension/signature mismatches only when both file metadata and detected signature information are available.

This ticket depends on reviewed S4-T03 signature results.

## Expected Scope

- Define extension mismatch result/status structures if S4-T01 did not already include them.
- Compare file name/extension metadata with a conservative mapping from detected signature to expected extensions.
- Return structured states such as match, mismatch, unknown extension, unknown signature, not evaluated, or unsupported content.
- Preserve source provenance, signature result provenance, provider identity, timestamp, and warnings.
- Keep mismatch rules simple, deterministic, and testable.

## Out Of Scope

- Signature detection itself unless a small helper is necessary.
- Deep MIME/category classification.
- User-facing UI flags.
- Search/timeline/reporting.
- Case-store persistence.
- Real parser work or native dependencies.

## Test Expectations

Tests should cover:

- Matching extension/signature pairs.
- Mismatched extension/signature pairs.
- Files without an extension.
- Unknown signatures.
- Non-file entries.
- Provenance and warning preservation.

Run `python -m pytest`.

## Review Checklist

- Mismatch logic does not run when required inputs are missing.
- Unknown or unsupported states are not reported as mismatches.
- Result wording does not imply real parser evidence if provider bytes are synthetic.
