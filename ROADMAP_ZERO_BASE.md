# Ganglion Refocus Roadmap

## Phase A — strategic refocus + repo truthfulness

Goal:
- align repo narrative, plan, and active surface with the new role as a lossless-claw companion

Deliverables:
- updated README
- updated reset/governing brief
- updated active posture docs
- explicit statement of what prototype code is transitional vs active
- development plan for the new direction

Exit criteria:
- no top-level docs present Ganglion as a competing memory engine
- repo posture clearly states lossless-claw is primary memory
- next implementation steps are operator-tool oriented

## Phase B — visibility and brain scan specifications

Goal:
- define the minimum operator-facing interfaces for inspecting lossless-claw state

Deliverables:
- visibility report spec
- brain scan spec
- backup/export artifact spec
- tuning recommendation spec
- before/after evidence format

Exit criteria:
- operator can understand what the first useful Ganglion outputs will be
- interfaces are clear enough to implement without product drift

## Phase C — minimum useful implementation

Goal:
- deliver the first real operator value around the existing lossless-claw deployment

Target features:
- inspect current session/agent memory posture
- produce a brain scan report
- export a safe backup/snapshot artifact
- generate tuning recommendations from observed posture

Required evidence:
- sample scan input
- produced visibility report
- produced backup artifact
- produced optimisation recommendation report
- tests or fixture-driven proof

## Phase D — safe tuning workflows

Goal:
- move from read-only inspection to controlled optimisation support

Target features:
- validate current lossless-claw settings
- compare current settings to recommended profile
- produce safe change plans
- optionally write config patches with explicit rollback path

Required evidence:
- before/after config diff
- rollback artifact
- validation output
- operator-facing summary of expected tradeoffs

## Out of scope unless explicitly revived

- replacing lossless-claw as the memory engine
- building a broad speculative brain runtime first
- general provider middleware expansion as the primary project identity
- large dashboard ambitions before useful operator tooling exists
