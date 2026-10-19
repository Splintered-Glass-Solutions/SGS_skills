# Authenticated Browser Testing Agent Playbook

This is a platform-neutral version of the `authenticated-browser-testing` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Verify authenticated rendered UI using an approved browser session, test identity and secure credential path. Keep hosted UI acceptance distinct from local or mocked checks.

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

# Authenticated Browser Testing

Resolve the target URL, environment, approved QA identity, tenant and role from
the request or project configuration. Use the user-approved browser. A runtime's
in-app browser is suitable when it supports the required identity and surface;
Playwright or another supported browser may be used when the project requires it.
Do not assume a particular browser, password manager or existing signed-in account.

1. Reuse a valid approved session when available. Verify visible identity and role.
2. If login is required, use the project's authorized credential manager or secure
   login flow. Never guess passwords, reset accounts or switch identities without
   authority. Report the precise unlock, access or tool blocker if unavailable.
3. Navigate through the actual UI. Re-read rendered state after material actions.
4. Exercise the accepted workflows with approved fixtures and mutation boundaries.
5. Record target, environment, browser, identity category, tenant/role, revision,
   observed result and safe evidence in the project's QA record.

Keep passwords, OTPs, recovery codes, tokens, cookies and browser storage out of
chat, source, logs, screenshots and public artifacts. Credential access does not
authorize unrelated account changes. Missing authenticated coverage remains
blocked/incomplete when required; public or mocked checks cannot substitute.
Label local, automated, hosted, authenticated and customer-visible proof separately.
