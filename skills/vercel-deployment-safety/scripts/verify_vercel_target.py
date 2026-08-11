#!/usr/bin/env python3
"""Read-only, fail-closed verifier for an approved Vercel deployment target."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = SKILL_ROOT / "references" / "project-registry.json"


def fail(message: str) -> None:
    print(f"BLOCKED: {message}", file=sys.stderr)
    raise SystemExit(1)


def run_git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args], text=True, capture_output=True, check=False
    )
    if result.returncode != 0:
        fail(f"could not read Git metadata for {repo}: {result.stderr.strip() or 'unknown error'}")
    return result.stdout.strip()


def load_registry() -> dict:
    try:
        return json.loads(REGISTRY_PATH.read_text())
    except (OSError, json.JSONDecodeError) as error:
        fail(f"could not load registry {REGISTRY_PATH}: {error}")


def find_entry(registry: dict, client: str, app: str) -> dict:
    matches = [
        entry for entry in registry.get("entries", [])
        if entry.get("client") == client and entry.get("app") == app
    ]
    if len(matches) != 1:
        fail(f"no unique registry entry exists for client={client!r}, app={app!r}")
    return matches[0]


def read_local_vercel_link(repo: Path) -> dict:
    link_path = repo / ".vercel" / "project.json"
    if not link_path.is_file():
        fail(f"missing local Vercel metadata: {link_path}")
    try:
        return json.loads(link_path.read_text())
    except json.JSONDecodeError as error:
        fail(f"invalid local Vercel metadata at {link_path}: {error}")


def verify(args: argparse.Namespace) -> None:
    registry = load_registry()
    entry = find_entry(registry, args.client, args.app)
    repo = Path(args.repo).resolve()
    expected_repo = Path(entry["repository"]).resolve()

    failures: list[str] = []
    if repo != expected_repo:
        failures.append(f"repository path is {repo}, expected exact approved path {expected_repo}")
    if not repo.is_dir():
        failures.append(f"repository does not exist: {repo}")
    if failures:
        fail("; ".join(failures))

    remote = run_git(repo, "remote", "get-url", "origin")
    if remote != entry["git_remote"]:
        failures.append(f"origin is {remote!r}, expected {entry['git_remote']!r}")

    link = read_local_vercel_link(repo)
    for key in ("projectId", "orgId", "projectName"):
        expected_key = {"projectId": "project_id", "orgId": "team_id", "projectName": "project_name"}[key]
        if link.get(key) != entry[expected_key]:
            failures.append(
                f".vercel/project.json {key} is {link.get(key)!r}, expected {entry[expected_key]!r}"
            )

    if failures:
        fail("; ".join(failures))

    print("TARGET VERIFIED (read-only; this is not deployment authorization)")
    print(f"client={entry['client']}")
    print(f"app={entry['app']}")
    print(f"repo={repo}")
    print(f"scope={entry['vercel_scope']}")
    print(f"team_id={entry['team_id']}")
    print(f"project_id={entry['project_id']}")
    print(f"environment_requested={args.environment}")
    print("next_gate=obtain explicit approval before any Vercel or GitHub write action")


def list_entries(_: argparse.Namespace) -> None:
    registry = load_registry()
    for entry in registry.get("entries", []):
        print(f"{entry['client']}/{entry['app']}: {entry['repository']} -> {entry['vercel_scope']}/{entry['project_name']} ({entry['project_id']})")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(required=True)
    list_parser = commands.add_parser("list", help="List explicitly mapped targets")
    list_parser.set_defaults(func=list_entries)
    verify_parser = commands.add_parser("verify", help="Fail unless repo and local Vercel link match a mapped target")
    verify_parser.add_argument("--client", required=True)
    verify_parser.add_argument("--app", required=True)
    verify_parser.add_argument("--repo", required=True)
    verify_parser.add_argument("--environment", required=True, choices=("preview", "staging", "production"))
    verify_parser.set_defaults(func=verify)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
