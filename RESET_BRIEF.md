# Ganglion Reset Brief

Canonical governing brief:
- `docs/briefs/GANGLION_ZERO_BASE_REBUILD_BRIEF_FULL.md`

## Status

Ganglion is under **strategic refocus**.

The earlier zero-base rebuild was useful as a discipline reset, but the project direction has now changed:
- **lossless-claw is the chosen memory engine**
- Ganglion should become a **visibility, brain scanning, backup, and memory optimisation companion** around that engine

## Short operating posture

- do not treat Ganglion as a competing memory system
- do not grow a parallel long-term memory runtime by default
- design around the existing lossless-claw integration
- prioritise operator visibility and safe tuning over broad middleware ambition
- keep earlier packet-spine and live-binding work as transitional prototype/reference material unless explicitly reused

## New first product target

The first meaningful Ganglion product is now:
- **inspectable operator tooling for lossless-claw**

That includes:
- session/agent memory visibility
- brain scan reports
- backup/export helpers
- tuning recommendations and optimisation workflows

## Current active/legacy split

- active refocus surface: repo root, `active/`, and updated docs/specs
- transitional prototype/reference surface: current packet-spine and live-binding code under `src/`, `scripts/`, and tests until reclassified
- archived legacy surface: `archive/legacy-pre-zero-base/`

## Evidence rule

No stage is complete without explicit operator-verifiable evidence.
