# Bonfire Browser Test Accounts Agent Playbook

This is a platform-neutral version of the `bonfire-browser-test-accounts` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Choose and verify the user's approved Bonfire browser-test identity. Use for Bonfire browser QA, authenticated acceptance, Super Admin portal checks, ordinary-user or least-privilege checks, login blockers, and requests involving Arc, the TAPOS space, or Bonfire credentials in 1Password.

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

# Bonfire Browser Test Accounts

Use the correct approved identity and verify it in the rendered application before claiming authenticated proof.

## Choose the account

| Test need | Bonfire login | Rule |
| --- | --- | --- |
| Most browser tests, staff-only behavior, or Super Admin | `the user@heybonfire.com` | Default browser-test identity and approved Super Admin account. |
| Normal-user, non-Super-Admin, or least-privilege behavior | `the userpope192@gmail.com` | Use when the assertion must reflect an ordinary user without Super Admin authority. |

If a test explicitly names a different role or fixture, follow that test's requirement. Do not silently substitute one of these identities when doing so would weaken the assertion.

## Browser and authentication

1. Prefer Arc for authenticated Bonfire browser QA.
2. Start with the TAPOS Arc space because the user normally keeps the approved session authenticated there.
3. Preserve a valid existing session. Do not sign out or reauthenticate merely to repeat proof already available under the required identity.
4. When sign-in is required, retrieve or autofill the matching credential from 1Password. Never store a password in this skill, source files, logs, screenshots, terminal output, chat, or QA evidence.
5. If 1Password requires the user's interaction or the credential cannot be accessed safely, report the exact blocker instead of guessing, resetting a password, or using another account.

## Proof requirements

- Verify the rendered signed-in email and, when material, the effective role before exercising the feature.
- For Super Admin proof, require `the user@heybonfire.com` plus evidence that the live Super Admin surface is actually authorized; a health check or login screen is insufficient.
- For normal-user proof, require `the userpope192@gmail.com` and confirm the session does not expose Super Admin behavior relevant to the test.
- Record the browser, environment, URL, identity, organization when relevant, and proof tier.
- Keep local, hosted Dev, production, and customer-visible proof distinct.
- If the active Arc session has the wrong identity for the assertion, do not relabel the result. Switch safely or report the mismatch.

## Safety

- Treat both addresses as approved test identities, not authorization for unrelated email, billing, production writes, role changes, or cross-organization data access.
- Keep production browser QA read-only unless the user explicitly authorizes the exact mutation.
- Never change permissions, grants, roles, ownership, or RLS to make a test account pass.
