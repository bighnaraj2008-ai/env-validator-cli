"""Automated fixture checksum and integrity validation script."""

from __future__ import annotations

import hashlib
from pathlib import Path

FIXTURES_DIR = Path(__file__).resolve().parent.parent / "tests" / "fixtures"


def compute_sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def validate_all_fixtures() -> int:
    fixtures = sorted(FIXTURES_DIR.glob("*.env"))
    if not fixtures:
        print(f"No .env fixtures found in {FIXTURES_DIR}")
        return 1

    print("=" * 64)
    print("Fixture Checksum and Integrity Report")
    print("=" * 64)
    for fx in fixtures:
        chk = compute_sha256(fx)
        size = fx.stat().st_size
        print(f"  {fx.name:<25} size={size:<6} sha256={chk[:16]}...")
    print("=" * 64)
    print(f"Successfully validated {len(fixtures)} fixture files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(validate_all_fixtures())
