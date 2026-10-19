# Standalone report renderer

Use `assets/project-update.html` and `scripts/render_update.py` for the approved connected-workstream layout. The template is project-neutral. The renderer embeds the chosen logo as a data URL, escapes text, and emits a standalone HTML document. It does not fetch branding, publish, or send messages.

Create a project-owned JSON file with these fields:

```json
{
  "project": "Exact client or project name",
  "title": "Project update",
  "prepared_by": "Actual preparer or firm",
  "focus": "One sentence describing the current focus.",
  "logo_path": "Optional local logo path relative to this JSON file",
  "colors": {
    "brand": "#334155",
    "header": "#1e293b",
    "header_ink": "#ffffff",
    "ink": "#17202a",
    "muted": "#475569",
    "canvas": "#fafafa",
    "soft": "#f1f5f9",
    "line": "#cbd5e1"
  },
  "workstreams": [
    {"name": "Actual workstream", "done": "Verified outcome.", "upcoming": "Planned next activity.", "needed": "Specific client input and owner if known."}
  ],
  "checkpoint": "Observable next checkpoint.",
  "validation": "Optional material remaining acceptance gap.",
  "later_scope": "Optional deferred scope."
}
```

The colors above are neutral defaults, not a client palette. Replace them with discovered project tokens. Omit `logo_path` for a text wordmark; otherwise supply a real readable PNG, JPEG, WebP, GIF or SVG. SVGs should be trusted project assets. Optional `validation` and `later_scope` fields disappear when absent. An empty workstream cell renders “No item identified in this update”; use that only when it accurately describes the evidence.

Render from any directory using absolute paths:

```sh
python3 /absolute/path/to/client-call-update/scripts/render_update.py /absolute/project/output/update.json /absolute/project/output/project-update.html
```

The JSON may contain local branding paths and remains an internal source file. Share the generated HTML. Keep the underlying date window, claim citations, and branding provenance in the project's separate evidence record. Adapt CSS or markup if the user requests a different layout; do not hardcode a particular client's content into the shared template.
