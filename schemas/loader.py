"""Schema loader reading declarative YAML contracts into Schema objects."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Union

from src.config.errors import EnvFileNotFoundError, SchemaError
from src.config.settings import EnvFieldSchema, EnvType
from src.validator.schema import Schema


def _parse_yaml_fallback(text: str) -> Dict[str, Any]:
    """Minimal stdlib YAML parser for schemas/env_schema.yaml when PyYAML is absent."""
    data: Dict[str, Any] = {"fields": []}
    current_field: Dict[str, Any] | None = None
    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- name:"):
            if current_field is not None:
                data["fields"].append(current_field)
            current_field = {"name": stripped.split(":", 1)[1].strip().strip('"').strip("'")}
            continue
        if ":" in stripped:
            k, _, v = stripped.partition(":")
            key = k.strip()
            val = v.strip().strip('"').strip("'")
            if current_field is not None:
                if val.lower() == "true":
                    current_field[key] = True
                elif val.lower() == "false":
                    current_field[key] = False
                elif key == "min_length" and val.isdigit():
                    current_field[key] = int(val)
                else:
                    current_field[key] = val
            else:
                data[key] = val
    if current_field is not None:
        data["fields"].append(current_field)
    return data


def load_yaml_schema(path: Union[str, Path]) -> Schema:
    """Load a Schema instance from a declarative YAML schema file."""
    schema_path = Path(path)
    if not schema_path.exists():
        raise EnvFileNotFoundError(f"Schema file not found: {schema_path}")

    raw_text = schema_path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        payload = yaml.safe_load(raw_text)
    except ImportError:
        payload = _parse_yaml_fallback(raw_text)

    if not isinstance(payload, dict) or "fields" not in payload:
        raise SchemaError(f"Invalid YAML schema structure in '{schema_path}': missing 'fields' key")

    fields: List[EnvFieldSchema] = []
    for entry in payload.get("fields", []):
        if not isinstance(entry, dict) or "name" not in entry:
            raise SchemaError(f"Malformed field definition in '{schema_path}': {entry}")
        fields.append(
            EnvFieldSchema(
                name=str(entry["name"]),
                required=bool(entry.get("required", True)),
                type=str(entry.get("type", EnvType.STRING)),
                pattern=entry.get("pattern"),
                default=entry.get("default"),
                description=entry.get("description"),
                min_length=entry.get("min_length"),
            )
        )

    return Schema(fields=fields, name=str(payload.get("schema_name", schema_path.stem)))
