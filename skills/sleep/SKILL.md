---
name: sleep
description: Pause the current Codex task for a requested duration before continuing or processing queued user work. Use when the user says sleep, wait, pause for a specific amount of time, delay the next response, or asks for a prompt-level equivalent of sleep().
---

# Sleep

Pause execution using an external timer so the model does not spend the delay reasoning or repeatedly narrating status.

## Workflow

1. Parse the requested duration. Use five minutes only when the user invokes the skill without specifying a duration.
2. Record the target wake time before starting the wait.
3. Run `scripts/wait.py <duration>` through a long-running execution session. Yield control quickly and retain the session handle.
4. Use the environment's wait/resume primitive while the timer runs. Respect any platform limit on a single wait call; use the longest permitted interval and do not simulate waiting with reasoning loops.
5. Do not process downstream work or release the final response before the target wake time.
6. If a new user message arrives during the delay, defer it until wake time unless it explicitly cancels, shortens, or overrides the sleep.
7. After the timer completes, process the queued next request or, if the user only requested a pause, confirm completion concisely.

## Output Rules

- Avoid user-facing progress messages during the delay unless a higher-priority instruction requires one.
- Do not claim the pause consumes literally zero tokens; external waiting minimizes model work, but orchestration may still have small overhead.
- Do not use a busy loop, repeated shell invocations, or repeated timestamp checks.
- Do not schedule a recurring automation for a one-time sleep.
- If the execution environment cannot preserve a waiting session, state that limitation and use the closest available one-shot wakeup mechanism.

## Duration Format

The bundled timer accepts bare seconds or compound values such as `30s`, `5m`, `1h`, and `1h30m`. It rejects negative, malformed, and longer-than-24-hour waits to prevent accidental orphaned sessions.

```bash
python3 scripts/wait.py 5m
```

The script emits no output until the deadline, then returns a compact JSON completion record.
