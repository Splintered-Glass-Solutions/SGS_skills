---
name: doc-sync
description: Audit a repository's documentation and improve it so the repo can serve as its own up-to-date source of truth across machines and future sessions. Use when the user asks whether repo docs are sufficient, wants a canonical docs spine, needs README/docs/runbooks reorganized, or wants the project vision, current state, architecture, workflows, decisions, blockers, and safe continuation path documented from repo evidence.
---

# Doc Sync

## Purpose

Use this skill to make a repository self-explanatory without relying on prior chat context, memory, or tribal knowledge. The goal is not to rewrite every doc; it is to create or tighten a small canonical documentation spine that points to deeper technical and operational references.

## When To Use

Trigger this skill when the user asks to:

- audit repo documentation quality
- make a repo easier to pick up on another machine
- add a canonical handbook, docs index, status doc, or decision log
- reconcile fragmented README/docs/runbooks into a clearer source of truth
- document project vision, product purpose, current state, workflows, or constraints
- preserve operational knowledge in-repo before handoff or future work

Do not use this skill as a substitute for product invention. If the repo does not support a claim, mark it as missing, uncertain, assumed, or blocked rather than filling the gap with speculation.

## Workflow

1. Classify the work as `planning` plus `build_work` for docs unless the user explicitly wants assessment only.
2. Inspect the repo before editing:
   - `README*`
   - `docs/`, `architecture/`, `planning/`, `runbooks/`, `handoff/`, `notes/`
   - package scripts, test commands, CI config, deployment config, env examples
   - recent changed files when relevant
3. Assess whether the repo already covers these areas well enough for a cold start on another machine:
   - vision and purpose
   - target users and product goals
   - current feature set and maturity
   - architecture and major integrations
   - setup and local development
   - deployment and environment expectations
   - testing and verification workflows
   - important decisions, tradeoffs, and constraints
   - roadmap, open gaps, and current blockers
   - canonical source-of-truth location
4. Identify what is missing, stale, fragmented, duplicated, or buried in the wrong place.
5. Create or tighten a canonical docs spine. Prefer a small set of durable entrypoints over broad rewrites.
6. Preserve useful existing docs. Add navigation and cross-links instead of flattening everything into one file.
7. Update docs using repo evidence only. Distinguish clearly between:
   - implemented
   - planned
   - verified
   - assumed
   - blocked
8. Sanity-check the entrypoints and links after editing.

## Canonical Docs Spine

The usual target structure is:

- root `README.md` updated so the docs spine is discoverable immediately
- `docs/README.md` or equivalent docs index as the obvious starting point
- project overview or product-foundation doc
- current-state or status doc
- architecture/system map if one does not already exist or is hard to find
- decision log, conventions doc, or repo-operating-rules section
- links to deeper runbooks, QA docs, deployment docs, and reference material

Do not force all of these if the repo already has strong versions of some. Tighten freshness and discoverability first.

## Evidence Rules

- Prefer repo files, scripts, config, tests, and current branch state over memory or prior conversation.
- Memory can provide leads, but the repo must remain the final source of truth.
- Do not invent deployment status, roadmap items, user claims, or architecture intent that the repo does not support.
- If a state is unclear, label it clearly instead of smoothing it over.
- Separate local proof from hosted or production proof when the repo distinguishes them.

## Editing Guidance

- Prefer additive doc structure over deleting useful notes.
- Keep duplicated content low; link outward from canonical docs to specialized references.
- Make the project easy to continue safely: include current state, blockers, verification commands, and operating constraints where appropriate.
- If a repo already has excellent docs, avoid gratuitous rewrites. Improve entrypoints, freshness, and explicit state labeling instead.

## Expected Output

End with:

- a short assessment of whether the repo had enough documentation before changes
- the highest-value gaps found
- what docs were added or updated
- what was sanity-checked
- any remaining uncertainty, stale areas, or blocked status

## Example Triggers

- "Audit this repo docs and make it self-explanatory across machines."
- "Do we have enough documentation here for another agent to pick this up cold?"
- "Create a canonical docs set for vision, current state, architecture, and blockers."
- "Tighten the README and docs so the repo is the source of truth."
- "Reorganize our scattered docs into one obvious starting point."

No bundled resources are required for the initial version of this skill.
