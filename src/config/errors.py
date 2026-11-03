"""Custom exceptions and structured validation issues for env-validator-cli.

All validation errors raised by the validator package inherit from
:class:`EnvValidationError` so callers can catch a single, well-known
exception type. Structured issues (:class:`ValidationIssue`) are produced
during rule evaluation and handed to the reporter layer for rendering.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


class EnvValidationError(Exception):
    """Base exception for every environment validation error."""

    def __init__(self, message: str, key: Optional[str] = None) -> None:
        super().__init__(message)
        self.message = message
        self.key = key

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.__class__.__name__}: {self.message}"


class EnvFileNotFoundError(EnvValidationError):
    """Raised when a required .env or schema file is missing on disk."""


class EnvParseError(EnvValidationError):
    """Raised when a .env file cannot be parsed (malformed lines, bad quoting)."""


class MissingEnvVarError(EnvValidationError):
    """Raised when a required environment variable is absent."""


class TypeCastError(EnvValidationError):
    """Raised when an environment variable cannot be cast to its declared type."""


class PatternMismatchError(EnvValidationError):
    """Raised when an environment variable fails a regex pattern constraint."""


class SchemaError(EnvValidationError):
    """Raised when a schema definition itself is invalid."""


class IssueSeverity:
    """Severity levels for structured validation issues."""

    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True)
class ValidationIssue:
    """A single structured issue found while validating an environment."""

    key: str
    code: str
    message: str
    severity: str = IssueSeverity.ERROR
    expected: Optional[str] = None
    actual: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "key": self.key,
            "code": self.code,
            "message": self.message,
            "severity": self.severity,
            "expected": self.expected,
            "actual": self.actual,
        }
