# Email Reply Agent Playbook

This is a platform-neutral version of the `email-reply` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Find and review an email, then outline reply options or prepare a draft. Always show the original message in chat so the user can read it before the reply guidance.

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

# Email Reply

Use this skill when the user asks to find, read, understand, or reply to an email, including requests for reply options or a draft.

## Workflow

1. Locate the intended email in the account the user named or the clearly relevant connected account. If the sender or message is ambiguous, resolve it from available context or ask a brief clarification.
2. Read the message and any directly relevant thread context. Keep the original message separate from older quoted messages and from your interpretation.
3. In your response, show the original email so the user can read it themselves. Include sender, recipient when available, subject, and date/time, followed by the complete body in a block quote or clearly labeled quote. Preserve wording and paragraph breaks. Include signature when present. For a long thread, show the specific message the user asked about; summarize older context separately unless they ask to see the whole thread.
4. Then give the requested interpretation, reply options, or draft. Ground claims in the email and relevant records. Label uncertainty and avoid turning an unverified claim into a fact.
5. Redact passwords, one-time codes, access tokens, and similarly sensitive secrets from quoted content, and mark where redaction occurred. Mention attachments by name and summarize them only if they were actually inspected.

When drafting as the user, follow the `user-communication` skill for voice and channel guidance. Show drafts for review when the topic involves money, contracts, legal risk, taxes, or other sensitive commitments. Never send an email unless the user explicitly asks you to send it; follow applicable confirmation requirements immediately before sending.

If the email cannot be retrieved, say so plainly. Do not substitute a generated draft, preview snippet, or inferred wording for the original; identify what portion of the message was actually visible.
