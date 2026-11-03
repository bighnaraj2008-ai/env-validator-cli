"""Core .env file parsing engine."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Union


@dataclass(frozen=True)
class ParsedEnv:
    """Outcome of parsing a ``.env`` file."""

    values: dict[str, str]
    source: str
    line_count: int


def parse_env_text(text: str, source: str = "<memory>") -> ParsedEnv:
    """Parse raw .env text into key-value pairs."""
    values: dict[str, str] = {}
    lines = text.splitlines()
    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].lstrip()
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in ("'", '"'):
            val = val[1:-1]
        if key:
            values[key] = val
    return ParsedEnv(values=values, source=source, line_count=len(lines))


def parse_env_file(path: Union[str, Path], *, encoding: str = "utf-8") -> ParsedEnv:
    """Parse a ``.env`` file into a :class:`ParsedEnv`."""
    p = Path(path)
    return parse_env_text(p.read_text(encoding=encoding), source=str(p))
