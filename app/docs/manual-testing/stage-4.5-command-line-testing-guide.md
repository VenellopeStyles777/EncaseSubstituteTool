# Stage 4.5 Command-Line Testing Guide

Purpose: provide copyable PowerShell commands and review steps for the Stage 4.5 first-testing workflow with user-provided E01 evidence.

This guide is for repository-local manual testing before Stage 5 search/timeline work. It does not add parser behavior, recursive traversal, broad crawl, UI, report-system, deleted recovery, carving, packaging, or search/timeline indexing.

## Prerequisites

- Run every command from the repository root.
- Use normal `python` for dependency-free checks.
- Use the project-local portable runtime for real E01 parser-backed checks:

```powershell
.\.python312-embed\python.exe
```

- Keep real E01 segment folders outside Git tracking. The local ` Test Image/` folder is ignored local evidence and must remain uncommitted.
- Select the first EWF segment, normally `.E01`. Do not select `.E02` or later as the primary input.
- Write case/output artifacts under `.test-artifacts\first-testing\` or another approved non-evidence path.
- Use `--redact-paths` for any command whose console or summary output may be shared.
- Do not paste unredacted evidence paths, case/client names, examiner names, evidence numbers, acquisition notes, root-entry names, or file content unless the user explicitly approves it.

## Safety Rules

- Evidence inputs are read-only.
- Case and output paths must not overlap the evidence folder.
- Do not write outputs beside E01 segments.
- Local JSON artifacts may preserve examiner-owned paths. Shared console text, `command-summary.txt`, screenshots, transcripts, and HTML excerpts should redact private paths as `<EVIDENCE_ROOT>`.
- Selected-file preview/export/hash/signature is opt-in. Do not run it against real evidence unless the user approves a specific safe root entry.

## Basic Commands

Use the portable runtime for real E01 parser-backed examples. Direct `.E01` input:

```powershell
.\.python312-embed\python.exe -m app.backend.api.first_testing "D:\Evidence\Sample.E01" --case ".test-artifacts\first-testing\direct-e01" --output ".test-artifacts\first-testing\direct-e01\outputs" --redact-paths
```

Evidence directory plus explicit first segment:

```powershell
.\.python312-embed\python.exe -m app.backend.api.first_testing --evidence-dir "D:\Evidence\SampleSet" --first-segment "Sample.E01" --case ".test-artifacts\first-testing\evidence-dir" --output ".test-artifacts\first-testing\evidence-dir\outputs" --redact-paths
```

Parseable JSON on stdout:

```powershell
.\.python312-embed\python.exe -m app.backend.api.first_testing "D:\Evidence\Sample.E01" --case ".test-artifacts\first-testing\json-only" --output ".test-artifacts\first-testing\json-only\outputs" --json-only --redact-paths
```

Dependency-free stub smoke with a non-sensitive local dummy filename:

```powershell
New-Item -ItemType Directory -Force ".test-artifacts\first-testing\stub-inputs"
Set-Content -Path ".test-artifacts\first-testing\stub-inputs\stub.E01" -Value "stub" -NoNewline -Encoding ASCII
python -m app.backend.api.first_testing ".test-artifacts\first-testing\stub-inputs\stub.E01" --case ".test-artifacts\first-testing\stub-smoke" --output ".test-artifacts\first-testing\stub-smoke\outputs" --adapter stub --redact-paths
```

Real parser-backed no-selection smoke with the local ignored test image:

```powershell
.\.python312-embed\python.exe -m app.backend.api.first_testing --evidence-dir ".\ Test Image" --first-segment "C16242-1-RL1-E003.E01" --case ".test-artifacts\first-testing\manual-guide-real-image" --output ".test-artifacts\first-testing\manual-guide-real-image\outputs" --redact-paths
```

Selected-file template only. Replace one placeholder after the user approves a safe, regular, allocated root entry:

```powershell
.\.python312-embed\python.exe -m app.backend.api.first_testing --evidence-dir ".\ Test Image" --first-segment "C16242-1-RL1-E003.E01" --case ".test-artifacts\first-testing\manual-guide-selected-file" --output ".test-artifacts\first-testing\manual-guide-selected-file\outputs" --selected-file-id "<approved-root-entry-file-id>" --selected-file-export-dir ".test-artifacts\first-testing\manual-guide-selected-file\exports" --redact-paths
```

Use either `--selected-file-id` or `--selected-file-path`, not both. Do not auto-select a file from the root listing for shared testing.

## Test Commands

Focused parser and first-testing checks:

```powershell
.\.python312-embed\python.exe -m pytest app\tests\test_ewf_reader_adapter.py app\tests\test_image_stream.py app\tests\test_volume_discovery.py app\tests\test_filesystem_adapter.py app\tests\test_directory_listing.py app\tests\test_selected_file_content.py app\tests\test_first_testing_command.py
```

Full suite:

```powershell
.\.python312-embed\python.exe -m pytest
```

## Expected Artifacts

The first-testing command writes a case workspace:

```text
<case>\
  case.db
  run-manifest.json
  command-summary.txt
  outputs\
    intake.json
    case.json
    metadata.json
    verification.json
    segment-discovery.json
    ewf-stream.json
    volumes.json
    filesystems.json
    root-listing.json
    demo-readiness.json
    selected-file-readiness.json
    selected-file-preview.json
    selected-file-analysis.json
    selected-file-export.json
    file-list.json
    file-list.csv
    audit.json
    unsupported-sections.json
    reports\
      summary.html
```

`summary.html` is a static local status/artifact summary. It is not a UI, search/timeline index, report system, or PDF report.

## Inspection Steps

Set a case variable for the run you want to inspect:

```powershell
$case = ".test-artifacts\first-testing\manual-guide-real-image"
```

Read the command summary:

```powershell
Get-Content "$case\command-summary.txt"
```

Inspect the manifest without exposing private paths in shared notes:

```powershell
$manifest = Get-Content "$case\run-manifest.json" | ConvertFrom-Json
$manifest | Select-Object status, source_modified, read_only_asserted
```

Inspect metadata and verification statuses:

```powershell
(Get-Content "$case\outputs\metadata.json" | ConvertFrom-Json).status
(Get-Content "$case\outputs\verification.json" | ConvertFrom-Json).status
```

Inspect stream, volume, filesystem, and root-listing status:

```powershell
(Get-Content "$case\outputs\ewf-stream.json" | ConvertFrom-Json).status
(Get-Content "$case\outputs\volumes.json" | ConvertFrom-Json) | Select-Object status, strategy, volume_count
(Get-Content "$case\outputs\filesystems.json" | ConvertFrom-Json).status
(Get-Content "$case\outputs\root-listing.json" | ConvertFrom-Json) | Select-Object status, parser_backing, entry_count
```

Inspect file-list output:

```powershell
$fileList = Get-Content "$case\outputs\file-list.json" | ConvertFrom-Json
$fileList | Select-Object @{Name="status";Expression={$_.status.code}}, entry_count, root_listing_status
Import-Csv "$case\outputs\file-list.csv" | Measure-Object
```

Open the local static HTML summary only on the local machine:

```powershell
Invoke-Item "$case\outputs\reports\summary.html"
```

Confirm selected-file operations were not run in the no-selection smoke:

```powershell
$readiness = Get-Content "$case\outputs\selected-file-readiness.json" | ConvertFrom-Json
$readiness.status.code
(Get-Content "$case\outputs\selected-file-preview.json" | ConvertFrom-Json).status
(Get-Content "$case\outputs\selected-file-analysis.json" | ConvertFrom-Json).status
(Get-Content "$case\outputs\selected-file-export.json" | ConvertFrom-Json).status
```

Check unsupported sections:

```powershell
(Get-Content "$case\outputs\unsupported-sections.json" | ConvertFrom-Json).sections
```

Before sharing a transcript, confirm:

- `source_modified` is `false`;
- `read_only_asserted` is `true`;
- output paths are outside the evidence folder;
- selected-file artifacts are `not_run` when no file was selected;
- no private metadata, root-entry names, file paths from inside evidence, or file content is pasted.

## Expected Local No-Selection Shape

For the local ` Test Image/` command, the reviewed expected shape is:

- command exits 0;
- run status is `ok_with_unsupported_sections`;
- segment count is 53;
- metadata status is `metadata_available`;
- verification status is `not_supported`;
- EWF stream status is `ok`;
- partition-table volume discovery status is `ok` with 5 volumes;
- filesystem status is `ok`;
- root listing is `real_parser_backed` with 11 entries;
- file-list JSON/CSV status is `ok` with 11 entries;
- static local HTML summary is created;
- selected-file readiness, preview, analysis, and export remain `not_run`;
- `source_modified` is `false`;
- `read_only_asserted` is `true`.

Do not include real metadata values, root-entry names, file paths from inside evidence, or file content in shared notes.

## Status Meanings

- `ok_with_unsupported_sections`: command orchestration completed, and remaining limits are explicitly listed.
- `ok`: a section completed successfully.
- `metadata_available`: metadata was read through the reviewed adapter path.
- `metadata_unavailable`: metadata could not be read, usually because the adapter dependency is unavailable.
- `dependency_unavailable`: an optional parser dependency such as `pyewf` or `pytsk3` is not importable in the active runtime.
- `not_run`: a section was intentionally not executed, such as selected-file operations without an explicit selection.
- `not_supported`: the installed adapter does not expose a reviewed safe API for that action, such as EWF verification.
- `verification_ok`: verification ran and reported success.
- `verification_failed`: verification ran and reported failure.
- `unsafe_output_path`: evidence, case, or output paths overlap unsafely and the command refused to write artifacts.
- `invalid_input`: the selected input is missing, unsupported, conflicting, or not the first `.E01` segment.

## Troubleshooting

Missing `pyewf`:

- Use `.\.python312-embed\python.exe` for real E01 parser-backed checks.
- If using normal `python`, expect dependency-unavailable metadata or stream status unless the dependency is installed there.

Missing `pytsk3`:

- Root filesystem listing will be unavailable or dependency-blocked.
- Use the portable runtime for the reviewed local path.

Selected `.E02` by mistake:

- Select the `.E01` first segment instead. Later segments are discovered as siblings.

Output path overlaps evidence:

- Move `--case` and `--output` under `.test-artifacts\first-testing\` or another non-evidence folder.

Unsupported filesystem or content path:

- Record the structured status and warning. Do not substitute stub bytes while claiming real parser-backed output.

Redaction:

- `--redact-paths` redacts console and summary paths, but local JSON can keep examiner-owned paths. Do not share local JSON extracts without checking for private values.

## Proof Boundaries

The no-selection real-image command can prove:

- a safe case workspace can be created;
- E01 segment discovery can process a real local segment set;
- best-effort metadata can be attempted through `pyewf`;
- verification status is separate from metadata;
- an EWF-backed logical stream can be opened when dependencies support it;
- partition-table volumes can be discovered;
- a real-parser-backed root filesystem listing can be produced;
- root-listing-derived file-list JSON/CSV can be written;
- a static local HTML summary can be created;
- evidence remains read-only and source modification is not asserted.

The no-selection command does not prove:

- recursive or nested directory traversal;
- broad full-volume crawl;
- arbitrary auto-selection, preview, export, hash, or signature analysis;
- full-text extraction from E01 content;
- real selected-file extraction without an approved explicit selection;
- deleted recovery or carving;
- Stage 5 search/timeline;
- UI, dynamic report system, PDF report, packaging, or executable workflow.

Future ownership:

- S4.5-IMP07 owns this command-line guide.
- A later reviewed ticket must own recursive traversal, broad crawl, or larger selected-file streaming if those become priorities.
- S5-T01 must be rerun after S4.5-IMP07 review before S5-T02 or later search/timeline work starts.

## Reviewer Transcript Template

```text
Ticket:
Command run:
Evidence path redacted as: <EVIDENCE_ROOT>
Output path:
Exit code:
Run status:
Segment count:
Metadata status:
Verification status:
EWF stream status:
Volume strategy/status/count:
Filesystem status:
Root-listing backing/count:
File-list JSON/CSV status/count:
Static HTML summary created:
Selected-file operations:
Source modified:
Read-only asserted:
Artifacts checked:
Skipped or unavailable pieces:
Privacy notes:
Scope confirmation:
```
