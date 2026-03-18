from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ganglion.antennule.request_adapter import RunRequest
from ganglion.axon.router import RoutingDecision, select_route
from ganglion.carapace.deployment import DeploymentManager
from ganglion.eyestalk.costs import estimate_cost
from ganglion.mandible.response_processor import RunResponse, process_response
from ganglion.peduncle.provider_adapter import ProviderAdapter
from ganglion.pleon.classifier import TaskClassification, classify_task
from ganglion.shellbank.artifacts import ArtifactWriter
from ganglion.supra.compiler import compile_brain
from ganglion.tracer.models import TraceBundle
from ganglion.tracer.service import TraceWriter, make_step
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
        self.memory_service = MemoryService(self.repo_root)
        self.artifact_writer = ArtifactWriter(self.repo_root / "artifacts")
        self.deployment_manager = DeploymentManager(self.repo_root / "artifacts" / "deployments")
        self.trace_writer = TraceWriter(self.repo_root / "artifacts" / "traces")

    def build_runtime_package(self, request: RunRequest) -> RuntimePackage:
        compiled = compile_brain(self.repo_root, request.agent_key)
        self.deployment_manager.record_deployment(
            agent_key=request.agent_key,
            version="runtime-current",
            checksum=compiled.checksum,
        )

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
        request_id = str(request.raw_payload.get("request_id", request.session_id))
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

        cost = estimate_cost(
            provider=provider_result.provider,
            model=provider_result.model,
            task_text=request.task_text,
            response_text=message,
            latency_ms=1200 if not provider_result.used_fallback else 1800,
        )

        run_payload = {
            "request_id": request_id,
            "agent_key": request.agent_key,
            "task_text": request.task_text,
            "compiled_checksum": runtime.compiled_checksum,
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
                "used_fallback": provider_result.used_fallback,
                "override_applied": runtime.routing.override_applied,
                "routing_reason": runtime.routing.routing_reason,
            },
            "memory": {
                "critical_count": len(runtime.memory_bundle["critical"]),
                "episodic_count": len(runtime.memory_bundle["episodic"]),
                "session_summary": runtime.memory_bundle["session_summary"],
            },
            "cost": {
                "provider": cost.provider,
                "model": cost.model,
                "estimated_input_tokens": cost.estimated_input_tokens,
                "estimated_output_tokens": cost.estimated_output_tokens,
                "estimated_cost_usd": cost.estimated_cost_usd,
                "latency_ms": cost.latency_ms,
            },
        }

        artifact_path = self.artifact_writer.write_run_artifact(
            run_id=request.session_id,
            payload=run_payload,
        )

        trace = TraceBundle(
            request_id=request_id,
            agent_key=request.agent_key,
            session_id=request.session_id,
            input_summary={
                "task_text": request.task_text,
                "channel_type": request.channel_type,
                "channel_id": request.channel_id,
                "requested_model": request.raw_payload.get("requested_model"),
                "requested_provider": request.raw_payload.get("requested_provider"),
                "requested_lane": request.requested_mode,
            },
            steps=[
                make_step(
                    "brain_compile",
                    "Compiled active brain from disk",
                    {
                        "compiled_checksum": runtime.compiled_checksum,
                        "compiled_length_chars": len(runtime.compiled_text),
                    },
                ),
                make_step(
                    "classification",
                    "Classified task complexity, confidentiality, and risk",
                    {
                        "complexity": runtime.classification.complexity,
                        "confidentiality": runtime.classification.confidentiality,
                        "risk": runtime.classification.risk,
                        "reasons": runtime.classification.reasons,
                    },
                ),
                make_step(
                    "memory_selection",
                    "Selected critical and episodic memory",
                    {
                        "critical_count": len(runtime.memory_bundle["critical"]),
                        "episodic_count": len(runtime.memory_bundle["episodic"]),
                        "session_summary": runtime.memory_bundle["session_summary"],
                    },
                ),
                make_step(
                    "routing",
                    "Selected provider/model lane",
                    {
                        "lane": runtime.routing.lane,
                        "provider": provider_result.provider,
                        "model": provider_result.model,
                        "override_applied": runtime.routing.override_applied,
                        "used_fallback": provider_result.used_fallback,
                        "routing_reason": runtime.routing.routing_reason,
                    },
                ),
                make_step(
                    "costing",
                    "Estimated latency, token usage, and cost",
                    {
                        "estimated_input_tokens": cost.estimated_input_tokens,
                        "estimated_output_tokens": cost.estimated_output_tokens,
                        "estimated_cost_usd": cost.estimated_cost_usd,
                        "latency_ms": cost.latency_ms,
                    },
                ),
                make_step(
                    "artifact_capture",
                    "Persisted run artifact",
                    {
                        "artifact_path": str(artifact_path),
                    },
                ),
            ],
            output_summary={
                "message": message,
                "artifact_path": str(artifact_path),
            },
        )
        trace_path = self.trace_writer.write_trace(trace)

        return process_response(
            agent_key=request.agent_key,
            session_id=request.session_id,
            compiled_checksum=runtime.compiled_checksum,
            compiled_text=runtime.compiled_text,
            message=message,
            metadata={
                "execution_note": runtime.execution_note,
                "mode": "integration-ready-routed-mock",
                "classification": run_payload["classification"],
                "routing": run_payload["routing"],
                "memory": {
                    "critical": [m.text for m in runtime.memory_bundle["critical"]],
                    "episodic": [m.text for m in runtime.memory_bundle["episodic"]],
                    "session_summary": runtime.memory_bundle["session_summary"],
                },
                "cost": run_payload["cost"],
                "artifact_path": str(artifact_path),
                "trace_path": str(trace_path),
            },
        )
