"""Schema validation engine.

A :class:`Schema` groups :class:`~src.config.settings.EnvFieldSchema`
declarations and applies the rule pipeline (see :mod:`src.validator.rules`)
against a parsed environment, producing a :class:`ValidationReport`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Optional, Sequence

from ..config.errors import IssueSeverity, ValidationIssue
from ..config.settings import EnvFieldSchema, ValidationConfig
from .rules import DEFAULT_RULES, Rule


@dataclass
class ValidationReport:
    """Aggregated result of validating one environment against one schema."""

    source: str
    issues: list[ValidationIssue] = field(default_factory=list)
    rules_applied: int = 0
    fields_checked: int = 0

    @property
    def errors(self) -> list[ValidationIssue]:
        return [issue for issue in self.issues if issue.severity == IssueSeverity.ERROR]

    @property
    def warnings(self) -> list[ValidationIssue]:
        return [issue for issue in self.issues if issue.severity == IssueSeverity.WARNING]

    @property
    def passed(self) -> bool:
        return not bool(self.errors)

    def add(self, issue: ValidationIssue) -> None:
        self.issues.append(issue)

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "passed": self.passed,
            "errors": [issue.to_dict() for issue in self.errors],
            "warnings": [issue.to_dict() for issue in self.warnings],
            "rules_applied": self.rules_applied,
            "fields_checked": self.fields_checked,
        }


class Schema:
    """A named collection of field declarations plus a rule pipeline."""

    def __init__(
        self,
        fields: Iterable[EnvFieldSchema],
        *,
        rules: Optional[Sequence[Rule]] = None,
        name: Optional[str] = None,
    ) -> None:
        self.fields = list(fields)
        self.name = name or "unnamed"
        self.rules = list(rules) if rules is not None else list(DEFAULT_RULES)
        self._by_name: dict[str, EnvFieldSchema] = {}
        for field_schema in self.fields:
            if field_schema.name in self._by_name:
                raise SchemaError(
                    f"Duplicate field declaration '{field_schema.name}' in schema '{self.name}'",
                    key=field_schema.name,
                )
            self._by_name[field_schema.name] = field_schema

    def validate(
        self,
        values: dict[str, str],
        config: Optional[ValidationConfig] = None,
    ) -> ValidationReport:
        """Run every rule against every declared field for the given values.

        Missing required fields are reported once via :class:`RequiredRule`;
        present fields are cast, pattern-matched, and length-checked.
        """
        config = config or ValidationConfig()
        report = ValidationReport(source=config.env_file)

        for field_schema in self.fields:
            report.fields_checked += 1
            value = values.get(field_schema.name)

            for rule in self.rules:
                report.rules_applied += 1
                result = rule.check(field_schema.name, value, field_schema)
                # Report every failure, plus genuine warnings (e.g. an optional
                # field left unset). Informational "ok" results are silent.
                if not result.passed or (
                    result.severity == IssueSeverity.WARNING
                    and result.code != "ok"
                ):
                    report.add(result.to_issue())

        # Extra-key detection: flag keys present in the environment but not
        # declared in the schema when the caller wants strict hygiene.
        if config.strict:
            declared = set(self._by_name)
            for extra_key in sorted(set(values) - declared):
                report.add(
                    ValidationIssue(
                        key=extra_key,
                        code="undeclared",
                        message=(
                            f"'{extra_key}' is present in the environment but "
                            "not declared in the schema"
                        ),
                        severity=IssueSeverity.ERROR,
                    )
                )

        return report

    def field(self, name: str) -> Optional[EnvFieldSchema]:
        """Look up a declared field by name."""
        return self._by_name.get(name)

    def __len__(self) -> int:
        return len(self.fields)


# Imported lazily below to avoid a circular import between schema and errors.
from ..config.errors import SchemaError  # noqa: E402
