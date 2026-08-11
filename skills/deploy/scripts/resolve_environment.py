#!/usr/bin/env python3
"""Resolve a deployment environment from the shared deploy registry."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse


SKILL_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = SKILL_ROOT / "references" / "environment-registry.json"
ENVIRONMENT_ALIASES = {
    "development": "dev",
    "prod": "production",
    "stage": "staging",
}


def fail(message: str, exit_code: int = 1) -> None:
    print(f"BLOCKED: {message}", file=sys.stderr)
    raise SystemExit(exit_code)


def load_registry() -> dict:
    try:
        return json.loads(REGISTRY_PATH.read_text())
    except (OSError, json.JSONDecodeError) as error:
        fail(f"could not load {REGISTRY_PATH}: {error}")


def canonical_remote(remote: str) -> str:
    value = remote.strip()
    if value.startswith("git@") and ":" in value:
        host, path = value[4:].split(":", 1)
        value = f"https://{host}/{path}"
    parsed = urlparse(value)
    if parsed.scheme and parsed.netloc:
        value = f"https://{parsed.netloc}{parsed.path}"
    return value.removesuffix("/").removesuffix(".git").lower()


def read_remote(repo: Path) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(repo), "remote", "get-url", "origin"],
        capture_output=True,
        check=False,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def find_project(registry: dict, repo: Path | None, project_name: str | None) -> dict:
    projects = registry.get("projects", [])
    matches: list[dict] = []

    if project_name:
        normalized = project_name.lower()
        matches = [
            project
            for project in projects
            if normalized == project.get("project", "").lower()
            or normalized in {alias.lower() for alias in project.get("aliases", [])}
        ]
    elif repo:
        resolved_repo = repo.resolve()
        remote = read_remote(resolved_repo)
        canonical = canonical_remote(remote) if remote else None
        for project in projects:
            paths = {Path(path).resolve() for path in project.get("repositories", [])}
            remotes = {
                canonical_remote(value) for value in project.get("git_remotes", [])
            }
            if resolved_repo in paths or (canonical and canonical in remotes):
                matches.append(project)
    else:
        fail("supply --repo or --project")

    if len(matches) != 1:
        identity = f"project={project_name!r}" if project_name else f"repo={str(repo)!r}"
        fail(f"no unique deployment mapping exists for {identity}")
    return matches[0]


def resolve(args: argparse.Namespace) -> None:
    registry = load_registry()
    repo = Path(args.repo) if args.repo else None
    project = find_project(registry, repo, args.project)
    environments = project.get("environments", [])
    supplied_environment = args.environment.lower() if args.environment else None
    requested = ENVIRONMENT_ALIASES.get(supplied_environment, supplied_environment)

    if requested:
        matches = [environment for environment in environments if environment.get("name") == requested]
        if len(matches) != 1:
            choices = ", ".join(environment.get("name", "<unnamed>") for environment in environments)
            fail(f"environment {requested!r} is not mapped for {project['project']}; choose one of: {choices}")
        selected = matches[0]
        resolution = "explicit"
    else:
        if not project.get("allow_implicit_environment") or len(environments) != 1:
            choices = ", ".join(environment.get("name", "<unnamed>") for environment in environments)
            fail(f"{project['project']} requires an explicit environment; choose one of: {choices}")
        selected = environments[0]
        resolution = "implicit-single-environment"

    result = {
        "project": project["project"],
        "environment": selected["name"],
        "resolution": resolution,
        "provider": selected.get("provider"),
        "provider_target": selected.get("provider_target"),
        "provider_project": selected.get("provider_project"),
        "source_branch": selected.get("source_branch"),
        "stable_url": selected.get("stable_url"),
        "identity_gate": selected.get("identity_gate"),
        "deploy_authorized": False,
    }
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        for key, value in result.items():
            print(f"{key}={json.dumps(value) if value is None or isinstance(value, bool) else value}")


def list_projects(_: argparse.Namespace) -> None:
    registry = load_registry()
    for project in registry.get("projects", []):
        environments = ",".join(item["name"] for item in project.get("environments", []))
        implicit = "yes" if project.get("allow_implicit_environment") else "no"
        print(f"{project['project']}: environments={environments} implicit={implicit}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(required=True)

    resolve_parser = commands.add_parser("resolve")
    resolve_parser.add_argument("--repo")
    resolve_parser.add_argument("--project")
    resolve_parser.add_argument("--environment")
    resolve_parser.add_argument("--json", action="store_true")
    resolve_parser.set_defaults(func=resolve)

    list_parser = commands.add_parser("list")
    list_parser.set_defaults(func=list_projects)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
