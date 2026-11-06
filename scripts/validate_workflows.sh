#!/usr/bin/env bash
# =============================================================================
# validate_workflows.sh - Validate GitHub Actions workflow YAML files
#
# Validates syntax and structure of all workflows under .github/workflows/.
#
# Usage:
#   ./scripts/validate_workflows.sh
# =============================================================================
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

PYTHON_BIN="${PYTHON:-python}"

echo "==> Validating GitHub Actions workflows"
"$PYTHON_BIN" -c "
from pathlib import Path
import yaml
import sys

workflows_dir = Path('.github/workflows')
failed = False
for yml in sorted(workflows_dir.glob('*.yml')):
    try:
        with open(yml, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            assert 'name' in data, 'Missing workflow name'
            assert 'jobs' in data, 'Missing jobs definition'
            print(f'  [OK] {yml.name} (Jobs: {list(data.get("jobs", {}).keys())})')
    except Exception as e:
        print(f'  [FAIL] {yml.name}: {e}')
        failed = True

if failed:
    sys.exit(1)
print('All workflow files valid.')
"

echo "==> Workflow validation complete!"
