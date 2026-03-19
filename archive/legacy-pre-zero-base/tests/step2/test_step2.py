from __future__ import annotations

from pathlib import Path

import pytest

from ganglion.carapace.manifests import ManifestError, load_manifest
from ganglion.carapace.registry import BrainRegistry
from ganglion.supra.compiler import compile_brain


def repo_root() -> Path:
    return Path.cwd()


def test_shared_and_agent_brain_load() -> None:
    registry = BrainRegistry(repo_root())
    record = registry.get_active_brain("surgeon")
    assert record.manifest.agent_key == "surgeon"
    assert record.manifest.status == "active"


def test_overlay_precedence_is_deterministic() -> None:
    compiled = compile_brain(repo_root(), "surgeon")
    assert compiled.sections["identity"] == "You are the surgeon brain for high-risk OpenClaw and system work."
    assert compiled.sections["style"] == "Be exact, auditable, and conservative with changes."
    assert compiled.sections["constraints"] == "Prefer precise, verified, structured output."
    assert compiled.section_sources["identity"].endswith("brains/agents/surgeon/core/identity.md")
    assert compiled.section_sources["constraints"].endswith("brains/shared/core/constraints.md")


def test_invalid_manifest_fails_clearly() -> None:
    with pytest.raises(ManifestError):
        load_manifest(repo_root() / "tests/fixtures/invalid_brain/manifest.json")


def test_checksum_is_stable() -> None:
    a = compile_brain(repo_root(), "surgeon")
    b = compile_brain(repo_root(), "surgeon")
    assert a.checksum == b.checksum
    assert a.compiled_text == b.compiled_text
