---
description: Create and deliver a concise StrIQ feature release update to the StrIQ L10 Team group text.
argument-hint: [feature-or-release-context]
---

# StrIQ Feature Release Update

Create a concise StrIQ feature release update and, unless the user explicitly asks for draft-only behavior, deliver it to the StrIQ L10 Team group text.

The user invoked this command with: $ARGUMENTS

## Preflight

1. Read and follow the local skill at `/Users/preston/.codex/skills/striq-feature-release-update/SKILL.md`.
2. Treat `$ARGUMENTS` as the feature, release, validation summary, deployment context, or StrIQ workstream to summarize.
3. If `$ARGUMENTS` is empty, infer the StrIQ feature context from the current conversation when obvious; otherwise ask for the feature or release context.
4. Do not claim stage/dev or production status without current deployment or smoke-test proof.
5. Do not send if the user explicitly says draft only, do not send, review first, or similar.

## Required Behavior

- Gather enough evidence to classify `Live Status`.
- Draft mobile-first L10 copy with a plain title line and concise emoji section markers.
- Verify the exact Messages destination from the skill before sending.
- Send to the verified StrIQ L10 Team group text by default when delivery is authorized.
- Verify delivery with a read-only Messages database query when local Messages was used.

## Output

For draft-only runs, return the skill's draft shape:

- `Title`
- `Feature Release Summary`
- `Live Status`
- `StrIQ L10 Team Text Copy`
- `Delivery Readiness`

For delivery runs, return:

- destination confirmed
- title used
- live status and proof
- message sent
- Messages verification result
- any blocker or caveat
