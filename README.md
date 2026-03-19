# Ganglion

Ganglion is now on a **clean working base**.

The active implementation surface has been reset so the repository can be rebuilt deliberately as a:
- **lossless-claw visibility tool**
- **brain scanner**
- **backup/export helper**
- **memory optimisation companion**

## Core decision

- **lossless-claw is the primary memory engine**
- Ganglion is the companion layer around that engine

## Current repository posture

### Active
Active work now starts from:
- docs
- development plan
- empty implementation placeholders under:
  - `src/`
  - `scripts/`
  - `tests/`
  - `fixtures/`

### Archived
Previous implementation attempts are preserved under `archive/`:
- `archive/legacy-pre-zero-base/`
- `archive/prototype-pre-lcm-companion-reset-2026-03-20/`

Those archives are reference only, not the active implementation base.

## Why reset again

The repo had drifted into carrying transitional prototype code from the earlier zero-base effort.
That code may still contain useful ideas, but it no longer reflected the current product intent.

This reset restores a truthful base so the next implementation phase can begin cleanly.

## What comes next

Ganglion should now be built in phased slices:

1. visibility report specifications
2. brain scan specifications
3. backup/export artifact specifications
4. optimisation review specifications
5. first read-only implementation slice
6. safe change-planning workflows

## Working principle

Ganglion should make lossless-claw:
- easier to understand
- easier to inspect
- easier to back up
- easier to tune
- safer to evolve

It should not become a second hidden memory system.

## Key files

- `DEVELOPMENT_PLAN.md`
- `RESET_BRIEF.md`
- `ROADMAP_ZERO_BASE.md`
- `docs/briefs/GANGLION_ZERO_BASE_REBUILD_BRIEF_FULL.md`
- `active/README.md`
- `archive/README.md`
