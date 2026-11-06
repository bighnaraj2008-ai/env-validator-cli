#!/usr/bin/env bash
# =============================================================================
# bump_version.sh - Release version bumping utility script
#
# Validates and updates the package version in pyproject.toml.
#
# Usage:
#   ./scripts/bump_version.sh <new_version>
# =============================================================================
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

NEW_VERSION="${1:-}"

if [[ -z "$NEW_VERSION" ]]; then
    CURRENT=$(grep -E '^version = ' pyproject.toml | head -1 | cut -d'"' -f2)
    echo "Current version: $CURRENT"
    echo "Usage: ./scripts/bump_version.sh <new_version>"
    exit 0
fi

PYTHON_BIN="${PYTHON:-python}"

"$PYTHON_BIN" -c "
import re
from pathlib import Path

p = Path('pyproject.toml')
text = p.read_text(encoding='utf-8')
new_text = re.sub(r'version = "[^"]+"', f'version = "$NEW_VERSION"', text, count=1)
p.write_text(new_text, encoding='utf-8')
print(f'Bumped version to: $NEW_VERSION')
"
