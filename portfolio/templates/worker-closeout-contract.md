# Worker Closeout Contract

Workers must return this exact shape:

```text
STATUS: done | blocked | needs_approval | no_new_signal
OBJECTIVE:
WHAT_CHANGED_OR_FOUND:
PROOF:
FILES_OR_LINKS:
VALIDATION:
RISKS_OR_UNCERTAINTY:
NEXT_RECOMMENDED_ACTION:
HANDOFF_RECEIPT:
  handoff_target:
  state_to_continue_from:
  files_touched_or_read:
  next_safe_prompt:
  blocked_by:
USER_DECISION_NEEDED:
ACTION_PROPOSAL:
  target:
  action:
  risk:
  proof_ready:
  approval_needed:
  rollback_or_undo:
APPROVAL_LEDGER_UPDATE:
WORK_LEDGER_UPDATE:
STANDARDS_APPLIED:
MEMORY_OR_CHECKPOINT_UPDATED:
```

Rules:

- Include exact file paths, PRs, URLs, command outputs, screenshots, log paths,
  DB row IDs, or artifact paths when they support the claim.
- Do not flatten local, hosted/browser, dev-live, and production-live proof.
- If blocked, name the smallest missing input or approval.
- Always include `HANDOFF_RECEIPT` so another project agent or worker can
  continue without reconstructing context from chat history:
  - `handoff_target`: persistent project thread, bounded worker, the user, or
    no handoff.
  - `state_to_continue_from`: the exact state, checkpoint, branch, artifact, or
    last verified fact the next agent should start from.
  - `files_touched_or_read`: compact list of paths, URLs, reports, or commands
    that matter for continuation. Include files read even when no files were
    changed.
  - `next_safe_prompt`: the smallest safe prompt to hand to the next agent,
    including authority limits and validation expectation.
  - `blocked_by`: empty when unblocked; otherwise name the exact missing
    approval, credential, repo state, source access, product decision, or
    validation failure.
- If the user approval is needed, include a proposed approval ledger update with
  project, requested decision, why the user is needed, approval unlocks, and safe
  fallback while waiting.
- If the work was picked up, delegated, blocked, waiting, completed, resumed,
  superseded, cancelled, or checked with no new signal, include the exact JSON
  object that should be appended to
  `$CODEX_HOME/portfolio/work-ledger.jsonl`.
- Name the standards applied from
  `$CODEX_HOME/portfolio/standards-registry.md`, especially any proof,
  approval, automation, frontend, code/test, or project-specific standard that
  affected the closeout.
- If the next recommended action is gated, include `ACTION_PROPOSAL`. The
  proposal must be specific enough for the user to approve or reject without
  reopening the full run: target, action, risk, proof_ready, approval_needed,
  and rollback_or_undo.
- If no new signal, include the source range checked and checkpoint result.
