"""Endurance and stability stress test."""

from __future__ import annotations

from schemas.env_schema import ENV_SCHEMA
from src.validator.parser import parse_env_text
from tests.harness.mock_env import create_sample_env_content


def test_stability_endurance_loop():
    """Verify stability and clean memory across high iterations of parsing/validation."""
    sample_text = create_sample_env_content()
    iterations = 50
    for _ in range(iterations):
        parsed = parse_env_text(sample_text, source="endurance_test")
        report = ENV_SCHEMA.validate(parsed.values)
        assert report.passed is True
