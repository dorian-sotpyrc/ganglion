# Legacy Implementation Inventory

Date: 2026-03-19
Status: archive/reference only

## Purpose

This inventory marks the pre-reset Ganglion implementation as legacy material.
It remains available for reference, but it is not the active base for the zero-base rebuild.

## Legacy surface retained in-place

Top-level legacy areas observed in the repository:

- `ganglion/`
  - large multi-module Python package surface
  - includes orchestrator, compiler, routing, provider abstraction, memory, metrics, tuning, artifacts, storage, and API layers
- `tests/`
  - multi-step test tree reflecting the prior staged build
- `scripts/`
  - helper entrypoints for harnesses, rendering, import, and API startup
- `migrations/`
  - schema scaffolding
- `artifacts/`
  - prior run, trace, deployment, and tuning artifacts
- `brains/`
  - prior brain/agent content layout
- `README.md`
  - documents the pre-reset architecture and completion narrative

## Legacy module families present

Within `ganglion/` the legacy package currently includes these families:

- `antennule`
- `axon`
- `carapace`
- `config`
- `cortex_api.py`
- `eyestalk`
- `forager`
- `mandible`
- `molt`
- `peduncle`
- `pleon`
- `shellbank`
- `storage`
- `supra`
- `tracer`
- `ventral`

## Reset interpretation

These areas are now treated as:
- reference for naming or idea extraction
- source material for contrast during design review
- non-authoritative for the new contracts

These areas are not treated as:
- the implementation baseline
- the required architecture for the rebuild
- proof that the new rebuild can skip the packet-spine evidence step

## Active rebuild root

The active zero-base rebuild root is:
- `zero-base/`

## Handling rule

Do not extend legacy modules as the default path for rebuild work.
If legacy material is consulted, extract the lesson into new zero-base documents or code instead of silently inheriting the old structure.
