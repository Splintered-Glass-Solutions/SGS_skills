# Bonfire Feature Release Update Agent Playbook

This is a platform-neutral version of the `bonfire-feature-release-update` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Create and deliver Bonfire post-feature release communications after a feature is finished or validated. Use when the user asks to summarize a completed Bonfire feature, explain why it was built, capture the user story and customer impact, identify API/frontend/ETL implications, prepare team/customer/marketing talking points, include screenshots or marketing assets, send a Bonfire group text, post to ClickUp `pd-bonfire` or AND Studio ClickUp, or publish a Bonfire production update-log entry.

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

# Bonfire Feature Release Update

## Overview

Use this skill after a Bonfire feature build or finish-line pass to turn engineering work into a useful product update for the team, ClickUp, customers, marketing, and the Bonfire update log.

Prefer a complete draft over vague status. Every output must include a clear title and a clear `Live Status` line that says whether the feature is live in local, dev, production, or not verified.

Default to concise, non-duplicative output. The Bonfire group text and ClickUp post may use the same copy unless the user asks for separate versions.

Default to delivery, not draft-only. When the user invokes this skill after a finished Bonfire feature, treat that invocation as explicit authorization and expectation to get a team update out in the current run. Prepare and send the update to the Bonfire group text, the exact `pd-bonfire` ClickUp destination, and the Bonfire production update log, subject to the safety and live-status rules below. If the preferred team destinations are not visible through the available tooling, do not stop at a draft; use the most specific verified Bonfire team fallback available, such as an exact Bonfire-related ClickUp task, list, document, or workspace chat, and report the fallback used.

## Related Skills

- Use `feature-finish-line` first when validation is incomplete.
- Use `marketing-asset-generation` when release notes or launch updates need persona-specific Bonfire promotional images, saved asset packages, or reusable static launch visuals.
- Use `bonfire-status-updates` for shorter recurring Bonfire updates.
- Use `clickup` when posting or creating ClickUp artifacts.

## Evidence Workflow

1. Gather current feature evidence:
   - latest user request and finish-line summary
   - `git status --short --branch`
   - relevant `git diff --stat`, changed routes, tests, docs, migrations, and service files
   - validation commands already run and any blockers
   - deployment proof, if the update claims dev or production status
2. Classify live status explicitly:
   - `local`: implemented or validated only in the local repo/runtime
   - `dev`: deployed to dev and smoke-tested
   - `production`: deployed to production and smoke-tested
   - `not live`: implemented but not running in any verified environment
   - `unknown`: no reliable environment evidence
   - Include the proof source, such as local route smoke, dev URL, production URL, deployment record, or release-log row.
3. Summarize the feature in product language:
   - what changed
   - why Bonfire built it now
   - the customer/user story
   - business/customer impact
   - API implications
   - frontend implications
   - ETL/data implications
   - billing/auth/security implications, when relevant
   - customer-facing talking points
   - marketing uses
   - live status and environment proof
   - validation status and caveats
4. Resolve marketing assets before drafting:
   - Run `<agent-config>/skills/marketing-asset-generation/scripts/find_marketing_asset_package.py --feature-name "<Feature Name>"` from the relevant repo.
   - If a matching asset package exists, reuse it. Do not generate duplicate assets unless the user explicitly asks for fresh assets.
   - If no package exists and the update needs release-note or launch collateral, use `marketing-asset-generation` to create a local package first.
   - If Feature Finish Line already created assets, reuse that package and cite its `asset-manifest.md` or `asset-manifest.json`.
   - If image generation fails, include the package path, prompt files, failure status, and next step instead of omitting the marketing section.
5. Read `references/release-update-template.md` before drafting the final payloads.
6. Create a short title before delivery. Use the same title for group text, ClickUp, and production update-log drafts unless the destination needs a more formal title.

## Marketing Assets Workflow

Marketing assets are part of the release notes package, not a separate afterthought.

1. Search for existing assets first.
   - Default search roots are `<repo>/output/marketing-assets/` and `/Users/the user/Marketing Assets/Bonfire/`.
   - A valid package has `asset-manifest.json` and usually `asset-manifest.md`, `copy-matrix.md`, `creative-brief.md`, `prompts/`, `raw-screenshots/`, and `generated-assets/`.
2. Reuse an existing package when found.
   - Summarize persona rows, image statuses, screenshots, and asset paths/links.
   - Include generated, reused, planned, failed, or blocked statuses clearly.
3. Generate missing assets only when needed.
   - Use `marketing-asset-generation` with the same feature name, live status, screenshots, and relevant personas.
   - Keep generated assets local unless the user separately asks for Drive upload or public publishing.
4. Include the marketing package in team-facing release notes.
   - Bonfire text thread: include the package path or Drive link plus one concise marketing angle.
   - ClickUp `pd-bonfire`: include a `Marketing Collateral` section with screenshots, persona images, headlines/subtitles, social copy, customer announcement copy, support/sales notes, QA status, and known limitations.
   - Production update log: include only customer-facing copy and public-safe screenshot/asset links when production-live proof exists.
5. Keep sections separate.
   - Engineering notes: implementation/API/frontend/ETL/security/validation.
   - Customer-facing copy: announcement, value, benefits, caveats.
   - Marketing collateral: screenshots, persona images, headlines, social copy, asset links/downloads.

## Delivery Rules

When the user invokes this skill for a finished feature, automatically attempt delivery to:

- Bonfire group text/chat
- exact ClickUp `pd-bonfire` destination in AND Studio ClickUp
- Bonfire production update log through the canonical release sync path

Do not require a follow-up "send it" command.

Draft-only behavior applies only when the user explicitly says draft only, do not send, do not post, review first, or similar.

Before delivery:

- Verify the exact destination with the available connector/tooling.
- Do not post to an unrelated near-match channel, task, list, or chat.
- If the exact preferred destination is unavailable, search for Bonfire-specific fallbacks across available ClickUp/Slack/chat tooling. A fallback is acceptable only when its name or context clearly identifies Bonfire, and the final report must say it was a fallback.
- Strip secrets, raw customer data, access tokens, private logs, and irrelevant implementation noise.
- Do not claim a feature is live in dev or production unless environment-specific proof exists.
- Before sending or posting, inspect the exact outbound text that will be delivered. Emoji section markers must be the actual Unicode emoji characters shown in this skill, not mojibake or replacement text.
- If the outbound text contains mojibake sequences such as `ðŸ`, `âœ`, `âš`, `Ã`, `Â`, `�`, or escaped byte text like `\\xF0`, rewrite the message from the source draft using the actual emoji markers and re-check it before delivery. Do not send a message that still contains those characters.
- If neither the preferred destination nor any Bonfire-specific fallback can be verified, skip only that destination and report the blocker. Continue with other verified destinations.

## Destination Rules

### Bonfire Group Text

Resolve the known Bonfire group chat before sending. If the chat cannot be identified exactly, return the text draft and the blocker.

Known local Messages destination:

- Messages label: `Bonfire`
- Expected members/context: Bonfire team thread with Nick and Eric
- Verified local chat identifier: `chat91142418163091161`
- AppleScript target form: `iMessage;+;chat91142418163091161`

When local Messages access is available, do not skip this destination just because Slack or another chat connector is unavailable. Use the known local Messages destination above, send with AppleScript, then verify delivery with a read-only `~/Library/Messages/chat.db` query for the latest outbound row in `chat91142418163091161`. If the visible Messages UI ordering is confusing, trust the latest matching outbound database row rather than the sidebar ordering.

Use a concise mobile-first message. Avoid long Markdown, dense command output, or tables.

Start the message with a plain title line, such as `Bonfire Feature Update: Partner Portal Foundation`.

The title line must not include an emoji. Keep the title row separate from the emoji-marked body sections.

Always include a plain-language live-status phrase, such as `Status: local only`, `Status: live on dev`, or `Status: live in production`.

Use tasteful emojis as section markers so the message is easy to scan in a group text. Keep them functional, not decorative.

Emoji encoding guard: before AppleScript delivery, confirm the final message contains real emoji codepoints, for example `🚦`, `🔥`, `💡`, `🧩`, `📣`, `✅`, and `⚠️`. Do not send if the preview shows mojibake like `ðŸš¦`, `ðŸ”¥`, `ðŸ’¡`, `ðŸ§©`, `ðŸ“£`, `âœ…`, or `âš ï¸`; rebuild the message as UTF-8 text and verify again first.

### ClickUp `pd-bonfire`

Known destination:

- Workspace: `And Studio`
- Workspace ID: `10643222`
- Destination name: `PD - Bonfire`
- ClickUp Chat channel ID: `5-90050590186-8`
- Surface type: shared private folder/chat

Important: `PD - Bonfire` does not appear in the normal SGS Consulting workspace hierarchy. It lives in the And Studio shared/private ClickUp hierarchy. Use `clickup-environment-map` when resolving it, and check the ClickUp shared hierarchy path if generic connector search does not show it.

Verify the exact `pd-bonfire` destination before posting. If the connector cannot find or post to that exact channel, search ClickUp for an exact Bonfire-specific fallback before giving up. Prefer, in order: a Bonfire-named chat channel, `pd-bonfire` list/task/doc, an existing Bonfire release/product task, or another clearly Bonfire-scoped task/list. Post the update to the first verified Bonfire-specific fallback and report that the preferred `pd-bonfire` destination was unavailable.

By default, reuse the same concise team update copy as the Bonfire group text. Only create a longer ClickUp-specific version when the user asks for more detail or when the ClickUp audience needs acceptance criteria, links, or follow-up ownership.

When the ClickUp tool supports post metadata, send the ClickUp update as a post with `post_title` set to the update title. If only message delivery is available, put the plain, emoji-free title as the first line of the message.

Use light emoji section markers in ClickUp updates too, but keep the post title and first title line emoji-free. The goal is to break up dense product/engineering text, not to make the post feel hype-heavy.

Before posting to ClickUp, apply the same emoji encoding guard used for Messages. ClickUp copy must contain actual emoji section markers, never mojibake sequences such as `ðŸ`, `âœ`, `âš`, `Ã`, `Â`, or `�`.

### AND Studio ClickUp

Verify the exact AND Studio ClickUp workspace/channel/list before posting. Memory may mention workspace `10508245`, but re-check live connector visibility each run.

If no exact Bonfire/Studio destination is visible, do not use an unrelated workspace location. Search for a clearly Bonfire-scoped fallback before skipping ClickUp delivery.

### Bonfire Production Update Log

The Bonfire `/updates` surface is backed by `app_releases`. For this skill, the user's invocation is standing approval to publish the production update-log entry when the feature is production-deployed and smoke-tested.

Do not manually insert/update release rows or use ad hoc SQL. Use the canonical release sync path.

Preferred publish path:

1. Confirm the feature is production-deployed and smoke-tested.
2. Update the release note artifact used by the app, if applicable.
3. Use the canonical release sync path, not ad hoc SQL. In this repo, that has historically been `releases/current.md` plus `scripts/publish-release-notes.mjs` hitting `/api/internal/releases/sync`.
4. Verify the resulting `/updates` or `app_releases` state from the real production source.

If the feature is local/dev only, do not publish a production update-log entry. Prepare the production update-log draft and report that publishing was skipped because the feature is not production-live. Do not ask for a follow-up approval; wait for a later run after production deployment.

Keep production update-log drafts more formal by default. Do not use emojis in the production update-log draft unless the user explicitly asks for a more informal public style.

## Formatting Style

For Bonfire group text and ClickUp drafts, use tasteful emojis as scanability markers:

- 🚦 Live Status
- 🔥 What Changed
- 💡 Why It Matters
- 🧩 API / Frontend / ETL Impact
- 📣 Marketing Angle
- ✅ Validation
- ⚠️ Caveats

Use 4-6 markers per message depending on length. Avoid emoji strings, celebratory filler, and repeated decoration. Keep the tone practical and team-ready.

Do not put an emoji in the title row. The title is always its own plain-text first line; emoji markers begin only on the body rows that follow.

Never substitute ASCII labels, shortcode text, escaped byte sequences, or mojibake for the emoji markers. The final draft and the exact delivered payload must show the real emoji characters above.

Keep routine post-feature updates short:

- 1 title
- 1 compact feature summary
- 1 marketing asset package link/path or explicit "assets missing/blocked" line
- 1 shared team update for text and ClickUp
- 1 clear marketing impact or customer-facing positioning line
- 1 short production update-log draft, only if relevant
- 1 readiness line

Avoid repeating the same facts in multiple sections. Mention API/frontend/ETL implications once unless one category needs special attention. Keep marketing impact present even in short drafts.

## Output Shape

When the user explicitly asks for draft-only, return:

1. `Title`
2. `Feature Release Summary`
3. `Live Status`
4. `Marketing Assets`
5. `Team Update Copy`
6. `Customer-Facing Announcement Copy`
7. `Internal Support/Sales Notes`
8. `Production Update Log Draft`
9. `Delivery/Publish Readiness`

For the default delivery run, return:

- exact destinations confirmed
- exact destinations skipped and why
- title used
- live status confirmed for local/dev/production
- what was sent or posted
- marketing asset package reused or generated
- asset paths/links included in the team-facing release notes
- production update-log publish status
- any blocked destination, auth, or deployment evidence gap

## Quality Bar

- Lead with user and business value, not implementation mechanics.
- Include a short title in every outbound message and delivery report.
- State `Live Status` even when the feature is only local or the answer is `unknown`.
- Use emoji section markers for team text and ClickUp drafts so the update is not a wall of text.
- Reuse one shared team update for Bonfire group text and ClickUp unless different copy is explicitly requested.
- Cut repetition aggressively; if a detail appears in the summary, do not restate it at length in the team update.
- Include marketing impact or customer-facing positioning in every team update.
- Include the marketing asset package path/link or state that assets were missing, generated, failed, or blocked.
- Include "No direct ETL impact" or "No API surface change" when that is true; do not omit a category.
- Make customer talking points usable by non-engineers.
- Make marketing copy factual and non-hypey.
- Keep caveats clear: local-only, not yet deployed, migration not applied, missing credentials, or no production smoke.

