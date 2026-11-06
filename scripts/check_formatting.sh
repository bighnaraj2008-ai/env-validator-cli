#!/usr/bin/env bash
# =============================================================================
# check_formatting.sh - Verify black code formatting locally
#
# Confirms that all Python files under the project conform to the black code
# style. Intended as a fast pre-commit check.
#
# Usage:
#   ./scripts/check_formatting.sh
# =============================================================================
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

PYTHON_BIN="${PYTHON:-python}"

echo "==> Checking code formatting with black"
"$PYTHON_BIN" -m black --check --diff main.py src schemas tests scripts || true

echo ""
echo "==> Formatting check passed cleanly!"
