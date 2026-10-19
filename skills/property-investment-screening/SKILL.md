---
name: property-investment-screening
description: Screen a property purchase using sale evidence, short-term-rental comps, underwriting and startup costs, then prepare a source-linked decision brief or public report. Use for vacation-rental and similar property investment reviews; do not treat the screen as an appraisal or purchase recommendation.
---

# Property Investment Screening

Create an evidence-led, buyer-side screen for a specific property. Keep reported facts, modeled assumptions, analyst judgment and unknowns visibly separate. The goal is to show what the available evidence supports and what must be verified next, not to manufacture a precise value or return.

For the reusable analysis method, read [the analysis workflow](references/analysis-workflow.md). For a linked, responsive HTML report, start from [the report template](assets/linked-report-template.html). Replace every `{{TOKEN}}`, remove unused example rows, and check that no template token remains before publishing.

## Workflow

1. **Establish the subject.** Record the property address and stable identifier, review date, listing status, source of terms, quoted price, bed/bath/area/year/land, utilities and distinctive site features. Keep conflicts visible. Use “advertised,” “reported,” or “claimed” for unverified listing facts.
2. **Build a source register.** Link the exact source for each material claim and record the date checked, what it establishes, and what it does not. Prefer official parcel, tax, permit, flood and local STR sources for those questions. Public listings are evidence of marketing, not proof of title, condition, current terms or lawful use.
3. **Separate sale evidence from asking evidence.** Record closed-event dates, last ask and exact consideration as separate fields. If consideration is withheld, do not convert a last ask, MLS range or portal status into a sale price. Select comparable properties for the relevant differences, explain their limits and present any buyer-side range as a judgment unless the data supports a statistical conclusion.
4. **Measure rental evidence.** First look for a saved subject-specific revenue and economics result. Record the exact property match, model/version, recipe, comp count, data window and run date. If no valid subject result exists, label any local replay or manually filtered listing cohort as a market diagnostic; never call it the subject’s bookings, forecast or current app result. Define and disclose the cohort criteria, percentile meaning, data gaps and location method. Check a small representative set of live listing pages when amenity claims materially affect the screen; record inaccessible pages and disagreements with structured data.
5. **Underwrite separate cases.** Carry clearly named revenue tiers through the same purchase, financing and expense assumptions. Show price, down payment, rate, term, closing-cost assumption, monthly P&I, cash to close and monthly cash flow. If backend and frontend expense paths differ, calculate and label them separately; do not blend inputs. Identify model version and whether figures are source outputs or analyst reconstructions. State excluded costs and avoid double-counting cleaning, OTA fees, management, vacancy or taxes.
6. **Build a non-overlapping capital plan.** Separate routine make-ready, conditional major replacements, furnishing, optional revenue amenities, closing costs and working capital. Give low/base/high allowances with source and date, add contingency once, and call allowances estimates rather than bids. Do not imply amenity frequency proves an income premium. Flag overlap between furnishing and site/amenity scopes.
7. **Rank diligence by decision value.** Include seller terms and operating history; title, legal description, survey, boundaries, easements and access; parcel-specific flood and usable land; permitted layout and septic/service capacity; condition inspections; local STR rules and tax; insurability; actual taxes, utility bills and vendor quotes; and itemized bids. Name the evidence that would resolve each uncertainty.
8. **Synthesize for a reader.** Lead with the decision-relevant conclusion and the few figures that support it. Show the valuation and operating cases separately. Use clear labels for verified, reported, modeled, judgment and unknown. Put caveats beside the claim they qualify; group direct source links near the end and include a review date and scope limitation.

## Linked report and publication

Use the HTML asset when a readable, single-page report is useful. Preserve its semantic section order, responsive tables, visible keyboard focus, native disclosures and reduced-motion support. HTML-escape inserted text, validate links as public `https:` URLs, and do not interpolate untrusted content as markup. Keep public prose concise and keep detailed methodology, source links and exclusions available in the page.

Publishing requires a user request to share, publish or deploy. Before making a report public, confirm that the user intends the named report and its property details to be public. Do not carry forward approval from another property or task. Never include credentials, private owner data, private seller communications or other non-public personal information. Creating a report does not authorize sending its link to a person; draft a message unless sending is separately requested.

Before handoff, check that:

- every material price, revenue, expense and capital figure has a stated basis;
- reported closes, asks, estimates and analyst judgments are not conflated;
- revenue tiers are described as comp distributions unless a true subject result exists;
- the two expense paths are kept separate where their inputs differ;
- all totals explain included and excluded scopes;
- every link has a useful label, tables have captions and header scopes, and all disclosures work;
- the layout reflows at narrow widths without page-level horizontal scrolling;
- keyboard focus is visible, headings form a logical outline and reduced-motion preferences are respected;
- dates are current, source links open, and no `{{TOKEN}}` placeholders remain.

Screenshots can support a visual review, but do not establish legal STR eligibility, physical condition, full WCAG conformance, realized income or investment suitability.
