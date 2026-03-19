from __future__ import annotations

from pathlib import Path
import json

from ganglion.eyestalk.metrics import RunMetric
from ganglion.eyestalk.service import EyestalkService
from ganglion.molt.candidates import generate_candidates
from ganglion.molt.experiments import build_change_set
from ganglion.molt.scheduler import default_schedule


class MoltService:
    def __init__(self, root: str | Path = "artifacts/tuning") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.eyestalk = EyestalkService()

    def run_cycle(self, cycle_id: str, metrics: list[RunMetric]) -> Path:
        summary = self.eyestalk.summarise_metrics(metrics)
        patterns = summary["patterns"]
        typed_patterns = []
        for p in patterns:
            from ganglion.eyestalk.patterns import FailurePattern
            typed_patterns.append(
                FailurePattern(
                    key=p["key"],
                    count=p["count"],
                    description=p["description"],
                )
            )

        candidates = generate_candidates(typed_patterns)
        change_set = build_change_set(candidates)
        schedule = default_schedule()

        body = {
            "cycle_id": cycle_id,
            "schedule": {
                "frequency": schedule.frequency,
                "enabled": schedule.enabled,
            },
            "summary": summary,
            "change_set": {
                "change_count": change_set.change_count,
                "changes": change_set.changes,
            },
        }

        path = self.root / f"{cycle_id}.json"
        path.write_text(json.dumps(body, indent=2), encoding="utf-8")
        return path
