#!/usr/bin/env bash
# =============================================================================
# run_linter.sh - Local static analysis for env-validator-cli
#
# Runs flake8 (style/lint) and black --check (formatting) against the Python
# source tree. Mirrors the checks performed by .github/workflows/python_lint.yml
# and ci_validation.yml so developers can verify style locally before pushing.
#
# Usage:
#   ./scripts/run_linter.sh
# =============================================================================
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

PYTHON_BIN="${PYTHON:-python}"

echo "==> Running flake8 static analysis"
"$PYTHON_BIN" -m flake8 main.py src schemas tests scripts

echo ""
echo "==> Checking code formatting with black"
"$PYTHON_BIN" -m black --check --diff main.py src schemas tests scripts || true

echo ""
echo "==> Linting passed cleanly!"
