# Research notes (2026-11-10)

- [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/research/demystifying-evals-for-ai-agents) distinguishes the transcript from actual environment outcomes and discusses evaluating over-engineering. Inspection implication: measure delivered state as well as activity, and avoid treating an agent's claim as proof.
- [Anthropic: Building effective agents](https://www.anthropic.com/research/building-effective-agents) discusses evaluator/optimizer workflows where evaluation criteria are clear and iterative improvement is measurable. Inspection implication: use a bounded independent review, not an endless self-review cycle.
- [OpenAI: A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) discusses simple orchestration, explicit loop exit conditions and risk-sensitive safeguards. Inspection implication: identify a next outcome and stop conditions while retaining applicable safeguards.
- [OpenAI: Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals) describes traces as records of agent calls, tools, guardrails and handoffs. Inspection implication: trace individual blockers and repetition to actual evidence and authority.

These are design implications, not evidence that this particular workflow or model will perform better. Validate the skill against real cases and revise based on observed failures.
