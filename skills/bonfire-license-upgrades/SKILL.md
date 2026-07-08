---
name: bonfire-license-upgrades
description: Use when Codex needs to inspect, explain, or change Bonfire organization license tiers, especially when the user says to upgrade/downgrade an org, move a customer to a paid tier, audit tier limits, or compare church/business pricing ladders in Bonfire/Bonfire_AI.
---

# Bonfire License Upgrades

Use this skill for Bonfire license entitlement work across `/Users/preston/Code/bonfire` and `/Users/preston/Code/Bonfire_AI`.

## Core Rule

When the user says "upgrade them" or "move them up", keep the organization in its current product ladder unless the user explicitly asks to switch ladders.

- Church ladder: `Free` -> `Start` -> `Connect` -> `Engage` -> `Scale`
- Business ladder: `Free` -> `Starter` -> `Pro` -> `Growth` -> `Scale`
- `Free` and `Scale` are shared endpoints; infer the paid ladder from the current paid tier, org type/category, or user wording.
- Do not treat `Start` -> `Starter` as the next upgrade. `Start` is church; `Starter` is business.

For churches/ministry orgs, the next tier after `Start` is `Connect`.

## Guardrails

- Confirm the target org and current active core license from the live cloud Supabase/Postgres DB before writing.
- Never use local Supabase or local Postgres for this repo.
- Treat `organization_license` changes as app entitlement changes only. They do not create or update a Stripe subscription unless a Stripe tool/API action is explicitly performed.
- If the user asks for billing/Stripe changes, verify the Stripe customer/subscription separately before mutation.
- Do not change permissions, grants, ownership, roles, or RLS.
- Prefer a transaction that deactivates the old active core row and inserts a new active core row, preserving history.

## Verification Queries

Use the configured cloud DB from `.env` in the relevant repo. Verify the DSN points to Supabase cloud before mutation.

Find the current core license:

```sql
select
  ol.id,
  ol.org_id,
  ol.license_id,
  l.name as license_name,
  l.license_type::text as license_type,
  ol.is_active,
  ol.start_date,
  ol.end_date,
  ol.stripe_subscription_id,
  ol.stripe_subscription_status
from public.organization_license ol
join public.license l on l.id = ol.license_id
where ol.org_id = $1
  and l.license_type = 'core'
order by ol.created_at desc;
```

Show the tier ladder from the live catalog:

```sql
select
  id,
  name,
  license_type::text as license_type,
  max_interactions,
  max_content,
  max_agents,
  max_owned_knowledge_bases,
  max_subscribed_knowledge_bases,
  stripe_product_id,
  stripe_price_id
from public.license
where license_type = 'core'
order by
  case when name = 'Free' then 0 else 1 end,
  case when max_interactions < 0 then 999999999 else max_interactions end,
  name;
```

Verify the effective active core row after a change:

```sql
select
  ol.id as organization_license_id,
  l.name as license_name,
  l.license_type::text as license_type,
  ol.is_active,
  ol.start_date,
  ol.end_date,
  coalesce(ol.override_max_interactions, l.max_interactions)::int as max_interactions,
  coalesce(ol.override_max_content, l.max_content)::int as max_content,
  coalesce(ol.override_max_agents, l.max_agents)::int as max_agents,
  coalesce(ol.override_max_owned_knowledge_bases, l.max_owned_knowledge_bases)::int as max_owned_knowledge_bases,
  coalesce(ol.override_max_subscribed_knowledge_bases, l.max_subscribed_knowledge_bases)::int as max_subscribed_knowledge_bases
from public.organization_license ol
join public.license l on l.id = ol.license_id
where ol.org_id = $1
  and l.license_type = 'core'
  and ol.is_active = true
  and (ol.start_date is null or ol.start_date <= now())
  and (ol.end_date is null or ol.end_date >= now())
order by coalesce(ol.start_date, ol.created_at) desc, ol.created_at desc
limit 1;
```

## Mutation Pattern

After confirming the intended target license ID, use a single transaction:

1. Deactivate active core `organization_license` rows for the org:
   - `is_active = false`
   - `end_date = coalesce(end_date, now())`
   - `updated_at = now()`
2. Insert a new `organization_license` row:
   - `org_id = target org`
   - `license_id = target core license`
   - `start_date = now()`
   - `end_date = null`
   - `is_active = true`
   - Stripe fields null unless a real Stripe subscription was verified and intentionally linked.
3. Re-query the effective active core row and report the resulting limits.

## Reporting

Always state:

- Previous tier and new tier.
- Effective interaction/content/agent/owned-KB/subscribed-KB limits.
- Whether Stripe billing was changed. If only `organization_license` changed, say it was app entitlement only.
