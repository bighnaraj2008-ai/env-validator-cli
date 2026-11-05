"""Markdown link and cross-reference validation script."""

from __future__ import annotations

from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent


def check_markdown_links() -> int:
    md_files = list(REPO_ROOT.glob("*.md")) + list((REPO_ROOT / "docs").glob("*.md"))
    broken_links = []

    link_pattern = re.compile(r"\[([^\]]+)\]\(([^\)]+)\)")

    for md_path in md_files:
        content = md_path.read_text(encoding="utf-8")
        for match in link_pattern.finditer(content):
            target = match.group(2)
            # Skip external URLs, email links, anchor-only links
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            # Remove intra-file anchor if present
            clean_target = target.split("#")[0]
            if not clean_target:
                continue
            resolved = (md_path.parent / clean_target).resolve()
            if not resolved.exists():
                broken_links.append((md_path.relative_to(REPO_ROOT), target))

    if broken_links:
        print(f"Found {len(broken_links)} broken link(s):")
        for file, target in broken_links:
            print(f"  {file} -> {target}")
        return 1

    print(f"All markdown documentation links valid across {len(md_files)} files.")
    return 0


if __name__ == "__main__":
    sys.exit(check_markdown_links())
