# Ganglion Canonical Packet Contract

## Purpose

Defines the canonical internal work packet Ganglion constructs after ingress normalization.

In the new design intent, this packet represents an operator-tool workflow rather than a mandatory provider-execution envelope.

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
  "operation": "brain_scan",
  "target": {
    "agent_id": "william",
    "session_id": "agent:william:discord:channel:1480766516810088480"
  },
  "evidence_mode": "write_local",
  "metadata": {
    "request_id": "req_01hxyz...",
    "channel": "discord"
  },
  "options": {
    "include_summary_depth": true,
    "include_backup_plan": true
  }
}
```

## Required fields

- `packet_version`
- `trace_id`
- `run_id`
- `source_system`
- `ingress_timestamp`
- `operation`
- `target`
- `evidence_mode`
- `metadata`

## Field rules

### `packet_version`
- fixed string in this phase: `v1alpha1`

### `operation`
Allowed values:
- `visibility_report`
- `brain_scan`
- `backup_plan`
- `optimisation_review`

### `target`
Should identify the session and/or agent being inspected or tuned.

### `evidence_mode`
Allowed values:
- `write_local`
- `disabled`

## Validation rules

- all required fields must exist
- `metadata` must be object-shaped
- `target` must be object-shaped
- packet must be JSON-serializable

## Failure contract

Invalid canonical packets must fail as `validation_error` before downstream scan/report/backup/tuning logic runs.
