"""Automated Markdown table generator for YAML schema contracts."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from schemas.loader import load_yaml_schema  # noqa: E402


def generate_schema_markdown(schema_path: Path) -> str:
    schema = load_yaml_schema(schema_path)
    lines = [
        f"# Schema Reference: {schema.name}",
        "",
        "| Field | Required | Type | Pattern / Constraints | Description |",
        "|---|---|---|---|---|",
    ]
    for field in schema.fields:
        req = "Yes" if field.required else "No"
        constraint = field.pattern or (f"min_len: {field.min_length}" if field.min_length else "-")
        desc = field.description or "-"
        lines.append(f"| `{field.name}` | {req} | `{field.type}` | `{constraint}` | {desc} |")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Markdown docs from schema.")
    parser.add_argument("--schema", type=Path, default=REPO_ROOT / "schemas" / "env_schema.yaml")
    args = parser.parse_args()
    print(generate_schema_markdown(args.schema))
    return 0


if __name__ == "__main__":
    sys.exit(main())
