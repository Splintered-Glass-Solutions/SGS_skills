# Release Update Template

Use this template as a checklist. Adapt wording to the feature and destination.

Default run: send the shared team update to the Bonfire group text and exact `pd-bonfire` ClickUp destination, and publish the production update log only when production-live proof exists. If Preston explicitly asks for draft-only, show the drafts without delivery.

## Feature Release Summary

Title:

Feature:

Live Status:

Environment proof:

What changed:

Why we built it:

User story:

Impact:

API implications:

Frontend implications:

ETL/data implications:

Billing/auth/security implications:

Customer talking points:

Marketing uses:

Marketing asset package:

Screenshots:

Persona-specific marketing images:

Suggested social copy:

Customer-facing announcement copy:

Internal support/sales notes:

Validation:

Open caveats:

## Marketing Assets

Use this section in the release notes package. Reuse existing marketing assets when available; generate missing assets with `marketing-asset-generation`.

Asset package path/link:

Asset package status: reused / generated / missing / failed / blocked

Screenshots:

- [screenshot title] - [path/link] - [usage note]

Persona-specific images:

| Persona | Headline | Subtitle | Status | Path/Link |
| --- | --- | --- | --- | --- |
| [persona] | [headline] | [subtitle] | [generated/reused/planned/failed/blocked] | [path/link] |

Suggested social graphics:

- [asset/path] - [recommended channel] - [caption]

Suggested social copy:

- [short post]

Customer-facing announcement copy:

[Plain-language announcement safe for customers. Include live-status caveat if not production-live.]

Internal notes for support/sales:

- [what to say]
- [what not to claim yet]
- [known limitations or QA caveats]

## Shared Team Update Copy

Use this same concise copy for the Bonfire group text and ClickUp by default. Mention:

- title as the first plain-text line, with no emoji
- what shipped or was finished
- whether it is live in local, dev, production, or not verified
- why it matters
- one team/customer talking point
- marketing impact or customer-facing positioning
- deployment caveat, if not production-live

Suggested format:

Bonfire Feature Update: [Feature Title]

🚦 Status:

🔥 What changed:

💡 Why it matters:

🧩 Impact:

📣 Marketing impact:

✅ Validation:

⚠️ Still needed:

## Optional Longer ClickUp Version

Only use this if Preston asks for more detail than the shared team update.

Post title:

🔥 **Feature**

🚦 **Live Status**

💡 **Why It Matters**

👥 **Customer Story**

🔥 **What Changed**

🧩 **API / Frontend / ETL Impact**

🗣️ **What The Team Should Say**

📣 **Marketing Angle**

🖼️ **Marketing Collateral**

- Asset package:
- Persona images:
- Screenshots:
- Suggested social copy:
- Customer-facing announcement:
- Support/sales notes:

✅ **Validation / Environment Proof**

⚠️ **Caveats / Next Steps**

## Production Update Log Draft

Keep this formal by default. Do not use emojis unless Preston asks for them in the release log.

Title:

Live Status:

Summary:

Details:

- customer-facing change
- operational/team impact
- integration/API/data impact, if any
- support or onboarding note
- public-safe marketing asset or screenshot link, if production-live and approved

Status caveat:

## Delivery Report

Title used:

Bonfire group text:

ClickUp `pd-bonfire`:

Production update log:

Marketing asset package:

Marketing assets included:

Skipped destinations:

Live-status proof:
