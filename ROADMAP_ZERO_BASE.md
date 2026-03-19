# Ganglion Zero-Base Roadmap

## Phase 0 — archive + explicit reset baseline

Goal:
- separate legacy implementation from active rebuild posture

Deliverables:
- `RESET_BRIEF.md`
- legacy inventory report
- phase 0 completion report
- fresh `zero-base/` working root

Exit criteria:
- legacy surface explicitly marked archive/reference only
- active rebuild root named and created
- no ambiguity about current scope

## Phase 1 — contracts and conventions

Goal:
- define the minimum rebuild contract pack before implementation

Deliverables:
- envelope contract: OpenClaw -> Ganglion
- provider request/response contract
- return packet contract: Ganglion -> OpenClaw
- path and naming conventions
- evidence rules and fixture format

Exit criteria:
- packet inputs/outputs are specified without depending on legacy code
- one canonical path for the minimum spine is defined

## Phase 2 — minimum packet spine

Goal:
- prove the narrowest viable end-to-end path

Target path:
- OpenClaw input packet
- Ganglion normalization
- provider invocation
- Ganglion response normalization
- OpenClaw return packet

Required evidence:
- fixture input
- exact normalized packet
- provider request payload
- provider response payload
- final return packet
- test/log transcript
- pass/fail report

Out of scope until Phase 2 evidence exists:
- memory selection
- routing complexity
- tuning/evals
- dashboard/Cortex surfaces
- deployment registry work
- import/export machinery
