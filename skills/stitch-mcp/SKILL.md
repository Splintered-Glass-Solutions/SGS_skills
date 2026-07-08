---
name: stitch-mcp
description: Connect Codex to Google Stitch through the remote MCP endpoint and use Stitch projects as design context across repos. Use when a user wants to pull from Stitch, authenticate a Stitch MCP client, inspect or operate on Stitch projects, translate Stitch designs into product or code work, or troubleshoot Stitch MCP setup in Codex, Cursor, VSCode, Claude Code, Antigravity, or Gemini CLI.
---

# Stitch MCP

## Overview

Use Stitch as a remote MCP-backed design source. Prefer API-key auth for simpler local setup; use OAuth when the client or workflow requires short-lived access tokens tied to a Google Cloud project.

## Workflow

1. Confirm whether Stitch MCP is already exposed in the current session.
2. If not exposed, help the user configure their MCP client against `https://stitch.googleapis.com/mcp`.
3. Prefer API-key auth unless the user explicitly needs OAuth or project-billed access.
4. Once connected, use Stitch as design context for implementation, review, export, or project discovery work.
5. If setup or auth details are needed, read [authentication.md](./references/authentication.md).
6. If tool capabilities or likely operations are needed, read [tools-and-usage.md](./references/tools-and-usage.md).

## Default Approach

- Treat Stitch as upstream design context, not as the final implementation surface.
- Pull only the project or screens needed for the current task.
- Preserve a hard distinction between:
  - reusable skill instructions
  - local machine secret injection
- Do not bake live credentials into repo files, committed skill files, or shared examples.

## Auth Decision

- Use API key auth when the user already has a Stitch API key and wants the fastest setup path.
- Use OAuth when the client expects `Authorization: Bearer ...` and `X-Goog-User-Project`, or when the user explicitly wants the Google Cloud project flow.
- If the user pasted a live API key or token into chat, warn them to rotate it after setup or after the turn if exposure risk matters.

## Codex-Specific Guidance

- Check available MCP resources/templates first. If Stitch is not exposed in-session, say so plainly and shift into setup guidance.
- For Codex work, prefer helping the user attach Stitch MCP at the client level rather than inventing unsupported in-thread access.
- If the user wants a reusable local setup, write config snippets that use placeholders or local secrets, not embedded live credentials.
- If the user wants product or engineering work derived from Stitch, summarize what must be fetched from Stitch before implementation starts.

## Common Requests

- "Connect Codex/Cursor/VSCode/Claude Code to my Stitch project."
- "Pull the latest designs from Stitch and use them to implement this page."
- "What Stitch MCP config do I need for API key auth?"
- "Set up OAuth-based Stitch MCP access for my client."
- "What can Stitch MCP do once it is connected?"
- "Troubleshoot why my Stitch MCP client says unauthenticated."

## Output Expectations

- When configuring a client, provide the exact config format for that client.
- When discussing auth, state clearly whether the flow is API key or OAuth.
- When discussing OAuth, note that access tokens are short-lived and may need manual refresh.
- When the Stitch server is unavailable in-session, state that explicitly instead of implying live access.

## References

- [authentication.md](./references/authentication.md)
- [tools-and-usage.md](./references/tools-and-usage.md)
