"""Automated Python style compliance test runner."""

from __future__ import annotations

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def test_flake8_config_exists():
    flake8_path = REPO_ROOT / ".flake8"
    assert flake8_path.is_file(), ".flake8 configuration file must exist"
    content = flake8_path.read_text(encoding="utf-8")
    assert "[flake8]" in content


def test_pyproject_contains_black_config():
    pyproject_path = REPO_ROOT / "pyproject.toml"
    assert pyproject_path.is_file(), "pyproject.toml must exist"
    content = pyproject_path.read_text(encoding="utf-8")
    assert "[tool.black]" in content
    assert "line-length" in content


def test_all_python_sources_valid_ast():
    py_files = list((REPO_ROOT / "src").rglob("*.py"))
    assert len(py_files) > 0, "Source files must exist in src/"
    for py_file in py_files:
        code = py_file.read_text(encoding="utf-8")
        parsed = ast.parse(code, filename=str(py_file))
        assert parsed is not None
