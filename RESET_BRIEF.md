# Ganglion Reset Brief

## Status

Ganglion is under **zero-base rebuild**.

This repository contains a substantial pre-reset implementation. That implementation is now treated as:
- **archive/reference only**
- useful for inspection, vocabulary extraction, and contrast
- **not** the active base for the rebuild

## Governing posture

The rebuild proceeds from first principles.

Primary rules:
- old code is not the starting implementation base
- first deliverable is contracts, conventions, and roadmap
- first technical proof is only the packet spine:
  - OpenClaw -> Ganglion -> provider -> Ganglion -> OpenClaw
- no memory, tuning, dashboard, import/export, or Cortex/API expansion before the spine is evidenced
- new implementation work should land under the fresh zero-base root, not by extending the legacy surface

## Phase framing

### Phase 0
Archive the legacy implementation and establish an explicit reset baseline.

### Phase 1
Define contracts, naming, path conventions, and repo execution rules.

### Phase 2
Implement the minimum packet spine and produce evidence artifacts.

## Active implementation root

The fresh rebuild root is:
- `zero-base/`

Legacy implementation remains in-place for reference under the existing repository structure.

## Evidence standard

A phase is complete only when it has:
- a written scope boundary
- explicit paths
- pass/fail criteria
- evidence artifacts or report files

## Anti-creep note

Until the packet spine is proven, the following are explicitly out of scope:
- memory systems
- tuning loops
- dashboard integration
- agent detail hydration
- import/export flows
- long-lived API/service surfaces beyond the minimum spine proof
