"""Basic environment parsing throughput benchmark harness."""

from __future__ import annotations

import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.validator.parser import parse_env_text  # noqa: E402


def benchmark_parser_throughput(iterations: int = 50) -> dict:
    sample_text = "\n".join(f"KEY_{i}=value_{i}" for i in range(100))
    start = time.perf_counter()
    for _ in range(iterations):
        parse_env_text(sample_text, source="bench")
    elapsed = time.perf_counter() - start
    return {"iterations": iterations, "elapsed_seconds": elapsed}


if __name__ == "__main__":
    res = benchmark_parser_throughput()
    print(f"Completed {res['iterations']} iterations in {res['elapsed_seconds']:.4f}s")
