# Bonfire Api Routes Agent Playbook

This is a platform-neutral version of the `bonfire-api-routes` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Add, change, review, or test Bonfire Next.js API route handlers under src/app/api, including validation, auth, org access, JSON response shape, CORS, runtime selection, Sentry logging, or route tests.

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

# Bonfire API Routes

Use this skill for Bonfire API route work in `<workspace>/bonfire`.

## Source Areas

- Routes: `src/app/api/**/route.ts`
- Route tests: colocated `route.test.ts`
- API helpers: `src/lib/api-response.ts`, `src/lib/api-utils.ts`
- Auth helpers: `src/lib/auth/authorization.ts`, `src/lib/auth/org-context.ts`
- Public chat CORS: `src/app/api/chat/cors.ts`
- Sentry handled failures: `src/lib/sentry/handled-failure.ts`
- Validation schemas: `src/lib/validations/**`

## Route Pattern

1. Start from the nearest existing route in the same domain.
2. Choose runtime deliberately. Use `nodejs` when route behavior depends on Node APIs, SDKs, streaming, or service-role operations.
3. Parse and validate request input with existing zod schemas or add schemas under `src/lib/validations/**` when reusable.
4. Use the correct Supabase client:
   - User-scoped SSR/server client for authenticated user actions.
   - Service-role client only for server-only fulfillment, admin operations, webhooks, and trusted internal jobs.
5. Enforce auth and org permissions through existing helpers before accessing org-scoped data.
6. Keep response shapes consistent with neighboring routes and client expectations.
7. Capture expected operational failures with `captureHandledFailure` where similar routes already do.
8. Add or update colocated route tests for status codes, auth failures, validation failures, and happy path.

## Public and Widget Routes

- For `src/app/api/chat/**`, inspect `cors.ts` and OPTIONS behavior before adding methods or headers.
- Preserve cross-origin embed compatibility.
- Do not require dashboard cookies for anonymous/public widget flows unless intentionally changing the contract.
- Validate `org_id`, `ai_id`, session identifiers, and forwarded session API authorization paths carefully.

## Auth and Error Handling

- Use `AuthorizationError` patterns from `src/lib/auth/authorization.ts` when the route is an authenticated app route.
- Return sanitized user-facing errors. Do not leak raw provider, database, or stack details into public responses.
- Log enough context to debug without logging secrets, full tokens, or private content.

## Focused Checks

Run the route's colocated test first:

```bash
NEXT_PUBLIC_POSTHOG_PROJECT_TOKEN= corepack pnpm exec vitest run path/to/route.test.ts
```

For wider API changes:

```bash
NEXT_PUBLIC_POSTHOG_PROJECT_TOKEN= corepack pnpm exec vitest run src/app/api
corepack pnpm type-check
```

If public API docs or OpenAPI behavior changes, inspect `src/lib/openapi/**` and `src/pages/BonfireApiDocs.tsx`.

