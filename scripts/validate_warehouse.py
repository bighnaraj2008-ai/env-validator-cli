"""Repository health and validation integrity check utility."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent


def validate_repository_integrity() -> int:
    required = [
        "README.md",
        "LICENSE",
        "CHANGELOG.md",
        "pyproject.toml",
        ".flake8",
        "schemas/env_schema.yaml",
        "tests/benchmarks/bench_parser.py",
    ]
    missing = [f for f in required if not (REPO_ROOT / f).exists()]
    if missing:
        print(f"Integrity check failed: missing {missing}")
        return 1
    print("All core repository assets verified successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(validate_repository_integrity())
