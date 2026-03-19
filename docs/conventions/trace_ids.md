# Trace and Correlation ID Rules

## Purpose

Ensure every Stage 1 run is inspectable across packets, logs, evidence artifacts, and return envelopes.

## IDs

### `trace_id`
- identifies the logical request journey
- must remain stable across the whole run
- format:
  - `trace_YYYYMMDD_<opaque>`
- example:
  - `trace_20260319_01f8ab2c9d7e`

### `run_id`
- identifies a single execution attempt
- unique per attempt
- format:
  - `run_YYYYMMDD_<opaque>`
- example:
  - `run_20260319_01f8ab2c9d7e`

## Correlation rules

The following must all carry the same `trace_id`:
- canonical packet
- provider request wrapper
- provider response wrapper
- trace logs
- evidence artifact
- OpenClaw return envelope

## Logging rule

Every stage transition log line should include at minimum:
- timestamp
- trace_id
- run_id
- stage
- status
