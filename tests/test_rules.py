"""Unit tests for type casting, required, pattern, and length rules."""

from src.config.errors import IssueSeverity
from src.config.settings import EnvFieldSchema, EnvType
from src.validator.rules import MinLengthRule, PatternRule, RequiredRule, TypeCastRule


def test_required_rule_missing_and_optional():
    req_schema = EnvFieldSchema(name="DB_URL", required=True)
    res_fail = RequiredRule().check("DB_URL", None, req_schema)
    assert res_fail.passed is False
    assert res_fail.code == "missing"

    opt_schema = EnvFieldSchema(name="SENTRY_DSN", required=False)
    res_warn = RequiredRule().check("SENTRY_DSN", None, opt_schema)
    assert res_warn.passed is True
    assert res_warn.severity == IssueSeverity.WARNING


def test_type_cast_rule_integer_and_boolean():
    int_field = EnvFieldSchema(name="PORT", type=EnvType.INTEGER)
    assert TypeCastRule().check("PORT", "8080", int_field).passed is True
    assert TypeCastRule().check("PORT", "not_int", int_field).passed is False

    bool_field = EnvFieldSchema(name="DEBUG", type=EnvType.BOOLEAN)
    assert TypeCastRule().check("DEBUG", "yes", bool_field).passed is True
    assert TypeCastRule().check("DEBUG", "maybe", bool_field).passed is False


def test_pattern_rule_regex_validation():
    field = EnvFieldSchema(name="APP_ENV", pattern=r"^(dev|staging|prod)$")
    assert PatternRule().check("APP_ENV", "prod", field).passed is True
    res_bad = PatternRule().check("APP_ENV", "local", field)
    assert res_bad.passed is False
    assert res_bad.code == "pattern_mismatch"


def test_min_length_rule():
    field = EnvFieldSchema(name="SECRET_KEY", min_length=8)
    assert MinLengthRule().check("SECRET_KEY", "12345678", field).passed is True
    assert MinLengthRule().check("SECRET_KEY", "short", field).passed is False
