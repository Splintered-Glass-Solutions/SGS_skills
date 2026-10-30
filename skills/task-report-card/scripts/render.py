#!/usr/bin/env python3
"""Render a standalone task report card from a JSON data file."""
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    data = json.loads(args.data.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("sections"), list):
        parser.error("input must be an object with a sections array")
    for section in data["sections"]:
        if not isinstance(section.get("items"), list):
            parser.error("each section needs an items array")
        for item in section["items"]:
            if item.get("status") not in {"done", "local_working", "blocked", "progress", "not_started"}:
                parser.error("each item needs a valid status")
    template = (Path(__file__).resolve().parents[1] / "assets/report-card.html").read_text(encoding="utf-8")
    marker = "__TASK_REPORT_DATA__"
    if template.count(marker) != 1:
        raise ValueError("template must contain exactly one data marker")
    encoded = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    encoded = encoded.replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(template.replace(marker, encoded), encoding="utf-8")
    print(f"Rendered {args.output} with {sum(len(s['items']) for s in data['sections'])} entries")


if __name__ == "__main__":
    main()
