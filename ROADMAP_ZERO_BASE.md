# Ganglion Refocus Roadmap

## Current state

Phase A is now effectively complete at the repo-structure level:
- design intent refocused around lossless-claw operations
- prototype code archived
- active implementation surface reset to a clean base

## Phase A — strategic refocus + clean base

Goal:
- align repo narrative and structure with Ganglion’s role as a lossless-claw companion

Deliverables:
- updated README and briefs
- updated active/archive posture docs
- archived transitional prototype code
- empty active implementation surface
- phased development plan

Exit criteria:
- repo does not imply Ganglion is a competing memory engine
- active code surface is clean and truthful
- next work starts from specs, not drift

## Phase B — visibility and brain scan specifications

Goal:
- define the minimum operator-facing outputs for inspecting lossless-claw state

Deliverables:
- visibility report spec
- brain scan spec
- backup/export artifact spec
- optimisation review spec
- before/after evidence format

Exit criteria:
- operator can understand the first useful Ganglion outputs
- interfaces are clear enough to implement cleanly

## Phase C — minimum useful read-only implementation

Goal:
- deliver the first operator value without write-risk

Target features:
- inspect current session/agent memory posture
- produce a brain scan report
- produce backup/export artifacts
- generate optimisation recommendations

Required evidence:
- sample inputs
- report artifacts
- backup artifacts
- fixture-driven tests
- operator-readable examples

## Phase D — safe change planning

Goal:
- move from diagnosis to safe improvement planning

Target features:
- compare active config to recommended profile
- produce safe change plans
- generate rollback notes
- validate before/after state

## Phase E — optional controlled write-paths

Goal:
- enable carefully guarded tuning changes only after read-only tooling is proven

Guardrails:
- backup first
- dry-run first
- explicit rollback path
- post-change validation
- human-readable tradeoff summary
