#!/usr/bin/env python3
"""Generate an authoritative .env.example template from a schema definition."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from schemas.env_schema import ENV_SCHEMA  # noqa: E402


def render_env_example() -> str:
    """Render all fields from ENV_SCHEMA as placeholder key=value lines."""
    lines = ["# Auto-generated .env.example template from ENV_SCHEMA", ""]
    for field in ENV_SCHEMA.fields:
        req_tag = "required" if field.required else "optional"
        if field.description:
            lines.append(f"# {field.description} ({field.type}, {req_tag})")
        sample_val = field.default or f"replace-with-{field.name.lower()}"
        lines.append(f"{field.name}={sample_val}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate .env.example template.")
    parser.add_argument("--output", default=".env.example.generated", help="Output path")
    args = parser.parse_args()
    out = Path(args.output)
    out.write_text(render_env_example(), encoding="utf-8")
    print(f"Generated template with {len(ENV_SCHEMA)} keys -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
