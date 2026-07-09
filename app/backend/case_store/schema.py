"""Minimal SQLite case-store schema for Stage 1."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
from typing import Any, Mapping
from uuid import uuid4


SCHEMA_VERSION = 1


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS schema_migrations (
    version INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cases (
    case_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS evidence_sources (
    evidence_id TEXT PRIMARY KEY,
    case_id TEXT NOT NULL,
    source_type TEXT NOT NULL DEFAULT 'ewf',
    source_path TEXT NOT NULL,
    selected_path TEXT NOT NULL,
    status TEXT NOT NULL,
    segment_count INTEGER NOT NULL DEFAULT 0 CHECK (segment_count >= 0),
    segment_discovery_json TEXT NOT NULL,
    adapter_name TEXT NOT NULL,
    adapter_available INTEGER NOT NULL CHECK (adapter_available IN (0, 1)),
    adapter_dependency_json TEXT NOT NULL,
    metadata_json TEXT NOT NULL,
    verification_status TEXT NOT NULL,
    verification_json TEXT NOT NULL,
    read_only_asserted INTEGER NOT NULL CHECK (read_only_asserted IN (0, 1)),
    warnings_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_evidence_sources_case_id
    ON evidence_sources(case_id);

CREATE TABLE IF NOT EXISTS audit_events (
    audit_event_id TEXT PRIMARY KEY,
    case_id TEXT NOT NULL,
    evidence_id TEXT,
    action TEXT NOT NULL,
    actor TEXT,
    details_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE,
    FOREIGN KEY (evidence_id) REFERENCES evidence_sources(evidence_id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_audit_events_case_id
    ON audit_events(case_id);

CREATE INDEX IF NOT EXISTS idx_audit_events_evidence_id
    ON audit_events(evidence_id);
"""


def connect(database: str | Path = ":memory:") -> sqlite3.Connection:
    """Create a SQLite connection configured for the case store."""

    connection = sqlite3.connect(str(database))
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_schema(connection: sqlite3.Connection) -> None:
    """Create the minimal Stage 1 schema on a SQLite connection."""

    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript(SCHEMA_SQL)
    connection.execute(
        "INSERT OR IGNORE INTO schema_migrations (version, applied_at) VALUES (?, ?)",
        (SCHEMA_VERSION, _utc_now()),
    )
    connection.commit()


def insert_case(
    connection: sqlite3.Connection,
    *,
    name: str,
    description: str | None = None,
    case_id: str | None = None,
) -> str:
    """Insert a case and return its id."""

    now = _utc_now()
    case_id = case_id or _new_id("case")
    connection.execute(
        """
        INSERT INTO cases (case_id, name, description, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (case_id, name, description, now, now),
    )
    connection.commit()
    return case_id


def insert_evidence_source(
    connection: sqlite3.Connection,
    *,
    case_id: str,
    intake_result: Mapping[str, Any],
    evidence_id: str | None = None,
    source_type: str = "ewf",
) -> str:
    """Insert an evidence source from an S1-T04-style intake result."""

    adapter = _mapping(intake_result.get("adapter"))
    dependency = _mapping(adapter.get("dependency"))
    verification = _mapping(intake_result.get("verification"))
    segment_discovery = _mapping(intake_result.get("segment_discovery"))
    metadata = _mapping(intake_result.get("metadata"))
    warnings = intake_result.get("warnings", [])
    source_path = str(intake_result.get("source_path") or intake_result.get("selected_path") or "")
    selected_path = str(intake_result.get("selected_path") or source_path)

    if not source_path:
        raise ValueError("intake_result must include source_path or selected_path")

    now = _utc_now()
    evidence_id = evidence_id or _new_id("evidence")
    connection.execute(
        """
        INSERT INTO evidence_sources (
            evidence_id,
            case_id,
            source_type,
            source_path,
            selected_path,
            status,
            segment_count,
            segment_discovery_json,
            adapter_name,
            adapter_available,
            adapter_dependency_json,
            metadata_json,
            verification_status,
            verification_json,
            read_only_asserted,
            warnings_json,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            evidence_id,
            case_id,
            source_type,
            source_path,
            selected_path,
            str(intake_result.get("status") or "unknown"),
            int(intake_result.get("segment_count") or 0),
            _json_dumps(segment_discovery),
            str(adapter.get("name") or "unknown"),
            _bool_to_int(bool(adapter.get("available", False))),
            _json_dumps(dependency),
            _json_dumps(metadata),
            str(verification.get("status") or "unknown"),
            _json_dumps(verification),
            _bool_to_int(bool(intake_result.get("read_only", False))),
            _json_dumps(warnings),
            now,
            now,
        ),
    )
    connection.commit()
    return evidence_id


def insert_audit_event(
    connection: sqlite3.Connection,
    *,
    case_id: str,
    action: str,
    details: Mapping[str, Any] | None = None,
    evidence_id: str | None = None,
    actor: str | None = None,
    audit_event_id: str | None = None,
) -> str:
    """Insert an audit event and return its id."""

    audit_event_id = audit_event_id or _new_id("audit")
    connection.execute(
        """
        INSERT INTO audit_events (
            audit_event_id,
            case_id,
            evidence_id,
            action,
            actor,
            details_json,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            audit_event_id,
            case_id,
            evidence_id,
            action,
            actor,
            _json_dumps(details or {}),
            _utc_now(),
        ),
    )
    connection.commit()
    return audit_event_id


def fetch_case(connection: sqlite3.Connection, case_id: str) -> sqlite3.Row | None:
    return connection.execute(
        "SELECT * FROM cases WHERE case_id = ?",
        (case_id,),
    ).fetchone()


def fetch_evidence_source(
    connection: sqlite3.Connection,
    evidence_id: str,
) -> sqlite3.Row | None:
    return connection.execute(
        "SELECT * FROM evidence_sources WHERE evidence_id = ?",
        (evidence_id,),
    ).fetchone()


def list_audit_events(
    connection: sqlite3.Connection,
    *,
    case_id: str,
) -> list[sqlite3.Row]:
    return list(
        connection.execute(
            "SELECT * FROM audit_events WHERE case_id = ? ORDER BY created_at, audit_event_id",
            (case_id,),
        ).fetchall()
    )


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _json_dumps(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _bool_to_int(value: bool) -> int:
    return 1 if value else 0


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex}"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
