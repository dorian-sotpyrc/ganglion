# Phase 0 Report — Archive + Explicit Reset Baseline

Date: 2026-03-19
Status: complete

## Objective

Complete Phase 0 of the Ganglion zero-base rebuild:
- archive the legacy implementation posture
- establish the explicit reset baseline
- create an unambiguous active root for new rebuild work

## Actions completed

1. Declared zero-base rebuild posture in `RESET_BRIEF.md`
2. Wrote phase roadmap in `ROADMAP_ZERO_BASE.md`
3. Produced legacy inventory in `docs/archive/LEGACY_IMPLEMENTATION_INVENTORY.md`
4. Created a fresh active root for rebuild work at `zero-base/`
5. Added minimal root marker in `zero-base/README.md`

## Result

Repository posture is now explicit:
- the previous implementation remains present but is treated as archive/reference only
- the active rebuild base is now `zero-base/`
- future work should begin from contracts and packet-spine proof, not from extending the legacy package

## Legacy/active split

### Legacy
- existing package tree under `ganglion/`
- existing staged tests, scripts, migrations, artifacts, and brain structure

### Active
- `zero-base/`

## Risks remaining

- the old README and package tree still describe the pre-reset implementation and can still attract drift if someone ignores the reset docs
- no Phase 1 contracts exist yet
- no packet-spine proof exists yet

## Recommended next step

Proceed to Phase 1 only:
- define contracts
- define naming/path conventions
- define evidence format

Do not expand into memory/dashboard/Cortex/tuning work before the minimum packet spine is specified and proven.
