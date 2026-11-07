"""Validation log export utility script."""

from __future__ import annotations

import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def export_logs(source_dir: str, output_file: str) -> None:
    src = Path(source_dir)
    dest = Path(output_file)
    print(f"Exporting validation logs from {src} to {dest}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export validation logs")
    parser.add_argument("--input", default="logs")
    parser.add_argument("--output", default="validation_archive.txt")
    args = parser.parse_args()
    export_logs(args.input, args.output)
