from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ganglion.antennule.request_adapter import RunRequest
from ganglion.mandible.response_processor import RunResponse, process_response
from ganglion.supra.compiler import compile_brain


@dataclass(frozen=True)
class RuntimePackage:
    agent_key: str
    session_id: str
    compiled_checksum: str
    compiled_text: str
    execution_note: str


class Orchestrator:
    def __init__(self, repo_root: str | Path) -> None:
        self.repo_root = Path(repo_root)

    def build_runtime_package(self, request: RunRequest) -> RuntimePackage:
        compiled = compile_brain(self.repo_root, request.agent_key)
        execution_note = (
            f"Mock run prepared for agent={request.agent_key} "
            f"session={request.session_id} channel={request.channel_type}"
        )
        return RuntimePackage(
            agent_key=request.agent_key,
            session_id=request.session_id,
            compiled_checksum=compiled.checksum,
            compiled_text=compiled.compiled_text,
            execution_note=execution_note,
        )

    def run(self, request: RunRequest) -> RunResponse:
        runtime = self.build_runtime_package(request)
        message = (
            f"Prepared mocked execution for {request.agent_key}. "
            f"Task: {request.task_text}"
        )
        return process_response(
            agent_key=request.agent_key,
            session_id=request.session_id,
            compiled_checksum=runtime.compiled_checksum,
            compiled_text=runtime.compiled_text,
            message=message,
            metadata={
                "execution_note": runtime.execution_note,
                "mode": "mock",
            },
        )
