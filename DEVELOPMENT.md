# DEVELOPMENT.md

Development plan for Ganglion.

This document explains how to build Ganglion in a practical order, how to test it, and how to keep the architecture disciplined while integrating it behind OpenClaw.

## Build philosophy

Build Ganglion as one Python application with clean modules first.

Do not start with:
- microservices
- embeddings-first architecture
- unrestricted self-editing
- overcomplicated event buses
- heavy infrastructure before the first useful run works

Start with:
- a strong module boundary
- brain packs on disk
- Postgres for structured truth
- filesystem artifacts
- deterministic assembly
- conservative routing
- auditable run capture

## Project goals during development

The development process should preserve these outcomes:

- provider neutrality
- small runtime contexts
- exportable brain assets
- good OpenClaw integration
- measurable cost reduction
- safe self-improvement

## Recommended 7-step build and test plan

### Step 1: Scaffold the project and storage layer

Build:
- repository skeleton
- Python package structure
- config loader
- logging setup
- Postgres connection
- migration framework
- filesystem artifact root
- minimal test harness

Implement first:
- `ganglion/config/settings.py`
- `ganglion/storage/db.py`
- `ganglion/storage/models.py`
- `ganglion/shellbank/object_store.py`

Tests:
- imports succeed
- configuration loads from environment
- database connects
- migrations run
- object storage can write and read a file

Definition of done:
- `pytest` passes basic smoke tests
- `alembic upgrade head` works
- local artifact root is writable

### Step 2: Build Carapace and Supra foundations

Build:
- brain manifest schema
- brain pack loader
- active version lookup
- deterministic section compiler
- core section ordering rules

Implement first:
- `ganglion/carapace/manifests.py`
- `ganglion/carapace/registry.py`
- `ganglion/supra/compiler.py`
- `ganglion/supra/selectors.py`

Tests:
- shared brain pack loads
- agent-specific brain pack loads
- overlay precedence works deterministically
- missing/invalid manifests fail clearly
- compiled result checksum is stable

Definition of done:
- one agent brain can be compiled from disk
- output is reproducible
- brain version metadata is stored and retrievable

### Step 3: Build Antennule, Pleon, and Mandible runtime path

Build:
- OpenClaw request adapter
- internal run request schema
- orchestrator
- response processor
- minimal end-to-end run flow without real model call

Implement first:
- `ganglion/antennule/request_adapter.py`
- `ganglion/antennule/openclaw_adapter.py`
- `ganglion/pleon/orchestrator.py`
- `ganglion/mandible/response_processor.py`

Tests:
- mock OpenClaw request enters Ganglion
- orchestrator resolves active brain
- compiled runtime package is produced
- response object is mapped back correctly

Definition of done:
- a mocked OpenClaw request can pass through Ganglion end to end

### Step 4: Build Axon and Peduncle routing layer

Build:
- task classification
- route profiles
- cheap-vs-strong lane selector
- provider abstraction interface
- fallback policy

Implement first:
- `ganglion/pleon/classifier.py`
- `ganglion/axon/router.py`
- `ganglion/axon/routing_profiles.py`
- `ganglion/peduncle/provider_adapter.py`

Tests:
- low-risk routine fixtures route to cheap tier
- high-risk or high-complexity fixtures route to strong tier
- fallback on simulated provider failure works
- provider abstraction can be swapped without changing orchestration logic

Definition of done:
- routing decisions are deterministic for test fixtures
- provider calls are abstracted behind Peduncle

### Step 5: Build Ventral, Forager, and Shellbank evidence flow

Build:
- memory metadata schema
- critical memory selector
- episodic memory selector
- archive search using FTS
- run capture and artifact storage
- session summary compaction

Implement first:
- `ganglion/ventral/service.py`
- `ganglion/ventral/selectors.py`
- `ganglion/forager/search.py`
- `ganglion/shellbank/artifacts.py`

Tests:
- critical memory loads when relevant
- irrelevant memory is excluded
- archive search returns ranked results
- run artifacts are written correctly
- compact session summary stays within budget

Definition of done:
- runtime assembly can include selected memory and capture artifacts

### Step 6: Build Eyestalk and Molt controlled optimisation

Build:
- run metrics
- evaluation records
- repeated failure pattern extraction
- tuning schedule
- candidate generation
- replay harness
- conservative change-set output

Implement first:
- `ganglion/eyestalk/service.py`
- `ganglion/eyestalk/metrics.py`
- `ganglion/eyestalk/patterns.py`
- `ganglion/molt/scheduler.py`
- `ganglion/molt/service.py`

Tests:
- repeated bad runs create detectable patterns
- tuning cycle runs on fixture data
- candidate improvements are generated
- candidate improvements do not auto-deploy without rule checks

Definition of done:
- Molt can run a scheduled cycle and produce auditable outputs

### Step 7: Integrate with real OpenClaw flow and harden

Build:
- real OpenClaw hook integration
- retention policy
- export/import commands
- rollback support
- regression fixture suite
- performance and cost tracking

Implement:
- real integration path in Antennule
- real deployment controls in Carapace
- export utilities in Shellbank

Tests:
- live integration smoke test
- multiple agent brain regression suite
- export/import round trip
- cheap-tier success benchmark
- strong-tier escalation benchmark
- rollback test

Definition of done:
- Ganglion works behind OpenClaw in a production-like flow
- brain assets can be exported and restored
- routing and assembly behaviour are measurable

## Daily development rules

Keep these rules during implementation:

1. Every module must have a clear boundary.
2. Brain assets stay in Markdown/JSON, not hidden in code.
3. Provider-specific behaviour must stay inside Peduncle.
4. Prompt budgets must be enforced inside Supra.
5. Memory writes must be explicit and scored inside Ventral.
6. Tuning must be auditable inside Molt.
7. Deployment state must be versioned in Carapace.

## Recommended initial database groups

### Brain and registry
- agents
- brain_versions
- brain_sections
- routing_profiles
- deployments

### Memory
- memory_items
- memory_links
- memory_access_log
- memory_candidates

### Runtime
- sessions
- runs
- run_outputs
- tool_calls

### Evaluation and tuning
- feedback_events
- evaluation_runs
- evaluation_metrics
- failure_patterns
- tuning_schedules
- tuning_cycles
- change_sets

## Suggested file creation order

Create files in this order:

1. `pyproject.toml`
2. `ganglion/config/settings.py`
3. `ganglion/storage/db.py`
4. `ganglion/storage/models.py`
5. `ganglion/carapace/manifests.py`
6. `ganglion/carapace/registry.py`
7. `ganglion/supra/compiler.py`
8. `ganglion/supra/assembler.py`
9. `ganglion/antennule/request_adapter.py`
10. `ganglion/pleon/orchestrator.py`
11. `ganglion/axon/router.py`
12. `ganglion/peduncle/provider_adapter.py`
13. `ganglion/ventral/service.py`
14. `ganglion/mandible/response_processor.py`
15. `ganglion/eyestalk/service.py`
16. `ganglion/molt/service.py`

## Suggested first brain packs

Create three initial brains:

### 1. Surgeon brain
Purpose:
- high-risk system changes
- verification-heavy technical work

### 2. Builder brain
Purpose:
- implementation planning
- scaffold creation
- system integration work

### 3. Analyst brain
Purpose:
- reports
- architecture summaries
- research-backed outputs

Each should contain:
- identity.md
- constraints.md
- style.md
- tool_contract.md
- memory_policy.md
- at least 3 SOPs
- at least 3 skills
- one routing profile

## Testing strategy

### Unit tests
Cover:
- manifest validation
- section ordering
- routing decisions
- memory selection
- response processing
- scoring logic

### Integration tests
Cover:
- OpenClaw request adaptation
- end-to-end assembly path
- provider abstraction behaviour
- artifact writing
- tuning cycle flow

### Regression tests
Use fixed fixtures for:
- compiled brain checksums
- route decisions
- memory inclusion/exclusion
- replay scores
- export/import round trips

## Non-negotiable safety controls

Do not allow automatic tuning to change without approval:
- safety rules
- destructive permissions
- identity and trust boundaries
- tool access scope

Do allow controlled tuning of:
- ranking weights
- retrieval thresholds
- compaction thresholds
- SOP ordering
- cheap-vs-strong routing thresholds

## First production target

The first production target is not “full self-learning”.

The first production target is:

- OpenClaw can call Ganglion
- Ganglion assembles a structured brain
- Ganglion selects memory selectively
- Ganglion routes cost-effectively
- Ganglion records enough evidence to improve later

That is the correct base.

## Definition of project success

Ganglion is successful when:
- brains become reusable assets rather than ad hoc prompts
- agent runtime cost becomes measurable and optimisable
- task-specific brains improve quality and consistency
- OpenClaw integration stays clean
- new providers can be added without rewriting the system
- the system learns through controlled evidence, not chaos
