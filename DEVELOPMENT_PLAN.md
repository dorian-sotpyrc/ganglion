# Ganglion Development Plan

## Current baseline

Ganglion is at a **clean working base**.

What is active now:
- governing docs
- phased plan
- empty implementation placeholders

What is archived now:
- pre-zero-base legacy implementation
- transitional prototype packet/live-binding implementation

This means future development can proceed from reviewed intent rather than inherited code drift.

## Product direction

Ganglion is a **lossless-claw visibility, brain scanner, backup, and memory optimisation companion**.

Primary memory remains with lossless-claw.
Ganglion improves operator understanding and control around that memory layer.

## Phase 1 — specifications

Goals:
- define the first useful outputs before writing implementation logic

Outputs to define:
- visibility report spec
- brain scan report spec
- backup/export artifact spec
- optimisation review spec
- evidence and comparison bundle spec

Acceptance:
- a reviewer can clearly see what Ganglion will produce
- boundaries are specific enough to implement without product drift

## Phase 2 — read-only implementation slice

Goals:
- deliver operator value with minimal risk

Target capabilities:
- inspect session/agent memory posture
- generate brain scan reports
- generate backup/export metadata/artifacts
- generate optimisation review reports

Acceptance evidence:
- fixture-driven outputs
- example artifacts committed to repo or docs
- tests for report generation paths

## Phase 3 — safe change planning

Goals:
- help operators plan improvements safely

Target capabilities:
- compare active settings to recommended settings
- produce config change plans
- include rollback notes and expected tradeoffs
- validate proposed changes before application

Acceptance evidence:
- before/after diff examples
- rollback example
- validation outputs

## Phase 4 — optional controlled write tooling

Goals:
- allow guarded tuning support only when earlier phases are proven

Guardrails:
- backup first
- dry-run first
- explicit rollback path
- validation after apply
- operator-readable summary

## Immediate next step

Pause implementation until documentation review is complete.
After review, begin Phase 1 spec authoring in detail.
