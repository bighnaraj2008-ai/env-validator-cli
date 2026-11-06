"""Clean build artifacts, bytecode caches, and coverage reports."""

from __future__ import annotations

from pathlib import Path
import shutil

REPO_ROOT = Path(__file__).resolve().parent.parent

CACHE_DIRS = [
    ".pytest_cache",
    ".coverage",
    "htmlcov",
    "build",
    "dist",
    "*.egg-info",
]


def clean_cache() -> None:
    print(f"Cleaning cache and build artifacts in: {REPO_ROOT}")
    for item in CACHE_DIRS:
        for match in REPO_ROOT.glob(item):
            if match.is_dir():
                shutil.rmtree(match, ignore_errors=True)
            else:
                match.unlink(missing_ok=True)
            print(f"  Removed: {match.name}")

    for pycache in REPO_ROOT.rglob("__pycache__"):
        if pycache.is_dir():
            shutil.rmtree(pycache, ignore_errors=True)
            print(f"  Removed: {pycache.relative_to(REPO_ROOT)}")

    print("Cache cleanup complete.")


if __name__ == "__main__":
    clean_cache()
