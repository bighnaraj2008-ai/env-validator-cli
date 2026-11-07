"""Validation package: parsing, schema engine, rules, and reporting.

This module exports the core public API for env-validator-cli, providing
zero-dependency environment variable parsing, strict schema validation,
pluggable rule evaluation, and customizable console/JSON reporting.
"""

from .parser import parse_env_file, ParsedEnv, EnvParseError
from .schema import Schema, ValidationReport
from .rules import Rule, RequiredRule, TypeCastRule, PatternRule
from .reporter import ConsoleReporter, ReportFormat

__all__ = [
    "parse_env_file",
    "ParsedEnv",
    "EnvParseError",
    "Schema",
    "ValidationReport",
    "Rule",
    "RequiredRule",
    "TypeCastRule",
    "PatternRule",
    "ConsoleReporter",
    "ReportFormat",
]
