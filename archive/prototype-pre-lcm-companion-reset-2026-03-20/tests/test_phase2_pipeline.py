from __future__ import annotations

import json
from pathlib import Path

from ganglion.pipeline import MockProviderAdapter, run_pipeline


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def test_phase2_success_writes_evidence(tmp_path: Path) -> None:
    ingress = json.loads((FIXTURES / "phase2_ingress_success.json").read_text())
    result = run_pipeline(ingress, runtime_root=tmp_path, adapter=MockProviderAdapter(mode="success", response_text="__ECHO__"))
    assert result["status"] == "success"
    assert result["output"]["content"] == "Echo: Ping Ganglion"
    evidence_path = Path(result["evidence"]["artifact_path"])
    assert evidence_path.exists()
    evidence = json.loads(evidence_path.read_text())
    assert evidence["contracts"]["canonical_packet"]["packet_version"] == "v1alpha1"
    assert evidence["contracts"]["provider_request"]["provider"] == "openai"
    assert evidence["contracts"]["provider_response"]["status"] == "success"
    assert evidence["contracts"]["openclaw_return"]["status"] == "success"


def test_phase2_invalid_ingress_returns_structured_error(tmp_path: Path) -> None:
    ingress = json.loads((FIXTURES / "phase2_ingress_invalid.json").read_text())
    result = run_pipeline(ingress, runtime_root=tmp_path)
    assert result["status"] == "error"
    assert result["error"]["type"] == "ingress_error"
    assert Path(result["evidence"]["artifact_path"]).exists()


def test_phase2_provider_error_maps_to_openclaw_error(tmp_path: Path) -> None:
    ingress = json.loads((FIXTURES / "phase2_ingress_success.json").read_text())
    result = run_pipeline(ingress, runtime_root=tmp_path, adapter=MockProviderAdapter(mode="error"))
    assert result["status"] == "error"
    assert result["error"]["type"] == "provider_transport_error"
