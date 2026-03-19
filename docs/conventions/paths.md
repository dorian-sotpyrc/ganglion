# Path Conventions

## Active repo areas

- `docs/contracts/` — written interface contracts
- `docs/conventions/` — naming, paths, trace rules, component glossary
- `docs/examples/` — worked examples and contract fixtures in document form
- `src/ganglion/` — future implementation root
- `tests/contracts/` — contract validation tests
- `tests/fixtures/` — reusable fixtures for contract and integration tests
- `runtime/evidence/` — per-run evidence artifacts
- `runtime/traces/` — structured trace logs
- `runtime/samples/` — sample packets and outputs
- `brains/` — future brain assets
- `exports/` — future export bundles
- `archive/legacy-pre-zero-base/` — archived pre-reset implementation

## Rules

- implementation files should not be introduced outside `src/` without strong reason
- runtime-generated files belong under `runtime/`
- operator-facing written guidance belongs under `docs/`
- archived material must remain under `archive/`
