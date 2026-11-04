"""Fixture-driven tests.

Validates the parser's output (telemetry structure: values, source, line
count) against the mock fixtures in tests/fixtures/, then runs the parsed
values through ENV_SCHEMA to prove injected anomalies are caught.
"""

from __future__ import annotations

import pytest
from pathlib import Path

from schemas.env_schema import ENV_SCHEMA
from src.config.errors import EnvParseError
from src.validator.parser import parse_env_file

FIXTURES_DIR = Path(__file__).parent / "fixtures"

VALID_ENV_KEYS = {
    "APP_NAME",
    "APP_ENV",
    "PORT",
    "DEBUG",
    "SECRET_KEY",
    "JWT_SECRET",
    "DATABASE_URL",
    "REDIS_URL",
    "API_KEY",
    "SENTRY_DSN",
}


def test_valid_env_parses_to_expected_telemetry():
    parsed = parse_env_file(FIXTURES_DIR / "valid.env")

    # Telemetry structure assertions.
    assert set(parsed.values) == VALID_ENV_KEYS
    assert parsed.source.endswith("tests/fixtures/valid.env") or parsed.source.endswith(
        "valid.env"
    )
    assert isinstance(parsed.line_count, int) and parsed.line_count > 0

    # Schema validation: a valid fixture must pass cleanly.
    report = ENV_SCHEMA.validate(parsed.values)
    assert report.passed is True
    assert len(report.errors) == 0
    assert len(report.warnings) == 0


def test_malformed_env_raises_parse_error():
    """Injected syntax errors must surface as EnvParseError, never silently."""
    with pytest.raises(EnvParseError):
        parse_env_file(FIXTURES_DIR / "malformed.env")


def test_missing_required_env_detected_by_schema():
    """A file that parses cleanly can still fail required-field validation."""
    parsed = parse_env_file(FIXTURES_DIR / "missing_required.env")

    # Parser telemetry is well-formed even though the config is incomplete.
    assert "APP_NAME" in parsed.values
    assert "PORT" not in parsed.values

    report = ENV_SCHEMA.validate(parsed.values)
    assert report.passed is False
    missing_keys = {
        err.key for err in report.errors if err.code == "missing"
    }
    expected_missing = {"PORT", "JWT_SECRET", "DATABASE_URL", "REDIS_URL"}
    assert expected_missing <= missing_keys, missing_keys
    for err in report.errors:
        if err.code == "missing":
            assert err.severity == "error"
            assert err.actual == "<missing>"


def test_invalid_types_env_detected_by_schema():
    """Type, pattern, and length violations must each produce an error."""
    parsed = parse_env_file(FIXTURES_DIR / "invalid_types.env")
    assert "APP_NAME" in parsed.values  # file still parses

    report = ENV_SCHEMA.validate(parsed.values)
    assert report.passed is False
    error_codes = {(err.key, err.code) for err in report.errors}

    assert ("APP_ENV", "pattern_mismatch") in error_codes
    assert ("PORT", "type_mismatch") in error_codes
    assert ("DEBUG", "type_mismatch") in error_codes
    assert ("SECRET_KEY", "too_short") in error_codes
    assert ("DATABASE_URL", "pattern_mismatch") in error_codes
    assert ("REDIS_URL", "pattern_mismatch") in error_codes

    # Every schema error carries expected/actual telemetry.
    for err in report.errors:
        assert err.expected is not None
        assert err.actual is not None
