# Ganglion Canonical Packet Contract

## Purpose

Defines the canonical runtime packet created after ingress normalization and before provider adaptation.

## Boundary owner

- Themed component: `Pleon`
- Plain role: packet assembly and transport body

## Contract shape

```json
{
  "packet_version": "v1alpha1",
  "trace_id": "trace_20260319_01f8ab2c9d7e",
  "run_id": "run_20260319_01f8ab2c9d7e",
  "source_system": "openclaw",
  "ingress_timestamp": "2026-03-19T01:54:00Z",
  "normalized_messages": [
    {
      "index": 0,
      "role": "user",
      "content": "hello"
    }
  ],
  "provider_target": "openai",
  "model_target": "gpt-5.4",
  "routing_mode": "direct_single_provider",
  "evidence_mode": "write_local",
  "metadata": {
    "request_id": "req_01hxyz...",
    "conversation_id": "channel:1480766516810088480",
    "channel": "discord"
  }
}
```

## Required fields

- `packet_version`
- `trace_id`
- `run_id`
- `source_system`
- `ingress_timestamp`
- `normalized_messages`
- `provider_target`
- `model_target`
- `routing_mode`
- `evidence_mode`
- `metadata`

## Field rules

### `packet_version`
- fixed string in Stage 1: `v1alpha1`

### `trace_id`
- globally unique trace identifier
- must be stable across all artifacts for a run

### `run_id`
- unique run identifier
- one run id per execution attempt

### `normalized_messages`
Each item must include:
- `index` — zero-based integer
- `role` — normalized role string
- `content` — normalized string content

### `provider_target`
- exactly one provider target in Stage 1

### `model_target`
- exactly one model target in Stage 1

### `routing_mode`
Allowed Stage 1 value:
- `direct_single_provider`

### `evidence_mode`
Allowed Stage 1 values:
- `write_local`
- `disabled`

## Validation rules

- all required fields must exist
- `normalized_messages` must be non-empty
- `metadata` must be object-shaped
- no nested binary payloads in Stage 1 packet
- packet must be JSON-serializable

## Failure contract

Invalid canonical packets must fail as `validation_error` before provider adaptation.
