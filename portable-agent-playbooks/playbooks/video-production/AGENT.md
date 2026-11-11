# Video Production Agent Playbook

This is a platform-neutral version of the `video-production` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Plan, produce, edit, or refine an AI-assisted film, advertisement, or website video using verified source imagery, generated motion, narration, music, and captions. Use for creative video production; use demo-video-production for product walkthrough recordings.

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

# Video Production

Make a cohesive film that serves the requested audience and action. Use AI as part of an editorial workflow: story first, intentional shots, natural movement, sound, and a finished edit. Reuse approved work when refining an existing film. The user's current instructions, decisions, and budget take precedence over defaults below.

## Brief and research

1. Establish the audience, message, desired action, distribution channel, duration, brand, tone, aspect ratio, deliverables, and review boundaries. Recover existing decisions, assets, scripts, provider access, budgets, and project context before asking again. Ask focused questions only for missing decisions; when the user requests a plan or photos for review first, stop at that requested boundary.
2. Research claims and real places using primary or authoritative sources where possible. Separate a project or opportunity from an operating facility; distinguish general regional advantages from a particular site's verified access. Keep source URLs, dates, and what each source actually supports in the project, not as intrusive warnings in the film. Do not invent facts, locations, access, or rights to make a stronger ad.
3. Write a concise narrative with a clear emotional arc, natural transitions, and a specific closing. Read it aloud for pacing and estimate runtime using spoken words, numbers, and pauses. Put supporting detail in concise on-screen text where it improves comprehension; avoid repeating narration verbatim or cluttering the screen. When requested, present script, visual direction, and scene plan before production.

## Source and plan the picture

- Build a shot list that records each shot's purpose, approximate timing, source, motion, narration, overlay, and transition. Choose strong establishing images; use actual authorized local places and people when authenticity matters. Source and label alternatives honestly: a different location or generic stock is not evidence of the named place or facility.
- Show the actual reference photographs and ask for a selection when the user requests that review. Source-page visibility, search-result previews, Google Street View, and a mockup are not permission to reuse or animate an image. Record creator, original link, license or permission, adaptation and attribution requirements, and any unresolved rights. Do not represent generated motion or an altered historical photograph as documentary footage of present conditions.
- Distinguish locked stills, digital zoom/pan, existing live footage, and AI-animated imagery. Do not describe a slow zoom as natural scene motion. Favor the user's visual direction: photographic realism and recognizable geometry when requested, with website/brand palette, typography, and well-matched icons instead of generic illustrated cards. Treat imagery, labels, and narration together so their combination does not imply an unverified fact.
- For image-to-video prompting, candidate review, and continuity checks, read [references/image-to-video.md](references/image-to-video.md). Use the selected real source as the starting frame, not an invented substitute.

## Generate and edit

- Prefer the user's requested connected tools or signed-in accounts and their existing assets. Discover current model capabilities, image-input workflow, price, and output settings from provider tools; obtain balance and quote before paid generation. Preserve explicit limits across revisions, record starting balance, remaining allocation, prices, job IDs, debits, failed/uncertain charges, and retries. Never purchase or exceed the authorized cap. When the cap is exhausted, request a new limit before further paid work. Do not resubmit an uncertain paid job until reconciled.
- Keep image/art direction separate from motion direction. In motion prompts specify what moves, what remains fixed, camera direction and speed, and duration. Favor restrained, motivated movement and temporal continuity; do not simply loop a short clip to fill a long scene. Preserve a clean editable timeline, original media, source records, and previous accepted export.
- Use the requested editor if available and appropriate; otherwise choose an available tool that preserves editability and explicitly report any limitation. Preserve the accepted script, voice, mix, captions, and timing unless the user asks to change them. Give voice, music, and ambient sound distinct roles; duck music under speech, avoid abrupt starts or endings, and audition the actual mix and names/pronunciations. Do not claim subjective listening or pronunciation review if it did not happen.
- Make overlays purposeful: consistent brand colors and hierarchy, strong contrast, legible type and icons, enough hold time, and space for captions and player controls. Avoid generic diagrams, repeated text, cramped phone layouts, and unwanted disclaimers. Communicate a claim accurately through careful wording or a better visual; retain rights and provenance in accompanying records. Add disclosures in the film only when requested or required for the intended use.

## Review and deliver

- Inspect the actual export at transitions and at the beginning, middle, and end of each generated clip. Check for repeated/skipping frames, shake, warped signage, drifting landmarks, artificial movement, unintended crops, clipped icons, caption collisions, and mismatched narration. Inspect key frames at full resolution and the intended displayed size, especially a phone-sized website player. Iterate on concrete visual defects; prefer one change per test.
- Verify output duration, dimensions, frame rate, full video/audio decode, audio/caption presence and synchronization, and readable captions. Compare unchanged audio or subtitle streams against the prior accepted export where relevant. Browser playback is additional evidence, not a substitute for real-time visual and listening review; report what was actually checked and what remains unverified.
- Deliver a playable video and relevant captions, poster, script, credits/source and license notes, plus an editable project or reproducible render instructions where practical. Separate local review, publication rights, user acceptance, deployment, and live playback; do not claim one proves another. Only publish or replace a live site asset when authorized for that destination, and follow its release workflow. Summarize improvements, remaining visual/rights limitations, and spending without burying the film in production jargon.
