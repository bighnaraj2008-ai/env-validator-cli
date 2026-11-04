"""Edge-case tests for integer and numeric casting validation."""

from __future__ import annotations

from src.config.settings import EnvFieldSchema, EnvType
from src.validator.rules import TypeCastRule


def test_integer_cast_rejects_non_numeric_and_float_strings():
    """Out-of-domain numeric strings must fail integer casting."""
    field = EnvFieldSchema(name="PORT", type=EnvType.INTEGER)
    assert TypeCastRule().check("PORT", "8080", field).passed is True
    assert TypeCastRule().check("PORT", "0", field).passed is True
    assert TypeCastRule().check("PORT", "-42", field).passed is True

    for bad in ("12.5", "0x10", "8k", "not-a-number", "", "  "):
        result = TypeCastRule().check("PORT", bad, field)
        assert result.passed is False, f"{bad!r} should not cast to integer"
        assert result.code == "type_mismatch"


def test_number_cast_accepts_decimals():
    """Verify number type accepts decimal and integer strings."""
    field = EnvFieldSchema(name="TIMEOUT", type=EnvType.NUMBER)
    assert TypeCastRule().check("TIMEOUT", "3.5", field).passed is True
    assert TypeCastRule().check("TIMEOUT", "10", field).passed is True
    assert TypeCastRule().check("TIMEOUT", "-0.75", field).passed is True
    assert TypeCastRule().check("TIMEOUT", "not-a-float", field).passed is False


def test_integer_boundary_limits():
    """Verify large integer values are accepted without overflow."""
    field = EnvFieldSchema(name="MAX_BYTES", type=EnvType.INTEGER)
    assert TypeCastRule().check("MAX_BYTES", "2147483647", field).passed is True
    assert TypeCastRule().check("MAX_BYTES", "-2147483648", field).passed is True
    assert TypeCastRule().check("MAX_BYTES", "9223372036854775807", field).passed is True
