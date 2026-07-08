# Bonfire Update Channel Patterns

## Tone

Use Preston's practical operator voice. Keep it conversational, concrete, and careful about deployment boundaries.

Default stance:

- lead with the value-add, not the task list
- sound like a teammate updating teammates, not a project manager updating a tracker
- use implementation detail only when it explains risk, value, or what someone should do next
- flag local/dev/production status without turning the message into a deployment report

Avoid:

- hype
- project-management phrasing like "workstream", "deliverables", "status cadence", or "stakeholders"
- vague "we shipped" language without deploy proof
- overexplaining implementation details to the text thread
- long inventories of files, branches, tests, or repo names unless the team needs them
- saying "live", "deployed", or "production" without current evidence

## Bonfire Text Thread

Goal: quick team awareness focused on why the work matters.

Format:

- one short paragraph
- no greeting or signoff
- no Markdown if actually sending through Messages
- include the biggest value-adds plus a clear local/dev/prod caveat

Default draft pattern:

```text
Quick Bonfire update: [what this unlocks for the product/team]. The main pieces are [short feature list]. Status: [local/dev/prod truth]. [Short next step if useful].
```

Good content:

- "local/source-branch right now"
- "dev verified"
- "prod not touched"
- "needs deploy + smoke before we treat it as live"
- "docs validate cleanly"
- "this gets us closer to..."
- "the useful bit is..."

Bad content:

- "shipped" when only local
- "ready for customers" without prod verification
- raw branch clutter unless useful
- long bullet lists
- status-board language

## ClickUp `pd-bonfire`

Goal: durable project-channel update that is still easy to read.

Format:

- short opening line that explains the value-add
- bullets grouped by product outcome, not repo or task owner
- explicit `Status:` line
- explicit `Next:` line only when action remains

Default draft pattern:

```text
Bonfire update: [one sentence on what this set of work unlocks].

- [Outcome/value]: [concrete change].
- [Outcome/value]: [concrete change].
- [Outcome/value]: [concrete change].

Status: [local/dev/prod truth].
Next: [next action].
```

Use more detail here than the text thread, especially for cross-repo work:

- app/UI changes
- Bonfire_AI API/runtime changes
- Bonfire_ETL worker/runtime changes
- shared contracts/docs changes
- validation performed
- deployment gaps

Prefer:

- "This gives us..."
- "The useful part is..."
- "This should make..."
- "Still local until..."

Avoid:

- "Completed items include..."
- "Cross-functional update..."
- "The team has executed..."
- "Per the current tracker..."

## Deployment Language

Use these labels consistently:

- `local/source-branch`: code or docs exist locally, but not confirmed in remote branch.
- `pushed`: branch or commit exists remotely, but no deploy proof.
- `dev deployed`: deployment target updated and smoke evidence exists.
- `production deployed`: production target updated and smoke evidence exists.
- `not verified`: evidence is missing or stale.

If the work spans several repos, list status per repo rather than flattening it into one claim.

## Verification Snippets

Useful commands when working locally:

```bash
git status --short --branch
git log --oneline --decorate --max-count=8
git diff --stat
```

For shared docs:

```bash
PATH=/usr/local/bin:$PATH python3 scripts/validate_docs.py
git diff --check
```

## Sending Discipline

Drafting is always safe. Sending/posting requires explicit permission in the user request.

For Messages:

- resolve the Bonfire chat first
- paste/send one message, not line-by-line
- verify the outbound row or visible sent state when practical

For ClickUp:

- verify exact `pd-bonfire`
- do not use a nearby `Bonfire`, `PD`, or task comment destination unless Preston explicitly redirects
- report auth/destination blockers plainly
