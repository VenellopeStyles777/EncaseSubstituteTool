# Backend API

Purpose: local command/API boundary between backend logic and the future UI.

Stage 1 target:

- Provide a minimal intake command or callable endpoint that returns structured evidence metadata.

## S1-T04 Intake Command

Callable usage from Python:

```python
from app.backend.api import run_e01_intake
from app.backend.forensic_core import StubEwfReaderAdapter

result = run_e01_intake("sample.E01", StubEwfReaderAdapter())
```

Command-line usage from the repository root:

```powershell
python -m app.backend.api.intake path\to\sample.E01
```

By default, the CLI uses the optional `pyewf` adapter and returns structured dependency-unavailable JSON if `pyewf` is not installed. For dependency-free smoke checks with synthetic metadata:

```powershell
python -m app.backend.api.intake path\to\sample.E01 --adapter stub
```

Normal invalid input, such as selecting a non-`.E01` path, prints structured JSON and exits with code `2` rather than a raw traceback.
