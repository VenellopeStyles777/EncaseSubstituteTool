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

Current status values include:

- `ok`: stub-backed intake completed with synthetic metadata.
- `metadata_unavailable`: adapter dependency is unavailable, such as missing `pyewf`.
- `reader_not_implemented`: adapter dependency is importable, but real metadata extraction is not implemented yet.
- `invalid_input`: selected path is missing or not a valid `.E01` first segment.
- `reader_error`: unexpected adapter exception caught at the command boundary.

S1-T04 does not persist results automatically. Use the case-store helpers explicitly when a case workflow is ready.

## S2-T05 Directory Listing Callable

Callable usage from Python:

```python
from app.backend.api import list_directory
from app.backend.forensic_core import StubFilesystemAdapter

result = list_directory(volume, "/", StubFilesystemAdapter())
```

`list_directory()` consumes a `VolumeInfo` and a filesystem adapter. It returns a JSON-friendly dictionary with:

- schema version and structured listing status;
- directory path;
- source path, volume id, volume offset/length, filesystem type, adapter/dependency details, and read-only assertion;
- file/directory entries from the filesystem adapter, including file id, path, name, type, size, timestamps, allocation/deleted state, status/warnings, and provenance;
- adapter/listing warnings.

Current S2-T05 behavior:

- root listing with `StubFilesystemAdapter` returns deterministic entries for `/Documents` and `/hello.txt`;
- empty path normalizes to `/`, and paths without a leading slash are normalized with one;
- nested directory paths such as `/Documents` return `path_unsupported`;
- file paths such as `/hello.txt` return `path_not_directory`;
- missing paths return `path_not_found`;
- dependency-unavailable or not-implemented adapters return `filesystem_unavailable`.

S2-T05 does not read file content, render raw/text/hex preview, export files, hash files, persist case-store data, parse real filesystems, or require `pytsk3`/The Sleuth Kit.
