# Email Triage Agent Playbook

This is a platform-neutral version of the `email-triage` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Review connected email accounts for messages that need a reply today, rank them, and prepare reply guidance for the highest-priority messages without sending.

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

# Email Triage

Use when the user asks to find emails needing replies, prioritize an inbox, or review reply workload across email accounts.

## Workflow

1. When Superhuman Mail is connected, use its account-list and query/search tools for this workflow. Do not switch to the graphical mail interface when the user asks for the connector. Discover every linked account and search across all of them, not only the primary account. State which accounts were reachable and disclose any account or folder that could not be searched.
2. Identify messages that are genuinely awaiting the user's reply today. Prioritize explicit deadlines or urgent requests, direct questions and decisions, active client or operational threads, then recency. Exclude newsletters, automated notifications, FYIs, messages already answered, and messages where the user is the latest sender unless new inbound content asks for a response.
3. Deduplicate threads and rank candidates. Briefly state the ranking basis and note when a due-today judgment is inferred rather than explicitly requested by the sender.
4. For the top five (or fewer if fewer qualify), apply the `email-reply` skill to each: show the original message in chat with sender, recipient when available, subject, date/time, and complete body; then provide concise reply options or a draft as requested. Keep each original clearly paired with its reply guidance. Redact credentials, one-time codes, access tokens, and similar secrets.
5. List the next ten candidates (or all remaining candidates if fewer) by sender and subject only when the user requests a compact review list. Follow the user's requested level of detail for these additional messages.
6. Do not send, archive, mark done, or otherwise change email state unless the user separately and explicitly requests that action. Drafts and recommendations are not sent messages.

Be clear about coverage limits, unread/search limits, and any uncertainty in ranking. Do not claim full-account coverage if only one account or a partial folder set was accessible.
