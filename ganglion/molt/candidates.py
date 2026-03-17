from __future__ import annotations

from dataclasses import dataclass

from ganglion.eyestalk.patterns import FailurePattern


@dataclass(frozen=True)
class ChangeCandidate:
    candidate_key: str
    category: str
    proposal: str
    safe_to_auto_apply: bool


def generate_candidates(patterns: list[FailurePattern]) -> list[ChangeCandidate]:
    candidates: list[ChangeCandidate] = []

    for p in patterns:
        if p.key.startswith("fallback:cheap"):
            candidates.append(
                ChangeCandidate(
                    candidate_key="cand-route-stronger-cheap",
                    category="routing",
                    proposal="Consider raising cheap-lane escalation threshold for similar tasks.",
                    safe_to_auto_apply=True,
                )
            )
        elif p.key == "confidential:fallback":
            candidates.append(
                ChangeCandidate(
                    candidate_key="cand-confidential-routing",
                    category="routing",
                    proposal="Review confidential-task routing defaults and fallback triggers.",
                    safe_to_auto_apply=False,
                )
            )
        elif p.key.startswith("failure:"):
            candidates.append(
                ChangeCandidate(
                    candidate_key=f"cand-{p.key.replace(':', '-')}",
                    category="evaluation",
                    proposal=f"Review repeated failures for pattern {p.key}.",
                    safe_to_auto_apply=False,
                )
            )

    deduped = {c.candidate_key: c for c in candidates}
    return list(deduped.values())
