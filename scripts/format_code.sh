#!/usr/bin/env bash
# =============================================================================
# format_code.sh - Automated source formatting fixer script
#
# Formats all Python files in the repository using black.
#
# Usage:
#   ./scripts/format_code.sh
# =============================================================================
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

PYTHON_BIN="${PYTHON:-python}"

echo "==> Auto-formatting Python sources with black"
"$PYTHON_BIN" -m black main.py src schemas tests scripts

echo ""
echo "==> Source formatting complete!"
