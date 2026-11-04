"""Edge-case tests for boolean values and required parameter checks."""

from __future__ import annotations

from src.config.settings import EnvFieldSchema, EnvType
from src.validator.rules import RequiredRule, TypeCastRule


def test_boolean_cast_accepts_common_true_false_forms():
    """Verify boolean rule accepts standard true/false literal strings."""
    field = EnvFieldSchema(name="DEBUG", type=EnvType.BOOLEAN)
    for true_form in ("1", "true", "True", "TRUE", "t", "yes", "y", "on"):
        assert TypeCastRule().check("DEBUG", true_form, field).passed is True
    for false_form in ("0", "false", "False", "f", "no", "n", "off"):
        assert TypeCastRule().check("DEBUG", false_form, field).passed is True


def test_boolean_cast_rejects_invalid_values():
    """Arbitrary strings must fail boolean casting."""
    field = EnvFieldSchema(name="DEBUG", type=EnvType.BOOLEAN)
    for bad in ("maybe", "2", "-1", "", "enabled", "probably", "truee"):
        result = TypeCastRule().check("DEBUG", bad, field)
        assert result.passed is False, f"{bad!r} should not cast to boolean"
        assert result.code == "type_mismatch"


def test_required_rule_rejects_empty_and_missing():
    """Required fields must fail on None or empty string."""
    field = EnvFieldSchema(name="SECRET_KEY", required=True)
    assert RequiredRule().check("SECRET_KEY", None, field).passed is False
    assert RequiredRule().check("SECRET_KEY", "", field).passed is False
    assert RequiredRule().check("SECRET_KEY", "   ", field).passed is True
    assert RequiredRule().check("SECRET_KEY", "s3cr3t", field).passed is True
