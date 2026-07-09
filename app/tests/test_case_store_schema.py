"""Tests for the minimal SQLite case-store schema."""

import json

from app.backend.case_store import (
    SCHEMA_VERSION,
    connect,
    fetch_case,
    fetch_evidence_source,
    initialize_schema,
    insert_audit_event,
    insert_case,
    insert_evidence_source,
    list_audit_events,
)


def _initialized_connection():
    connection = connect()
    initialize_schema(connection)
    return connection


def _sample_intake_result() -> dict[str, object]:
    return {
        "schema_version": "stage1.intake.v1",
        "status": "ok",
        "source_path": "C:/evidence/sample.E01",
        "selected_path": "C:/evidence/sample.E01",
        "read_only": True,
        "segment_count": 2,
        "segment_discovery": {
            "is_valid_input": True,
            "segments": [
                {"segment_number": 1, "path": "C:/evidence/sample.E01"},
                {"segment_number": 2, "path": "C:/evidence/sample.E02"},
            ],
            "warnings": [],
        },
        "adapter": {
            "name": "stub-ewf-reader",
            "available": True,
            "read_only": True,
            "dependency": {"name": "stub", "available": True},
        },
        "metadata": {"reader": "stub", "segment_count": 2},
        "verification": {"status": "not_supported", "supported": False},
        "warnings": [{"source": "reader", "code": "stub_metadata"}],
    }


def test_initialize_schema_creates_required_tables():
    connection = _initialized_connection()

    tables = {
        row["name"]
        for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        ).fetchall()
    }
    migration = connection.execute(
        "SELECT version FROM schema_migrations WHERE version = ?",
        (SCHEMA_VERSION,),
    ).fetchone()

    assert {"cases", "evidence_sources", "audit_events"}.issubset(tables)
    assert migration["version"] == SCHEMA_VERSION


def test_insert_and_fetch_case():
    connection = _initialized_connection()

    case_id = insert_case(
        connection,
        case_id="case-test",
        name="Training Case",
        description="Stage 1 schema test",
    )
    row = fetch_case(connection, case_id)

    assert row["case_id"] == "case-test"
    assert row["name"] == "Training Case"
    assert row["description"] == "Stage 1 schema test"
    assert row["created_at"].endswith("Z")


def test_insert_evidence_source_preserves_intake_provenance():
    connection = _initialized_connection()
    case_id = insert_case(connection, case_id="case-evidence", name="Evidence Case")

    evidence_id = insert_evidence_source(
        connection,
        case_id=case_id,
        evidence_id="evidence-test",
        intake_result=_sample_intake_result(),
    )
    row = fetch_evidence_source(connection, evidence_id)

    segment_discovery = json.loads(row["segment_discovery_json"])
    adapter_dependency = json.loads(row["adapter_dependency_json"])
    verification = json.loads(row["verification_json"])
    warnings = json.loads(row["warnings_json"])

    assert row["evidence_id"] == "evidence-test"
    assert row["case_id"] == case_id
    assert row["source_path"] == "C:/evidence/sample.E01"
    assert row["selected_path"] == "C:/evidence/sample.E01"
    assert row["segment_count"] == 2
    assert row["adapter_name"] == "stub-ewf-reader"
    assert row["adapter_available"] == 1
    assert row["verification_status"] == "not_supported"
    assert row["read_only_asserted"] == 1
    assert segment_discovery["segments"][1]["path"] == "C:/evidence/sample.E02"
    assert adapter_dependency["name"] == "stub"
    assert verification["status"] == "not_supported"
    assert warnings[0]["code"] == "stub_metadata"


def test_insert_and_list_audit_events_for_case_and_evidence():
    connection = _initialized_connection()
    case_id = insert_case(connection, case_id="case-audit", name="Audit Case")
    evidence_id = insert_evidence_source(
        connection,
        case_id=case_id,
        evidence_id="evidence-audit",
        intake_result=_sample_intake_result(),
    )

    audit_id = insert_audit_event(
        connection,
        case_id=case_id,
        evidence_id=evidence_id,
        audit_event_id="audit-test",
        action="evidence_source_added",
        actor="tester",
        details={"status": "ok", "evidence_id": evidence_id},
    )
    events = list_audit_events(connection, case_id=case_id)
    details = json.loads(events[0]["details_json"])

    assert audit_id == "audit-test"
    assert len(events) == 1
    assert events[0]["case_id"] == case_id
    assert events[0]["evidence_id"] == evidence_id
    assert events[0]["action"] == "evidence_source_added"
    assert events[0]["actor"] == "tester"
    assert details["evidence_id"] == evidence_id
