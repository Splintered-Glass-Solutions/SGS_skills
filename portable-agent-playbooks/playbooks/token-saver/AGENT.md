# Token Saver Agent Playbook

This is a platform-neutral version of the `token-saver` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Reduce avoidable context, source, output, tool, model-call, and retry token use without weakening correctness, and measure savings across the whole job. Use for long or multi-step tasks, large files or document sets, repeated revisions, research-to-writing handoffs, expensive API workflows, context-window pressure, or when the user asks to conserve tokens, avoid usage limits, reuse an accepted result, or keep an AI task lean.

## Portability Notes

- Replace `<agent-config>` with the local configuration folder for the
  target agent platform.
- Replace `<workspace>` with the user's active project/workspace root.
- Treat slash commands and `$skill-name` references as invocation hints.
  If the target platform does not support slash commands, paste this
  playbook into the agent's custom instructions or project memory.
- Keep all original safety gates. Do not send messages, deploy, mutate
  production data, change permissions, or perform irreversible actions
  without explicit approval from the user.
- If a referenced connector or tool is not available in the target platform,
  stop and report the missing capability instead of simulating external
  actions.

## Instructions

# Token Saver

Complete the task with the smallest context that preserves correctness, evidence, and the user's intent. Optimize automatically; do not make the user manage token hygiene. Loading this skill has a context cost, so earn it by preventing larger source loads, tool catalogs, outputs, retries, or later context reloads.

Cut in this order: old material carried forward, new material loaded, output/tool/retry material added afterward, then the price of irreducible repetition. Caching changes price or latency, not token volume.

## Operating Rules

1. Preserve correctness first. Never omit required evidence, validation, security context, or user constraints merely to reduce tokens.
2. Reuse before re-creating. Search for accepted answers, durable artifacts, prior decisions, and exact identifiers before repeating research or computation. Return an accepted answer unchanged only when the request and relevant source fingerprints match exactly and a person explicitly accepted it.
3. Search before opening. Use filenames, metadata, indexes, `rg`, targeted queries, or table-of-contents scans before reading large sources.
4. Read the smallest useful slice. Load matching passages, relevant line ranges, selected records, or necessary pages instead of entire files or collections. If the first packet is insufficient, add one more bounded passage; do not jump straight to loading everything.
5. Prefer the lightest faithful source form. Use text or Markdown when layout is irrelevant; use images, PDFs, audio, or full documents only when their native form matters.
6. Execute exact mechanical work with deterministic tools or code when that is cheaper and more reliable than asking a model to reason through every item.
7. Keep only useful state. Carry forward the accepted artifact, confirmed decisions, proof, open questions, and the requested delta—not rejected drafts, stale tool output, or the full argument that produced the result.
8. Match the requested output. If the user specifies a format or length, honor it. Otherwise, return the shortest answer that fully resolves the task.
9. Avoid blind retries. After a failure, inspect the error and change the hypothesis, input, provider, command, or approach before retrying.
10. Use only tools relevant to the job. Prefer deferred tool loading or targeted tool search when supported; do not broadly discover, connect, or call unrelated tools. Do not claim this unloads definitions already supplied by the platform.
11. Count the whole job. Include planning, selection, model calls, checks, repairs, and human repair when comparing paths. A cheaper model or cached prompt is not a token saving by itself.

## Workflow

### 1. Set the task boundary

- Identify the current objective and required deliverable.
- Batch questions only when they share the same source or background. Keep unrelated jobs separate.
- Infer an output contract from the request: format, length, audience, and proof level.
- Ask a question only when a missing choice would materially change the result.
- When the objective changes, recommend or create a clean task only if the current platform and user authority allow it. Otherwise, write a compact handoff and continue from that artifact.

### 2. Build a narrow context packet

Use this order:

1. Search durable memory, accepted artifacts, indexes, and local metadata.
2. Search source contents for task-specific terms.
3. Inspect only the strongest matches. For large text trees, use `scripts/select_context.py` rather than opening every candidate.
4. Expand with one additional bounded slice when the first packet is insufficient.
5. Open a full source only when structure, completeness, or cross-document reasoning requires it.

Example bounded selection:

```bash
python3 /absolute/path/to/token-saver/scripts/select_context.py \
  --request-file /tmp/request.txt --root /absolute/path/to/project \
  --max-packet-bytes 12000 --output /tmp/context-packet.md \
  --report /tmp/context-report.json
```

If the report shows omitted matches and the answer is missing, run a narrower second selection. Do not substitute the project root with a broader directory merely to get more matches.

For a large source packet, keep:

- the user's constraints;
- exact source locations or links;
- selected evidence;
- accepted decisions;
- unresolved uncertainty.

Drop:

- duplicate excerpts;
- rejected paths that no longer affect the decision;
- verbose tool logs after extracting the useful error or proof;
- drafts superseded by an accepted version.

### 3. Choose the cheapest reliable execution path

- Use shell search, structured queries, parsers, formulas, formatters, or scripts for exact filtering, counting, extraction, conversion, comparison, and validation.
- Use model reasoning for ambiguity, judgment, synthesis, design, and communication.
- Prefer the simplest capable model when model choice is available, but require it to pass the same acceptance check. Use stronger reasoning for high-risk, ambiguous, or architecture-heavy work.
- Mention a model change only when the mismatch is material and actionable.
- Count failures, escalation, and human repair before calling a smaller model cheaper.
- Use prompt caching only for irreducible repeated API background with an exact stable prefix and the changing assignment last. Remove irrelevant background first. Treat caching as a cost/latency optimization, not a token reduction.

### 4. Maintain an accepted-state checkpoint

After a meaningful stage, preserve a compact state containing:

- objective;
- accepted artifact or result;
- decisions and constraints;
- proof gathered;
- remaining uncertainty;
- next action.

Build revisions from the accepted artifact plus the requested change. Do not replay the entire drafting or research history unless the user asks for it or a disputed decision depends on it.

Use `scripts/accepted_state.py` when accepted-state reuse will recur:

```bash
python3 /absolute/path/to/token-saver/scripts/accepted_state.py save \
  --state /absolute/path/to/project/.token-saver/task.json \
  --accepted-file /absolute/path/to/accepted-result.md \
  --request-file /tmp/request.txt --source /absolute/path/to/source

python3 /absolute/path/to/token-saver/scripts/accepted_state.py packet \
  --state /absolute/path/to/project/.token-saver/task.json \
  --change-file /tmp/change.txt --output /tmp/revision-packet.md
```

Save only after explicit human acceptance. Keep one current result, not a growing history. For zero-regeneration reuse, run `lookup` with the current request and relevant sources; a changed request or source must miss.

For genuinely long work near context limits, create or update this checkpoint before compaction, context editing, or task handoff. Keep the small fact or decision the next step needs and drop the raw page, screenshot, log, or tool output. Do not compact short conversations merely because the feature exists. Treat compacted state as lossy: retain exact identifiers, commands, citations, and safety constraints verbatim. Remember that context editing can break an exact prompt-cache prefix; compare the whole job rather than preserving waste for a discount.

### 5. Control retries

On failure:

1. Capture the concise error and the attempted approach.
2. State a concrete new hypothesis.
3. Provide the failed check and the smallest missing evidence to one bounded repair.
4. Validate the new result.

Never retry a token-limit or usage-limit failure unchanged. Reduce the request, narrow the source, drop irrelevant tools, move exact work into code, switch to a justified cheaper path, or wait for the limit to reset. Allow at most one bounded repair for a deficient answer; after that, stop and report the blocker unless a clearly distinct safe approach changes the request itself.

### 6. Measure the whole job

When usage data is available, record fresh input, reused or cached input, cache writes, output, reasoning output when reported, model calls, retries, model used, and human repair. Sum every planning, selection, answering, checking, and repair call.

- Record unavailable metrics as `unavailable`; never estimate them as facts.
- Moving tokens to another model or worker is not a saving unless the combined total falls.
- A cache discount is a cost saving, not a token reduction.
- A shorter answer is not a win if it omits required work or fails the same acceptance check.

### 7. Finish leanly

Lead with the outcome. Include only:

- what was completed;
- the proof that matters;
- the artifact or link, when one exists;
- any real remaining uncertainty or blocker.

Do not narrate routine tool use, repeat the prompt, or append generic next steps.

## User-Correction Handling

When the user corrects a mistaken instruction:

- treat the latest correction as authoritative within existing safety and scope boundaries;
- stop carrying the invalid instruction into later work;
- rebuild from the last accepted state rather than layering corrections onto a known-bad draft;
- suggest editing and resending the original user message only when the client supports it and doing so would materially avoid a long, contaminated branch.

## Hard Limits and Honesty

This skill cannot:

- shrink the conversation, system instructions, or tool definitions already included before the skill loads;
- guarantee provider billing, rate-limit, or context-window behavior;
- unload platform tools that are already active;
- enforce transport-level input, output, or cost caps unless the platform exposes controls for them;
- replace external routing or middleware that can reject, cache, or rewrite a request before a model call.

If the user needs strict token or cost ceilings, recommend platform or API controls such as request-size validation, separate fresh/reused/output/call limits, provider budgets, retrieval, or middleware. Keep those recommendations separate from what this skill itself has verified.

## Source Notes

Read [references/video-principles.md](references/video-principles.md) only when auditing or revising this skill. It records the verified guide, original video, fifteen-move map, evidence boundaries, and reconstruction limits; it is not required during normal task execution.
