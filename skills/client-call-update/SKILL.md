---
name: client-call-update
description: Prepare an evidence-based client project update and a branded, shareable HTML report covering progress, upcoming work, client inputs, and blockers. Use before client calls or for project progress summaries; does not send communications.
---

# Client Call Update

Prepare concise client-facing prose and a standalone HTML report. Explain delivered outcomes, upcoming work, client inputs, and remaining validation. Apply this workflow to any project; discover its branding and workstreams each time.

This skill prepares a draft. It does not authorize sending email, messages, calendar invitations, or other communications.

## Gather current evidence

1. Identify the client, project, next call date, and reporting period. Use the client's timezone. Cover the agreed period or changes since the last substantive update; if neither is available, choose a reasonable period and label the assumption in the evidence record. Do not narrow a multi-week progress request to this week's activity.
2. Review the latest relevant project records: current scope, recent project notes, source-controlled work, QA or acceptance records, and client communications or meeting notes. Use the sources that exist; do not assume a project board or CRM is authoritative without checking.
3. Build a workstream inventory before summarizing. Check application features, data/export investigations, research, workflow preparation, training/adoption, access, and work led by other project team members. Reconcile it with the previous substantive update and project roadmap; do not let the latest code changes or reporting window erase older work still relevant to the project. Attribute team-led work accurately, and avoid implying every lane is an active delivery commitment.
4. Reconcile conflicting or stale records. Prefer current, direct evidence. Keep exact links or paths for material claims. If a current state cannot be verified, call it out as unverified rather than filling the gap from memory.
5. Sort work into **completed**, **in progress**, **planned**, **blocked**, and **deferred**. Do not describe a proposal, prototype, or test as a delivered client outcome.

## Keep proof and scope clear

- Distinguish local or sample-data checks, production-data checks, hosted access, live workflow acceptance, and client acceptance. State only the strongest proof actually observed.
- Separate the current phase from later opportunities. Do not imply a future idea or an adjacent client workstream is included in the active scope.
- Treat commercial terms, dates, delivery commitments, savings, ROI, or other measured outcomes as confirmed only when supported by current evidence.
- Use plain language in the client update. Translate internal project labels into outcomes; omit implementation details unless the client needs them to make a decision.
- Create local report artifacts without changing application code, shared data, access, deployments, or client systems. Preserve existing authorization boundaries.

## Standard update outline

Use this order, adjusting only when a section is genuinely not relevant:

1. **Overall status:** one short sentence on the project’s current phase and the main outcome being pursued.
2. **What has moved forward:** concrete work completed since the last update, with its proof level stated accurately.
3. **Where this fits:** the active phase, its purpose, and the next major phase or deferred scope.
4. **This week:** a small set of specific activities and expected outcomes for the stated reporting period. Label these as planned when they are not confirmed commitments.
5. **What we need from you:** each client request, the reason it matters, the best-suited owner if known, and a needed-by date only when established.
6. **Next checkpoint or risk:** the decision, dependency, or observable milestone that will determine the next step.

Keep the main update short enough to scan before a call. Prefer a few meaningful bullets over a full task log. If no work is verified as complete, say what is ready and what is waiting instead of manufacturing progress.

## Discover the project's branding

- Look first in the selected project's brand assets, public/static folders, design docs, existing report templates, stylesheets, theme tokens and components. Use targeted file searches; inspect the candidate logo and relevant styles directly.
- If local sources are insufficient, use the project's known official website or connected brand materials. Verify that the logo and colors belong to the exact client/project. Use current tools to inspect these sources; do not infer branding from the project name or borrow it from another client.
- Prefer explicit brand/design tokens over colors guessed from a screenshot. Identify the primary/accent color, header treatment, text colors, surfaces and separators; preserve readable contrast and logo proportions. Find a logo variant suitable for the header background.
- Use an existing authorized asset. Embed a local image in the report so recipients do not need local paths, authentication or a live image server. Do not invent or regenerate the client's logo. If reliable branding is unavailable, use a text wordmark and neutral accessible palette, and note the fallback to the user.
- Keep branding source paths/URLs and the reporting period in the internal evidence record. Keep project-specific logos, palettes, names and facts in that project, outside this skill.

## Create the shareable HTML report

- Use the approved layout by default: a branded header; **Project update** title; one short focus sentence; workstream rows with **Done**, **Upcoming · planned**, and **Needed from your team** columns. A subtle connected vertical spine supplies progression without implying a calendar or completion percentage. Finish with the next checkpoint and material remaining validation or later scope.
- Choose rows from the actual project. Consolidate related outcomes without dropping substantiated workstreams. Distinguish investigation completed from the underlying problem fixed. Preserve client-reported acceptance as such.
- Omit completion dates and time-window slogans from the client layout unless requested or necessary for a decision. Retain dated evidence internally. Do not invent deadlines, planned completion dates, or empty-column claims; an absent item means none identified, not proof that no work or dependency exists.
- Create a full standalone HTML document in a dated, project-owned output folder. Use semantic headings, embedded/local styles, stacked mobile rows with repeated column labels, readable typography, and print CSS. A visible Print control should call the browser's print action. Avoid internal scrolling, required network dependencies, backend calls, and editing controls.
- Use [the reusable template and renderer](references/html-report.md) when this layout fits. Customize the content and branding for the current project; preserve the user-approved design on follow-up edits. New design exploration or image mockups are needed only when requested or when the layout changes materially.
- Keep raw transcripts, private email links, local evidence paths, credentials, and implementation bookkeeping in a separate internal evidence file. Include only client-appropriate facts in the shareable report.
- Return the HTML file link and, when useful, open a local preview. A local file or localhost preview is not a publicly hosted URL. Publish only to a target authorized for this task, and send communications only with explicit authorization. State the actual sharing status.
- An inline visual may supplement the report when useful. Follow the visualization skill's fragment/output rules for that separate surface; do not substitute an inline fragment for the standalone shareable file.

## Shape client requests

- Ask for the smallest useful set of inputs that unlocks the next step.
- Make each request specific: name the artifact, decision, access, or reviewer needed and explain what it will let the team confirm.
- Do not request passwords, API keys, or secrets in email or chat. Ask for a client-approved access path instead.
- If a needed owner, deadline, sample, or decision is unknown, ask for it without inventing one.
- End with a simple next checkpoint, such as reviewing a sample together or validating an agreed workflow.

## Final check

Before returning the draft, verify:

- Dates match the stated reporting period and client timezone.
- Each completion claim has direct support and an accurate proof label.
- The active scope, later scope, this-week plan, and client asks are easy to distinguish.
- The client can tell what to do next and why.
- The HTML agrees with the prose and dated evidence, uses the correct project's branding, and introduces no unsupported claims.
- The output has no unresolved template tokens or private local paths, and remains usable without project access. Review the rendered layout when tools and task scope permit; report any unverified mobile, print, or browser behavior accurately.
- The draft is client-ready and has not been sent.
