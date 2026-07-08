---
name: bonfire-docs-sync
description: Keep Bonfire documentation current after major app, workflow, configuration, deployment, or cross-repo changes. Use when the user asks to update Bonfire docs, sync repo docs with shared docs, refresh Bonfire org KB/user-facing articles, document deployed app behavior, reconcile README/runbooks/product KB after feature work, or ensure `/Users/preston/Code/bonfire_shared_docs` reflects current Bonfire implementation across `bonfire`, `Bonfire_AI`, and `Bonfire_ETL`.
---

# Bonfire Docs Sync

## Purpose

Use this skill to turn major Bonfire implementation changes into accurate repo-local docs, shared integration docs, and user-facing KB articles. The job is evidence-first: inspect code/config/workflows before editing docs, and flag unclear deployment or runtime state instead of filling gaps with assumptions.

## Repos

Default scope:

- `/Users/preston/Code/bonfire_shared_docs`
- `/Users/preston/Code/bonfire`
- `/Users/preston/Code/Bonfire_AI`
- `/Users/preston/Code/Bonfire_ETL`

Include other Bonfire checkouts only when the user names them or the inspected docs/code clearly reference them.

## Workflow

1. Inspect memory for Bonfire shared-docs/docs-sync guidance when available.
2. Record git status for every repo in scope. Preserve existing dirty work and do not stage, commit, push, merge, or promote unless the user explicitly asks.
3. Identify the change surface from the user prompt, current branch diffs, recent modified files, repo docs, route/config files, migrations, workflows, tests, and deployment config.
4. Compare current implementation against:
   - repo-level `README.md`, `docs/`, `docs/product-kb/`, `docs/qa/`, API docs, runbooks, and workflow docs
   - `bonfire_shared_docs/{bonfire,Bonfire_AI,Bonfire_ETL,shared,user_facing_kb}`
   - `docs_manifest.yaml`
5. Update docs in the right layer:
   - Repo-local implementation details stay in the owning repo.
   - Cross-system contracts, runtime boundaries, shared flows, and operational coupling go in `bonfire_shared_docs/shared` or the relevant system folder.
   - Customer-facing help and Bonfire org KB content go in `bonfire/docs/product-kb` and `bonfire_shared_docs/user_facing_kb`.
6. Keep edits surgical. Preserve existing document style, metadata, canonicality boundaries, and review-cycle fields. Avoid unrelated refactors or wording churn.
7. Distinguish local code, merged branch state, dev deployment, production deployment, and Bonfire org KB readiness. Verify deployed state when making deployed claims; otherwise mark it as unverified.
8. Flag unclear items separately, especially missing migrations, environment-specific rollout state, hosted workflow gaps, or feature behavior that exists in code but is not provably deployed.

## Required Checks

Run shared-doc validation whenever `bonfire_shared_docs` changes:

```bash
PATH=/usr/local/bin:$PATH python3 scripts/validate_docs.py --write-manifest
PATH=/usr/local/bin:$PATH python3 scripts/validate_docs.py
```

Run Bonfire product KB validation whenever `bonfire/docs/product-kb` or `bonfire_shared_docs/user_facing_kb` changes:

```bash
corepack pnpm product-kb:validate
```

Run additional repo-specific doc/test checks only when the touched repo exposes a relevant validator or the change is risky enough to require it. Report any validator that could not run and why.

## Output

End with a concise summary that lists:

- repos updated
- major docs changed
- validation commands and results
- unclear or unverified areas
- dirty work that pre-existed or was intentionally left untouched

Do not claim the Bonfire org KB or hosted app docs are updated unless the actual KB/deployed target was verified or updated in the current run.
