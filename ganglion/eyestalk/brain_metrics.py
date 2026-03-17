from __future__ import annotations

from pathlib import Path
import json
from collections import defaultdict
from datetime import datetime, timezone


class BrainMetricsService:
    def __init__(
        self,
        runs_root: str | Path = "artifacts/runs",
        out_root: str | Path = "artifacts/brain_metrics",
    ) -> None:
        self.runs_root = Path(runs_root)
        self.out_root = Path(out_root)
        self.out_root.mkdir(parents=True, exist_ok=True)

    def _iter_run_payloads(self) -> list[dict]:
        payloads: list[dict] = []
        if not self.runs_root.exists():
            return payloads

        for path in sorted(self.runs_root.glob("*.json")):
            try:
                body = json.loads(path.read_text(encoding="utf-8"))
                payload = body.get("payload", {})
                if payload:
                    payloads.append(payload)
            except Exception:
                continue
        return payloads

    def summarise(self) -> dict:
        grouped: dict[str, list[dict]] = defaultdict(list)
        for payload in self._iter_run_payloads():
            agent_key = payload.get("agent_key", "unknown")
            grouped[agent_key].append(payload)

        summary: dict[str, dict] = {}
        for agent_key, rows in grouped.items():
            total_runs = len(rows)
            fallback_runs = sum(1 for r in rows if r.get("routing", {}).get("used_fallback"))
            confidential_runs = sum(
                1
                for r in rows
                if r.get("classification", {}).get("confidentiality") == "confidential"
            )
            estimated_cost = sum(float(r.get("cost", {}).get("estimated_cost_usd", 0.0)) for r in rows)
            avg_latency = (
                sum(int(r.get("cost", {}).get("latency_ms", 0)) for r in rows) / total_runs
                if total_runs else 0.0
            )
            avg_episodic = (
                sum(int(r.get("memory", {}).get("episodic_count", 0)) for r in rows) / total_runs
                if total_runs else 0.0
            )
            avg_critical = (
                sum(int(r.get("memory", {}).get("critical_count", 0)) for r in rows) / total_runs
                if total_runs else 0.0
            )

            summary[agent_key] = {
                "total_runs": total_runs,
                "fallback_runs": fallback_runs,
                "fallback_rate": (fallback_runs / total_runs) if total_runs else 0.0,
                "confidential_runs": confidential_runs,
                "confidential_rate": (confidential_runs / total_runs) if total_runs else 0.0,
                "estimated_total_cost_usd": round(estimated_cost, 6),
                "average_latency_ms": round(avg_latency, 2),
                "average_episodic_memories_selected": round(avg_episodic, 2),
                "average_critical_memories_selected": round(avg_critical, 2),
            }

        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "brains": summary,
        }

    def write_summary(self) -> Path:
        summary = self.summarise()
        path = self.out_root / "brain_performance_summary.json"
        path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        return path
