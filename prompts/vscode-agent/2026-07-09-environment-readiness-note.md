# 2026-07-09 - Environment Readiness Note

Use this prompt if the VS Code implementation agent runs into Python or test execution issues during S1-T01.

```text
Environment note for S1-T01:

The research/review agent checked the local environment. Git is working and main tracks origin/main, but the normal PowerShell environment does not currently have a real Python interpreter on PATH. The `python` command resolves to the Microsoft Store alias, `py` is unavailable, and `pip` is unavailable.

Before treating failing tests as a code failure, check whether your VS Code terminal is using a real Python 3.11+ interpreter or only the Store alias.

For S1-T01, do not install dependencies automatically unless the user approves. If Python/pytest is unavailable, document the blocker in progression.md and app/docs/environment-readiness.md, and keep the backend skeleton implementation dependency-light.

Expected eventual setup:
- Install Python 3.11+.
- Create .venv.
- Install pytest.
- Run python -m pytest from the repository root.

Continue to keep S1-T01 scoped to the backend package skeleton and smoke test only.
```
