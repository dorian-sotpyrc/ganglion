# Phase 1 Contract Examples

## Valid input example

```json
{
  "request_id": "req_123",
  "conversation_id": "channel:1480766516810088480",
  "timestamp": "2026-03-19T01:54:00Z",
  "messages": [
    {"role": "user", "content": "Ping Ganglion"}
  ],
  "provider_hint": "openai",
  "model_hint": "gpt-5.4",
  "metadata": {
    "source_system": "openclaw",
    "channel": "discord"
  }
}
```

## Invalid input example

Reason: missing `request_id`, `messages` empty, malformed `metadata`.

```json
{
  "timestamp": "2026-03-19T01:54:00Z",
  "messages": [],
  "metadata": "discord"
}
```

## Success response example

```json
{
  "trace_id": "trace_20260319_01f8ab2c9d7e",
  "run_id": "run_20260319_01f8ab2c9d7e",
  "status": "success",
  "output": {
    "role": "assistant",
    "content": "Ping received."
  },
  "provider": {
    "name": "openai",
    "model": "gpt-5.4"
  },
  "usage": {
    "input_tokens": 9,
    "output_tokens": 5,
    "total_tokens": 14,
    "cost": null,
    "currency": null
  },
  "evidence": {
    "written": true,
    "artifact_path": "runtime/evidence/2026-03-19T01-54-02Z_trace_20260319_01f8ab2c9d7e_run.json"
  },
  "error": null
}
```

## Failure response example

```json
{
  "trace_id": "trace_20260319_01f8ab2c9d7e",
  "run_id": "run_20260319_01f8ab2c9d7e",
  "status": "error",
  "output": null,
  "provider": {
    "name": "openai",
    "model": "gpt-5.4"
  },
  "usage": null,
  "evidence": {
    "written": true,
    "artifact_path": "runtime/evidence/2026-03-19T01-54-02Z_trace_20260319_01f8ab2c9d7e_run.json"
  },
  "error": {
    "type": "provider_transport_error",
    "message": "provider timeout",
    "stage": "peduncle",
    "retryable": true,
    "details": {"timeout_ms": 30000}
  }
}
```

## Evidence artifact example

```json
{
  "run_id": "run_20260319_01f8ab2c9d7e",
  "trace_id": "trace_20260319_01f8ab2c9d7e",
  "status": "success",
  "start_time": "2026-03-19T01:54:01Z",
  "end_time": "2026-03-19T01:54:02Z",
  "duration_ms": 913,
  "provider": "openai",
  "model": "gpt-5.4",
  "request_summary": {
    "message_count": 1,
    "roles": ["user"],
    "content_preview": "Ping Ganglion"
  },
  "response_summary": {
    "output_preview": "Ping received.",
    "status": "success"
  },
  "error_summary": null,
  "usage": {
    "input_tokens": 9,
    "output_tokens": 5,
    "total_tokens": 14,
    "cost": null,
    "currency": null
  },
  "paths": {
    "trace_log_path": "runtime/traces/2026-03-19T01-54-02Z_trace_20260319_01f8ab2c9d7e.log"
  }
}
```
