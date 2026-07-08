# Stitch MCP Tools And Usage

Use this file when deciding what Stitch MCP is for after connection is working.

## Primary Uses

- Pull design project context into implementation work
- Inspect existing Stitch projects and screens
- Generate or manage design variants
- Edit screens or layouts through Stitch-backed workflows
- Download artifacts and move from design to code
- Use Stitch as upstream product/design truth during coding tasks

## Typical Tool Categories

The Stitch docs describe tool coverage in categories like:

- Project management
  - `create_project`
  - `get_project`
  - `list_projects`
- Design system creation
  - `create_design_system`
- Additional design and artifact workflows
  - screen editing
  - variant generation
  - artifact download
  - theme extraction

Check the live Stitch MCP reference when exact schemas or argument names matter.

## Recommended Working Pattern

1. Connect Stitch MCP.
2. Discover the relevant project or screen.
3. Pull only the design context needed for the current task.
4. Translate the design into code, product documentation, or implementation planning.
5. If the user wants iterative design/code loops, keep Stitch as the design-side system and the repo as the implementation-side system.

## Good Prompts

- "Use Stitch MCP to list my projects and identify the one that matches this feature branch."
- "Use Stitch MCP to inspect the target screen, then implement the matching page in this repo."
- "Use Stitch MCP to pull the latest design context for this flow and summarize the intended UX."
- "Use Stitch MCP to review the existing screen before making code changes."

## Guardrails

- Do not claim live Stitch access unless the MCP server is actually exposed in-session.
- Do not infer exact tool schemas if the live reference is unavailable.
- Do not treat Stitch as a backend or source of runtime business data; treat it as design context.
