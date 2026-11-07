#!/usr/bin/env bash
# =============================================================================
# run_benchmarks.sh - Automated benchmark execution runner script
# =============================================================================
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

PYTHON_BIN="${PYTHON:-python}"

echo "==> Running Parser Performance Benchmarks"
"$PYTHON_BIN" tests/benchmarks/bench_parser.py --files 100 --lines 50

echo ""
echo "==> Running Memory Allocation Benchmarks"
"$PYTHON_BIN" tests/benchmarks/bench_memory.py --cycles 100

echo ""
echo "==> All performance benchmarks completed successfully!"
