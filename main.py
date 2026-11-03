#!/usr/bin/env python3
"""env-validator-cli — strict .env validation CLI.

Day 1 refactor entry point. Delegates to modular components:

* :mod:`src.validator.parser`     — .env parsing
* :mod:`src.validator.schema`     — schema engine + validation report
* :mod:`src.validator.rules`      — required / type / pattern / length rules
* :mod:`src.validator.reporter`   — console + JSON reporting
* :mod:`src.config.settings`      -- validation configuration
* :mod:`schemas.env_schema`       — default schema template

Run:

    python main.py                        # strict schema validation
    python main.py --env .env --strict    # fail on undeclared keys too
    python main.py --compare-example      # legacy key-sync check vs .env.example
    python main.py --format json          # machine-readable output

Exit codes: 0 = valid, 1 = validation failed, 2 = usage/error.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

# Allow running both as `python main.py` from the repo root and as an
# installed package (``python -m env_validator_cli``).
try:  # package-style imports
    from src.config.errors import EnvValidationError
    from src.config.settings import ValidationConfig
    from src.validator.parser import parse_env_file
    from src.validator.reporter import ConsoleReporter, ReportFormat
    from src.validator.schema import Schema
    from schemas.env_schema import SchemaCatalog
except ImportError:  # pragma: no cover - fallback when src/ is not on sys.path
    import sys as _sys

    _sys.path.insert(0, str(Path(__file__).resolve().parent))
    from src.config.errors import EnvValidationError  # type: ignore[no-redef]
    from src.config.settings import ValidationConfig  # type: ignore[no-redef]
    from src.validator.parser import parse_env_file  # type: ignore[no-redef]
    from src.validator.reporter import (  # type: ignore[no-redef]
        ConsoleReporter,
        ReportFormat,
    )
    from src.validator.schema import Schema  # type: ignore[no-redef]
    from schemas.env_schema import SchemaCatalog  # type: ignore[no-redef]


def _ensure_console_output() -> None:
    """Replace unsupported console characters instead of crashing (e.g. cp1252)."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(
                    encoding=stream.encoding or "utf-8", errors="replace"
                )
            except Exception:  # pragma: no cover - defensive
                pass


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="env-validator-cli",
        description="Validate .env configuration against a strict schema.",
    )
    parser.add_argument(
        "--env",
        default=".env",
        help="Path to the .env file to validate (default: .env)",
    )
    parser.add_argument(
        "--schema",
        default="default",
        help="Schema template name to use (default: default). "
        "Available templates: %(choices)s",
    )
    parser.add_argument(
        "--list-schemas",
        action="store_true",
        help="List available schema templates and exit.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on environment keys not declared in the schema",
    )
    parser.add_argument(
        "--format",
        default="text",
        choices=[ReportFormat.TEXT, ReportFormat.JSON],
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--compare-example",
        action="store_true",
        help="Run the legacy key-sync check against .env.example",
    )
    parser.add_argument(
        "--example",
        default=".env.example",
        help="Path to the .env.example template (default: .env.example)",
    )
    return parser


def load_schema(schema_name: str) -> Schema:
    """Load a named schema template, raising a clear error on failure."""
    try:
        return SchemaCatalog.get(schema_name)
    except KeyError as exc:
        available = ", ".join(SchemaCatalog.names())
        raise EnvValidationError(
            f"Schema template '{schema_name}' not found. Available: {available}"
        ) from exc


def run_comparison(env_path: str, example_path: str) -> int:
    """Legacy behaviour: compare .env keys against .env.example keys."""
    try:
        env_values = parse_env_file(env_path).values
        example_values = parse_env_file(example_path).values
    except EnvValidationError as exc:
        print(f"❌ {exc}")
        return 2

    example_keys = set(example_values)
    local_keys = set(env_values)
    missing = example_keys - local_keys
    extra = local_keys - example_keys

    print("🔍 Scanning environment configuration...\n")
    if not missing and not extra:
        print("✅ Environment configuration is fully synchronized and valid!")
        return 0
    if missing:
        print(f"❌ Missing keys in your local .env: {sorted(missing)}")
    if extra:
        print(f"⚠️ Extra keys in your local .env not found in example: {sorted(extra)}")
    return 1


def main(argv: Optional[Sequence[str]] = None) -> int:
    _ensure_console_output()
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list_schemas:
        print("Available schema templates:")
        for name in SchemaCatalog.names():
            print(f"  - {name}")
        return 0

    config = ValidationConfig(
        env_file=args.env,
        strict=args.strict,
        compare_example=args.compare_example,
    )

    # Legacy compatibility mode: original key-sync behaviour.
    if args.compare_example:
        return run_comparison(args.env, args.example)

    # Default mode: strict schema validation.
    try:
        schema = load_schema(args.schema)
        parsed = parse_env_file(args.env)
    except EnvValidationError as exc:
        print(f"❌ {exc}")
        return 2

    report = schema.validate(parsed.values, config=config)
    reporter = ConsoleReporter(format=args.format)
    return reporter.report(report)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except EnvValidationError as exc:
        print(f"❌ {exc}", file=sys.stderr)
        raise SystemExit(2)
