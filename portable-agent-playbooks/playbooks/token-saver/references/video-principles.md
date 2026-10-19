# Source-derived principles

Primary source: Nate B. Jones, [“15 Ways to Cut Token Waste in Codex and Claude”](https://unlock-ai.natebjones.com/guides/cut-token-waste), last verified by the publisher on 2026-07-28 and retrieved for this skill on 2026-08-05.

Earlier source: “Paste This Into Claude, Never Hit a Token Limit Again,” published 2026-07-29. Local transcript: `<workspace-root>/personal/output/youtube-Y8vAQ1FgNbM-transcript.md`.

The web guide provides the authoritative fifteen-move ordering and clearer evidence boundaries than the auto-caption transcript. This local skill is an adapted implementation, not a copy of the publisher’s downloadable skill.

## Fifteen moves

1. Edit or rewind a plainly bad turn rather than stacking a correction onto the rejected branch.
2. Batch questions only when they share background.
3. Start a clean task when the job changes.
4. Carry the accepted result and new change, not the discussion that produced the result.
5. Search large sources before a model reads them; expand with another bounded passage if needed.
6. Use the lightest faithful source form: text instead of layout, a crop instead of a full screenshot, changed rows instead of a workbook, or a diff instead of two files.
7. Move work with one right answer into deterministic code.
8. Return a human-accepted answer without regeneration only on an exact request and source match.
9. Load only tools the job can use, using deferred loading or tool search when available.
10. Compact obsolete tool output only during genuinely long work and preserve the facts the next step needs.
11. Ask for only the usable answer, while giving writing enough room when writing is itself the product.
12. Route bounded work to a cheaper model only when the complete path passes the same check and costs less after failures and repair.
13. Put hard stops on oversized requests, outputs, calls, and repairs before the call when the platform allows it; never repeat a token-limit failure unchanged.
14. Cache irreducible repeated background using an exact stable prefix. Caching can reduce price or latency but does not remove processed tokens.
15. Use pre-call middleware only when the request must be reduced, answered locally, routed, or stopped before the model sees it. An in-call skill cannot provide that control retroactively.

## Evidence and accounting boundary

The guide reports one matched job in which the clean path used one call instead of three, reported zero reused input instead of 51,712, and reduced provider-reported input plus output by 85.77% while passing the same fact-and-structure checklist. It separately reports a deterministic code path that completed the checklist from a prepared fact file without a model call.

Treat those as bounded demonstrations, not universal percentages. The checklist did not prove identical writing quality, a reported zero does not reveal every hidden byte a product may transmit, and one job is not a full day.

Count the whole job: fresh input, reused or cached input, cache writes, output, reasoning output when reported, every planning/checking/repair call, and human repair. Record missing measurements as unavailable. Moving work between providers is not automatically a token saving, and discounted cached input is still input.

## Local implementation boundary

The guide’s downloadable package includes deterministic passage-selection and accepted-state helpers. This local skill now includes independently maintained equivalents:

- `scripts/select_context.py` selects scored, bounded passages from safe local text files.
- `scripts/accepted_state.py` keeps one accepted result, builds accepted-result-plus-delta packets, and permits zero-regeneration lookup only when request and source fingerprints match.

These helpers operate after the skill has loaded. They cannot shrink the current conversation, remove preloaded tool definitions, enforce provider-side budgets, or intercept the request before the model call.
