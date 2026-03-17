from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, ValidationError


class BrainManifest(BaseModel):
    schema_version: Literal["1.0"] = "1.0"
    agent_key: str = Field(min_length=1)
    brain_key: str = Field(min_length=1)
    version: str = Field(min_length=1)
    extends: str | None = None
    status: Literal["draft", "active", "retired"] = "draft"


class ManifestError(ValueError):
    pass


def load_manifest(path: str | Path) -> BrainManifest:
    p = Path(path)
    if not p.exists():
        raise ManifestError(f"Manifest not found: {p}")
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ManifestError(f"Invalid manifest JSON: {p}") from e
    try:
        return BrainManifest.model_validate(data)
    except ValidationError as e:
        raise ManifestError(f"Manifest validation failed: {p}") from e
