# User-Provided E01 Inputs

Purpose: document how Stage 4.5 manual testing should use real E01 files supplied by the user.

Do not place real evidence files in this committed folder. This folder is documentation only.

## Rules

- Do not commit `.E01`, `.E02`, `.Ex01`, raw images, filesystem images, or private case files.
- Provide E01 paths at command time, or store local-only scratch inputs under ignored paths such as `.test-artifacts/first-testing/`.
- Treat all user-provided E01 files and sibling segments as read-only.
- Write output summaries only to explicit output directories that do not overlap the evidence folder.
- Redact sensitive source paths before sharing logs, screenshots, or review summaries outside the local machine.

## Stage 4.5 Intended Input Shape

Preferred manual test input:

```text
X:\path\to\sample.E01
X:\path\to\sample.E02
X:\path\to\sample.E03
```

The selected path should be the first segment, normally `.E01`.

Supported input forms for planned Stage 4.5 work:

- direct `.E01` path;
- evidence folder plus explicit first-segment filename;
- ignored local run configuration under `.test-artifacts/first-testing/`.

Selecting `.E02` or later segments as the primary evidence path should be treated as invalid input with guidance to select `.E01`.

## Output Location Rules

Manual-test outputs should live under an explicit case/output folder, for example:

```text
.test-artifacts/first-testing/local-runs/case-a/
```

Outputs should not overlap the evidence folder. Exports, summaries, file lists, logs, manifests, and reports should never be written beside the E01 segment set.

## Redaction Rules

Shared logs or screenshots should redact private local paths as `<EVIDENCE_ROOT>` and should avoid exposing case names, client names, user names, serial numbers, acquisition notes, or examiner names unless the user approves.

## Current Project Behavior With Real E01 Inputs

Current code can inspect sibling filenames and produce structured segment discovery output.

Current code does not yet read real EWF metadata, verify the EWF image, parse partitions, parse filesystems, or extract file bytes from the E01. Those behaviors need Stage 4.5 implementation tickets before they can be demonstrated honestly.
