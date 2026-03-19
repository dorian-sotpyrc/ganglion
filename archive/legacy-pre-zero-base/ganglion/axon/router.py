from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ganglion.axon.routing_profiles import RoutingProfile, default_routing_profile
from ganglion.pleon.classifier import TaskClassification


@dataclass(frozen=True)
class RoutingDecision:
    lane: str
    provider: str
    model: str
    override_applied: bool
    routing_reason: list[str]
    confidentiality: str
    fallback_provider: str
    fallback_model: str


DEFAULT_LANE_MAP = {
    "cheap": ("openrouter", "openrouter/auto"),
    "strong": ("openai-codex", "gpt-5.4"),
    "private_strong": ("openai-codex", "gpt-5.4"),
    "fallback": ("anthropic", "claude-sonnet-4-6"),
}


def resolve_lane_from_classification(
    classification: TaskClassification,
    profile: RoutingProfile,
) -> str:
    if classification.confidentiality == "confidential":
        return profile.confidential_lane
    if classification.risk == "high" or classification.complexity == "high":
        return profile.strong_lane
    return profile.default_lane


def select_route(
    *,
    classification: TaskClassification,
    requested_lane: str | None = None,
    requested_provider: str | None = None,
    requested_model: str | None = None,
    profile: RoutingProfile | None = None,
) -> RoutingDecision:
    profile = profile or default_routing_profile()
    reasons: list[str] = []
    override_applied = False

    lane = resolve_lane_from_classification(classification, profile)
    reasons.append(f"classification_selected_lane:{lane}")

    if requested_lane and profile.allow_user_lane_override and requested_lane in profile.allowed_lanes:
        if classification.confidentiality == "confidential" and requested_lane == "cheap":
            reasons.append("requested_lane_rejected_due_to_confidentiality")
        else:
            lane = requested_lane
            override_applied = True
            reasons.append(f"user_lane_override_applied:{requested_lane}")

    provider, model = DEFAULT_LANE_MAP[lane]

    if requested_provider and profile.allow_user_provider_override:
        if classification.confidentiality == "confidential" and requested_provider == "openrouter":
            reasons.append("requested_provider_rejected_due_to_confidentiality")
        else:
            provider = requested_provider
            override_applied = True
            reasons.append(f"user_provider_override_applied:{requested_provider}")

    if requested_model and profile.allow_user_model_override:
        if classification.confidentiality == "confidential" and lane == "cheap":
            reasons.append("requested_model_rejected_due_to_confidentiality")
        else:
            model = requested_model
            override_applied = True
            reasons.append(f"user_model_override_applied:{requested_model}")

    fallback_provider, fallback_model = DEFAULT_LANE_MAP[profile.fallback_lane]

    return RoutingDecision(
        lane=lane,
        provider=provider,
        model=model,
        override_applied=override_applied,
        routing_reason=reasons,
        confidentiality=classification.confidentiality,
        fallback_provider=fallback_provider,
        fallback_model=fallback_model,
    )
