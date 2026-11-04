#!/usr/bin/env python3
"""Automated test harness for env-validator-cli (Day 2).

Responsibilities:

1. Ingest the mock ``.env`` fixtures under ``tests/fixtures/`` and report
   fixture telemetry (exists, key count, expected anomaly class).
2. Discover and run the unit-test suite under ``tests/`` via pytest.
3. Measure assertion pass/fail rates from the pytest summary.
4. Emit a structured diagnostic summary (human-readable table + JSON block)
   to stdout and return a non-zero exit code when any check fails.

Usage:

    python scripts/run_unit_tests.py
    python scripts/run_unit_tests.py --json-only
    python scripts/run_unit_tests.py --tests tests/test_edge_cases.py
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures"
REQUIRED_FIXTURES = [
    "valid.env",
    "malformed.env",
    "missing_required.env",
    "invalid_types.env",
]

# Expected anomaly class per fixture, used for fixture telemetry.
FIXTURE_ANOMALY = {
    "valid.env": "none",
    "malformed.env": "syntax-error",
    "missing_required.env": "missing-required",
    "invalid_types.env": "type-pattern-length-violation",
}


def ingest_fixtures() -> tuple[bool, list[dict]]:
    """Verify every required fixture exists and summarize its contents."""
    results: list[dict] = []
    all_ok = True
    for name in REQUIRED_FIXTURES:
        path = FIXTURES_DIR / name
        entry: dict = {"fixture": name}
        if not path.exists():
            all_ok = False
            entry.update(
                {
                    "status": "MISSING",
                    "keys": 0,
                    "anomaly": FIXTURE_ANOMALY[name],
                    "note": "fixture file not found",
                }
            )
            results.append(entry)
            continue

        text = path.read_text(encoding="utf-8")
        # Crude key telemetry: lines matching KEY=something.
        key_lines = [
            line
            for line in text.splitlines()
            if line.strip()
            and not line.strip().startswith("#")
            and "=" in line
            and line.split("=", 1)[0].strip()
        ]
        entry.update(
            {
                "status": "OK",
                "keys": len(key_lines),
                "anomaly": FIXTURE_ANOMALY[name],
                "note": "ingested",
            }
        )
        results.append(entry)
    return all_ok, results


def run_pytest(test_paths: list[str]) -> tuple[int, str, dict]:
    """Run pytest over ``test_paths`` and parse the diagnostic summary."""
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        *test_paths,
        "-v",
        "--tb=short",
        "-p",
        "no:cacheprovider",
        "-q",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    output = proc.stdout + proc.stderr

    passed = failed = errors = 0
    summary_match = re.search(
        r"(\d+) passed(?:, (\d+) failed)?(?:, (\d+) error[s]?)?",
        output,
    )
    if summary_match:
        passed = int(summary_match.group(1))
        failed = int(summary_match.group(2) or 0)
        errors = int(summary_match.group(3) or 0)

    total = passed + failed + errors
    pass_rate = (passed / total * 100) if total else 0.0

    per_test: list[dict] = []
    for line in output.splitlines():
        m = re.match(
            r"\s*(tests/.+?::.+?)\s+(PASSED|FAILED|ERROR|SKIPPED)"
            r"(?:\s*\[\s*\d+%\s*\])?\s*$",
            line,
        )
        if m:
            per_test.append(
                {"node": m.group(1), "status": m.group(2)}
            )

    return proc.returncode, output, {
        "total": total,
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "skipped": sum(1 for t in per_test if t["status"] == "SKIPPED"),
        "pass_rate": round(pass_rate, 2),
        "per_test": per_test,
    }


def build_report(
    fixtures_ok: bool,
    fixture_results: list[dict],
    rc: int,
    summary: dict,
    raw_output: str,
) -> dict:
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repository": str(REPO_ROOT),
        "fixtures": {
            "all_present": fixtures_ok,
            "results": fixture_results,
        },
        "tests": summary,
        "exit_code": rc if rc else (0 if fixtures_ok and summary["failed"] == 0 and summary["errors"] == 0 else 1),
        "raw_pytest_tail": raw_output.strip().splitlines()[-5:],
    }


def render_human_readable(report: dict) -> str:
    lines = []
    lines.append("=" * 64)
    lines.append("env-validator-cli — Day 2 Test Harness")
    lines.append("=" * 64)
    lines.append("")
    lines.append("[1/4] Ingesting test fixtures")
    for fx in report["fixtures"]["results"]:
        mark = "OK " if fx["status"] == "OK" else "!! "
        lines.append(
            f"    {mark}{fx['fixture']:<30} status={fx['status']:<9} "
            f"keys={fx['keys']:<4} anomaly={fx['anomaly']}"
        )
    lines.append(f"    All fixtures present: {report['fixtures']['all_present']}")
    lines.append("")
    lines.append("[2/4] Running unit test suite")
    lines.append(f"    Exit code: {report['exit_code']}")
    lines.append("")
    lines.append("[3/4] Assertion pass/fail summary")
    tests = report["tests"]
    lines.append(f"    Total : {tests['total']}")
    lines.append(f"    Passed: {tests['passed']}")
    lines.append(f"    Failed: {tests['failed']}")
    lines.append(f"    Errors: {tests['errors']}")
    lines.append(f"    Skipped: {tests['skipped']}")
    lines.append(f"    Pass rate: {tests['pass_rate']}%")
    lines.append("")
    lines.append("[4/4] Per-test results")
    for entry in tests["per_test"]:
        lines.append(f"    {entry['status']:<9} {entry['node']}")
    if not tests["per_test"]:
        lines.append("    (per-test breakdown unavailable from parser output)")
    lines.append("")
    lines.append("Diagnostic summary (JSON):")
    lines.append(json.dumps(report, indent=2))
    lines.append("=" * 64)
    overall = (
        "PASS"
        if report["exit_code"] == 0
        else "FAIL"
    )
    lines.append(f"Overall result: {overall}")
    lines.append("=" * 64)
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run env-validator-cli unit tests with fixture ingestion and diagnostics."
    )
    parser.add_argument(
        "tests",
        nargs="*",
        default=["tests"],
        help="Test paths to pass to pytest (default: all of tests/)",
    )
    parser.add_argument(
        "--json-only",
        action="store_true",
        help="Emit only the JSON diagnostic summary.",
    )
    args = parser.parse_args(argv)

    fixtures_ok, fixture_results = ingest_fixtures()
    rc, raw_output, summary = run_pytest(args.tests)

    report = build_report(fixtures_ok, fixture_results, rc, summary, raw_output)

    if args.json_only:
        print(json.dumps(report, indent=2))
    else:
        print(render_human_readable(report))

    return report["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
