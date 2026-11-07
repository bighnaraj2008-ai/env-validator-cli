"""Memory allocation footprint benchmarking utility for CLI parsing and validation."""

from __future__ import annotations

import argparse
import json
import sys
import tracemalloc
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from schemas.env_schema import ENV_SCHEMA  # noqa: E402
from src.validator.parser import parse_env_text  # noqa: E402


def benchmark_memory_footprint(cycles: int = 100) -> dict:
    text = "\n".join([
        "APP_NAME=BenchApp",
        "PORT=8080",
        "DEBUG=true",
        "SECRET_KEY=longsecretsigningkey12345",
    ])
    tracemalloc.start()
    initial_current, _ = tracemalloc.get_traced_memory()

    for _ in range(cycles):
        parsed = parse_env_text(text, source="bench_memory.env")
        ENV_SCHEMA.validate(parsed.values)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "cycles": cycles,
        "baseline_kb": round(initial_current / 1024, 2),
        "peak_memory_kb": round(peak / 1024, 2),
        "memory_retained_kb": round((current - initial_current) / 1024, 2),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cycles", type=int, default=100)
    args = parser.parse_args()
    report = benchmark_memory_footprint(args.cycles)
    print(json.dumps(report, indent=2))
