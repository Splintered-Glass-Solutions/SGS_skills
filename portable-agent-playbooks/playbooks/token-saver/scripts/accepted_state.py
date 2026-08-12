#!/usr/bin/env python3
"""Store one human-accepted result and build strict reuse or revision packets."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Sequence

STATE_VERSION = 1
SENSITIVE = re.compile(
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\bsk-[A-Za-z0-9_-]{16,}|\b(?:ghp|github_pat)_[A-Za-z0-9_-]{16,}|\bAKIA[0-9A-Z]{16}\b"
)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def read_text(direct: str | None, file_path: Path | None, label: str) -> str:
    if direct is not None:
        value = direct
    elif file_path is not None:
        value = file_path.read_text(encoding="utf-8")
    else:
        raise ValueError(f"{label} is required")
    if not value.strip():
        raise ValueError(f"{label} is empty")
    return value


def fingerprint(path: Path) -> dict[str, object]:
    resolved = path.expanduser().resolve()
    if not resolved.is_file():
        raise ValueError(f"source is not a file: {resolved}")
    digest = hashlib.sha256()
    with resolved.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    stat = resolved.stat()
    return {"path": str(resolved), "sha256": digest.hexdigest(), "size": stat.st_size}


def fingerprints(paths: Sequence[Path]) -> list[dict[str, object]]:
    return sorted((fingerprint(path) for path in paths), key=lambda item: str(item["path"]))


def write_text(path: Path | None, value: str) -> None:
    if path is None:
        sys.stdout.write(value)
        if not value.endswith("\n"):
            sys.stdout.write("\n")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def load_state(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("version") != STATE_VERSION or not isinstance(data.get("accepted_result"), str):
        raise ValueError("unsupported or invalid accepted-state file")
    return data


def add_text_pair(parser: argparse.ArgumentParser, name: str, label: str) -> None:
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(f"--{name}", help=label)
    group.add_argument(f"--{name}-file", type=Path, help=f"File containing {label.lower()}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    save = commands.add_parser("save", help="Replace state with one explicitly accepted result")
    save.add_argument("--state", required=True, type=Path)
    add_text_pair(save, "accepted", "Human-accepted result")
    request = save.add_mutually_exclusive_group()
    request.add_argument("--request")
    request.add_argument("--request-file", type=Path)
    save.add_argument("--source", action="append", default=[], type=Path)

    packet = commands.add_parser("packet", help="Build accepted-result plus requested-change packet")
    packet.add_argument("--state", required=True, type=Path)
    add_text_pair(packet, "change", "Requested change")
    packet.add_argument("--max-packet-bytes", type=int, default=16_000)
    packet.add_argument("--output", type=Path)

    lookup = commands.add_parser("lookup", help="Return accepted result only on exact request/source match")
    lookup.add_argument("--state", required=True, type=Path)
    add_text_pair(lookup, "request", "Current request")
    lookup.add_argument("--source", action="append", default=[], type=Path)
    lookup.add_argument("--output", type=Path)

    inspect = commands.add_parser("inspect", help="Show metadata without printing accepted content")
    inspect.add_argument("--state", required=True, type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "save":
            accepted = read_text(args.accepted, args.accepted_file, "accepted result")
            if SENSITIVE.search(accepted):
                raise ValueError("accepted result appears to contain a credential; redact it before saving")
            request = None
            if args.request is not None or args.request_file is not None:
                request = read_text(args.request, args.request_file, "request")
            data = {
                "version": STATE_VERSION,
                "accepted_result": accepted,
                "accepted_sha256": sha256_bytes(accepted.encode("utf-8")),
                "request_sha256": sha256_bytes(request.encode("utf-8")) if request is not None else None,
                "sources": fingerprints(args.source),
            }
            args.state.parent.mkdir(parents=True, exist_ok=True)
            args.state.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            print(json.dumps({key: value for key, value in data.items() if key != "accepted_result"}))
            return 0

        state = load_state(args.state)

        if args.command == "packet":
            change = read_text(args.change, args.change_file, "change")
            result = str(state["accepted_result"])
            packet = f"# Accepted result\n\n{result.rstrip()}\n\n# Requested change\n\n{change.rstrip()}\n"
            if len(packet.encode("utf-8")) > args.max_packet_bytes:
                raise ValueError("revision packet exceeds --max-packet-bytes; narrow the accepted artifact")
            write_text(args.output, packet)
            return 0

        if args.command == "lookup":
            request = read_text(args.request, args.request_file, "request")
            current_request = sha256_bytes(request.encode("utf-8"))
            current_sources = fingerprints(args.source)
            if state.get("request_sha256") != current_request or state.get("sources") != current_sources:
                print("accepted-state miss: request or source changed", file=sys.stderr)
                return 3
            write_text(args.output, str(state["accepted_result"]))
            return 0

        metadata = {key: value for key, value in state.items() if key != "accepted_result"}
        print(json.dumps(metadata, indent=2, sort_keys=True))
        return 0
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        print(f"accepted_state: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
