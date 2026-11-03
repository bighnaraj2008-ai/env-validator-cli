"""Command-line interface module for env-validator-cli."""

from __future__ import annotations

from typing import Optional, Sequence

from main import build_parser, load_schema, main as _main, run_comparison

__all__ = ["build_parser", "load_schema", "run_comparison", "main"]


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Invoke the CLI entrypoint with optional explicit argument list."""
    return _main(argv)
