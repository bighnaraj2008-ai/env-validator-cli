"""Individual validation rules applied to environment variables.

Each rule implements :class:`Rule` and produces a :class:`ValidationResult`.
Rules are stateless and side-effect free so they can be composed, reused, and
tested independently of the reporter or CLI layers.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

from ..config.errors import IssueSeverity, ValidationIssue
from ..config.settings import EnvFieldSchema, EnvType


@dataclass(frozen=True)
class ValidationResult:
    """Outcome of evaluating one rule against one variable."""

    key: str
    passed: bool
    code: str
    message: str
    severity: str = IssueSeverity.ERROR
    expected: Optional[str] = None
    actual: Optional[str] = None

    def to_issue(self) -> ValidationIssue:
        return ValidationIssue(
            key=self.key,
            code=self.code,
            message=self.message,
            severity=self.severity,
            expected=self.expected,
            actual=self.actual,
        )


class Rule:
    """Base class for validation rules.

    Subclasses implement :meth:`check`, which receives a variable name, its
    raw string value (or ``None`` when absent), and the field schema.
    """

    def check(
        self,
        key: str,
        value: Optional[str],
        schema: EnvFieldSchema,
    ) -> ValidationResult:
        raise NotImplementedError


class RequiredRule(Rule):
    """Ensures required variables are present and non-empty."""

    code = "missing"

    def check(
        self,
        key: str,
        value: Optional[str],
        schema: EnvFieldSchema,
    ) -> ValidationResult:
        present = value is not None and value != ""
        if not schema.required:
            if not present:
                return ValidationResult(
                    key=key,
                    passed=True,
                    code="optional_absent",
                    message=f"'{key}' is optional and unset",
                    severity=IssueSeverity.WARNING,
                )
            return ValidationResult(
                key=key,
                passed=True,
                code="ok",
                message=f"'{key}' present",
            )
        if not present:
            return ValidationResult(
                key=key,
                passed=False,
                code=self.code,
                message=(
                    f"Required environment variable '{key}' is missing or empty"
                ),
                expected="<present, non-empty value>",
                actual="<missing>",
            )
        return ValidationResult(key=key, passed=True, code="ok", message=f"'{key}' present")


class TypeCastRule(Rule):
    """Strictly casts a value to the schema-declared type.

    Supported casts: ``string`` (no-op), ``integer``, ``number`` (float),
    ``boolean`` (accepts 1/0, true/false, yes/no, on/off).
    """

    code = "type_mismatch"

    _BOOLEAN_TRUE = {"1", "true", "t", "yes", "y", "on"}
    _BOOLEAN_FALSE = {"0", "false", "f", "no", "n", "off"}

    def check(
        self,
        key: str,
        value: Optional[str],
        schema: EnvFieldSchema,
    ) -> ValidationResult:
        if value is None:
            return ValidationResult(
                key=key,
                passed=True,
                code="ok",
                message=f"'{key}' absent; skipping type cast",
            )

        casted = self._cast(value, schema.type)
        if casted is None:
            return ValidationResult(
                key=key,
                passed=False,
                code=self.code,
                message=(
                    f"Cannot cast '{key}'={value!r} to type '{schema.type}'"
                ),
                expected=schema.type,
                actual=value,
                severity=IssueSeverity.ERROR,
            )
        return ValidationResult(
            key=key,
            passed=True,
            code="ok",
            message=f"'{key}' cast to {schema.type}",
            actual=value,
        )

    @staticmethod
    def _cast(value: str, target_type: str) -> Optional[object]:
        if target_type == EnvType.STRING:
            return value
        if target_type == EnvType.INTEGER:
            try:
                return int(value)
            except (TypeError, ValueError):
                return None
        if target_type == EnvType.NUMBER:
            try:
                return float(value)
            except (TypeError, ValueError):
                return None
        if target_type == EnvType.BOOLEAN:
            lowered = value.strip().lower()
            if lowered in TypeCastRule._BOOLEAN_TRUE:
                return True
            if lowered in TypeCastRule._BOOLEAN_FALSE:
                return False
            return None
        return None


class PatternRule(Rule):
    """Validates a value against a regular expression pattern."""

    code = "pattern_mismatch"

    def check(
        self,
        key: str,
        value: Optional[str],
        schema: EnvFieldSchema,
    ) -> ValidationResult:
        if value is None or not schema.pattern:
            return ValidationResult(
                key=key,
                passed=True,
                code="ok",
                message=f"'{key}' pattern check skipped",
            )
        if re.search(schema.pattern, value):
            return ValidationResult(
                key=key,
                passed=True,
                code="ok",
                message=f"'{key}' matches pattern",
                actual=value,
            )
        return ValidationResult(
            key=key,
            passed=False,
            code=self.code,
            message=f"'{key}'={value!r} does not match pattern '{schema.pattern}'",
            expected=schema.pattern,
            actual=value,
        )


class MinLengthRule(Rule):
    """Enforces a minimum string length for sensitive values (e.g. secrets)."""

    code = "too_short"

    def check(
        self,
        key: str,
        value: Optional[str],
        schema: EnvFieldSchema,
    ) -> ValidationResult:
        if value is None or schema.min_length is None:
            return ValidationResult(
                key=key,
                passed=True,
                code="ok",
                message=f"'{key}' min-length check skipped",
            )
        if len(value) < schema.min_length:
            return ValidationResult(
                key=key,
                passed=False,
                code=self.code,
                message=(
                    f"'{key}' is too short: {len(value)} chars, "
                    f"minimum {schema.min_length}"
                ),
                expected=f">={schema.min_length} chars",
                actual=f"{len(value)} chars",
            )
        return ValidationResult(
            key=key,
            passed=True,
            code="ok",
            message=f"'{key}' meets minimum length",
            actual=value,
        )


DEFAULT_RULES: tuple[Rule, ...] = (
    RequiredRule(),
    TypeCastRule(),
    PatternRule(),
    MinLengthRule(),
)
