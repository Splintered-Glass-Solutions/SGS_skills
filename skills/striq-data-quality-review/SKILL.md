---
name: striq-data-quality-review
description: Review StrIQ stage-to-prod data quality, promotion health, valid-property coverage, and analytics backlog. Use when Preston asks how StrIQ data quality looks today, whether stage/prod sync is healthy, whether valid properties are missing from the app, or what ER/Economics/StriqScore/source-data items need resolution.
---

# StrIQ Data Quality Review

## Guiding Principle

Treat the hard success definition as:

> Every active, real MLS property in stage with usable MLS location data must be present in prod/the app.

Analytics completeness is secondary. Missing ER, Economics, StriqScore, price, or AI extraction should be reported as analytics/source-data backlog unless it also causes a valid stage property to be absent from prod.

Usable MLS location means the stage row has non-empty, non-`Unknown` `MLSMarket`, `CityName`, and `StateName`. Rows missing those fields are not valid app inventory until the source/location issue is fixed.

## Source Of Truth

- Stage/prod sync and promotion health code: `/Users/preston/Code/stage-migration`
- StrIQ backend analytics code and env mapping: `/Users/preston/Code/striq-backend`
- GCP project/region for production-owned jobs: `airiq-4074f`, `us-central1`
- Main jobs:
  - `striq-stage-sync-unified-listings`
  - `striq-stage-sync-enhanced-revenue`
  - `striq-stage-sync-economics`
  - `striq-stage-sync-property`
  - `striq-promotion-health-report`
  - `striq-stage-unified-property-ai-extraction`
  - `striq-stage-populate-economics-v2`
  - `striq-stage-striq-score-v2`

Use `rg` first when locating code. Do not change DB permissions, grants, ownership, or RLS. Do not mutate prod unless Preston explicitly asks for a fix, rerun, or deploy; a review should be read-only.

## Review Workflow

1. Verify the live promotion report/run context.
   - Check the latest `striq-promotion-health-report` execution logs.
   - Confirm the report says `Valid=<n> Prod=<n> Valid missing prod=0 Prod not in valid stage=0`.
   - If it still says `Qualified=...`, `Qualified missing prod`, or uses analytics-qualified language, flag that the old report semantics may be running.

2. Validate app property coverage.
   - Count valid stage properties using the valid-stage definition.
   - Count prod `property` rows.
   - Confirm `property`, `property_details`, and `property_identity` are aligned enough for app visibility.
   - Treat any non-zero `Valid missing prod` as the highest-priority failure.

3. Separate hard blockers from analytics backlog.
   - Hard blockers: missing/invalid MLS location, prod row missing for valid stage row, unintended market/admin-disabled hiding, failed property sync/swap.
   - Analytics backlog: `has_er_waiting_economics`, `has_economics_waiting_score`, `missing_er_no_terminal_reason`, `missing_price_for_er`, ER geocode/no-comp terminal outcomes.
   - Do not describe analytics backlog as "valid properties missing from prod" if coverage reconciliation is clean.

4. Check pipeline/job health.
   - Confirm daily jobs ran in the intended order.
   - Confirm `striq-stage-sync-property` and `striq-promotion-health-report` are using the expected image/job revision.
   - Confirm `ProductionVersions` is on intended analytics versions; do not leave a temporary rollback in place unless Preston explicitly wants it.

5. Report concise status.
   - Lead with coverage: `Valid stage = X, Prod = X, missing = 0`.
   - Then list source-data blockers.
   - Then list analytics backlog with top gates/markets/sources.
   - Include concrete examples only when asked or when a category needs explanation.

## Useful Commands

Run these from `/Users/preston/Code/stage-migration` unless noted.

Latest report logs:

```bash
gcloud logging read 'resource.type="cloud_run_job" AND resource.labels.job_name="striq-promotion-health-report"' \
  --project airiq-4074f \
  --limit=100 \
  --format='value(timestamp,textPayload)' \
  --freshness=24h
```

Latest report object:

```bash
gsutil ls -l gs://striq-inactive-property-reports/prod/ | sort | tail -5
```

Analyze a downloaded promotion-health CSV:

```bash
npm run report:analyze -- /tmp/promotion-health-YYYY-MM-DDTHH-MM-SS.csv
```

Verify live job images:

```bash
gcloud run jobs describe striq-stage-sync-property \
  --project airiq-4074f \
  --region us-central1 \
  --format='value(spec.template.spec.template.spec.containers[0].image)'

gcloud run jobs describe striq-promotion-health-report \
  --project airiq-4074f \
  --region us-central1 \
  --format='value(spec.template.spec.template.spec.containers[0].image)'
```

Read current production versions from stage:

```bash
node - <<'NODE'
require('dotenv').config({ path: '/Users/preston/Code/striq-backend/.env' });
const { Pool } = require('pg');
const pool = new Pool({
  user: process.env.STRIQ_STAGE_PG_USER,
  password: process.env.STRIQ_STAGE_PG_PASSWORD,
  host: process.env.STRIQ_STAGE_PG_HOST,
  database: process.env.STRIQ_STAGE_PG_DATABASE,
  port: Number(process.env.STRIQ_STAGE_PG_PORT || 5432),
  ssl: { rejectUnauthorized: false },
});
(async () => {
  const res = await pool.query(`
    SELECT "pipeline", "version", "production", "startdate"
    FROM "striqAnalytics"."ProductionVersions"
    WHERE "pipeline" IN ('EnhancedRevenue','Economics','StriqScore')
    ORDER BY "pipeline", "production" DESC, "startdate" DESC NULLS LAST, "version" DESC
  `);
  console.table(res.rows);
})().finally(() => pool.end());
NODE
```

Count prod properties:

```bash
node - <<'NODE'
require('dotenv').config({ path: '/Users/preston/Code/striq-backend/.env' });
const { Pool } = require('pg');
const prod = new Pool({
  user: process.env.STRIQ_PROD_PG_USER,
  password: process.env.STRIQ_PROD_PG_PASSWORD,
  host: process.env.STRIQ_PROD_PG_HOST,
  database: process.env.STRIQ_PROD_PG_DATABASE,
  port: Number(process.env.STRIQ_PROD_PG_PORT || 5432),
  ssl: { rejectUnauthorized: false },
});
(async () => {
  const res = await prod.query('SELECT COUNT(*)::int AS property_count FROM property');
  console.table(res.rows);
})().finally(() => prod.end());
NODE
```

## Interpretation Rules

- `Valid missing prod = 0` is the main green signal.
- `expected_pending` analytics rows are not sync failures.
- `missing_location` is a real source-data blocker because the row cannot be assigned to a usable app market.
- `missing_price_for_er` blocks ER/Economics quality, not property visibility.
- `missing_er_no_terminal_reason` means ER needs an attempt/outcome, not necessarily that the property should be absent.
- If changing a version threshold does not increase valid coverage, restore the intended production version and fix the sync/report gate instead.

## Status Template

```text
Core coverage: valid stage <X>, prod <Y>, valid missing prod <Z>, prod not in valid stage <W>.
Verdict: <green/red> for app property coverage.

Remaining blockers:
- Source/location: <count and top markets>
- Analytics backlog: <count by gate, top markets/sources>
- Runtime notes: <job/image/version observations>

Next actions:
- <only list actions that follow from the evidence>
```
