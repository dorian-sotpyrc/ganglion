from __future__ import annotations

from pathlib import Path

import pytest

from ganglion.antennule.request_adapter import RequestAdapterError, adapt_openclaw_request
from ganglion.antennule.openclaw_adapter import handle_openclaw_request
from ganglion.pleon.orchestrator import Orchestrator


def sample_payload() -> dict[str, str]:
    return {
        "agent_key": "surgeon",
        "session_id": "sess-001",
        "channel_type": "discord",
        "channel_id": "chan-001",
        "user_id": "user-001",
        "task_text": "Diagnose why the service did not start.",
    }


def test_request_adapter_accepts_valid_payload() -> None:
    request = adapt_openclaw_request(sample_payload())
    assert request.agent_key == "surgeon"
    assert request.session_id == "sess-001"


def test_request_adapter_rejects_missing_fields() -> None:
    payload = sample_payload()
    payload.pop("task_text")
    with pytest.raises(RequestAdapterError):
        adapt_openclaw_request(payload)


def test_orchestrator_builds_runtime_package() -> None:
    request = adapt_openclaw_request(sample_payload())
    orchestrator = Orchestrator(Path.cwd())
    runtime = orchestrator.build_runtime_package(request)
    assert runtime.agent_key == "surgeon"
    assert runtime.compiled_checksum
    assert "Mock run prepared" in runtime.execution_note


def test_openclaw_adapter_end_to_end_mock() -> None:
    response = handle_openclaw_request(Path.cwd(), sample_payload())
    assert response["status"] == "ok"
    assert response["agent_key"] == "surgeon"
    assert response["compiled_checksum"]
    assert "Prepared mocked execution" in response["message"]
    assert response["metadata"]["mode"] == "mock"
