"""Automated tests validating markdown syntax across documentation."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def test_markdown_files_exist_and_non_empty():
    docs_dir = REPO_ROOT / "docs"
    md_files = list(docs_dir.glob("*.md"))
    assert len(md_files) >= 10, f"Expected at least 10 documentation files, found {len(md_files)}"

    for md in md_files:
        content = md.read_text(encoding="utf-8")
        assert len(content.strip()) > 0, f"Documentation file {md.name} is empty"
        assert content.startswith("# "), f"File {md.name} must start with top-level H1 header"


def test_readme_contains_table_of_contents():
    readme = REPO_ROOT / "README.md"
    content = readme.read_text(encoding="utf-8")
    assert "## Table of Contents" in content or "## Overview" in content
