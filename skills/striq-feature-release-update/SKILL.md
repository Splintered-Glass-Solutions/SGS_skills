---
name: striq-feature-release-update
description: Create and deliver StrIQ post-feature release communications after a StrIQ feature is finished, validated, deployed, or materially advanced. Use when Preston asks to summarize completed StrIQ work, explain customer or business impact, capture frontend/backend/admin/API/data-pipeline implications, prepare L10/team talking points, or send a StrIQ L10 Team group text.
---

# StrIQ Feature Release Update

## Overview

Use this skill after StrIQ feature work, rollout work, QA, or a meaningful implementation milestone to turn engineering evidence into a concise team-ready update.

Every output must include a clear title and a clear `Live Status` line that says whether the work is local only, on stage/dev, in production, not live, or unknown.

Default to delivery, not draft-only. When Preston invokes this skill after finished or validated StrIQ work, treat that invocation as authorization to prepare and send the update to the StrIQ L10 Team group text, subject to the safety and live-status rules below.

Draft-only behavior applies only when Preston explicitly says draft only, do not send, review first, or similar.

## Related Skills

- Use `striq-clickup` when Preston asks to create or update StrIQ ClickUp tasks.
- Use `striq-ecosystem` when repo ownership, deployment state, or StrIQ runtime boundaries are unclear.
- Use `feature-finish-line` first when validation is incomplete.

## Evidence Workflow

1. Gather current feature evidence:
   - latest user request and finish-line summary
   - `git status --short --branch` for affected repos
   - relevant `git diff --stat`, changed routes, tests, docs, migrations, data jobs, and service files
   - validation commands already run and any blockers
   - deployment proof, if the update claims stage/dev or production status
2. Classify live status explicitly:
   - `local`: implemented or validated only in a local repo/runtime
   - `stage/dev`: deployed to StrIQ stage/dev and smoke-tested
   - `production`: deployed to production and smoke-tested
   - `not live`: implemented but not running in any verified environment
   - `unknown`: no reliable environment evidence
   - Include the proof source, such as local test output, stage URL, Cloud Run revision, Vercel preview, production URL, GitHub Actions run, or smoke result.
3. Summarize the work in product language:
   - what changed
   - why StrIQ needed it now
   - customer/user story
   - business impact
   - frontend implications
   - backend/API implications
   - admin implications
   - ETL/data/pipeline implications
   - billing/auth/security implications, when relevant
   - customer-facing talking points
   - validation status and caveats
4. Create a short title before delivery.

## Delivery Rules

Automatically attempt delivery to:

- StrIQ L10 Team group text

Before delivery:

- Verify the exact Messages destination through local Messages data or the known identifier below.
- Do not send to a near-match thread such as `strIQ Tech`, `strIQ Tech/Data`, `StrIQ Customer Success`, `strIQ squad`, or one-to-one StrIQ contacts.
- Strip secrets, raw customer data, access tokens, private logs, exact database credentials, and irrelevant implementation noise.
- Do not claim stage/dev or production status unless environment-specific proof exists.
- Before sending, inspect the exact outbound text that will be delivered. Emoji section markers must be the actual Unicode emoji characters shown in this skill, not mojibake or replacement text.
- If the outbound text contains mojibake sequences such as `ðŸ`, `âœ`, `âš`, `Ã`, `Â`, `�`, or escaped byte text like `\\xF0`, rewrite the message from the source draft using the actual emoji markers and re-check it before delivery. Do not send a message that still contains those characters.
- If the exact Messages destination cannot be verified, return the text draft and the blocker instead of sending.

## Destination Rules

### StrIQ L10 Team Group Text

Known local Messages destination:

- Messages label: `strIQ L10 Team`
- Current/alternate Messages label observed for the same chat: `strIQ Leadership Team`
- Verified local chat identifier: `chat325477239352170807`
- AppleScript target form: `iMessage;+;chat325477239352170807`

When local Messages access is available, use the known Messages destination above, send with AppleScript, then verify delivery with a read-only `~/Library/Messages/chat.db` query for the latest outbound row in `chat325477239352170807`.

Use a concise mobile-first message. Avoid long Markdown, dense command output, tables, or implementation dump.

Start the message with a plain title line, such as `StrIQ Feature Update: Partner Lead Attribution`.

The title line must not include an emoji. Keep the title row separate from the emoji-marked body sections.

Always include a plain-language live-status phrase, such as `Status: local only`, `Status: live on stage`, or `Status: live in production`.

Use tasteful emojis as section markers so the message is easy to scan in a group text. Keep them functional, not decorative.

Emoji encoding guard: before AppleScript delivery, confirm the final message contains real emoji codepoints, for example `🚦`, `📌`, `💡`, `🧩`, `✅`, `⚠️`, and `📣`. Do not send if the preview shows mojibake like `ðŸš¦`, `ðŸ“Œ`, `ðŸ’¡`, `ðŸ§©`, `âœ…`, `âš ï¸`, or `ðŸ“£`; rebuild the message as UTF-8 text and verify again first.

## Formatting Style

For StrIQ L10 Team messages, use 4-6 concise markers depending on the update:

- 🚦 Status
- 📌 What Changed
- 💡 Why It Matters
- 🧩 Product / API / Data Impact
- ✅ Validation
- ⚠️ Caveats
- 📣 Customer Angle

Do not put an emoji in the title row.

Never substitute ASCII labels, shortcode text, escaped byte sequences, or mojibake for the emoji markers. The final draft and the exact delivered payload must show the real emoji characters above.

Keep routine updates short:

- 1 title
- 1 live-status line
- 1 compact feature summary
- 1 practical business/customer impact line
- 1 implementation-impact line covering frontend/backend/admin/API/data as relevant
- 1 validation/caveat line

Include "No direct data-pipeline impact", "No API surface change", or "No admin impact" when true and relevant. Do not omit important categories just to keep the message short.

## Output Shape

When Preston explicitly asks for draft-only, return:

1. `Title`
2. `Feature Release Summary`
3. `Live Status`
4. `StrIQ L10 Team Text Copy`
5. `Delivery Readiness`

For default delivery runs, return:

- exact destination confirmed
- title used
- live status confirmed for local/stage/dev/production
- what was sent
- verification result from Messages
- any blocked destination, auth, or deployment evidence gap

## Quality Bar

- Lead with StrIQ customer and business value, not implementation mechanics.
- Include a short title in every outbound message and delivery report.
- State `Live Status` even when the status is `unknown`.
- Keep the L10 message readable on mobile.
- Use enough implementation context for leadership to understand scope without turning the message into a changelog.
- Make customer talking points usable by non-engineers.
- Keep claims factual and non-hypey.
- Keep caveats clear: local-only, not yet deployed, migration not applied, missing credentials, incomplete smoke, or no production proof.
