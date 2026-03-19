from __future__ import annotations

from pathlib import Path

from ganglion.antennule.openclaw_adapter import handle_openclaw_request
from ganglion.axon.router import select_route
from ganglion.pleon.classifier import classify_task


def test_low_risk_routes_to_cheap() -> None:
    c = classify_task("Summarise this short note.")
    decision = select_route(classification=c)
    assert decision.lane == "cheap"


def test_high_complexity_routes_to_strong() -> None:
    c = classify_task("Refactor the OpenClaw architecture and debug validator orchestration.")
    decision = select_route(classification=c)
    assert decision.lane == "strong"


def test_confidentiality_routes_to_private_strong() -> None:
    c = classify_task("Review this confidential API key and secret token handling.")
    decision = select_route(classification=c)
    assert decision.lane == "private_strong"
    assert decision.confidentiality == "confidential"


def test_user_requested_model_override_applies_when_allowed() -> None:
    c = classify_task("Summarise this note.")
    decision = select_route(
        classification=c,
        requested_provider="openai-codex",
        requested_model="gpt-5.4",
    )
    assert decision.override_applied is True
    assert decision.provider == "openai-codex"
    assert decision.model == "gpt-5.4"


def test_confidentiality_blocks_cheap_lane_override() -> None:
    c = classify_task("This is confidential client data with password details.")
    decision = select_route(classification=c, requested_lane="cheap")
    assert decision.lane == "private_strong"
    assert any("rejected_due_to_confidentiality" in r for r in decision.routing_reason)


def test_fallback_path_is_used_on_simulated_failure() -> None:
    payload = {
        "agent_key": "surgeon",
        "session_id": "sess-step4-fallback",
        "channel_type": "discord",
        "channel_id": "chan-step4-fallback",
        "user_id": "user-step4-fallback",
        "task_text": "FAIL_PRIMARY diagnose why the service did not start.",
    }
    response = handle_openclaw_request(Path.cwd(), payload)
    assert response["metadata"]["routing"]["used_fallback"] is True
