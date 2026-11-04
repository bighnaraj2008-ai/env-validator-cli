"""Mock environment file fixture helper for unit and CLI tests."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping, Optional


def write_temp_env(
    directory: Path,
    variables: Mapping[str, str],
    filename: str = ".env.mock",
) -> Path:
    """Write a temporary key=value environment file inside ``directory`` and return its path."""
    target = directory / filename
    lines = [f"{key}={val}" for key, val in variables.items()]
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return target


def create_sample_env_content(overrides: Optional[Mapping[str, str]] = None) -> str:
    """Generate a standard valid .env content string with optional key overrides."""
    base = {
        "APP_NAME": "MockService",
        "APP_ENV": "development",
        "PORT": "8080",
        "DEBUG": "true",
        "SECRET_KEY": "supersecretmock123",
        "JWT_SECRET": "jwt-token-secret-xyz",
        "DATABASE_URL": "postgresql://user:pass@localhost:5432/mockdb",
        "REDIS_URL": "redis://localhost:6379/1",
        "API_KEY": "sk_test_mockapikey999",
        "SENTRY_DSN": "https://pubkey@sentry.io/42",
    }
    if overrides:
        base.update(overrides)
    return "\n".join(f"{k}={v}" for k, v in base.items()) + "\n"
