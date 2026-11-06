"""Local build matrix and workflow verification tests."""

from __future__ import annotations

from pathlib import Path
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def test_ci_validation_workflow_matrix():
    workflow_path = REPO_ROOT / ".github" / "workflows" / "ci_validation.yml"
    assert workflow_path.is_file(), "ci_validation.yml must exist"

    data = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
    assert "jobs" in data
    assert "validate" in data["jobs"]

    matrix = data["jobs"]["validate"]["strategy"]["matrix"]
    versions = matrix["python-version"]
    assert "3.9" in versions
    assert "3.10" in versions
    assert "3.11" in versions
    assert "3.12" in versions


def test_validator_ci_workflow_exists():
    workflow_path = REPO_ROOT / ".github" / "workflows" / "validator_ci.yml"
    assert workflow_path.is_file(), "validator_ci.yml must exist"
