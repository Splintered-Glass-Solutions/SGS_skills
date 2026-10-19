# Authenticated Browser Testing Agent Playbook

This is a platform-neutral version of the `authenticated-browser-testing` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Use the the agent internal browser as the user's required default browser for authenticated live UI testing, hosted QA, user-story walkthroughs, and Computer Use checks that depend on an existing signed-in session. Trigger for signed-in Dev, staging, or production browser validation across example-project-13, example-project-12, example-project-14, and other the user projects; for login/session blockers; and whenever another testing skill needs authenticated rendered-UI proof.

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

> Public template: example project paths, schemas and fixtures are illustrative.
> Resolve real bindings and current authority from private project configuration;
> examples confer no account, data-write, permission or deployment authority.


# Authenticated Browser Testing

Use the the agent internal browser (in-app browser, `iab`) for every authenticated live browser test for the user.

## Browser and login workflow

1. Open or inspect the target in the the agent internal browser through the available browser tools. With Computer Use, use `cua.createBrowserTab("iab", targetUrl, { visible: true })` or reuse a matching existing internal-browser tab.
2. Reuse a valid internal-browser session when it satisfies the required identity and role.
3. When login is needed, search 1Password for the matching site/domain and approved username. Use its credentials to complete the login, preferably through secure autofill. Use available 1Password app, integration, or CLI capabilities; Developer Environments tools alone do not provide login-item search or autofill. Do not assume an unavailable capability exists.
4. Verify the visible environment, account identity, organization/tenant, and effective role before claiming proof.
5. Navigate and test in the internal browser. Re-read rendered state after each material action.
6. Use Playwright, Chromium, or another runner for deterministic, mocked, or repository-owned automated suites. Keep that evidence separate from authenticated hosted UI acceptance in the internal browser.

Do not call authentication blocked merely because no signed-in session exists. First try the matching approved 1Password login. If 1Password requires unlocking, approval, or inaccessible credentials, report that exact blocker; never guess credentials or reset a password to bypass it.

## Exceptions

Use another browser only when the user explicitly requests it, the acceptance criterion requires browser-specific or cross-browser coverage, or the internal browser cannot exercise the required surface after a bounded check. Record the exception and keep the internal browser as the default for remaining checks. If the session has the wrong identity, switch safely when authorized or report the mismatch; never relabel the session.

## Authentication and evidence

- Prefer an existing valid session over reauthentication.
- Use only project-approved QA identities and the matching credentials in 1Password. Credential access does not authorize unrelated account or application changes.
- Use secrets only for the intended login. Never expose or persist passwords, OTPs, tokens, recovery codes, cookies, or browser storage in chat, terminal output, logs, screenshots, source files, or QA evidence.
- Follow applicable browser-tool requirements for login, permissions, and consequential actions.
- Keep live authenticated proof separate from local, mocked, API, deployed-runtime, and production/customer-visible proof.
- Record the the agent internal browser, target URL, environment, identity category, tenant/organization when relevant, and observed result in the QA ledger.
