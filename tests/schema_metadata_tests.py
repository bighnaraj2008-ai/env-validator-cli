"""Metadata and structural integrity validation for schema definitions."""

from __future__ import annotations

from pathlib import Path
from schemas.env_schema import ENV_SCHEMA
from schemas.loader import load_yaml_schema

SCHEMA_YAML_PATH = Path(__file__).resolve().parent.parent / "schemas" / "env_schema.yaml"


def test_schema_field_count():
    """Verify default schema contains all required enterprise fields."""
    assert len(ENV_SCHEMA.fields) == 10
    names = {f.name for f in ENV_SCHEMA.fields}
    assert "APP_NAME" in names
    assert "SECRET_KEY" in names
    assert "PORT" in names


def test_schema_yaml_loader_metadata():
    """Verify YAML schema loader parses metadata without errors."""
    schema = load_yaml_schema(SCHEMA_YAML_PATH)
    assert schema.name in ("env-validator-cli", "env_schema")
    assert len(schema.fields) == 10
