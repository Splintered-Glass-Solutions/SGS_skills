---
name: bonfire-chat-widget
description: Work on Bonfire's embeddable chat widget, widget preview, public chat APIs, streaming UI, widget build, mobile widget behavior, cross-origin embed behavior, or files under src/features/chat-widget, src/app/widget, public/widget.js, or src/app/api/chat.
---

# Bonfire Chat Widget

Use this skill for Bonfire widget changes in `/Users/preston/Code/bonfire`.

## Source Areas

- Widget app and UI: `src/features/chat-widget/**`
- Widget shell pages: `src/app/widget/**`, `src/app/widget/preview/**`
- Public chat API routes: `src/app/api/chat/**`
- Built embed output: `public/widget.js`, `dist/widget.js`
- Widget docs: `src/pages/ChatWidgetDocs.tsx`, `src/app/chat-widget-docs/page.tsx`

## Engineering Rules

- Preserve the public embed API: existing `org_id`, `ai_id`, `widgetId`, `viewerEmail`, and `isAuthenticatedUser` behavior must remain backward compatible unless the user explicitly asks for a breaking change.
- Reduce `use client` surface where practical, but do not destabilize the widget runtime. Keep interactive state inside widget components/state modules.
- Keep cross-origin behavior in mind. Public widget requests may need CORS handling from `src/app/api/chat/cors.ts`.
- Keep anonymous visitor, token, and session scope behavior stable. Check `state/chat-api.ts`, `state/token-manager.ts`, `state/session-storage.ts`, and `state/session-api-base.ts` before changing session lifecycle.
- Preserve streaming semantics. For message streaming changes, inspect `state/chat-stream.ts`, `state/chat-store.ts`, `components/StreamingText.tsx`, and `src/app/api/chat/message/route.ts`.
- For mobile behavior, check `hooks/useResponsive.ts`, `components/WidgetContainer.tsx`, `components/LauncherBubble.tsx`, overlays/modals, and viewport constraints.
- Avoid layout shifts in fixed widget surfaces. Define stable dimensions for launchers, headers, message lists, overlays, buttons, and loading/error states.
- Before local widget verification, confirm the running Next process is pointed at the intended Session API base URL. If `.env.local` changed after `next dev` started, restart the dev process.
- If the Session API is running in Docker, rebuild and restart the API container before treating local widget results as current.

## Workflow

1. Identify whether the change affects UI-only widget behavior, public API behavior, session/token behavior, streaming, or the build artifact.
2. Read the nearest component/state/API tests before editing.
3. If API behavior changes, inspect the matching route under `src/app/api/chat/**` and its test file.
4. If runtime config changes, inspect `app/widget-config.ts`, `state/config-fetcher.ts`, and `server/active-widget-config.ts`.
5. If build or embed output changes, run the widget build and verify `public/widget.js` is updated only when expected.
6. Use Browser Use or Playwright when the user asks to inspect, click, screenshot, or test the widget in browser.

## Focused Checks

Run the narrowest useful checks first:

```bash
corepack pnpm exec vitest run src/features/chat-widget
corepack pnpm type-check:widget
corepack pnpm run build:widget
```

For scripture/source rendering work:

```bash
corepack pnpm test:scripture
```

For broader confidence before handoff:

```bash
NEXT_PUBLIC_POSTHOG_PROJECT_TOKEN= corepack pnpm exec vitest run
corepack pnpm type-check
corepack pnpm lint:check
```

For production widget outage or deploy verification, run the Session API streamed smoke from `/Users/preston/Code/Bonfire_AI` against both the direct Session API and the app proxy when applicable:

```bash
python3 scripts/smoke_widget_streaming.py \
  --mode both \
  --session-api-url "$SESSION_API_URL" \
  --app-url "$APP_URL" \
  --org-id "$ORG_ID" \
  --ai-id "$AI_ID" \
  --require "10:30"
```

## Handoff Notes

Report whether the change touched:

- Public embed API.
- Chat API route contracts.
- Session/token persistence.
- Streaming events or rendering.
- Mobile/full-page widget behavior.
- Built widget output.
