""".env file parsing logic.

The parser is intentionally dependency-free: it reads a ``.env`` file line by
line, skips comments and blank lines, strips an optional ``export`` prefix,
splits on the first ``=``, and unquotes single/double-quoted values. The
result is a plain ``dict[str, str]`` consumed by the schema validation layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

from ..config.errors import EnvFileNotFoundError, EnvParseError


@dataclass(frozen=True)
class ParsedEnv:
    """Outcome of parsing a ``.env`` file."""

    values: dict[str, str]
    source: str
    line_count: int


def _strip_bom(text: str) -> str:
    """Remove a leading UTF-8 BOM if an editor wrote one into the file."""
    if text.startswith("\ufeff"):
        return text[len("\ufeff"):]
    return text


def _unquote(value: str) -> str:
    """Remove matching single or double quotes surrounding a value.

    Only strips quotes when the first and last characters are the same quote
    character. Inner quotes are preserved untouched (no escape processing),
    keeping the parser predictable and dependency-free.
    """
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


def parse_env_file(
    path: Union[str, Path],
    *,
    encoding: str = "utf-8",
) -> ParsedEnv:
    """Parse a ``.env`` file into a :class:`ParsedEnv`.

    Rules:
    * Blank lines and lines starting with ``#`` are ignored.
    * A leading ``export `` prefix is stripped.
    * The key is everything before the first ``=``; the value is the rest.
    * Surrounding matching quotes on the value are removed.

    Raises:
        EnvFileNotFoundError: if the file does not exist.
        EnvParseError: if a non-comment line lacks an ``=`` separator or has
            an empty key.
    """
    path = Path(path)
    if not path.exists():
        raise EnvFileNotFoundError(
            f"Environment file not found: {path}", key=None
        )

    values: dict[str, str] = {}
    line_count = 0

    try:
        text = path.read_text(encoding=encoding)
    except OSError as exc:
        raise EnvFileNotFoundError(
            f"Cannot read environment file '{path}': {exc}", key=None
        ) from exc

    text = _strip_bom(text)

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line_count += 1
        line = raw_line.strip()

        # Skip blank lines and comments.
        if not line or line.startswith("#"):
            continue

        # Support ``export KEY=value`` shell-style declarations.
        if line.startswith("export "):
            line = line[len("export ") :].lstrip()

        if "=" not in line:
            raise EnvParseError(
                f"Malformed line {line_number} in '{path}': missing '=' separator",
                key=None,
            )

        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()

        if not key:
            raise EnvParseError(
                f"Malformed line {line_number} in '{path}': empty variable name",
                key=None,
            )

        values[key] = _unquote(value)

    return ParsedEnv(values=values, source=str(path), line_count=line_count)


def parse_env_text(
    text: str,
    *,
    source: Optional[str] = None,
) -> ParsedEnv:
    """Parse ``.env`` formatted text (handy for tests and inline config)."""
    values_dict: dict[str, str] = {}
    line_count = 0
    text = _strip_bom(text)

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line_count += 1
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].lstrip()
        if "=" not in line:
            origin = f" in '{source}'" if source else ""
            raise EnvParseError(
                f"Malformed line {line_number}{origin}: missing '=' separator",
                key=None,
            )
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if not key:
            origin = f" in '{source}'" if source else ""
            raise EnvParseError(
                f"Malformed line {line_number}{origin}: empty variable name",
                key=None,
            )
        values_dict[key] = _unquote(value)

    return ParsedEnv(values=values_dict, source=source or "<text>", line_count=line_count)
