"""CI pipeline orchestrator integration example code."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from schemas.env_schema import ENV_SCHEMA  # noqa: E402
from src.validator.parser import parse_env_file  # noqa: E402


def run_deployment_pipeline_gate(env_file_path: str) -> bool:
    print(f"Deploy Gate: Validating configuration {env_file_path}...")
    try:
        parsed = parse_env_file(env_file_path)
        report = ENV_SCHEMA.validate(parsed.values)
        if report.passed:
            print("Deploy Gate: Environment config is valid. Deployment authorized.")
            return True
        else:
            print(f"Deploy Gate: Validation failed with {len(report.errors)} error(s).")
            for err in report.errors:
                print(f"  - [{err.key}] {err.message}")
            return False
    except Exception as exc:
        print(f"Deploy Gate: Error reading configuration: {exc}")
        return False


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else ".env.example"
    success = run_deployment_pipeline_gate(target)
    sys.exit(0 if success else 1)
