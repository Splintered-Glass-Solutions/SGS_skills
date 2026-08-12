#!/usr/bin/env python3
"""Sleep for a validated duration and report completion only after waking."""

from __future__ import annotations

import argparse
import json
import re
import time
from datetime import datetime, timedelta, timezone


MAX_SECONDS = 24 * 60 * 60
TOKEN_PATTERN = re.compile(r"(?P<value>\d+(?:\.\d+)?)(?P<unit>[smh]?)", re.IGNORECASE)
UNIT_SECONDS = {"": 1.0, "s": 1.0, "m": 60.0, "h": 3600.0}


def parse_duration(value: str) -> float:
    normalized = value.strip().lower().replace(" ", "")
    if not normalized:
        raise ValueError("duration is required")

    position = 0
    seconds = 0.0
    while position < len(normalized):
        match = TOKEN_PATTERN.match(normalized, position)
        if match is None or match.end() == position:
            raise ValueError(f"invalid duration: {value!r}")
        seconds += float(match.group("value")) * UNIT_SECONDS[match.group("unit")]
        position = match.end()

    if seconds > MAX_SECONDS:
        raise ValueError("duration exceeds the 24-hour safety limit")
    return seconds


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("duration", help="Seconds or a compound duration such as 5m or 1h30m")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and report the duration without waiting",
    )
    args = parser.parse_args()

    try:
        seconds = parse_duration(args.duration)
    except ValueError as error:
        parser.error(str(error))

    started_at = datetime.now(timezone.utc)
    wake_at = started_at + timedelta(seconds=seconds)
    monotonic_start = time.monotonic()

    if not args.dry_run:
        time.sleep(seconds)

    elapsed = 0.0 if args.dry_run else time.monotonic() - monotonic_start
    print(
        json.dumps(
            {
                "requested_seconds": seconds,
                "elapsed_seconds": round(elapsed, 3),
                "started_at": started_at.isoformat(),
                "wake_at": wake_at.isoformat(),
                "dry_run": args.dry_run,
            },
            separators=(",", ":"),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
