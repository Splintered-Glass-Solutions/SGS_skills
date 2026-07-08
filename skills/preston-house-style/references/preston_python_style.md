# Preston Python Style (Bonfire_ETL-Inspired)

Use this as a template library. Adapt to the repo you are in; do not fight an established style guide if one exists.

## Response Helpers Pattern

Prefer returning structured dicts and short-circuiting with `require_ok`.

```python
from bonfire_etl_shared import response


def helper() -> dict[str, object]:
    if bad:
        return response.error("SOME_FAILED", "explain what failed", status=500, retryable=True)
    return response.ok("some_ok", data={"x": 1})


def boundary() -> dict[str, object]:
    try:
        resp = helper()
        response.require_ok(resp)
        return response.ok("ok")
    except response.ResponseError as exc:
        err = exc.response.get("error") or {}
        return response.error(
            err.get("code", "UNKNOWN"),
            err.get("message", "unknown error"),
            status=int(exc.response.get("status") or 400),
            retryable=bool(err.get("retryable", False)),
        )
```

## Lambda/Queue Handler Skeleton

Prefer `handle_request(...)` delegating to `main(...)` and a separate `handle_sqs_message(...)` that normalizes inputs.

```python
import json
from typing import Dict

from bonfire_etl_shared import response
from bonfire_etl_shared.validate import validate_ids

FUNCTION_NAME = "some.function.name"


def handle_request(req: Dict[str, object]) -> Dict[str, object]:
    return main(req)


def handle_sqs_message(record: Dict[str, object]) -> Dict[str, object]:
    try:
        payload = json.loads(record.get("body") or "{}")
        req = {
            "org_id": payload["org_id"],
            "user_id": payload["user_id"],
            "metadata": payload.get("metadata", {}),
            "requested_at": payload.get("requested_at"),
            "trigger": {"type": "sqs", "request_id": str(record.get("messageId", "unknown"))},
        }
    except Exception as exc:  # noqa: BLE001 - placeholder error handling
        return {
            "ok": False,
            "function": FUNCTION_NAME,
            "request_id": "unknown",
            "entity_ids": {"org_id": None, "user_id": None, "kb_id": None, "content_id": None, "source_id": None},
            "routed_to": None,
            "actions": {"updated_rows": 0, "wrote_storage_objects": 0, "enqueued_messages": 0},
            "errors": [{"code": "CONFIG_INVALID", "message": f"Invalid SQS payload: {exc}", "retryable": False}],
        }
    return main(req)


def main(req: Dict[str, object]) -> Dict[str, object]:
    """
    Steps:
    1) validate inputs
    2) load rows
    3) apply policy gates / idempotency
    4) perform work
    5) persist updates
    6) enqueue downstream work
    7) return summary
    """
    request_id = str((req.get("trigger") or {}).get("request_id", "unknown"))
    entity_ids = {
        "org_id": req.get("org_id"),
        "user_id": req.get("user_id"),
        "kb_id": req.get("kb_id"),
        "content_id": req.get("content_id"),
        "source_id": req.get("source_id"),
    }
    try:
        resp_vi = validate_ids(org_id=req["org_id"], user_id=req["user_id"])
        response.require_ok(resp_vi)
        return {
            "ok": True,
            "function": FUNCTION_NAME,
            "request_id": request_id,
            "entity_ids": entity_ids,
            "routed_to": {"queue_name": "", "route_key": ""},
            "actions": {"updated_rows": 0, "wrote_storage_objects": 0, "enqueued_messages": 0},
            "errors": [],
        }
    except response.ResponseError as exc:
        err = exc.response.get("error") or {}
        return {
            "ok": False,
            "function": FUNCTION_NAME,
            "request_id": request_id,
            "entity_ids": entity_ids,
            "routed_to": None,
            "actions": {"updated_rows": 0, "wrote_storage_objects": 0, "enqueued_messages": 0},
            "errors": [
                {
                    "code": err.get("code", "UNKNOWN"),
                    "message": err.get("message", "unknown error"),
                    "retryable": bool(err.get("retryable", False)),
                }
            ],
        }
```

## Skip/Idempotency Conventions

- Return success with `actions.skipped=True` and a stable `skip_code`.
- Use `_SKIP` suffixes for skip codes (`ALREADY_PROCESSED_SKIP`, `CONTENT_INACTIVE_SKIP`).
- Record skip decisions if the repo supports it (for ETL budgets/observability).

## Error Code Conventions

- Use SCREAMING_SNAKE.
- Prefer:
  - `CONFIG_MISSING`, `CONFIG_INVALID`
  - `DB_READ_FAILED`, `DB_WRITE_FAILED`
  - `STORAGE_READ_FAILED`, `STORAGE_WRITE_FAILED`
  - `SQS_PUBLISH_FAILED`

## Pytest Patterns

Use `monkeypatch` to stub dependencies and env vars.

```python
from bonfire_etl_shared import response


def test_missing_env_var(monkeypatch):
    monkeypatch.delenv("SOME_ENV", raising=False)
    out = some_fn()
    assert out["error"] is not None
    assert out["error"]["code"] == "CONFIG_MISSING"
```
