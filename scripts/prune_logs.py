"""Log rotation and historical validation log pruning utility script."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def prune_validation_logs(
    logs_dir: str,
    retention_days: int = 7,
    dry_run: bool = False,
    manifest_path: str | None = None,
) -> list[str]:
    target = Path(logs_dir)
    if not target.exists():
        print(f"Directory {target} does not exist. Nothing to prune.")
        return []

    cutoff = datetime.now(timezone.utc) - timedelta(days=retention_days)
    pruned = []

    for f in target.glob("*"):
        if f.is_file() and f.suffix in (".log", ".json", ".tmp"):
            mtime = datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc)
            if mtime < cutoff:
                pruned.append(str(f.name))
                if not dry_run:
                    f.unlink()

    status = "Identified" if dry_run else "Pruned"
    print(f"{status} {len(pruned)} old file(s) in {target} (retention: {retention_days} days).")

    if manifest_path:
        Path(manifest_path).write_text(json.dumps({"pruned": pruned}, indent=2), encoding="utf-8")

    return pruned


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Prune historical logs")
    p.add_argument("--logs-dir", default="logs")
    p.add_argument("--retention-days", type=int, default=7)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--manifest", help="Optional output manifest JSON path")
    args = p.parse_args()
    prune_validation_logs(args.logs_dir, args.retention_days, args.dry_run, args.manifest)
