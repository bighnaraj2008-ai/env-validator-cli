"""Automated test suite runner script for env-validator-cli."""

from __future__ import annotations

import argparse
import subprocess
import sys


def run_pytest(test_paths: list[str]) -> int:
    """Execute pytest with standard flags and return the exit code."""
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        *test_paths,
        "-v",
        "--tb=short",
        "-p",
        "no:cacheprovider",
    ]
    proc = subprocess.run(cmd)
    return proc.returncode


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run unit test suite.")
    parser.add_argument("tests", nargs="*", default=["tests"], help="Paths to run")
    args = parser.parse_args(argv)
    print("=" * 64)
    print("env-validator-cli - Running Unit Test Suite")
    print("=" * 64)
    return run_pytest(args.tests)


if __name__ == "__main__":
    raise SystemExit(main())
