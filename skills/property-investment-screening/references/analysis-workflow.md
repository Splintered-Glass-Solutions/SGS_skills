# Analysis workflow and evidence rules

This is the repeatable method behind the 121 Winding Oak buyer-side screen. Reuse the sequence and claim boundaries; rebuild the facts and assumptions for each property. The example figures and cohort thresholds below describe that one research pass and are not defaults for a new property.

## 1. Subject and evidence register

Start with an exact address plus a stable listing or parcel identifier. Capture listing status and history, current seller terms if available, bedrooms, baths, living area, year, lot, utilities, access and distinctive site conditions. Record where each fact came from. Keep conflicts in a short register instead of silently choosing one source: for example, a listing brochure may report more baths than public record, or may claim both public water and a well while capacity is unknown.

Use distinct labels throughout:

| Label | Meaning |
| --- | --- |
| Verified | Checked against an authoritative or direct source for the stated fact |
| Reported | Appears in a listing, portal, broker feed or seller statement |
| Modeled | Produced from explicit assumptions, formulas or source-code reconstruction |
| Judgment | Analyst screening choice, with a stated rationale |
| Unknown | Evidence is missing, conflicting or inaccessible |

For each cited link, note its checked date and the claim it supports. A public record lookup, portal card or map view does not establish facts it does not expose.

## 2. Value and sale context

Build two separate evidence groups:

- **Reported closed events:** date, source's close label/range, last observed ask, whether exact consideration is public, physical attributes and material differences from the subject.
- **Asking references:** current or historical asking price, status checked, property attributes and why the reference is relevant.

Do not treat last asking price as consideration. Do not infer exact sale price from a broad tax/portal/MLS display range. Explain whether each property is a close physical match, a land/creek/vintage context point or a weak reference. If the record does not support dollar adjustments, say so. Any screening band remains a buyer-side judgment, not an appraisal, broker CMA, statistical value conclusion or guaranteed negotiation result.

## 3. Short-term-rental evidence

Use a saved subject-level result only when the record is matched to the exact subject using a stable identifier and the relevant model/version, recipe, date, comp count and data window are known. Distinguish persistent database output from source-code replay and from manual cohort analysis. If the subject has no saved revenue/economics row, state that directly before showing market comps.

When deriving a comparable-listing cohort:

1. Preserve the original extract and record its source, pull date, query criteria, location method, discount assumptions and measurement window.
2. Inspect the actual fields that define distance, capacity, bedrooms, baths, reviews, rating and available days. Validate query semantics instead of trusting labels alone.
3. Apply explicit filters to the saved rows when the original query is known to be defective. Keep the unfiltered count, excluded rows, reasons and retained count so the cohort can be reproduced.
4. Calculate and show P50/P75/P90 per listing from the same metric before aggregating. State whether it is gross revenue, net revenue or another measure and how annualization was done.
5. Describe the percentiles as positions within that filtered comp set. P75 can be an upper-quartile target and P90 an upside case; neither is a subject-level forecast, confidence interval, occupancy estimate or ADR guarantee.
6. Select a small, transparent sample of the closest/highest-fit listing pages when page-level amenity or capacity evidence affects assumptions. Record accessible-page denominator and any source-field conflict. Do not convert amenity frequency into a causal revenue premium.

### Reference case recipe (not a future default)

The Winding Oak source replay returned 259 candidate rows, but known query defects affected distance, capacity and review filtering. The saved rows were manually filtered to 91 using: distance at most 5 miles, exactly 3 bedrooms, 1–4 baths, accommodates 8–10, rating at least 4.5, at least 20 reviews and at least 275 available days. Those thresholds were appropriate to that specific screen, not a universal recipe. The resulting P50/P75/P90 values were a local manual market diagnostic; the subject was absent from the searched stage and production property records, so no subject-specific Enhanced Revenue result or current hosted-app calculation was claimed.

The final report also separated the ten nearest listing-page review from the 91-row cohort. A listing page that failed to load remained in the comp table with a status caveat; amenity frequency used an accessible-page denominator when a page could not be checked. Keep these counts separate.

## 4. Underwriting paths

Write down all inputs before calculating: purchase price, revenue tier, down payment/LTV, rate, term, closing assumption, tax, insurance, utilities, maintenance, cleaning/turnovers, OTA/platform fee, management, HOA, vacancy treatment and reserves. Record which are current bills/quotes and which are model seeds. Confirm whether revenue includes cleaning-fee receipts before adding a cleaning expense, and whether a discount or vacancy adjustment is already embedded.

Calculate cash to close and debt service from the stated financing assumptions. For an amortizing fixed-rate loan, monthly principal and interest is based on principal, monthly rate and payment count; taxes, insurance, escrows and working capital are separate. Show monthly cash flow after the specified operating expenses and P&I, and identify the included revenue basis.

Where backend and frontend paths differ, preserve both complete input sets and calculate them independently. Label source path/version and whether the result is a hosted read, database output, local source reconstruction or analyst formula. Never combine backend expenses with frontend defaults into an attractive hybrid. If additional metrics such as cap rate, break-even or DSCR are calculated outside the product, show their formula and do not attribute them to the product.

Use tiers consistently: P50/base, P75/target and P90/upside when those percentiles exist. A management/no-management sensitivity can be useful, but identify the model default separately from any investor-selected sensitivity. State exclusions beside the table: setup costs, inspection, escrow/prepaids, owner use, working capital, unmodeled reserves, conditional repairs and recurring optional-amenity costs.

## 5. Capital plan without double-counting

Keep separate line groups for:

- routine guest-ready make-ready;
- conditional major-system or structural replacements;
- furnishing and equipment;
- optional revenue-positioning amenities;
- cash to close and prepaids;
- operating cash and working capital.

Provide low/base/high allowances and local source/date where available. Include one explicit contingency at the selected level and do not apply it twice. A replacement-risk table describes possible findings, not known defects; do not automatically add every row to the routine reserve. Optional packages should be tied to a capacity or positioning hypothesis and remain optional unless property evidence establishes the need. Nearby listing features are not proof of an income uplift. Reconcile potential overlap between furnishing formulas, outdoor space, landscaping and amenity work before totaling.

If you show a stacked startup subtotal, list the components and state its additive assumption, exclusions and overlap risk. It is not a firm cash requirement or vendor estimate until scopes, bids and current lender/title costs are verified.

## 6. Diligence and synthesis

Rank next evidence by what it changes: current seller terms and operating history; official parcel/title/survey/boundary/access; floodway and usable land; legal layout, permits and septic capacity; structure and system inspections; utility, well and septic service; local STR legality, tax and insurance; actual property tax and operating quotes; itemized repair/furnishing/amenity bids. Use official local sources for rules and parcel questions. Do not infer legal STR eligibility from nearby listings or from a citywide FAQ alone.

Open with the key finding, then state its basis and confidence. Keep the sale screen and operating case independent. Explain that a weak sale-comp set cannot support precise adjustments and a comp cohort cannot promise subject revenue. Put caveats with the relevant numbers, end with dated source groups and state what an inspection, title review, quote, seller record or current app run could resolve.

## 7. Linked-report checks

Use [the HTML starter](../assets/linked-report-template.html). Keep its anchor order: overview; property/price; rental evidence; underwriting; capital; diligence and sources. Replace or remove each example row, update all dates and direct source links, and ensure text remains readable at desktop and narrow widths. Check source and disclosure interactions with the browser, not from source code alone. Run a visual review at the first screen, a dense table and the final disclosure. Confirm headings, links, table labels, keyboard focus and reduced-motion styles. Do not claim comprehensive accessibility testing from screenshot evidence.

Public access is an external sharing decision. Publish only when the user requests it and confirms the report is intended for that audience. Draft any accompanying message unless sending is explicitly requested.
