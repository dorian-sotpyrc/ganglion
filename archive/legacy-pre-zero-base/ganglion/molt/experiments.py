from __future__ import annotations

from dataclasses import dataclass

from ganglion.molt.candidates import ChangeCandidate


@dataclass(frozen=True)
class ChangeSet:
    change_count: int
    changes: list[dict]


def build_change_set(candidates: list[ChangeCandidate]) -> ChangeSet:
    changes = [
        {
            "candidate_key": c.candidate_key,
            "category": c.category,
            "proposal": c.proposal,
            "safe_to_auto_apply": c.safe_to_auto_apply,
        }
        for c in candidates
    ]
    return ChangeSet(change_count=len(changes), changes=changes)
