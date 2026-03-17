from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ProviderResult:
    ok: bool
    provider: str
    model: str
    content: str
    used_fallback: bool
    metadata: dict[str, Any]


class ProviderAdapter:
    def invoke(
        self,
        *,
        provider: str,
        model: str,
        prompt: str,
        fallback_provider: str,
        fallback_model: str,
    ) -> ProviderResult:
        if "FAIL_PRIMARY" in prompt:
            return ProviderResult(
                ok=True,
                provider=fallback_provider,
                model=fallback_model,
                content=f"[fallback:{fallback_provider}/{fallback_model}] {prompt}",
                used_fallback=True,
                metadata={"reason": "simulated_primary_failure"},
            )

        return ProviderResult(
            ok=True,
            provider=provider,
            model=model,
            content=f"[primary:{provider}/{model}] {prompt}",
            used_fallback=False,
            metadata={"reason": "primary_success"},
        )
