"""Unit tests for the command-line interface entrypoint."""

import json

from src.validator.cli import main


def test_cli_list_schemas_returns_zero(capsys):
    rc = main(["--list-schemas"])
    captured = capsys.readouterr()
    assert rc == 0
    assert "default" in captured.out


def test_cli_validates_example_env_json_format(capsys):
    rc = main(["--env", ".env.example", "--format", "json"])
    captured = capsys.readouterr()
    assert rc == 0
    payload = json.loads(captured.out)
    assert payload["passed"] is True
    assert payload["fields_checked"] == 10


def test_cli_strict_mode_fails_on_extra_key(tmp_path):
    env_file = tmp_path / ".env.extra"
    clean_example = open(".env.example", encoding="utf-8").read()
    env_file.write_text(clean_example + "\nUNDOCUMENTED_VAR=oops\n", encoding="utf-8")
    rc = main(["--env", str(env_file), "--strict"])
    assert rc == 1


def test_cli_compare_example_succeeds_for_matching_keys():
    rc = main(["--env", ".env.example", "--example", ".env.example", "--compare-example"])
    assert rc == 0
