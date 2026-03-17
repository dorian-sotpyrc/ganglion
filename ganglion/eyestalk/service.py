from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
import json

from ganglion.eyestalk.metrics import RunMetric
from ganglion.eyestalk.patterns import extract_failure_patterns
from ganglion.eyestalk.replay import replay_metrics


class EyestalkService:
    def __init__(self, root: str | Path = "artifacts/eval") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def record_run_metric(self, metric: RunMetric) -> Path:
        path = self.root / f"{metric.run_id}.json"
        path.write_text(json.dumps(asdict(metric), indent=2), encoding="utf-8")
        return path

    def summarise_metrics(self, metrics: list[RunMetric]) -> dict:
        replay = replay_metrics(metrics)
        patterns = extract_failure_patterns(metrics)
        return {
            "replay": {
                "fixture_count": replay.fixture_count,
                "success_rate": replay.success_rate,
                "fallback_rate": replay.fallback_rate,
            },
            "patterns": [
                {"key": p.key, "count": p.count, "description": p.description}
                for p in patterns
            ],
        }
