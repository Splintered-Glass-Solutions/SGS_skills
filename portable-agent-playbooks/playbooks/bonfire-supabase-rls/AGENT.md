# Bonfire Supabase Rls Agent Playbook

This is a platform-neutral version of the `bonfire-supabase-rls` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Work on Bonfire Supabase schema, migrations, row-level security, multi-tenant data access, generated Supabase types, auth hooks, service-role access, or files under supabase/migrations, supabase/seed.sql, src/types/supabase.ts, src/lib/supabase, or src/lib/auth/org-context.

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

# Bonfire Supabase + RLS

Use this skill for Bonfire database and multi-tenant data access changes in `<workspace>/bonfire`.

## Source Areas

- Migrations: `supabase/migrations/**`
- Seed data: `supabase/seed.sql`
- Generated types: `src/types/supabase.ts`
- Supabase clients: `src/lib/supabase/**`
- Org context and auth helpers: `src/lib/auth/org-context.ts`, `src/lib/auth/authorization.ts`
- Schema mapping reference: `docs/SCHEMA_MAPPING.md`

## RLS Principles

- Treat org isolation as the default. Any org-scoped table should have an explicit `org_id` path or a clearly documented relationship to org scope.
- Prefer least-privilege policies. Authenticated user access should be mediated through membership/permission checks, not broad authenticated grants.
- Service-role clients may bypass RLS for backend fulfillment, webhooks, background jobs, and admin-only paths. Confirm the callsite is server-only.
- Do not weaken existing policies to make tests pass. Fix the data path or policy predicate.
- For public/widget access, verify whether anonymous access is intentional and constrained by org/AI/widget identifiers.
- Migrations should be forward-only and safe against partially populated existing data.

## Migration Workflow

1. Inspect recent migrations to match naming, ordering, and SQL style.
2. Create a timestamped migration in `supabase/migrations/YYYYMMDDHHMMSS_description.sql`.
3. For new tables, decide explicitly:
   - Primary key and timestamps.
   - `org_id` or ownership relationship.
   - RLS enabled.
   - Policies for authenticated, anonymous, and service paths.
   - Indexes for expected query filters.
4. For RPCs/functions, set search path defensively when appropriate and avoid leaking cross-org data.
5. Update TypeScript code and tests after schema changes.
6. Regenerate Supabase types when the local schema is available:

```bash
corepack pnpm db:gen-types
```

## Review Checklist

- Does every org-scoped query filter by org or use a helper that proves org access?
- Are anonymous policies limited to public/widget flows only?
- Could a user with access to one org infer rows from another org?
- Are write policies stricter than read policies?
- Are indexes aligned with new filters and uniqueness constraints?
- Are service-role callsites server-only and not exposed to client bundles?

## Focused Checks

Use the tests nearest the changed data path. Common broader checks:

```bash
NEXT_PUBLIC_POSTHOG_PROJECT_TOKEN= corepack pnpm exec vitest run src/lib/auth src/services src/features
corepack pnpm type-check
```

For security-sensitive work, include a short written note describing the access boundary you verified.

