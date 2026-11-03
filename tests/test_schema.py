"""Unit tests for the environment Schema engine and YAML loader."""

import pytest

from schemas.env_schema import ENV_SCHEMA
from schemas.loader import load_yaml_schema
from src.config.errors import SchemaError
from src.config.settings import EnvFieldSchema, EnvType, ValidationConfig
from src.validator.schema import Schema


def test_schema_passes_valid_values():
    values = {
        "APP_NAME": "TestApp",
        "APP_ENV": "production",
        "PORT": "8000",
        "DEBUG": "true",
        "SECRET_KEY": "supersecretkey",
        "JWT_SECRET": "jwtsecret123",
        "DATABASE_URL": "postgresql://localhost/db",
        "REDIS_URL": "redis://localhost:6379/0",
        "API_KEY": "api-1234",
    }
    report = ENV_SCHEMA.validate(values)
    assert report.passed is True
    assert len(report.errors) == 0


def test_schema_strict_mode_flags_undeclared_keys():
    schema = Schema([EnvFieldSchema(name="APP_NAME", required=True, type=EnvType.STRING)])
    config = ValidationConfig(strict=True)
    report = schema.validate({"APP_NAME": "App", "EXTRA_KEY": "oops"}, config=config)
    assert report.passed is False
    assert any(err.key == "EXTRA_KEY" and err.code == "undeclared" for err in report.errors)


def test_duplicate_field_raises_schema_error():
    with pytest.raises(SchemaError):
        Schema([
            EnvFieldSchema(name="DUP", type=EnvType.STRING),
            EnvFieldSchema(name="DUP", type=EnvType.STRING),
        ])


def test_yaml_schema_loader_parses_default_yaml():
    schema = load_yaml_schema("schemas/env_schema.yaml")
    assert len(schema) == 10
    assert schema.field("PORT") is not None
    assert schema.field("PORT").type == EnvType.INTEGER
