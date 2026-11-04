"""Utility script to generate custom .env test fixtures for local testing."""

from __future__ import annotations

import argparse
from pathlib import Path


def generate_fixture(
    output_path: Path,
    environment: str = "staging",
    port: int = 8080,
) -> None:
    lines = [
        f"# Auto-generated test fixture for {environment} tier",
        "APP_NAME=CustomFixtureApp",
        f"APP_ENV={environment}",
        f"PORT={port}",
        "DEBUG=false",
        "SECRET_KEY=custom-super-secret-key-12345",
        "JWT_SECRET=custom-jwt-secret-token-67890",
        f"DATABASE_URL=postgresql://custom_user:pass@localhost:5432/{environment}_db",
        "REDIS_URL=redis://localhost:6379/2",
        "API_KEY=sk_test_custom_fixture_key_abcdef",
        "SENTRY_DSN=https://sample@sentry.io/100",
    ]
    content = "\n".join(lines) + "\n"
    output_path.write_text(content, encoding="utf-8")
    print(f"Generated fixture at: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate custom .env test fixture.")
    parser.add_argument("--out", type=Path, default=Path("tests/fixtures/generated.env"))
    parser.add_argument(
        "--tier",
        default="staging",
        choices=["development", "staging", "production"],
    )
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    generate_fixture(args.out, args.tier, args.port)
