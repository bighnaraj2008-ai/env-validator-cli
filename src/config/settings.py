"""Configuration dataclasses for schema fields and validation behaviour."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .errors import SchemaError


class EnvType:
    """Supported environment variable types for strict casting."""

    STRING = "string"
    INTEGER = "integer"
    NUMBER = "number"
    BOOLEAN = "boolean"

    @classmethod
    def all(cls) -> tuple[str, ...]:
        return (cls.STRING, cls.INTEGER, cls.NUMBER, cls.BOOLEAN)


@dataclass(frozen=True)
class EnvFieldSchema:
    """Declaration of a single environment variable's validation contract.

    Attributes:
        name: Environment variable name (e.g. ``PORT``).
        required: Whether the variable must be present in the environment.
        type: One of :class:`EnvType` constants; values are cast strictly.
        pattern: Optional regular expression the (string) value must match.
        default: Value substituted when the variable is absent and not required.
        description: Human readable documentation of the variable's purpose.
        min_length: Minimum permitted length of the string value.
    """

    name: str
    required: bool = True
    type: str = EnvType.STRING
    pattern: Optional[str] = None
    default: Optional[str] = None
    description: Optional[str] = None
    min_length: Optional[int] = None

    def __post_init__(self) -> None:
        if self.type not in EnvType.all():
            raise SchemaError(
                f"Invalid type '{self.type}' for field '{self.name}'. "
                f"Allowed: {', '.join(EnvType.all())}",
                key=self.name,
            )
        if self.pattern is not None:
            import re

            try:
                re.compile(self.pattern)
            except re.error as exc:
                raise SchemaError(
                    f"Invalid regex pattern '{self.pattern}' for field '{self.name}': {exc}",
                    key=self.name,
                ) from exc


@dataclass
class ValidationConfig:
    """Runtime configuration governing how validation is performed."""

    env_file: str = ".env"
    example_file: str = ".env.example"
    strict: bool = False
    warn_on_extra: bool = True
    compare_example: bool = False
    encoding: str = "utf-8"

    def __post_init__(self) -> None:
        if not self.env_file:
            raise SchemaError("env_file must be a non-empty path")
