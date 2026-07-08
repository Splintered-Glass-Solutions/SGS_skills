---
name: preston-house-style
description: "Apply Preston's pragmatic, Python-first house style when writing or refactoring code. Use when implementing ETL/Lambda-style handlers, request/response flows, parsing/normalization, policy gating, idempotency/skip logic, or pytest tests where you want: structured response dicts, explicit error/skip codes, defensive boundary checks, step-wise main() flows, env-driven config with clear CONFIG_MISSING errors, and minimal abstractions."
---

# Preston House Style

## Overview

Produce code that matches Preston's "structured + defensive + explicit" style: clear control flow, stable error/skip codes, and predictable response shapes, with focused pytest coverage.

## Quick Start

1. Define the boundary response shape: use `bonfire_etl_shared.response.ok/error` for helpers, and function-level `ok_response/error_response` envelopes for handlers.
2. Make skip decisions explicit: return `ok_response(..., actions={..., "skipped": True, "skip_code": "SOME_SKIP"})`.
3. Use stable error codes: SCREAMING_SNAKE (`CONFIG_MISSING`, `DB_READ_FAILED`, `KB_RATE_LIMIT_MINUTE_SKIP`).
4. Normalize inputs defensively at boundaries: check types, default to `{}`/`[]`, and guard against empty/invalid bytes/JSON.
5. Add pytest tests that assert on response fields and cover at least one edge-case regression.

## Conventions

### Shape And Errors

- Prefer explicit dict envelopes over ad-hoc exceptions across layers.
- Use `response.require_ok(resp)` to short-circuit helpers and catch `response.ResponseError` at the boundary.
- Prefer `response.error(code, message, status=..., retryable=...)` over raising for expected failures.
- Keep error codes stable and searchable; use `_SKIP` for allowed skips and `_FAILED` for operational failures.

### Control Flow

- Prefer a `main(req)` function with a docstring that lists numbered steps.
- Use early returns for skip cases and config validation.
- Keep helpers small and single-purpose (DB read/write, storage read, chunking, enqueue).

### Config And Environment

- Read config via `os.environ.get(...)` / `os.getenv(...)`.
- If a required env var is missing, return `CONFIG_MISSING` (or `CONFIG_INVALID` when present-but-bad).
- Allow metadata overrides when it makes sense (env defaults, explicit metadata wins).

### Exceptions

- Catch broad exceptions at boundaries when needed and annotate: `except Exception as exc:  # noqa: BLE001 - <reason>`.
- Convert unexpected exceptions into `..._FAILED` errors with `retryable=True` only when the caller can safely retry.

### Types, Naming, And Docs

- Use type hints for boundaries (request dicts, helper returns). Keep it simple; avoid over-modeling.
- Prefer `FUNCTION_NAME = "..."` constants for handler identity.
- Put a short module docstring at the top of non-trivial modules.

### Testing

- Use pytest function tests with `monkeypatch` to stub I/O and env vars.
- Assert on the stable response shape and specific error/skip codes.
- Add regression tests for edge cases (infinite loops, empty input, boundary conditions).

## References

Read `references/preston_python_style.md` for copy/paste templates (handler skeletons, response envelopes, test patterns) and naming conventions.
