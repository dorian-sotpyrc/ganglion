from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ganglion.antennule.request_adapter import RunRequest
from ganglion.axon.router import RoutingDecision, select_route
from ganglion.mandible.response_processor import RunResponse, process_response
from ganglion.peduncle.provider_adapter import ProviderAdapter
from ganglion.pleon.classifier import TaskClassification, classify_task
from ganglion.shellbank.artifacts import ArtifactWriter
from ganglion.supra.compiler import compile_brain
from ganglion.ventral.service import MemoryService


@dataclass(frozen=True)
class RuntimePackage:
    agent_key: str
    session_id: str
    compiled_checksum: str
    compiled_text: str
    execution_note: str
    classification: TaskClassification
    routing: RoutingDecision
    memory_bundle: dict


class Orchestrator:
    def __init__(self, repo_root: str | Path) -> None:
        self.repo_root = Path(repo_root)
        self.provider_adapter = ProviderAdapter()
        self.memory_service = MemoryService()
        self.artifact_writer = ArtifactWriter(self.repo_root / "artifacts")

    def build_runtime_package(self, request: RunRequest) -> RuntimePackage:
        compiled = compile_brain(self.repo_root, request.agent_key)
        classification = classify_task(request.task_text, request.risk_hint)
        routing = select_route(
            classification=classification,
            requested_lane=request.requested_mode,
            requested_provider=request.raw_payload.get("requested_provider"),
            requested_model=request.raw_payload.get("requested_model"),
        )
        memory_bundle = self.memory_service.memory_bundle(
            request.agent_key,
            request.task_text,
            request.session_messages,
        )
        execution_note = (
            f"Prepared routed execution for agent={request.agent_key} "
            f"session={request.session_id} lane={routing.lane}"
        )
        return RuntimePackage(
            agent_key=request.agent_key,
            session_id=request.session_id,
            compiled_checksum=compiled.checksum,
            compiled_text=compiled.compiled_text,
            execution_note=execution_note,
            classification=classification,
            routing=routing,
            memory_bundle=memory_bundle,
        )

    def run(self, request: RunRequest) -> RunResponse:
        runtime = self.build_runtime_package(request)
        provider_result = self.provider_adapter.invoke(
            provider=runtime.routing.provider,
            model=runtime.routing.model,
            prompt=request.task_text,
            fallback_provider=runtime.routing.fallback_provider,
            fallback_model=runtime.routing.fallback_model,
        )

        message = (
            f"Prepared execution for {request.agent_key}. "
            f"Route: {provider_result.provider}/{provider_result.model}. "
            f"Task: {request.task_text}"
        )

        artifact_path = self.artifact_writer.write_run_artifact(
            run_id=request.session_id,
            payload={
                "agent_key": request.agent_key,
                "task_text": request.task_text,
                "compiled_checksum": runtime.compiled_checksum,
                "routing": {
                    "lane": runtime.routing.lane,
                    "provider": provider_result.provider,
                    "model": provider_result.model,
                    "used_fallback": provider_result.used_fallback,
                },
                "memory": {
                    "critical_count": len(runtime.memory_bundle["critical"]),
                    "episodic_count": len(runtime.memory_bundle["episodic"]),
                    "session_summary": runtime.memory_bundle["session_summary"],
                },
            },
        )

        return process_response(
            agent_key=request.agent_key,
            session_id=request.session_id,
            compiled_checksum=runtime.compiled_checksum,
            compiled_text=runtime.compiled_text,
            message=message,
            metadata={
                "execution_note": runtime.execution_note,
                "mode": "routed-mock",
                "classification": {
                    "complexity": runtime.classification.complexity,
                    "confidentiality": runtime.classification.confidentiality,
                    "risk": runtime.classification.risk,
                    "reasons": runtime.classification.reasons,
                },
                "routing": {
                    "lane": runtime.routing.lane,
                    "provider": provider_result.provider,
                    "model": provider_result.model,
                    "override_applied": runtime.routing.override_applied,
                    "routing_reason": runtime.routing.routing_reason,
                    "used_fallback": provider_result.used_fallback,
                    "fallback_provider": runtime.routing.fallback_provider,
                    "fallback_model": runtime.routing.fallback_model,
                },
                "memory": {
                    "critical": [m.text for m in runtime.memory_bundle["critical"]],
                    "episodic": [m.text for m in runtime.memory_bundle["episodic"]],
                    "session_summary": runtime.memory_bundle["session_summary"],
                },
                "artifact_path": str(artifact_path),
            },
        )
