---
name: marketing-asset-generation
description: Generate or prepare reusable persona-specific Bonfire promotional image assets for feature launches, release notes, Feature Finish Line closeouts, product updates, marketing packages, and social/share collateral. Use when Preston asks for marketing assets, launch images, persona-specific graphics, promotional screenshots, feature announcement visuals, saved asset packages, or release/finish-line marketing images for Bonfire features.
---

# Marketing Asset Generation

## Overview

Use this skill to turn a Bonfire feature into a reusable local marketing asset package: persona-specific headlines, subtitles, image prompts, generated PNG image assets, screenshot references, and saved asset paths.

This is a local content-production workflow, not a Bonfire app feature. Do not add product UI, backend storage, database schema, asset hosting, or release-note publishing unless the user explicitly scopes that work separately.

## Safety Gate

Before generating assets, classify each requested capability:

- Safe now: local skill workflow, local file package, persona copy, image prompts, generated local PNG images, generated images from an image tool when requested, screenshot reuse, local manifests, and integration notes for finish-line or release-update workflows.
- Backlog: in-app multi-select UI, screenshot upload/select UI, persisted asset library, API-backed generation jobs, cloud storage links, approval workflow, brand admin settings, and automatic release-note publishing.
- Blocked: claims that a feature is live without dev or production proof, images using private customer data, assets based on unreleased-sensitive facts without permission, or generated screenshots that could be mistaken for real UI when accuracy matters.

If a request is out of scope or risky, add it to the package `backlog.md` with the reason instead of implementing it silently.

## Inputs

Accept these inputs from the user or infer conservative defaults:

- Feature name.
- Feature description.
- Target personas: business owner, business employee, technical buyer, non-technical buyer, church network leader, senior pastor, executive pastor, communications pastor/director, ministry leader, congregant, or additional named personas.
- Include screenshot: yes or no.
- Screenshot paths or URLs, when available.
- Asset sizes: square, landscape, story.
- Output options: headline, subtitle, persona-specific image, saved asset links or files.
- Live status: local, dev, production, not live, or unknown.

If no personas are selected, do not fail. Create the package with a `persona-selection-needed` row and recommend the smallest persona set.

## Workflow

1. Gather evidence.
   - Inspect the feature summary, diffs, finish-line report, release notes, screenshots, and validation status available in the current thread.
   - Do not browse or inspect production unless the user asks for live verification.
   - Do not claim dev or production availability without proof from that environment.

2. Read the persona and brand guide when producing copy or prompts:
   - `references/persona-brand-guide.md`

3. Create the local asset package.
   - Before creating a new package, run `scripts/find_marketing_asset_package.py --feature-name "<Feature Name>"` from the relevant repo or search root.
   - If an existing package is found, reuse it unless the user explicitly asks for fresh assets.
   - Run `scripts/create_marketing_asset_package.py`.
   - Default output root: `output/marketing-assets/` under the current repo.
   - For cross-repo or non-repo work, use `/Users/preston/Marketing Assets/Bonfire/` unless the user names another folder.
   - Include any screenshot paths with `--screenshot`.

4. Generate persona copy.
   - Keep headlines short, specific, and value-led.
   - Use subtitles only when they clarify the value.
   - Avoid internal route names, table names, implementation jargon, or unverified live claims.
   - Write for each persona's job-to-be-done, not just the feature mechanic.

5. Generate or prepare images.
   - By default, generate one local Bonfire-branded PNG image per selected persona and requested size into `generated-assets/`.
   - The package script renders local promotional PNGs even when no external image-generation provider is available.
   - Use prompt-only rows only when generation is intentionally deferred, blocked, unsafe, or explicitly requested. In that case pass `--asset-status planned --no-generate-images` and explain why.
   - If an external image-generation tool is available and the user wants richer generated art, generate or replace the local PNGs and keep the prompt files in `prompts/`.
   - When screenshots are included, use them as grounded UI references. Do not invent realistic UI states that could misrepresent the product.
   - Use Bonfire assets from `assets/bonfire-inline-full-color.svg` and `assets/bonfire-mark-full-color.svg` when compositing or prompting.

6. Update manifests.
   - Keep `asset-manifest.json` machine-readable.
   - Keep `asset-manifest.md` human-readable with persona, headline, subtitle, image/status, and saved path or link.
   - Add asset reuse notes when an existing image or screenshot can be reused.
   - Use `--asset-status failed` or `--asset-status blocked` with `--status-note` when image generation fails or is intentionally deferred.
   - Use `--reuse-asset "Persona:size:/path/to/asset.png"` when a row should point at an existing reusable image.

7. Integrate with launch workflows.
   - Feature Finish Line: call this after tests/docs/rollout status are known and before final marketing handoff.
   - Release notes: call this after live status is classified so public-facing assets do not overclaim.
   - Marketing video packages: use this for static persona images and prompts; use `bonfire-marketing-video-package` for full video packages.

## Script Usage

```bash
python3 /Users/preston/.codex/skills/marketing-asset-generation/scripts/create_marketing_asset_package.py \
  --feature-name "Agent Font Size Options" \
  --description "Admins can choose Standard or Large text for installed agent experiences." \
  --persona "Communications pastor/director" \
  --persona "Technical buyer" \
  --size square \
  --size landscape \
  --include-screenshot \
  --screenshot /absolute/path/to/screenshot.png
```

Useful status/reuse options:

```bash
--asset-status failed --status-note "Image provider unavailable"
--asset-status planned --no-generate-images --status-note "Waiting for approved screenshot"
--reuse-asset "Technical buyer:square:/absolute/path/to/existing.png"
```

The script prints the package path and writes:

- `creative-brief.md`
- `copy-matrix.md`
- `asset-manifest.json`
- `asset-manifest.md`
- `backlog.md`
- `prompts/*.md`
- `raw-screenshots/`
- `generated-assets/*.png` unless generation was intentionally deferred
- `exports/`

Same-day reruns create a suffixed package folder instead of overwriting the existing package.

Find an existing package:

```bash
python3 /Users/preston/.codex/skills/marketing-asset-generation/scripts/find_marketing_asset_package.py \
  --feature-name "Agent Font Size Options"
```

The finder exits `0` when it finds a matching `asset-manifest.json` and exits `1` when none exists. Use the JSON output to decide whether to reuse assets or run package creation.

## Output Requirements

Every run should return:

- Package path.
- Persona rows with headline and subtitle.
- Image status: generated, planned, reused, failed, or blocked.
- Saved file path or link for every generated/reused asset.
- Confirmation that generated assets exist on disk, or the reason generation was intentionally deferred.
- Backlog items with reason for anything intentionally not done.
- Any claims that must not be used publicly yet.

## QA Checklist

Cover these cases in the workflow or package notes:

- No personas selected.
- One persona selected.
- Many personas selected.
- Long feature description.
- Include screenshot.
- No screenshot.
- Asset generation failure.
- Asset reuse.

## Quality Bar

- Use Bonfire branding and a clean, warm, product-forward look.
- Prefer real screenshots or honest abstract feature visuals over fake UI.
- Keep text short enough to work in square, landscape, and story layouts.
- Produce assets that are reusable later, not just chat output.
- Separate generated files, prompts, raw screenshots, and exports.
- Do not overwrite existing package assets without checking first.
