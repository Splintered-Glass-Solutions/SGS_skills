# Looker API Notes

Use these Looker API concepts for dashboard migration diagnostics:

- `GET /dashboards/{dashboard_id}/dashboard_elements` returns dashboard element records for a dashboard. Request fields such as `id`, `title`, `type`, `query_id`, `query`, `look`, `result_maker`, and `vis_config`.
- `GET /queries/{query_id}/run/sql` returns the generated SQL for a saved query instead of executing and returning data rows.
- `POST /queries/run/sql` can return generated SQL for an inline query body when a tile exposes full query metadata but not a reusable query id.
- Query objects identify the Looker model, Explore/view, fields, pivots, filters, sorts, limits, and dynamic fields. These are the key inputs for mapping a Looker tile to Fabric semantic model objects.
- User-defined dashboard tiles commonly expose `query_id` or `query`; LookML dashboards and some result-maker/merged-result tiles may need special handling through `result_maker`, LookML files, or UI inspection.

Primary docs:

- https://docs.cloud.google.com/looker/docs/reference/looker-api/latest
- https://docs.cloud.google.com/looker/docs/reference/looker-api/latest/methods/Dashboard/dashboard_dashboard_elements
- https://docs.cloud.google.com/looker/docs/reference/looker-api/latest/methods/Query/run_query
- https://docs.cloud.google.com/looker/docs/reference/looker-api/latest/methods/Query/run_inline_query
