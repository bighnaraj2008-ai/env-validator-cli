"""Duplicate environment key handling and conflict resolution tests."""

from __future__ import annotations

from src.validator.parser import parse_env_text


def test_duplicate_keys_resolve_to_last_value():
    """Parser telemetry should keep the final declaration (dict semantics)."""
    text = "DUP_KEY=first_value\nOTHER=keep\nDUP_KEY=second_value\n"
    parsed = parse_env_text(text)
    assert parsed.values["DUP_KEY"] == "second_value"
    assert parsed.values["OTHER"] == "keep"


def test_multiple_duplicate_keys_override_sequentially():
    """Multiple redeclarations of the same key cascade to the last value."""
    text = "CONFIG_TIER=dev\nCONFIG_TIER=stage\nCONFIG_TIER=prod\n"
    parsed = parse_env_text(text)
    assert parsed.values["CONFIG_TIER"] == "prod"
    assert parsed.line_count == 3


def test_duplicate_keys_with_whitespace_variations():
    """Keys with identical stripped names override each other."""
    text = "TARGET_HOST = host1\nTARGET_HOST=host2\n"
    parsed = parse_env_text(text)
    assert parsed.values["TARGET_HOST"] == "host2"
