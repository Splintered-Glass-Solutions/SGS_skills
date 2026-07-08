---
name: sgs-proposal-microsites
description: "Use when creating, updating, reviewing, or deploying client proposal microsites in the SGS proposal repository at /Users/preston/Code/sgs_proposals. Trigger this skill for tasks such as adding a new proposal client, reusing or extending the shared proposal page infrastructure, creating client note folders or deliverable drafts, splitting informal personal notes from formal overviews, or answering deployment and persistence questions for this repo."
---

# SGS Proposal Microsites

## Overview

This skill standardizes how proposal microsites are created and maintained in the SGS proposal repo. Use it to keep proposal content in the shared data layer, keep rendering in the shared app infrastructure, and avoid drifting into one-off per-client builds.

## Quick Start

1. Read `/Users/preston/Code/sgs_proposals/AGENTS.md`.
2. Read `clients/<slug>/proposal-details.md` if the client already exists.
3. Update or add the proposal object in `/Users/preston/Code/sgs_proposals/app/proposals/proposal-data.ts`.
4. Reuse the shared renderer in `/Users/preston/Code/sgs_proposals/app/proposals/proposal-page.tsx`.
5. Add or update any cover email or supporting draft in `/Users/preston/Code/sgs_proposals/deliverables`.
6. Run `npm run build`.
7. Before sending any client-facing proposal link, verify the exact live URL returns the expected proposal content.

## Workflow

### 1. Gather Context

- Confirm whether the client already exists under `clients/`.
- Check whether the request fits one of the current proposal kinds before inventing a new structure.
- Read [references/repo-structure.md](./references/repo-structure.md) for the active app paths and deployment model.

### 2. Keep Proposal Content Centralized

- Store all live proposal page content in `app/proposals/proposal-data.ts`.
- Do not create bespoke client-only route logic when the shared route can handle the page.
- Keep proposal notes, call notes, and working context in `clients/<slug>/proposal-details.md`.
- Keep email drafts and other shareable client artifacts in `deliverables/`.

### 3. Use The Shared Proposal Model

- Every proposal should include `preparedOn`.
- If there is an informal opener, use `personalNote` and keep `overview` formal.
- Prefer existing proposal kinds:
  - `website-build`
  - `strategic-retainer`
  - `hybrid-advisor`
  - `unified`
- Only extend the proposal union when the content shape truly cannot fit an existing kind.

### 4. Extend The App Carefully

- If a new proposal kind is required, change both:
  - `/Users/preston/Code/sgs_proposals/app/proposals/proposal-data.ts`
  - `/Users/preston/Code/sgs_proposals/app/proposals/proposal-page.tsx`
- Add only the minimum CSS needed in `/Users/preston/Code/sgs_proposals/app/globals.css`.
- Keep the homepage index generic so all proposal slugs surface automatically.

### 5. Validate

- Run `npm run build` after proposal changes.
- Confirm the proposal appears at `/proposals/<slug>`.
- Confirm `/` still lists the proposal directory cleanly.
- If a proposal URL will be texted, emailed, or otherwise sent to a client, verify the exact production URL that will be sent before sending it.
- The production URL check must confirm:
  - HTTP status is `200` after redirects.
  - The final URL is the intended proposal route, not a generic index or 404 page.
  - The response contains a proposal-specific string such as the client name, proposal title, or slug-specific headline.
- If the exact URL is not live and content-verified, stop and deploy or fix the route before sending the message.

Example verification command:

```bash
node - <<'NODE'
const url = 'https://proposals.splinteredglass.solutions/proposals/<slug>';
const expected = '<proposal-specific title or client name>';
const res = await fetch(url, { redirect: 'follow' });
const text = await res.text();
console.log({ status: res.status, finalUrl: res.url, hasExpectedContent: text.includes(expected) });
if (res.status !== 200 || !text.includes(expected)) process.exit(1);
NODE
```

## Deployment And Persistence

- Do not add a database by default.
- The default persistence model is code plus Vercel deployment history.
- Recommended deployment flow:
  1. Update proposal content in repo.
  2. Commit changes.
  3. Deploy the same Vercel project again.
- If a proposal slug remains in `proposal-data.ts`, it remains in the live app.
- If point-in-time preservation matters, keep the git commit and deployment URL for that version.
- Only consider a CMS or database later if non-developers need direct editing or proposal volume becomes hard to manage in code.

## Resources

Read [references/repo-structure.md](./references/repo-structure.md) when you need the current repo paths, proposal kinds, or deployment model.
