from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ganglion.pipeline import MockProviderAdapter, run_pipeline

MAX_MEMORY_ITEMS = 4
MAX_ITEM_CHARS = 280


def shorten(text: str, limit: int) -> str:
    text = " ".join(str(text).split())
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def read_imported_bundle(repo_root: str | Path, agent_key: str) -> dict[str, Any]:
    bundle_path = Path(repo_root) / "artifacts" / "imported_state" / agent_key / "memory_bundle.json"
    if not bundle_path.exists():
        return {"critical": [], "episodic": [], "sources": {}, "bundle_path": None}
    data = json.loads(bundle_path.read_text(encoding="utf-8"))
    data["bundle_path"] = str(bundle_path)
    return data


def derive_channel_id(payload: dict[str, Any]) -> str:
    if payload.get("channel_id"):
        return str(payload["channel_id"])
    session_id = str(payload.get("session_id") or "")
    metadata = payload.get("metadata") or {}
    if isinstance(metadata, dict):
        for key in ("channel_id", "conversation_id"):
            value = metadata.get(key)
            if value:
                return str(value)
    marker = "channel:"
    if marker in session_id:
        return session_id.split(marker, 1)[1].split(":", 1)[0]
    return ""


def build_rewrite(agent_key: str, result: dict[str, Any], imported_bundle: dict[str, Any], task_text: str) -> str:
    packet = result.get("packet") or {}
    metadata = result.get("ganglion_metadata") or {}
    memory = metadata.get("memory") or {}
    routing = metadata.get("routing") or {}
    critical = [shorten(x, MAX_ITEM_CHARS) for x in memory.get("critical", [])[:MAX_MEMORY_ITEMS]]
    episodic = [shorten(x, MAX_ITEM_CHARS) for x in memory.get("episodic", [])[:MAX_MEMORY_ITEMS]]
    session_summary = shorten(memory.get("session_summary", ""), 600)
    execution_note = shorten(result.get("message", ""), 500)
    runtime_checksum = str(metadata.get("compiled_checksum") or packet.get("trace_id") or "")

    lines = [
        "[Ganglion Pilot Context]",
        f"Use the following as {agent_key}'s active brain/memory/routing context for this turn.",
        "Do not mention Ganglion unless the user explicitly asks.",
        f"Brain checksum: {runtime_checksum}",
        f"Routing lane: {routing.get('lane', 'direct_single_provider')}",
        f"Provider/model intent: {routing.get('provider', 'openai')}/{routing.get('model', 'gpt-5.4')}",
    ]
    if critical:
        lines.append("Critical memory:")
        lines.extend(f"- {item}" for item in critical)
    if episodic:
        lines.append("Relevant episodic memory:")
        lines.extend(f"- {item}" for item in episodic)
    if session_summary:
        lines.append(f"Session summary: {session_summary}")
    if execution_note:
        lines.append(f"Execution note: {execution_note}")
    if imported_bundle.get("bundle_path"):
        lines.append(f"Imported state bundle: {imported_bundle['bundle_path']}")
    lines.extend(
        [
            f"Answer as {agent_key} in the agent's normal voice, using the Ganglion context above to guide memory and judgment.",
            "--- END GANGLION PILOT CONTEXT ---",
            task_text,
        ]
    )
    return "\n\n".join(lines).strip()


def handle_live_binding(repo_root: str | Path, payload: dict[str, Any]) -> dict[str, Any]:
    repo_root = Path(repo_root)
    agent_key = str(payload.get("agent_key") or "agent").strip().lower() or "agent"
    imported_bundle = read_imported_bundle(repo_root, agent_key)
    critical = [str(item.get("text", "")).strip() for item in imported_bundle.get("critical", []) if str(item.get("text", "")).strip()]
    episodic = [str(item.get("text", "")).strip() for item in imported_bundle.get("episodic", []) if str(item.get("text", "")).strip()]
    session_summary = str(imported_bundle.get("session_summary_seed") or "").strip()

    session_messages = payload.get("session_messages") or []
    messages = []
    for message in session_messages[-12:]:
        if isinstance(message, str) and message.strip():
            messages.append({"role": "user", "content": message.strip()})
    task_text = str(payload.get("task_text") or "").strip()
    if task_text:
        messages.append({"role": "user", "content": task_text})
    if not messages:
        messages.append({"role": "user", "content": "No task text provided."})

    ingress = {
        "request_id": str(payload.get("request_id") or f"req-{agent_key}"),
        "conversation_id": derive_channel_id(payload) or str(payload.get("session_id") or ""),
        "timestamp": str(payload.get("timestamp") or payload.get("created_at") or "2026-03-19T00:00:00Z"),
        "messages": messages,
        "provider_hint": str(payload.get("requested_provider") or "openai"),
        "model_hint": str(payload.get("requested_model") or "gpt-5.4"),
        "metadata": {
            "source_system": "openclaw-live-binding",
            "channel": str(payload.get("channel_type") or "unknown"),
            "evidence_mode": "write_local",
            "agent_key": agent_key,
            "channel_id": derive_channel_id(payload),
        },
    }
    result = run_pipeline(
        ingress,
        runtime_root=repo_root / "artifacts",
        adapter=MockProviderAdapter(mode="success", response_text="__ECHO__"),
    )
    result["packet"] = {
        "trace_id": result["trace_id"],
        "run_id": result["run_id"],
    }
    result["ganglion_metadata"] = {
        "artifact_path": result["evidence"]["artifact_path"],
        "compiled_checksum": result["trace_id"],
        "routing": {
            "lane": "direct_single_provider",
            "provider": ingress["provider_hint"],
            "model": ingress["model_hint"],
        },
        "memory": {
            "critical": critical,
            "episodic": episodic,
            "session_summary": session_summary,
        },
    }
    result["message"] = result.get("output", {}).get("content") or ""
    result["rewrite"] = build_rewrite(agent_key, result, imported_bundle, task_text)
    return result
