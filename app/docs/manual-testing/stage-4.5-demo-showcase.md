# Stage 4.5 Demo Showcase

Purpose: a short, presentable walkthrough for showing the current real-E01 command-line demo without overclaiming what the project can do.

This demo shows that the project can open the local ignored E01 segment set, create a safe case/output workspace, discover segments, read available parser-backed metadata/status, list a real filesystem root, generate file-list and HTML review artifacts, navigate into a nested directory, and use a live terminal browser to move through directory listings.

The 2026-07-24 demo follow-ups are now part of the showcase: S4.5-IMP11 adds project/inspector/custodian identity and better logical-image navigation labels, and S4.5-IMP12 adds accurate progress/loading-bar plus interrupted-status behavior for full-image hashing.

It does not show recursive crawl, search/timeline indexing, deleted recovery, carving, GUI workflow, report generation, or automatic file-content extraction.

## Demo Message

Use this framing:

> This is the first real-evidence command-line demo. It opens an E01 image read-only, builds a named local case/output folder, shows parser-backed filesystem listings, lets me navigate directories in the terminal, and keeps hashing, unsupported areas, and provenance explicit.

Keep shared screenshots or notes privacy-safe. Do not publish private evidence paths, internal filenames, metadata values, or file content unless specifically approved.

## Setup

Open PowerShell from the repository root:

```powershell
cd "C:\Users\cqi\desktop\codexProject\Encase substitute"
```

Use the repository-local portable Python runtime:

```powershell
.\.python312-embed\python.exe --version
```

The local evidence folder used for this demo is ignored by Git:

```powershell
".\ Test Image"
```

## 1. Start With Fresh Outputs

This clears only the demo output folder under `.test-artifacts`.

```powershell
$run = ".test-artifacts\first-testing\demo-showcase"
$projectName = "Stage 4.5 Demo"
$inspector = "Demo Inspector"
$custodian = "Demo Custodian"
if (Test-Path $run) { Remove-Item -LiteralPath $run -Recurse -Force }
```

## 2. Run The Main E01 Demo

```powershell
.\.python312-embed\python.exe -m app.backend.api.first_testing --evidence-dir ".\ Test Image" --first-segment "C16242-1-RL1-E003.E01" --case $run --output "$run\outputs" --project-name $projectName --inspector $inspector --custodian $custodian --demo-list-first-directory --redact-paths
```

What this proves:

- The command accepts the `.E01` first segment and discovers the segment set.
- The evidence is treated read-only.
- A separate case/output workspace is created.
- Project, inspector, and custodian labels are written to the demo artifacts without replacing evidence provenance.
- Parser-backed EWF stream, volume, filesystem, root listing, file-list, nested navigation, and static HTML status artifacts are produced when dependencies and parser support are available.
- Unsupported or not-run areas stay labeled instead of being hidden.

## 3. Inspect The High-Level Summary

```powershell
Get-Content "$run\command-summary.txt"
```

Useful things to point out:

- segment count;
- metadata status;
- verification status;
- EWF stream status;
- volume/filesystem status;
- root listing status;
- file-list output;
- nested navigation status;
- project, inspector, and custodian identity labels;
- selected-file operations are `not_run` unless explicitly selected.

## 4. Inspect The Proof Fields

```powershell
$demo = Get-Content "$run\outputs\demo-readiness.json" -Raw | ConvertFrom-Json
$nav = Get-Content "$run\outputs\navigation-readiness.json" -Raw | ConvertFrom-Json

[pscustomobject]@{
  RootParserBacking = $demo.root_listing_parser_backing
  RootEntryCount = $demo.root_entry_count
  VolumeCount = $demo.volume_count
  NestedStatus = $nav.status
  NestedEntryCount = $nav.selected_directory_entry_count
  FilesVisible = $nav.file_visible
  NestedFileCount = $nav.selected_directory_file_count
  ReadOnlyAsserted = $nav.read_only_asserted
  SourceModified = $nav.source_modified
}
```

For the reviewed local smoke, the important shape was:

- root listing: `real_parser_backed`;
- nested navigation: parser-backed and file-visible;
- read-only asserted: `true`;
- source modified: `false`.

Report counts and statuses in shared notes. Avoid copying internal paths or filenames.

## 5. Open The Visual Summary

```powershell
Invoke-Item "$run\outputs\reports\summary.html"
```

Use this as the visual part of the showcase. It is a static local HTML summary, not a full report system.

What to point out:

- project, inspector, and custodian identity;
- artifact inventory;
- root listing/file-list status;
- parser and dependency status;
- image hash status and progress artifact path;
- unsupported sections;
- selected-file operations remain `not_run` unless explicitly requested.

## 6. Show The Live Directory Browser

Start the browser:

```powershell
.\.python312-embed\python.exe -m app.backend.api.directory_browser --evidence-dir ".\ Test Image" --first-segment "C16242-1-RL1-E003.E01" --project-name $projectName --redact-paths
```

Inside the browser, use a simple sequence:

```text
dir
cd "<directory shown in the listing>"
dir
cd "<child directory shown in the listing>"
dir
cd ..
pwd
help
exit
```

What this proves:

- The browser opens the E01-backed parser path.
- The browser header and prompt use the project/logical-image label instead of the `.E01` segment as the main navigation label.
- `dir` lists actual filesystem entries from inside the image.
- `cd` moves into a real directory only when parser-backed listing succeeds.
- `cd ..` returns to the parent.
- The browser is read-only and does not preview, export, hash, recurse, search, or write transcripts by default.

If a chosen target is a file, the browser should report `path_not_directory` and keep the current directory unchanged.

## 7. Optional Full Logical-Image Hash

This is an important capability, but it can take a long time because the reviewed local image reports about a 1 TB logical media size.

Run it only when you have time:

```powershell
$hashRun = ".test-artifacts\first-testing\demo-image-hash"
if (Test-Path $hashRun) { Remove-Item -LiteralPath $hashRun -Recurse -Force }

.\.python312-embed\python.exe -m app.backend.api.first_testing --evidence-dir ".\ Test Image" --first-segment "C16242-1-RL1-E003.E01" --case $hashRun --output "$hashRun\outputs" --hash-image --redact-paths
```

While it runs, the terminal shows progress on stderr and the command updates `outputs\image-hash-progress.json`. The final command result is still written normally when hashing completes or when an interruption is caught.

Inspect the result and progress:

```powershell
Get-Content "$hashRun\outputs\image-hash.json" -Raw | ConvertFrom-Json
Get-Content "$hashRun\outputs\image-hash-progress.json" -Raw | ConvertFrom-Json
```

What this proves if completed:

- The SHA-256 is computed over the EWF logical image stream.
- It is not copied from stored EWF metadata.
- It is not a hash of the `.E01/.E02/...` container files.
- It records bytes hashed, logical media size, byte-count match, read-only assertion, and source-modified assertion.
- Progress shows bytes hashed, percent, elapsed time, throughput, ETA, and current/final status.
- If stopped with a caught interruption before completion, the status is non-success and no digest is available. A scripted stop or process kill may leave the last progress artifact at `hashing` or `failed`; do not call that a completed hash.

If you skip this during a short demo, say:

> The full image hash is implemented as an opt-in command with progress and interrupted-status artifacts, but I am not running it to completion live because it hashes the full logical image, which is about 1 TB in this local demo.

## 8. Optional Selected-File Template

Only use this after choosing an approved, safe, regular parser-backed root entry. Do not auto-select a file during a shared demo.

```powershell
$selectedRun = ".test-artifacts\first-testing\demo-selected-file"
if (Test-Path $selectedRun) { Remove-Item -LiteralPath $selectedRun -Recurse -Force }

.\.python312-embed\python.exe -m app.backend.api.first_testing --evidence-dir ".\ Test Image" --first-segment "C16242-1-RL1-E003.E01" --case $selectedRun --output "$selectedRun\outputs" --selected-file-id "<approved-root-entry-file-id>" --selected-file-export-dir "$selectedRun\exports" --redact-paths
```

This path is for explicit preview/export/hash/signature over one approved selected file. It is not broad extraction.

## Close The Demo

Good closing summary:

> The current Stage 4.5 demo can open the real E01 set, create a named safe workspace, show parser-backed filesystem listings, navigate folders live, produce file-list and HTML review artifacts, and optionally hash the full logical image with visible progress. The next stage can use only these reviewed, provenance-rich records. Search, timeline, recursive crawl, and UI/reporting remain separate future work.

## Quick Troubleshooting

If `pyewf` or `pytsk3` is missing:

- Use `.\.python312-embed\python.exe`, not the regular `python`.

If the command says the input is unsupported:

- Make sure the selected first segment is `.E01`, not `.E02` or later.

If output overlap is rejected:

- Keep outputs under `.test-artifacts\first-testing\...`, outside the evidence folder.

If the browser cannot `cd` into a path:

- Confirm the target is a directory shown in the current listing.
- Use quotes around names with spaces.
- A file target should produce `path_not_directory`, which is expected.
