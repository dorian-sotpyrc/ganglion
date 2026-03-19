from __future__ import annotations

from dataclasses import dataclass
from collections import Counter

from ganglion.eyestalk.metrics import RunMetric


@dataclass(frozen=True)
class FailurePattern:
    key: str
    count: int
    description: str


def extract_failure_patterns(metrics: list[RunMetric]) -> list[FailurePattern]:
    failed = [m for m in metrics if not m.success or m.used_fallback]
    counts = Counter()

    for m in failed:
        if m.used_fallback:
            counts[f"fallback:{m.lane}"] += 1
        if not m.success:
            counts[f"failure:{m.lane}"] += 1
        if m.confidentiality == "confidential" and m.used_fallback:
            counts["confidential:fallback"] += 1

    patterns = [
        FailurePattern(
            key=k,
            count=v,
            description=f"Detected repeated pattern {k} ({v} occurrences)"
        )
        for k, v in counts.items()
        if v >= 1
    ]
    patterns.sort(key=lambda p: (-p.count, p.key))
    return patterns
