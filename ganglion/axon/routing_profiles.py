from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class RoutingProfile:
    default_lane: str = "cheap"
    strong_lane: str = "strong"
    confidential_lane: str = "private_strong"
    fallback_lane: str = "fallback"
    allow_user_model_override: bool = True
    allow_user_provider_override: bool = True
    allow_user_lane_override: bool = True
    allowed_lanes: tuple[str, ...] = ("cheap", "strong", "private_strong", "fallback")


def default_routing_profile() -> RoutingProfile:
    return RoutingProfile()
