---
name: ninety-rock-entry
description: Add Rocks and milestones into Ninety/EOS from prepared rock-copy text or an HTML copyboard. Use when the user wants Codex to enter quarterly Rocks, owners, due dates, outcomes/descriptions, and milestones in the Ninety web app, especially after demonstrating the workflow with Record & Replay.
---

# Ninety Rock Entry

## Overview

Use this skill to enter planned Rocks into Ninety with their milestone breakdowns. The workflow was learned from a Record & Replay capture on the Ninety quarterly meeting Rocks page.

## Source Content

- Prefer a prepared copyboard or source doc with one rock title, outcome/description, and milestone list per rock.
- Do not invent or rewrite the content while entering it unless the user explicitly asks.
- If an HTML copyboard exists, use its copy buttons or parse its embedded `rocks` data to prepare reliable copy text.
- Preserve milestone titles as the first line and milestone detail as the body.

## Ninety Entry Workflow

1. Open Ninety to the quarterly meeting Rocks page. In the recorded workflow this was `eos.ninety.io/.../quarterly/rocks/rocks`.
2. Click `ROCKS` in the meeting navigation if needed, then select the `Rocks` tab.
3. Click `Create`.
4. Paste the Rock title into `Add a title for the Rock...`.
5. Paste the Rock outcome/description into the rich-text description area.
6. Set `Quarter` to the intended quarter, usually `Q3 FY 2026` for the StrIQ Q3 planning workflow.
7. Confirm due date and owner/team if the user specified them. If not specified, leave Ninety's current defaults unless the user instructs otherwise.
8. Click `Create Rock`.
9. Open the created Rock detail if Ninety does not open it automatically.
10. For each milestone, click `Add Milestone for <Rock title>`.
11. Paste the milestone text in the form:
    ```text
    Milestone Title

    Milestone detail sentence or paragraph.
    ```
12. Ninety may put the whole pasted block into the title first. Click into the description area so Ninety splits the first line into `Title` and the remainder into the body. If it does not split cleanly, manually move the first line into `Title` and leave the detail text in the description/body field.
13. Click `Add`.
14. Repeat for each milestone, then verify the Rock detail shows the expected milestone count and names.

## Automation Guidance

- Use Computer Use or browser-control tools for live Ninety UI work; there is no known stable connector for semantic Ninety Rock creation.
- Prefer accessibility labels over coordinates: `Create`, `Create Rock`, `Add Milestone for ...`, `Title`, and the rich-text description area were visible in the recording.
- After each Rock, verify the visible table/detail page shows the created title before adding milestones.
- After each milestone, verify it appears in the milestone list before moving on.
- If a save/add action appears to do nothing, wait for loading indicators to settle and inspect whether the title field, description field, or required quarter/owner field is still invalid.
- Avoid changing statuses unless asked. Newly created milestones and Rocks should remain in Ninety's default status.

## Validation Checklist

- Created Rock title matches source.
- Description/outcome matches source.
- Quarter and due date match the requested planning period.
- Milestone count matches source.
- Each milestone title is not accidentally duplicated into the milestone body.
- No unrelated existing Rocks were edited.
