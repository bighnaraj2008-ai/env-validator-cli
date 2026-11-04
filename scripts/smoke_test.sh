#!/usr/bin/env bash
set -euo pipefail

echo "==> Running env-validator-cli pre-flight smoke tests"
PYTHON_BIN="${PYTHON:-python}"

"$PYTHON_BIN" main.py --list-schemas
"$PYTHON_BIN" main.py --env .env.example --strict
"$PYTHON_BIN" main.py --env .env.example --format json >/dev/null
"$PYTHON_BIN" scripts/validate_env.py --env .env.example --compare-example --example .env.example
"$PYTHON_BIN" scripts/generate_template.py --output smoke_env_example.tmp
rm -f smoke_env_example.tmp

echo "==> Running test suite verification"
"$PYTHON_BIN" scripts/run_unit_tests.py
"$PYTHON_BIN" scripts/validate_fixtures.py

echo "==> Smoke tests passed cleanly!"
