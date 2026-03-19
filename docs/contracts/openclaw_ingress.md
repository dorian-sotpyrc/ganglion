# OpenClaw Ingress Contract

## Purpose

Defines the minimum OpenClaw-origin request envelope Ganglion accepts at the ingress boundary for Phase 1 / Stage 1.

## Boundary owner

- Themed component: `Antennule`
- Plain role: ingress sensing and intake normalization

## Contract shape

```json
{
  "request_id": "req_01hxyz...",
  "conversation_id": "channel:1480766516810088480",
  "timestamp": "2026-03-19T01:54:00Z",
  "messages": [
    {
      "role": "user",
      "content": "hello"
    }
  ],
  "provider_hint": "openai",
  "model_hint": "gpt-5.4",
  "metadata": {
    "source_system": "openclaw",
    "channel": "discord"
  }
}
```

## Required fields

- `request_id` — unique source request identifier
- `timestamp` — ingress timestamp in ISO 8601 UTC form
- `messages` — non-empty ordered list of message objects
- `metadata` — object bag for source metadata

## Conditionally required / recommended fields

- `conversation_id` — recommended when available
- `provider_hint` — optional hint only, not a guarantee
- `model_hint` — optional hint only, not a guarantee

## Message object

Each `messages[]` item must include:
- `role` — one of `system`, `user`, `assistant`, `tool`
- `content` — string content for Phase 1

Optional:
- `name`
- `tool_call_id`
- `metadata`

## Validation rules

- unknown top-level fields are allowed only if preserved under `metadata` by the caller; Ganglion should not rely on them in Stage 1
- `messages` must contain at least one item
- each message `content` must be a string in Stage 1
- `timestamp` must be parseable ISO 8601
- `metadata` must be an object

## Failure contract

Ingress must fail with structured `ingress_error` when:
- required fields are absent
- `messages` is empty
- message content type is unsupported
- top-level shape is not an object

## Notes

This contract is intentionally small. It does not attempt to mirror the full OpenClaw internal envelope surface in Phase 1.
