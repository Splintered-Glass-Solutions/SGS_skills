---
name: showme
description: Show real, feature-scoped proof that an implemented change works, then prepare reusable proof images for web, social, presentation, email, and team sharing. Use after a test or QA pass and before collapse or closeout, especially when the user asks to see highlighted screenshots for frontend work or live execution evidence for a non-frontend feature.
---

# Feature Proof

## Purpose

Show tangible evidence that the requested feature works. Treat this as a proof pass, not a second implementation pass and not a written restatement of test results.

Run this after the repository's test/QA workflow (often `$test`) and before the thread is collapsed or handed off (often `$collapse-bulk-edits-thread`). Keep the proof scoped to the feature that was just tested.

## Establish the proof boundary

Before collecting evidence, identify and record:

- The repository, worktree, branch, and current commit or working-tree state.
- The exact feature surfaces covered by the request and the files or routes that changed.
- The environment being exercised: local working tree, preview, Dev/staging, production, provider, or another named runtime.
- Whether the runtime is using the exact current worktree/commit. A source diff, a passing test, or a ready deployment alone does not prove that the exercised runtime contains the change.
- Whether authentication, tenant, account, or test-data context affects the result. Record categories and identifiers needed to reproduce the proof, but never expose secrets or personal data.

Label every claim with its actual boundary. Keep local, merged, deployed, authenticated, provider-backed, production, and customer-visible evidence separate. Do not upgrade one kind of evidence into another.

If the preceding test/QA pass is failed, incomplete, or blocked, collect useful evidence when possible but report the feature as `PARTIAL` or `INCOMPLETE`; do not call it proven.

## Choose the proof mode

Use the narrowest mode that covers the feature:

1. **Frontend or UI feature:** Exercise the rendered HTML interface in the exact available environment. Capture a real browser screenshot showing the changed surface and the resulting state. Include a second screenshot for an important interaction state when one screenshot cannot establish the behavior.
2. **Non-frontend feature:** Run the real command, API request, job, worker, integration, data query, generated artifact, or other applicable runtime path. Capture direct output or a result that demonstrates the changed behavior.
3. **Mixed feature:** Collect both UI proof and the underlying runtime proof when both are part of the acceptance criteria.

Use available browser, terminal, API, database, job, provider, or observability tools. Prefer a small, deterministic example with a clear before/after or input/result relationship.

## Frontend evidence

- Open the actual rendered feature in the current environment. Do not use a source-code screenshot, mockup, design file, or generated promotional graphic as the primary proof.
- Exercise the changed path, including the relevant filter, form, navigation, empty state, loading state, error state, or interaction.
- Save the raw screenshot, then create an annotated copy with a box, arrow, or concise callout that identifies the implemented change. Preserve the raw image unchanged.
- Make the annotation identify what the screenshot proves; do not edit away errors, alter values, or make an unproven environment appear live.
- If the feature requires auth or tenant context, record that context without including credentials or sensitive customer data.
- Re-open or inspect the saved artifact so the final handoff points to a real readable image.
- When producing collateral, treat the browser capture of the rendered HTML as the
  source of truth. Do not substitute a source-code image, mockup, or hand-redrawn
  interface for the physical screenshot.

### Branded proof presentation

When the user asks for polished, customer-facing screenshots or marketing proof,
add a presentation layer after the raw proof is captured. The presentation
layer is supplemental collateral; it never replaces the raw screenshot or the
annotated proof artifact.

- Use the exact rendered screenshot as the source image. Do not redraw the UI,
  edit values, remove errors, or let generated artwork become the feature proof.
- Read the project's active visual system from the relevant app or product
  repository when it is not already known. Discover, in order: an existing
  brand guide or design tokens, the rendered app shell, logo/wordmark assets,
  font declarations, and established color, gradient, radius, and shadow
  conventions. Prefer the real project assets over approximations.
- If the project has no identifiable brand system, use a restrained neutral
  fallback with an accessible sans-serif, high-contrast text, and no invented
  logo or unsupported brand claim. Record that fallback in the manifest.
- Write a short customer-facing title, a plain-language feature description,
  and, when useful, one sentence explaining the customer or business value.
  Keep the copy factual and tied to the visible feature.
- For an initial style review, create two or three clearly named candidates
  with meaningful composition differences, such as a white-corner vignette,
  an editorial split layout, and a clean proof-card layout. Inspect each image
  before handing it off and ask the user to select the template style.
- Once a style is selected, promote it as the named template baseline for the
  project or feature family, keep the prior candidate as a versioned reference,
  and use the same layout rules for future proof images unless a new style
  review is requested.
- When branded proof is requested and no narrower format is specified, produce
  a reusable format set from the same evidence and copy system:
  - `landscape-16x9`: 1600x900 for presentations, decks, and general web use.
  - `square`: 1080x1080 for square social posts and compact sharing.
  - `instagram-portrait`: 1080x1350 at 4:5 for Instagram feed posts. Verify
    current platform limits before a campaign export because platform specs can
    change.
  - `portrait-story`: 1080x1920 at 9:16 for phone-first stories, messages, and
    full-height portrait use.
- Keep important title, logo, and proof callouts inside a platform-safe area.
  Recompose the branded canvas for each aspect ratio; do not merely stretch one
  image across every format. Preserve the raw and annotated evidence separately
  from these presentation exports.
- Use gradients, soft shadows, and a directional vignette to improve hierarchy,
  but preserve enough contrast that the real UI and its proof callouts remain
  readable. A decorative treatment must not imply a stronger environment or
  customer-visible status than the raw evidence supports.
- Keep generated backgrounds, decorative textures, and logos separate from
  the screenshot layer. If image generation is used for exploration, label the
  result as presentation exploration and do not use it as the primary proof.

The reusable presentation contract is: **real evidence image + project theme +
feature-specific copy + explicit proof boundary**. A template may standardize
canvas size, spacing, hierarchy, vignette direction, card treatment, and
caption placement, but it must not hardcode a project's name, logo, colors,
feature labels, metrics, or environment claims.

For a chart, table, filter, or detail view, show enough surrounding UI to establish that the value belongs to the feature under test. For responsive behavior, capture only the viewport(s) relevant to the acceptance criteria, then create the requested branded format set from the inspected evidence.

## Non-frontend evidence

Collect a real result from the feature's execution boundary, such as:

- A command or script run from the exact working tree with its meaningful output.
- An API request and response showing the changed contract or behavior.
- A worker, queue, scheduled job, or integration run with its resulting status and artifact.
- A database or analytics query showing the expected derived result, using safe test or approved data.
- A generated file, report, log, metric, provider readback, or other direct runtime artifact.

Include the exact command/request/query shape, relevant input, result, timestamp, and environment in the handoff. Redact secrets and minimize personal or customer data. A static code inspection or a passing unit test may support the explanation, but it is not the real execution evidence when a runtime example is available.

If the feature is a library or other code path without a persistent service, use a real invocation from the current tree and preserve the output or generated artifact. If no safe runtime or example is available, report `INCOMPLETE — PROOF BLOCKED` and state precisely what is missing.

## Artifact handling

Use the repository's existing QA/evidence convention when one exists. For
durable feature proof that will be reused in release notes, prefer this
project-local convention:

```text
<repo>/output/showme/<feature-slug>/
  manifest.md
  raw/                  # immutable screenshots or runtime evidence
  annotated/            # proof callouts, when needed
  branded/              # customer-facing presentation candidates
  branded/release-ready/ # optional promoted assets after style selection
  shared/               # optional delivery receipts or links, never the only copy
```

If the repository has no suitable output directory, use a clearly named
temporary or ignored evidence location, such as `showme/<timestamp>/`, and
record the path in the handoff. Keep:

- `raw/` evidence unchanged where annotation is needed.
- `annotated/` screenshots or callouts for human review.
- `branded/` presentation treatments separate from proof evidence.
- Use explicit format names in filenames, such as
  `<feature-slug>__instagram-portrait__candidate-a.png` and
  `<feature-slug>__landscape-16x9__release-ready.png`.
- A short `manifest.md` listing the title, customer-facing description, value
  statement, source environment, artifact provenance, candidate styles, output
  formats, and whether an asset is the selected template baseline or
  release-ready.

### Project sharing and Google Drive delivery

After local artifacts are inspected, check the configured project-to-Google
Drive mapping before offering team-share delivery. The mapping is external to
this general skill and may be maintained in Codex project configuration; do not
hardcode folder IDs or infer a destination from a project name.

- Keep the repository copy as the canonical evidence and release-note source.
- When an approved project mapping and an available Drive connector exist,
  copy the selected or `release-ready` branded assets to that project's mapped
  shared folder. Preserve the same format set there.
- Use the mapped destination for the current project only when that mapping is
  explicitly configured. Never guess or upload to a similarly named folder.
- Record the project key, mapped folder name or link, copied asset names,
  delivery timestamp, and connector result in `manifest.md` or a small file in
  `shared/`. Do not store credentials or private tokens.
- If the mapping or connector is unavailable, keep the local artifacts, mark
  Drive delivery as `NOT CONFIGURED` or `BLOCKED`, and report the exact missing
  configuration. Do not claim the team folder received the files.
- Treat Drive upload as a separate external-delivery action. Perform it only
  when the user has authorized sharing for the current task or the configured
  workflow explicitly grants that authority.

If a release-note workflow exists, its skill should inspect this manifest and
use only assets explicitly marked `release-ready` (or the project's documented
equivalent) or placed under `branded/release-ready/`. Candidate images are
queued for selection, not final approved collateral. If no release-note
workflow exists, retain the same status distinction for handoff and customer
communications.

Do not delete existing user artifacts or clean unrelated working-tree changes. Do not commit, merge, push, deploy, send customer communications, mutate production/provider data, or collapse the thread unless the user separately authorizes that action.

## Completion report

Return a compact, evidence-first report:

```text
Status: PROVEN | PARTIAL | INCOMPLETE — PROOF BLOCKED
Feature: <feature name>
Scope: <repo/worktree/branch/commit or working-tree state>
Environment: <exact environment and runtime provenance>

Evidence:
- <clickable artifact>: <what it proves>
- <clickable artifact>: <what it proves>

Branded presentation candidates:
- <clickable artifact>: <style and customer-facing use>
- <clickable artifact>: <style and customer-facing use>

Delivery formats:
- <clickable artifact>: <landscape, square, Instagram portrait, or story portrait>

Team sharing:
- <mapped Drive folder/link and copied assets, or NOT CONFIGURED/BLOCKED>

Proof boundary: <local/current environment/preview/Dev/staging/production/provider/customer-visible>
Test relationship: <preceding test/QA result and any remaining failures>
Remaining uncertainty or blocker: <none, or exact limitation>
Next safe action: <usually hand off to collapse/closeout; deployment or merge is not implied>
```

Use `PROVEN` only when the relevant feature surface has a real, readable primary artifact and the exercised runtime's provenance is known. Use `PARTIAL` when only some surfaces or environments are proven. Use `INCOMPLETE — PROOF BLOCKED` when the requested evidence cannot be collected, the runtime cannot be tied to the change, or the result is only inferred from source/tests.
