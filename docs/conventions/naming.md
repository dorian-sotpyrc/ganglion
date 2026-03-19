# Naming Conventions

## Goals

Names must be:
- explicit
- stable
- sortable
- grep-friendly
- environment-safe
- human-readable

## Rules

- lowercase only for file and directory names
- use underscores for artifact filenames where needed
- use descriptive nouns, not vague abbreviations
- version labels must be explicit, e.g. `v1alpha1`, `v001`
- timestamps must sort lexically
- themed crustacean names must be paired with plain-language descriptions in docs

## Examples

Good:
- `openclaw_ingress.md`
- `ganglion_packet.md`
- `2026-03-19T01-54-02Z_trace_ab12cd34_run.json`

Avoid:
- `packet-final-new.md`
- `misc.md`
- `tmp2.json`
