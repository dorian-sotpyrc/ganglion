from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
import json
from datetime import datetime, timezone

from ganglion.tracer.models import TraceBundle, TraceStep


class TraceWriter:
    def __init__(self, root: str | Path = "artifacts/traces") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def write_trace(self, trace: TraceBundle) -> Path:
        path = self.root / f"{trace.request_id}.json"
        body = {
            "written_at": datetime.now(timezone.utc).isoformat(),
            "trace": asdict(trace),
        }
        path.write_text(json.dumps(body, indent=2), encoding="utf-8")
        return path


def make_step(step_key: str, summary: str, data: dict | None = None, status: str = "ok") -> TraceStep:
    return TraceStep(
        step_key=step_key,
        status=status,
        summary=summary,
        data=data or {},
    )
