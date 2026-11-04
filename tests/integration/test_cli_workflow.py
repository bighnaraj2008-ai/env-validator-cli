"""Integration test suite for CLI workflow execution."""

from __future__ import annotations

import json
from pathlib import Path
from src.validator.cli import main


def test_cli_integration_valid_fixture(tmp_path: Path):
    """Test full CLI flow with a valid fixture file."""
    env_file = tmp_path / ".env"
    env_file.write_text(
        "APP_NAME=IntegrateApp\nAPP_ENV=production\nPORT=8080\nDEBUG=true\n"
        "SECRET_KEY=integrate123\nJWT_SECRET=jwtintegrate123\n"
        "DATABASE_URL=postgresql://localhost:5432/intdb\nREDIS_URL=redis://localhost:6379/0\n"
        "API_KEY=integ_key_123\n",
        encoding="utf-8",
    )
    code = main(["--env", str(env_file)])
    assert code == 0


def test_cli_integration_json_output(tmp_path: Path, capsys):
    """Test CLI JSON format output telemetry structure."""
    env_file = tmp_path / ".env"
    env_file.write_text("PORT=not_an_int\n", encoding="utf-8")

    code = main(["--env", str(env_file), "--format", "json"])
    assert code == 1
    captured = capsys.readouterr().out
    data = json.loads(captured)
    assert data["passed"] is False
    assert any(err["key"] == "PORT" for err in data["errors"])
