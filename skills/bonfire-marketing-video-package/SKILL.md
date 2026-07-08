---
name: bonfire-marketing-video-package
description: Create Bonfire feature marketing packages after a new feature is finished or validated. Use when Preston asks to turn a Bonfire feature into marketing copy, a one-pager, static screenshot assets, Remotion/raw video content, social/video ideas, Google Drive deliverables, or a Bonfire text-thread update with links to the feature folder and video.
---

# Bonfire Marketing Video Package

## Overview

Use this skill after meaningful Bonfire feature work to create a marketing-ready package for non-technical teammates: a plain-language one-pager, copy bank, static screenshot assets, video brief, Remotion source/raw video files, rendered draft video when possible, and a Bonfire text-thread announcement linking to the Drive folder and video.

Default to execution, not draft-only. Preston has authorized this workflow to create the feature folder, upload deliverables, and send the Bonfire text-thread update unless he explicitly says draft only, do not upload, or do not send.

## Fixed Destinations

- Parent Google Drive folder: `https://drive.google.com/drive/folders/1CaF0UIG9c3gCcl449LWl2fqw1jzAns0s?usp=sharing`
- Parent Drive folder ID: `1CaF0UIG9c3gCcl449LWl2fqw1jzAns0s`
- Bonfire Messages thread: `chat91142418163091161`
- Folder naming pattern: `<Feature Name> - Marketing Package - YYYY-MM-DD`

If Google Drive or Messages tooling is unavailable, still create the local package and report the exact blocker. Do not claim a Drive link or video link exists unless it was created or verified in the current run.

## Related Skills

- Use `bonfire-feature-release-update` for production/dev/team release-update copy and live-status framing.
- Use `marketing-asset-generation` for persona-specific static promotional images and launch asset prompts.
- Use `remotion-best-practices` when writing or rendering Remotion code.
- Use `google-drive:google-drive` when the Google Drive connector is needed.
- Use `preston-communication` only if the outgoing text needs Preston-specific tone refinement beyond the template here.

## Workflow

1. Gather evidence.
   - Inspect the relevant repo status, diff, commits, docs, route/component files, tests, screenshots, and validation logs.
   - Identify whether the feature is `local`, `dev`, `production`, `not live`, or `unknown`.
   - Do not market a feature as live in dev or production without environment-specific proof.
   - Separate product value from implementation detail. Non-technical marketing readers should understand who benefits and why.

2. Create the local package scaffold.
   - Run `scripts/create_package_scaffold.py --feature "<Feature Name>" --root <local-output-root>`.
   - Use a temporary or repo-local `output/marketing-packages/` root unless Preston names another local location.
   - Replace the scaffold placeholders with real copy, evidence, asset references, and video directions.

3. Produce the package files.
   - `marketing-one-pager.md`: executive summary, user problem, value, audience, proof points, caveats, and suggested usage.
   - `copy-bank.md`: headlines, short social posts, email blurbs, website blurbs, video captions, and CTA options.
   - `video-brief.md`: creative concept, audience, story arc, shot list, voiceover draft, on-screen text, and asset list.
   - `usage-guide.md`: what the marketing team should do with the files, recommended channels, and what not to claim yet.
   - `asset-manifest.md`: all screenshots, clips, recordings, generated assets, Remotion source, and rendered videos with provenance.
   - `static-screenshots/`: polished still-image assets for social, website, sales, and internal enablement.
   - `static-screenshots/screenshot-captions.md`: suggested captions, alt text, and usage notes for each selected screenshot.
   - `remotion/`: editable Remotion source for the feature video.
   - `renders/`: draft rendered video files, ideally `feature-video-draft.mp4`.
   - `raw-assets/`: source screenshots, recordings, images, JSON, or other raw visual material used by the video.

4. Prepare static screenshot assets.
   - Include at least 3-6 strong stills when the feature has a visible UI, flow, rendered output, or before/after state.
   - Prefer clean, cropped, presentation-ready screenshots over noisy test artifacts.
   - Save originals or uncropped captures in `raw-assets/`; save edited/selected stills in `static-screenshots/`.
   - Include desktop and mobile variants when the feature has meaningful responsive behavior.
   - Add captions, alt text, recommended use, environment, and caveats in `static-screenshots/screenshot-captions.md`.
   - If no screenshot is possible, add `static-screenshots/no-screenshot-available.md` explaining why.

5. Build Remotion/raw video content.
   - Prefer existing screenshots, Playwright screenshots, QA artifacts, browser recordings, or generated graphics that show the real feature.
   - Create a short draft video composition that the team can edit. Default to a practical 20-45 second feature explainer.
   - Include both source and rendered output when rendering is feasible.
   - If rendering fails, keep the Remotion source and include a clear `video-render-blocker.md`; do not call the video ready.

6. Create the Drive folder and upload.
   - Use the Google Drive connector when available. If tools are not loaded, search for Google Drive tools with `tool_search`.
   - Create a child folder under folder ID `1CaF0UIG9c3gCcl449LWl2fqw1jzAns0s`.
   - Folder name must begin with the feature name.
   - Upload every deliverable file and the static screenshot, Remotion, render, and raw asset folders.
   - Capture the Drive folder URL and the direct video URL for the rendered draft video.
   - Verify that the links are usable from the connector response or Drive metadata.

7. Send the Bonfire text-thread update.
   - Send to local Messages chat `chat91142418163091161`.
   - Use AppleScript or the available Messages connector/tooling.
   - Verify success with a read-only `~/Library/Messages/chat.db` query against `chat91142418163091161` when local Messages tooling was used.
   - The text must include the feature name, one-sentence value explanation, Drive folder link, and direct video link.

8. Report completion.
   - List local package path, Drive folder link, direct video link, and text-thread delivery verification.
   - List the static screenshot assets included and any screenshot gaps.
   - Call out live-status caveats and any unverified claims the marketing team should avoid.

## Marketing One-Pager Requirements

Keep the one-pager useful to a non-technical marketing teammate.

Include:

- Feature name
- Live status and caveat
- One-sentence positioning
- User problem
- What changed
- Why it matters
- Who it is for
- Before/after story
- Suggested marketing angles
- Visual proof or demo ideas
- Copy examples
- Short FAQ
- Claims to avoid until verified
- Source evidence and screenshots

Write in buyer-outcome language. Avoid internal route names, table names, and implementation mechanics unless they explain a claim or caveat.

## Video Package Requirements

Default video structure:

1. Problem opener, 3-5 seconds
2. Feature reveal, 5-8 seconds
3. Demo beats, 10-20 seconds
4. Outcome/value statement, 5-8 seconds
5. CTA or next step, 3-5 seconds

Save:

- editable Remotion source
- static screenshots and caption/alt-text notes
- raw screenshots/recordings
- rendered MP4 if feasible
- script/voiceover text
- shot list
- on-screen text list
- usage notes for social, website, sales, and internal enablement

## Bonfire Text Template

Use this shape, keeping it mobile-readable:

```text
New feature video ready: <Feature Name>

<One sentence explaining what the feature does for users.>

Marketing folder: <Drive folder URL>
Video: <Direct video URL>

Status: <local/dev/production/unknown plus short caveat>
```

If there is no rendered video, change the title to `New feature marketing package ready` and replace `Video:` with `Video render status:`. Do not say "video ready" without a rendered, uploaded video link.

## Quality Bar

- Lead with user value and marketing usage, not implementation notes.
- Use concrete examples and suggested copy the team can adapt immediately.
- Preserve live-status accuracy.
- Include raw/editable video material, not only final prose.
- Upload all files to the correct Drive parent folder.
- Send the Bonfire text update after upload unless explicitly told not to.
- Never include secrets, access tokens, private customer data, raw logs, or unreleased-sensitive claims.
