# OpenClaw Ingress Contract

## Purpose

Defines the minimum OpenClaw-origin inspection/tuning request envelope Ganglion accepts at the ingress boundary in its new companion role.

This ingress is now primarily for:
- visibility requests
- brain scan requests
- backup/export requests
- optimisation/tuning analysis requests

## Boundary owner

- Themed component: `Antennule`
- Plain role: ingress sensing and intake normalization

## Contract shape

```json
{
  "request_id": "req_01hxyz...",
  "timestamp": "2026-03-19T01:54:00Z",
  "operation": "brain_scan",
  "agent_id": "william",
  "session_id": "agent:william:discord:channel:1480766516810088480",
  "metadata": {
    "source_system": "openclaw",
    "channel": "discord"
  },
  "options": {
    "include_summary_depth": true,
    "include_backup_plan": true
  }
}
```

## Required fields

- `request_id` — unique source request identifier
- `timestamp` — ingress timestamp in ISO 8601 UTC form
- `operation` — requested Ganglion operation
- `metadata` — object bag for source metadata

## Recommended identifiers

At least one of the following should normally be present:
- `agent_id`
- `session_id`

## Allowed Stage-A operations

- `visibility_report`
- `brain_scan`
- `backup_plan`
- `optimisation_review`

## Validation rules

- `operation` must be one of the allowed values
- `timestamp` must be parseable ISO 8601
- `metadata` must be an object
- if both `agent_id` and `session_id` are absent, ingress should fail unless the operation explicitly supports global inspection
- `options`, if present, must be an object

## Failure contract

Ingress must fail with structured `ingress_error` when:
- required fields are absent
- requested operation is unsupported
- no inspection target is provided where required
- top-level shape is not an object

## Notes

This contract no longer assumes Ganglion is taking ownership of all provider traffic. It assumes Ganglion is receiving targeted operator-tool requests around an existing lossless-claw deployment.
