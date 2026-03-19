from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TuningSchedule:
    frequency: str
    enabled: bool = True


def default_schedule() -> TuningSchedule:
    return TuningSchedule(frequency="daily", enabled=True)
