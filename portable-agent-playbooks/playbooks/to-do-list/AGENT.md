# To Do List Agent Playbook

This is a platform-neutral version of the `to-do-list` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Put the current the agent task into to-do-list gathering mode. Use when the user says to start a to-do list, wants to collect related tasks for later, or invokes $to-do-list. Capture each actionable item as a concise planning note without planning, implementing, messaging, or executing it.

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

# To Do List

## Overview

Use this skill as the gathering phase for a later planning-and-execution
workflow. While active, treat each new user message as a candidate to-do item
unless the user explicitly changes modes or asks for something outside the
list.

## Gathering workflow

1. Rename the current the agent task with the `📋` prefix. If this is the first
   message and the current name is only a generic or invocation-derived title,
   use `📋 <useful topic-specific name>` based on the first substantive to-do
   item. Otherwise, preserve the existing thread name exactly after the
   prefix.
2. Classify the user's latest message as a to-do item. Preserve its intent,
   but remove conversational filler and redact secrets or sensitive details.
   Preserve an explicit batch ID verbatim when supplied. Otherwise, infer only
   an obvious initiative label from the active task; do not invent a batch ID
   or ask a question while gathering.
3. Save exactly one small Markdown note using the existing `note` skill's
   capture rules and location. Do not overwrite an existing note.
4. Return only `Noted.` after a successful save.
5. Do not inspect repositories, create tasks, edit product files, send
   messages, make plans, ask clarification questions, or take follow-on
   action during gathering mode.

## Mode boundaries

- Gathering mode is capture-only. A captured item is not an approved plan,
  commitment, task assignment, or implementation authorization.
- If the user says to stop, switch modes, or use a different skill, follow that
  instruction immediately.
- `to-do-list-planning` is the next phase. It turns one bounded note set into
  a proposed Batch Brief; do not perform that analysis from this skill.
- When a later execution phase is explicitly started, use the existing
  `bulk-edits-thread` workflow for repository preparation and preserve its
  safety boundaries.
