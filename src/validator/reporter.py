"""Console reporting for validation reports.

The reporter layer is the only place that knows about presentation (emojis,
colour, exit codes). Validation logic itself never prints.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Optional

from .schema import ValidationReport


# ANSI colour codes. Kept minimal; colours are disabled when stdout is not a
# TTY so piped/CI output stays clean.
_COLORS = {
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "bold": "\033[1m",
    "reset": "\033[0m",
}


def _color(text: str, name: str, enabled: bool) -> str:
    if not enabled:
        return text
    return f"{_COLORS[name]}{text}{_COLORS['reset']}"


def _write_safe(file, text: str) -> None:
    """Write text to a file-like object, replacing unsupported characters.

    Some terminals (e.g. Windows cp1252) cannot encode emojis; fall back to
    replacement characters instead of crashing.
    """
    try:
        file.write(text)
    except UnicodeEncodeError:
        encoding = getattr(file, "encoding", None) or "utf-8"
        file.write(text.encode(encoding, errors="replace").decode(encoding))


class ReportFormat:
    TEXT = "text"
    JSON = "json"


@dataclass
class ConsoleReporter:
    """Renders a :class:`ValidationReport` to the terminal."""

    use_color: Optional[bool] = None
    format: str = ReportFormat.TEXT

    def __post_init__(self) -> None:
        if self.use_color is None:
            self.use_color = sys.stdout.isatty()
        if self.format not in (ReportFormat.TEXT, ReportFormat.JSON):
            raise ValueError(
                f"Unknown report format '{self.format}'. "
                f"Use '{ReportFormat.TEXT}' or '{ReportFormat.JSON}'."
            )

    def report(self, report: ValidationReport, file=None) -> int:
        """Print the report and return a process exit code (0 = pass, 1 = fail)."""
        file = file or sys.stdout

        if self.format == ReportFormat.JSON:
            import json

            json.dump(report.to_dict(), file, indent=2)
            _write_safe(file, "\n")
            return 0 if report.passed else 1

        self._render_text(report, file)
        return 0 if report.passed else 1

    def _render_text(self, report: ValidationReport, file) -> None:
        bold = _COLORS["bold"] if self.use_color else ""
        reset = _COLORS["reset"] if self.use_color else ""

        _write_safe(file, "\n")
        _write_safe(
            file,
            f"{bold}🔍 env-validator-cli — validation report for '{report.source}'{reset}\n",
        )
        _write_safe(
            file,
            f"Fields checked: {report.fields_checked}  |  Rules applied: {report.rules_applied}\n",
        )
        _write_safe(file, "\n")

        if report.passed:
            _write_safe(
                file,
                _color("✅  All environment variables are valid.\n", "green", self.use_color),
            )
        else:
            _write_safe(
                file,
                _color("❌  Validation failed — errors found below.\n", "red", self.use_color),
            )

        if report.errors:
            _write_safe(file, f"\n{bold}🚨 Errors:{reset}\n")
            for issue in report.errors:
                _write_safe(
                    file,
                    f"  [{issue.code}] {issue.key}: {issue.message}",
                )
                if issue.expected is not None:
                    _write_safe(file, f" (expected: {issue.expected}")
                    if issue.actual is not None:
                        _write_safe(file, f", actual: {issue.actual}")
                    _write_safe(file, ")")
                _write_safe(file, "\n")

        if report.warnings:
            _write_safe(file, f"\n{bold}⚠️  Warnings:{reset}\n")
            for issue in report.warnings:
                _write_safe(
                    file,
                    f"  [{issue.code}] {issue.key}: {issue.message}\n",
                )

        if not report.errors and not report.warnings:
            _write_safe(file, _color("   (none)\n", "green", self.use_color))

        _write_safe(file, f"\n{bold}Result:{reset} ")
        _write_safe(
            file,
            _color("PASS", "green", self.use_color)
            if report.passed
            else _color("FAIL", "red", self.use_color),
        )
        _write_safe(file, "\n\n")
