#!/usr/bin/env python3
"""Render a portable client update from project-specific JSON and local branding."""
import argparse
import base64
import html
import json
import mimetypes
from pathlib import Path
import re

def render(source, destination):
    data = json.loads(source.read_text())
    escape = lambda value: html.escape(str(value), quote=True)
    defaults = {"brand":"#334155", "header":"#1e293b", "header_ink":"#ffffff", "ink":"#17202a", "muted":"#475569", "canvas":"#fafafa", "soft":"#f1f5f9", "line":"#cbd5e1"}
    colors = {**defaults, **data.get("colors", {})}
    for name in defaults:
        if not re.fullmatch(r"#[0-9a-fA-F]{6}", colors[name]):
            raise ValueError(f"Invalid six-digit hex color: {name}")
    project = escape(data["project"])
    mark = f'<span class="wordmark">{project}</span>'
    if data.get("logo_path"):
        logo = Path(data["logo_path"])
        if not logo.is_absolute():
            logo = source.parent / logo
        mime = mimetypes.guess_type(logo.name)[0]
        if mime not in {"image/png", "image/jpeg", "image/webp", "image/gif", "image/svg+xml"}:
            raise ValueError("Use a PNG, JPEG, WebP, GIF or SVG logo")
        encoded = base64.b64encode(logo.read_bytes()).decode("ascii")
        mark = f'<img class="logo" src="data:{mime};base64,{encoded}" alt="{project}">'
    rows = []
    for i, row in enumerate(data["workstreams"]):
        name = escape(row["name"])
        cells = []
        for key, label in (("done","Done"),("upcoming","Upcoming · planned"),("needed","Needed from your team")):
            cells.append(f'<section class="cell" aria-label="{label}"><span class="cell-label" aria-hidden="true">{label}</span><p>{escape(row.get(key) or "No item identified in this update.")}</p></section>')
        rows.append(f'<article class="workstream" aria-labelledby="workstream-{i}"><h2 id="workstream-{i}">{name}</h2>{"".join(cells)}</article>')
    tokens = {name.upper(): value for name, value in colors.items() if name in defaults}
    tokens.update({"DOCUMENT_TITLE":f'{project} — {escape(data.get("title", "Project update"))}', "BRAND_MARK":mark, "PREPARED_BY":escape(data.get("prepared_by", "")), "TITLE":escape(data.get("title", "Project update")), "FOCUS":escape(data["focus"]), "WORKSTREAMS":"\n".join(rows), "CHECKPOINT":escape(data["checkpoint"]), "VALIDATION":f'<p class="validation"><strong>Remaining validation:</strong> {escape(data["validation"])}</p>' if data.get("validation") else "", "LATER_SCOPE":f'<footer>{escape(data["later_scope"])}</footer>' if data.get("later_scope") else ""})
    template = Path(__file__).resolve().parents[1] / "assets/project-update.html"
    document = template.read_text()
    document = re.sub(r"\{\{([A-Z_]+)\}\}", lambda match: tokens[match.group(1)], document)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(document)
    print(destination.resolve())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    render(args.source.resolve(), args.destination.resolve())
