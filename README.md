# Ganglion

Ganglion is in **zero-base rebuild** mode.

## Current status

This repository has been hard-reset so the active posture is visually unambiguous:
- active rebuild materials live at the repo surface and under `active/`
- pre-reset implementation has been moved under `archive/legacy-pre-zero-base/`
- legacy code is reference only, not the active implementation base

## Current phases

- Phase 0: reset baseline
- Phase 1: contracts and conventions
- Phase 2: minimum packet spine only

## First technical proof

The first proof target is only:
- OpenClaw -> Ganglion -> provider -> Ganglion -> OpenClaw

Explicitly out of scope until that path is evidenced:
- memory systems
- tuning/evals
- dashboard/Cortex expansion
- import/export machinery
- broader service architecture

## Key files

- `RESET_BRIEF.md`
- `ROADMAP_ZERO_BASE.md`
- `docs/phase0/PHASE0_REPORT_2026-03-19.md`
- `docs/archive/LEGACY_IMPLEMENTATION_INVENTORY.md`
- `archive/README.md`
- `active/`
