from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CostRecord:
    provider: str
    model: str
    estimated_input_tokens: int
    estimated_output_tokens: int
    estimated_cost_usd: float
    latency_ms: int


def estimate_cost(provider: str, model: str, task_text: str, response_text: str, latency_ms: int) -> CostRecord:
    input_tokens = max(1, len(task_text) // 4)
    output_tokens = max(1, len(response_text) // 4)

    if provider == "openrouter":
        rate = 0.0000015
    elif provider == "openai-codex":
        rate = 0.000006
    else:
        rate = 0.000004

    estimated_cost = round((input_tokens + output_tokens) * rate, 6)

    return CostRecord(
        provider=provider,
        model=model,
        estimated_input_tokens=input_tokens,
        estimated_output_tokens=output_tokens,
        estimated_cost_usd=estimated_cost,
        latency_ms=latency_ms,
    )
