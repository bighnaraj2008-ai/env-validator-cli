"""Export validation output logs into structured JSON archives."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent


def export_logs_json(
    input_path: Optional[str] = None,
    output_path: Optional[str] = None,
    use_stdin: bool = False,
) -> dict:
    records = []
    if use_stdin:
        try:
            content = sys.stdin.read().strip()
            if content:
                records.append(json.loads(content))
        except Exception as exc:
            print(f"Warning: Could not parse stdin JSON: {exc}", file=sys.stderr)
    elif input_path:
        inp = Path(input_path)
        if inp.is_dir():
            for f in sorted(inp.glob("*.json")):
                try:
                    records.append(json.loads(f.read_text(encoding="utf-8")))
                except Exception:
                    pass

    payload = {
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "total_records": len(records),
        "records": records,
    }

    if output_path:
        Path(output_path).write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"Exported {len(records)} log record(s) to {output_path}")

    return payload


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Export logs to structured JSON")
    p.add_argument("--input", help="Directory containing JSON logs")
    p.add_argument("--output", help="Output JSON archive path")
    p.add_argument("--stdin", action="store_true", help="Read JSON from standard input")
    args = p.parse_args()
    res = export_logs_json(args.input, args.output, args.stdin)
    if not args.output:
        print(json.dumps(res, indent=2))
