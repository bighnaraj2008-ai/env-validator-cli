"""Memory consumption and safety verification for validator engine."""

from __future__ import annotations

import tracemalloc
from schemas.env_schema import ENV_SCHEMA
from src.validator.parser import parse_env_text


def test_memory_profile_during_parsing_and_validation():
    """Verify memory allocation remains bounded during 500 validation cycles."""
    sample_text = (
        "APP_NAME=MemApp\nAPP_ENV=production\nPORT=8080\nDEBUG=true\n"
        "SECRET_KEY=s3cr3tkey123\nJWT_SECRET=jwtsecret123\n"
        "DATABASE_URL=postgresql://localhost:5432/db\nREDIS_URL=redis://localhost:6379/0\n"
        "API_KEY=apikey123\n"
    )

    tracemalloc.start()
    for _ in range(500):
        parsed = parse_env_text(sample_text)
        ENV_SCHEMA.validate(parsed.values)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Peak memory overhead should remain under 10MB
    assert peak < 10 * 1024 * 1024, f"Peak memory exceeded threshold: {peak / (1024 * 1024):.2f}MB"
