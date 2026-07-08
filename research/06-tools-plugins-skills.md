# Tools, Plugins, And Skills

Purpose: collect useful libraries, Codex skills, and development tools.

Codex-side skills/plugins:

- Browser control skill: useful for checking the app UI once a local dev server or desktop web UI exists.
- PDF skill: useful later for verifying generated forensic reports.
- Documents skill: useful if reports need Word-compatible exports.
- Spreadsheets skill: useful if hash lists, exports, or triage tables need `.xlsx` output.
- OpenAI docs skill: useful only if adding OpenAI-powered triage later.

Development libraries/tools to investigate:

- libewf / pyewf for `.E01/.E02/...` support.
- The Sleuth Kit / pytsk3 for volume and filesystem analysis. Source: https://www.sleuthkit.org/sleuthkit/
- SQLite for case database.
- libmagic or a curated signature table for file type detection.
- Built-in language hash libraries for MD5, SHA-1, and SHA-256.
- SQLite FTS5 for early full-text search.
- HTML plus PDF export for early reports.
- NIST NSRL hash data for known-file matching. Source: https://www.nist.gov/itl/csd/secure-systems-and-applications/national-software-reference-library-nsrl

Suggested stack direction:

- Start with a Python forensic-service spike to prove E01 plus filesystem access.
- Delay the final UI framework decision until the backend can produce structured forensic data.
- Wrap the forensic code behind a clean command/API boundary so the UI can later be Tauri, Electron, or another desktop shell.
- Use SQLite for case storage from the start.

See also: [08-stack-direction.md](08-stack-direction.md).

Backend tradeoffs:

- Rust: strong for desktop apps, streaming, hashing, and safety; native bindings may take more setup.
- Python: fastest MVP with `pyewf`, `pytsk3`, SQLite, and workers; Windows native dependency packaging may be painful.
- C++/Qt: strong native library fit, but heavier development cost.
