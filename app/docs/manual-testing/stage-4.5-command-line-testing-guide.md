# Stage 4.5 Command-Line Testing Guide

Purpose: provide copyable PowerShell commands and review steps for the Stage 4.5 first-testing workflow with user-provided E01 evidence.

This guide is for repository-local manual testing before Stage 5 search/timeline work. It does not add parser behavior, recursive traversal, broad crawl, UI, report-system, deleted recovery, carving, packaging, or search/timeline indexing.

## Current Stage 4.5 Demo Package

S4.5-IMP10 is the reviewed documentation/status refresh for the Stage 4.5 demo runway. User hands-on testing on 2026-07-24 reopened two narrow demo follow-ups before major Stage 5 work.

- S4.5-IMP08 adds an explicit independent full logical-image hash command path and is reviewed/done.
- S4.5-IMP09 adds explicit nested directory navigation, and S4.5-IMP09A is reviewed/done after correcting the default demo to prefer regular-file-visible nested listings when available.
- S4.5-IMP09B is reviewed/done with a live command-line browser over the same reviewed parser-backed directory listing path.
- S4.5-IMP10 packages the final copyable guide and Stage 5 gate packet and is reviewed/done.
- S4.5-IMP11 is reviewed/done for project/inspector/custodian identity fields and logical-image navigation labels.
- S4.5-IMP12 is reviewed/done for accurate full-image hash progress/loading-bar and interrupted-status behavior.

S5-T01 rerun is accepted with a passed-gate result. S5-T02 is the next Stage 5 ticket to prepare.

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

## Hands-On Demo Flow

These commands are intended to be copied from the repository root. They use separate output folders so each proof stays easy to inspect.

Set demo paths:

```powershell
$demoRoot = ".test-artifacts\first-testing"
$noSelectionCase = "$demoRoot\s4-5-demo-no-selection"
$navigationCase = "$demoRoot\s4-5-demo-navigation"
$hashCase = "$demoRoot\s4-5-demo-image-hash"
$selectedCase = "$demoRoot\s4-5-demo-selected-file"
$projectName = "Stage 4.5 Demo"
$inspector = "Demo Inspector"
$custodian = "Demo Custodian"
```

Optional fresh-output cleanup under `.test-artifacts\first-testing\`:

```powershell
foreach ($path in @($noSelectionCase, $navigationCase, $hashCase, $selectedCase)) {
    if (Test-Path -LiteralPath $path) {
        Remove-Item -LiteralPath $path -Recurse -Force
    }
}
```

Run the no-selection E01 workflow:

```powershell
.\.python312-embed\python.exe -m app.backend.api.first_testing --evidence-dir ".\ Test Image" --first-segment "C16242-1-RL1-E003.E01" --case $noSelectionCase --output "$noSelectionCase\outputs" --project-name $projectName --inspector $inspector --custodian $custodian --redact-paths --json-only
```

Inspect the no-selection artifacts without pasting private values:

```powershell
$manifest = Get-Content "$noSelectionCase\run-manifest.json" | ConvertFrom-Json
$root = Get-Content "$noSelectionCase\outputs\root-listing.json" | ConvertFrom-Json
$fileList = Get-Content "$noSelectionCase\outputs\file-list.json" | ConvertFrom-Json
$manifest | Select-Object status, source_modified, read_only_asserted
$manifest.identity | Select-Object project_name, inspector, custodian
$root | Select-Object status, parser_backing, entry_count
$fileList | Select-Object @{Name="status";Expression={$_.status.code}}, entry_count, parser_backing
Import-Csv "$noSelectionCase\outputs\file-list.csv" | Measure-Object
```

Open the static local HTML summary on the local machine:

```powershell
Invoke-Item "$noSelectionCase\outputs\reports\summary.html"
```

Run the nested directory navigation demo:

```powershell
.\.python312-embed\python.exe -m app.backend.api.first_testing --evidence-dir ".\ Test Image" --first-segment "C16242-1-RL1-E003.E01" --case $navigationCase --output "$navigationCase\outputs" --project-name $projectName --inspector $inspector --custodian $custodian --demo-list-first-directory --redact-paths --json-only
```

Inspect the nested navigation artifacts:

```powershell
$navigation = Get-Content "$navigationCase\outputs\navigation-readiness.json" | ConvertFrom-Json
$listing = Get-Content "$navigationCase\outputs\directory-listing.json" | ConvertFrom-Json
$navigation | Select-Object status, selected_directory_entry_count, selected_directory_file_count, selected_depth, real_parser_backed
$listing | Select-Object status, selector_mode, entry_count, file_count, directory_count, other_entry_count, parser_backing, read_only_asserted, source_modified
Import-Csv "$navigationCase\outputs\directory-listing.csv" | Select-Object entry_type, size, allocated, deleted | Format-Table -AutoSize
```

Optional full logical-image hash command. The local logical image is about 1 TB, so this can be long-running; do not claim the hash is complete unless this command actually finishes and `image-hash.json` reports `completed`. While hashing, the command writes a terminal progress line to stderr and updates `image-hash-progress.json` with bytes hashed, percent, elapsed time, throughput, ETA, and current status. With `--json-only`, stdout remains the final parseable run manifest.

```powershell
.\.python312-embed\python.exe -m app.backend.api.first_testing --evidence-dir ".\ Test Image" --first-segment "C16242-1-RL1-E003.E01" --case $hashCase --output "$hashCase\outputs" --hash-image --redact-paths --json-only
```

Inspect `image-hash.json` and `image-hash-progress.json` after a hash run:

```powershell
$imageHash = Get-Content "$hashCase\outputs\image-hash.json" | ConvertFrom-Json
$imageProgress = Get-Content "$hashCase\outputs\image-hash-progress.json" | ConvertFrom-Json
$imageHash | Select-Object status, algorithm, bytes_hashed, logical_media_size, byte_count_matches_media_size, read_only_asserted, source_modified
$imageProgress | Select-Object status, bytes_hashed, logical_media_size, percent_complete, throughput_bytes_per_second, eta_seconds, digest_available
```

The independent image hash is computed over the EWF logical image stream. Stored EWF hash metadata, segment-container file hashes, selected-file hashes, and stub bytes are not this proof. If the user stops hashing before completion, the status is `interrupted`, no digest is written, and the progress artifact preserves the last honest byte count/status.

Run the live command-line browser:

```powershell
.\.python312-embed\python.exe -m app.backend.api.directory_browser --evidence-dir ".\ Test Image" --first-segment "C16242-1-RL1-E003.E01" --project-name $projectName --redact-paths
```

Inside the browser:

```text
dir
cd "<directory name from the current listing>"
dir
cd ..
pwd
help
exit
```

The browser lists actual parser-backed filesystem entries one current directory at a time. Its header and prompt should show the project/logical-image label, not the selected `.E01` segment as the primary navigation root. It is not a recursive crawl, search index, timeline index, content reader, export command, hash command, report generator, or transcript writer.

Selected-file preview/export/hash/signature template only. Replace one placeholder after the user approves a safe, regular, allocated root entry:

```powershell
.\.python312-embed\python.exe -m app.backend.api.first_testing --evidence-dir ".\ Test Image" --first-segment "C16242-1-RL1-E003.E01" --case $selectedCase --output "$selectedCase\outputs" --selected-file-id "<approved-root-entry-file-id>" --selected-file-export-dir "$selectedCase\exports" --redact-paths --json-only
```

Inspect selected-file outputs only after an explicit approved selection:

```powershell
$readiness = Get-Content "$selectedCase\outputs\selected-file-readiness.json" | ConvertFrom-Json
$preview = Get-Content "$selectedCase\outputs\selected-file-preview.json" | ConvertFrom-Json
$analysis = Get-Content "$selectedCase\outputs\selected-file-analysis.json" | ConvertFrom-Json
$export = Get-Content "$selectedCase\outputs\selected-file-export.json" | ConvertFrom-Json
$readiness.status.code
$preview.status
$analysis.status
$export.status
```

Do not auto-select a file from real evidence for shared testing. Do not paste file content or real in-image paths into a shared transcript.

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

Explicit full logical-image hash command. This can be long-running on large evidence, so run it only when the reviewer/user is ready to wait for completion:

```powershell
.\.python312-embed\python.exe -m app.backend.api.first_testing --evidence-dir ".\ Test Image" --first-segment "C16242-1-RL1-E003.E01" --case ".test-artifacts\first-testing\image-hash-real-image" --output ".test-artifacts\first-testing\image-hash-real-image\outputs" --hash-image --redact-paths
```

The hash is computed over the EWF logical image stream, not copied from stored EWF hash metadata, not computed over segment container files, and not derived from selected-file analysis.

Nested directory navigation demo with the local ignored test image:

```powershell
.\.python312-embed\python.exe -m app.backend.api.first_testing --evidence-dir ".\ Test Image" --first-segment "C16242-1-RL1-E003.E01" --case ".test-artifacts\first-testing\nested-navigation-real-image" --output ".test-artifacts\first-testing\nested-navigation-real-image\outputs" --demo-list-first-directory --redact-paths
```

Explicit path form, using a path chosen from a local-only root listing inspection:

```powershell
.\.python312-embed\python.exe -m app.backend.api.first_testing --evidence-dir ".\ Test Image" --first-segment "C16242-1-RL1-E003.E01" --case ".test-artifacts\first-testing\nested-navigation-path" --output ".test-artifacts\first-testing\nested-navigation-path\outputs" --list-directory-path "<approved-directory-path-from-root>" --redact-paths
```

Use either `--list-directory-path` or `--demo-list-first-directory`, not both. The current command does not expose `--list-directory-id`; directory-id selection remains deferred until the parser-backed file-id shape is reviewed as a stable resolver.

Interactive E01 directory browser with the local ignored test image:

```powershell
.\.python312-embed\python.exe -m app.backend.api.directory_browser --evidence-dir ".\ Test Image" --first-segment "C16242-1-RL1-E003.E01" --project-name "Stage 4.5 Demo" --redact-paths
```

Inside the browser:

```text
dir
cd "<directory name from the current listing>"
dir
cd ..
pwd
help
exit
```

The browser keeps a current in-image path, lists direct children only, supports quoted names with spaces, and reports `path_not_directory` if `cd` targets a file. With `--project-name`, its prompt/header uses that logical-image label; without it, the neutral fallback is `Logical Image`. It does not read file contents, export, hash, recurse, search, index, or write a transcript by default.

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

Focused interactive browser checks:

```powershell
.\.python312-embed\python.exe -m pytest app\tests\test_directory_browser.py app\tests\test_directory_listing.py app\tests\test_filesystem_adapter.py
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
    image-hash.json
    image-hash-progress.json
    directory-listing.json
    directory-listing.csv
    navigation-readiness.json
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
$manifest.identity | Select-Object project_name, inspector, custodian
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

Inspect image-hash output:

```powershell
$imageHash = Get-Content "$case\outputs\image-hash.json" | ConvertFrom-Json
$imageProgress = Get-Content "$case\outputs\image-hash-progress.json" | ConvertFrom-Json
$imageHash | Select-Object status, algorithm, bytes_hashed, logical_media_size, byte_count_matches_media_size
$imageProgress | Select-Object status, bytes_hashed, logical_media_size, percent_complete, throughput_bytes_per_second, eta_seconds, digest_available
```

Inspect nested directory navigation output:

```powershell
$navigation = Get-Content "$case\outputs\navigation-readiness.json" | ConvertFrom-Json
$listing = Get-Content "$case\outputs\directory-listing.json" | ConvertFrom-Json
$navigation | Select-Object status, candidate_directory_count, attempted_directory_count, selected_directory_entry_count, selected_directory_file_count, real_parser_backed
$listing | Select-Object status, selector_mode, entry_count, file_count, directory_count, other_entry_count, parser_backing, read_only_asserted, source_modified
Import-Csv "$case\outputs\directory-listing.csv" | Select-Object entry_type, size, allocated, deleted | Format-Table -AutoSize
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
- project, inspector, and custodian identity appear in `run-manifest.json`, `outputs/case.json`, `command-summary.txt`, and `outputs/reports/summary.html` when supplied;
- segment count is 53;
- metadata status is `metadata_available`;
- verification status is `not_supported`;
- EWF stream status is `ok`;
- partition-table volume discovery status is `ok` with 5 volumes;
- filesystem status is `ok`;
- root listing is `real_parser_backed` with 11 entries;
- file-list JSON/CSV status is `ok` with 11 entries;
- image hash status is `not_run` unless `--hash-image` was requested;
- directory navigation status is `not_run` unless `--list-directory-path` or `--demo-list-first-directory` was requested;
- interactive browser status is not represented in the first-testing artifact bundle because `directory_browser` is a live terminal session and does not write transcripts by default;
- static local HTML summary is created;
- selected-file readiness, preview, analysis, and export remain `not_run`;
- `source_modified` is `false`;
- `read_only_asserted` is `true`.

Do not include real metadata values, root-entry names, file paths from inside evidence, or file content in shared notes.

## Expected Nested Navigation Shape

For the local ` Test Image/` nested-navigation demo command, the expected S4.5-IMP09A review shape is:

- command exits 0;
- run status is `ok_with_unsupported_sections`;
- root listing remains `real_parser_backed`;
- directory navigation status is `ok`;
- selector mode is `demo_first_directory` unless an explicit path was supplied;
- nested entry count is greater than zero;
- `file_count` is greater than zero when the bounded two-level demo can find a regular-file-visible listing;
- `selected_depth`, `file_visible`, root candidate attempts, and child candidate attempts are recorded;
- `directory-listing.json`, `directory-listing.csv`, and `navigation-readiness.json` are created;
- selected-file readiness, preview, analysis, and export remain `not_run` unless a separate explicit selected-file option is supplied;
- `source_modified` is `false`;
- `read_only_asserted` is `true`.

Do not quote the selected real directory name, real child entry names, internal paths, metadata values, or file content in shared notes. Report only statuses and counts.

## Expected Interactive Browser Shape

For the local ` Test Image/` browser command, the expected S4.5-IMP09B review shape is:

- browser setup exits cleanly when the scripted or manual session sends `exit` or `quit`;
- browser header and prompt use the supplied project/logical-image label, or `Logical Image` when no project name is supplied;
- startup segment discovery reports 53 segments for the local ignored image;
- root listing is `real_parser_backed` and has a nonzero entry count;
- `dir` or `ls` shows direct child entries for the current path;
- `cd` into a real directory succeeds and a later `dir` or `ls` shows a parser-backed nested listing with a nonzero entry count;
- at least one regular file is visible somewhere in the scripted session when available;
- `cd ..` returns to the parent path;
- attempting to `cd` into a known file reports `path_not_directory`;
- `source_modified` is `false`;
- `read_only_asserted` is `true`.

The local terminal session may show in-image names so the examiner can browse, but shared notes should report only status and count fields.

## Status Meanings

- `ok_with_unsupported_sections`: command orchestration completed, and remaining limits are explicitly listed.
- `ok`: a section completed successfully.
- `metadata_available`: metadata was read through the reviewed adapter path.
- `metadata_unavailable`: metadata could not be read, usually because the adapter dependency is unavailable.
- `dependency_unavailable`: an optional parser dependency such as `pyewf` or `pytsk3` is not importable in the active runtime.
- `not_run`: a section was intentionally not executed, such as selected-file operations without an explicit selection or the default no-hash image-hash path.
- `completed`: requested image-level hashing completed and byte count matched logical media size.
- `failed`: requested image-level hashing started but could not complete honestly.
- `stream_unavailable`: requested image-level hashing could not open a usable EWF logical image stream.
- `interrupted`: requested image-level hashing was stopped before completion; progress/byte count may be preserved, but no digest is available.
- `nested_directory_files_visible`: requested or demo-selected nested directory listing produced nonzero parser-backed entries and at least one regular file.
- `nested_directory_listing_available`: requested or demo-selected nested directory listing produced nonzero parser-backed entries but no regular files were visible in the bounded probe.
- `empty_directory_listing`: requested directory was listed but contained no direct child entries.
- `no_readable_directory`: demo mode did not find a nonempty readable root-directory candidate in the bounded probe set.
- `path_not_found`: requested path was not found by the parser-backed path.
- `path_not_directory`: requested path resolved to a file or other non-directory entry.
- `path_unsupported`: selected adapter cannot list that nested directory path.
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
- an independent full logical-image SHA-256 can be computed only when `--hash-image` is explicitly requested and the command completes;
- image-hash progress can be shown and preserved while hashing, and interrupted runs remain non-success artifacts without a digest;
- one explicit or bounded-demo nested directory can be listed only when `--list-directory-path` or `--demo-list-first-directory` is explicitly requested, and demo mode can probe one child-directory level to prefer a regular-file-visible listing when available;
- live shell-like directory browsing can call the same reviewed parser-backed `list_directory()` path one current directory at a time;
- a static local HTML summary can be created;
- evidence remains read-only and source modification is not asserted.

The no-selection command does not prove:

- nested directory navigation unless a nested directory option is supplied;
- recursive or indexed navigation beyond explicit one-path-at-a-time browser calls;
- recursive directory traversal;
- broad full-volume crawl;
- image-level hashing for normal no-selection runs where `--hash-image` was not requested;
- arbitrary auto-selection, preview, export, hash, or signature analysis;
- full-text extraction from E01 content;
- real selected-file extraction without an approved explicit selection;
- deleted recovery or carving;
- Stage 5 search/timeline;
- UI, dynamic report system, PDF report, packaging, or executable workflow.

Future ownership:

- S4.5-IMP07 owns this command-line guide.
- S4.5-IMP08 owns independent full logical-image hashing and is reviewed/done.
- S4.5-IMP09 owns explicit nested directory navigation and is reviewed/done.
- S4.5-IMP09A owns the file-visible demo correction and nested file-path `path_not_directory` status, and is reviewed/done.
- S4.5-IMP09B owns the interactive command-line navigator for a shell-like `dir`, `cd <folder>`, and back/up workflow, and is reviewed/done.
- S4.5-IMP10 owns the final guide refresh after hash/navigation/browser and is reviewed/done.
- S4.5-IMP11 owns project/inspector/custodian identity and logical-image navigation labels, and is reviewed/done.
- S4.5-IMP12 owns hash progress/loading-bar and interrupted-status behavior, and is reviewed/done.
- A later reviewed ticket must own broad recursive crawl or larger selected-file streaming if those become priorities.
- S5-T01 rerun is accepted with a passed-gate result. S5-T02 is the next Stage 5 ticket to prepare; S5-T03 or later work must wait until earlier Stage 5 tickets are reviewed.

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
Directory navigation status/count/type counts:
Image-hash status/bytes/logical-size:
Browser root/nested status/counts:
Browser parent navigation:
Browser file-target status:
Static HTML summary created:
Selected-file operations:
Source modified:
Read-only asserted:
Artifacts checked:
Skipped or unavailable pieces:
Full image hash skipped/completed:
Privacy notes:
Scope confirmation:
```
