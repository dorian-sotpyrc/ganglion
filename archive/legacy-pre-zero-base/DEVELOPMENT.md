# DEVELOPMENT.md

Development plan and implementation tracker for Ganglion.

This document now serves two purposes:
- original build plan
- current implementation tracker with deviations noted clearly

---

## Build philosophy

Build Ganglion as one Python application with clear module boundaries first.

Do not start with:
- microservices
- embeddings-first architecture
- uncontrolled self-editing
- overcomplicated event buses
- heavy infrastructure before core value is proven

Start with:
- strong module boundaries
- brain packs on disk
- deterministic assembly
- conservative routing
- auditable evaluation
- progressive hardening

---

## Project goals during development

The development process should preserve these outcomes:

- provider neutrality
- small runtime contexts
- exportable brain assets
- clean OpenClaw integration
- measurable cost reduction
- safe self-improvement

---

## Development tracker

Legend:
- [x] completed
- [~] partially completed / scaffolded
- [ ] not yet complete

---

## Step 1: Scaffold the project and storage layer

**Status:** [x] Completed

### Original target
- repository skeleton
- Python package structure
- config loader
- logging setup
- Postgres connection
- migration framework
- filesystem artifact root
- minimal test harness

### Implemented
- `ganglion/config/settings.py`
- `ganglion/storage/db.py`
- `ganglion/storage/models.py`
- `ganglion/shellbank/object_store.py`
- `pyproject.toml`
- `alembic.ini`
- migration environment scaffold
- smoke tests

### Tests achieved
- imports succeed
- configuration loads from environment
- DB engine can be created
- migration scaffold exists
- object store write/read works
- pytest smoke passed

### Definition of done result
- [x] `pytest` passes basic smoke tests
- [x] `alembic` scaffold exists and is usable
- [x] local artifact root is writable

### Actual implementation notes vs original design
- DB layer is scaffolded but real persisted application state is not yet database-backed
- Python 3.10 was used successfully in practice even though early scaffold text targeted 3.12+

---

## Step 2: Build Carapace and Supra foundations

**Status:** [x] Completed

### Original target
- brain manifest schema
- brain pack loader
- active version lookup
- deterministic section compiler
- core section ordering rules

### Implemented
- `ganglion/carapace/manifests.py`
- `ganglion/carapace/registry.py`
- `ganglion/supra/compiler.py`
- `ganglion/supra/selectors.py`
- sample shared brain
- sample `surgeon` brain

### Tests achieved
- shared brain pack loads
- agent-specific brain pack loads
- overlay precedence is deterministic
- invalid manifest fails clearly
- compiled checksum is stable

### Definition of done result
- [x] one agent brain can be compiled from disk
- [x] output is reproducible
- [~] brain version metadata is stored and retrievable through manifest/registry, but not yet in a DB-backed deployment registry at this stage

### Actual implementation notes vs original design
- versioning is manifest-driven and filesystem-based rather than DB-driven
- shared and agent overlays were proven early with the `surgeon` example brain

---

## Step 3: Build Antennule, Pleon, and Mandible runtime path

**Status:** [x] Completed

### Original target
- OpenClaw request adapter
- internal run request schema
- orchestrator
- response processor
- minimal end-to-end run flow without real model call

### Implemented
- `ganglion/antennule/request_adapter.py`
- `ganglion/antennule/openclaw_adapter.py`
- `ganglion/pleon/orchestrator.py`
- `ganglion/mandible/response_processor.py`

### Tests achieved
- mock OpenClaw request enters Ganglion
- orchestrator resolves active brain
- compiled runtime package is produced
- response object maps back correctly

### Definition of done result
- [x] mocked OpenClaw request passes end to end

### Actual implementation notes vs original design
- runtime path stayed intentionally mocked at provider execution level
- this preserved architectural momentum without waiting for live provider hookup

---

## Step 4: Build Axon and Peduncle routing layer

**Status:** [x] Completed

### Original target
- task classification
- route profiles
- cheap-vs-strong lane selector
- provider abstraction interface
- fallback policy

### Implemented
- `ganglion/pleon/classifier.py`
- `ganglion/axon/router.py`
- `ganglion/axon/routing_profiles.py`
- `ganglion/peduncle/provider_adapter.py`

### Additional implemented behaviour beyond original baseline
- confidentiality auto-detection
- confidentiality-aware route escalation
- user-requested lane/provider/model overrides
- rejection of unsafe cheap overrides for confidential work

### Tests achieved
- low-risk tasks route to cheap lane
- high-complexity tasks route to strong lane
- confidential tasks route to private strong lane
- user model/provider override applies when allowed
- unsafe confidential downgrade is rejected
- simulated fallback path works

### Definition of done result
- [x] routing decisions are deterministic for test fixtures
- [x] provider calls are abstracted behind Peduncle

### Actual implementation notes vs original design
- provider mapping is currently hardcoded in router logic rather than external config
- confidentiality-aware selection arrived earlier and stronger than the original generic step description

---

## Step 5: Build Ventral, Forager, and Shellbank evidence flow

**Status:** [x] Completed

### Original target
- memory metadata schema
- critical memory selector
- episodic memory selector
- archive search using FTS
- run capture and artifact storage
- session summary compaction

### Implemented
- `ganglion/ventral/service.py`
- `ganglion/forager/search.py`
- `ganglion/shellbank/artifacts.py`
- orchestrator integration for memory bundle and artifact writing

### Tests achieved
- critical memory loads
- relevant episodic memory selected
- session summary compacts correctly
- archive search returns results
- run artifact written correctly

### Definition of done result
- [x] runtime assembly can include selected memory
- [x] artifacts are captured for runs

### Actual implementation notes vs original design
- memory currently uses seeded in-code items, not DB persistence
- search is simple text search rather than true Postgres FTS yet
- despite this, the architectural interfaces are in place and working

---

## Step 6: Build Eyestalk and Molt controlled optimisation

**Status:** [x] Completed

### Original target
- run metrics
- evaluation records
- repeated failure pattern extraction
- tuning schedule
- candidate generation
- replay harness
- conservative change-set output

### Implemented
- `ganglion/eyestalk/metrics.py`
- `ganglion/eyestalk/patterns.py`
- `ganglion/eyestalk/replay.py`
- `ganglion/eyestalk/service.py`
- `ganglion/molt/scheduler.py`
- `ganglion/molt/candidates.py`
- `ganglion/molt/experiments.py`
- `ganglion/molt/service.py`

### Tests achieved
- failure patterns detected
- replay summary generated
- candidates generated
- tuning cycle writes artifact output

### Definition of done result
- [x] Molt can run a scheduled cycle on fixture data
- [x] outputs are conservative and auditable

### Actual implementation notes vs original design
- tuning remains artifact-driven and conservative
- no auto-deploy behaviour was introduced
- this matches the intended safety direction well

---

## Step 7: Integrate with real OpenClaw flow and harden

This step was split into two parts in practice.

### Step 7A: Integration-ready hardening without live OpenClaw

**Status:** [x] Completed

#### Original step elements targeted in 7A
- stronger integration path in Antennule
- retention policy
- export/import commands
- rollback support
- regression fixture suite
- performance and cost tracking scaffolding

#### Implemented
- `ganglion/antennule/integration_contract.py`
- upgraded `ganglion/antennule/openclaw_adapter.py`
- `ganglion/carapace/deployment.py`
- `ganglion/shellbank/exports.py`
- `ganglion/shellbank/retention.py`
- `ganglion/eyestalk/costs.py`
- integration harness script
- Step 7A regression fixtures and tests

#### Tests achieved
- envelope normalisation works
- integration harness runs
- export/import roundtrip works
- deployment record and rollback record work
- retention policy runs
- cost estimate scaffold works
- Step 7A pytest passes

#### Definition of done result
- [x] integration-ready path exists
- [x] export/import exists
- [x] rollback support exists
- [x] retention policy exists
- [x] regression harness exists
- [x] cost/performance tracking scaffold exists

#### Actual implementation notes vs original design
- this is **integration-ready**, not **live OpenClaw validated** yet
- the harness uses a production-like mocked envelope rather than a live OpenClaw runtime

### Step 7B: Live OpenClaw runtime validation

**Status:** [ ] Not yet complete

#### Still required to fully close Step 7
- real OpenClaw ingress compatibility testing
- real tool/runtime handoff testing
- real provider execution under OpenClaw control
- real session/channel metadata verification
- production-like regression against live environment behaviour

---

## Suggested file creation order actually used

The implementation broadly followed the intended phased order, but in practice the work grouped around working vertical slices:

1. scaffold / settings / db / object store
2. manifest / registry / compiler
3. request / orchestrator / response
4. classifier / routing / provider abstraction
5. memory / search / artifact capture
6. evaluation / tuning
7. integration contract / export / rollback / retention / cost tracking

This was a good implementation approach because each stage delivered a testable working layer.

---

## Current completion summary

### Core architecture
- [x] scaffold
- [x] compiler
- [x] runtime path
- [x] routing
- [x] memory selection
- [x] evaluation and tuning
- [x] integration-ready hardening
- [ ] live OpenClaw runtime validation

### Brain assets
- [x] shared brain
- [x] surgeon agent brain
- [ ] broader agent pack library

### Persistence
- [x] filesystem artifacts
- [~] DB scaffold only
- [ ] full DB-backed runtime state

### Provider integration
- [x] abstraction interface
- [x] simulated fallback behaviour
- [ ] live provider APIs

### Testing
- [x] smoke tests
- [x] step-by-step regression tests through 7A
- [ ] live environment regression with real OpenClaw runtime

---

## Actual implementation changes compared to original design

### Change 1: file-first implementation instead of database-first implementation
Reason:
- faster end-to-end progress
- easier debugging on VPS
- less friction while architecture was still changing

Impact:
- many artefacts and state transitions are JSON/file-backed today
- future work should migrate selected state into DB where it adds real value

### Change 2: confidentiality-aware routing added as a first-class concern early
Reason:
- explicit requirement for model/provider choice based on sensitivity

Impact:
- routing architecture is already stronger and more realistic than the original minimal router brief

### Change 3: Step 7 split into 7A and 7B
Reason:
- no live OpenClaw environment was required to continue building value

Impact:
- architecture is integration-ready now
- final runtime validation remains a clearly bounded future task

### Change 4: provider layer remains mock-first
Reason:
- allowed safe validation of routing, metadata flow, and fallback semantics without external dependency noise

Impact:
- next provider integration step should preserve the current Peduncle interface rather than redesigning it

### Change 5: memory remains seeded and selection-driven, not persistent yet
Reason:
- validates memory interfaces and orchestration before committing to a storage design

Impact:
- future persistent memory work can be done behind existing Ventral interfaces

---

## Recommended next work after 7A

### Priority 1: Step 7B live OpenClaw validation
- wire Ganglion behind real OpenClaw entrypoints
- validate request shape and response shape against real runtime
- validate tool runtime expectations
- validate real provider execution path

### Priority 2: externalise config
- provider/model mapping
- confidentiality policies
- lane policy
- override permissions

### Priority 3: move selected state into persistent storage
- deployment state
- memory state
- eval state
- tuning cycle history

### Priority 4: expand agent library
- builder brain
- analyst brain
- more OpenClaw-specialised brains

---

## Non-negotiable safety controls

Still keep these rules:
- do not auto-deploy tuning changes without approval
- do not let tuning change identity/trust boundaries automatically
- do not allow unsafe cheap routing for confidential tasks
- do not let provider overrides bypass policy

---

## Success definition now

Ganglion has already succeeded at the architecture proof stage when:
- brains are compiled deterministically
- memory is selected instead of dumped
- confidentiality influences routing
- provider choice is abstracted
- evidence is captured
- tuning outputs are auditable
- OpenClaw integration seam is real and testable

Ganglion will fully succeed at the runtime integration stage when:
- it is proven behind live OpenClaw workflows
- it can execute through real providers safely
- its persisted state model is hardened

---

## Step 8: Traceability and per-brain performance visibility

**Status:** [x] Completed

### Scope added
- full request-to-output trace capture
- ordered internal process step recording
- trace artifact writing
- per-brain performance summary generation
- cost / latency rollup visibility
- memory-selection visibility

### Implemented
- `ganglion/tracer/models.py`
- `ganglion/tracer/service.py`
- `ganglion/eyestalk/brain_metrics.py`
- orchestrator patch for trace writing and richer run payloads
- Step 8 regression tests

### Tests achieved
- trace file is written
- trace contains step-level details
- brain metrics summary file is written
- brain metrics contains expected fields

### Definition of done result
- [x] run can be traced from input to output
- [x] internal process step results are visible
- [x] per-brain performance summary can be generated from artifacts

### Actual implementation notes vs original design
- traceability was added as a dedicated runtime concern rather than being buried only in general artifacts
- brain-performance reporting is currently file/artifact based, not DB-first
- performance visibility aggregates from `artifacts/runs`
- this extends the original design cleanly rather than replacing earlier structure

### Practical value now available
Ganglion can now show:
- what came in
- what happened inside
- what came out
- how a given brain is performing over multiple runs

This creates the basis for future dashboard visualisation and stronger learning/performance comparison.

---

## Step 8B: Strict OpenClaw profile + Cortex API

**Status:** [x] Completed

### Scope added
- strict OpenClaw integration profile enforcement
- canonical artifact/state naming helpers
- Cortex API for read-only brain performance visibility
- actual metric ingestion when integrations provide real tokens/cost/latency

### Implemented
- `ganglion/openclaw_profile.py`
- strict envelope enforcement in `ganglion/antennule/integration_contract.py`
- actual-metric passthrough in `ganglion/pleon/orchestrator.py`
- Cortex metrics service in `ganglion/cortex_api.py`
- Cortex HTTP runner in `scripts/run_cortex_api.py`
- tests in `tests/step8/test_cortex_api.py`

### Practical purpose
This closes another operational gap:
- OpenClaw integrations are validated more strictly
- state/trace naming is more standardized and grep-friendly
- dashboards can query a stable brain-performance surface instead of scraping raw artifacts
- cost/latency metrics can move from estimated to actual when supplied by the integration

---

## Step 8A: Legacy OpenClaw state import for pilot canaries

**Status:** [x] Completed

### Scope added
- file-backed imported memory bundles for existing OpenClaw agents
- additive import utility for workspace memory, legacy agent memory, and session transcript seeds
- generic live-binding renderer support for agent pilots

### Implemented
- imported-state loading in `ganglion/ventral/service.py`
- import utility `scripts/import_openclaw_agent_state.py`
- live-binding renderer `scripts/render_live_binding.py`
- imported-state tests in `tests/step8/test_imported_state.py`

### Practical purpose
This closes a real pilot gap:
- existing OpenClaw agents do not need to start cold inside Ganglion
- legacy memory and session continuity can be carried into shadow-mode canaries
- migration remains additive and auditable rather than mutating original OpenClaw state
- a live pilot can inject Ganglion-built agent context into OpenClaw turn generation without replacing the whole channel runtime
- environment-specific agent definitions remain local to the deployment, not in the shared repo
