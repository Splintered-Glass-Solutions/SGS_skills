#!/usr/bin/env python3
"""Check public artifacts for private bindings and broken local dependencies.

This is a deterministic gate, not proof that arbitrary prose is privacy-safe.
Semantic review of each publication diff remains required. Diagnostics never echo
matched credentials or personal content. Requires Python 3.10+; YAML is checked
separately by validate-skill-metadata.rb.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
RULES = {
    "personal-home-path": re.compile(r"/(?:Users|home)/[A-Za-z0-9_.-]+(?=/)|[A-Z]:\\Users\\[A-Za-z0-9_.-]+", re.I),
    "numbered-private-project-copy": re.compile(r"example-project-\d+"),
    "private-key": re.compile(r"-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----"),
    "provider-credential": re.compile(r"\b(?:AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{25,}|sk-(?:proj-)?[A-Za-z0-9_-]{30,})\b"),
    "live-provider-id": re.compile(r"\barn:aws:[^\s]*:\d{12}:|\b(?:prj|team)_[A-Za-z0-9]{16,}\b"),
    "private-automation-path": re.compile(r"(?:<agent-config>|\.codex)/automations/[a-z0-9]+(?:-[a-z0-9]+)+/"),
}
EMAIL = re.compile(r"(?<![\w.-])[\w.+%-]+@([\w.-]+\.[A-Za-z]{2,})")
UUID = re.compile(r"\b[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b", re.I)
URL = re.compile(r"https?://[^\s<>\x60\x22\x27)\]]+")
LINK = re.compile(r"(?<!!)\[[^\]\n]*\]\((<[^>]+>|[^)\n]+)\)")


def scan_text(text: str, hosts: set[str]) -> list[tuple[int, str]]:
    findings = []
    for number, line in enumerate(text.splitlines(), 1):
        for rule, pattern in RULES.items():
            if pattern.search(line):
                findings.append((number, rule))
        for match in EMAIL.finditer(line):
            domain = match[1].lower()
            if domain not in {"example.com", "example.org", "example.net"} and not domain.endswith((".example", ".invalid", ".test")):
                findings.append((number, "non-example-email"))
        for match in UUID.finditer(line):
            if match[0] != "00000000-0000-0000-0000-000000000000":
                findings.append((number, "non-example-resource-id"))
        for match in URL.finditer(line):
            host = (urlsplit(match[0]).hostname or "").lower()
            if not host or any(c in host for c in "{}$…") or host in {"...", "localhost", "127.0.0.1", "::1"}:
                continue
            if host in hosts or host in {"example.com", "example.org", "example.net"} or host.endswith((".example.com", ".example.org", ".example.net", ".example", ".invalid", ".test")):
                continue
            findings.append((number, "unreviewed-public-host"))
    return sorted(set(findings))


def markdown_checks(path: Path, text: str) -> list[tuple[int, str]]:
    findings = []
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if match:
            value = match[1]
            if fence is None:
                fence = value
            elif value[0] == fence[0] and len(value) >= len(fence):
                fence = None
            continue
        if fence:
            continue
        for match in LINK.finditer(line):
            target = match[1].strip("<>").split("#", 1)[0]
            if not target or re.match(r"[a-z][a-z0-9+.-]*:", target, re.I) or any(c in target for c in "<>${}|*"):
                continue
            # Markdown titles are not part of the target filename.
            target = target.split(' "', 1)[0]
            if not (path.parent / unquote(target)).exists():
                findings.append((number, "missing-relative-link"))
    if fence:
        findings.append((len(text.splitlines()), "unclosed-markdown-fence"))
    return findings


def validate(root: Path) -> tuple[list[str], int]:
    hosts = set(json.loads((root / "scripts/public-hosts.json").read_text()))
    problems = []
    count = 0
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if any(part in {".git", "__pycache__", "node_modules"} for part in rel.parts):
            continue
        if path.is_symlink():
            problems.append(f"{rel}: symlink-requires-review")
            continue
        if not path.is_file():
            continue
        if path.name == ".env" or path.name.startswith(".env.") or path.suffix in {".log", ".sqlite", ".db", ".pem", ".key", ".pyc"}:
            problems.append(f"{rel}: forbidden-public-artifact")
            continue
        data = path.read_bytes()
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            # Bundled icons/fonts/licenses are reviewed separately; never skip
            # an unknown binary that could contain live state or credentials.
            if path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".woff", ".woff2", ".ttf"}:
                problems.append(f"{rel}: unreviewed-binary")
            continue
        count += 1
        problems.extend(f"{rel}:{line}: {rule}" for line, rule in scan_text(text, hosts))
        if path.suffix.lower() in {".md", ".markdown"}:
            problems.extend(f"{rel}:{line}: {rule}" for line, rule in markdown_checks(path, text))
        if path.suffix == ".py":
            try:
                ast.parse(text)
            except SyntaxError as error:
                problems.append(f"{rel}:{error.lineno}: invalid-python")
    return problems, count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    problems, count = validate(args.root.resolve())
    if problems:
        print("\n".join(problems))
        print(f"FAIL: {len(problems)} finding(s) across {count} text files")
        return 1
    print(f"PASS: {count} text files; privacy patterns, URL hosts, local links, Markdown fences and Python syntax")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
