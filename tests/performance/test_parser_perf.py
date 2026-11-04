"""Performance benchmark test for high-volume .env file parsing."""

from __future__ import annotations

import time
from src.validator.parser import parse_env_text


def test_parser_throughput_large_payload():
    """Verify that 2,000 environment lines parse in under 500ms."""
    lines = [f"KEY_{i}=value_string_{i}_data" for i in range(2000)]
    payload = "\n".join(lines)

    start = time.perf_counter()
    result = parse_env_text(payload)
    duration = time.perf_counter() - start

    assert len(result.values) == 2000
    assert result.line_count == 2000
    assert duration < 0.50, f"Parsing took too long: {duration:.4f}s"
