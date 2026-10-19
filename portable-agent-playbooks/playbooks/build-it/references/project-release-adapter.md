# Project release adapter

The public archive excludes live project deployment registries and account maps.
Before a build reaches release, load the project-owned release/deploy workflow.

Require an exact repository, release ref, environment, provider project/account,
trigger, build configuration, migration sequencing, verification and rollback path.
Verify these against current provider and repository state. Respect the current
request’s release limits and separately required permission or spending authority.

If project-specific `project-deploy-paths`, `deploy`, or provider safety skills are
installed, use them together with the project’s documented route. Otherwise use
an equivalent project-owned procedure. Do not guess an environment or create a
live mapping from placeholders. Missing authority or configuration blocks release;
retain local proof and report the precise missing requirement.
