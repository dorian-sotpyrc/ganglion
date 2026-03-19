from __future__ import annotations

from pathlib import Path
import json

from ganglion.eyestalk.metrics import RunMetric
from ganglion.eyestalk.patterns import extract_failure_patterns
from ganglion.eyestalk.replay import replay_metrics
from ganglion.molt.candidates import generate_candidates
from ganglion.molt.service import MoltService


def sample_metrics() -> list[RunMetric]:
    return [
        RunMetric(
            run_id="run-001",
            success=True,
            latency_ms=900,
            used_fallback=False,
            confidentiality="normal",
            lane="cheap",
            provider="openrouter",
            model="openrouter/auto",
            task_text="Summarise note",
        ),
        RunMetric(
            run_id="run-002",
            success=True,
            latency_ms=1400,
            used_fallback=True,
            confidentiality="normal",
            lane="cheap",
            provider="anthropic",
            model="claude-sonnet-4-6",
            task_text="Diagnose service logs",
        ),
        RunMetric(
            run_id="run-003",
            success=False,
            latency_ms=1800,
            used_fallback=True,
            confidentiality="confidential",
            lane="private_strong",
            provider="anthropic",
            model="claude-sonnet-4-6",
            task_text="Review confidential token flow",
        ),
    ]


def test_failure_patterns_detected() -> None:
    patterns = extract_failure_patterns(sample_metrics())
    assert len(patterns) >= 1


def test_replay_metrics_summary() -> None:
    replay = replay_metrics(sample_metrics())
    assert replay.fixture_count == 3
    assert replay.success_rate >= 0.0
    assert replay.fallback_rate > 0.0


def test_candidates_generated() -> None:
    patterns = extract_failure_patterns(sample_metrics())
    candidates = generate_candidates(patterns)
    assert len(candidates) >= 1


def test_molt_cycle_writes_output() -> None:
    svc = MoltService()
    path = svc.run_cycle("cycle-step6-test", sample_metrics())
    assert path.exists()
    body = json.loads(path.read_text(encoding="utf-8"))
    assert body["cycle_id"] == "cycle-step6-test"
    assert body["change_set"]["change_count"] >= 1
