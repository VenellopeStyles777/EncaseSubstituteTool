# Environment Readiness Check

Purpose: record the local tool/environment state before Stage 1 development.

Last checked: 2026-07-09

## Summary

The repository, Git remote, and normal Python environment are ready for Stage 1 review.

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

- Status: ready for Stage 1.
- `python --version`: Python 3.14.6.
- `python -m pip --version`: pip 26.1.2.
- `python -m pytest`: 22 passed during S1-T06 handoff.
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
- This is acceptable for Stage 1 because the project is backend-first and UI work is postponed.

Native build tooling:

- `cmake` is not available.
- `cl` / Microsoft C++ compiler is not available in the normal shell.
- `rustc` and `cargo` are not available.
- This is acceptable for S1-T01 and S1-T02.
- These may matter later for native forensic dependencies, pyewf/pytsk3 builds, Tauri, or packaging.

Forensic Python libraries:

- `pyewf`: not installed.
- `pytsk3`: not installed.
- `python-magic`: not installed.
- This is expected for now. Stage 1 should include stub/fallback adapters and should not block on these libraries.

## Recommended Setup Before Reviewing Stage 1

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

Stage 2 and later:

- `pytsk3`, libewf/pyewf, native build tools, or packaged binaries may become important.
- Decide those only after the basic backend contract is stable.

## Review Note

If the VS Code agent reports that tests cannot run, check whether it is using a real Python interpreter or only the Microsoft Store alias. That should be treated as an environment blocker, not necessarily a code failure.
