# Package File Spec

Use this reference when filling the package files created by `scripts/create_package_scaffold.py`.

## marketing-one-pager.md

Purpose: Give a non-technical marketing teammate the full feature story.

Required sections:

- Feature name
- Live status
- One-sentence positioning
- User problem
- What changed
- Why it matters
- Who it helps
- Before and after
- Suggested marketing angles
- Example copy
- Visual/demo ideas
- Static screenshot ideas
- Proof and source evidence
- Claims to avoid

## copy-bank.md

Purpose: Provide ready-to-adapt copy.

Include:

- 5 headline options
- 5 short social posts
- 3 email/newsletter blurbs
- 3 website/product blurbs
- 5 video caption options
- CTA options

## video-brief.md

Purpose: Guide the Remotion draft and future edited versions.

Include:

- Audience
- Key message
- Video length target
- Story arc
- Shot list
- Voiceover draft
- On-screen text
- Asset list
- Music/sound direction when relevant
- Static screenshot list when still images support the video or social campaign

## static-screenshots/

Purpose: Provide polished still-image assets that marketing can use without opening the video source.

Include:

- 3-6 selected screenshots when the feature has a visible UI or output
- Desktop and mobile variants when relevant
- Cropped/presentation-ready files, not only raw Playwright captures
- `screenshot-captions.md` with caption, alt text, recommended use, environment, and caveat for each still

If no screenshot is available, include `no-screenshot-available.md` with the reason and suggested capture plan.

## usage-guide.md

Purpose: Tell the marketing team how to use the package.

Include:

- Best channels
- Recommended edits before publishing
- Approval needs
- Live-status caveats
- Suggested rollout order

## asset-manifest.md

Purpose: Make every visual/source asset traceable.

For each item include:

- File path
- Source/provenance
- What it shows
- Whether it is production/dev/local/generated
- Any privacy or claim caveat

Static screenshots should also be listed here, even when they are duplicated in `static-screenshots/screenshot-captions.md`.
