"""Custom assertion helper functions for validation test suites."""

from __future__ import annotations

from typing import Iterable, List, Set
from src.validator.schema import ValidationReport


def assert_report_passed(
    report: ValidationReport,
    msg: str = "Expected report to pass cleanly",
) -> None:
    """Assert that a ValidationReport contains zero validation errors."""
    formatted_errors = [f"[{e.key}] {e.code}: {e.message}" for e in report.errors]
    assert report.passed is True, f"{msg}: found errors: {formatted_errors}"
    assert len(report.errors) == 0


def assert_report_failed(
    report: ValidationReport,
    expected_error_count: int | None = None,
) -> None:
    """Assert that a ValidationReport failed and optionally check error count."""
    assert report.passed is False, "Expected report to have validation errors"
    if expected_error_count is not None:
        assert len(report.errors) == expected_error_count, (
            f"Expected {expected_error_count} errors, got {len(report.errors)}"
        )


def assert_has_error_code(report: ValidationReport, key: str, code: str) -> None:
    """Assert that an issue with the specified key and code exists in the report."""
    matching = [err for err in report.errors if err.key == key and err.code == code]
    assert matching, f"No error found for key '{key}' with code '{code}'. Errors: {report.errors}"


def assert_missing_keys(report: ValidationReport, keys: Iterable[str]) -> None:
    """Assert that the report flagged the specified keys as missing."""
    actual_missing: Set[str] = {err.key for err in report.errors if err.code == "missing"}
    expected = set(keys)
    assert expected <= actual_missing, f"Missing keys {expected - actual_missing} not flagged"


def format_report_diagnostics(report: ValidationReport) -> List[str]:
    """Format report errors and warnings into human-readable diagnostic lines."""
    diagnostics = []
    for err in report.errors:
        diagnostics.append(f"ERROR: [{err.key}] {err.code} -> {err.message}")
    for warn in report.warnings:
        diagnostics.append(f"WARN:  [{warn.key}] {warn.code} -> {warn.message}")
    return diagnostics
