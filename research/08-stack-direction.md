# Stack Direction Research

Purpose: explain the stack choice in simple terms so the implementation agent can make good early decisions.

Last updated: 2026-07-08

## Short Recommendation

Start with a Python backend/service for the forensic proof of concept, then add a desktop UI later.

Best near-term direction:

- Backend: Python.
- Forensic libraries: `pyewf`/libewf for E01, `pytsk3`/The Sleuth Kit for filesystems.
- Storage: SQLite.
- API boundary: simple command-line JSON first, then FastAPI or another local API only when the UI needs it.
- UI later: Tauri or Electron, after the evidence pipeline works.

Why: this project lives or dies on E01 and filesystem parsing. Python currently gives the shortest path to testing those forensic libraries without first solving a whole desktop packaging problem.

## What Matters Most

The important stack question is not "Which UI framework is nicest?"

The real question is:

Can the app reliably open forensic images, parse filesystems, keep evidence read-only, and preserve provenance?

That points us toward building the backend first.

## Option A - Python Backend First

Good for:

- Fast proof of concept.
- Direct access to forensic bindings.
- Easy tests.
- SQLite integration.
- Simple command-line tools for Stage 1.

Useful libraries:

- libewf/pyewf: E01/EWF evidence image access.
- pytsk3: Python bindings for The Sleuth Kit.
- sqlite3 or SQLAlchemy: case storage.
- hashlib: file/image hashes.
- pytest: tests.

Risks:

- Native dependencies can be annoying on Windows.
- Packaging into a polished desktop app comes later.
- For untrusted forensic input, parsing libraries should eventually be isolated or sandboxed.

Best use now:

- Use this for Stage 1 and Stage 2.
- Keep clean interfaces so the backend can be wrapped by a UI later.

## Option B - Tauri Desktop App

Good for:

- Smaller desktop app than Electron.
- Rust backend can be safer and fast.
- Web UI with native desktop packaging.

Costs:

- Requires Rust, Microsoft C++ Build Tools, and WebView2 on Windows.
- Rust-native forensic library support for E01/filesystem parsing is less obvious than Python bindings.
- Adds desktop packaging complexity before the forensic pipeline is proven.

Best use later:

- Consider Tauri after the backend proves E01 intake and filesystem browsing.
- Tauri can call a Python sidecar/service if staying with Python forensic code.

## Option C - Electron Desktop App

Good for:

- Very common desktop framework.
- Easy web UI development.
- Familiar JavaScript/TypeScript ecosystem.
- Native modules and subprocesses can call a backend service.

Costs:

- Larger app size and memory use.
- Still does not solve forensic parsing by itself.
- Needs careful security boundaries between UI and local system access.

Best use later:

- Useful if the team is more comfortable with TypeScript and wants a faster UI path.
- Should still call a backend forensic service rather than doing forensic parsing in the UI.

## Option D - C++/Qt Native App

Good for:

- Strong native-library integration.
- Mature desktop UI.
- Good performance.

Costs:

- Slower development.
- More manual memory/build complexity.
- Harder for Codex agents to iterate quickly unless the project already has C++/Qt structure.

Best use:

- Not recommended for the first MVP unless the project decides it must be a native C++ forensic workstation from the beginning.

## Recommended Architecture For Now

Stage 1:

- Python package under `app/backend`.
- Command-line intake command that returns JSON.
- No full UI yet.
- Adapter interface for E01 readers.
- Stub adapter so tests pass without native libraries.
- Optional real pyewf/libewf adapter when installed.
- SQLite schema draft for case/evidence/audit.

Stage 2:

- Add pytsk3 filesystem access behind an interface.
- Keep command/API output structured.
- Add small test fixtures or mocks.

Stage 3 and later:

- Add local API.
- Add UI once the backend produces useful, tested data.
- Choose Tauri or Electron based on packaging needs and developer comfort.

## Simple Decision

Use Python first. Delay the UI framework decision.

The project should not choose Tauri/Electron/Qt as the main identity yet. It should choose a backend contract:

```text
Evidence image path in -> structured forensic data out
```

Once that works, the UI can be changed without throwing away the forensic core.

## Sources

- libewf repository: https://github.com/libyal/libewf
- The Sleuth Kit overview: https://www.sleuthkit.org/sleuthkit/
- pytsk3 PyPI page: https://pypi.org/project/pytsk3/
- pytsk GitHub repository: https://github.com/py4n6/pytsk
- Tauri prerequisites: https://tauri.app/start/prerequisites/
- Electron documentation: https://www.electronjs.org/docs/latest/
