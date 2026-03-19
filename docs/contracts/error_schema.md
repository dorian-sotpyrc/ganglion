# Error Contract

## Purpose

Defines the structured error shape used across Stage 1 boundaries.

## Canonical shape

```json
{
  "type": "provider_transport_error",
  "message": "provider timeout",
  "stage": "peduncle",
  "retryable": true,
  "details": {
    "timeout_ms": 30000
  }
}
```

## Required fields

- `type`
- `message`
- `stage`
- `retryable`
- `details`

## Allowed `type` values in Stage 1

- `ingress_error`
- `validation_error`
- `provider_transport_error`
- `response_shaping_error`
- `evidence_write_error`

## Allowed `stage` values in Stage 1

- `antennule`
- `pleon`
- `ventral`
- `peduncle`
- `mandible`
- `cortex_seed`

## Rules

- `message` must be operator-readable
- `details` must be JSON-serializable
- internal stack traces should not be required for normal operator understanding
- retryability must be explicit, never implied
