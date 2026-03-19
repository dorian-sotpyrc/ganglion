# OpenClaw Return Envelope Contract

## Purpose

Defines the minimum return payload Ganglion emits back toward OpenClaw after response shaping.

## Boundary owner

- Themed component: `Mandible`
- Plain role: response shaping and consumable return

## Success shape

```json
{
  "trace_id": "trace_20260319_01f8ab2c9d7e",
  "run_id": "run_20260319_01f8ab2c9d7e",
  "status": "success",
  "output": {
    "role": "assistant",
    "content": "hello back"
  },
  "provider": {
    "name": "openai",
    "model": "gpt-5.4"
  },
  "usage": {
    "input_tokens": 10,
    "output_tokens": 12,
    "total_tokens": 22,
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

## Failure shape

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
    "retryable": true
  }
}
```

## Rules

- `status` must be `success` or `error`
- `output.role` is fixed to `assistant` on success in Stage 1
- `output.content` must be plain string in Stage 1
- evidence linkage must be explicit when evidence writing is enabled
- callers should be able to surface a useful error without reading raw provider output
