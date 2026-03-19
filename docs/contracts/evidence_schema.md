# Evidence Artifact Contract

## Purpose

Defines the per-run local evidence artifact written by Cortex Seed during Stage 1.

## Boundary owner

- Themed component: `Cortex Seed`
- Plain role: evidence capture and logging seed

## Artifact shape

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
    "content_preview": "hello"
  },
  "response_summary": {
    "output_preview": "hello back",
    "status": "success"
  },
  "error_summary": null,
  "usage": {
    "input_tokens": 10,
    "output_tokens": 12,
    "total_tokens": 22,
    "cost": null,
    "currency": null
  },
  "paths": {
    "trace_log_path": "runtime/traces/2026-03-19T01-54-02Z_trace_20260319_01f8ab2c9d7e.log"
  }
}
```

## Required fields

- `run_id`
- `trace_id`
- `status`
- `start_time`
- `end_time`
- `duration_ms`
- `provider`
- `model`
- `request_summary`
- `response_summary`
- `error_summary`
- `usage`
- `paths`

## Rules

- evidence artifact must be JSON
- one evidence artifact per run attempt
- `trace_id` must match trace logs and return envelope
- `error_summary` is null on success and populated on failure
- redaction-safe summaries are preferred over raw message dumps in Stage 1 evidence artifacts

## Redaction posture

Stage 1 evidence should prefer:
- content previews
- counts
- ids
- timing
- statuses

Stage 1 evidence should avoid:
- uncontrolled raw provider payload dumps in the main artifact
- secrets or auth headers
