"""Mock environment file fixture helper for unit and CLI tests."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping


def write_temp_env(directory: Path, variables: Mapping[str, str], filename: str = ".env.mock") -> Path:
    """Write a temporary key=value environment file inside ``directory`` and return its path."""
    target = directory / filename
    lines = [f"{key}={val}" for key, val in variables.items()]
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return target
