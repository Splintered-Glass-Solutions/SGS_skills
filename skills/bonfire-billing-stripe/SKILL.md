---
name: bonfire-billing-stripe
description: Work on Bonfire billing, Stripe checkout, Stripe webhooks, license enforcement, pricing catalog, add-ons, AI credit usage, billing reconciliation, or files under src/features/billing, src/services/billing-service.ts, src/app/api/stripe, src/actions/billing-actions.ts, docs/billing-reconcile.md, or billing-related Supabase migrations.
---

# Bonfire Billing + Stripe

Use this skill for Bonfire billing and Stripe work in `/Users/preston/Code/bonfire`.

## Source Areas

- Billing feature code: `src/features/billing/**`
- Service wrapper: `src/services/billing-service.ts`
- Stripe route: `src/app/api/stripe/webhook/route.ts`
- Billing actions: `src/actions/billing-actions.ts`
- Stripe client: `src/lib/stripe/client.ts`
- Billing docs: `docs/billing-reconcile.md`
- Pricing and license migrations: `supabase/migrations/*license*`, `*stripe*`, `*pricing*`, `*ai_credit*`

## Safety Rules

- Do not create, update, cancel, or refund real production Stripe objects unless the user explicitly asks and the target account/object is clear.
- Do not modify real paid production subscriptions during QA without explicit approval.
- Stripe webhooks must verify signatures before parsing fulfillment behavior.
- Webhook fulfillment must be idempotent. Check `stripe_processed_events` and existing service patterns before changing event handling.
- License changes must keep plan limits, add-ons, and widget access in sync.
- Use service-role Supabase only in trusted server-side billing paths.

## Workflow

1. Classify the change: checkout, webhook fulfillment, license sync, plan presentation, add-on limits, widget access, AI credits, or reconciliation.
2. Read the closest service and repository tests before editing.
3. For webhook changes, inspect both `src/app/api/stripe/webhook/route.ts` and `src/features/billing/services/billing-service.ts`.
4. For license or pricing changes, inspect recent migrations and `docs/billing-reconcile.md`.
5. For UI plan changes, keep `src/features/billing/lib/plan-presentation.ts` and billing components aligned.
6. For widget entitlement changes, inspect `src/features/billing/server/widget-access.ts`.

## Focused Checks

```bash
NEXT_PUBLIC_POSTHOG_PROJECT_TOKEN= corepack pnpm exec vitest run src/features/billing src/services/billing-service.test.ts src/actions/billing-actions.ts src/app/api/stripe
corepack pnpm type-check
```

If migrations changed, also follow `bonfire-supabase-rls`.

## Handoff Notes

State whether the change affects:

- Stripe checkout.
- Webhook event handling.
- License limits or add-ons.
- Widget entitlement.
- AI credit usage.
- Production billing data.
