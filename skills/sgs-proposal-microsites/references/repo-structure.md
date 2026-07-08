# SGS Proposal Repo Reference

## Primary Paths

- Repo root: `/Users/preston/Code/sgs_proposals`
- Shared data: `/Users/preston/Code/sgs_proposals/app/proposals/proposal-data.ts`
- Shared renderer: `/Users/preston/Code/sgs_proposals/app/proposals/proposal-page.tsx`
- Shared route: `/Users/preston/Code/sgs_proposals/app/proposals/[slug]/page.tsx`
- Shared styles: `/Users/preston/Code/sgs_proposals/app/globals.css`
- Client notes: `/Users/preston/Code/sgs_proposals/clients/<slug>/proposal-details.md`
- Deliverables: `/Users/preston/Code/sgs_proposals/deliverables`
- Repo guide: `/Users/preston/Code/sgs_proposals/AGENTS.md`

## Proposal Data Rules

- All live proposal pages come from `proposal-data.ts`.
- Prefer existing proposal kinds:
  - `website-build`
  - `strategic-retainer`
  - `hybrid-advisor`
  - `unified`
- Every proposal should include `preparedOn`.
- Use `personalNote` only for informal opening context that should sit above the formal overview.

## Deployment And Persistence

- No database is needed for the current workflow.
- Persistence comes from:
  - git history
  - deployed Vercel builds
  - retained proposal slugs in the shared data file
- Standard deployment model:
  - update content in repo
  - run `npm run build`
  - deploy the same Vercel project again
- If proposal content must become editable by non-developers later, consider adding a CMS or content store. Do not add that complexity by default.
