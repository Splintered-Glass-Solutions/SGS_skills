#!/usr/bin/env python3
"""Find an existing Bonfire marketing asset package for a feature."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "bonfire-feature"


def default_roots() -> list[Path]:
    roots: list[Path] = []
    cwd = Path.cwd()
    roots.append(cwd / "output" / "marketing-assets")
    roots.append(Path.home() / "Marketing Assets" / "Bonfire")
    return roots


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--feature-name", required=True)
    parser.add_argument("--search-root", action="append", default=[])
    return parser.parse_args()


def load_manifest(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def matches(manifest: dict[str, Any], manifest_path: Path, feature_name: str) -> bool:
    expected = feature_name.strip().casefold()
    expected_slug = slugify(feature_name)
    manifest_feature = str(manifest.get("feature_name", "")).strip().casefold()
    if manifest_feature == expected:
        return True
    return expected_slug in str(manifest_path.parent.name).casefold()


def summarize(manifest: dict[str, Any], manifest_path: Path) -> dict[str, Any]:
    assets = manifest.get("assets")
    asset_rows = assets if isinstance(assets, list) else []
    status_counts: dict[str, int] = {}
    personas: list[str] = []
    for row in asset_rows:
        if not isinstance(row, dict):
            continue
        status = str(row.get("image_status", "unknown"))
        status_counts[status] = status_counts.get(status, 0) + 1
        persona = str(row.get("persona", "")).strip()
        if persona and persona not in personas:
            personas.append(persona)
    return {
        "found": True,
        "package_path": str(manifest_path.parent),
        "manifest_path": str(manifest_path),
        "feature_name": manifest.get("feature_name"),
        "live_status": manifest.get("live_status"),
        "asset_count": len(asset_rows),
        "status_counts": status_counts,
        "personas": personas,
        "screenshots": manifest.get("screenshots", []),
    }


def main() -> int:
    args = parse_args()
    roots = [
        Path(root).expanduser()
        for root in (args.search_root or [str(root) for root in default_roots()])
    ]
    candidates: list[tuple[float, Path, dict[str, Any]]] = []
    for root in roots:
        if not root.exists():
            continue
        for manifest_path in root.rglob("asset-manifest.json"):
            manifest = load_manifest(manifest_path)
            if manifest and matches(manifest, manifest_path, args.feature_name):
                candidates.append(
                    (manifest_path.stat().st_mtime, manifest_path, manifest)
                )
    if not candidates:
        print(
            json.dumps(
                {
                    "found": False,
                    "feature_name": args.feature_name,
                    "searched_roots": [str(root) for root in roots],
                },
                indent=2,
            )
        )
        return 1

    _, manifest_path, manifest = sorted(candidates, key=lambda item: item[0])[-1]
    print(json.dumps(summarize(manifest, manifest_path), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
