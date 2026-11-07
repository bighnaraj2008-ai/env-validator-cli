"""Master workspace cleaning and reset utility script."""

from __future__ import annotations

import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def clean_workspace() -> None:
    print(f"Cleaning all caches and temporary files in {REPO_ROOT}...")
    for pat in ["__pycache__", ".pytest_cache", "*.egg-info", "build", "dist"]:
        for p in REPO_ROOT.rglob(pat):
            if p.is_dir():
                shutil.rmtree(p, ignore_errors=True)
                print(f"  Removed: {p.relative_to(REPO_ROOT)}")
    print("Master cleaning completed successfully.")


if __name__ == "__main__":
    clean_workspace()
