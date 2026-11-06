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

echo "==> Running static analysis verification"
"$PYTHON_BIN" -m flake8 main.py src schemas tests scripts

echo "==> Running test suite verification"
"$PYTHON_BIN" scripts/run_unit_tests.py
"$PYTHON_BIN" scripts/validate_fixtures.py

echo "==> Running documentation link verification"
"$PYTHON_BIN" scripts/validate_docs.py

echo "==> Smoke tests passed cleanly!"
