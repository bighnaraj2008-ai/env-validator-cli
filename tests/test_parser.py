"""Unit tests for the .env file parser module."""

import pytest

from src.config.errors import EnvFileNotFoundError, EnvParseError
from src.validator.parser import parse_env_file, parse_env_text


def test_parse_valid_env_text_strips_comments_export_and_quotes():
    text = """
    # Database configuration
    export APP_NAME="MyApp"
    PORT=8080
    SECRET='s3cr3t=with=equals'
    """
    parsed = parse_env_text(text)
    assert parsed.values["APP_NAME"] == "MyApp"
    assert parsed.values["PORT"] == "8080"
    assert parsed.values["SECRET"] == "s3cr3t=with=equals"


def test_parse_missing_file_raises_not_found(tmp_path):
    with pytest.raises(EnvFileNotFoundError):
        parse_env_file(tmp_path / "does_not_exist.env")


def test_parse_malformed_line_raises_parse_error():
    with pytest.raises(EnvParseError):
        parse_env_text("INVALID_LINE_WITHOUT_EQUALS")


def test_parse_empty_key_raises_parse_error():
    with pytest.raises(EnvParseError):
        parse_env_text("=value_without_key")


def test_parse_bom_and_file_roundtrip(tmp_path):
    env_file = tmp_path / ".env.test"
    env_file.write_text("\ufeffKEY_ONE=alpha\nKEY_TWO=beta\n", encoding="utf-8")
    parsed = parse_env_file(env_file)
    assert parsed.values == {"KEY_ONE": "alpha", "KEY_TWO": "beta"}
    assert parsed.line_count == 2
