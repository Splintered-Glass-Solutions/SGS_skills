# Claude / Claude Code Adapter

Use these playbooks as project-level instructions or command-specific
prompts.

## Claude Project

1. Open the Claude project.
2. Add the relevant `AGENT.md` contents to project instructions or knowledge.
3. Upload any referenced templates or reference docs from the playbook folder.
4. Tell Claude which tools are available and which actions require approval.

## Claude Code

Recommended pattern:

- Put persistent project guidance in `CLAUDE.md`.
- Put specific playbooks in a `playbooks/` or `agent-playbooks/` folder.
- Start a session with: `Use the <name> playbook from <path> for this task.`

## Tool Mapping

- Shell commands: Claude Code terminal.
- File edits: Claude Code patch/edit flow.
- Browser checks: Playwright, browser MCP, or a platform browser tool.
- External services: use real connectors only when available and authorized.
- Memory/ledgers: use local markdown/jsonl files if the platform has no native
  memory API.
