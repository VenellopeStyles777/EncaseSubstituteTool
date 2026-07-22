# Environment Readiness Check

Purpose: record the local tool/environment state for backend-first development.

Last checked: 2026-07-14

## Summary

The repository, Git remote, and normal Python environment are ready for Stage 4 planning and dependency-free backend tests after Stage 3 review.

Earlier on 2026-07-09, `python` resolved only to the Microsoft Store app execution alias. That has since been fixed.

## Current Findings

Git:

- Status: installed.
- Version checked: `git version 2.55.0.windows.2`.
- Branch checked during S1-T06: `stage-1-e01-intake`.
- Upstream: stage branch workflow; merge to `main` is handled after review.
- Remote: `https://github.com/VenellopeStyles777/EncaseSubstituteTool.git`.
- Latest visible local commit during S1-T06: `2aeae90 Stage 1: SQLite case store schema`.

Python:

- Status: ready for Stage 4 planning and backend tests after Stage 3 review.
- `python --version`: Python 3.14.6.
- `python -m pip --version`: pip 26.1.2.
- `python -m pytest`: 99 passed in 4.42s during the final S3-T06 review.
- Pytest version observed: 9.1.1.
- Earlier warning: pytest could not create one cache path under `.pytest_cache`; tests still passed.
- Follow-up: project config now disables pytest's optional cache provider. Current S1-T06 test run completed without that warning.
- S1-T02 follow-up: pytest's default Windows temp path also produced permission issues for `tmp_path`/temporary-directory style tests. The project now configures pytest to use repo-local ignored path `.test-artifacts/pytest-temp` for temporary files and disables pytest's optional cache provider.

Codex bundled runtime:

- Python is available inside the Codex desktop runtime at:
  `C:\Users\cqi\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`
- Bundled Python version checked: `3.12.13`.
- Bundled SQLite checked: `3.50.4`.
- This runtime does not currently include `pytest`, `pyewf`, `pytsk3`, `python-magic`, `sqlalchemy`, or `fastapi`.
- Treat this as a diagnostic/runtime helper, not the project development environment.

Node/UI tooling:

- `node` is not available in the normal shell.
- `npm` is not available in the normal shell.
- This is acceptable through Stage 3 because the project is backend-first and UI work is postponed.

Native build tooling:

- `cmake` is not available.
- `cl` / Microsoft C++ compiler is not available in the normal shell.
- `rustc` and `cargo` are not available.
- This is acceptable through Stage 3 because native forensic dependencies remain optional.
- These may matter later for native forensic dependencies, pyewf/pytsk3 builds, Tauri, or packaging.

Forensic Python libraries:

- `pyewf`: not installed.
- `pytsk3`: not installed.
- `python-magic`: not installed.
- This is expected for now. Stage 1 and Stage 2 include stub/fallback adapters, and Stage 3 S3-T01 contract work should not block on these libraries.

Stage 4.5 note:

- Rechecked `pyewf` availability on 2026-07-15 with `importlib.util.find_spec("pyewf")`; result was `missing`.
- Rechecked `pytsk3` availability on 2026-07-15 with `importlib.util.find_spec("pytsk3")`; result was `missing`.
- S4.5-T03 keeps real `pyewf` metadata and verification as a planning/investigation item. No dependency installation has been performed.
- S4.5-T04 keeps EWF-backed streams, partition parsing, and real filesystem parsing as planning/investigation items. No dependency installation has been performed.
- Default tests must continue to pass without `pyewf`, libewf, `pytsk3`, The Sleuth Kit, native build tools, or real E01 files.

## Recommended Setup Before Stage 3 S3-T01

Verify from the project root:

```powershell
python --version
python -m pip --version
```

Create a project virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install pytest
python -m pytest
```

If PowerShell blocks venv activation, either run the activation command from a terminal that allows it or adjust execution policy for the current user.

Current note: tests pass with the currently available global Python 3.14.6, but a project `.venv` is still recommended before adding dependencies beyond `pytest`.

The project test configuration stores pytest temporary files under `.test-artifacts/pytest-temp` instead of the default Windows temp folder. It also disables pytest's optional cache provider for now. This keeps test scratch files inside the writable repository workspace and avoids the observed `C:\Users\cqi\AppData\Local\Temp\pytest-of-cqi` and pytest cache permission issues.

## Stage 1 Dependency Policy

Required for tests:

- Python 3.11+.
- `pytest`.

Not required for Stage 1 tests:

- Real E01 evidence.
- `pyewf`/libewf.
- `pytsk3`.
- Node, Rust, CMake, Visual C++ tools.

Optional:

- `pyewf`/libewf. Missing `pyewf` produces structured dependency-unavailable output. Importable `pyewf` still does not provide real metadata extraction in Stage 1.

Stage 3 and later:

- `pytsk3`, libewf/pyewf, native build tools, or packaged binaries may become important.
- Decide those only after the basic backend contract is stable.

## Stage 3 Dependency Policy

Required for S3-T01 through the initial export foundation:

- Python 3.11+.
- `pytest`.

Not required for default Stage 3 tests:

- Real raw disk images.
- Real E01/EWF evidence.
- `pyewf`/libewf.
- `pytsk3` or The Sleuth Kit.
- Node, Rust, CMake, Visual C++ tools, or desktop UI tooling.

S3-T01 through S3-T06 are reviewed and done. S3-T05 is planning/docs only and does not add recovery code because no real filesystem adapter support exposes deleted entries and recoverable bytes. S3-T06 remained a documentation/review handoff. Stage 3 export-service tests use workspace-local output directories, in-memory SQLite for audit checks, and explicit stub/provider-backed bytes.

## Stage 2 Dependency Policy

Required for Stage 2 tests:

- Python 3.11+.
- `pytest`.

Not required for Stage 2 tests:

- Real raw disk images.
- Real E01/EWF evidence.
- `pyewf`/libewf.
- `pytsk3` or The Sleuth Kit.
- Node, Rust, CMake, Visual C++ tools, or desktop UI tooling.

Optional for later Stage 2 integration checks:

- `pytsk3`/The Sleuth Kit for real filesystem parsing.
- `pyewf`/libewf for real EWF-backed byte streams.
- Tiny local raw or EWF training fixtures kept outside Git.

Stage 2 implementation should introduce dependency boundaries before requiring native forensic packages. Missing `pytsk3`, The Sleuth Kit, `pyewf`, or libewf must produce structured adapter/dependency status and skip optional integration behavior instead of causing default test failures. Normal `python -m pytest` should remain runnable without private evidence or native forensic dependencies.

## Stage 2 Final Dependency Notes

- Default tests use stubs, generated tiny local files, and synthetic provider bytes.
- `LocalFileImageStream` reads tiny local files, but no default test requires a real forensic image.
- `Pytsk3FilesystemAdapter` is a dependency-status skeleton only. Missing or importable `pytsk3` must not make default tests fail.
- `PyewfEwfReaderAdapter` remains a metadata-reader skeleton only. Missing or importable `pyewf` must not be treated as complete real EWF parsing.
- Stage 2 does not require Node, Rust, CMake, Visual C++ tools, `pyewf`, libewf, `pytsk3`, The Sleuth Kit, real EWF images, real raw disk images, or real filesystem images.

## Review Note

If the VS Code agent reports that tests cannot run, check whether it is using a real Python interpreter or only the Microsoft Store alias. That should be treated as an environment blocker, not necessarily a code failure.
