from __future__ import annotations

import json
import uuid
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class GanglionError(Exception):
    def __init__(self, error_type: str, message: str, *, stage: str, retryable: bool = False, details: dict[str, Any] | None = None):
        super().__init__(message)
        self.error_type = error_type
        self.message = message
        self.stage = stage
        self.retryable = retryable
        self.details = details or {}

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.error_type,
            "message": self.message,
            "stage": self.stage,
            "retryable": self.retryable,
            "details": self.details,
        }


@dataclass
class MockProviderAdapter:
    mode: str = "success"
    response_text: str = "Ping received."

    def invoke(self, request: dict[str, Any]) -> dict[str, Any]:
        now = utc_now()
        if self.mode == "error":
            return {
                "trace_id": request["trace_id"],
                "run_id": request["run_id"],
                "status": "error",
                "provider": request["provider"],
                "model": request["model"],
                "output_text": None,
                "raw_timing": {
                    "started_at": now,
                    "completed_at": now,
                    "duration_ms": 1,
                },
                "transport_metadata": {
                    "http_status": 504,
                    "request_id": f"provider_req_{uuid.uuid4().hex[:12]}",
                },
                "usage": None,
                "raw_response_ref": None,
                "error": {
                    "type": "provider_transport_error",
                    "message": "provider timeout",
                    "stage": "peduncle",
                    "retryable": True,
                    "details": {"timeout_ms": request["transport"]["timeout_ms"]},
                },
            }

        prompt = request["messages"][-1]["content"]
        output_text = self.response_text if self.response_text != "__ECHO__" else f"Echo: {prompt}"
        usage = {
            "input_tokens": sum(len(m["content"].split()) for m in request["messages"]),
            "output_tokens": len(output_text.split()),
            "total_tokens": 0,
            "cost": None,
            "currency": None,
        }
        usage["total_tokens"] = usage["input_tokens"] + usage["output_tokens"]
        return {
            "trace_id": request["trace_id"],
            "run_id": request["run_id"],
            "status": "success",
            "provider": request["provider"],
            "model": request["model"],
            "output_text": output_text,
            "raw_timing": {
                "started_at": now,
                "completed_at": now,
                "duration_ms": 1,
            },
            "transport_metadata": {
                "http_status": 200,
                "request_id": f"provider_req_{uuid.uuid4().hex[:12]}",
            },
            "usage": usage,
            "raw_response_ref": None,
            "error": None,
        }


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _stamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H-%M-%SZ")


def _mkdir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _write_json(path: Path, payload: dict[str, Any]) -> str:
    _mkdir(path)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return str(path)


def validate_ingress(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise GanglionError("ingress_error", "top-level shape is not an object", stage="antennule")
    for field in ("request_id", "timestamp", "messages", "metadata"):
        if field not in payload:
            raise GanglionError("ingress_error", f"missing required field: {field}", stage="antennule")
    if not isinstance(payload["metadata"], dict):
        raise GanglionError("ingress_error", "metadata must be an object", stage="antennule")
    if not isinstance(payload["messages"], list) or not payload["messages"]:
        raise GanglionError("ingress_error", "messages must be a non-empty list", stage="antennule")
    datetime.fromisoformat(payload["timestamp"].replace("Z", "+00:00"))
    for idx, message in enumerate(payload["messages"]):
        if not isinstance(message, dict):
            raise GanglionError("ingress_error", f"message {idx} is not an object", stage="antennule")
        if message.get("role") not in {"system", "user", "assistant", "tool"}:
            raise GanglionError("ingress_error", f"message {idx} has invalid role", stage="antennule")
        if not isinstance(message.get("content"), str):
            raise GanglionError("ingress_error", f"message {idx} content must be string", stage="antennule")
    return deepcopy(payload)


def build_packet(ingress: dict[str, Any]) -> dict[str, Any]:
    request_id = ingress["request_id"]
    trace_token = uuid.uuid5(uuid.NAMESPACE_URL, request_id).hex[:12]
    trace_id = f"trace_{datetime.now(timezone.utc).strftime('%Y%m%d')}_{trace_token}"
    run_id = f"run_{datetime.now(timezone.utc).strftime('%Y%m%d')}_{uuid.uuid4().hex[:12]}"
    packet = {
        "packet_version": "v1alpha1",
        "trace_id": trace_id,
        "run_id": run_id,
        "source_system": ingress["metadata"].get("source_system", "openclaw"),
        "ingress_timestamp": ingress["timestamp"],
        "normalized_messages": [
            {"index": idx, "role": m["role"], "content": m["content"]}
            for idx, m in enumerate(ingress["messages"])
        ],
        "provider_target": ingress.get("provider_hint") or "openai",
        "model_target": ingress.get("model_hint") or "gpt-5.4",
        "routing_mode": "direct_single_provider",
        "evidence_mode": ingress["metadata"].get("evidence_mode", "write_local"),
        "metadata": {
            "request_id": ingress["request_id"],
            "conversation_id": ingress.get("conversation_id"),
            **ingress["metadata"],
        },
    }
    return packet


def build_provider_request(packet: dict[str, Any]) -> dict[str, Any]:
    return {
        "trace_id": packet["trace_id"],
        "run_id": packet["run_id"],
        "provider": packet["provider_target"],
        "model": packet["model_target"],
        "messages": [
            {"role": m["role"], "content": m["content"]}
            for m in packet["normalized_messages"]
        ],
        "transport": {"timeout_ms": 30000},
        "metadata": {"source_system": "ganglion"},
    }


def build_return(provider_response: dict[str, Any], evidence_path: str) -> dict[str, Any]:
    success = provider_response["status"] == "success"
    return {
        "trace_id": provider_response["trace_id"],
        "run_id": provider_response["run_id"],
        "status": provider_response["status"],
        "output": {"role": "assistant", "content": provider_response["output_text"]} if success else None,
        "provider": {"name": provider_response["provider"], "model": provider_response["model"]},
        "usage": provider_response.get("usage") if success else None,
        "evidence": {"written": True, "artifact_path": evidence_path},
        "error": None if success else provider_response["error"],
    }


def write_evidence(runtime_root: Path, packet: dict[str, Any], provider_request: dict[str, Any], provider_response: dict[str, Any], final_return: dict[str, Any]) -> str:
    stamp = _stamp()
    trace_id = packet["trace_id"]
    evidence_path = runtime_root / "evidence" / f"{stamp}_{trace_id}_run.json"
    trace_path = runtime_root / "traces" / f"{stamp}_{trace_id}.log"
    transcript_path = runtime_root / "samples" / f"{stamp}_{trace_id}.transcript.log"
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    transcript_path.parent.mkdir(parents=True, exist_ok=True)
    trace_path.write_text(
        "\n".join([
            f"trace_id={trace_id}",
            f"run_id={packet['run_id']}",
            f"provider={packet['provider_target']}",
            f"model={packet['model_target']}",
            f"status={provider_response['status']}",
        ]) + "\n",
        encoding="utf-8",
    )
    transcript_path.write_text(
        json.dumps({
            "ingress": packet["metadata"].get("request_id"),
            "last_user_message": packet["normalized_messages"][-1]["content"],
            "assistant_output": final_return["output"]["content"] if final_return["output"] else None,
            "status": final_return["status"],
        }, indent=2) + "\n",
        encoding="utf-8",
    )
    artifact = {
        "run_id": packet["run_id"],
        "trace_id": trace_id,
        "status": final_return["status"],
        "start_time": provider_response["raw_timing"]["started_at"],
        "end_time": provider_response["raw_timing"]["completed_at"],
        "duration_ms": provider_response["raw_timing"]["duration_ms"],
        "provider": packet["provider_target"],
        "model": packet["model_target"],
        "request_summary": {
            "message_count": len(packet["normalized_messages"]),
            "roles": [m["role"] for m in packet["normalized_messages"]],
            "content_preview": packet["normalized_messages"][-1]["content"][:160],
        },
        "response_summary": {
            "output_preview": (final_return["output"] or {}).get("content"),
            "status": final_return["status"],
        },
        "error_summary": final_return["error"],
        "usage": provider_response.get("usage"),
        "paths": {
            "trace_log_path": str(trace_path),
            "transcript_path": str(transcript_path),
        },
        "contracts": {
            "canonical_packet": packet,
            "provider_request": provider_request,
            "provider_response": provider_response,
            "openclaw_return": final_return,
        },
    }
    return _write_json(evidence_path, artifact)


def run_pipeline(ingress: dict[str, Any], *, runtime_root: str | Path, adapter: MockProviderAdapter | None = None) -> dict[str, Any]:
    runtime_root = Path(runtime_root)
    adapter = adapter or MockProviderAdapter()
    try:
        validated = validate_ingress(ingress)
        packet = build_packet(validated)
        provider_request = build_provider_request(packet)
        provider_response = adapter.invoke(provider_request)
        final_return = build_return(provider_response, evidence_path="pending")
        evidence_path = write_evidence(runtime_root, packet, provider_request, provider_response, final_return)
        final_return["evidence"]["artifact_path"] = evidence_path
        return final_return
    except GanglionError as exc:
        trace_id = f"trace_{datetime.now(timezone.utc).strftime('%Y%m%d')}_{uuid.uuid4().hex[:12]}"
        run_id = f"run_{datetime.now(timezone.utc).strftime('%Y%m%d')}_{uuid.uuid4().hex[:12]}"
        final_return = {
            "trace_id": trace_id,
            "run_id": run_id,
            "status": "error",
            "output": None,
            "provider": {"name": ingress.get("provider_hint", "openai"), "model": ingress.get("model_hint", "gpt-5.4")},
            "usage": None,
            "evidence": {"written": True, "artifact_path": "pending"},
            "error": exc.to_dict(),
        }
        evidence_path = _write_json(runtime_root / "evidence" / f"{_stamp()}_{trace_id}_run.json", {
            "run_id": run_id,
            "trace_id": trace_id,
            "status": "error",
            "start_time": utc_now(),
            "end_time": utc_now(),
            "duration_ms": 0,
            "provider": ingress.get("provider_hint", "openai"),
            "model": ingress.get("model_hint", "gpt-5.4"),
            "request_summary": None,
            "response_summary": {"output_preview": None, "status": "error"},
            "error_summary": exc.to_dict(),
            "usage": None,
            "paths": {"trace_log_path": None},
            "contracts": {"openclaw_return": final_return},
        })
        final_return["evidence"]["artifact_path"] = evidence_path
        return final_return
