# 2026-07-09 - S2-T05 Directory Listing And File Metadata Prompt

Use this prompt to hand S2-T05 to the Stage 2 VS Code implementation agent.

```text
Implement ticket S2-T05: Directory Listing And File Metadata View.

Before editing, read these files:
- prompts/vscode-agent/2026-07-09-stage-2-familiarization.md
- Goal.md
- progression.md
- tickets/stage-2/S2-T05-directory-listing-metadata.md
- tickets/stage-2/README.md
- app/backend/forensic_core/filesystem_adapter.py
- app/backend/forensic_core/volume_discovery.py
- app/backend/forensic_core/README.md
- app/backend/api/README.md
- app/backend/api/intake.py
- app/fixtures/README.md
- app/docs/environment-readiness.md
- functionality.md
- plan.md
- review.md
- workflow.md

Context:
- Stage 1 is complete.
- S2-T01 fixture/dependency strategy is complete.
- S2-T02 read-only image byte-stream abstraction is complete.
- S2-T03 volume discovery boundary is complete.
- S2-T04 filesystem adapter boundary is complete.
- Current focus is only S2-T05.
- S2-T05 should expose a backend directory listing/file metadata view over the existing filesystem adapter boundary.
- This is still a backend-first Stage 2 ticket, not a UI or executable-packaging ticket.
- S2-T06 is raw/text/hex preview foundation. Do not read or render file content in S2-T05.
- Do not add pytsk3 or The Sleuth Kit as required dependencies.
- Do not parse real filesystems as a default path.
- Do not add UI, export/recovery, hashing, or real evidence fixtures.
- Treat all source/evidence paths as read-only.
- Preserve provenance in every returned entry/result.
- Missing native dependencies and unsupported paths must be structured statuses, not raw tracebacks.
- Do not commit or push. Stop for review after this ticket.

Before implementing:
- Briefly summarize your understanding of S2-T05.
- List the files you expect to create or modify.
- If you see a scope conflict between the docs and this prompt, pause and explain it instead of broadening the ticket.

Your task:
- Add a small backend listing layer, preferably under app/backend/api/ if that fits the existing local command/API boundary.
- Provide a callable such as `list_directory(...)` or similarly named function that accepts:
  - a `VolumeInfo` or enough explicit test data to build one;
  - a directory path, defaulting to `/`;
  - a filesystem adapter, defaulting to a dependency-safe adapter if appropriate.
- The callable should inspect/list through `FilesystemAdapter.inspect_volume()` and return a JSON-serializable dict.
- Root listing with `StubFilesystemAdapter` should return deterministic entries for `/Documents` and `/hello.txt`.
- Include entry metadata from S2-T04: path, name, entry type, size, timestamps, allocated/deleted state, status/warnings, adapter name, filesystem type, source path, volume id, offset/length, and read-only assertion.
- Add structured status values for expected outcomes, for example:
  - `ok` for successful directory listing;
  - `path_not_found`, `path_not_directory`, or `path_unsupported` for unsupported/non-root paths;
  - `filesystem_unavailable` or similar when the adapter result is dependency-unavailable/not implemented.
- Include adapter/result warnings in the listing response.
- A tiny CLI is acceptable if it is simple and dependency-free, but the callable and tests are the priority.
- Prefer simple, explicit data structures that match the existing Stage 1/Stage 2 style.
- Keep the listing layer separate from `filesystem_adapter.py` unless a tiny adapter helper is clearly needed.
- Do not mutate adapter result objects in place.
- Do not introduce background jobs, persistence, or case-store writes in this ticket.
- Update app/backend/api/README.md and app/backend/forensic_core/README.md as needed.
- Update functionality.md for S2-T05 status and keep Manual Test as `Untested`.
- Update plan.md if the Stage 2 note needs to advance from S2-T04 to S2-T05.
- Update progression.md with what changed, what was learned, blockers if any, and the next step.
- Update review.md with a handoff section or review notes if useful.
- Set `tickets/stage-2/S2-T05-directory-listing-metadata.md` to `Review` when implementation is complete.
- Set S2-T05 to `Review` in `tickets/stage-2/README.md` when implementation is complete.
- Run `python -m pytest` and report the result.

Likely files to create or modify:
- app/backend/api/directory_listing.py or a similarly named API module
- app/backend/api/__init__.py if exports are needed
- app/tests/test_directory_listing.py or a similarly named test file
- app/backend/api/README.md
- app/backend/forensic_core/README.md
- functionality.md
- plan.md
- progression.md
- review.md
- tickets/stage-2/README.md
- tickets/stage-2/S2-T05-directory-listing-metadata.md

Tests to add:
- stub root listing returns `/Documents` and `/hello.txt`;
- listing response is JSON-serializable;
- entry provenance/read-only fields are preserved;
- unsupported nested path behavior is structured;
- file path such as `/hello.txt` is not treated as a directory unless explicitly supported;
- pytsk3 dependency-unavailable or importable-but-not-implemented adapter state is structured and not reported as successful listing.
- invalid or unusual directory path normalization is deterministic, for example empty path, `/`, and paths without a leading slash if supported;
- no real evidence, native dependency, private fixture, or network access is required.

Scope boundaries:
- Do not implement S2-T06 raw/text/hex preview.
- Do not return file bytes or decode file contents.
- Do not implement export/recovery or deleted-file recovery.
- Do not compute hashes.
- Do not add UI.
- Do not require pytsk3, The Sleuth Kit, pyewf, or libewf.
- Do not commit real evidence, raw disk images, E01 files, or filesystem images.

Deliverable:
- A dependency-safe backend directory listing/file metadata view that later S2-T06 preview work can consume.

Final handoff:
- Summarize files changed.
- Summarize behavior added.
- Report the exact pytest command and result.
- State any limitations or deferred work.
- Confirm you did not begin S2-T06.

Stop after S2-T05 and hand off for review. Do not commit, push, or begin S2-T06.
```
