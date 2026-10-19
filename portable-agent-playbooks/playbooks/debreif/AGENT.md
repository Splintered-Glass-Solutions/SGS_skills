# Debreif Agent Playbook

This is a platform-neutral version of the `debreif` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Debrief a call from Fathom, with connected email/calendar recaps or emailed transcripts as fallback. Use when the user invokes /debreif or asks to name, summarize, contextualize, or extract follow-up work from a meeting. Rename the current thread with a 📞 prefix, gather project and prior-call context, separate discussed commitments from suggested follow-ups, and create a reviewable to-do-list capture note.

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

# Debreif

## Overview

Turn one meeting into a concise, evidence-backed debrief and a review queue.
Treat the result as planning and capture only: never send email, create
external tasks, change project files, or present a suggested follow-up as an
agreed commitment.

## Invocation and target selection

Support both forms:

- `/debreif <person, company, topic, or date>`: use the supplied clue to find
  the call.
- `/debreif`: use the most recent completed meeting on the user's calendar as
  the target. If calendar search is unavailable, use the newest plausible
  Fathom meeting. If there are multiple equally plausible matches, ask one
  concise question rather than silently choosing.

Use America/Chicago for relative dates and preserve the meeting's original
date, participants, title, and source links in the internal working context.

## Source recovery order

1. Use Fathom first. Read and follow `$fathom-notes-api` when direct Fathom
   tools are absent or unreliable. List meetings with summaries and action
   items, identify the candidate using title/date/participants, and retrieve
   the transcript for the selected recording when available. Cross-check the
   generated summary and action items against transcript speaker turns.
2. If Fathom is unavailable, rate-limited, missing the recording, or missing
   useful notes, use the connected email/calendar search. Look for a Gemini
   recap, a Fathom recap email, or an emailed transcript using the call title,
   date, participants, company, and distinctive agenda terms. Fetch the full
   matching email thread before relying on its snippet.
3. If only a partial fallback is found, continue with the available evidence
   and explicitly state the source and gap. Never claim transcript coverage
   when only a recap email was found, and never invent a recording URL.

Do not print API keys, raw credentials, or a full sensitive transcript. Keep
raw source payloads out of the repository; temporary working files belong in a
task-specific `/tmp/<task-slug>/` directory if needed.

## Context gathering

Infer the project, client, or initiative from the call and verify it with:

- the active project/workspace and relevant local docs;
- recent project history and decisions, using read-only file and Git history
  inspection when useful;
- earlier Fathom calls or email recaps involving the same people/project; and
- durable planning notes or prior debriefs, clearly labeling them as prior
  context rather than current-call evidence.

Prefer narrow searches around the identified project and participants. Preserve
the distinction between current-call facts, prior history, planned work, and
your own inference. Include a confidence note when identity or context is
uncertain. Do not modify the repo while gathering context.

## Thread title

After identifying the call subject, rename the current agent thread to:

`📞 <call subject>`

Use the available thread-title tool and keep the subject concise enough for the
sidebar. Use the actual call subject, not a generic title such as “Call
Debrief”. This is a status replacement: do not carry any existing leading
status marker into the new title. If the title tool is unavailable, report the
exact title that should be used and continue with the debrief.

## Required output

Return these sections in this order:

1. `Call`: subject, date, participants, source used, and confidence.
2. `Summary`: a short plain-language summary of the purpose, decisions, open
   questions, and meaningful discussion.
3. `Context`: the project/history/prior-call context that changes how the call
   should be understood, with source or evidence labels.
4. `Discussed action items`: only work explicitly assigned, promised, or
   clearly agreed in the call. For each item include owner, due date if stated,
   and a short evidence basis. Use “unassigned” or “not stated” rather than
   guessing.
5. `Suggested follow-ups`: useful items implied by gaps, dependencies, or
   decisions but not explicitly discussed. Label every item `Suggested — not
   discussed` and keep these separate from commitments.
6. `To-do list for review`: a checkbox list containing both groups, with
   `[Discussed]` or `[Suggested]` labels, so the user can adjust, delete, or add
   items.
7. `Coverage`: what was found, what was unavailable, and which claims are
   based on fallback evidence.

Keep the debrief useful without dumping the transcript. Quote only short
snippets when a precise commitment or decision needs proof; otherwise paraphrase.

## To-do-list handoff

Create exactly one capture-only to-do-list note containing the reviewed list,
using the existing `$to-do-list` skill's note-capture rules and location. The
note may include both discussed and suggested items, but must preserve those
labels and state that suggested items are not commitments.

Do not invoke `$to-do-list` as an interactive gathering mode that replaces the
thread title with `📋` or returns only `Noted.`; that mode is for a user's raw
to-do message. For this skill, perform the same single-note capture as the
handoff artifact, retain the required `📞` title, then show the checkbox list
for review. Do not execute, assign, message, or schedule any item.

If the note cannot be saved, say so plainly and still show the reviewable list;
never claim the handoff was created when it was not.
