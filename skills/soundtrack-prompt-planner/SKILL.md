---
name: soundtrack-prompt-planner
description: Use when creating, adapting, or generalizing generated-music soundtrack prompt plans for games, apps, videos, products, interactive experiences, or branded worlds. Produces paste-ready prompts for Suno, Udio, Lyria, or similar music generators; useful for mode-based game soundtracks, adaptive music states, loopable cues, stingers, ambience beds, shared motif systems, and cohesive soundtrack packages.
---

# Soundtrack Prompt Planner

## Overview

Create a reusable generated-music prompt package from a project brief, repo, mood,
or existing soundtrack plan. Favor paste-ready prompts that can be generated
immediately, then auditioned and mapped to product states.

## Workflow

1. Classify the product: game/app/video/brand/world, audience, primary loop, and
   emotional arc.
2. Inspect provided context. If working in a repo and the user wants execution,
   look for docs, audio systems, asset manifests, scene/state names, existing
   music files, and gameplay modes before inventing track names.
3. Choose a soundtrack direction in one sentence: genre, energy, emotional
   posture, and production style.
4. Decide whether the package needs a shared motif. Use a motif when the user
   wants soundtrack cohesion across several cues, a recognizable game identity,
   or variations that feel connected without sounding repetitive.
5. Build a mode list from real states first. If context is thin, use the default
   15-track set below and rename it to fit the project.
6. Write each prompt with consistent constraints and enough distinct detail that
   generated tracks do not collapse into the same cue. Preserve soundtrack
   cohesion, but treat same-sounding tracks as a failure.
7. Add notes for looping, replacement targets, layering, stingers, and where each
   cue maps in the product.
8. Validate the package against the review checklist. If saving files, add the
   plan to the most discoverable docs or design/audio location.

## Output Format

Use this structure unless the user requested a different format:

```markdown
# Soundtrack Prompt Plan: [Project Name]

## Summary
[1-2 paragraphs describing the soundtrack direction and product fit.]

## Prompt Template
`Instrumental seamless loop, [project genre] music, [scene mood], [instrument palette], [tempo/energy], [texture], no vocals, no lyrics, [negative constraints], non-distracting background music, clean loop ending`

## Creative Defaults
- Instrument palette: ...
- Tempo: ...
- Safe/low-pressure cues: ...
- Danger/high-pressure cues: ...
- Looping/stinger guidance: ...

## Main Motif
- **Motif Title:** [Project Name] - Main Melodic Motif
- **Motif Prompt:** [Short generated-music prompt for the standalone motif.]
- **Reuse Guidance:** Reference the motif loosely, later in each cue, and below
  the main texture. Do not make every track lead with the motif.

## Track Set

### 1. [Track Name]
- **Mode / Use Case:** ...
- **Music Role:** ...
- **Generated-Music Prompt:** ...
- **Notes:** ...

## Review Criteria
- Paste-ready.
- Distinct from the other tracks.
- Cohesive as one soundtrack package.
- Correctly tied to product scenes, states, or user actions.
- Calm/readable enough for repeated use unless intentionally a sting.
```

Use **Suno Prompt** instead of **Generated-Music Prompt** when the user names
Suno specifically.

### Copyable Title / Style Description Fields

When the user asks for generated-music fields, copyable fields, title and
description, title and style description, or output for pasting into Suno/Udio
form fields, convert the package into separate individually copyable blocks.
Start with the main motif when one exists. For each cue, output the title block
first and the style-description block second:

```text
[Cue Title]
```

```text
[Paste-ready style description or prompt text]
```

Do not combine `Title:` and `Style Description:` in the same code block unless
the user explicitly asks for labeled pairs. Keep each field clean of labels so
it can be pasted directly into a generator UI. Use concise style descriptions
when the user asks for style descriptions; use the full prompt when the user
asks for full prompts.

## Motif Handling

When using a shared motif, create one standalone motif prompt before rewriting
the full track list. Keep it short, memorable, and reusable:

```text
[Project Name] - Main Melodic Motif
Instrumental short melodic motif, [project genre] music, memorable but subtle 4 to 6 note theme, [key/emotional posture], [core instruments], [tempo/energy], designed to be reused quietly across menu, gameplay, danger, failure, and victory cues, no vocals, no lyrics, no busy lead melody, clean natural ending
```

Then add motif language to the track prompts carefully:

- Prefer: `with a very subtle optional echo of the main motif appearing only later in the loop`.
- Prefer: `with only a faint delayed hint of the main motif if it fits naturally`.
- Prefer: `with a restrained background reference to the main motif only after the groove is established`.
- Prefer: `with the main motif only implied subtly in a later background layer`.
- Prefer: `with a barely-there delayed trace of the main motif stretched into ambience`.
- Avoid: `features the main motif`, `introduces the main motif`, `prominent main motif`, `main motif in the lead`, or putting the motif instruction near the start of every prompt.
- Do not force the motif into stingers or ambient beds. Make it optional, faint,
  delayed, and subordinate to the cue's primary job.
- Vary the reuse language across cues so the generator does not over-weight the
  motif instruction.

## Track Variety

Make the package cohesive without making it feel like the same song repeated.
The cue title and product state should drive the music first; shared genre,
palette, and motif references should act as connective tissue only.

- Make every cue meaningfully different in at least 3-4 dimensions: tempo,
  rhythm pattern, instrument palette, density, harmony, mood, texture, register,
  ambience, percussion style, and melodic activity.
- Avoid reusing the same instrument list in every prompt.
- Avoid keeping every cue in the same BPM range.
- Avoid describing every cue as a variation on the main theme.
- Use contrast intentionally: include sparse cues, rhythmic cues, ambient cues,
  tense cues, warm cues, dark cues, and resolving cues when the product supports
  those states.
- Let some cues be melody-light or texture-first. Not every track needs a clear
  lead phrase.
- When using a shared motif, make the motif less prominent than the cue-specific
  identity. The motif should not be the reason every track sounds connected.

## Default 15-Track Set

Adapt this set to the project instead of copying labels literally:

1. Title / Main Menu
2. Opening / Wake-Up / First Interaction
3. Safe Exploration / Low Pressure
4. Activity Focus / Core Work Loop
5. Travel / Traversal / Route Movement
6. Resource Gathering / Collection / Discovery
7. Crafting / Loadout / Preparation
8. Building / Creation / Customization
9. Social / Hub / Village / Base
10. Night / Downtime / Ambient Bed
11. Light Encounter / Minor Conflict
12. Danger Escalation / High Threat
13. Boss / Crisis / Major Set Piece
14. Failure / Loss Sting
15. Victory / Resolution / Endgame

For non-game products, translate the modes into equivalent user states:
onboarding, browsing, focus work, confirmation, error, upgrade, celebration,
idle ambience, launch moment, and closing resolution.

## Prompt Rules

- Start prompts with the intended form: `Instrumental seamless loop`, `Instrumental short sting`, or `Instrumental ambient bed`.
- Name the product genre and emotional role early: cozy survival, tactical horror,
  premium SaaS focus, arcade racer, educational calm, etc.
- Include a specific instrument palette. Avoid generic labels like "epic music"
  unless the product truly needs it.
- Include tempo or energy. Use BPM when helpful.
- Include texture and mix notes: dry, dusty, underwater, close interior, wide
  outdoor, low-fi, polished, toy-like, organic, metallic, warm, cold.
- Include negative constraints that protect the product: no vocals, no lyrics,
  no trailer hits, no sudden jump scares, no EDM drop, no harsh drums, no busy
  lead melody, no copyrighted references.
- Keep loop prompts stable and non-distracting. Reserve peaks, hard endings, or
  big cadences for stingers.
- Make danger cues darker through harmony, pulse, register, and texture rather
  than sudden volume spikes.
- Make every track distinct by changing at least 3-4 of: tempo, rhythm pattern,
  instrument palette, density, harmony, mood, texture, register, ambience,
  percussion style, or melodic activity.
- If a shared motif is requested, mention it late in each prompt, framed as an
  optional delayed hint or background allusion, not a lead melody.
- Do not ask the generator to imitate a specific living artist, copyrighted
  soundtrack, or named song. Use genre, era, instrumentation, and mood instead.

## Practical Mapping Notes

When the project already has audio code or shipped tracks, include a short note
for likely mapping:

- Replacement candidate: existing cue id or filename.
- Expansion candidate: new optional state not currently implemented.
- Layer candidate: can sit over an existing loop.
- Sting: should be exported short or trimmed after generation.
- Ambience bed: should leave headroom for SFX, dialogue, UI, and gameplay.

When the user wants implementation after generation, save exact source notes and
license/provenance metadata next to audio assets.

## Review Checklist

Before finalizing:

- Count tracks and prompts; ensure every track has exactly one paste-ready prompt.
- Confirm the prompt package matches the actual product, not the source template.
- Confirm prompts are cohesive but not interchangeable.
- Confirm no two adjacent cues read like the same prompt with a few words
  changed.
- Confirm the soundtrack has real contrast: not one BPM band, not one instrument
  list, not one rhythm pattern, and not one mood repeated.
- Confirm loops do not specify hard endings, except stingers/resolution cues.
- If using a shared motif, confirm motif references are loose, subtle, late in
  the cue, and varied across prompts.
- Confirm negative constraints match the product's risks.
- Confirm any saved file is linked from a discoverable docs or asset index.
