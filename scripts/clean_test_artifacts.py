"""Clean test artifacts, bytecode caches, and coverage reports."""

from __future__ import annotations

from pathlib import Path
import shutil

REPO_ROOT = Path(__file__).resolve().parent.parent

ARTIFACT_DIRS = [
    ".pytest_cache",
    ".coverage",
    "htmlcov",
    "build",
    "dist",
]


def clean_artifacts() -> None:
    print(f"Cleaning test artifacts in: {REPO_ROOT}")
    for item in ARTIFACT_DIRS:
        target = REPO_ROOT / item
        if target.exists():
            if target.is_dir():
                shutil.rmtree(target, ignore_errors=True)
            else:
                target.unlink(missing_ok=True)
            print(f"  Removed: {item}")

    for pycache in REPO_ROOT.rglob("__pycache__"):
        if pycache.is_dir():
            shutil.rmtree(pycache, ignore_errors=True)
            print(f"  Removed: {pycache.relative_to(REPO_ROOT)}")

    print("Cleanup complete.")


if __name__ == "__main__":
    clean_artifacts()
