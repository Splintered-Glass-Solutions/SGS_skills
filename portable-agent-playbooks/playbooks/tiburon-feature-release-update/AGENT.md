# Tiburon Feature Release Update Agent Playbook

This is a platform-neutral version of the `tiburon-feature-release-update` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Create and send Caleb concise Tiburon post-feature release updates after implementation, validation, migration, or deployment work. Use when the user asks to update Caleb, send Tiburon release notes, report what shipped, explain a completed feature, share testing instructions or screenshots, request user testing, or summarize Tiburon release status and next steps.

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

# Tiburon Feature Release Update

## Overview

Turn verified Tiburon engineering work into a concise email Caleb can act on.
Default to sending the email in the current run when this skill is explicitly
invoked. Draft only when the user explicitly asks to review first, draft only, or
not send.

Read [references/release-update-template.md](references/release-update-template.md)
before drafting.

## Related Skills

- Use `feature-finish-line` when validation is incomplete.
- Use `deploy` when the user asks to publish changes before the update.
- Use `full-suite-tests` when the update requires broad test proof.
- Use `the user-communication` to match the user's normal email voice.
- Use Gmail or Superhuman Mail to find the verified Caleb thread and deliver.

## Evidence Workflow

1. Gather current evidence from the Tiburon repo:
   - latest request and feature finish-line summary
   - `git status --short --branch`
   - relevant commits, changed routes, migrations, tests, and screenshots
   - deployment record and public route smoke checks
   - hosted database migration state when database changes are claimed
2. Separate proof layers:
   - `local`: implemented or validated only in the local worktree
   - `hosted`: deployed to the single Tiburon Vercel environment and smoke-tested
   - `customer-visible`: reachable through the stable URL and appropriate login
   - `unknown`: no current evidence
3. Verify the exact hosted targets before making hosted claims:
   - Vercel team: `tiburon-ai`
   - Vercel project: `tiburon-dev`
   - stable URL: `https://tiburon-dev.vercel.app`
   - Git repository: `Stewardship-IS/tiburon`
   - deployment branch: `dev`
   - remote Supabase project: `uqgvqwxenppqsltishsk`
4. Follow the repository provider boundary:
   - run `./bin/tiburon doctor <provider>` before provider reads or writes
   - use `./bin/tiburon` for GitHub, Vercel, and Supabase operations
   - never use host-level provider CLIs
   - never start or use local Supabase for this workflow
5. State validation exactly:
   - commands or browser flows that passed
   - environment where they passed
   - failures, skipped checks, and remaining uncertainty

Do not call a deployment successful because a Git push succeeded. Confirm the
deployed commit, ready state, stable alias, and public route response.

## Email Content

Lead with product and workflow value. Keep implementation detail subordinate.
Every email must include:

- a short subject
- `Live status`
- what changed
- why it matters to Tiburon users
- validation and environment proof
- what Caleb should test
- known caveats
- next steps or decisions needed

Include API, frontend, data, auth, or security implications only when they are
material. Say `No database change` or `No auth change` when useful.

When screenshots exist, attach or link only the clearest 1-3 images. Label what
each image proves. Do not attach duplicate, stale, private, or misleading
screenshots.

## Delivery Workflow

Explicit invocation of this skill is approval to send one release-update email
to Caleb in the current run. It is not approval for unrelated external messages.

1. Search Gmail or Superhuman for recent Tiburon correspondence with Caleb.
2. Resolve Caleb's exact verified email from the existing thread or contacts.
   Do not guess or hardcode an unverified address.
3. Prefer replying in the latest relevant Tiburon testing/update thread.
   Start a new thread only when the topic is materially different.
4. Inspect the exact recipient, subject, body, links, and attachment names.
5. Remove secrets, tokens, raw client data, private source-document contents,
   provider payloads, and irrelevant logs.
6. Send unless the user requested draft-only.
7. Verify the sent message or thread state with a read-only mail check.

If the mail connector is unavailable or the recipient cannot be verified, stop
before sending and return the complete draft plus the exact blocker.

## Access And Testing Details

- Use the stable URL, not an ephemeral Vercel deployment URL.
- Describe magic-link login with the user's approved email.
- Never email passwords, API keys, service-role keys, session links, or tokens.
- Confirm Caleb's account is active before saying he can sign in.
- Distinguish account readiness from successful end-to-end login proof.
- Ask Caleb to report the ticket number, browser/device, and screenshot for any
  defect without including private ticket contents in the reply.

## Safety Rules

- Do not claim hosted, live, migrated, or customer-visible without current proof.
- Do not expose private source packet contents or extracted client rows.
- Do not attach raw tickets unless the user explicitly approves that exact file.
- Do not trigger deployments, migrations, database permission changes, or paid
  OCR runs merely because release communications were requested.
- Do not start local Supabase.
- Preserve unrelated dirty or untracked files.
- Keep the email concise enough to scan on a phone.

## Output

After delivery, report:

- recipient and subject
- whether the email was a reply or new thread
- live status stated
- links and attachment names included
- sent-message verification
- any skipped evidence or unresolved caveat

For draft-only requests, return:

1. `Subject`
2. `Email Draft`
3. `Live Status`
4. `Evidence Used`
5. `Attachments`
6. `Send Readiness`
