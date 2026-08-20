# SGS Refined Proposal Template

The Dry Ground proposal establishes the default layout for client-facing strategic retainer proposals. Reuse the shared `strategic-retainer` proposal kind with `theme: "refined"` before creating a new page shape.

## Page rhythm

1. **Cover**
   - Client and engagement label
   - One clear proposal title
   - Short outcome-focused summary
   - Four to five cover facts, with the recommended starting point visible
2. **Personal note**
   - One short, client-specific paragraph
   - Keep the conversational context here, not in the formal overview
3. **Overview**
   - One concise paragraph describing the engagement and ownership model
4. **Immediate value**
   - Make the first practical wins the most prominent section after the overview
   - Use four icon-led cards whenever possible
   - Each card should have a specific outcome title and one short explanation
5. **Why start here**
   - Two or three short rationale blocks
   - Explain why the first sequence is practical and appropriately paced
6. **Monthly options**
   - Present three clear tiers
   - Show hours, monthly fee, and best fit
   - Mark one recommended tier
   - Do not show effective hourly rates in the client-facing cards
7. **First six months**
   - Use three phases with time range, phase title, and one-sentence focus
8. **What we can build around**
   - Use the icon grid for the broader capability map
9. **Retainer coverage**
   - Keep included support as a short list of practical work categories
10. **Guardrails**
    - State client ownership, scale-down flexibility, tool continuity, and human review where relevant
11. **Recommendation and next steps**
    - Give the recommendation its own highlighted card
    - Keep next steps short and operational
12. **Closing**
    - One brief closing note and the standard proposal footer

## Content rules

- Lead with value the client can recognize immediately: visibility, speed, fewer manual steps, better decisions, or team leverage.
- Keep section introductions to one short paragraph. Move detailed action items into the proposal, not the cover email.
- Use concrete nouns and verbs. Prefer “one view across seven property managers” to “improve operational visibility.”
- Keep cards scannable: a short title, one sentence, and an icon where the shared icon set supports it.
- Price cards should communicate choice and pacing, not internal economics. Omit effective rates.
- Preserve client ownership and human-review guardrails when they are part of the offer.

## Visual system

- Use the shared refined theme rather than a one-off page shell.
- Keep the teal accent for section indices, icon cards, recommendation emphasis, and the recommended pricing tier.
- Use rounded cards, thin borders, restrained shadows, and light blue/teal background gradients.
- Use the shared discipline icons: `portfolio`, `pipeline`, `match`, `filter`, `data`, `workflow`, `people`, and `shield`.
- Keep the page generous and quiet. One idea per card is better than a dense wall of copy.

## Responsive behavior

- Desktop: two-column immediate-value cards, three pricing cards, and three-column capability grid.
- Tablet: retain the same hierarchy while allowing grids to collapse to two columns.
- Mobile: stack all cards and phases, keep headings left-aligned, reduce padding, and preserve the recommended option's visual emphasis.
- Test the full page at a narrow mobile width before sharing the proposal link.

## Implementation checklist

- Add the proposal to `app/proposals/proposal-data.ts` with `kind: "strategic-retainer"` and `theme: "refined"`.
- Keep the client context in `clients/<slug>/proposal-details.md`.
- Put the cover email in `deliverables/<slug>-cover-email.md`.
- Reuse `immediateValue`, `focusAreas`, `tiers`, `timeline`, and `recommendation` rather than adding a bespoke renderer.
- Run `npm run build`.
- Verify the exact production URL returns HTTP 200 and contains the client-specific headline before sending it.

