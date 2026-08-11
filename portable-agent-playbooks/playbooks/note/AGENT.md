# Note Agent Playbook

This is a platform-neutral version of the `note` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Save a concise planning note from the current conversation for later reference without taking follow-on action. Use when the user says to note, remember, jot down, save for later, or invokes /note.

## Portability Notes

- Replace `<agent-config>` with the local configuration folder for the
  target agent platform.
- Replace `<workspace>` with the user's active project/workspace root.
- Treat slash commands and `$skill-name` references as invocation hints.
  If the target platform does not support slash commands, paste this
  playbook into the agent's custom instructions or project memory.
- Keep all original safety gates. Do not send messages, deploy, mutate
  production data, change permissions, or perform irreversible actions
  without explicit approval from the user.
- If a referenced connector or tool is not available in the target platform,
  stop and report the missing capability instead of simulating external
  actions.

## Instructions

# Note

Use this skill to preserve a brief decision, constraint, reminder, or idea from
the active conversation. This is capture only, never a request to plan, build,
message, deploy, or modify a product.

## Capture Rules

1. Treat the invoked text or the user's immediately preceding note as the note
   content. If neither is clear, ask one short question for the note.
2. Infer a concise initiative label from the active thread when it is obvious;
   otherwise use `general-planning`.
3. Save one small Markdown file under
   `<agent-config>/memories/extensions/ad_hoc/notes/` named
   `YYYY-MM-DD-<initiative>-note.md`. Add a short time suffix if that filename
   already exists.
4. Use this exact structure:

   ```markdown
   # <Initiative> planning note

   - Captured: YYYY-MM-DD
   - Context: current planning conversation

   <The concise note>
   ```

5. Never store secrets, API keys, private tokens, full sensitive transcripts,
   personal data, or copied credentials. Redact those items and preserve only
   the non-sensitive decision when possible.

## Boundaries

- Do not inspect repositories, run builds, edit product files, change settings,
  send messages, create tasks, or perform any external action.
- Do not turn the note into a plan, recommend next steps, or add speculative
  work.
- Do not overwrite an existing note.
- Do not save a note to a Git repository.

## Response

After a successful save, return only `Noted.` Do not send commentary.
If the note cannot be saved or is unsafe to store, return one concise sentence
explaining why.
