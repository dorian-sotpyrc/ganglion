from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from ganglion.eyestalk.brain_metrics import BrainMetricsService
from ganglion.openclaw_profile import INTEGRATION_PROFILE_OPENCLAW_STRICT


@dataclass(frozen=True)
class BrainOverview:
    agent_key: str
    compiled_checksum: str | None
    deployment_revision: str | None
    integration_profile: str
    latest_run_at: str | None
    latest_trace_at: str | None
    success_rate: float | None
    task_completion_rate: float | None
    re_prompt_rate: float | None
    memory_hit_rate: float | None
    avg_critical_selected: float | None
    avg_episodic_selected: float | None
    skills_count: int
    session_compaction_count: int
    private_strong_runs_pct: float | None
    unsafe_override_rejections: int
    actual_input_tokens_24h: float | None
    actual_output_tokens_24h: float | None
    actual_total_tokens_24h: float | None
    actual_cost_usd_24h: float | None
    cost_per_successful_run: float | None
    latency_p95_ms: float | None
    trace_coverage_rate: float | None


class CortexMetricsService:
    def __init__(self, repo_root: str | Path) -> None:
        self.repo_root = Path(repo_root)
        self.artifacts_root = self.repo_root / "artifacts"
        self.runs_root = self.artifacts_root / "runs"
        self.traces_root = self.artifacts_root / "traces"
        self.session_compactions_root = self.artifacts_root / "session_compactions"
        self.brains_root = self.repo_root / "brains" / "agents"
        self.metrics_service = BrainMetricsService(self.runs_root, self.artifacts_root / "brain_metrics")

    def _iter_run_files(self) -> list[Path]:
        if not self.runs_root.exists():
            return []
        return sorted(self.runs_root.glob("*.json"), key=lambda p: p.stat().st_mtime)

    def _iter_trace_files(self) -> list[Path]:
        if not self.traces_root.exists():
            return []
        return sorted(self.traces_root.glob("*.json"), key=lambda p: p.stat().st_mtime)

    def _load_json(self, path: Path) -> dict[str, Any] | None:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return None

    def _rows_for_agent(self, agent_key: str) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for path in self._iter_run_files():
            body = self._load_json(path) or {}
            payload = body.get("payload") or {}
            if payload.get("agent_key") == agent_key:
                payload = {**payload, "_written_at": body.get("written_at"), "_path": str(path)}
                rows.append(payload)
        return rows

    def _traces_for_agent(self, agent_key: str) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for path in self._iter_trace_files():
            body = self._load_json(path) or {}
            trace = body.get("trace") or {}
            if trace.get("agent_key") == agent_key:
                rows.append({**trace, "_written_at": body.get("written_at"), "_path": str(path)})
        return rows

    def _skills_count(self, agent_key: str) -> int:
        skills_dir = self.brains_root / agent_key / "operations" / "skills"
        if not skills_dir.exists():
            return 0
        return sum(1 for p in skills_dir.rglob("*") if p.is_file())

    def _session_compaction_count(self, agent_key: str) -> int:
        root = self.session_compactions_root / agent_key
        if not root.exists():
            return 0
        return sum(1 for p in root.glob("*.json") if p.is_file())

    def _latest_checksum(self, rows: list[dict[str, Any]]) -> str | None:
        if not rows:
            return None
        return rows[-1].get("compiled_checksum")

    def _actual_metric_24h(self, rows: list[dict[str, Any]], key: str) -> float | None:
        now = datetime.now(timezone.utc)
        total = 0.0
        seen_actual = False
        for row in rows:
            written_at = row.get("_written_at")
            if not written_at:
                continue
            try:
                ts = datetime.fromisoformat(str(written_at))
            except Exception:
                continue
            if (now - ts).total_seconds() > 86400:
                continue
            actual = row.get("actual_metrics") or {}
            if key in actual and actual.get(key) is not None:
                total += float(actual.get(key) or 0.0)
                seen_actual = True
        return round(total, 6) if seen_actual else None

    def _latency_p95(self, rows: list[dict[str, Any]]) -> float | None:
        vals: list[float] = []
        for row in rows:
            actual = row.get("actual_metrics") or {}
            if actual.get("latency_ms") is not None:
                vals.append(float(actual.get("latency_ms")))
            elif row.get("cost", {}).get("latency_ms") is not None:
                vals.append(float(row.get("cost", {}).get("latency_ms")))
        if not vals:
            return None
        vals.sort()
        idx = max(0, min(len(vals) - 1, int(round(0.95 * (len(vals) - 1)))))
        return round(vals[idx], 2)

    def _trace_coverage_rate(self, rows: list[dict[str, Any]], traces: list[dict[str, Any]]) -> float | None:
        if not rows:
            return None
        run_ids = {str(r.get("request_id")) for r in rows if r.get("request_id")}
        trace_ids = {str(t.get("request_id")) for t in traces if t.get("request_id")}
        if not run_ids:
            return None
        return round(len(run_ids & trace_ids) / len(run_ids), 4)

    def _private_strong_pct(self, rows: list[dict[str, Any]]) -> float | None:
        if not rows:
            return None
        count = sum(1 for r in rows if r.get("routing", {}).get("lane") == "private_strong")
        return round(count / len(rows), 4)

    def _avg_selected(self, rows: list[dict[str, Any]], key: str) -> float | None:
        if not rows:
            return None
        return round(sum(float(r.get("memory", {}).get(key, 0)) for r in rows) / len(rows), 2)

    def _success_rate(self, rows: list[dict[str, Any]]) -> float | None:
        if not rows:
            return None
        success = sum(1 for r in rows if not r.get("routing", {}).get("used_fallback"))
        return round(success / len(rows), 4)

    def _task_completion_rate(self, rows: list[dict[str, Any]]) -> float | None:
        if not rows:
            return None
        completed = sum(1 for r in rows if bool(str(r.get("task_text", "")).strip()))
        return round(completed / len(rows), 4)

    def _re_prompt_rate(self, rows: list[dict[str, Any]]) -> float | None:
        if not rows:
            return None
        followups = sum(1 for r in rows if int(r.get("memory", {}).get("episodic_count", 0)) > 0)
        return round(followups / len(rows), 4)

    def _memory_hit_rate(self, rows: list[dict[str, Any]]) -> float | None:
        if not rows:
            return None
        hits = sum(1 for r in rows if (int(r.get("memory", {}).get("critical_count", 0)) + int(r.get("memory", {}).get("episodic_count", 0))) > 0)
        return round(hits / len(rows), 4)

    def _unsafe_override_rejections(self, rows: list[dict[str, Any]]) -> int:
        total = 0
        for row in rows:
            reasons = row.get("routing", {}).get("routing_reason") or []
            total += sum(1 for reason in reasons if "rejected" in str(reason))
        return total

    def _deployment_revision(self) -> str | None:
        path = self.repo_root / ".deployed_sha"
        if path.exists():
            return path.read_text(encoding="utf-8", errors="replace").strip() or None
        return None

    def brain_overview(self, agent_key: str) -> BrainOverview:
        rows = self._rows_for_agent(agent_key)
        traces = self._traces_for_agent(agent_key)
        success_rate = self._success_rate(rows)
        actual_input_24h = self._actual_metric_24h(rows, "input_tokens")
        actual_output_24h = self._actual_metric_24h(rows, "output_tokens")
        actual_total_24h = self._actual_metric_24h(rows, "total_tokens")
        actual_cost_24h = self._actual_metric_24h(rows, "cost_usd")
        successful_runs = max(1, sum(1 for r in rows if not r.get("routing", {}).get("used_fallback"))) if rows else 0
        cost_per_success = round(actual_cost_24h / successful_runs, 6) if actual_cost_24h is not None and successful_runs else None
        latest_run_at = rows[-1].get("_written_at") if rows else None
        latest_trace_at = traces[-1].get("_written_at") if traces else None
        return BrainOverview(
            agent_key=agent_key,
            compiled_checksum=self._latest_checksum(rows),
            deployment_revision=self._deployment_revision(),
            integration_profile=INTEGRATION_PROFILE_OPENCLAW_STRICT,
            latest_run_at=latest_run_at,
            latest_trace_at=latest_trace_at,
            success_rate=success_rate,
            task_completion_rate=self._task_completion_rate(rows),
            re_prompt_rate=self._re_prompt_rate(rows),
            memory_hit_rate=self._memory_hit_rate(rows),
            avg_critical_selected=self._avg_selected(rows, "critical_count"),
            avg_episodic_selected=self._avg_selected(rows, "episodic_count"),
            skills_count=self._skills_count(agent_key),
            session_compaction_count=self._session_compaction_count(agent_key),
            private_strong_runs_pct=self._private_strong_pct(rows),
            unsafe_override_rejections=self._unsafe_override_rejections(rows),
            actual_input_tokens_24h=actual_input_24h,
            actual_output_tokens_24h=actual_output_24h,
            actual_total_tokens_24h=actual_total_24h,
            actual_cost_usd_24h=actual_cost_24h,
            cost_per_successful_run=cost_per_success,
            latency_p95_ms=self._latency_p95(rows),
            trace_coverage_rate=self._trace_coverage_rate(rows, traces),
        )

    def brains_index(self) -> dict[str, Any]:
        generated_at = datetime.now(timezone.utc).isoformat()
        metrics_summary = self.metrics_service.summarise()
        agent_keys = sorted(metrics_summary.get("brains", {}).keys())
        return {
            "generated_at": generated_at,
            "integration_profile": INTEGRATION_PROFILE_OPENCLAW_STRICT,
            "agents": [asdict(self.brain_overview(agent_key)) for agent_key in agent_keys],
        }
