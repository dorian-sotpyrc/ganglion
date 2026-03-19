# Ganglion Development Plan

## Product direction

Ganglion is now a **lossless-claw visibility, brain scanner, backup, and memory optimisation companion**.

Primary memory remains with lossless-claw.
Ganglion should improve operator understanding and control around that existing memory layer.

## Workstreams

### Workstream 1 — repo cleanup and truthfulness

Goals:
- align docs with actual project intent
- mark transitional prototype code clearly
- remove or quarantine misleading language

Planned tasks:
- update README and briefs
- update roadmap
- classify existing code as active vs transitional
- document implementation boundaries

### Workstream 2 — visibility and scan specifications

Goals:
- define the first useful operator outputs

Planned outputs:
- visibility report spec
- brain scan spec
- backup/export spec
- optimisation review spec
- evidence bundle spec

Questions to answer:
- what exact lossless-claw state needs to be visible?
- what should be summarized versus raw in a scan?
- what constitutes an optimisation recommendation?

### Workstream 3 — minimum useful read-only implementation

Goals:
- deliver value without write-risk first

Target capabilities:
- inspect session/agent memory posture
- generate brain scan report
- generate backup plan / snapshot metadata
- produce optimisation review report

Acceptance evidence:
- fixture-driven report outputs
- sample scan artifacts
- reproducible test run
- operator-readable examples

### Workstream 4 — safe change planning

Goals:
- move from diagnosis to safe improvement support

Target capabilities:
- compare active config to recommended profile
- generate config diff and rollback note
- validate change plan before write
- produce before/after evidence

### Workstream 5 — optional write-path tooling

Goals:
- allow controlled tuning changes only after read-only mode is proven

Guardrails:
- backup before change
- explicit rollback path
- dry-run first
- validation after apply
- human-readable summary of tradeoffs

## Current repo interpretation

### Keep / likely reusable
- evidence-writing posture
- trace/report discipline
- tests/fixtures structure
- some artifact-generation patterns

### Transitional / likely to be repurposed
- packet spine prototype
- live-binding prototype
- provider-path assumptions

### Archive if they distort intent
- docs or specs that imply Ganglion replaces lossless-claw
- code paths that force the project back into a competing-memory identity

## Sequencing

1. complete doc refocus
2. define first operator-facing report contracts
3. implement read-only visibility + brain scan path
4. implement backup/export artifact path
5. implement optimisation review path
6. only then consider safe config patching

## Definition of success for next review

For the next review pass, the repo should make it obvious that:
- lossless-claw is the memory engine
- Ganglion is the companion tool layer
- the first implementation target is inspectability and tuning support
