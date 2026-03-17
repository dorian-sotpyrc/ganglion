from __future__ import annotations

from pathlib import Path
import json

from ganglion.antennule.integration_contract import normalise_envelope
from ganglion.antennule.openclaw_adapter import handle_openclaw_request
from ganglion.carapace.deployment import DeploymentManager
from ganglion.shellbank.exports import BrainExportService
from ganglion.shellbank.retention import RetentionPolicy


def repo_root() -> Path:
    return Path.cwd()


def load_fixture(name: str) -> dict:
    return json.loads((repo_root() / "tests" / "fixtures" / "step7a" / name).read_text(encoding="utf-8"))


def test_envelope_normalisation() -> None:
    env = normalise_envelope(load_fixture("request_normal.json"))
    assert env.request_id == "req-fixture-normal"
    assert env.agent_key == "surgeon"


def test_integration_ready_openclaw_path() -> None:
    result = handle_openclaw_request(repo_root(), load_fixture("request_confidential.json"))
    assert result["status"] == "ok"
    assert result["request_id"] == "req-fixture-confidential"
    assert result["metadata"]["classification"]["confidentiality"] == "confidential"


def test_export_import_roundtrip() -> None:
    svc = BrainExportService()
    export_dir = svc.export_brain("surgeon", repo_root() / "brains" / "agents" / "surgeon")
    imported = svc.import_brain(export_dir, repo_root() / "artifacts" / "integration" / "surgeon_import_test")
    assert export_dir.exists()
    assert imported.exists()
    assert (imported / "manifest.json").exists()


def test_deployment_record_and_rollback() -> None:
    mgr = DeploymentManager()
    mgr.record_deployment("surgeon", "v-test", "chk-123")
    active = mgr.read_active("surgeon")
    assert active["version"] == "v-test"
    rollback = mgr.rollback("surgeon", "v-prev", "chk-prev")
    assert rollback.exists()


def test_retention_policy_runs() -> None:
    policy = RetentionPolicy(repo_root() / "artifacts" / "runs")
    removed = policy.prune_to_latest(keep_latest=100)
    assert isinstance(removed, list)
