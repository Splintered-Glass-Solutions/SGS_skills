#!/usr/bin/env python3
"""Append one local-only JSONL time entry with source-ID deduplication."""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


TIMEZONE = "UTC"
LEDGER_RELATIVE = Path(".codex/time_tracking.jsonl")


def parse_args() -> argparse.Namespace:
    timezone_parser = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    timezone_parser.add_argument("--timezone", default=TIMEZONE)
    known, _ = timezone_parser.parse_known_args()
    now = datetime.now(ZoneInfo(known.timezone))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timezone", default=known.timezone)
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--date", default=now.strftime("%Y-%m-%d"))
    parser.add_argument("--time", default=now.strftime("%H:%M"))
    parser.add_argument("--minutes", required=True, type=int)
    parser.add_argument("--description", required=True)
    parser.add_argument("--project", required=True)
    parser.add_argument("--source", default="manual")
    parser.add_argument("--source-id")
    parser.add_argument("--source-duration-ms", type=int)
    parser.add_argument("--task")
    parser.add_argument("--task-id")
    parser.add_argument("--billable", choices=("true", "false"))
    return parser.parse_args()


def git_exclude_path(root: Path) -> Path | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--git-path", "info/exclude"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    path = Path(result.stdout.strip())
    return path if path.is_absolute() else root / path


def ensure_local_only(root: Path, ledger: Path) -> None:
    exclude = git_exclude_path(root)
    if exclude is None:
        return
    exclude.parent.mkdir(parents=True, exist_ok=True)
    existing = exclude.read_text() if exclude.exists() else ""
    pattern = str(ledger.relative_to(root))
    if pattern not in {line.strip() for line in existing.splitlines()}:
        with exclude.open("a") as handle:
            if existing and not existing.endswith("\n"):
                handle.write("\n")
            handle.write(f"{pattern}\n")


def existing_source_ids(ledger: Path) -> set[str]:
    if not ledger.exists():
        return set()
    ids: set[str] = set()
    for line in ledger.read_text().splitlines():
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        source_id = item.get("source_id")
        if source_id:
            ids.add(str(source_id))
    return ids


def main() -> int:
    args = parse_args()
    if args.minutes <= 0:
        raise SystemExit("--minutes must be greater than zero")
    try:
        datetime.strptime(args.date, "%Y-%m-%d")
        datetime.strptime(args.time, "%H:%M")
    except ValueError as exc:
        raise SystemExit("--date must be YYYY-MM-DD and --time must be HH:MM") from exc

    root = args.project_root.expanduser().resolve()
    ledger = root / LEDGER_RELATIVE
    ledger.parent.mkdir(parents=True, exist_ok=True)
    ensure_local_only(root, ledger)

    if args.source_id and str(args.source_id) in existing_source_ids(ledger):
        print(json.dumps({"status": "duplicate", "ledger": str(ledger), "source_id": str(args.source_id)}))
        return 0

    billable = None if args.billable is None else args.billable == "true"
    entry = {
        "date": args.date,
        "time": args.time,
        "minutes": args.minutes,
        "description": args.description.strip(),
        "project": args.project,
        "timezone": args.timezone,
        "source": args.source,
        "source_id": args.source_id,
        "task": args.task,
        "task_id": args.task_id,
        "billable": billable,
    }
    if args.source_duration_ms is not None:
        entry["source_duration_ms"] = args.source_duration_ms
    if ledger.exists() and ledger.stat().st_size and not ledger.read_bytes().endswith(b"\n"):
        with ledger.open("a") as handle:
            handle.write("\n")
    with ledger.open("a") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(json.dumps({"status": "appended", "ledger": str(ledger), "source_id": args.source_id}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
