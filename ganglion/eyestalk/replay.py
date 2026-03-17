from __future__ import annotations

from dataclasses import dataclass

from ganglion.eyestalk.metrics import RunMetric


@dataclass(frozen=True)
class ReplayResult:
    fixture_count: int
    success_rate: float
    fallback_rate: float


def replay_metrics(metrics: list[RunMetric]) -> ReplayResult:
    if not metrics:
        return ReplayResult(fixture_count=0, success_rate=0.0, fallback_rate=0.0)

    total = len(metrics)
    success_rate = sum(1 for m in metrics if m.success) / total
    fallback_rate = sum(1 for m in metrics if m.used_fallback) / total
    return ReplayResult(
        fixture_count=total,
        success_rate=success_rate,
        fallback_rate=fallback_rate,
    )
