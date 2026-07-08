# Bonfire Auth Org Permissions Agent Playbook

This is a platform-neutral version of the `bonfire-auth-org-permissions` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Work on Bonfire authentication, email verification, invites, org membership, org switching, roles, permission checks, staff org access, login/signup redirects, onboarding access, or files under src/lib/auth, src/features/auth, src/app/auth, src/services/*org*, or src/actions/profile-email-change.

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

# Bonfire Auth, Org, and Permissions

Use this skill for Bonfire identity and access changes in `<workspace>/bonfire`.

## Source Areas

- Auth library: `src/lib/auth/**`
- Auth app routes/actions: `src/app/auth/**`
- Auth feature code: `src/features/auth/**`
- Org services/actions: `src/services/org-service.ts`, `src/services/org-provisioning-service.ts`, `src/actions/organization-settings.ts`
- Permission service: `src/services/permission-service.ts`
- Staff org access: `src/services/bonfire-staff-org-access-service.ts`
- Dashboard org UI: `src/features/dashboard/components/OrgSwitcher.tsx`, team/settings components

## Access Model

- Use `requireAuthenticatedUser`, `requireVerifiedUser`, `requireOrgAccess`, `requireVerifiedOrgAccess`, and `requirePermission` from `src/lib/auth/authorization.ts` instead of reimplementing access checks.
- Preserve role hierarchy behavior from `src/lib/auth/role-hierarchy.ts`.
- Email verification is required for sensitive authenticated mutations when neighboring code requires it.
- Staff org access reconciliation is intentional. Do not remove or bypass it without understanding `bonfire-staff-org-access-service`.
- Keep org context explicit. Do not infer access from client-provided `orgId` without server-side verification.

## Workflow

1. Determine whether the change affects authentication, verification, org membership, role level, invite flow, or UI-only display.
2. Read the relevant tests before editing. Auth regressions usually already have focused tests.
3. For server mutations, verify the minimum role required and whether email verification is required.
4. For invite and onboarding flows, preserve token validation, redirect behavior, and joined-org messaging.
5. For role or permission changes, update both helper tests and user-facing UI state tests where applicable.
6. For RLS or schema changes, also use the `bonfire-supabase-rls` workflow.

## Focused Checks

For auth/signup regression:

```bash
NEXT_PUBLIC_POSTHOG_PROJECT_TOKEN= corepack pnpm exec vitest run src/app/auth/actions.test.ts src/app/@modal/'(.)signup'/page.test.tsx src/lib/auth/request-origin.test.ts src/lib/auth/login-redirect.test.ts
```

For permission/org behavior:

```bash
NEXT_PUBLIC_POSTHOG_PROJECT_TOKEN= corepack pnpm exec vitest run src/lib/auth src/features/auth src/services/bonfire-staff-org-access-service.test.ts src/services/org-service.test.ts
```

Before handoff, state which boundary was verified: authentication, email verification, org membership, role level, or resource permission.

