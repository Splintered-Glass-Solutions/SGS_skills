---
name: bonfire-demo-prep
description: Prepare Bonfire demos for a specific customer or organization. Use when auditing Bonfire org/AI/widget setup, testing demo prompts, improving guidance or source-backed behavior, fixing app or test blockers, deploying changes to dev, running Bonfire QA/full-suite checks, and producing a verified demo agenda or talk track.
---

# Bonfire Demo Prep

## Operating Mode

Treat demo prep as build work plus QA. Gather live proof before giving the demo plan: DB/config rows, deployed app behavior, Session API/widget responses, source counts, health checks, CI/deploy status, and browser/test output.

Keep these claims separate:

- **Config-ready**: org/AI/widget guidance, sample prompts, KBs, source settings, and branding look correct.
- **Prompt-ready**: the exact demo prompts pass against the intended live surface.
- **Dev-deployed**: code or test fixes are merged to `dev` and the dev deployment is healthy.
- **Suite-green**: the relevant deterministic and hosted-browser checks passed.

Do not say a demo is ready because a prompt "sounds good" if sources, length, personalization, or the actual app path failed.

## Repo And Skill Order

Start from the relevant Bonfire repo:

- App/UI/proxy behavior: `/Users/preston/Code/bonfire`
- ETL/content/reprocessing: `/Users/preston/Code/Bonfire_ETL`
- AI/retrieval/session audits: `/Users/preston/Code/Bonfire_AI`

Use these skills when applicable:

- `bonfire-content-etl` or `bonfire-etl-validation` for content/reprocessing questions.
- `bonfire-qaqc`, `full-suite-tests`, and `codex-safe-run` for validation and safe execution.
- `bonfire-feature-release-update` only when the user asks for a release/update message.

## Workflow

1. **Classify the ask**
   - If the user asks only for an agenda, answer with the best verified agenda and identify any stale/unverified assumptions.
   - If they ask to audit/fix/verify, inspect live setup and run prompt tests before writing the agenda.
   - If they ask to deploy, use PR-to-`dev`; do not push or promote to `main` without explicit approval.

2. **Identify the demo target**
   - Resolve the organization, AI agent, widget, KBs, and intended demo URL/surface.
   - Prefer canonical IDs over names when multiple orgs or duplicate records exist.
   - Record org ID, AI ID, widget ID, and target host in the working notes.

3. **Audit setup**
   - Check org instructions, AI config, sample prompts, custom instructions, response settings, response quality, selected KB IDs, widget config, and source/citation display settings.
   - Check source/content health: source rows, processed/embedded status, manual-required rows, stale syncs, missing KB assignments, and obvious duplicate org/content issues.
   - Preserve backups before editing long instructions or config JSON.

4. **Test the exact demo path**
   - Test through the same path the user will demo when possible: widget bootstrap -> start session -> `/api/chat/message`, or dev UI/browser when the demo is dashboard-based.
   - Score each prompt with explicit criteria: required domain terms, concise length, source count, personalization, and no generic/off-brand claims.
   - Keep exact prompts stable. A prompt is only "demo-safe" after it passes live.
   - For widget demos, prefer `scripts/run-widget-demo-prompts.mjs` instead of rewriting ad hoc bootstrap/chat code.

5. **Fix the smallest reliable layer**
   - Prefer guidance/config when the answer is broadly correct but needs tone, terms, length, or demo framing.
   - Prefer reprocessing/embedding when sources are missing, stale, or unsearchable.
   - Prefer app code when saved config is not reaching the Session API, UI behavior blocks the demo, or tests reveal real product drift.
   - Add focused tests for app code changes.

6. **Deploy to dev**
   - Use a clean worktree when the main checkout is dirty.
   - Create a `codex/...` branch from `origin/dev`.
   - Commit only the intended code/test files; leave unrelated generated artifacts unstaged.
   - Push, open a PR to `dev`, wait for checks, merge, then verify Railway/dev health for the merged SHA.

7. **Run validation**
   - Run focused tests for any code touched.
   - Run the relevant Bonfire QA gates. For a high-stakes demo, run the full suite:

```bash
NEXT_PUBLIC_POSTHOG_PROJECT_TOKEN= corepack pnpm exec vitest run
corepack pnpm type-check
corepack pnpm lint:check
NEXT_PUBLIC_POSTHOG_PROJECT_TOKEN= corepack pnpm test:knowledge
NEXT_PUBLIC_POSTHOG_PROJECT_TOKEN= corepack pnpm test:db-pressure
NEXT_PUBLIC_POSTHOG_PROJECT_TOKEN= corepack pnpm test:guidance
NEXT_PUBLIC_POSTHOG_PROJECT_TOKEN= corepack pnpm test:studio
NEXT_PUBLIC_POSTHOG_PROJECT_TOKEN= corepack pnpm test:knowledge:computer
NEXT_PUBLIC_POSTHOG_PROJECT_TOKEN= corepack pnpm test:db-pressure:computer
corepack pnpm build
corepack pnpm test:computer
```

For hosted browser checks, set `PLAYWRIGHT_BASE_URL=https://dev.heybonfire.com` and `PLAYWRIGHT_SKIP_WEBSERVER=true`. Load the dev env before build/guidance/studio if local validation complains about missing Supabase or Session API env vars.

8. **Close with a demo agenda**
   - Lead with the best exact prompts, not broad categories.
   - Include "avoid this wording" notes if a looser prompt answered well but failed sources or consistency.
   - State current proof: prompt pass/fail, source counts, deploy SHA/status, and test gates.

## Prompt Readiness Criteria

Use a simple pass/fail rubric:

- The answer uses the customer's vocabulary naturally.
- The answer references the customer's framework or differentiator.
- The answer is concise enough for a live demo, usually under 1200-1700 characters unless the user asks for more.
- The answer includes sources when the demo is meant to prove groundedness.
- The answer gives an operational next step, plan, or workflow when the prompt asks for use cases.

If a prompt fails only because the wording is too generic, improve the demo prompt and sample prompts. If the intended natural wording must work, fix retrieval/guidance/code until it does.

## Widget Prompt Runner

Use `scripts/run-widget-demo-prompts.mjs` when the demo uses the public widget/chat path. It bootstraps the widget, starts a session, sends each prompt with `stream: false`, scores the answer, prints JSON, and exits nonzero when any prompt fails.

Example:

```bash
node /Users/preston/.codex/skills/bonfire-demo-prep/scripts/run-widget-demo-prompts.mjs \
  --suite /tmp/demo-prompts.json \
  --out /tmp/demo-results.json
```

Prompt-suite JSON:

```json
{
  "baseUrl": "https://dev.heybonfire.com",
  "widgetId": "widget-uuid",
  "pageUrl": "https://dev.heybonfire.com/demo-check",
  "pageTitle": "Codex demo check",
  "metadata": { "source": "codex-demo-qa" },
  "prompts": [
    {
      "key": "identity",
      "prompt": "Who are you and what does this organization do?",
      "mustInclude": ["organization-specific term"],
      "mustMatch": ["source-backed regex"],
      "minSources": 1,
      "minChars": 80,
      "maxChars": 1500
    }
  ]
}
```

Use `mustInclude` for literal terms that should appear, `mustMatch` for regular expressions, `minSources` to enforce grounding, and `maxChars` to keep the demo answer concise. Store result JSON under `/tmp` or an `output/qa/...` folder and cite the prompt keys, source counts, and failures in the closeout.

## Useful Prep Artifacts

Create only the artifacts that help the current demo decision:

- **Prompt suite JSON**: exact prompts, required terms, source threshold, and length caps.
- **Before/after config backup**: long org instructions or `ai.config` JSON before edits.
- **Demo scorecard**: prompt key, pass/fail, chars, source count, missing terms, preview.
- **Failure ledger**: failed prompt wording, failure reason, fix layer used, retest result.
- **Demo agenda**: exact prompts and talk track, with "avoid this wording" notes.
- **Validation log bundle**: paths to QA logs, PRs, deploy SHA, and health response.

Do not preserve secrets in these artifacts. Redact tokens, API keys, cookies, and passwords.

## TruCenter / Dr. Tim Yee Example

Use this as a pattern, not as a universal script.

Best verified flow:

1. `Who are you and what is TruCenter?`
2. `How can a pastor use TruCenter's 32 motivations and volunteerism grid to guide volunteer placement?`
3. `How would I use TruCenter for personalized mentoring in our church?`
4. `Give me a 30-minute discussion plan for church leaders using TruCenter.`

Key lesson: "where they are called" produced a useful answer, but the more source-anchored wording with "32 motivations" and "volunteerism grid" was the reliable live-demo prompt. When a customer framework has named concepts, put those concepts in both sample prompts and custom instructions.

Suggested talk track:

"Let's imagine a pastor wants to move from filling volunteer slots to helping people serve from their God-given design. First we'll ask what TruCenter is, then use the 32 motivations and volunteerism grid for volunteer placement, then turn that into mentoring and a leader discussion plan."

## Common Failure Modes

- Saved agent custom instructions exist in `ai.config` but are not forwarded to Session API chat.
- Good answers return zero sources because the prompt is answered from instructions rather than retrieved content.
- Demo prompts are too broad; use named customer concepts to pull source-backed content.
- App navigation/test labels drift, causing browser checks to fail even when product behavior is fine.
- Local build/pre-push hooks fail from missing env; rerun with dev env loaded before treating it as a code failure.
- The dev health endpoint can be green before the newest SHA finishes deploying; verify commit status or Railway status for the merged SHA.

## Final Response Shape

Report:

- What was fixed or changed.
- Exact demo prompts and recommended flow.
- Any prompts that failed and how they were corrected.
- Dev deploy/PR/SHA status.
- Test suite results, including skipped tests and known unrelated warnings.
- Remaining risks or things not touched.
