#!/usr/bin/env bash
# =============================================================================
# cli_batch_demo.sh - Batch validation CLI demonstration script
# =============================================================================
set -euo pipefail

echo "==> Running batch environment configuration validation demo"

PYTHON_BIN="${PYTHON:-python}"

for env_file in .env.example tests/fixtures/valid.env; do
    if [[ -f "$env_file" ]]; then
        echo "Validating: $env_file"
        "$PYTHON_BIN" main.py --env "$env_file" --format json >/dev/null
        echo "  [PASS] $env_file verified successfully"
    fi
done

echo "==> Batch demonstration completed successfully."
