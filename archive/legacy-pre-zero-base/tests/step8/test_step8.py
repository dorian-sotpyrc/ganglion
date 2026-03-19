from __future__ import annotations

from pathlib import Path
import json

from ganglion.antennule.openclaw_adapter import handle_openclaw_request
from ganglion.eyestalk.brain_metrics import BrainMetricsService


def repo_root() -> Path:
    return Path.cwd()


def run_payload(session_id: str, task_text: str, requested_model: str | None = None) -> dict:
    payload = {
        "request_id": f"req-{session_id}",
        "agent_key": "surgeon",
        "session_id": session_id,
        "channel_type": "discord",
        "channel_id": f"chan-{session_id}",
        "user_id": f"user-{session_id}",
        "task_text": task_text,
        "session_messages": [
            "Need diagnosis.",
            "Need safe path.",
        ],
    }
    if requested_model:
        payload["requested_model"] = requested_model
    return payload


def test_trace_file_written() -> None:
    result = handle_openclaw_request(
        repo_root(),
        run_payload("sess-step8-trace", "Review confidential service logs and rollback options.", "gpt-5.4"),
    )
    trace_path = Path(result["metadata"]["trace_path"])
    assert trace_path.exists()
    body = json.loads(trace_path.read_text(encoding="utf-8"))
    assert body["trace"]["request_id"] == "req-sess-step8-trace"
    assert len(body["trace"]["steps"]) >= 5


def test_trace_has_step_details() -> None:
    result = handle_openclaw_request(
        repo_root(),
        run_payload("sess-step8-details", "Summarise service restart findings."),
    )
    trace_path = Path(result["metadata"]["trace_path"])
    body = json.loads(trace_path.read_text(encoding="utf-8"))
    step_keys = [s["step_key"] for s in body["trace"]["steps"]]
    assert "brain_compile" in step_keys
    assert "classification" in step_keys
    assert "routing" in step_keys


def test_brain_metrics_summary_written() -> None:
    handle_openclaw_request(
        repo_root(),
        run_payload("sess-step8-m1", "Summarise service restart findings."),
    )
    handle_openclaw_request(
        repo_root(),
        run_payload("sess-step8-m2", "Review confidential token handling and service logs.", "gpt-5.4"),
    )
    svc = BrainMetricsService()
    path = svc.write_summary()
    assert path.exists()
    body = json.loads(path.read_text(encoding="utf-8"))
    assert "surgeon" in body["brains"]


def test_brain_metrics_contains_expected_fields() -> None:
    svc = BrainMetricsService()
    body = svc.summarise()
    if "surgeon" in body["brains"]:
        metrics = body["brains"]["surgeon"]
        assert "total_runs" in metrics
        assert "fallback_rate" in metrics
        assert "estimated_total_cost_usd" in metrics
        assert "average_latency_ms" in metrics
