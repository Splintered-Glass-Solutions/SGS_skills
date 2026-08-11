#!/usr/bin/env python3
"""Select bounded, relevant passages from local text sources without a model call."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

TEXT_SUFFIXES = {
    ".csv", ".html", ".js", ".json", ".jsx", ".log", ".md", ".py", ".sql",
    ".toml", ".ts", ".tsx", ".txt", ".xml", ".yaml", ".yml",
}
SKIP_DIRS = {".git", ".next", ".venv", "build", "dist", "node_modules", "vendor"}
SENSITIVE_NAMES = {".env", ".npmrc", ".pypirc", "credentials", "credentials.json"}
STOP_WORDS = {
    "about", "after", "again", "also", "and", "are", "did", "does", "for", "from",
    "have", "into", "need", "that", "the", "this", "what", "when", "where", "which",
    "with", "would", "your",
}


@dataclass(frozen=True)
class Chunk:
    path: Path
    start: int
    end: int
    text: str
    score: int


def terms(request: str) -> tuple[str, ...]:
    found = re.findall(r"[A-Za-z0-9][A-Za-z0-9_.:/-]{2,}", request.lower())
    return tuple(dict.fromkeys(word for word in found if word not in STOP_WORDS))


def safe_candidate(path: Path) -> bool:
    return (
        path.is_file()
        and path.suffix.lower() in TEXT_SUFFIXES
        and path.name.lower() not in SENSITIVE_NAMES
        and not any(part in SKIP_DIRS for part in path.parts)
    )


def candidates(sources: Iterable[Path], root: Path | None, max_files: int) -> list[Path]:
    found: list[Path] = []
    for source in sources:
        resolved = source.expanduser().resolve()
        if safe_candidate(resolved):
            found.append(resolved)
    if root is not None:
        base = root.expanduser().resolve()
        for path in base.rglob("*"):
            if len(found) >= max_files:
                break
            if safe_candidate(path):
                found.append(path.resolve())
    return list(dict.fromkeys(found))[:max_files]


def make_chunks(path: Path, query_terms: Sequence[str], lines_per_chunk: int, overlap: int) -> list[Chunk]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    result: list[Chunk] = []
    step = max(1, lines_per_chunk - overlap)
    for offset in range(0, len(lines), step):
        block = lines[offset : offset + lines_per_chunk]
        if not block:
            continue
        text = "\n".join(block).strip()
        lower = text.lower()
        score = sum(lower.count(term) for term in query_terms)
        if score:
            result.append(Chunk(path, offset + 1, offset + len(block), text, score))
    return result


def render(chunk: Chunk) -> str:
    return f"## {chunk.path} lines {chunk.start}-{chunk.end}\n\n{chunk.text}\n"


def write(path: Path | None, value: str) -> None:
    if path is None:
        sys.stdout.write(value)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    request = parser.add_mutually_exclusive_group(required=True)
    request.add_argument("--request")
    request.add_argument("--request-file", type=Path)
    parser.add_argument("--source", action="append", default=[], type=Path)
    parser.add_argument("--root", type=Path)
    parser.add_argument("--max-packet-bytes", type=int, default=12_000)
    parser.add_argument("--max-file-bytes", type=int, default=4_000_000)
    parser.add_argument("--max-files", type=int, default=200)
    parser.add_argument("--lines-per-chunk", type=int, default=36)
    parser.add_argument("--overlap", type=int, default=6)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--report", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        request = args.request if args.request is not None else args.request_file.read_text(encoding="utf-8")
        query_terms = terms(request)
        if not query_terms:
            raise ValueError("request has no useful search terms")
        paths = candidates(args.source, args.root, args.max_files)
        if not paths:
            raise ValueError("no safe text sources found")

        chunks: list[Chunk] = []
        skipped: list[str] = []
        for path in paths:
            if path.stat().st_size > args.max_file_bytes:
                skipped.append(f"{path}: exceeds max file bytes")
                continue
            chunks.extend(make_chunks(path, query_terms, args.lines_per_chunk, args.overlap))
        chunks.sort(key=lambda item: (-item.score, str(item.path), item.start))

        selected: list[Chunk] = []
        used = 0
        for chunk in chunks:
            block = render(chunk)
            size = len(block.encode("utf-8"))
            if used + size > args.max_packet_bytes:
                continue
            selected.append(chunk)
            used += size

        packet = "\n".join(render(chunk).rstrip() for chunk in selected)
        if packet:
            packet += "\n"
        report = {
            "terms": query_terms,
            "files_considered": len(paths),
            "matching_chunks": len(chunks),
            "selected_chunks": [
                {"path": str(chunk.path), "start": chunk.start, "end": chunk.end, "score": chunk.score}
                for chunk in selected
            ],
            "packet_bytes": len(packet.encode("utf-8")),
            "skipped": skipped,
            "needs_bounded_expansion": not selected or len(selected) < len(chunks),
        }
        write(args.output, packet)
        if args.report is not None:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        elif args.output is not None:
            print(json.dumps(report))
        return 0 if selected else 3
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"select_context: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
