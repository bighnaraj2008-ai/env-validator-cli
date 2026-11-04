"""Stress testing suite for massive environment files and edge payloads."""

from __future__ import annotations

from src.validator.parser import parse_env_text


def test_high_volume_variable_storm():
    """Verify parser stability with 5,000 distinct variables."""
    payload = "\n".join(f"VAR_{idx}=storm_payload_{idx}" for idx in range(5000))
    result = parse_env_text(payload)
    assert len(result.values) == 5000
    assert result.values["VAR_4999"] == "storm_payload_4999"


def test_large_value_payload():
    """Verify parsing values with extensive characters up to 100KB."""
    large_val = "x" * 100_000
    text = f"LARGE_PAYLOAD={large_val}\n"
    result = parse_env_text(text)
    assert result.values["LARGE_PAYLOAD"] == large_val
