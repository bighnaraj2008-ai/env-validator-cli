"""Environment parsing throughput and files-per-second benchmark harness."""

from __future__ import annotations

import argparse
import json
import sys
import time
import tracemalloc
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.validator.parser import parse_env_text  # noqa: E402


def run_benchmark(files: int = 100, lines: int = 50) -> dict:
    sample = "\n".join(f"APP_VAR_{i}=synthetic_val_{i}" for i in range(lines))
    tracemalloc.start()
    t0 = time.perf_counter()
    for i in range(files):
        parse_env_text(sample, source=f"bench_{i}.env")
    duration = time.perf_counter() - t0
    _, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    fps = files / duration if duration > 0 else 0.0
    return {
        "files_count": files,
        "lines_per_file": lines,
        "duration_seconds": round(duration, 4),
        "files_per_second": round(fps, 2),
        "peak_memory_kb": round(peak_mem / 1024, 2),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parser throughput benchmark")
    parser.add_argument("--files", type=int, default=100)
    parser.add_argument("--lines", type=int, default=50)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    metrics = run_benchmark(files=args.files, lines=args.lines)
    if args.json:
        print(json.dumps(metrics, indent=2))
    else:
        msg = (
            f"Processed {metrics['files_count']} files in "
            f"{metrics['duration_seconds']}s ({metrics['files_per_second']} files/s)"
        )
        print(msg)
