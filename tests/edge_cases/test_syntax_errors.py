"""Syntax error and special character edge-case tests for env parser."""

from __future__ import annotations

import pytest
from src.config.errors import EnvParseError
from src.validator.parser import parse_env_text


def test_unquoted_special_characters_are_preserved():
    """Values containing '=', nested quotes, and surrounding whitespace."""
    text = "KEY=value=with=equals\nQUOTED='single=double=mixed'\nSPACES=  padded  \nEMPTY=\n"
    parsed = parse_env_text(text)
    assert parsed.values["KEY"] == "value=with=equals"
    assert parsed.values["QUOTED"] == "single=double=mixed"
    assert parsed.values["SPACES"] == "padded"
    assert parsed.values["EMPTY"] == ""


def test_comment_and_blank_lines_do_not_pollute_telemetry():
    """Verify comments and blank lines are ignored while retaining line count."""
    text = "\n# Database section\n  \nPORT=8080\n# end\n"
    parsed = parse_env_text(text)
    assert parsed.values == {"PORT": "8080"}
    assert parsed.line_count == 5


def test_export_prefix_is_stripped():
    """Verify export prefix is handled cleanly across declarations."""
    text = "export APP_NAME=FromExport\nPORT=9000\n"
    parsed = parse_env_text(text)
    assert parsed.values["APP_NAME"] == "FromExport"
    assert parsed.values["PORT"] == "9000"


def test_malformed_text_raises_parse_error():
    """Malformed syntax missing equals or key must raise EnvParseError."""
    with pytest.raises(EnvParseError):
        parse_env_text("THIS_LINE_HAS_NO_EQUALS_SIGN")

    with pytest.raises(EnvParseError):
        parse_env_text("=value_without_key_name")
