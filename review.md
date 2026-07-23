# Review - Code and Architecture Review Notes

Purpose: use this file for findings from research/review agents. Keep reviews focused on defects, forensic-soundness risks, data-integrity risks, missing tests, and architecture drift.

Review priorities for this project:

- Evidence must be opened read-only unless an explicit export/write operation targets a separate output path.
- Every parsed file, exported file, hash, and report item should preserve source provenance.
- Long operations need cancellation, progress, and error recovery.
- Tests should use known tiny forensic images or generated fixtures, not uncontrolled real evidence.
- UI convenience must not hide evidence integrity state, parsing errors, or unsupported filesystem/image features.

## Current Review Queue

## 2026-07-23 - S5-T01 Rerun Review Acceptance

Result: accepted. S5-T01 rerun is done with a passed-gate result.

Findings:

- No blocking findings.
- The gate correctly treats the July 16 failed S5-T01 result as historical.
- S4.5-IMP01 through S4.5-IMP10 satisfy the Stage 4.5 substantial-test runway for this gate.
- Stage 5 search/timeline implementation has not started; S5-T02 remains Draft and is the next ticket to prepare.
- Allowed and blocked Stage 5 inputs preserve the main proof boundaries: `not_run` image hashes are not digest proof, static HTML is not an authoritative index, browser/navigation is not recursive crawl, and selected-file content remains explicit-selection only.

Verification:

- Full reviewer run: `.\.python312-embed\python.exe -m pytest`: 207 passed in 41.53s.
- Reviewer real-image no-selection/navigation smoke exited 0 with `ok_with_unsupported_sections`, 53 segments, metadata `metadata_available`, verification `not_supported`, EWF stream `ok`, logical media size 1,024,209,543,168 bytes, 5 volumes, filesystem `ok`, root listing `real_parser_backed` with 11 entries, file-list JSON/CSV `ok` with 11 entries, nested directory listing `real_parser_backed` with 19 entries, files=19, directories=0, other=0, navigation `nested_directory_files_visible`, static HTML created, image hash `not_run`, selected-file operations `not_run`, `source_modified: false`, and `read_only_asserted: true`.
- Full `--hash-image` was intentionally not run because the local logical image is about 1 TB and the command is documented as long-running.

Next:

- Prepare S5-T02 as the next ticket.
- Do not start S5-T03 or later until earlier Stage 5 tickets are reviewed.

## 2026-07-23 - S5-T01 Rerun Implementation Handoff

Result: ready for research/review agent review with a passed-gate result.

Findings:

- No Stage 4.5 runway blocker was found. S4.5-IMP01 through S4.5-IMP10 are present, marked `Done`, and backed by review/progression/documentation acceptance records.
- S5-T00 and S5-T01A are accepted and `Done`.
- Stage 5 search/timeline implementation has not started; S5-T02 through S5-T16 remain `Draft`.
- The July 16 S5-T01 failed gate remains historical and correct for its time.

Gate decision:

- S5-T01 can pass after research/review-agent acceptance.
- S5-T02 may be prepared as the next ticket only after that acceptance.
- Stage 5 inputs must stay limited to reviewed provenance-rich records; `image-hash.json` with `not_run` is not a completed hash proof, static HTML is not an authoritative index, browser/navigation is not recursive crawl, and selected-file content remains explicit-selection only.

Verification:

- Full portable-runtime run: `.\.python312-embed\python.exe -m pytest`: 207 passed in 53.94s.
- Privacy-safe real-image no-selection/navigation smoke exited 0 with 53 segments, metadata `metadata_available`, verification `not_supported`, EWF stream `ok`, logical media size 1,024,209,543,168 bytes, 5 volumes, filesystem `ok`, root listing `real_parser_backed` with 11 entries, file-list JSON/CSV `ok` with 11 entries, nested directory listing `ok` / `real_parser_backed` with 19 entries, files=19, directories=0, other=0, navigation `nested_directory_files_visible`, static HTML created, image hash `not_run`, selected-file operations `not_run`, `source_modified: false`, and `read_only_asserted: true`.
- Full `--hash-image` was intentionally not run because the local logical image is about 1 TB and that command is documented as long-running.

Scope intentionally not changed:

- No app source behavior, tests, schema, parser behavior, dependency setup, evidence fixtures, evidence handling, search/timeline modules, UI/reporting/PDF, deleted recovery, carving, packaging, commit, or push.

## 2026-07-23 - S5-T01 Rerun Ticket Promotion

Result: ready to feed to the coding agent.

Direction:

- Rerun S5-T01 as a documentation/review gate over the completed S4.5-IMP01 through S4.5-IMP10 runway.
- Preserve the July 16 failed S5-T01 result as historical only.
- Do not implement search/timeline, app source behavior, parser behavior, dependency setup, UI/reporting, or evidence handling.
- If the gate passes, mark S5-T01 as `Review`, keep S5-T02 through S5-T16 `Draft`, and recommend S5-T02 only after research/review-agent acceptance.
- If the gate fails, mark S5-T01 as `Review` with exact blockers and keep S5-T02 through S5-T16 `Draft`.

Review expectations:

- Verify the completion matrix covers S4.5-IMP01 through S4.5-IMP10.
- Verify allowed and blocked Stage 5 input records preserve provenance/status/warning labels and do not overclaim full hash, verification, recursive crawl, full-text content, or UI/report coverage.
- Run the full portable-runtime test suite and, if practical, the privacy-safe no-selection/navigation real-image smoke.

## 2026-07-23 - S4.5-IMP10 Review Acceptance

Result: accepted. S4.5-IMP10 is done.

Findings:

- No blocking findings.
- The work stayed documentation/status-only; changed files are documentation, ticket, prompt, and status records.
- The guide now gives copyable PowerShell flows for the hands-on Stage 4.5 demo and keeps privacy/proof boundaries explicit.
- Stage 5 S5-T02 through S5-T16 remain blocked/draft.

Verification:

- Full reviewer run: `.\.python312-embed\python.exe -m pytest`: 207 passed in 49.87s.
- Reviewer real-image no-selection/navigation smoke exited 0 with `ok_with_unsupported_sections`, metadata `metadata_available`, verification `not_supported`, EWF stream `ok`, 5 volumes, filesystem `ok`, root listing `real_parser_backed` with 11 entries, file-list JSON/CSV `ok` with 11 entries, nested listing `real_parser_backed` with 19 entries, files=19, directories=0, other=0, static HTML created, image hash `not_run`, selected-file operations `not_run`, `source_modified: false`, and `read_only_asserted: true`.
- Full `--hash-image` was intentionally not run because the logical image is large and the command is long-running.

Next:

- Rerun S5-T01 as the next practical ticket.
- Do not start S5-T02 or later search/timeline work until S5-T01 passes after this Stage 4.5 acceptance.

## 2026-07-23 - S4.5-IMP10 Implementation Handoff

Result: ready for research/review agent review.

Completed:

- Marked `tickets/stage-4.5/S4.5-IMP10-demo-guide-and-stage-5-gate-refresh.md` as `Review`.
- Refreshed the command-line testing guide with copyable PowerShell commands for fresh-output cleanup, no-selection first-testing, optional full logical-image hashing, nested directory navigation, live browser use, file-list/static HTML inspection, and selected-file preview/export/hash/signature only after explicit approved selection.
- Added a short manual-testing demo showcase document that repackages the same command-line workflow for presentation without adding product behavior or sensitive evidence detail.
- Updated Stage 4.5 and Stage 5 gate docs so S5-T01 must check S4.5-IMP01 through S4.5-IMP10 before any S5-T02+ search/timeline implementation can start.
- Preserved privacy boundaries: shared handoffs should report statuses/counts only, not private filenames, internal paths, metadata values, file content, screenshots, real evidence files, or generated sensitive outputs.

Verification:

- Full portable-runtime run: `.\.python312-embed\python.exe -m pytest`: 207 passed in 49.26s.
- Privacy-safe real-image no-selection/navigation smoke exited 0 with 53 segments, metadata `metadata_available`, verification `not_supported`, EWF stream `ok`, logical media size 1,024,209,543,168 bytes, 5 volumes, filesystem `ok`, root listing `real_parser_backed` with 11 entries, file-list JSON/CSV `ok` with 11 entries, nested directory listing `ok` / `real_parser_backed` with 19 entries, files=19, directories=0, other=0, static HTML created, image hash `not_run`, selected-file operations `not_run`, `source_modified: false`, and `read_only_asserted: true`.
- Full `--hash-image` was intentionally not run because the local logical image is about 1 TB and the guide documents it as a long-running user/reviewer option.

Scope intentionally not changed:

- No app source behavior, parser behavior, hashing behavior, navigation/browser behavior, dependencies, evidence handling behavior, UI/report/PDF, deleted recovery, carving, packaging, transcript persistence, Stage 5 search/timeline, commit, or push.
- S5-T02 through S5-T16 remain blocked/draft until S4.5-IMP10 is reviewed and S5-T01 is rerun and accepted.

## 2026-07-23 - S4.5-IMP10 Ticket Promotion

Result: S4.5-IMP10 is ready to feed to the coding agent.

Direction:

- Keep the ticket documentation/status-only. Do not add parser, hash, navigation, browser, UI/reporting, Stage 5 search/timeline, dependency, or evidence-handling behavior.
- Refresh the command-line testing guide so the user can repeat the Stage 4.5 demo with exact PowerShell commands for no-selection intake, optional full logical-image hash, nested directory listing, live browser navigation, static HTML/file-list review, and selected-file template usage.
- Refresh Stage 4.5 and Stage 5 gate docs so S5-T01 is the next recommended ticket after S4.5-IMP10 review acceptance, while S5-T02 through S5-T16 remain blocked/draft.

Review expectations:

- Verify this remains documentation/status-only.
- Run the full portable-runtime test suite.
- If practical, run the safe no-selection real-image smoke with `--demo-list-first-directory`.
- Do not require full `--hash-image` completion; it is a long-running command on the local logical image unless explicitly run by the user/reviewer.

## 2026-07-23 - S4.5-IMP09B Review Acceptance

Result: accepted. S4.5-IMP09B is done.

Findings:

- No blocking findings.
- The live browser satisfies the hands-on demo gap for shell-like `dir`, `cd <folder>`, `cd ..`, `pwd`, `help`, and `exit` navigation over the reviewed parser-backed listing boundary.
- The implementation reuses EWF segment discovery, `EwfImageByteStream`, partition-table volume discovery, `Pytsk3FilesystemAdapter`, and `list_directory()` rather than creating a separate parser path.

Verification:

- Focused reviewer run: `.\.python312-embed\python.exe -m pytest app\tests\test_directory_browser.py app\tests\test_directory_listing.py app\tests\test_filesystem_adapter.py`: 28 passed in 0.56s.
- Full reviewer run: `.\.python312-embed\python.exe -m pytest`: 207 passed in 56.56s.
- Reviewer real-image browser smoke exited 0 with 53 segments, root listing `ok` / `real_parser_backed` with 11 entries, nested listing `ok` / `real_parser_backed` with 19 entries, files=19, directories=0, other=0, parent navigation observed, file-target `path_not_directory`, `source_modified: false`, and `read_only_asserted: true`.

Residual scope:

- S4.5-IMP10 remains required before S5-T01 rerun.
- Stage 5 search/timeline remains blocked until S4.5-IMP10 is reviewed and S5-T01 is rerun and accepted.
- The browser is not a recursive crawler, search indexer, content reader, export tool, hashing tool, transcript writer, UI, report system, deleted recovery path, carving path, or packaging slice.

## 2026-07-23 - S4.5-IMP09B Implementation Handoff

Result: ready for research/review agent review.

Completed:

- Added `app.backend.api.directory_browser`, a live terminal browser over the reviewed EWF stream, partition-table volume discovery, `Pytsk3FilesystemAdapter`, and `list_directory()` path.
- Added a stateful command loop for `help` / `?`, `pwd`, `ls` / `dir`, `cd <path-or-name>`, `cd ..`, `cd /`, `root`, `exit`, and `quit`.
- Added quoted-name handling, relative/absolute path resolution, parent/root navigation, and `path_not_directory` reporting that leaves the current path unchanged when a file is targeted.
- Exposed browser helpers from `app.backend.api` and added dependency-free scripted tests.
- Updated active docs/status so S4.5-IMP09B is `Review`, S4.5-IMP10 remains Draft/pending, and Stage 5 search/timeline remains blocked.

Verification:

- Focused portable-runtime run: `.\.python312-embed\python.exe -m pytest app\tests\test_directory_browser.py app\tests\test_directory_listing.py app\tests\test_filesystem_adapter.py`: 28 passed in 1.26s.
- Full portable-runtime run: `.\.python312-embed\python.exe -m pytest`: 207 passed in 54.11s.
- Privacy-safe real-image browser smoke exited 0 with 53 segments, root listing `ok` / `real_parser_backed` with 11 entries, nested listing `ok` / `real_parser_backed` with 19 entries, files=19, directories=0, other=0, parent navigation `ok`, file-target `path_not_directory`, `source_modified: false`, and `read_only_asserted: true`.

Scope intentionally not implemented:

- No recursive traversal, broad crawl, transcript artifact, content preview/export/hash/signature, selected-file auto-selection, file-list expansion, static HTML/report-system work, search/timeline, UI, deleted recovery, carving, packaging, dependency installation, commit, or push.

## 2026-07-23 - S4.5-IMP09B Ticket Promotion

Result: S4.5-IMP09B is ready to feed to the coding agent.

Direction:

- The live browser should reuse the accepted S4.5-IMP09/09A directory navigation framework.
- Existing behavior is stateless and artifact-producing: call `list_directory()` for one path and write JSON/CSV.
- New behavior should be stateful and human-facing: keep a current path, accept `dir`, `ls`, `cd`, `cd ..`, `pwd`, `help`, and `exit`, and call the same parser-backed `list_directory()` boundary at each step.

Ticket decisions:

- Added `tickets/stage-4.5/S4.5-IMP09B-interactive-e01-directory-browser.md`.
- Added `prompts/vscode-agent/2026-07-23-s4.5-imp09b-interactive-e01-directory-browser.md`.
- Kept content reads, export, hashing, search/timeline, recursive crawl, UI/reporting, deleted recovery, carving, packaging, and real evidence commits out of scope.
- Updated Stage 4.5/Stage 5 gate docs so S4.5-IMP09B is required before S4.5-IMP10 and S5-T01 rerun.

## 2026-07-23 - S4.5-IMP09A Review Acceptance

Result: accepted. S4.5-IMP09 and S4.5-IMP09A are done.

Findings:

- No blocking findings.
- The corrected demo satisfies the user's Stage 4.5 proof bar for seeing actual files inside the real E01-backed filesystem through bounded parser-backed directory navigation.
- The implementation remains a command/artifact demo, not an interactive `cd`/`dir` browser.

Verification:

- Focused reviewer run: `.\.python312-embed\python.exe -m pytest app\tests\test_filesystem_adapter.py app\tests\test_directory_listing.py app\tests\test_first_testing_command.py`: 42 passed in 52.20s.
- Full reviewer run: `.\.python312-embed\python.exe -m pytest`: 199 passed in 40.70s.
- Reviewer real-image corrected demo smoke exited 0 with `ok_with_unsupported_sections`, 53 segments, root listing `real_parser_backed` with 11 entries, directory navigation `ok` / `real_parser_backed`, 19 nested entries, files=19, directories=0, other=0, selected depth 2, root/child attempts 1/2, selected-file operations `not_run`, `source_modified: false`, and `read_only_asserted: true`.
- Reviewer explicit nested file-path smoke exited 0 with `path_not_directory`, parser backing `real_parser_backed`, entry count 0, selected depth 3, `source_modified: false`, and `read_only_asserted: true`.
- `git diff --check` found no whitespace errors, only normal line-ending notices.
- No lingering Python or pytest process was found after verification.

Residual scope:

- S4.5-IMP10 remains required before S5-T01 rerun.
- S4.5-IMP09B now owns the interactive command-line navigator for shell-like `dir`, `cd <folder>`, and back/up browsing.

## 2026-07-23 - S4.5-IMP09A Implementation Handoff

Result: ready for research/review agent review.

Completed:

- Updated `--demo-list-first-directory` to keep the S4.5-IMP09 bounded root-candidate behavior and probe direct child directories only when needed to find a file-visible listing.
- Added `selected_depth`, `file_visible`, `candidate_directory_count`, `attempted_directory_count`, and `attempted_child_directory_count` to directory listing artifacts, navigation readiness, manifest, command summary, and static HTML summary.
- Fixed parser-backed explicit nested file paths so they return `path_not_directory`, not `path_not_found`, without reading file content.
- Added dependency-free fake-parser tests for file-visible child probing and nested file-path status.

Verification:

- Focused portable-runtime run: `.\.python312-embed\python.exe -m pytest app\tests\test_filesystem_adapter.py app\tests\test_directory_listing.py app\tests\test_first_testing_command.py`: 42 passed in 62.18s.
- Full portable-runtime run: `.\.python312-embed\python.exe -m pytest`: 199 passed in 46.10s.
- Corrected real-image demo smoke exited 0 with `ok_with_unsupported_sections`, 53 segments, root listing `real_parser_backed` with 11 entries, directory navigation `ok` / `real_parser_backed` with 19 nested entries, type counts files=19 directories=0 other=0, selected depth 2, root/child attempts 1/2, selected-file operations `not_run`, `source_modified: false`, and `read_only_asserted: true`.
- Explicit nested file-path smoke exited 0 with directory status `path_not_directory`, parser backing `real_parser_backed`, entry count 0, selected depth 3, `source_modified: false`, and `read_only_asserted: true`.

Scope intentionally not implemented:

- No interactive `cd`/`dir` style command-line navigator, recursive traversal, broad crawl, content extraction, selected-file auto-selection, selected-file preview/export/hash/signature, search/timeline, UI/reporting system, deleted recovery, carving, packaging, dependency installation, commit, or push.
- A separate future ticket should own the interactive command-line navigation experience if the user wants shell-like go-in/go-out browsing.

## 2026-07-23 - S4.5-IMP09 Review Findings

Result: not accepted as done yet; S4.5-IMP09A is required.

Findings:

- The S4.5-IMP09 real-image demo mode produced a real parser-backed nested listing, but it reported `file_count = 0`, `directory_count = 4`. That proves nested directory navigation, but it still falls short of the user's hands-on demo requirement to see actual files within the image.
- A reviewer-run explicit deeper directory path produced a parser-backed listing with regular files, proving the implementation can reach files when pointed at the right nested path. The default demo path should use a bounded correction to get there without broad crawling.
- A reviewer-run explicit nested file path returned `path_not_found`; known file paths should return `path_not_directory`.

Verification:

- Focused reviewer run: `.\.python312-embed\python.exe -m pytest app\tests\test_filesystem_adapter.py app\tests\test_directory_listing.py app\tests\test_first_testing_command.py`: 38 passed in 53.37s.
- Full reviewer run: `.\.python312-embed\python.exe -m pytest`: 195 passed in 47.23s.
- Reviewer real-image demo smoke exited 0 with directory navigation `ok` / `real_parser_backed`, 4 entries, files=0, directories=4, other=0.
- Reviewer explicit deeper path smoke exited 0 with directory navigation `ok` / `real_parser_backed`, 19 entries, files=19, directories=0, other=0.

Correction:

- Added `tickets/stage-4.5/S4.5-IMP09A-file-visible-navigation-correction.md`.
- Added `prompts/vscode-agent/2026-07-23-s4.5-imp09a-file-visible-navigation-correction.md`.
- Stage 5 remains blocked; do not proceed to S4.5-IMP10 or S5-T01 until S4.5-IMP09A is reviewed.

## 2026-07-23 - S4.5-IMP09 Implementation Handoff

Result: ready for research/review agent review.

Completed:

- Added explicit nested directory navigation to the first-testing command with `--list-directory-path` and `--demo-list-first-directory`.
- Added `outputs/directory-listing.json`, `outputs/directory-listing.csv`, and `outputs/navigation-readiness.json`.
- Updated `Pytsk3FilesystemAdapter` and `list_directory()` so parser-backed adapters can list one requested directory below root while root-only adapters keep structured unsupported states.
- Updated run manifest, command summary, static local HTML summary, unsupported sections, tests, and active status docs.
- Deferred `--list-directory-id` because the current parser-backed file-id shape is not yet a safe stable directory resolver.

Verification:

- Focused portable-runtime run: `.\.python312-embed\python.exe -m pytest app\tests\test_filesystem_adapter.py app\tests\test_directory_listing.py app\tests\test_first_testing_command.py`: 38 passed in 48.60s.
- Full portable-runtime run: `.\.python312-embed\python.exe -m pytest`: 195 passed in 69.93s.
- Real-image nested-navigation smoke exited 0 with `ok_with_unsupported_sections`, 53 segments, root listing `real_parser_backed` with 11 entries, directory navigation `ok` / `real_parser_backed` with 4 nested entries, type counts files=0 directories=4 other=0, candidate/attempted root-directory counts 2/2, selected-file operations `not_run`, `source_modified: false`, and `read_only_asserted: true`.
- The smoke found no regular file among the bounded root-directory candidate set; it did try both candidates before using the nonempty parser-backed directory listing.

Scope intentionally not implemented:

- No S4.5-IMP10 guide/gate refresh, S5-T01 rerun, S5-T02+ work, recursive traversal, broad crawl, content extraction, selected-file auto-selection, search/timeline, UI/reporting system, deleted recovery, carving, packaging, dependency installation, commit, or push.

## 2026-07-23 - S4.5-IMP09 Ticket Promotion

Result: S4.5-IMP09 is ready to feed to the coding agent.

Ticket decisions:

- Accepted S4.5-IMP08 as the reviewed image-hash capability slice after focused/full tests and a real-image no-hash smoke; the completed full-image hash remains a long-running reviewer/user artifact unless separately produced.
- Promoted S4.5-IMP09 from draft to ready.
- Tightened S4.5-IMP09 so the coding agent must produce parser-backed nested directory-listing artifacts from the real E01, not only partition/root status.
- Required a real-image smoke with nonzero nested entry count, type counts, read-only/source-modified assertions, and no real internal names/paths quoted in the handoff.

## 2026-07-22 - S4.5-IMP08 Review Acceptance

Result: accepted as implementation/capability; S4.5-IMP08 is done.

Completed:

- Added explicit `--hash-image`, `--image-hash-algorithm`, and `--image-hash-chunk-size` first-testing options.
- Added `outputs/image-hash.json` with `not_run` by default and requested full logical-image SHA-256 hashing over the EWF stream.
- Added chunked image-stream hashing support with dependency/stream failure statuses and read-only/source-modified assertions.
- Updated run manifest, command summary, static HTML summary, unsupported sections, tests, and active status docs.

Verification:

- Focused portable-runtime run: `.\.python312-embed\python.exe -m pytest app\tests\test_image_stream.py app\tests\test_first_testing_command.py`: 31 passed in 32.90s.
- Full portable-runtime run: `.\.python312-embed\python.exe -m pytest`: 189 passed in 87.61s.
- Real full-image hash command was not run to completion in the coding-agent session because the existing reviewed real-image smoke reports a logical media size of 1,024,209,543,168 bytes. The local first segment exists, and the documented reviewer/user command writes under `.test-artifacts\first-testing\image-hash-real-image` with `--hash-image --redact-paths`.

Scope intentionally not implemented:

- No S4.5-IMP09 nested navigation, S4.5-IMP10 guide/gate refresh, Stage 5 search/timeline, recursive traversal, broad crawl, selected-file auto-selection, UI/reporting system, deleted recovery, carving, packaging, dependency installation, commit, or push.
- Stored EWF hash metadata, segment-container hashes, selected-file hashes, and stub bytes are not treated as independent image-level verification.

## 2026-07-22 - S4.5 Demo Feedback Extension

Result: Stage 4.5 reopened with new hard prerequisites before Stage 5.

User feedback:

- The demo needs an independent verification-style hash for the entire image.
- The demo needs navigation into actual directories/files inside the image, not only partition/root status.

Ticket decisions:

- Added S4.5-IMP08 as `Ready` for an independent full logical-image hash artifact over the EWF stream.
- Added S4.5-IMP09 for nested directory navigation into actual filesystem entries; it was later promoted to `Ready`.
- Added S4.5-IMP10 as `Draft` for final command-line guide and Stage 5 gate refresh after hash/navigation.
- At that time, Stage 5 S5-T01 rerun and S5-T02+ remained blocked on the added Stage 4.5 demo-feedback tickets. This was later narrowed to S4.5-IMP10 after S4.5-IMP09A acceptance.

## 2026-07-22 - S4.5-IMP07 Review Acceptance

Result: accepted; S4.5-IMP07 is done.

Findings:

- No blocking issues found.
- The command-line guide gives a repeatable PowerShell path for the current no-selection real-E01 demo, including case workspace creation, segment discovery, metadata/verification status, EWF stream, volume discovery, root filesystem listing, file-list JSON/CSV, static HTML summary, and artifact inspection.
- Review correction: changed generic real-E01 examples to use the reviewed portable runtime and clarified file-list/selected-file status inspection commands so users see status codes instead of raw status objects.
- Selected-file real extraction remains template-only and opt-in; no real selected-file extraction, recursive traversal, broad crawl, search/timeline, UI/reporting system, deleted recovery, carving, or packaging was added.

Verification:

- Reviewer final full portable-runtime run: `.\.python312-embed\python.exe -m pytest`: 184 passed in 28.38s.
- Reviewer real-image no-selection smoke exited 0 with `ok_with_unsupported_sections`, 53 segments, metadata `metadata_available`, verification `not_supported`, EWF stream `ok`, partition-table status `ok` with 5 volumes, filesystem status `ok`, root listing `real_parser_backed` with 11 entries, file-list JSON/CSV `ok` with 11 entries, static HTML summary created, selected-file operations `not_run`, `source_modified: false`, and `read_only_asserted: true`.
- Artifact inspection confirmed file-list CSV has 11 rows, unsupported sections remain explicit, and the static HTML summary exists.

Remaining scope:

- S4.5-IMP07 was accepted as done; later hands-on demo feedback extends the Stage 4.5 runway with S4.5-IMP08 through S4.5-IMP10 before S5-T01 rerun.
- Next required implementation slice is S4.5-IMP08, not S5-T01.

## 2026-07-22 - S4.5-IMP07 Implementation Handoff

Result: ready for research/review agent review.

Completed:

- Created `app/docs/manual-testing/stage-4.5-command-line-testing-guide.md` with prerequisites, evidence safety, exact PowerShell commands, portable-runtime real-E01 commands, artifact inspection steps, expected statuses, troubleshooting, proof boundaries, and a reviewer transcript template.
- Linked the guide from the manual-testing index and reconciled active Stage 4.5/Stage 5 status docs so S4.5-IMP07 is in review.
- Kept selected-file real extraction as an opt-in template only; no selected-file extraction was run against the real image.
- Kept Stage 5 search/timeline blocked until S4.5-IMP07 is accepted and S5-T01 is rerun.

Verification:

- Full portable-runtime run: `.\.python312-embed\python.exe -m pytest`: 184 passed in 41.91s.
- Real-image no-selection smoke exited 0 with `ok_with_unsupported_sections`, 53 segments, metadata `metadata_available`, verification `not_supported`, EWF stream `ok`, partition-table status `ok` with 5 volumes, filesystem status `ok`, root listing `real_parser_backed` with 11 entries, file-list JSON/CSV `ok` with 11 entries, static HTML summary created, selected-file operations `not_run`, `source_modified: false`, and `read_only_asserted: true`.

Scope intentionally not implemented:

- No parser behavior, dependencies, real evidence fixtures, selected-file real extraction, recursive traversal, broad crawl, search/timeline, UI/report system, PDF, deleted recovery, carving, packaging, commit, or push.
- Sensitive real evidence metadata values, evidence-internal names/paths, and file content are not quoted in shared docs or handoffs.

## 2026-07-22 - S4.5-IMP07 Ready Ticket Preparation

Result: ready to feed to the coding agent.

Scope:

- Documentation/instruction only: create the user-facing PowerShell testing guide and update related manual-testing/status docs.
- The guide must be based on reviewed S4.5-IMP01 through S4.5-IMP06 behavior, including the portable-runtime real-image no-selection smoke shape.
- It must keep selected-file real extraction opt-in only, avoid quoting sensitive metadata/root-entry names/content, and keep outputs under ignored `.test-artifacts/first-testing/`.
- Stage 5 search/timeline remains blocked until S4.5-IMP07 is implemented/reviewed and S5-T01 is rerun.

## 2026-07-22 - S4.5-IMP06 Review Acceptance

Result: accepted; S4.5-IMP06 is done.

Findings:

- No blocking issues found.
- The Stage 4.5 and Stage 5 handoff docs now preserve the reviewed implementation truth through S4.5-IMP05, record S4.5-IMP06 as the documentation/status gate packet, and keep S4.5-IMP07 as the remaining Stage 4.5 blocker.
- The allowed future Stage 5 inputs are provenance-rich reviewed artifacts only: intake/segments, case/evidence/audit rows, metadata and verification-status records, EWF stream status, volume/filesystem/root-listing records, root-listing-derived file-list outputs, and explicit selected-file records when selection provenance exists.
- The blocked inputs remain clear: recursive crawl, broad enumeration, full-text E01 content, auto-selected analysis/export, deleted recovery/carving, UI/report records, and unsupported verification-success claims.

Verification:

- Reviewer full portable-runtime run: `.\.python312-embed\python.exe -m pytest`: 184 passed in 32.93s.
- Real-image smoke was not rerun because S4.5-IMP06 is documentation/status-only; the reviewed S4.5-IMP05 no-selection smoke remains the current real-image evidence record.

Remaining scope:

- S4.5-IMP07 command-line testing guide remains required before S5-T01 can rerun as a passing gate.
- Stage 5 search/timeline remains blocked until S4.5-IMP07 is completed/reviewed and S5-T01 is rerun.

## 2026-07-22 - S4.5-IMP06 Implementation Handoff

Result: ready for research/review agent review.

Completed:

- Reconciled active Stage 4.5 and Stage 5 docs so S4.5-IMP01 through S4.5-IMP05 are reviewed/done, S4.5-IMP06 is in review, S4.5-IMP07 remains drafted, and S5-T02 through S5-T16 remain blocked/draft.
- Added the Stage 5 gate handoff packet in active docs: completion matrix, reviewed artifacts available, allowed future input records, blocked inputs, required provenance/status/warning labels, and the recommendation to rerun S5-T01 only after S4.5-IMP07 is completed/reviewed.
- Updated optional stale scaffold docs so they no longer say no first-testing command or real-E01 parser path exists.
- Preserved the reviewed real-image truth without quoting sensitive metadata, filenames, root entries, or content.

Verification:

- Full portable-runtime run: `.\.python312-embed\python.exe -m pytest`: 184 passed in 44.69s.
- Real-image smoke was not rerun for S4.5-IMP06 because this ticket is documentation/status-only; the reviewed S4.5-IMP05 no-selection smoke remains the current real-image evidence record.

Remaining scope:

- S4.5-IMP07 command-line testing guide, recursive traversal, broad crawl, selected-file real-content run with approved selection, search/timeline/indexing, UI/report system, PDF, deleted recovery, carving, packaging, commit, and push remain out of scope.
- Stage 5 search/timeline remains blocked until S4.5-IMP07 is completed/reviewed and S5-T01 is rerun.

## 2026-07-17 - S4.5-IMP05 Review Acceptance

Result: accepted; S4.5-IMP05 is done.

Findings:

- No blocking issues found.
- File-list JSON/CSV is correctly derived from the current root listing only, with honest zero-entry output when root listing is unavailable or not real-parser-backed.
- Static HTML is local, escaped, non-interactive, and scoped to statuses/counts/artifact inventory instead of becoming a UI or report system.
- Review correction: hardened HTML redaction for escaped evidence-root strings and expanded the redaction test with an evidence path containing `&`.

Verification:

- Focused portable-runtime run after review correction: `.\.python312-embed\python.exe -m pytest app\tests\test_first_testing_command.py`: 13 passed in 24.49s.
- Full portable-runtime run after review correction: `.\.python312-embed\python.exe -m pytest`: 184 passed in 29.26s.
- Reviewer real-image no-selection smoke exited 0 with `ok_with_unsupported_sections`, 53 segments, root listing `real_parser_backed` with 11 entries, file-list JSON/CSV `ok` with 11 entries, HTML summary created, selected-file operations `not_run`, `source_modified: false`, and `read_only_asserted: true`.
- Artifact checks confirmed CSV header order, no S4.5-IMP05 output entries left in unsupported sections, no raw evidence root in shared summary/HTML, no script/network references in HTML, and no search/timeline/PDF artifacts.

Remaining scope:

- S4.5-IMP06 guardrail/review handoff, S4.5-IMP07 command-line testing guide, recursive traversal, broad crawl, auto-selection/export, selected-file real extraction without approved selection, search/timeline/indexing, UI, report system/PDF, deleted recovery, carving, packaging, commit, and push remain out of scope.
- Stage 5 search/timeline remains blocked until S4.5-IMP06 through S4.5-IMP07 are completed and reviewed.

## 2026-07-17 - S4.5-IMP05 Implementation Handoff

Result: ready for research/review agent review.

Implemented:

- Added root-listing-derived `file-list.json` with schema/status/provenance fields, entry status/warnings, read-only/source-modified assertions, and honest zero-entry output when root listing is unavailable.
- Added UTF-8 `file-list.csv` with stable headers, standard CSV writer output, warning-code joining, empty-cell preservation, and formula-looking cell protection.
- Added static local `outputs/reports/summary.html` with escaped statuses/counts/artifact inventory, no network assets, no JavaScript app, and no evidence content.
- Updated first-testing `run-manifest.json`, `command-summary.txt`, and unsupported sections so S4.5-IMP05 outputs are inventoried and no longer listed as not implemented.
- Preserved selected-file opt-in behavior; no arbitrary evidence file is auto-selected, previewed, exported, hashed, or signature-checked.

Verification:

- Focused portable-runtime run: `.\.python312-embed\python.exe -m pytest app\tests\test_first_testing_command.py`: 13 passed in 22.53s.
- Full portable-runtime run: `.\.python312-embed\python.exe -m pytest`: 184 passed in 27.70s.
- Real-image no-selection smoke exited 0 with `ok_with_unsupported_sections`, 53 segments, EWF stream `ok`, partition-table status `ok` with 5 volumes, filesystem status `ok`, root listing `ok` / `real_parser_backed` with 11 entries, file-list JSON/CSV `ok` with 11 entries, HTML summary created, and selected-file operations `not_run`.
- Smoke artifact check reported `source_modified: false` and `read_only_asserted: true`.

Scope intentionally not implemented:

- No recursive traversal, broad crawl, auto-selection/export, selected-file real extraction beyond existing explicit path, search/timeline/indexing, dynamic UI, report system, PDF, deleted recovery, carving, packaging, commit, or push.
- No real evidence files were added to the repository, and sensitive real evidence filenames, root entry names, metadata values, and content are not quoted in shared summaries.

## 2026-07-17 - S4.5-IMP04 Review Acceptance

Result: accepted; S4.5-IMP04 is done.

Findings:

- No blocking issues found.
- Selected-file preview/export/hash/signature now run only through explicit parser-backed root-entry selection and reuse the existing provider surfaces instead of creating a separate behavior path.
- The default real-E01 smoke stayed non-invasive: no file was auto-selected, selected-file operations stayed `not_run`, and no selected export artifacts were created.
- Review caveat: I did not run a real selected-file extraction smoke because no explicit safe real file selection was approved. Dependency-free fake-parser tests cover the selected-byte provider path without exposing real evidence content.

Verification:

- Focused portable-runtime run: `.\.python312-embed\python.exe -m pytest app\tests\test_selected_file_content.py app\tests\test_file_preview.py app\tests\test_file_export.py app\tests\test_content_analysis_hashing.py app\tests\test_content_analysis_signatures.py app\tests\test_first_testing_command.py`: 80 passed in 20.75s.
- Full portable-runtime run: `.\.python312-embed\python.exe -m pytest`: 183 passed in 20.82s.
- Reviewer real-image no-selection smoke exited 0 with `ok_with_unsupported_sections`; selected-file readiness, preview, analysis, hash, signature, and export statuses were all `not_run`.
- Artifact check confirmed no `file-list.json`, `file-list.csv`, `report.html`, selected export output, or selected export manifest was created by the no-selection smoke.

Remaining scope:

- S4.5-IMP05 file-list JSON/CSV, command summary, artifact inventory, optional static HTML, S4.5-IMP06 handoff reconciliation, S4.5-IMP07 command-line guide, search/timeline, UI, reports, deleted recovery, carving, packaging, commit, and push remain out of scope.
- Stage 5 search/timeline remains blocked until S4.5-IMP05 through S4.5-IMP07 are completed and reviewed.

## 2026-07-17 - S4.5-IMP04 Implementation Handoff

Result: ready for research/review agent review.

Implemented:

- Added a selected-file content reader and provider wrappers for preview, export, and analysis over explicit parser-backed E01 root entries.
- Reused `preview_file()`, `export_file()`, `hash_file_content()`, `detect_file_signature()`, and `evaluate_extension_mismatch()` instead of replacing those surfaces.
- Added first-testing selected-file flags and artifacts: `selected-file-readiness.json`, `selected-file-preview.json`, `selected-file-analysis.json`, and `selected-file-export.json`.
- Kept selected-file operations `not_run` when no file is explicitly selected and refused unsupported/deleted/metadata-only/unreadable/large-file paths with structured statuses.

Verification:

- Focused portable-runtime run: `.\.python312-embed\python.exe -m pytest app\tests\test_selected_file_content.py app\tests\test_file_preview.py app\tests\test_file_export.py app\tests\test_content_analysis_hashing.py app\tests\test_content_analysis_signatures.py app\tests\test_first_testing_command.py`: 80 passed in 22.41s.
- Full portable-runtime run: `.\.python312-embed\python.exe -m pytest`: 183 passed in 26.98s.
- Real-image no-selection smoke exited 0 with `ok_with_unsupported_sections`, 53 segments, EWF stream `ok`, logical media size 1,024,209,543,168 bytes, partition-table status `ok` with 5 volumes, filesystem status `ok`, a `real_parser_backed` root listing with 11 entries, and selected-file readiness/preview/hash/signature/export all `not_run` because no explicit safe file was selected.
- Artifact check found no `file-list.json`, `file-list.csv`, or HTML artifacts from S4.5-IMP04.

Scope intentionally not implemented:

- No S4.5-IMP05 file-list JSON/CSV, static HTML, broad filesystem crawl, arbitrary auto-selection/export, search/timeline, UI, reports, deleted recovery, carving, packaging, commit, or push.
- No real evidence files were added to the repository, and sensitive real evidence filenames, paths, root entry names, metadata values, and content are not quoted in shared summaries.

## 2026-07-17 - S4.5-IMP03 Review Acceptance

Result: accepted; S4.5-IMP03 is done.

Findings:

- No blocking issues found.
- The hard gate passed under reviewer rerun: the local real-E01 smoke produced a `real_parser_backed` root listing with 11 entries from the actual evidence.
- Root-listing artifact consistency check confirmed entries came from `pytsk3-filesystem-adapter` and were marked read-only.
- Later-slice artifacts checked during review: no `file-list.json`, `file-list.csv`, or `report.html` was created.
- Review correction: updated a stale `run_first_testing()` docstring that still said filesystem parsing was not added. This was documentation-only inside code and did not change behavior.

Verification:

- Focused portable-runtime run: `.\.python312-embed\python.exe -m pytest app\tests\test_image_stream.py app\tests\test_volume_discovery.py app\tests\test_filesystem_adapter.py app\tests\test_directory_listing.py app\tests\test_first_testing_command.py`: 48 passed in 21.79s.
- Full portable-runtime run: `.\.python312-embed\python.exe -m pytest`: 174 passed in 25.71s.
- Reviewer real-image smoke exited 0 with `ok_with_unsupported_sections`, 53 segments, `metadata_available`, verification `not_supported`, EWF stream `ok`, logical media size 1,024,209,543,168 bytes, partition-table status `ok` with 5 volumes, filesystem status `ok`, and `real_parser_backed` root listing with 11 entries.

Remaining scope:

- S4.5-IMP04 selected-file content providers, E01-backed preview/export/hash/signature, file-list JSON/CSV, static HTML, search/timeline, UI, reports, deleted recovery, carving, packaging, commit, and push remain out of scope.
- Stage 5 search/timeline remains blocked until S4.5-IMP04 through S4.5-IMP07 are completed and reviewed.

## 2026-07-17 - S4.5-IMP03 Implementation Handoff

Result: ready for research/review agent review.

Implemented:

- Added `EwfImageByteStream` for read-only EWF-backed logical-image metadata and bounded reads.
- Added a `partition_table` volume discovery path over `pytsk3.Volume_Info` while preserving existing whole-image behavior.
- Upgraded `Pytsk3FilesystemAdapter` so an image-stream-backed volume can return real parser-backed root entries in existing `FilesystemResult` and `FilesystemEntry` shapes.
- Integrated first-testing artifacts for `ewf-stream.json`, `volumes.json`, `filesystems.json`, `root-listing.json`, and `demo-readiness.json`.
- Updated the command summary and run manifest so EWF stream, volume, filesystem, root-listing, and demo-readiness states stay separate.

Verification:

- Focused run: `.\.python312-embed\python.exe -m pytest app\tests\test_image_stream.py app\tests\test_volume_discovery.py app\tests\test_filesystem_adapter.py app\tests\test_directory_listing.py app\tests\test_first_testing_command.py`: 48 passed in 41.99s.
- Full run: `.\.python312-embed\python.exe -m pytest`: 174 passed in 51.01s.

Real-image smoke:

- Command: `.\.python312-embed\python.exe -m app.backend.api.first_testing --evidence-dir ".\ Test Image" --first-segment "C16242-1-RL1-E003.E01" --case ".test-artifacts\first-testing\s4-5-imp03-real-filesystem-demo" --redact-paths`
- Exit code: 0.
- Run status: `ok_with_unsupported_sections`.
- Segment count: 53.
- Metadata status: `metadata_available`.
- Verification status: `not_supported`.
- EWF stream status: `ok`.
- Logical media size: 1,024,209,543,168 bytes.
- Volume strategy/status/count: `partition_table` / `ok` / 5.
- Filesystem status: `ok`.
- Root listing: `real_parser_backed`, 11 entries.
- Demo readiness: `real_parser_backed_root_listing_available`.
- Source modified: `false`; read-only asserted: `true`.

Scope intentionally not implemented:

- No S4.5-IMP04 selected-file byte providers, preview/export/hash/signature over E01 content, file-list JSON/CSV, static HTML, search/timeline, UI, reports, deleted recovery, carving, packaging, commit, or push.
- No real evidence files or generated real-evidence outputs were added for commit.
- Sensitive real-E01 metadata values and root entry names are not quoted in shared summaries.

## 2026-07-17 - S4.5-IMP03 Dependency Setup Review

Result: blocker cleared for retry, not yet a completed S4.5-IMP03 demo.

Setup accepted for local development:

- Project-local runtime: `.\.python312-embed\python.exe`, Python 3.12.10.
- Runtime folders `.python312/` and `.python312-embed/` are ignored by git.
- Installed packages: `libewf-python 20240506` as import module `pyewf`, `pytsk3 20260715`, and `pytest 9.1.1`.
- Import preflight: `pyewf=available`; `pytsk3=available`.

Verification:

- Focused portable-runtime run: 56 passed in 8.40s.
- Full portable-runtime run: 167 passed in 14.99s.

Real-image setup smoke:

- Command exited 0 against the local ` Test Image` E01 set.
- Segment count: 53.
- Adapter/dependency: `pyewf-reader` available; `pyewf` available.
- Metadata status: `metadata_available`.
- Verification status: `not_supported`.
- No `ewf-stream.json`, `volumes.json`, `filesystems.json`, or `root-listing.json` was created yet because S4.5-IMP03 app behavior is still unimplemented.

Review guardrails:

- Do not quote sensitive real-E01 metadata values in shared summaries.
- The S4.5-IMP03 success gate is unchanged: a `Review` handoff must include a real-parser-backed root listing from the actual evidence, or the ticket must return `Blocked` with the next precise API/implementation blocker.
- Do not start S4.5-IMP04 or Stage 5 search/timeline.

## 2026-07-17 - S4.5-IMP03 Real E01 Filesystem Demo Gate

Result: blocked, not ready for review.

Preflight:

- `pyewf`: missing.
- `pytsk3`: missing.
- Local evidence exists: ` Test Image/C16242-1-RL1-E003.E01`.
- First segment size observed locally: 2,147,479,074 bytes.

Manual smoke attempted:

- Command: `python -m app.backend.api.first_testing --evidence-dir ".\ Test Image" --first-segment "C16242-1-RL1-E003.E01" --case ".test-artifacts\first-testing\s4-5-imp03-real-filesystem-demo" --redact-paths`
- Exit code: 0.
- Status: `ok_with_unsupported_sections`.
- Segment count: 53.
- Adapter/dependency: `pyewf-reader`, available `False`; `pyewf`, available `False`.
- Metadata status: `metadata_unavailable`.
- Verification status: `not_run`.
- Source modified: `false`.
- Read-only asserted: `true`.
- EWF stream status: unavailable; no `ewf-stream.json` artifact was created.
- Partition/volume status/count: unavailable; no `volumes.json` artifact and no real volume count.
- Filesystem status: unavailable; no `filesystems.json` artifact.
- Root listing: no `root-listing.json`; root entry count unavailable/0; no real-parser-backed entries.

Blocker:

- S4.5-IMP03 cannot satisfy the non-negotiable demo gate until `pyewf`/libewf and `pytsk3`/The Sleuth Kit are installed and usable in the active environment.
- Dependency-unavailable output remains honest, but it is not a successful real-E01 filesystem demo.

Verification:

- Focused run: `python -m pytest app\tests\test_image_stream.py app\tests\test_volume_discovery.py app\tests\test_filesystem_adapter.py app\tests\test_directory_listing.py app\tests\test_first_testing_command.py`: 41 passed in 16.15s.
- Full run: `python -m pytest`: 167 passed in 23.39s.

Scope intentionally not implemented:

- No EWF-backed stream, partition/filesystem parser, E01-backed content provider, file-list output, static HTML, search/timeline, UI, reports, deleted recovery, carving, packaging, native dependency installation, commit, or push.

## 2026-07-17 - S4.5-IMP03 Demo Gate Revision

Result: S4.5-IMP03 revised and ready for coding-agent handoff.

Review direction:

- S4.5-IMP03 is now the first hard real-E01 filesystem demo gate.
- A successful `Review` handoff must include a real-parser-backed root listing from ` Test Image/C16242-1-RL1-E003.E01`.
- If `pyewf`, `pytsk3`, libewf, The Sleuth Kit, build tooling, or API mismatch blocks that demo, the coding agent must mark S4.5-IMP03 `Blocked`, not `Review`, and return exact blocker evidence plus recommended setup.

Local preflight:

- `pyewf=missing`
- `pytsk3=missing`

## 2026-07-17 - S4.5-IMP02 And S4.5-IMP02A Acceptance

Result: accepted; both tickets marked done.

Findings:

- No blocking issues found after S4.5-IMP02A.
- The earlier `metadata_partial` concern is fixed: complete metadata plus stored hash metadata no longer emits `metadata_partial`, while true metadata-field unavailability still does.

Verification:

- Focused run: `python -m pytest app\tests\test_ewf_reader_adapter.py app\tests\test_intake_command.py app\tests\test_first_testing_command.py`: 25 passed in 7.35s.
- Full run: `python -m pytest`: 167 passed in 9.77s.
- `git diff --check` passed, with only normal Windows line-ending notices.

Remaining risk:

- `pyewf` is still unavailable locally, so real metadata extraction and verification are dependency-safe but not exercised against the local real E01. EWF-backed streams, partition/filesystem parsing, E01-backed file content, file-list output, static HTML, and full manual E01 workflow remain later Stage 4.5 slices.

## 2026-07-17 - S4.5-IMP02A Metadata Warning Semantics Handoff

Result: ready for research/review agent review.

Implemented:

- Corrected `app/backend/forensic_core/ewf_reader.py` so `metadata_partial` is emitted only when `metadata_field_unavailable` is present.
- Preserved `stored_hash_not_verified` as separate stored-hash metadata context, not verification success and not a metadata-partial trigger by itself.
- Preserved verification warning semantics separately from metadata warning semantics.
- Added dependency-free fake-`pyewf` assertions covering complete metadata plus stored hashes, partial metadata, and stored hashes without verification success.

Scope intentionally not implemented:

- No S4.5-IMP03 work.
- No EWF-backed streams, partition/filesystem parsing, E01-backed content providers, file-list output, static HTML, search/timeline, UI, reports, deleted recovery, carving, packaging, native dependency installation, commit, or push.

Verification:

- Focused run: `python -m pytest app\tests\test_ewf_reader_adapter.py app\tests\test_intake_command.py app\tests\test_first_testing_command.py`: 25 passed in 11.04s.
- Full run: `python -m pytest`: 167 passed in 14.52s.

Review note:

- Previous S4.5-IMP02 finding addressed: complete metadata reads with stored EWF hash metadata no longer emit `metadata_partial` solely because `stored_hash_not_verified` is present.

## 2026-07-17 - S4.5-IMP02 Real EWF Metadata And Verification Handoff

Result: ready for research/review agent review.

Implemented:

- Upgraded `PyewfEwfReaderAdapter` from importable-but-not-implemented skeleton to best-effort `pyewf` metadata and explicit verification handling.
- Preserved missing-`pyewf` dependency-unavailable behavior.
- Normalized metadata fields including format, segment count, reader/version, media size, bytes per sector, selected acquisition header fields, dates, and stored hashes when exposed.
- Kept stored hash metadata separate from verification success with `stored_hash_not_verified`.
- Added verification status handling for success, failure, exception/error, partial/unsupported shapes, unsupported API, and dependency-not-run states.
- Converted expected open, metadata, and verification errors into structured warnings/statuses.
- Added `metadata.json`, `verification.json`, and `segment-discovery.json` to the first-testing artifact bundle.
- Updated run manifest and command summary to surface metadata and verification status.
- Added dependency-free fake-`pyewf` tests.

Scope intentionally not implemented:

- No native dependency installation.
- No EWF-backed byte streams, partition/filesystem parsing, E01-backed preview/export/hash/signature content providers, file-list JSON/CSV, static HTML, search/timeline, UI, reports, deleted recovery, carving, packaging, commit, or push.
- No real E01 fixture was added to the repository.

Verification:

- Focused run: `python -m pytest app\tests\test_ewf_reader_adapter.py app\tests\test_intake_command.py app\tests\test_first_testing_command.py`: 25 passed in 14.62s.
- Full run: `python -m pytest`: 167 passed in 17.24s.
- Optional real-image smoke command used ` Test Image/C16242-1-RL1-E003.E01` with output under `.test-artifacts/first-testing/review-s4-5-imp02-real-image`.
- Smoke result: `ok_with_unsupported_sections`; 53 segments discovered; intake status `metadata_unavailable`; metadata status `metadata_unavailable`; verification status `not_run`; adapter `pyewf-reader`; dependency unavailable; `read_only_asserted: true`; `source_modified: false`; 6 unsupported rows.
- Smoke artifact check found `metadata.json`, `verification.json`, and `segment-discovery.json`, and no file-list, CSV, export, report, or HTML artifacts.

## 2026-07-16 - S4.5-IMP07 Testing Guide Ticket Addition

Result: added as draft; no coding-agent handoff yet.

Prepared:

- Added `tickets/stage-4.5/S4.5-IMP07-command-line-testing-guide.md`.
- Added `prompts/vscode-agent/2026-07-16-s4.5-imp07-command-line-testing-guide.md`.
- Updated Stage 4.5 and Stage 5 gate language so the pre-Stage-5 runway is S4.5-IMP01 through S4.5-IMP07.

Purpose:

- Ensure the real-evidence first-testing work produces a practical command-line guide, not just implementation artifacts.
- Require exact PowerShell commands, expected artifacts, inspection steps, troubleshooting, proof boundaries, privacy/redaction rules, and reviewer transcript templates.

Scope intentionally not implemented:

- No app behavior, parser behavior, dependencies, evidence handling, real evidence artifacts, Stage 5 search/timeline, UI, reports, commit, or push.

Verification:

- `python -m pytest`: 160 passed in 15.73s.

## 2026-07-16 - S4.5-IMP02 Through S4.5-IMP06 Ticket Population

Result: implementation runway populated; no coding-agent handoff yet.

Prepared:

- Added `S4.5-IMP02-real-ewf-metadata-verification.md` as `Ready`.
- Added `S4.5-IMP03-ewf-stream-partition-filesystem.md` as `Draft`.
- Added `S4.5-IMP04-e01-file-content-providers.md` as `Draft`.
- Added `S4.5-IMP05-file-list-output-visual-summary.md` as `Draft`.
- Added `S4.5-IMP06-final-guardrail-review-handoff.md` as `Draft`.
- Added matching VS Code coding-agent prompts for S4.5-IMP02 through S4.5-IMP06.

Reviewer rationale:

- Stage 4.5 planning was created to reach a substantial real-evidence first-testing display before Stage 5 search/timeline.
- Generating the remaining IMP tickets now makes that runway explicit and prevents S5-T02 from absorbing unfinished first-testing work.
- S4.5-IMP02 is next because S4.5-IMP01 produced the command shell and case workspace, but metadata/verification are still unavailable.

Scope intentionally not implemented:

- No app behavior, parser behavior, schema change, dependency installation, evidence handling, output artifact, visual summary, search/timeline, UI, report, commit, or push.

Verification:

- `python -m pytest`: 160 passed in 18.27s.

## 2026-07-16 - S4.5-IMP01 Review Result

Result: accepted; S4.5-IMP01 marked `Done`.

Findings:

- No blocking findings.
- The command implements the requested S4.5-IMP01 shell without adding real parser behavior or Stage 5 search/timeline work.
- Evidence/case/output overlap checks happen before workspace/artifact creation.
- The artifact bundle contains the expected `case.db`, `run-manifest.json`, `command-summary.txt`, `intake.json`, `case.json`, `audit.json`, and `unsupported-sections.json`.
- Unsupported sections clearly identify later owners S4.5-IMP02 through S4.5-IMP06.
- Manual status is only partial: the command shell was smoke-tested against a real local E01 set, but real EWF metadata, verification, partition/filesystem parsing, E01-backed content extraction, file-list output, and static HTML remain unimplemented.

Reviewer verification:

- Focused automated test rerun: `python -m pytest app\tests\test_first_testing_command.py`: 8 passed in 11.82s.
- Full-suite rerun: `python -m pytest`: 160 passed in 31.64s.
- Real-image smoke command used ` Test Image/C16242-1-RL1-E003.E01` with output under `.test-artifacts/first-testing/review-s4-5-imp01-real-image`.
- Smoke result: `ok_with_unsupported_sections`; 53 segments discovered; intake status `metadata_unavailable`; adapter `pyewf-reader`; dependency unavailable; `read_only_asserted: true`; `source_modified: false`; 4 audit events; 8 unsupported rows.
- Artifact check found no file-list, CSV, static HTML, export, or report artifacts from S4.5-IMP01.

Next:

- Prepare S4.5-IMP02 for real EWF metadata and verification work.
- Keep S5-T02 through S5-T16 `Draft` until S4.5-IMP01 through S4.5-IMP06 are completed and reviewed.

## 2026-07-16 - S4.5-IMP01 First-Testing Command Shell Handoff

Result: ready for research/review agent review.

Implemented:

- Added `app/backend/api/first_testing.py` with `python -m app.backend.api.first_testing`.
- Exposed `run_first_testing()`, `first_testing_to_json()`, and `format_first_testing_summary()` from `app.backend.api`.
- Added validation for direct `.E01` input and `--evidence-dir` plus `--first-segment`, required `--case`, optional `--output`, `--case-name`, `--case-description`, `--actor`, `--adapter pyewf|stub`, `--json-only`, and `--redact-paths`.
- Rejected `.E02+` primary inputs, unsupported extensions, missing/conflicting input forms, direct directories, and unsafe evidence/case/output overlap before artifact writes.
- Created the required S4.5-IMP01 artifact layout: `case.db`, `run-manifest.json`, `command-summary.txt`, `intake.json`, `case.json`, `audit.json`, and `unsupported-sections.json`.
- Reused `run_e01_intake()`, `connect()`, `initialize_schema()`, `insert_case()`, `insert_evidence_source()`, `insert_audit_event()`, and `list_audit_events()`.
- Added focused tests in `app/tests/test_first_testing_command.py`.

Scope intentionally not implemented:

- No real EWF metadata or verification.
- No EWF-backed stream, partition/filesystem parsing, E01-backed content provider, file-list output, static HTML, search/timeline, UI, reports, deleted recovery, carving, packaging, native dependency installation, real E01 fixture, commit, or push.
- Manual E01 status remains `Untested`.

Verification:

- Focused run: `python -m pytest app\tests\test_first_testing_command.py`: 8 passed in 9.86s.
- Full run: `python -m pytest`: 160 passed in 9.12s.

## 2026-07-16 - S4.5-IMP01 Ticket Preparation

Result: ready for coding-agent handoff; implementation not started by reviewer.

Prepared:

- Added `tickets/stage-4.5/S4.5-IMP01-first-testing-command-shell.md`.
- Added `prompts/vscode-agent/2026-07-16-s4.5-imp01-first-testing-command-shell.md`.
- Scoped the ticket to the first-testing command shell, safe case workspace, intake persistence, run manifest, command summary, audit artifact, and unsupported-section output.
- Required reuse of existing intake and case-store helpers: `run_e01_intake()`, `connect()`, `initialize_schema()`, `insert_case()`, `insert_evidence_source()`, `insert_audit_event()`, and `list_audit_events()`.
- Required focused automated coverage without real E01 fixtures or native forensic dependencies.

Scope intentionally excluded:

- No real EWF metadata, real EWF verification, EWF-backed stream, partition/filesystem parsing, E01-backed content provider, file-list output, static HTML output, search/timeline implementation, UI, reports, deleted recovery, carving, packaging, commit, or push.

Reviewer notes:

- S5-T01A is accepted and done, so active guidance no longer permits bypassing the Stage 4.5 implementation runway.
- S4.5-IMP01 is the next practical implementation ticket.
- S5-T02 through S5-T16 remain `Draft`; Stage 5 search/timeline remains blocked until S4.5-IMP01 through S4.5-IMP06 are completed and reviewed.

Verification:

- Pre-handoff status scan confirmed the S4.5-IMP01 ticket and prompt are present and Stage 5 remains blocked.
- `python -m pytest`: 152 passed in 3.25s.

## 2026-07-16 - S5-T01A Stage 4.5 Gate Language Hardening

Result: accepted; S5-T01A marked `Done`.

Implemented:

- Removed active Stage 4.5 wording that implied the user could bypass or set aside the Stage 4.5 implementation runway to begin Stage 5 search/timeline.
- Clarified that the user may pause work, review documentation, or choose when to start S4.5-IMP01, but S5-T02 or later search/timeline implementation must wait for S4.5-IMP01 through S4.5-IMP06 to be completed and reviewed.
- Kept S5-T01 as `Done` with the accepted failed-gate/blocker result.
- Kept S5-T02 through S5-T16 as `Draft`.
- Kept S4.5-IMP01 as the next practical implementation ticket.

Reviewer result:

- No blocking findings.
- Confirmed active Stage 4.5 and manual-testing guidance no longer allows Stage 5 search/timeline to proceed by setting aside or bypassing S4.5-IMP01 through S4.5-IMP06.
- Confirmed remaining old-wording matches are historical or explanatory, not active bypass guidance.
- Marked S5-T01A as `Done`.

Scope intentionally not implemented:

- No app source code, tests, schema, parser behavior, evidence handling behavior, evidence fixtures, first-testing implementation, search/timeline implementation, UI, reports, local artifacts, commit, or push.

Verification:

- Focused active Stage 4.5 wording search: no remaining `set aside`, `priority changes`, `changes priority`, `unless the user changes priority`, `explicitly set aside`, `explicitly moves on`, `user changes priority`, or `unless priority changes` matches.
- Stage 5 status search: no readiness drift for S5-T02 through S5-T16 in the checked indexes.
- Remaining old-wording matches are historical review/log/prompt-history notes, privacy wording unrelated to bypassing, or S5-T01/S5-T01A descriptions of the wording that was hardened.
- `python -m pytest`: 152 passed in 7.64s.

## 2026-07-16 - S5-T01 Readiness And Stage 4.5 Completion Gate

Result: accepted as a completed failed gate; S5-T01 marked `Done`.

Findings:

- S5-T00 is accepted and done.
- No `S4.5-IMP01` through `S4.5-IMP06` implementation ticket files or prompt files were found.
- `app/backend/api/first_testing.py` is absent.
- Reviewed backend code still has only the existing `pyewf` dependency-safe reader skeleton and `pytsk3` dependency-safe filesystem skeleton; real metadata, real verification, EWF-backed streams, real partition/filesystem parsing, and E01-backed file-content providers are not implemented.
- Stage 4.5 has no reviewed first-testing command, output bundle, file-list artifacts, static HTML summary, or confirmed manual E01 workflow.
- Manual E01 status remains `Untested`.
- S5-T02 through S5-T16 must remain `Draft`; Stage 5 search/timeline implementation remains blocked/deferred.

Stage 4.5 completion matrix summary:

- S4.5-IMP01: not created / not implemented / not reviewed.
- S4.5-IMP02: not created / not implemented / not reviewed.
- S4.5-IMP03: not created / not implemented / not reviewed.
- S4.5-IMP04: not created / not implemented / not reviewed.
- S4.5-IMP05: not created / not implemented / not reviewed.
- S4.5-IMP06: not created / not implemented / not reviewed.

Allowed Stage 5 planning inputs remain limited to reviewed record families with honest labels: intake/segment discovery results, explicit case/evidence/audit rows, Stage 2 local-file/stub/provider filesystem and preview records, Stage 3 export manifests/results, and Stage 4 provider-backed hash/signature/mismatch/known-file records. Blocked inputs include real parser-backed E01 metadata, first-testing manifests/file-list artifacts, real EWF verification, EWF-backed partition/filesystem records, E01-backed file-content records, and full-text records from E01 content.

Documentation wording note:

- Current Stage 5 docs and `workflow.md` enforce S5-T01 as the hard gate.
- Older active Stage 4.5 planning/manual-testing docs still contain softer "user changes priority" or "explicitly set aside" wording. This S5-T01 result overrides that wording for Stage 5 readiness.

Reviewer result:

- No blocking issue with the S5-T01 failed-gate record itself.
- Accepted S5-T01 as `Done` with Stage 5 search/timeline still blocked/deferred.
- Created S5-T01A as a small documentation-hardening follow-up before S4.5-IMP01 preparation.

Scope intentionally not implemented:

- No app source code, tests, parser behavior, schema, native dependency setup, evidence fixtures, first-testing implementation, search/timeline implementation, UI, reports, local artifacts, commit, or push.

Verification:

- Coding-agent run: `python -m pytest`: 152 passed in 3.34s.
- Reviewer rerun after S5-T01 acceptance and S5-T01A ticket creation: `python -m pytest`: 152 passed in 7.85s.

## 2026-07-16 - S5-T00 Documentation Organization Cleanup

Result: accepted; S5-T00 marked `Done`.

Implemented:

- Applied the S5-T00 source-of-truth model across the main project docs and indexes.
- Reduced duplicate long status narrative in `readme.md` and `plan.md`.
- Kept `tickets/` as ticket scope/status and `prompts/vscode-agent/` as prompt history.
- Marked S5-T00 as `Review` while keeping S5-T01 through S5-T16 as draft future work.
- Confirmed S5-T01 remains the hard gate before S5-T02+ search/timeline implementation.
- Removed `prompts/stage-5a-onboarding/` after confirming it was empty and had no unique information to preserve.

Reviewer result:

- No blocking findings.
- Updated the Stage 5 review-agent handoff prompt to describe the stage-5a cleanup candidates as resolved rather than current folders to inspect.
- Marked S5-T00 as `Done`.

Scope intentionally not implemented:

- No app source code, tests, parser behavior, native dependency setup, evidence handling behavior, UI/reporting, Stage 4.5 first-testing implementation, Stage 5 search/timeline implementation, local artifacts, evidence files, fixtures, commit, or push.

Verification:

- Coding-agent run: `python -m pytest`: 152 passed in 7.15s.
- Reviewer rerun after S5-T00 acceptance/status updates: `python -m pytest`: 152 passed in 5.58s.

## 2026-07-15 - Stage 5 Detailed Ticket Population

Result: ready for user/review confirmation.

Implemented:

- Read the Stage 5 review-agent handoff prompt and populated detailed Stage 5 tickets S5-T01 through S5-T16.
- Added matching paste-ready VS Code coding-agent prompts for S5-T01 through S5-T16.
- Updated the Stage 5 README, main plan, prompt indexes, handoff prompt, workflow notes, and current status docs so S5-T00 remains the documentation cleanup gate and S5-T01 is the hard Stage 4.5 completion gate.
- Documented that S5-T01 must block S5-T02 and later if the Stage 4.5 substantial-test implementation runway is incomplete.

Scope intentionally not implemented:

- No Python source behavior, tests, schema, parser behavior, evidence handling behavior, native dependency setup, search/timeline implementation, UI, reporting, local artifacts, E01 fixtures, commit, or push.

Verification:

- `python -m pytest`: 152 passed in 4.75s.

## 2026-07-15 - S4.5-T08 Documentation And Review Handoff

Result: ready for user/review confirmation.

Implemented:

- Completed the S4.5-T08 documentation-only handoff and marked the ticket `Review`.
- Reconciled Stage 4.5 status across top-level docs, app/backend docs, ticket indexes, prompt indexes, manual-testing docs, progression, review notes, and documentation logs.
- Confirmed S4.5-T00 through S4.5-T07 remain planning in review.
- Confirmed the implementation runway from S4.5-IMP01 through S4.5-IMP06 stays visible, with S4.5-IMP01 as the next practical implementation slice unless the user changes priority.
- Preserved the current real-E01 truth: segment filename discovery exists, but real EWF metadata, real verification, partition/filesystem parsing, and E01-backed file-content extraction do not.
- Kept Stage 5 search/timeline deferred and left broad documentation organization cleanup to S5-T00.

Scope intentionally not implemented:

- No Python source behavior, tests, schema, parser behavior, native dependency setup, evidence handling behavior, UI/reporting, Stage 5 search/timeline implementation, broad S5-T00 cleanup, local artifacts, E01 fixtures, dependency installation, commit, or push.

Tests:

- `python -m pytest`: 152 passed in 10.64s.

## 2026-07-15 - S4.5-T07 Workflow Guardrail Review Optimization

Result: ready for user/review confirmation.

Implemented:

- Sent the S4.5-T06 documentation-only handoff prompt to the Stage 4.5 coding-agent task.
- Expanded S4.5-T07 into a detailed documentation-only workflow, guardrail, and review optimization plan.
- Added review gates for the future Stage 4.5 implementation runway.
- Defined per-slice manual-test/review checklists, required handoff format, review-note categories, `functionality.md` manual-test status rules, privacy/redaction rules, no-overclaim checks, and evidence safety checks.
- Updated `workflow.md` and the manual-testing guide with Stage 4.5 handoff and review rules.
- Added a ticket-specific coding-agent prompt that points to the Stage 4.5 familiarization prompt.

Scope intentionally not implemented:

- No Python source, product behavior, output rendering, parser behavior, first-testing command behavior, file-content providers, search/timeline, UI, packaging, deleted recovery, carving, local artifacts, E01 fixtures, dependency installation, commit, or push.

Tests:

- `python -m pytest`: 152 passed in 7.28s.

## 2026-07-15 - S4.5-T06 File List And Output Plan

Result: ready for user/review confirmation.

Implemented:

- Sent the S4.5-T05 documentation-only handoff prompt to the Stage 4.5 coding-agent task.
- Expanded S4.5-T06 into a detailed documentation-only file-list and output plan.
- Defined command prompt summary, JSON artifact bundle, CSV file-list columns, optional static HTML, redaction rules, and output artifact layout.
- Added an implementation runway lining up S4.5 planning tickets into future buildable implementation slices before Stage 5 search/timeline.
- Added a ticket-specific coding-agent prompt that points to the Stage 4.5 familiarization prompt.

Scope intentionally not implemented:

- No Python source, output rendering, CSV writing, HTML generation, first-testing command behavior, parser behavior, file-content providers, local artifacts, E01 fixtures, dependency installation, search/timeline, reporting UI, packaging, deleted recovery, carving, commit, or push.

Tests:

- `python -m pytest`: 152 passed in 4.26s.

## 2026-07-15 - S4.5-T05 E01 File Content Provider Plan

Result: ready for user/review confirmation.

Implemented:

- Sent the S4.5-T04 documentation-only handoff prompt to the Stage 4.5 coding-agent task.
- Expanded S4.5-T05 into a detailed documentation-only plan for E01-backed file-content providers.
- Defined the shared selected-file content reader direction plus thin provider wrappers for preview, export, and analysis.
- Mapped future real parser bytes to existing `preview_file()`, `export_file()`, `hash_file_content()`, `detect_file_signature()`, and `evaluate_extension_mismatch()` behavior.
- Added provenance, provider identity, status/warning, memory/streaming, deleted/sparse/special-file, test, manual integration, and implementation-sequence planning.
- Added a ticket-specific coding-agent prompt that points to the Stage 4.5 familiarization prompt.

Scope intentionally not implemented:

- No Python source, dependency installation, byte extraction, content reader, provider wrapper, parser behavior, streaming API, first-testing command behavior, tests, schema migration, E01 fixtures, manual evidence run, file-list export, static HTML, search/timeline, reporting, UI, commit, or push.

Tests:

- `python -m pytest`: 152 passed in 4.30s.

## 2026-07-15 - S4.5-T04 EWF Stream, Partition, And Filesystem Plan

Result: ready for user/review confirmation.

Implemented:

- Sent the S4.5-T03 documentation-only handoff prompt to the Stage 4.5 coding-agent task.
- Expanded S4.5-T04 into a detailed documentation-only plan for EWF-backed image streams, partition discovery, and real filesystem metadata parsing.
- Recorded that local `pyewf` and `pytsk3` are still missing.
- Defined the future data path from selected `.E01` to `ImageByteStream`, `VolumeInfo`, `FilesystemResult`, `FilesystemEntry`, and `list_directory()` outputs.
- Added dependency/status/warning planning, mocked test strategy, manual integration logging, and future implementation boundaries.
- Added a ticket-specific coding-agent prompt that points to the Stage 4.5 familiarization prompt.

Scope intentionally not implemented:

- No Python source, dependency installation, EWF stream, partition parser, pytsk image wrapper, real filesystem parser, tests, schema migration, E01 fixtures, manual evidence run, file-content provider, preview/export/hash/signature bridge, file-list export, static HTML, search/timeline, reporting, UI, commit, or push.

Tests:

- `python -m pytest`: 152 passed in 3.65s.

## 2026-07-15 - S4.5-T03 Pyewf Metadata And Verification Plan

Result: ready for user/review confirmation.

Implemented:

- Sent the S4.5-T02 documentation-only handoff prompt to the Stage 4.5 coding-agent task.
- Expanded S4.5-T03 into a detailed documentation-only plan for real `pyewf` metadata and verification investigation.
- Recorded that local `pyewf` is still missing.
- Defined dependency investigation questions, metadata field scope, verification statuses, warning codes, test strategy, manual integration logging, and future implementation boundaries.
- Added a ticket-specific coding-agent prompt that points to the Stage 4.5 familiarization prompt.

Scope intentionally not implemented:

- No Python source, dependency installation, real metadata reader, real verification, tests, schema migration, E01 fixtures, manual evidence run, EWF stream, partition/filesystem parser, file-content provider, preview/export/hash/signature bridge, file-list export, static HTML, search/timeline, UI, commit, or push.

Tests:

- `python -m pytest`: 152 passed in 5.38s.

## 2026-07-15 - S4.5-T02 Case Workspace And First-Testing Command Plan

Result: ready for user/review confirmation.

Implemented:

- Expanded S4.5-T02 into a detailed documentation-only plan for the first-testing command and case workspace.
- Defined the future command target, arguments, case workspace layout, manifest fields, text summary shape, JSON artifacts, and audit expectations.
- Mapped the future command to current intake and case-store helpers.
- Added a ticket-specific coding-agent prompt that points to the Stage 4.5 familiarization prompt.

Scope intentionally not implemented:

- No Python source, first-testing command, tests, schema migration, dependency installation, evidence fixtures, real EWF metadata, verification, EWF stream, partition/filesystem parser, file-content provider, preview/export/hash/signature bridge, file-list export, static HTML, search/timeline, UI, commit, or push.

Tests:

- `python -m pytest`: 152 passed in 5.64s.

## 2026-07-15 - Stage 4.5 First Testing Scaffold

Result: ready for user/review confirmation.

Implemented:

- Added Stage 4.5 scaffold for first testing with user-provided E01 files before Stage 5 search/timeline.
- Added draft tickets under `tickets/stage-4.5/`.
- Added onboarding prompt and app-side user-provided E01/script/manual-test placeholder folders.
- Updated planning and app docs to keep Stage 4.5 separate from Stage 5 search/timeline implementation.
- Documented the current functionality summary and the key real-E01 limit: segment discovery exists, but real EWF metadata, verification, partition parsing, filesystem parsing, and file-content extraction do not.

Scope intentionally not implemented:

- No Python source behavior, tests, schema, API wrapper, first-testing command, real `pyewf` metadata reader, verification, search/timeline, persistence, UI, real partition/filesystem parser work, deleted recovery, carving, commit, or push.

Expected verification:

- `python -m pytest`.

## 2026-07-15 - S4.5-T00 Current-Code Utilization Plan

Result: ready for user/review confirmation.

Implemented:

- Expanded S4.5-T00 with a current-code utilization table for the desired command-line E01 MVP.
- Mapped intended functionality to current functions and classes:
  - intake and segment discovery;
  - case-store helpers;
  - EWF adapter contracts;
  - image/volume/filesystem shapes;
  - preview/export/analysis provider surfaces;
  - audit and output artifacts.
- Reworked the Stage 4.5 follow-on ticket sequence to align with the current goal.
- Marked Stage 5 search/timeline as deferred behind first-testing.

Scope intentionally not implemented:

- No source behavior, tests, schema, API wrapper, real EWF metadata reader, verification, EWF stream, parser, file-content provider, output renderer, search/timeline, UI, commit, or push.

Expected verification:

- `python -m pytest`.

## 2026-07-15 - S4.5-T01 User-Provided E01 Handling Plan

Result: ready for user/review confirmation.

Implemented:

- Expanded S4.5-T01 into a detailed user-provided E01 handling and privacy plan.
- Updated the user-provided E01 fixture documentation and Stage 4.5 manual-testing guide.
- Added a ticket-specific coding-agent prompt that points to the Stage 4.5 familiarization prompt.

Scope intentionally not implemented:

- No Python source, tests, schema, first-testing command, dependency installation, E01 fixtures, parser behavior, search/timeline, UI, commit, or push.

Expected verification:

- `python -m pytest`.

## 2026-07-15 - S4-T07 Review

Result: approved for commit.

Findings:

- No blocking issues found.
- S4-T07 stayed documentation/status reconciliation only; no Python source, schema, tests, API behavior, persistence behavior, parser behavior, search/timeline code, UI, native dependency configuration, Stage 5 implementation, commit, or push was added.
- Final Stage 4 docs accurately describe S4-T01 contracts, S4-T02 provider-backed hashing, S4-T03 bounded signature detection, S4-T04 extension mismatch over existing signature results plus metadata, S4-T05 fixture-sized known-file matching over existing hash results plus caller-supplied in-memory records, and S4-T06 persistence planning only.
- Stage 3 export-output SHA-256 verification remains separate from Stage 4 per-file analysis hashing, and whole-image verification remains unsupported.
- Docs keep synthetic/generated/provider-backed labels visible and preserve the warning that Stage 5 must not turn synthetic or stub-only data into confident real-evidence findings.
- Stage 5 remains rough/draft with search/timeline unstarted; this older readiness note is now superseded by S5-T00 documentation cleanup first, with readiness/risk audit moved to S5-T01.
- Manual-test status remains `Untested`.

Tests:

- `python -m pytest`: 152 passed in 2.45s.

Residual notes:

- Stage 5 should run documentation cleanup first, then a readiness/risk audit that either adds a reality anchor or explicitly limits search/timeline to provenance-rich, labeled provider-backed records.

## 2026-07-15 - S4-T07 Stage 4 Documentation Handoff

Result: ready for research/review agent review.

Implemented:

- Marked `tickets/stage-4/S4-T07-docs-review-handoff.md` as `Review`.
- Reconciled top-level, backend, ticket, fixture, progression, review, and documentation logs for the final Stage 4 behavior and limits.
- Documented S4-T01 contracts, S4-T02 provider-backed hashing, S4-T03 bounded signature detection, S4-T04 extension mismatch over existing signature results plus metadata, S4-T05 fixture-sized known-file matching over existing hash results plus caller-supplied in-memory records, and S4-T06 persistence planning only.
- Re-stated that Stage 3 export-output SHA-256 verification is separate from Stage 4 per-file analysis hashing, and whole-image verification remains unsupported.
- Kept synthetic/generated/provider-backed labels visible and kept Stage 5 rough/draft with all tickets still unstarted.

Scope intentionally not implemented:

- No Python source, schema, tests, API behavior, persistence behavior, search/timeline code, UI, parser behavior, native dependency configuration, Stage 5 implementation, commit, or push.

Tests:

- `python -m pytest`: 152 passed in 4.21s.

## 2026-07-15 - S4-T07 Handoff Preparation

Result: ready for implementation agent.

Guardrails:

- S4-T07 is documentation/review-handoff only.
- S4-T01 through S4-T06 are reviewed and done; S4-T07 should reconcile docs and prepare Stage 5 readiness notes without new behavior.
- Do not modify Python source, tests, SQLite schema, case-store helpers, API wrappers, persistence behavior, search/timeline code, UI, parser code, native dependency configuration, commit, or push.
- Final Stage 4 docs must separate provider-backed per-file analysis from Stage 3 export-output verification and unsupported whole-image verification.
- Docs must preserve synthetic/generated/provider-backed labels and avoid implying real evidence-backed filesystem extraction.
- Stage 5 must remain rough/draft and should preserve source/provenance/status/warnings/source-kind uncertainty before any search/timeline implementation.

Expected verification:

- `python -m pytest`.

## 2026-07-15 - S4-T06 Review

Result: approved for commit.

Findings:

- No blocking issues found.
- S4-T06 stayed planning/documentation-only and did not change Python source, tests, SQLite schema, case-store exports, file export behavior, or Stage 4 analysis behavior.
- The persistence decision is correctly deferred until a later reviewed workflow/API/job layer owns explicit caller intent, connection/case context, and policy for successful, failed, partial, and not-evaluated results.
- Future persistence requirements preserve source provenance, content-source identity, source kind, synthetic/generated labels, status JSON, full result JSON with `schema_version`, warnings, timestamps, and provider/parser names and versions.
- The recommended future schema direction is clear enough for a later ticket: a parent `analysis_results` table plus optional child/index tables for hash digests, signature detections, extension mismatch flags, and known-file matches.
- Docs explicitly state that embedded `case_id` or `evidence_id` values in analysis provenance do not trigger writes, and standalone Stage 4 helper calls remain non-persistent.
- Search/timeline/reporting, UI, external known-file dataset storage, real parser work, native dependencies, S4-T07, and Stage 5 remain deferred.

Tests:

- `python -m pytest`: passed with 152 tests.

Residual notes:

- S4-T07 should reconcile Stage 4 docs and preserve the reality-anchor warning before Stage 5 search/timeline work begins.

## 2026-07-15 - S4-T06 Case-Store Persistence Plan Handoff

Result: ready for research/review agent review.

Implemented:

- `tickets/stage-4/S4-T06-case-store-persistence-plan.md` is marked `Review`.
- S4-T06 documents that analysis-result persistence is deferred beyond this ticket.
- The plan records an explicit opt-in future persistence context: SQLite connection, explicit case id, optional evidence id, optional actor/examiner, optional analysis job id, failed/partial/not-evaluated result policy, and caller intent to persist.
- Future table requirements are documented for stable result id, case/evidence ids, analysis type, source provenance JSON, content-source identity JSON, source kind, synthetic/generated flags, status code/JSON, full result JSON with `schema_version`, warnings JSON, timestamps, and parser/provider name/version fields.
- Future index/query needs are documented for case/evidence id, file id/path, analysis type, status, source kind, hash digests, detected signatures, mismatch values, and known-file categories.
- The recommended future schema direction is a parent `analysis_results` table plus optional child/index tables for hash digests, signature detections, extension mismatch flags, and known-file matches.
- Docs state that embedded `case_id` or `evidence_id` in analysis provenance must not trigger writes, and standalone Stage 4 helper calls must remain non-persistent.

Scope intentionally not implemented:

- No SQLite schema migration, new table, case-store helper, API wrapper, automatic persistence, background job, test change, S4-T01 through S4-T05 behavior change, search/timeline/reporting/UI, external known-file dataset storage, real parser work, native dependency, S4-T07, Stage 5, commit, or push.

Tests:

- Full run: `python -m pytest` reported 152 passed in 3.10s.

## 2026-07-15 - S4-T06 Handoff Preparation

Result: ready for implementation agent.

Guardrails:

- S4-T06 is planning/documentation-only.
- Do not modify `app/backend/case_store/schema.py`, add migrations, add tables, add persistence helpers, add API wrappers, or add tests unless a code change is explicitly approved later.
- The current case store has cases, evidence sources, audit events, and schema migrations only.
- Stage 3 export audit is the model for explicit opt-in persistence; embedded source `case_id` or `evidence_id` must not trigger writes.
- The future plan must preserve source provenance, content-source identity, source kind, synthetic/generated labels, statuses, warnings, timestamps, and full result JSON.
- Future persistence should be designed for hash, signature, extension mismatch, and known-file match result shapes, while keeping search/timeline/reporting out of Stage 4.
- Do not change S4-T01 through S4-T05 behavior, do not add background jobs, and do not start Stage 5 work.

Expected verification:

- `python -m pytest`.

## 2026-07-14 - S4-T05 Review

Result: approved for commit.

Findings:

- No blocking issues found.
- `app/backend/forensic_core/content_analysis.py` adds fixture-sized known-file matching through `KnownFileRecord`, `KnownFileMatchResult`, `match_known_file_hashes()`, `match_known_files()`, and `known_file_match_result_to_json()`.
- The matcher consumes an existing S4-T02 `HashAnalysisResult` plus caller-supplied in-memory records only; it does not accept providers, read bytes, read known-file lists from disk/network, or calculate hashes internally.
- SHA-256, MD5, and SHA-1 records are normalized with the same algorithm spelling rules as S4-T02, and digest comparison is case-insensitive.
- Matching prefers SHA-256 for the top-level match fields while preserving all records that match available computed digests.
- Results preserve source provenance, content-source identity, source kind/status, bytes analyzed, hash status, digest statuses, hash timestamps, source hash warnings, matched record metadata, and synthetic/generated context warnings.
- Non-ok hashes, missing computed digests, invalid records, duplicate records, no-match states, and conflicting categories for the same digest are structured and tested.
- `known_file_no_match` is treated as a successful evaluation status while the outcome is carried by `matched=False`; review accepted this convention because callers should use the explicit `matched` field.
- S4-T05 stayed in scope and did not add case-store persistence, schema migrations, external datasets, known-file file readers, network access, search/timeline, UI/reporting, real parser work, deleted recovery, carving, native dependencies, S4-T02/S4-T03/S4-T04 behavior changes, export-output behavior changes, or Stage 5 work.

Tests:

- `python -m pytest app/tests/test_content_analysis_known_files.py`: 12 passed in 0.19s.
- `python -m pytest`: 152 passed in 3.47s.

Residual notes:

- S4-T06 should decide persistence as a plan or carefully scoped implementation only after preserving these standalone result shapes and synthetic/generated source labels.

## 2026-07-14 - S4-T05 Known-File Matching Handoff

Result: ready for research/review agent review.

Implemented:

- `app/backend/forensic_core/content_analysis.py` adds `KnownFileRecord`, `KnownFileMatchResult`, `match_known_file_hashes()`, `match_known_files()`, and `known_file_match_result_to_json()`.
- The matcher consumes an existing S4-T02 `HashAnalysisResult` plus caller-supplied in-memory records only. It does not accept providers, read bytes, read known-file lists from disk/network, or calculate hashes internally.
- SHA-256, MD5, and SHA-1 records are normalized with the same algorithm spelling rules as S4-T02, and digest comparison is case-insensitive.
- Matching prefers SHA-256 for the top-level match fields while preserving all records that match available computed digests.
- Results preserve source provenance, content-source identity, source kind/status, bytes analyzed, hash status, digest statuses, hash timestamps, source hash warnings, matched record metadata, and synthetic/generated context warnings.
- Non-ok hashes, missing computed digests, invalid records, duplicate records, no-match states, and conflicting categories for the same digest are structured and tested.

Scope intentionally not implemented:

- No S4-T02 hash calculation changes, S4-T03 signature detection changes, S4-T04 extension mismatch changes, analysis provider argument, byte reads, known-file file readers, external datasets, NSRL import, case-store persistence, search/timeline, UI/reporting, real parser work, deleted recovery, carving, native dependencies, export-output behavior changes, or Stage 5 work.

Tests:

- Focused S4-T05 run: `python -m pytest app/tests/test_content_analysis_known_files.py` reported 12 passed in 0.37s.
- Full run: `python -m pytest` reported 152 passed in 5.97s.

## 2026-07-14 - S4-T05 Handoff Preparation

Result: ready for implementation agent.

Guardrails:

- S4-T05 consumes reviewed S4-T02 `HashAnalysisResult` objects plus tiny caller-supplied in-memory known-file records only.
- The matcher must not accept an analysis provider, read bytes, read known-file data from disk/network, or call `hash_file_content()` / `calculate_hashes()` internally.
- Preserve hash result source provenance, content-source identity, source kind/status, bytes analyzed, hash status, digest statuses, timestamps, and warnings.
- Keep categories small and explicit: `known_good`, `known_bad`, and `known_unknown`.
- Invalid records and conflicting categories should be structured and tested, not silently ignored or resolved.
- Known-file matches against synthetic/generated provider bytes must keep those labels visible and must not be worded as real evidence-backed database matches.
- Do not add case-store persistence, schema migrations, NSRL imports, large/external datasets, file readers, network access, search/timeline, UI/reporting, real parser work, deleted recovery, carving, native dependencies, S4-T02/S4-T03/S4-T04 behavior changes, or Stage 5 work.

Expected verification:

- `python -m pytest`.

## 2026-07-14 - S4-T04 Review

Result: approved for commit.

Findings:

- No blocking issues found.
- `app/backend/forensic_core/content_analysis.py` adds extension mismatch contracts and evaluators through `SignatureExtensionRule`, `SIGNATURE_EXTENSION_RULES`, `SUPPORTED_SIGNATURE_EXTENSIONS`, `ExtensionMismatchResult`, `evaluate_extension_mismatch()`, `check_extension_mismatch()`, and `extension_mismatch_result_to_json()`.
- The evaluator consumes an existing S4-T03 `SignatureAnalysisResult` plus copied file name/path metadata only; it does not accept providers, read bytes, or call `detect_file_signature()` internally.
- Conservative rules cover PDF, PNG, JPEG extension variants, GIF, ZIP/container allow-list extensions, ELF, and MZ executable candidates.
- Evaluated matches and mismatches use explicit `mismatch=False` or `True`; missing metadata, no extension, non-file sources, non-ok signature statuses, missing detected type, and unsupported detected types return structured not-evaluated results with `mismatch=None`.
- Results preserve S4-T03 source provenance, content-source identity, signature status, detected type/signature/MIME fields, signature timestamps, source/provider warnings, and new mismatch warnings.
- `extension_mismatch` is treated as a successful evaluation status while the finding is carried by `mismatch=True`; review accepted this convention because callers are not expected to infer the finding from `status.ok`.
- S4-T04 stayed in scope and did not add known-file matching, case-store persistence, search/timeline, UI/reporting, real parser work, deleted recovery, carving, native dependencies, S4-T02/S4-T03 behavior changes, export-output behavior changes, or Stage 5 work.

Tests:

- `python -m pytest`: 140 passed in 3.14s.

Residual notes:

- S4-T05 should remain fixture-sized and should not make synthetic/provider-backed hash results look like real evidence-backed known-file matches.

## 2026-07-14 - S4-T04 Extension Mismatch Rules Handoff

Result: ready for research/review agent review.

Implemented:

- `app/backend/forensic_core/content_analysis.py` adds `SignatureExtensionRule`, `SIGNATURE_EXTENSION_RULES`, `SUPPORTED_SIGNATURE_EXTENSIONS`, `ExtensionMismatchResult`, `evaluate_extension_mismatch()`, `check_extension_mismatch()`, and `extension_mismatch_result_to_json()`.
- The evaluator consumes an existing S4-T03 `SignatureAnalysisResult` and source file name/path metadata only. It does not accept providers, read bytes, or call `detect_file_signature()` internally.
- Conservative rules cover PDF, PNG, JPEG extension variants, GIF, ZIP/container allow-list extensions, ELF, and MZ executable candidates.
- Matching and mismatching evaluated states include explicit `mismatch=False` or `True`; missing metadata, no extension, non-file sources, non-ok signature statuses, missing detected type, and unsupported detected types return not-evaluated results with `mismatch=None`.
- Results preserve source provenance, content-source identity, signature status, detected type/signature/MIME fields, signature timestamps, source/provider warnings, and new mismatch warnings.
- `app/tests/test_content_analysis_extension_mismatch.py` covers case-insensitive matches, mismatches, JPEG variants, ZIP allow-list behavior, MZ matches/mismatches, missing/no-extension states, unknown/insufficient signatures, unsupported types, directory sources, provenance/warnings, JSON safety, and S4-T02/S4-T03 regression behavior.

Scope intentionally not implemented:

- No S4-T02 hashing changes, S4-T03 signature detection changes, provider byte reads, known-file matching, case-store persistence, search/timeline, UI/reporting, real parser work, deleted recovery, carving, native dependencies, export-output changes, or Stage 5 work.

Tests:

- `python -m pytest`: 140 passed in 4.99s.

## 2026-07-14 - S4-T04 Handoff Preparation

Result: ready for implementation agent.

Guardrails:

- S4-T04 consumes reviewed S4-T03 `SignatureAnalysisResult` objects plus source metadata only.
- Extension mismatch evaluation must not read provider bytes, accept an analysis provider, or call signature detection internally.
- Evaluate only when the source is a file, the signature status is `ok`, a detected type exists, an extension rule exists, and file metadata includes an extension.
- Unknown, insufficient, failed, unsupported, missing, and no-extension states should be structured not-evaluated results rather than mismatches.
- Preserve S4-T03 source provenance, content-source identity, detected fields, source labels, timestamps, and warnings.
- Include an explicit mismatch value instead of making callers infer findings only from status truthiness.
- Do not add known-file matching, case-store persistence, search/timeline, UI/reporting, real parser work, deleted recovery, carving, native dependencies, S4-T02/S4-T03 behavior changes, export-output changes, or Stage 5 work.

Expected verification:

- `python -m pytest`.

## 2026-07-14 - S4-T03 Review

Result: approved for commit.

Findings:

- No blocking issues found.
- `app/backend/forensic_core/content_analysis.py` adds bounded provider-backed signature detection through `FileSignatureDefinition`, `SUPPORTED_FILE_SIGNATURES`, `detect_file_signature()`, and `analyze_file_signature()`.
- Detection reuses the S4-T02 `AnalysisContentProvider` boundary and inspects only a bounded prefix of provider bytes.
- Invalid or non-positive max-byte requests, including non-integer values, return structured `invalid_analysis_request` results before provider reads.
- Directory/non-file entries are rejected before provider reads, while metadata-only sources, unavailable provider content, and provider exceptions return structured non-ok `SignatureAnalysisResult` objects.
- Known signatures are conservative for PDF, PNG, JPEG, GIF87a/GIF89a, ZIP header variants, ELF, and MZ executable candidates.
- Unknown prefixes and partial known prefixes return structured `unknown_signature` or `insufficient_signature_bytes` statuses rather than guessed types.
- Results preserve S4-T01 source provenance, content-source identity, source kind/status, max bytes requested, byte count inspected when applicable, read-only assertion, timestamps, and warnings.
- Synthetic/generated provider bytes are labeled through content-source identity and warnings.
- S4-T03 stayed in scope and did not use preview-rendered output, preview providers, export providers, written export artifacts, or filesystem metadata as signature source bytes.
- S4-T03 did not add extension mismatch checks, known-file matching, case-store persistence, search/timeline, UI/reporting, real parser work, deleted recovery, carving, native dependencies, S4-T02 hash behavior changes, export-output behavior changes, or Stage 5 work.

Tests:

- `python -m pytest`: 127 passed in 5.39s.

Residual notes:

- S4-T04 should consume reviewed signature result fields plus file metadata only, and should not reinterpret unknown or insufficient signature results as mismatches.

## 2026-07-14 - S4-T03 File Signature Detection Handoff

Result: ready for research/review agent review.

Implemented:

- `FileSignatureDefinition` and `SUPPORTED_FILE_SIGNATURES` define a small dependency-free magic-byte table.
- `detect_file_signature()` and `analyze_file_signature()` reuse the S4-T02 `AnalysisContentProvider` boundary.
- Detection inspects only a bounded prefix of provider bytes through `content.data[:max_bytes]`.
- Known signatures cover PDF, PNG, JPEG, GIF87a/GIF89a, ZIP header variants, ELF, and conservative MZ executable candidates.
- Invalid or non-positive max-byte requests return structured non-ok results before provider reads.
- Directory/non-file, metadata-only, unavailable-content, provider-exception, insufficient partial known signature, and unknown-signature paths return structured non-ok `SignatureAnalysisResult` objects.
- Results preserve S4-T01 source provenance, content-source identity, source kind/status, max bytes requested, bytes inspected when applicable, read-only assertion, timestamps, warnings, and JSON-safe detection fields.
- Synthetic/generated bytes are labeled with explicit source identity and warnings.

Scope intentionally not implemented:

- No extension mismatch checks, known-file matching, case-store persistence, search/timeline, UI/reporting, real EWF parsing, real partition/filesystem parsing, deleted recovery, carving, native dependencies, or Stage 5 work.
- No preview-rendered output, preview provider, export provider, written export artifact, or metadata-only filesystem entry is treated as signature source content.
- S4-T02 hash behavior and Stage 3 export-output SHA-256 behavior are unchanged.

Tests:

- Focused run before docs: `python -m pytest app/tests/test_content_analysis_contracts.py app/tests/test_content_analysis_hashing.py app/tests/test_content_analysis_signatures.py`: 28 passed in 0.38s.
- Final full-suite run: `python -m pytest`: 127 passed in 4.41s.

## 2026-07-14 - S4-T03 Handoff Preparation

Result: ready for implementation agent.

Guardrails:

- S4-T03 builds on reviewed S4-T01 contracts and reviewed S4-T02 provider-backed content handling.
- Signature detection must use explicit Stage 4 analysis content providers only.
- Inspect only a bounded prefix of provider bytes.
- Validate invalid or non-positive max-byte requests before provider reads.
- Keep detection dependency-free and conservative: PDF, PNG, JPEG, GIF, ZIP, ELF, and MZ executable candidate are enough.
- Unknown or insufficient content should return structured non-ok results, not guessed types.
- Do not add extension mismatch checks; that is S4-T04.
- Do not add known-file matching, case-store persistence, search/timeline, UI/reporting, parser work, deleted recovery, carving, or native dependencies.
- Do not use preview-rendered output, preview providers, export providers, written export artifacts, or filesystem metadata as signature source bytes.
- Do not change S4-T02 hash behavior or Stage 3 export-output verification.

Expected verification:

- `python -m pytest`.

## 2026-07-14 - S4-T02 Review

Result: approved for commit.

Findings:

- No blocking issues found.
- `app/backend/forensic_core/content_analysis.py` adds provider-backed hash behavior through `AnalysisContent`, `AnalysisContentProvider`, `StubAnalysisContentProvider`, `hash_file_content()`, and `calculate_hashes()`.
- SHA-256 is computed by default from explicit Stage 4 analysis-provider bytes; MD5 and SHA-1 are computed only when requested.
- Unsupported and malformed algorithm requests return structured non-ok results before provider bytes are read.
- Directory/non-file entries, metadata-only sources without a provider, unavailable provider content, and provider exceptions return structured non-ok `HashAnalysisResult` objects.
- Results preserve S4-T01 source provenance, content-source identity, byte count when available, read-only assertion, timestamps, and warnings.
- Synthetic and generated fixture bytes are labeled through content-source identity and warnings.
- S4-T02 stayed in scope and did not use preview-rendered output, preview providers, export providers, written export artifacts, or filesystem metadata as analysis source bytes.
- S4-T02 did not add signature detection, extension mismatch checks, known-file matching, case-store persistence, search/timeline, UI/reporting, real parser work, deleted recovery, carving, native dependencies, export-output behavior changes, or Stage 5 work.

Tests:

- `python -m pytest`: 116 passed in 4.21s.

Residual notes:

- S4-T03 should reuse the explicit Stage 4 analysis-provider boundary for bounded signature bytes, while keeping signature detection separate from extension mismatch and known-file matching.

## 2026-07-14 - S4-T02 Provider-Backed Hashing Handoff

Result: ready for research/review agent review.

Implemented:

- `AnalysisContent`, `AnalysisContentProvider`, and `StubAnalysisContentProvider` define an explicit Stage 4 analysis byte boundary separate from preview and export providers.
- `hash_file_content()` and `calculate_hashes()` compute SHA-256 by default from explicit analysis-provider bytes.
- MD5 and SHA-1 are computed only when explicitly requested and remain comparison hashes.
- Algorithm names are normalized before execution, and unsupported or malformed algorithm requests return structured non-ok results before provider reads.
- Structured non-ok paths cover directory/non-file entries, metadata-only sources with no provider, unavailable provider content, and provider exceptions.
- Results preserve S4-T01 source provenance, content-source identity, source kind/status, byte count when available, read-only assertion, timestamps, warnings, and JSON-safe digest output.
- Synthetic/generated bytes are labeled with explicit source identity and warnings.

Scope intentionally not implemented:

- No file signature detection, extension mismatch checks, known-file matching, case-store persistence, search/timeline, UI/reporting, real EWF parsing, real partition/filesystem parsing, deleted recovery, carving, native dependencies, or Stage 5 work.
- No preview-rendered output, preview provider, export provider, written export artifact, or metadata-only filesystem entry is treated as analysis source bytes.
- Stage 3 export-output SHA-256 behavior is unchanged.

Tests:

- Focused run before docs: `python -m pytest app/tests/test_content_analysis_contracts.py app/tests/test_content_analysis_hashing.py`: 17 passed in 0.27s.
- Final full-suite run: `python -m pytest`: 116 passed in 3.38s.

## 2026-07-14 - S4-T02 Handoff Preparation

Result: ready for implementation agent.

Guardrails:

- S4-T02 builds on reviewed S4-T01 contracts.
- Hashes must come from explicit Stage 4 analysis content providers only.
- The implementation may add a dependency-free `StubAnalysisContentProvider`, but it must label synthetic/generated bytes honestly.
- Validate requested algorithms before reading provider bytes.
- SHA-256 should be computed by default.
- MD5 and SHA-1 should be optional comparison hashes only.
- Do not use preview-rendered text/hex, preview providers, Stage 3 exported artifacts, or export providers as implicit analysis source content.
- Do not change Stage 3 export-output verification.
- Do not add signature detection, extension mismatch, known-file matching, persistence, search/timeline, UI, parser work, deleted recovery, carving, or native dependencies.

Expected verification:

- `python -m pytest`.

## 2026-07-14 - S4-T01 Review

Result: approved for commit.

Findings:

- No blocking issues found.
- `app/backend/forensic_core/content_analysis.py` adds contract-only Stage 4 hash/signature structures and does not read bytes, compute hashes, detect signatures, persist results, or invoke preview/export providers.
- `AnalysisSourceProvenance` preserves Stage 2-style metadata without treating it as source content.
- `AnalysisContentSourceIdentity` carries provider/source identity, source kind, read-only assertion, synthetic/generated flags, content size placeholder, parser/source names, version fields, and source status.
- Hash result placeholders use nullable digests and `hash_not_computed`; signature result placeholders use nullable detection fields and `signature_not_checked`.
- Package exports, tests, and docs were updated consistently.
- S4-T01 stayed in scope and did not change Stage 3 export-output SHA-256 verification, claim whole-image verification, add known-file matching, add case-store persistence, start search/timeline/reporting/UI, add parser work, deleted recovery, carving, or native dependencies.

Tests:

- `python -m pytest`: 106 passed in 4.82s.

Residual notes:

- S4-T02 should build directly on these reviewed contracts and add provider-backed hash calculation only from explicit analysis content providers.
- S4-T02 should keep MD5/SHA-1 optional and framed as comparison hashes, while SHA-256 remains the primary digest.

## 2026-07-14 - S4-T01 Hash And Signature Contracts Handoff

Result: ready for research/review agent review.

Implemented:

- `app/backend/forensic_core/content_analysis.py` defines Stage 4 contract-only structures for hash/signature analysis requests, results, statuses, warnings, source provenance, content-source identity, digest placeholders, and signature placeholders.
- `AnalysisSourceProvenance` can be built from Stage 2-style file-entry metadata while preserving optional case/evidence ids, volume provenance, file id/path/name, entry type, allocation/deleted state, filesystem/adapter names, read-only assertion, and timestamps.
- `AnalysisContentSourceIdentity` explicitly labels provider name, source kind, read-only assertion, synthetic/generated flags, source content size, status, parser/source names, and versions.
- Hash contracts preserve requested algorithms, nullable `bytes_analyzed`, and per-algorithm nullable digest placeholders with `hash_not_computed`.
- Signature contracts preserve max bytes requested, nullable `bytes_inspected`, nullable detected type/signature/MIME placeholders, and `signature_not_checked`.
- Package exports, focused tests, and documentation/status notes were added.

Scope intentionally not implemented:

- No hashes are computed.
- No file signatures are detected.
- No preview-rendered text/hex is used as source content.
- No filesystem metadata entry is treated as byte-bearing.
- No Stage 3 export-output SHA-256 behavior was changed.
- No whole-image verification, known-file matching, case-store persistence, search, timeline, reporting, UI, real EWF parsing, partition parsing, filesystem parsing, deleted recovery, carving, native dependency, commit, or push was added.

Tests:

- `python -m pytest`: 106 passed in 4.51s.

## 2026-07-14 - Stage 4 Ticket Planning And Risk Memo

Result: ready to hand S4-T01 to the VS Code implementation agent after user approval.

Current truth:

- Real local byte access is limited to `LocalFileImageStream` reading tiny local files in read-only mode.
- Real write behavior is limited to Stage 3 export artifacts and manifests written from explicit export-provider bytes.
- Stage 3 SHA-256 verifies the written export artifact only; it is not per-file evidence analysis.
- Case-store writes are explicit helper calls or explicit `ExportAuditContext`; source provenance ids alone do not persist anything.
- EWF parsing, image verification, partition parsing, real filesystem parsing, real filesystem content extraction, deleted recovery, carving, UI, search, timeline, reporting, and packaging remain unimplemented.

Stubbed or synthetic today:

- `StubEwfReaderAdapter`, `StubFilesystemAdapter`, `StubPreviewProvider`, and `StubExportContentProvider` provide deterministic synthetic behavior for tests.
- `PyewfEwfReaderAdapter` and `Pytsk3FilesystemAdapter` are dependency/status skeletons; importable native modules are still reported as not implemented.
- Stub filesystem entries are metadata-only and do not provide file bytes by themselves.

Tests prove:

- Result contracts, JSON serialization, read-only assertions, dependency-unavailable status paths, preview bounds, destination safety, overwrite refusal, partial-write cleanup, SHA-256 from written export output, and explicit audit opt-in are covered.

Tests do not prove:

- Real evidence-derived file-content extraction.
- Real EWF/partition/filesystem parsing.
- Whole-image verification.
- Deleted-file recovery or carving.
- Hash/signature analysis over parsed evidence bytes.

Highest-risk architectural gap:

- The project can build correct Stage 4 contracts and provider-backed behavior, but synthetic/provider-backed success can easily look like real forensic analysis if provider identity and source status are not carried everywhere.

Ticket plan:

- `tickets/stage-4/` now contains detailed S4-T00 through S4-T07 tickets.
- S4-T00 is the review-agent familiarization/risk audit and is recorded as done.
- S4-T01 is ready as a contract-only implementation ticket.
- S4-T02 through S4-T07 remain draft until each prior ticket lands and is reviewed.
- `tickets/stage-5/README.md` now captures a rough Stage 5 search/timeline sequence and guardrails.

Verification:

- Baseline before planning edits: `python -m pytest` reported 99 passed in 6.46s.

## 2026-07-14 - Project Reflection Before Stage 4

Weakest point:

- The project has strong contracts, provenance fields, status/warning discipline, and dependency-safe tests, but it still lacks a real evidence-to-file-content pipeline. Beyond tiny local byte-stream reads, the user-facing forensic workflows are stub/provider-backed. That is acceptable for the staged foundation, but it is the biggest risk if later stages start presenting hash, signature, search, timeline, or report output as if it came from parsed evidence.

Most urgent improvement:

- Establish a truthful content-source strategy before Stage 4 analysis expands. The next stage should first prove which bytes are being analyzed, where they came from, how synthetic/provider-backed bytes are labeled, and what would be required before results can claim real evidence-derived file content.

Risks to pass forward:

- Hash/signature analysis can become misleading if it hashes preview-rendered text/hex or synthetic stub bytes without clear source labels.
- Search/timeline/reporting can amplify unsupported parser states if they index or report synthetic/stub data as findings.
- UI or packaging too early would make the project feel more complete than it is.
- Native dependency work could become a time sink unless default tests remain dependency-free and optional integration paths are isolated.
- Audit/reporting workflows must preserve unsupported and partial states, not only successful findings.

Recommendations for future stages:

- Stage 4 should begin with content-source contracts and fixture policy, then add provider-backed hash/signature behavior.
- Stage 5 search/timeline should wait for stable result contracts and should label synthetic/unsupported inputs clearly.
- Stage 6 reporting should foreground provenance, parser status, unsupported recovery, and audit context.
- Packaging/UI should wait until at least one manually tested backend workflow is useful and honest about what is real versus stubbed.

## 2026-07-14 - S3-T06 Review

Result: approved for commit.

Findings:

- No blocking issues found.
- Reconciled Stage 3 status across top-level docs, backend docs, fixture/environment docs, ticket indexes, functionality, plan, progression, review, and documentation log.
- Documented final Stage 3 export behavior: Stage 2-style metadata input, explicit export content provider bytes, synthetic default `StubExportContentProvider` for `stub-file-hello`, examiner/test-selected destinations, overwrite refusal, sibling manifests, SHA-256/byte-count verification from written artifacts, and optional explicit `ExportAuditContext`.
- Re-stated limitations: no real EWF parsing, image verification, partition parsing, filesystem parsing, filesystem extraction, deleted recovery, carving, UI, search, timeline, reporting, bookmarks, notes, packaging, or Stage 4 hash/signature analysis.
- Added Stage 4 handoff guidance to build hash/signature contracts on explicit content providers, avoid preview text/hex as source content, avoid whole-image verification claims without adapter support, and keep known-file matching plus persistence optional until result contracts are reviewed.
- S3-T06 stayed documentation/review-handoff only and did not change backend behavior, export APIs, tests, parser behavior, recovery/carving behavior, UI/search/reporting scope, native dependencies, or evidence fixtures.

Tests:

- `python -m pytest`: 99 passed in 4.42s.

Residual notes:

- Stage 3 is complete as a backend fixture/stub export foundation.
- Stage 4 should begin with explicit content-provider hash/signature contracts, not preview-rendered bytes or metadata-only filesystem entries.

## 2026-07-14 - S3-T06 Stage 3 Docs Handoff Preparation

Result: ready for implementation agent.

Guardrails:

- S3-T06 is documentation/review-handoff only.
- Reconcile the project docs so Stage 3 is accurately described after S3-T01 through S3-T05.
- Keep current limitations visible: no real EWF parsing, image verification, partition parsing, real filesystem parsing, real filesystem byte extraction, deleted recovery, carving, UI, search, timeline, reporting, bookmarks, notes, packaging, or Stage 4 hash/signature analysis.
- Document the export workflow as explicit provider-backed bytes written to examiner-selected output, with manifest provenance, SHA-256/byte-count verification from the written artifact, and optional audit only through explicit `ExportAuditContext`.
- Keep manual-test fields `Untested` unless the user reports a manual run.
- Do not change backend behavior or begin Stage 4 code.

Expected verification:

- Run `python -m pytest`.
- Mark S3-T06 as `Review` after implementation, then stop for final Stage 3 review.

Handoff prep verification:

- `python -m pytest`: 99 passed in 4.36s.

## 2026-07-13 - S3-T05 Review

Result: approved for commit.

Findings:

- No blocking issues found.
- Documentation now distinguishes active allocated file export, deleted entry metadata, deleted-file recovery, carving/unallocated-space recovery, and unsupported or unrecoverable entries.
- Current project truth is recorded: stub filesystem entries are allocated and not deleted; filesystem entries are metadata-only; preview/export providers supply synthetic bytes only for registered ids; current export is not deleted-file recovery; no real deleted-file recovery exists.
- Future recovery requirements are documented for allocation/deleted state, recoverable ranges or explicit recovery content providers, completeness/confidence, overwritten/sparse/partial/unavailable warnings, filesystem-specific provenance, read-only source handling, and compatibility with export manifests, SHA-256/byte counts, and audit logging.
- Future status/warning names include `deleted_recovery_unsupported`, `deleted_entry_metadata_only`, `recovery_content_unavailable`, `recovery_partial`, `recovery_not_attempted`, and `carving_deferred`.
- S3-T05 stayed documentation/planning-only and did not add recovery APIs, fake deleted entries, fake recoverable deleted bytes, pytsk3 parsing, real EWF parsing, real partition parsing, real filesystem parsing, carving, unallocated-space scanning, UI, reporting, Stage 4 hash/signature analysis, or native dependency requirements.

Tests:

- `python -m pytest`: 99 passed in 6.72s.

Residual notes:

- Deleted-file recovery remains unsupported/deferred until a future real adapter exposes deleted entries and recoverable bytes.
- S3-T06 is the next Stage 3 gate and should be limited to final documentation/review handoff.

## 2026-07-13 - S3-T05 Deleted-File Recovery Plan Handoff

Result: ready for implementation agent.

Guardrails:

- S3-T05 is documentation/planning-only with the current codebase.
- Current `StubFilesystemAdapter` entries are allocated and not deleted; current providers supply synthetic bytes only for explicitly registered ids.
- `Pytsk3FilesystemAdapter` is dependency/status scaffolding and does not parse real filesystems, deleted entries, or file content.
- Do not implement recovery APIs, fake deleted entries, fake recoverable deleted bytes, carving, unallocated-space scanning, real parser work, UI, or native dependency requirements.
- Docs should clearly distinguish active allocated file export, deleted entry metadata, deleted-file recovery, carving/unallocated-space recovery, and unsupported/unrecoverable entries.
- Future recovery requirements should preserve provenance, read-only source handling, explicit content-source identity, completeness/confidence, and warnings for overwritten/sparse/unavailable ranges.

Expected verification:

- Update documentation/status files only unless a reviewed real adapter unexpectedly exists.
- Run `python -m pytest`.

Handoff prep verification:

- `python -m pytest`: 99 passed in 3.70s.

## 2026-07-13 - S3-T04 Review

Result: approved for commit.

Findings:

- No blocking issues found.
- `app.backend.api.ExportAuditContext` provides explicit opt-in audit context with database connection, case id, optional evidence id, optional actor, and `audit_failed_exports`.
- `export_file()` and `export_file_to_json()` accept audit context while standalone exports continue to work without case-store writes.
- Successful audited exports create one `audit_events` row using `action="file_export"` and existing `insert_audit_event()`.
- Audit details JSON records export status, source provenance, audit context ids, destination/output/manifest paths, byte counts, SHA-256/hash status, destination status, content-source identity, and warnings.
- Failed exports are not audited by default; when `audit_failed_exports=True`, details preserve the non-ok status and hash/byte placeholders.
- Source provenance case/evidence ids alone do not trigger database writes.
- S3-T04 uses the existing case-store schema and does not add automatic case/evidence creation, automatic persistence for other API calls, deleted recovery, UI, reporting, real parser work, or Stage 4 hash/signature analysis.

Tests:

- `python -m pytest`: 99 passed in 3.19s.

Residual notes:

- Audit persistence errors are documented as surfacing to the caller rather than being hidden as success.
- S3-T05 remains the next Stage 3 gate and should stay planning/research-focused unless real adapter support exists.

## 2026-07-13 - S3-T03 Review

Result: approved for commit.

Findings:

- No blocking issues found.
- `app/backend/api/file_export.py` now verifies successful output writes by reopening the exported artifact, streaming bytes through SHA-256, and counting bytes from disk.
- Returned `ExportResult` and persisted manifest JSON agree on `bytes_requested`, `bytes_written`, `hashes.sha256`, `hashes.status`, final status, and warnings.
- Structured post-write verification failures cover `byte_count_mismatch` and `export_verification_failed`; missing/unreadable output uses hash status `hash_failed`.
- Existing S3-T02 destination safety, exclusive create writes, overwrite refusal, and generic write-failure cleanup behavior remain in place.
- S3-T03 stayed in scope and did not add MD5/SHA-1 production hashing, known-file matching, file signatures, extension mismatch checks, image verification, audit integration, deleted recovery, UI, real parser work, native dependency requirements, or preview-rendered export bytes.

Tests:

- `python -m pytest`: 93 passed in 4.04s.

Residual notes:

- S3-T04 is the next Stage 3 implementation gate and should remain optional/explicit case-store audit integration only.
- Broader hash/signature analysis remains Stage 4.

## 2026-07-13 - S3-T02 Fixture/Stub Export Service Handoff

Result: ready for research/review agent review.

Implemented:

- `app/backend/api/file_export.py` defines a separate raw export content provider protocol, `StubExportContentProvider`, `export_file()`, and `export_file_to_json()`.
- Successful exports require an explicit output directory, use provider-owned raw bytes, write the output file, write a sibling JSON manifest from the S3-T01 result/manifest shape, and return `ExportResult`.
- Destination safety checks run before writing and reject overlap with known source/evidence paths.
- Structured statuses cover `ok`, `path_not_file`, `content_source_unavailable`, `destination_not_selected`, `unsafe_destination`, `invalid_output_name`, `output_exists`, and `export_write_failed`.
- Tests cover successful stub export, manifest JSON, byte equality, result/manifest agreement, missing content, directory entries, missing destination, unsafe destination, traversal/invalid output names, existing output refusal, and provider data non-mutation.

Tests:

- `python -m pytest`: 83 passed.

Scope intentionally not implemented:

- No SHA-256/hash computation; hashes remain `hash_not_computed`.
- No audit integration.
- No deleted-file recovery.
- No UI, search, reporting, real EWF parsing, real partition parsing, real filesystem parsing, required native dependencies, commit, or push.
- No preview-rendered text/hex used as export bytes.

## 2026-07-13 - S3-T02 Review

Result: changes requested.

Findings:

- [P2] `app/backend/api/file_export.py`: `export_file()` checks for existing output/manifest paths, then writes with overwrite-capable `Path.write_bytes()` and `Path.write_text()`. A file appearing between the preflight check and write would be overwritten despite the `output_exists` policy. Use exclusive creation for both output and manifest writes, such as `open("xb")`/`open("x", encoding="utf-8")`, and map `FileExistsError` to structured `output_exists`. Add a regression test that proves an existing output/manifest cannot be overwritten by the write path.
- [P2] `app/backend/api/file_export.py`: if the output file write succeeds and the manifest write fails, `export_file()` returns `export_write_failed` but leaves the exported file behind without a manifest. A failed export should not leave an unmanifested artifact unless the result/warnings explicitly document a partial artifact and the design chooses to retain it. Prefer best-effort cleanup of the just-written output file on manifest-write failure, with a test that simulates manifest-write failure.
- [P2] `app/backend/api/file_export.py`: `ExportRequest.requested_output_path` is captured early but ignored on the success path; the service writes `source.file_name` unless `output_name` is passed. This means an `ExportRequest` asking for `custom.txt` silently writes `hello.txt`, and an unsafe requested path is not validated. Support a safe request-level output name or reject unsupported/unsafe requested paths with `invalid_output_name`; add tests for both safe and traversal-style `ExportRequest.requested_output_path` values.

Tests:

- `python -m pytest`: 83 passed.

Verified good behavior:

- Export content comes from an explicit export provider separate from preview providers.
- The default stub export provider returns raw synthetic bytes and manifests label the content source as stub/synthetic.
- Destination/source overlap, missing destination, non-file entries, missing content, invalid names, and existing outputs are structured in normal preflight paths.
- Result and manifest preserve S3-T01 provenance and keep hashes at `hash_not_computed`.
- S3-T02 did not add SHA-256 computation, audit integration, deleted recovery, UI, real parser work, or native dependency requirements.

Required fix:

- Make overwrite refusal atomic at write time.
- Prevent failed manifest writes from leaving silent unmanifested export artifacts, or explicitly model and test partial-artifact retention if that is the chosen behavior.
- Honor or reject `ExportRequest.requested_output_path` predictably.
- Rerun `python -m pytest`.

## 2026-07-13 - S3-T02 Re-Review

Result: changes requested.

Findings:

- [P2] `app/backend/api/file_export.py`: the write-failure cleanup still misses partial files created by a generic `OSError` inside the exclusive write helpers. `output_created` is set only after `_write_bytes_exclusive()` returns, so if the output helper creates the file and then raises, the `except OSError` path will not clean up the partial output. Likewise, if `_write_text_exclusive()` creates a manifest and then raises, the code cleans up the output but not the partial manifest. For an export workflow, failed writes should not leave silent partial artifacts. In the generic `OSError` path, do best-effort cleanup of both the output path and manifest path, while keeping `FileExistsError` separate so pre-existing files are not removed.

Tests:

- `python -m pytest`: 88 passed.

Verified fixes:

- Output and manifest writes now use exclusive create helpers.
- Write-time `FileExistsError` maps to structured `output_exists`.
- The manifest `FileExistsError` path cleans up the just-written output.
- Safe `ExportRequest.requested_output_path` values are honored, and traversal/path components are rejected with `invalid_output_name`.
- S3-T02 still keeps SHA-256, audit integration, deleted recovery, UI, parser work, and preview-rendered export bytes out of scope.

Required fix:

- In the generic `OSError` branch, best-effort cleanup both output and manifest paths.
- Add regression tests where `_write_bytes_exclusive()` creates a partial output then raises `OSError`, and `_write_text_exclusive()` creates a partial manifest then raises `OSError`.
- Rerun `python -m pytest`.

## 2026-07-13 - S3-T02 Second Re-Review

Result: approved for commit.

Findings:

- No blocking issues found.
- The previous partial-artifact cleanup finding is fixed. Generic `OSError` write failures now best-effort clean up both output and manifest paths.
- `FileExistsError` remains separate, preserving the policy that pre-existing files are reported as `output_exists` and not removed.
- Regression coverage now simulates partial output creation followed by `OSError` and partial manifest creation followed by `OSError`; both paths return structured `export_write_failed` and leave no partial artifact behind.
- Earlier fixes remain in place: exclusive write helpers, write-time `output_exists`, safe `ExportRequest.requested_output_path` support, traversal rejection, and manifest-write failure cleanup.
- S3-T02 stayed in scope and did not add SHA-256 computation, audit integration, deleted recovery, UI, real parser work, native dependency requirements, or preview-rendered export bytes.

Tests:

- `python -m pytest`: 90 passed.

Residual notes:

- S3-T03 should build directly on this accepted write path and add SHA-256 plus byte-count verification only.

## S3-T02 Review Expectations

- Export must use an explicit export content provider/source, separate from preview providers.
- Export must not use rendered preview text/hex as output bytes.
- Destination safety checks must run before writing output or manifest files.
- Source/evidence paths must not be modified.
- Successful S3-T02 exports should write only the expected exported file and manifest JSON under an explicit output directory.
- Result and manifest should preserve S3-T01 provenance and content-source identity.
- SHA-256 must remain `hash_not_computed`; S3-T03 owns hashing.
- S3-T02 should not add audit integration, deleted recovery, UI, real parsers, required native dependencies, or Stage 4 hash/signature scope.

## 2026-07-13 - S3-T01 Export Manifest Contract Handoff

Result: ready for research/review agent review.

Implemented:

- `app/backend/forensic_core/export_manifest.py` defines Stage 3 export contract structures for request, result, manifest, status, warning, source provenance, content-source identity, and hash placeholders.
- Export source provenance preserves Stage 2-style fields including source path, volume id/offset/length, file id/path/name, filesystem type, adapter name, read-only assertion, allocation/deleted state, optional case/evidence ids, and timestamps.
- Content-source identity explicitly records provider name, source kind, read-only assertion, synthetic flag, content size, parser fields, and source status.
- Result/manifest structures include nullable destination/output/manifest paths, nullable byte counts, SHA-256 placeholder fields, destination safety status, UTC timestamps, warnings, and stable JSON serialization helpers.
- Tests cover serialization, JSON dumping, provenance, synthetic content-source labeling, placeholder hash/byte-count fields, warning serialization, non-ok statuses, and UTC timestamp format.

Tests:

- `python -m pytest`: 73 passed.

Scope intentionally not implemented:

- No file export or manifest file writing.
- No hash computation.
- No destination-overlap or source-path safety enforcement beyond placeholder/status fields.
- No case-store audit integration.
- No deleted-file recovery.
- No preview-rendered text/hex used as export bytes.
- No UI, search, reporting, real EWF parsing, real partition parsing, real filesystem parsing, native dependency requirement, commit, or push.

## 2026-07-13 - S3-T01 Review

Result: changes requested.

Findings:

- [P2] `app/backend/forensic_core/export_manifest.py`: `ExportResult.source_read_only` and `ExportManifest.source_read_only` default to `True` independently of `ExportSourceProvenance.read_only`. A caller can construct a result/manifest from a non-read-only source and accidentally serialize `"source_read_only": true` by omission. Because read-only source handling is a forensic integrity assertion, the contract should derive this field from `source.read_only` or default it to a non-assertive value instead of optimistic `True`. Add regression coverage for a source entry with `read_only=False`.

Tests:

- `python -m pytest`: 73 passed.

Verified good behavior:

- S3-T01 stayed contract-only and did not write files or manifests.
- Export content source identity is explicit and distinct from preview rendering.
- Result/manifest structures preserve Stage 2 source provenance and JSON serialization.
- Hash, byte-count, output path, manifest path, and destination-safety fields remain placeholders.
- No audit integration, deleted recovery, UI, real parser work, native dependency requirement, or S3-T02 work was introduced.

Required fix:

- Make `source_read_only` impossible to overstate by default. Prefer deriving the serialized value from `source.read_only` in both result and manifest shapes.
- Add a test proving a non-read-only source serializes as `source_read_only: false`.
- Rerun `python -m pytest`.

## 2026-07-13 - S3-T01 Re-Review

Result: approved for commit.

Findings:

- No blocking issues found.
- The previous read-only assertion finding is fixed. `ExportResult` and `ExportManifest` now serialize `source_read_only` from `source.read_only` when no explicit override is supplied.
- Regression coverage verifies that a source entry with `read_only=False` serializes `source.read_only` and `source_read_only` as false in both result and manifest shapes.
- S3-T01 remains contract-only and did not add file export, manifest writing, hash computation, destination safety enforcement, audit integration, deleted recovery, UI, or parser work.

Tests:

- `python -m pytest`: 74 passed.

Residual notes:

- S3-T02 should build on this contract by adding a separate export content provider/source and destination safety checks before any write.

## 2026-07-13 - Stage 3 Ticket Readiness Review

Result: S3-T01 ready for implementation handoff; later Stage 3 tickets remain Draft.

Findings:

- No code issues reviewed in this pass; this was onboarding/ticketing review only.
- The Stage 3 ticket files existed but were too high-level compared with the Stage 2 ticket prompts.
- Leaving the tickets marked `Ready` risked sending the implementation agent into export work without enough contract detail, status names, test expectations, or scope boundaries.
- The Stage 3 tickets are now marked `Draft` until each ticket is expanded.
- A Stage 3 VS Code familiarization prompt was added at `prompts/vscode-agent/2026-07-13-stage-3-familiarization.md`.
- Follow-up update: S3-T01 is now expanded and marked `Ready`, with a paste-ready implementation prompt at `prompts/vscode-agent/2026-07-13-s3-t01-export-manifest-contract.md`.
- S3-T02 through S3-T06 are expanded as detailed stage plans, but remain `Draft` pending review after each preceding ticket.

Recommended next action:

- Hand S3-T01 to the coding agent using the dedicated prompt.
- S3-T01 should define export request/result/manifest/status/warning/content-source structures and serialization tests.
- S3-T01 should not write files, compute real hashes, add audit events, implement deleted recovery, add UI, add real parsers, or require native dependencies.

Review stance for Stage 3:

- Export bytes must come from an explicit content-source/provider boundary.
- Preview-rendered text/hex must not be used as export bytes.
- Stage 2 filesystem metadata entries must not be treated as byte-bearing objects.
- Destination safety checks must be centralized and heavily tested once file writing begins.
- Manifests must identify whether bytes are stubbed, generated fixture bytes, provider-backed, or later real parser bytes.

## S2-T07 Review Expectations

- Documentation should accurately describe completed Stage 2 behavior and test commands.
- Docs should clearly separate real behavior from stubbed/synthetic/provider-backed behavior.
- Docs should not claim real EWF byte parsing, real partition parsing, real filesystem parsing, UI work, export/recovery, hashing, search, or reporting.
- `Goal.md`, `readme.md`, `plan.md`, `functionality.md`, `progression.md`, `tickets/stage-2/`, and backend docs should agree on Stage 2 status.
- S2-T07 should not add new app behavior or begin Stage 3.

## 2026-07-09 - Stage 2 Final Review Handoff

Result: ready for final Stage 2 review.

Implemented in Stage 2:

- Fixture/dependency strategy for pure stubs, tiny generated files, and optional local-only forensic fixtures.
- Read-only `LocalFileImageStream` for tiny local files and bounded byte reads.
- Whole-image volume discovery boundary.
- Filesystem adapter boundary with deterministic stub entries and dependency-safe `pytsk3` skeleton behavior.
- Backend directory listing/file metadata callable over adapter entries.
- Bounded raw/text/hex preview callable over explicit provider bytes.
- Documentation updates that separate real local-file behavior, stubbed filesystem/listing behavior, and synthetic preview-provider content.

Final review checklist:

- Confirm docs do not claim real EWF byte parsing, real image verification, real partition parsing, real filesystem parsing, or real file extraction.
- Confirm `pyewf`, libewf, `pytsk3`, and The Sleuth Kit remain optional for default tests.
- Confirm Stage 2 API results are not described as automatically persisted to the case store.
- Confirm no export/recovery, hashing/signature analysis, search/timeline, reporting, UI, executable packaging, S2-T08, or Stage 3 work was introduced.
- Confirm manual-test fields remain `Untested` until the user explicitly reports manual testing.

Tests:

- `python -m pytest`: 67 passed.

## 2026-07-09 - Stage 2 Final Review

Result: Stage 2 approved for commit.

Findings:

- No blocking issues found.
- Documentation accurately describes Stage 2 as a backend browsing/preview foundation using real local-file byte-stream behavior, stubbed volume/filesystem/listing behavior, and synthetic preview-provider bytes.
- Docs clearly state that real EWF byte parsing, image verification, partition parsing, filesystem parsing, real file extraction, UI, export/recovery, hashing/signatures, search/timeline, reporting, executable packaging, and automatic Stage 2 result persistence are not implemented.
- Dependency notes keep `pyewf`, libewf, `pytsk3`, and The Sleuth Kit optional for default tests.
- Manual-test fields remain `Untested`, as expected.
- S2-T07 stayed docs/status-only and did not begin Stage 3.

Tests:

- `python -m pytest`: 67 passed.

Residual notes:

- `tickets/README.md` had one stale Stage 2 status line saying "planned next"; this review corrected it to Stage 2 complete at handoff and Stage 3 planned next.

## S2-T06 Review Expectations

- Preview code should use bounded, read-only reads from a stub or tiny generated preview source.
- Preview results should be JSON-friendly and preserve source, volume, file id/path, offset, requested length, returned length, mode, truncation, status, and warnings.
- Text preview should handle decoding errors visibly and safely; hex preview should be deterministic.
- Missing files, directories, invalid ranges, unsupported modes, and size-limit truncation should return structured statuses or warnings.
- S2-T06 should not add export/recovery, hashing, UI work, real filesystem parsing, required native dependencies, persistence, or real evidence fixtures.

## 2026-07-09 - S2-T06 Review

Result: changes requested.

Findings:

- [P2] `app/backend/api/file_preview.py`: `preview_file()` reports `status.code == "ok"` when `offset` is beyond the available preview content and `length` is omitted. Example: `/hello.txt` has 13 stub bytes, but `preview_file(entry, mode="text", offset=99)` returns `ok`, zero bytes, empty text, and no truncation warning. A preview offset outside the content should be a structured non-ok status or warning, such as `preview_truncated`, `content_unavailable`, or a dedicated range status. This matters because a forensic preview boundary should not quietly report success for a range that cannot exist.

Tests:

- `python -m pytest`: 66 passed.

Verified good behavior:

- Text, hex, and raw preview outputs are JSON-friendly.
- Stub preview content is clearly labeled as synthetic, not parsed evidence.
- Negative offset/length, unsupported mode, directory entry, missing content, max-length truncation, content-size truncation with an explicit length, decode replacement, and provenance/read-only fields are covered.
- S2-T06 stayed in scope and did not add export/recovery, hashing, UI, persistence, native dependency requirements, real parsing, S2-T07, or Stage 3 work.

Required fix:

- Add a regression test for `offset > source_content_size` with omitted `length`.
- Return a structured non-ok status/warning for that case.
- Keep the change inside S2-T06 and rerun `python -m pytest`.

## 2026-07-09 - S2-T06 Review Fix Handoff

Result: ready for re-review.

Implemented:

- `preview_file()` now returns structured `content_unavailable` status when the requested offset is beyond provider content size.
- Added regression coverage for `offset > source_content_size` with omitted `length`, preserving provenance, read-only fields, zero returned bytes, and JSON-friendly shape.

Tests:

- `python -m pytest`: 67 passed.

Scope intentionally not implemented:

- No S2-T07 or Stage 3 work.
- No export/recovery, hashing, UI, persistence, native dependency requirement, real filesystem parsing, or real evidence fixture.

## 2026-07-09 - S2-T06 Re-Review

Result: approved for commit.

Findings:

- No blocking issues found.
- The previous offset-boundary finding is fixed: `preview_file(..., offset=99)` for the 13-byte stub file now returns structured `content_unavailable` instead of `ok`.
- Regression coverage verifies non-ok status, zero returned bytes, no preview payload, preserved source size, read-only provenance, and a `content_unavailable` warning.
- Existing text, hex, raw serialization, truncation, missing content, directory/non-file, unsupported mode, invalid range, decode replacement, and provenance tests still pass.
- S2-T06 stayed in scope and did not add S2-T07, Stage 3, export/recovery, hashing, UI, persistence, native dependencies, real filesystem parsing, or real evidence fixtures.

Tests:

- `python -m pytest`: 67 passed.

## 2026-07-09 - S2-T06 Preview Foundation Handoff

Result: ready for research/review agent review.

Implemented:

- `preview_file()` backend API callable for provider-backed raw/text/hex previews.
- `preview_file_to_json()` serialization helper.
- `StubPreviewProvider` with synthetic bytes for `stub-file-hello` (`/hello.txt`).
- JSON-friendly preview result shape with source path, volume id/offset/length, file id/path/name/type, requested offset/length, returned bytes, source content size, truncation flag, read-only assertion, provider details, mode, status, preview data, and warnings.
- Tests for text, hex, raw JSON serialization, bounded offset/length, max-length truncation, content-size truncation, missing content, directory entry rejection, unsupported mode, invalid ranges, decode replacement warning, and provenance/read-only fields.

Scope intentionally not implemented:

- No real filesystem byte extraction.
- No real EWF, partition, or filesystem parsing.
- No export/recovery or hashing.
- No UI, persistence, background jobs, or case-store writes.
- No required native dependency or real evidence fixture.

Suggested review command:

```powershell
python -m pytest
```

## S2-T05 Review Expectations

- Directory listing view should consume the filesystem adapter boundary instead of parsing real filesystems directly.
- Root listing should return deterministic JSON-friendly entries from the stub adapter.
- Unsupported, missing, file, or nested paths should return structured status/warning results unless explicitly supported.
- Adapter dependency-unavailable or real-parser-not-implemented states should be visible in the listing response.
- S2-T05 should not add raw/text/hex preview, export/recovery, hashing, UI work, real filesystem parsing, or required native dependencies.

## 2026-07-09 - S2-T05 Review

Result: approved for commit.

Findings:

- No blocking issues found.
- `list_directory()` consumes `FilesystemAdapter.inspect_volume()` and returns a JSON-friendly directory listing response without parsing real filesystems directly.
- Stub root listing returns deterministic `/Documents` and `/hello.txt` metadata entries with source, volume, adapter, filesystem, status, timestamp, allocation/deleted, and read-only provenance preserved.
- Unsupported nested paths, file paths, unknown paths, dependency-unavailable adapters, importable-but-not-implemented pytsk3, and defensive adapter exceptions are represented as structured statuses.
- Tests do not require `pytsk3`, The Sleuth Kit, real filesystems, real evidence, private fixtures, or network access.
- S2-T05 stayed in scope and did not add file-content preview, export/recovery, hashing, UI work, persistence, case-store writes, real filesystem parsing, or required native dependencies.

Tests:

- `python -m pytest`: 53 passed.

Residual notes:

- The default adapter path is dependency-safe but normally returns `filesystem_unavailable` until real pytsk3 parsing exists. For current smoke/manual checks, callers should pass `StubFilesystemAdapter`.

## 2026-07-09 - S2-T05 Directory Listing Handoff

Result: ready for research/review agent review.

Implemented:

- `list_directory()` backend API callable over `FilesystemAdapter.inspect_volume()`.
- `directory_listing_to_json()` serialization helper.
- Root listing for `StubFilesystemAdapter` returning `/Documents` and `/hello.txt`.
- Structured statuses for `ok`, `path_not_found`, `path_not_directory`, `path_unsupported`, `filesystem_unavailable`, and defensive `filesystem_error`.
- Tests for root listing, JSON shape, provenance/read-only fields, unsupported nested path, file path, unknown path, path normalization, and pytsk3 dependency-unavailable/not-implemented states.

Scope intentionally not implemented:

- No file-content reads or raw/text/hex preview.
- No export/recovery or hashing.
- No UI, persistence, background jobs, or case-store writes.
- No real filesystem parsing or required native dependency.
- No real evidence or filesystem images.

Suggested review command:

```powershell
python -m pytest
```

## S2-T04 Review Expectations

- Filesystem adapter boundary should expose stable result/status/entry shapes.
- Tests must pass without `pytsk3`, The Sleuth Kit, real filesystems, or evidence images.
- Stub adapter should provide deterministic entries for later directory listing work.
- Dependency-unavailable behavior should be structured, not an import crash.
- S2-T04 should not add directory-listing CLI/workflow, preview rendering, export/recovery, or required native dependencies.

## 2026-07-09 - S2-T04 Review

Result: approved for commit.

Findings:

- No blocking issues found.
- `filesystem_adapter.py` defines stable JSON-friendly adapter, dependency, result, status, warning, and entry shapes.
- `StubFilesystemAdapter` returns deterministic root entries for `/Documents` and `/hello.txt`.
- `Pytsk3FilesystemAdapter` reports `dependency_unavailable` when `pytsk3` is missing and `real_parser_not_implemented` when a pytsk3 module is importable but real parsing is still deferred.
- Tests do not require `pytsk3`, The Sleuth Kit, real filesystems, real evidence, or private fixtures.
- S2-T04 stayed in scope and did not add directory-listing workflow, preview rendering, export/recovery, hashing, UI work, or required native dependencies.

Tests:

- `python -m pytest`: 44 passed.

Residual notes:

- Stub entry `/hello.txt` is metadata-only for now. S2-T05/S2-T06 should not assume file content exists until a listing/preview content boundary is explicitly added.

## 2026-07-09 - S2-T04 Filesystem Adapter Handoff

Result: ready for research/review agent review.

Implemented:

- `FilesystemAdapter` protocol and JSON-friendly result/status/warning/dependency/entry structures.
- `StubFilesystemAdapter` with deterministic root entries for `/Documents` and `/hello.txt`.
- `Pytsk3FilesystemAdapter` skeleton that reports `dependency_unavailable` when `pytsk3` is missing and `real_parser_not_implemented` when injected/importable but still deferred.
- Entry provenance fields for source path, volume id, volume offset/length, filesystem type, adapter name, read-only assertion, allocation/deleted state, timestamps, status, and warnings.
- Tests for stub metadata/result shape, root entries, read-only provenance, pytsk3 dependency-unavailable behavior, JSON serialization, and importable-but-unimplemented pytsk3 status.

Scope intentionally not implemented:

- No directory-listing CLI/workflow.
- No real filesystem parsing.
- No preview rendering.
- No export/recovery, hashing, or native dependency requirement.
- No real evidence or filesystem images.

Suggested review command:

```powershell
python -m pytest
```

## S2-T03 Review Expectations

- Volume discovery should produce structured JSON-friendly results with provenance.
- Whole-image/single-volume behavior is acceptable for S2-T03.
- Missing, unreadable, or zero-byte sources should be handled predictably.
- S2-T03 should not introduce filesystem parsing, pytsk3/TSK requirements, preview rendering, export/recovery, or real evidence fixtures.

## 2026-07-09 - S2-T03 Review

Result: approved for commit.

Findings:

- No blocking issues found.
- `discover_volumes()` defines a JSON-friendly volume discovery boundary over `ImageByteStream`.
- Whole-image/single-volume behavior works for readable non-empty streams.
- Missing/unavailable streams, zero-byte sources, and unsupported partition strategies return structured statuses and warnings.
- Tests use tiny generated files and do not require real evidence or native forensic dependencies.
- S2-T03 stayed in scope and did not add filesystem parsing, preview rendering, export/recovery, hashing, UI work, or real partition parsing.

Tests:

- `python -m pytest`: 38 passed.

Residual notes:

- Volume id is currently the stable placeholder `volume-0` for whole-image strategy. Future real partition parsing should define deterministic ids from source/evidence id plus partition metadata.

## 2026-07-09 - S2-T03 Volume Discovery Handoff

Result: ready for research/review agent review.

Implemented:

- `discover_volumes()` volume discovery boundary over `ImageByteStream`.
- Whole-image/single-volume behavior for readable non-empty streams.
- Structured statuses for successful discovery, unavailable image stream, zero-byte image, and unsupported partition parsing strategies.
- JSON-friendly result objects with source path, stream type, source size, read-only assertion, volume id/index, offset, length, type, description, status, and warnings.
- Generated-file tests for non-empty local source, zero-byte source, missing source, serialization shape, read-only provenance, and unsupported partition strategy.

Scope intentionally not implemented:

- No real partition table parsing.
- No filesystem adapter or directory listing.
- No preview rendering.
- No export/recovery, hashing, or native forensic dependencies.
- No real evidence or binary forensic fixtures.

Suggested review command:

```powershell
python -m pytest
```

## S2-T02 Review Expectations

- Byte stream implementation must be read-only and bounded by offset/length.
- Tests should use tiny generated files under ignored paths, not evidence images.
- Missing paths, directories, and invalid ranges should return structured errors or documented exceptions.
- S2-T02 should not introduce volume parsing, filesystem parsing, preview rendering, export/recovery, or native forensic dependencies.

## 2026-07-09 - S2-T02 Review

Result: approved for commit.

Findings:

- No blocking issues found.
- `LocalFileImageStream` provides read-only local file metadata and bounded `read_at(offset, length)` behavior.
- Structured statuses cover missing paths, directories, unreadable/non-regular files, invalid ranges, reads beyond EOF, and successful reads.
- Tests use tiny generated files under ignored workspace paths and do not require real evidence or native forensic dependencies.
- S2-T02 stayed in scope and did not add volume discovery, filesystem parsing, preview rendering, export/recovery, hashing, or UI work.

Tests:

- `python -m pytest`: 32 passed.

Residual notes:

- Offset exactly at EOF with a nonzero length currently returns status `ok` with zero bytes and a `read_truncated_at_eof` warning. This is acceptable for now; later preview/volume callers should treat `bytes_read` and warnings as authoritative.

## 2026-07-09 - S2-T02 Image Byte-Stream Handoff

Result: ready for research/review agent review.

Implemented:

- `LocalFileImageStream` read-only local file-backed stream.
- Structured stream metadata, read result, status, and warning objects.
- Bounded `read_at(offset, length)` reads with source path, stream type, size, read-only assertion, status, and warning provenance.
- Generated-file tests for metadata, normal ranges, offset zero, EOF truncation, read beyond EOF, missing paths, directory paths, negative offset/length, and zero-length reads.

Scope intentionally not implemented:

- No volume discovery.
- No filesystem adapter.
- No directory listing.
- No raw/text/hex preview renderer.
- No export/recovery, hashing, or native forensic dependencies.

Suggested review command:

```powershell
python -m pytest
```

## S2-T01 Review Expectations

- Confirm `app/fixtures/README.md` defines a clear Stage 2 fixture strategy.
- Confirm default Stage 2 tests remain free of private evidence, large images, `pyewf`, libewf, `pytsk3`, and The Sleuth Kit.
- Confirm optional real raw/EWF/TSK fixtures are documented as local-only and opt-in.
- Confirm S2-T01 does not add byte-stream, volume-discovery, filesystem-adapter, preview, export, hash, or UI implementation.
- Confirm missing native dependencies are expected to become structured status results, not raw crashes or default test blockers.

## 2026-07-09 - S2-T01 Review

Result: approved for commit.

Findings:

- No blocking issues found.
- Stage 2 fixture tiers are clear: pure stubs, tiny generated files, and optional local-only forensic fixtures.
- Default tests remain free of private evidence, large images, `pyewf`, libewf, `pytsk3`, and The Sleuth Kit.
- Optional real raw/EWF/TSK fixtures are documented as local-only and opt-in.
- S2-T01 stayed documentation-only and did not add byte-stream, volume, filesystem, preview, export, hash, or UI implementation.

Tests:

- `python -m pytest`: 22 passed.

Residual notes:

- S2-T02 should use this strategy to define read-only byte-stream tests around tiny generated files and structured missing/unreadable path behavior.

## 2026-07-09 - S2-T01 Fixture/Dependency Strategy Handoff

Result: ready for research/review agent review.

Implemented documentation:

- Stage 2 fixture tiers: pure stubs, tiny generated files, and optional local-only forensic fixtures.
- Guidance for S2-T02 through S2-T06 on which tests should use stubs versus generated bytes.
- Later real-fixture rules for legal training images, regeneration notes, expected hashes/sizes, and opt-in integration tests.
- Stage 2 dependency policy making `pytsk3`, The Sleuth Kit, `pyewf`, and libewf optional for default tests.

Scope intentionally not implemented:

- No image/byte-stream abstraction.
- No volume discovery.
- No filesystem adapter.
- No pytsk3 dependency addition.
- No real evidence or binary fixtures.

Suggested review command:

```powershell
python -m pytest
```

## S1-T06 Review Expectations

- Docs should accurately describe current Stage 1 behavior and limitations.
- Test commands should be current and runnable.
- The handoff should not claim real EWF parsing, filesystem parsing, UI, or automatic persistence.
- The final Stage 1 review section should make it clear what is ready for Stage 2 planning.

## 2026-07-09 - Stage 1 Final Review

Result: Stage 1 complete at the planning/review level.

Verified Stage 1 scope:

- Backend skeleton exists and imports.
- E01 segment discovery is implemented and tested without real evidence.
- EWF reader adapter boundary is implemented with stub and pyewf-unavailable behavior.
- Intake JSON callable/CLI exists and handles invalid input/dependency states.
- SQLite case-store schema exists for cases, evidence sources, audit events, and schema migration marker.
- Documentation clearly states that real EWF byte parsing, filesystem parsing, UI, and automatic intake persistence are not implemented yet.

Stage 2 readiness:

- Stage 2 tickets exist under `tickets/stage-2/`.
- Stage 2 should begin with fixture/dependency strategy before implementing byte streams or filesystem adapters.
- Review should continue enforcing read-only source handling, structured unsupported-dependency behavior, and no private evidence in tests.

Stage 3 readiness:

- Stage 3 tickets exist under `tickets/stage-3/`.
- Stage 3 should not begin until Stage 2 provides a stable file/metadata source.

## 2026-07-09 - Stage 1 Final Review Handoff

Result: ready for research/review agent final Stage 1 review.

Implemented capabilities to verify:

- Backend Python package skeleton and pytest configuration.
- E01 segment discovery with ordered segments and structured warnings.
- EWF reader adapter boundary with stub metadata, verification status shape, and pyewf dependency-unavailable behavior.
- Intake JSON command/callable through `python -m app.backend.api.intake path\to\sample.E01`.
- SQLite schema/helpers for `cases`, `evidence_sources`, `audit_events`, and `schema_migrations`.

Current limitations to keep visible:

- No real EWF byte parsing or real image verification yet.
- No partition/filesystem parsing yet.
- No UI yet.
- No automatic persistence from intake command to SQLite yet.
- `pyewf`/libewf is optional and not required for tests.
- No real forensic evidence is required for tests.

Review commands:

```powershell
python -m pytest
python -m app.backend.api.intake path\to\sample.E01 --adapter stub
```

Expected S1-T06 test result:

- `python -m pytest`: 22 passed.

Suggested final review checklist:

- Confirm documentation does not overclaim Stage 1 behavior.
- Confirm test and intake commands are accurate on Windows.
- Confirm no Stage 2 filesystem/UI work was introduced.
- Confirm `plan.md`, `progression.md`, ticket status, and backend docs agree.

## 2026-07-09 - S1-T05 Review

Result: approved for commit.

Findings:

- No blocking issues found.
- Schema includes `cases`, `evidence_sources`, `audit_events`, and `schema_migrations`.
- Evidence source rows preserve S1-T04 intake provenance through source paths, segment discovery JSON, adapter/dependency JSON, metadata JSON, verification JSON/status, warnings JSON, read-only assertion, and timestamps.
- Audit events link to cases and optionally evidence sources.
- Tests use in-memory SQLite and do not require real evidence or persistent user data.
- The implementation stayed in scope and did not wire automatic intake persistence, UI, filesystem parsing, or real EWF parsing.

Tests:

- `python -m pytest`: 22 passed.

Residual notes:

- Audit timestamps currently use second precision. This is acceptable for the Stage 1 foundation, but later audit-heavy workflows may want higher precision or an explicit monotonic sequence.

## S1-T05 Review Expectations

- Schema should include cases, evidence_sources, and audit_events.
- Evidence source records should preserve enough provenance for S1-T04 intake output.
- Tests should use in-memory or temporary SQLite databases, not persistent user data.
- The implementation should not broaden into UI, filesystem parsing, or automatic full case workflow.
- Audit events should be generic enough to record future actions without schema churn.

## 2026-07-09 - S1-T04 Re-Review

Result: approved for commit.

Findings:

- No blocking issues found.
- The previous status-contract issue is fixed: importable-but-unimplemented pyewf now returns `reader_not_implemented` instead of `ok`.
- Stub-backed intake still returns `ok`.
- Missing-pyewf intake still returns `metadata_unavailable`.
- The intake command remains scoped to S1-T04 and does not add SQLite, UI, filesystem parsing, or real EWF parsing.

Tests:

- `python -m pytest`: 18 passed.

Residual notes:

- The CLI currently returns nonzero only for `invalid_input`; future stages may decide whether `reader_not_implemented` or `metadata_unavailable` should also have nonzero CLI exit codes.

## 2026-07-09 - S1-T04 Review

Result: changes requested.

Findings:

- [P2] `app/backend/api/intake.py`: `run_e01_intake()` reports `status: "ok"` whenever `adapter_available` is true. If `PyewfEwfReaderAdapter` is importable but real metadata extraction is still deferred, it returns empty metadata plus `real_reader_not_implemented`, yet intake status is `"ok"`. That would mislead future users who install `pyewf` before real parsing is implemented.

Tests:

- `python -m pytest`: 17 passed.

Good notes:

- The intake layer correctly composes segment discovery and EWF adapter output.
- Invalid input returns structured JSON-style data rather than a traceback.
- CLI behavior for invalid input is tested.
- No SQLite, filesystem parsing, UI work, real evidence, or native dependency requirement was added.

## S1-T04 Review Expectations

- Intake command should compose segment discovery and reader adapter output without duplicating their logic.
- Output should be JSON-serializable and stable enough for future UI use.
- Tests must pass without real evidence or native forensic dependencies.
- Invalid input should not produce raw tracebacks for expected user mistakes.
- S1-T04 must not add case storage, filesystem parsing, or UI work.

## 2026-07-09 - S1-T03 Review

Result: approved for commit.

Findings:

- No blocking issues found.
- The adapter boundary is separate from segment discovery.
- The stub adapter returns predictable synthetic metadata and verification shape for tests.
- The pyewf adapter skeleton handles missing `pyewf` as structured dependency-unavailable data, not a raw import crash.
- Tests do not require real evidence, pyewf, or libewf.

Tests:

- `python -m pytest`: 12 passed.

Residual notes:

- Real pyewf metadata extraction is intentionally deferred beyond S1-T03.
- Result dataclasses contain normal dictionaries; this is acceptable for the current boundary, but later evidence-facing code should avoid mutating returned result objects in place.

## S1-T03 Review Expectations

- Adapter interface should be separate from segment discovery.
- Tests must pass without `pyewf`, libewf, or real E01 evidence.
- Stub adapter should return predictable metadata and verification status.
- Missing dependency behavior should be structured and visible, not a raw import crash.
- Real pyewf adapter code, if added, should be optional and read-only by design.

## 2026-07-09 - S1-T02 Re-Review

Result: approved for commit.

Findings:

- No blocking issues found.
- The previous `.E00` issue is fixed: `.E00` is treated as an unsupported sibling segment and is not included in discovered segments.
- Regression coverage was added for `.E00`.
- Segment discovery remains dependency-free and read-only; it only inspects path names and directory entries.

Tests:

- `python -m pytest`: 8 passed.

Residual notes:

- Old ignored scratch/cache folders from earlier temp-directory experiments may remain locally, but they do not affect tests or Git-tracked files.

## S1-T02 Review Expectations

- Segment discovery must use temporary dummy files or mocks, not real E01 evidence.
- The code should not parse EWF content yet; that belongs to S1-T03 and later.
- Results should be structured and stable enough for the later intake JSON command.
- Missing/gap behavior should be visible through warnings or a documented exception/result.
- Tests should cover valid chains, invalid input, and gaps.

## 2026-07-09 - S1-T02 Initial Review

Result: changes requested.

Findings:

- [P2] `app/backend/forensic_core/segment_discovery.py`: `_parse_segment_number()` accepts `.E00` as segment number `0`. When `sample.E00` sits next to `sample.E01`, discovery includes `.E00` in `segments`, emits no warning, and marks the set complete. Stage 1 discovery should treat `.E00` as unsupported/invalid because the selected evidence chain starts at `.E01`.

Tests:

- `python -m pytest`: 7 passed.

Good notes:

- The implementation stays dependency-free and does not parse evidence bytes.
- The result shape is clear and future JSON-friendly.
- Tests use dummy workspace-local files, not real evidence.
- The pytest temp/cache mitigation is working; the latest test run completed without warnings.

## 2026-07-09 - S1-T01/S1-T01A Review

Result: approved for commit.

Findings:

- No blocking issues found.
- The backend package skeleton is intentionally minimal and stays within S1-T01 scope.
- Smoke tests cover package import and backend subpackage import.
- `.gitignore` covers Python cache/test artifacts, virtual environments, and common build outputs.
- `python -m pytest` passed: 2 tests passed, 1 warning.

Residual notes:

- Pytest still reports a non-blocking cache warning under `.pytest_cache`; tests pass.
- No E01 logic is expected in S1-T01. Segment discovery should begin in S1-T02.
