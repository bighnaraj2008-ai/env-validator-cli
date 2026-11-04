"""Test configuration constants and benchmark thresholds."""

from __future__ import annotations

DEFAULT_TEST_TIMEOUT_SECONDS = 5.0
MAX_PARSER_LATENCY_MS = 250.0
MAX_MEMORY_THRESHOLD_MB = 15.0
PERF_BENCHMARK_ITERATIONS = 2000

TEST_SCHEMA_MINIMAL = {
    "APP_NAME": {"type": "string", "required": True},
    "PORT": {"type": "integer", "required": True},
    "DEBUG": {"type": "boolean", "required": False},
}
