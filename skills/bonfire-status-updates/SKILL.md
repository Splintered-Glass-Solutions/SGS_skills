---
name: bonfire-status-updates
description: Draft, prepare, or send recurring conversational Bonfire team updates for the Bonfire text thread and the ClickUp `pd-bonfire` channel. Use when Preston asks for a Bonfire status update, recap, release/update message, shared-docs summary, recent-work report, value-add summary, or cross-repo Bonfire update intended for the team text thread, ClickUp channel, or both destinations.
---

# Bonfire Status Updates

## Overview

Use this skill to turn recent Bonfire engineering work into team-ready updates that explain the value of the work and where it is running.

- Bonfire text thread: short, mobile-first, one paste-safe message.
- ClickUp `pd-bonfire` channel: slightly more structured, with bullets only when useful and explicit local/dev/prod status.

Read `references/channel-patterns.md` before drafting or sending.

## Workflow

1. Identify whether Preston asked to draft only or send/post. If he says "send", "post", or "update them", treat it as permission to deliver, subject to destination verification.
2. Gather current evidence before writing. Prefer shared-docs change logs, source repo `git status`, source repo branch/log state, PR/deploy evidence, and actual dev/prod smoke evidence if available.
3. Translate implementation details into value before drafting. Lead with what the work unlocks for customers, operators, QA, or the next release.
4. Classify every item as one of:
   - local/source-branch only
   - committed/pushed but not deployed
   - deployed to dev and verified
   - deployed to production and verified
   - unknown/not verified
5. Draft both destinations from the same facts, but do not make them identical. The text thread should sound like a quick team note; ClickUp can carry the fuller recap.
6. Include only the status flags that matter: local, dev, production, or not verified. Do not list branches, dirty files, command output, or project-management mechanics unless they change what the team should do.
7. Include caveats plainly when deployment proof is missing. Do not imply a feature is live just because code or docs exist.
8. Strip secrets, raw customer data, private tokens, and internal-only URLs unless Preston explicitly asks for them and the destination is appropriate.
9. If sending to Messages, keep the body as a single paste-safe message. Avoid Markdown bullets and line breaks unless the send path is verified not to split them.
10. If posting to ClickUp, verify the exact `pd-bonfire` destination. Do not post to a near-match channel or task and do not claim delivery unless the tool confirms it.

## Evidence To Check

Use the narrowest source that answers the question:

- `/Users/preston/Code/bonfire_shared_docs/*/integrator_change_log.md` for cross-repo external feature summaries.
- `/Users/preston/Code/bonfire_shared_docs/shared/quality/integration_validation_matrix.md` for cross-system validation expectations.
- `/Users/preston/Code/bonfire`, `/Users/preston/Code/Bonfire_AI`, and `/Users/preston/Code/Bonfire_ETL` for local branch, dirty tree, commit, and deployment posture.
- Live dev/prod URLs, CI, release notes, or deployment logs only when Preston asks for deployed status or the update would otherwise risk overclaiming.

## Destination Rules

- Bonfire text thread: known recurring local Messages destination, but still resolve/verify the chat before sending. If resolution fails, return the draft and the blocker.
- ClickUp `pd-bonfire`: exact destination required. If connector tools cannot find or post to exactly `pd-bonfire`, return the draft and the blocker.
- Draft-only requests should not trigger send/post tooling.

## Output Shape

When drafting, return:

1. `Bonfire Text Thread`
2. `ClickUp pd-bonfire`

When sending/posting, return a concise delivery report with:

- where it was sent
- whether each destination was confirmed
- any unresolved destination or auth blocker
