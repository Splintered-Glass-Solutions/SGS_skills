# Demo Video Production Agent Playbook

This is a platform-neutral version of the `demo-video-production` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Produce narrated product demos from real browser footage using Arc, Remotion, FFmpeg, and ElevenLabs. Use for recording, editing, or revising walkthrough videos with a first-demo review before batch production.

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

# Demo Video Production

Create accurate, readable demonstrations of real product behavior. Use actual browser recordings, Remotion for editing and annotations, ElevenLabs for scene narration, and FFmpeg for capture when authorized and final processing.

## Review boundary

Produce one demo for review before continuing the remaining series. A 30–45 second finished sample can establish framing, voice, captions, and annotations first. Do not treat a successful render as approval of the style or create the remaining demos while feedback is pending. Reuse existing cuts and assets when the requested change is narrow.

## Prepare the story

- Reconcile the requested workflow with current customer-facing behavior. Verify the environment, organization, source material, and final outputs before filming.
- Use consistent synthetic names, dates, rosters, and schedules. Do not imply that a roster without guardian emails resolves an email audience.
- Write short, natural prompts a customer would actually type. For example: “Can you suggest six devotional topics for our flag-football camp?” followed by “Can you make a PDF for each one?” Keep internal IDs and technical instructions out of customer prompts.
- Script each scene with narration, exact browser actions, expected result, approximate duration, and annotation. Narration should explain purpose and value rather than every click.
- Start with the useful finished result, explain the task briefly, demonstrate the essential steps, inspect the actual output, and end with a practical next step.
- Rehearse through the final result. Fix product blockers only within current authorization; capture and product repair are distinct scopes.

## Capture and edit

Read [capture-and-edit.md](references/capture-and-edit.md) when recording or rendering on the established Mac setup.

- Prefer Arc for authenticated Bonfire demonstrations. When an external monitor is available, verify and use that Arc window; do not take over the laptop window or capture unrelated content.
- Record bounded scenes with room before and after actions. Verify a short test capture before a long take. Retain originals and record the environment and resource version.
- Show real results. Do not recreate UI to disguise failed workflows. Retrospective conversation footage must not be narrated as a newly performed action.
- Remove mistakes, dead space, and repeated navigation. Label compressed processing time. Use deliberate zooms and highlights; keep document text readable at normal playback size and hold results long enough to inspect.
- For PDFs, show the document inside Studio when available, inspect relevant pages, and separately open a real download if the story promises downloads.
- Keep email drafting, scheduling, dry-run completion, and delivery distinct. A skipped email step proves no delivery. Never activate automation or send to recipients without the current task's authorization.

## Narration and voice choice

For demos narrated as the user, use his communication style: direct, practical, conversational, with natural contractions and short spoken sentences. Explain the task as if walking a customer through it together. Avoid corporate sales language, forced enthusiasm, repeated summaries, and em dashes. Do not imitate typing mistakes or invent personal anecdotes. Keep necessary qualifications brief and attached to what the viewer sees. Use `the user-communication` for additional voice guidance when available. A cloned voice alone does not make a script sound like its speaker.

Keep script revisions separate from already-rendered delivery packages until the corresponding audio, captions, and timing are updated. When only wording is requested, prepare reviewable scripts without automatically regenerating paid audio or resuming a paused series.

- the user is the selected voice for the current FCA demo. Verify its identity in the connected ElevenLabs account; do not infer a voice ID from its display name.
- Optional future-demo candidate: **Hallie - Fun, Young & Feminine**, shown by the user in ElevenLabs with the description beginning “Cute, high-energy feminine voice…”. This is a candidate to audition, not an approved replacement or a verified voice ID. Use a short representative sample before committing a full video to a new voice.
- Confirm account access, usage allowance, voice availability, and applicable licensing before paid generation. Prior plan and company-size confirmations are dated facts, not permanent license guarantees.
- Generate scene by scene and reuse unchanged audio. Store narration text and timing alignment alongside each clip; never store credentials in source, logs, or packages.
- Check pronunciation of FCA, Bonfire, and example names. Synchronize visuals to the spoken words, and derive captions from final audio timing. Re-time captions after speed changes.

## Verification and delivery

- Review the whole cut for factual accuracy, readable text, clean framing, appropriate holds, and agreement among narration, captions, annotations, and visible results.
- Check video resolution, frame rate, audio tracks, duration, full decode, caption bounds, and representative transition frames. Transcript comparison can detect wording mismatches but cannot replace listening for voice quality, pronunciation, or audio artifacts. Explicitly report an outstanding listening review when audio cannot be heard.
- Package the review MP4, caption file, narration script, shot list, raw footage, audio tracks, editable Remotion source/media, and a short verification record. Keep noisy raw captures outside a shareable package if they expose unrelated windows or history.
- Present the first demo and wait for feedback before producing the rest. Draft delivery messages if requested; this skill does not authorize publishing, uploads, sends, or deployment.

## Improve this workflow as we use it

the user has requested ongoing updates to this skill as the demo creation flow improves. After meaningful review feedback, a verified production improvement, or a repeatable failure, update the relevant instruction or reference during the same work. Preserve accepted preferences and replace superseded guidance rather than accumulating conflicting rules. Distinguish proven practices from candidates still being auditioned. Keep project-specific timestamps, resource IDs, and review notes in the project; save only reusable lessons here. Validate changed skill files and sync the scoped changes to the skills archive. Do not change the skill after routine runs that reveal no new lesson.
