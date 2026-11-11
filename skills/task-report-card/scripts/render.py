#!/usr/bin/env python3
"""Render a standalone task report card from a JSON data file."""
import argparse
from datetime import datetime, timedelta
import json
import os
from pathlib import Path
import tempfile


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
            if item.get("status") not in {"done", "verified_dev", "local_working", "blocked", "progress", "not_started", "deferred"}:
                parser.error("each item needs a valid status")
            proof = item.get("localProof") or {}
            if not isinstance(proof, dict) or not isinstance(proof.get("story") or {}, dict):
                parser.error("localProof and its story must be objects")
            story = proof.get("story") or {}
            if item["status"] == "local_working" and story.get("status") in {"failed", "incomplete"}:
                parser.error("a failed or incomplete user story must be in progress or blocked")
            dev_proof = item.get("devProof") or {}
            if not isinstance(dev_proof, dict):
                parser.error("devProof must be an object")
            if item["status"] == "verified_dev" and (dev_proof.get("status") != "passed" or not dev_proof.get("evidence")):
                parser.error("Verified in Dev requires passing, evidence-linked Dev proof")
    # Record observed report entries, not inferred historical task states.
    statuses = ("done", "verified_dev", "local_working", "blocked", "progress", "not_started", "deferred")
    counts = {status: 0 for status in statuses}
    for section in data["sections"]:
        for item in section["items"]:
            counts[item["status"]] += 1
    history = data.setdefault("statusHistory", [])
    if not isinstance(history, list):
        parser.error("statusHistory must be an array")
    for point in history:
        if (not isinstance(point, dict) or not isinstance(point.get("at"), str)
                or not isinstance(point.get("counts"), dict)
                or any(type(point["counts"].get(k, 0)) is not int or point["counts"].get(k, 0) < 0 for k in statuses)):
            parser.error("statusHistory contains an invalid snapshot")
    # Keep report details current while limiting chart points to one per 30 minutes.
    update_label = str(data.get("updated", ""))
    now = datetime.now().astimezone()
    try:
        last_at = datetime.fromisoformat(history[-1]["at"]) if history else None
        if last_at is not None and last_at.utcoffset() is None:
            parser.error("statusHistory timestamps must include a timezone")
    except ValueError:
        parser.error("statusHistory contains an invalid timestamp")
    changed = not history or any(history[-1]["counts"].get(status, 0) != counts[status] for status in statuses)
    if changed and (last_at is None or now - last_at >= timedelta(minutes=30)):
        history.append({"at": now.isoformat(timespec="seconds"),
                        "updateLabel": update_label, "counts": counts})
        # Replace atomically so a failed write cannot leave truncated JSON.
        fd, name = tempfile.mkstemp(prefix="." + args.data.name + ".", dir=args.data.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as out:
                json.dump(data, out, ensure_ascii=False, indent=2)
                out.write("\n")
            os.chmod(name, args.data.stat().st_mode & 0o777)
            os.replace(name, args.data)
        finally:
            if os.path.exists(name):
                os.unlink(name)
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
