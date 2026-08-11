---
name: vercel-deployment-safety
description: Enforce a fail-closed Vercel target check before any Vercel deploy, promote, rollback, relink, environment/domain edit, or Git action expected to trigger a Vercel deployment. Use whenever a task mentions Vercel, a hosted web deployment, a Vercel-linked repository, preview/staging/production promotion, or an existing deployment map.
---

# Vercel Deployment Safety

Treat project/client isolation as a hard safety boundary. Never deploy, link, promote, roll back, pull environment variables, edit Vercel settings, or push a Git ref that may trigger Vercel until the exact target is verified.

## Mandatory preflight

1. Read `references/project-registry.json`. It is the only source of approved local client/app-to-team/project mappings for this skill.
2. Require the requester to state the client, application, environment, and
   whether the action is an actual deploy or a Git push that can trigger one.
   The environment may instead come from an
   `implicit-single-environment` result produced by
   `/Users/preston/.codex/skills/deploy/scripts/resolve_environment.py`; state
   that resolved target to the requester before publishing. Do not otherwise
   infer a target from a folder, branch, URL, or project name.
3. Run the read-only verifier before any write action:

   ```bash
   python3 /Users/preston/.codex/skills/vercel-deployment-safety/scripts/verify_vercel_target.py verify \
     --client <client> --app <app> --repo <absolute-repository-path> --environment <preview|staging|production>
   ```

4. Continue only if it exits `0`, the user explicitly authorized the specific write, and the requested environment matches that authorization. A green check verifies target identity only; it is never deploy authorization.

## Hard stops

Stop and report the mismatch without attempting a workaround when the verifier fails, the app is absent from the registry, a worktree is not explicitly mapped, `.vercel/project.json` is absent/stale, the Git remote differs, or a Vercel project/team ID differs.

Never solve a failure by running `vercel link`, copying `.vercel`, changing `--scope`, accepting a membership request, or retrying against a same-named project. These are configuration or access changes and need a separately explicit approval after the target record has been updated from authoritative evidence.

Do not treat the active `vercel whoami`, a Vercel project name, a Vercel URL, or a GitHub organization as identity proof. Use immutable project and team IDs.

## Mapping maintenance

Use `scripts/verify_vercel_target.py list` to see current records. Add a client/app only after gathering authoritative evidence for the repository remote, Vercel team ID, Vercel project ID, project name, scope, and intended aliases. Mark uncertain entries as unmapped rather than guessing.

For STRIQ, also read `/Users/preston/Code/striq-shared-docs/VERCEL_DEPLOYMENT_MAP.md`; the registry carries the preflight subset and the shared document records evidence and known local-link hazards.

## Git-integration incidents

If Vercel reports an unrecognized Git committer, distinguish it from a CLI target failure. Record the repo/commit/author and Vercel project shown in the incident. Do not approve a Vercel membership request or alter Git/Vercel integration settings without authorization. The repository's Vercel integration and recognized Vercel account linkage must be corrected by an authorized owner.
