"""Memory and execution time profiler script for env-validator-cli."""

from __future__ import annotations

from pathlib import Path
import sys
import time
import tracemalloc

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from schemas.env_schema import ENV_SCHEMA  # noqa: E402
from src.validator.parser import parse_env_text  # noqa: E402


def profile_pipeline(iterations: int = 1000) -> dict:
    sample_text = (
        "APP_NAME=ProfilerApp\nAPP_ENV=production\nPORT=8000\nDEBUG=false\n"
        "SECRET_KEY=prodsecret123\nJWT_SECRET=prodjwtsecret123\n"
        "DATABASE_URL=postgresql://db:5432/app\nREDIS_URL=redis://cache:6379/0\n"
        "API_KEY=prodapikey999\n"
    )

    tracemalloc.start()
    start_time = time.perf_counter()

    for _ in range(iterations):
        parsed = parse_env_text(sample_text)
        ENV_SCHEMA.validate(parsed.values)

    elapsed = time.perf_counter() - start_time
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "iterations": iterations,
        "elapsed_seconds": round(elapsed, 4),
        "ops_per_second": round(iterations / elapsed, 2),
        "peak_memory_kb": round(peak / 1024, 2),
    }


if __name__ == "__main__":
    stats = profile_pipeline()
    print("=" * 48)
    print("env-validator-cli Pipeline Performance Profile")
    print("=" * 48)
    for k, v in stats.items():
        print(f"  {k:<20}: {v}")
    print("=" * 48)
