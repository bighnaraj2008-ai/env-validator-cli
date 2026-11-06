"""CI environment diagnostic health check script."""

from __future__ import annotations

import importlib
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_MODULES = ["pytest", "yaml"]
RECOMMENDED_MODULES = ["flake8", "black"]


def run_health_check() -> int:
    print(f"==> Python Version: {sys.version.split()[0]}")
    print(f"==> Working Directory: {REPO_ROOT}")

    missing_required = []
    for mod in REQUIRED_MODULES:
        try:
            importlib.import_module(mod)
            print(f"  [OK] Required module: {mod}")
        except ImportError:
            print(f"  [FAIL] Missing required module: {mod}")
            missing_required.append(mod)

    for mod in RECOMMENDED_MODULES:
        try:
            importlib.import_module(mod)
            print(f"  [OK] Tooling module: {mod}")
        except ImportError:
            print(f"  [WARN] Optional tooling module: {mod}")

    # Verify schema files exist
    schemas_dir = REPO_ROOT / "schemas"
    if schemas_dir.is_dir() and list(schemas_dir.glob("*.yaml")):
        print("  [OK] Schemas directory contains YAML definitions")
    else:
        print("  [FAIL] Missing schema definitions in schemas/")
        missing_required.append("schemas")

    if missing_required:
        print(f"Health check failed with {len(missing_required)} error(s).")
        return 1

    print("Health check passed cleanly.")
    return 0


if __name__ == "__main__":
    sys.exit(run_health_check())
