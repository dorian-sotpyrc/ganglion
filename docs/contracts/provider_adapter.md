# Provider Adapter Contracts

## Purpose

Defines the outbound provider request contract and inbound normalized provider response contract for Phase 1.

## Boundary owner

- Themed component: `Peduncle`
- Plain role: provider/API interface bridge

## Stage 1 scope

Stage 1 supports exactly one provider adapter path at a time. The contract remains provider-agnostic at the Ganglion side and provider-specific at the transport edge.

---

## Outbound provider request contract

```json
{
  "trace_id": "trace_20260319_01f8ab2c9d7e",
  "run_id": "run_20260319_01f8ab2c9d7e",
  "provider": "openai",
  "model": "gpt-5.4",
  "messages": [
    {
      "role": "user",
      "content": "hello"
    }
  ],
  "transport": {
    "timeout_ms": 30000
  },
  "metadata": {
    "source_system": "ganglion"
  }
}
```

### Required fields
- `trace_id`
- `run_id`
- `provider`
- `model`
- `messages`
- `transport`
- `metadata`

### Rules
- `messages` must preserve message order from `normalized_messages`
- `transport.timeout_ms` must be explicit
- Stage 1 supports one outbound request per run attempt

---

## Inbound normalized provider response contract

```json
{
  "trace_id": "trace_20260319_01f8ab2c9d7e",
  "run_id": "run_20260319_01f8ab2c9d7e",
  "status": "success",
  "provider": "openai",
  "model": "gpt-5.4",
  "output_text": "hello back",
  "raw_timing": {
    "started_at": "2026-03-19T01:54:01Z",
    "completed_at": "2026-03-19T01:54:02Z",
    "duration_ms": 913
  },
  "usage": {
    "input_tokens": 10,
    "output_tokens": 12,
    "total_tokens": 22,
    "cost": null,
    "currency": null
  },
  "transport_metadata": {
    "http_status": 200,
    "request_id": "provider_req_123"
  },
  "raw_response_ref": null,
  "error": null
}
```

### Required fields
- `trace_id`
- `run_id`
- `status`
- `provider`
- `model`
- `raw_timing`
- `transport_metadata`

### Success rules
If `status = success`:
- `output_text` must be present and string typed
- `error` must be null

### Failure rules
If `status = error`:
- `error` must contain structured error object
- `output_text` may be omitted or null

### Allowed status values
- `success`
- `error`

---

## Transport error mapping

Provider transport failures must be normalized into `provider_transport_error` rather than leaking provider-native shapes directly across Ganglion boundaries.
