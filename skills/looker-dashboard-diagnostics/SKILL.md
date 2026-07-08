---
name: looker-dashboard-diagnostics
description: Inspect Looker dashboards for BI migration diagnostics, especially when migrating Looker dashboards backed by dbt/Snowflake/Fivetran into Microsoft Fabric. Use when asked to connect to Looker, inventory dashboards/tiles/filters, identify which data a dashboard component uses, extract generated SQL, map Looker Explores/fields to warehouse objects, or compare Looker reporting logic with Fabric semantic models.
---

# Looker Dashboard Diagnostics

## Core Approach

Prefer the Looker API over browser replay for repeatable diagnostics. Use the UI only when credentials are unavailable, visual layout matters, or the user needs to demonstrate a one-off interaction.

For migration work, keep these outputs separate:

- dashboard inventory: title, id, folder, filters, tile names, visualization types
- tile query metadata: model, Explore/view, fields, filters, pivots, sorts, limits
- generated SQL: SQL returned by Looker for the saved tile query
- migration notes: source warehouse tables, dbt model candidates, Fabric semantic model/table mapping

Do not paste Looker API secrets into chat. Ask the user to place credentials in the shell environment, a local `.env`, or a `.looker.ini` file.

## API Diagnostics

Use `scripts/extract_dashboard.py` when a dashboard id or Looker dashboard URL is available.

Expected environment:

```bash
export LOOKERSDK_BASE_URL="https://example.cloud.looker.com"
export LOOKERSDK_CLIENT_ID="..."
export LOOKERSDK_CLIENT_SECRET="..."
```

Run:

```bash
python3 /Users/preston/.codex/skills/looker-dashboard-diagnostics/scripts/extract_dashboard.py \
  --dashboard 254 \
  --output /tmp/looker-dashboard-254.json
```

The script:

1. Logs in with the Looker API.
2. Fetches dashboard metadata and dashboard elements.
3. Finds each tile query id where available.
4. Calls Looker's `run query` endpoint with `sql` result format to retrieve generated SQL.
5. Writes a JSON artifact that can be searched, mapped to dbt models, and compared with Fabric semantic model metadata.

If the script reports `missing_query_id`, inspect the returned element metadata. LookML dashboards and some merged/result-maker tiles may expose query details differently than user-defined dashboard tiles.

## Browser Fallback

Use the browser path when API access is not ready or a tile needs visual confirmation:

1. Open the Looker instance and authenticate.
2. Open the dashboard URL or dashboard id.
3. Use dashboard actions to enter edit mode.
4. For the target component/tile, choose the tile edit control.
5. Open the Data panel to see selected fields and result data.
6. Open the SQL tab to inspect generated SQL.
7. Capture: dashboard id, dashboard title, filter values in the URL/header, tile title, fields, generated SQL, and any table names visible in the SQL.
8. Cancel/exit edit mode unless the user explicitly asked to save a dashboard change.

The recorded example followed this path on a Looker dashboard named `Net Promoter Score Responses`, entered edit mode, opened a tile edit view, selected the SQL tab, and saw generated SQL referencing `CORE.SALESFORCE_NPS_RESPONSES`.

## Migration Analysis

After extracting dashboard JSON:

1. Summarize dashboard filters and URL filter defaults.
2. Group tiles by Looker model, Explore/view, and warehouse table names found in generated SQL.
3. Flag custom table calculations, pivots, merged results, text tiles, and tiles without query ids.
4. Map warehouse objects to dbt models or Fabric lakehouse/warehouse tables where local metadata exists.
5. Produce a migration checklist: source objects, measures/dimensions, filters, visual type, SQL availability, risks, and Fabric target recommendation.

For Fabric-specific work in `/Users/preston/Code/fabric_ai`, compare extracted Looker metadata against:

- `metadata/semantic-model-metadata.config.json`
- `sql/semantic_model_metadata_schema.sql`
- `tools/fabric_semantic_metadata.py`
- `semantic_models/`

Keep "Looker API inventory succeeded", "generated SQL extracted", and "Fabric mapping verified" as separate proof claims.
