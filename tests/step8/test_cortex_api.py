from __future__ import annotations

import json
from pathlib import Path

from ganglion.antennule.integration_contract import EnvelopeValidationError, normalise_envelope
from ganglion.cortex_api import CortexMetricsService


def test_openclaw_strict_rejects_bad_agent_key() -> None:
    payload = {
        "request_id": "req-1",
        "agent_key": "bad agent",
        "session_id": "sess-1",
        "channel_type": "discord",
        "channel_id": "chan-1",
        "user_id": "user-1",
        "task_text": "hello",
        "metadata": {},
    }
    try:
        normalise_envelope(payload)
    except EnvelopeValidationError as exc:
        assert "agent_key" in str(exc)
    else:
        raise AssertionError("Expected EnvelopeValidationError")


def test_cortex_metrics_reads_actual_metrics(tmp_path: Path) -> None:
    runs = tmp_path / "artifacts" / "runs"
    traces = tmp_path / "artifacts" / "traces"
    runs.mkdir(parents=True)
    traces.mkdir(parents=True)
    agent_brain = tmp_path / "brains" / "agents" / "surgeon" / "operations" / "skills"
    agent_brain.mkdir(parents=True)
    (agent_brain / "triage.md").write_text("skill", encoding="utf-8")
    compactions = tmp_path / "artifacts" / "session_compactions" / "surgeon"
    compactions.mkdir(parents=True)
    (compactions / "sess-1.json").write_text("{}", encoding="utf-8")
    (tmp_path / ".deployed_sha").write_text("abc123\n", encoding="utf-8")

    run_payload = {
        "written_at": "2026-03-18T05:00:00+00:00",
        "payload": {
            "request_id": "req-1",
            "agent_key": "surgeon",
            "compiled_checksum": "checksum-1",
            "task_text": "check host",
            "routing": {"lane": "private_strong", "used_fallback": False, "routing_reason": ["requested_provider_rejected_due_to_confidentiality"]},
            "memory": {"critical_count": 2, "episodic_count": 1},
            "cost": {"estimated_cost_usd": 0.12, "latency_ms": 999},
            "actual_metrics": {"cost_usd": 0.22, "latency_ms": 321, "input_tokens": 10, "output_tokens": 20, "total_tokens": 30},
        },
    }
    trace_payload = {
        "written_at": "2026-03-18T05:00:01+00:00",
        "trace": {"request_id": "req-1", "agent_key": "surgeon", "session_id": "sess-1", "steps": [{"step_key": "brain_compile"}]},
    }
    (runs / "sess-1.json").write_text(json.dumps(run_payload), encoding="utf-8")
    (traces / "req-1.json").write_text(json.dumps(trace_payload), encoding="utf-8")

    svc = CortexMetricsService(tmp_path)
    overview = svc.brain_overview("surgeon")

    assert overview.compiled_checksum == "checksum-1"
    assert overview.deployment_revision == "abc123"
    assert overview.skills_count == 1
    assert overview.session_compaction_count == 1
    assert overview.actual_input_tokens_24h == 10.0
    assert overview.actual_output_tokens_24h == 20.0
    assert overview.actual_total_tokens_24h == 30.0
    assert overview.actual_cost_usd_24h == 0.22
    assert overview.latency_p95_ms == 321.0
    assert overview.trace_coverage_rate == 1.0
    assert overview.private_strong_runs_pct == 1.0
    assert overview.unsafe_override_rejections == 1
