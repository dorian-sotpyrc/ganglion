# Ganglion

Provider-agnostic brain, memory, routing, evaluation, and optimisation substrate for OpenClaw.

Ganglion sits **behind OpenClaw** and turns agents into durable, versioned working assets instead of oversized prompts. It assembles a structured runtime brain from stable brain sections, selected memory, current task context, and routing policy, then chooses an execution lane and provider/model path with confidentiality-aware controls.

---

## Status

**Current implemented state:** Step 1 through **Step 7A** complete.

Implemented now:
- project scaffold and storage foundation
- Carapace manifest + registry foundations
- Supra deterministic brain compilation
- Antennule request adaptation and integration contract
- Pleon orchestration and classifier
- Mandible response shaping
- Axon routing with confidentiality-aware lane selection
- Peduncle provider abstraction with fallback simulation
- Ventral critical + episodic memory selection
- Forager archive search
- Shellbank artifacts, export/import, retention
- Eyestalk metrics, failure pattern extraction, replay, cost tracking
- Molt tuning cycle and conservative change-set output
- Step 7A integration-ready hardening layer for mocked OpenClaw envelopes

Not yet fully complete:
- **Step 7B live OpenClaw runtime validation** in a real OpenClaw environment
- true provider APIs replacing the current mock provider adapter
- real database-backed persistence for memory / eval / deployment state
- full Alembic-backed schema evolution beyond scaffolding

---

## What Ganglion is

Ganglion is the architecture responsible for:
- structured brain packs
- deterministic brain compilation
- memory selection instead of memory dumping
- confidentiality-aware routing
- provider abstraction
- run capture and cost tracking
- evaluation and repeated-failure pattern extraction
- controlled tuning / self-improvement loops
- exportable and rollbackable brain assets

OpenClaw remains the operator-facing runtime and gateway layer.
Ganglion provides the intelligence substrate behind it.

---

## System view

```mermaid
flowchart LR
    U[User / Operator] --> C[OpenClaw Channel / Gateway]
    C --> A[Antennule\nRequest + envelope adaptation]
    A --> P[Pleon\nOrchestrator]
    P --> S[Supra\nBrain compiler]
    P --> V[Ventral\nMemory selection]
    P --> X[Axon\nRouting decision]
    X --> PD[Peduncle\nProvider abstraction]
    PD --> M[Model / Provider]
    M --> MN[Mandible\nResponse shaping]
    MN --> C

    P --> E[Eyestalk\nMetrics / evaluation]
    E --> MO[Molt\nTuning cycle]

    S --> CR[Carapace\nRegistry / deployment]
    V --> F[Forager\nArchive search]
    P --> SH[Shellbank\nArtifacts / exports]
```

---

## Runtime flow

```mermaid
sequenceDiagram
    participant User
    participant OpenClaw
    participant Antennule
    participant Pleon
    participant Supra
    participant Ventral
    participant Axon
    participant Peduncle
    participant Model
    participant Mandible
    participant Eyestalk
    participant Shellbank

    User->>OpenClaw: request
    OpenClaw->>Antennule: normalised envelope
    Antennule->>Pleon: RunRequest
    Pleon->>Supra: compile brain
    Pleon->>Ventral: select memory
    Pleon->>Axon: classify + route
    Axon->>Peduncle: provider/model decision
    Peduncle->>Model: invoke
    Model-->>Peduncle: response
    Peduncle-->>Pleon: provider result
    Pleon->>Mandible: shaped output
    Pleon->>Eyestalk: metrics + evaluation signals
    Pleon->>Shellbank: run artifact
    Mandible-->>OpenClaw: final response payload
    OpenClaw-->>User: response
```

---

## Brain architecture

A brain is not one prompt.

A Ganglion brain is a compiled runtime package built from four layers:

```mermaid
flowchart TD
    A[Core brain\nidentity / constraints / style / tool contract / memory policy]
    B[Operational brain\nSOPs / skills / templates / routing profile]
    C[Memory brain\ncritical memory / episodic memory / session summary]
    D[Runtime context\ncurrent task / envelope / requested overrides]
    E[Compiled runtime brain\nordered deterministic context package]

    A --> E
    B --> E
    C --> E
    D --> E
```

### Layer 1: Core brain
Stable low-change sections.

Includes:
- identity
- constraints
- style
- tool contract
- memory policy

### Layer 2: Operational brain
Reusable working modules.

Includes:
- SOPs
- skills
- routing profile
- templates later

### Layer 3: Memory brain
Selective durable knowledge.

Includes:
- critical memory
- episodic memory
- session summary

### Layer 4: Runtime context
Current execution context.

Includes:
- incoming task
- user / session / channel metadata
- requested model/provider/lane overrides
- risk hints

---

## Module map

### Antennule
Ingress adaptation layer.

Implemented:
- request adapter
- OpenClaw-style envelope normalisation
- integration-ready contract for Step 7A

Key files:
- `ganglion/antennule/request_adapter.py`
- `ganglion/antennule/openclaw_adapter.py`
- `ganglion/antennule/integration_contract.py`

### Pleon
Main orchestrator.

Implemented:
- runtime package assembly coordination
- classifier invocation
- memory selection invocation
- routing and provider selection invocation
- artifact writing
- cost estimation metadata

Key files:
- `ganglion/pleon/orchestrator.py`
- `ganglion/pleon/classifier.py`

### Supra
Brain compiler.

Implemented:
- deterministic core section ordering
- shared + agent overlay precedence
- stable checksum generation

Key files:
- `ganglion/supra/compiler.py`
- `ganglion/supra/selectors.py`

### Carapace
Registry, manifest handling, deployment record, rollback record.

Implemented:
- manifest loading and validation
- active brain lookup
- deployment record writing
- rollback record writing

Key files:
- `ganglion/carapace/manifests.py`
- `ganglion/carapace/registry.py`
- `ganglion/carapace/deployment.py`

### Ventral
Memory layer.

Implemented:
- critical memory selection
- episodic memory selection
- session summary compaction

Key files:
- `ganglion/ventral/service.py`

### Forager
Archive search.

Implemented:
- simple ranked text search over archive docs

Key files:
- `ganglion/forager/search.py`

### Axon
Routing engine.

Implemented:
- complexity / confidentiality / risk-aware lane choice
- user override handling for lane / provider / model
- policy rejection for unsafe confidential downgrades

Key files:
- `ganglion/axon/router.py`
- `ganglion/axon/routing_profiles.py`

### Peduncle
Provider abstraction.

Implemented:
- provider/model invocation interface
- fallback simulation path

Key files:
- `ganglion/peduncle/provider_adapter.py`

### Mandible
Response shaping.

Implemented:
- structured run response object generation

Key files:
- `ganglion/mandible/response_processor.py`

### Eyestalk
Evaluation and metrics.

Implemented:
- run metrics object
- failure pattern extraction
- replay metrics summary
- cost estimation scaffold

Key files:
- `ganglion/eyestalk/metrics.py`
- `ganglion/eyestalk/patterns.py`
- `ganglion/eyestalk/replay.py`
- `ganglion/eyestalk/service.py`
- `ganglion/eyestalk/costs.py`

### Molt
Controlled tuning loop.

Implemented:
- tuning schedule
- candidate generation
- conservative change-set output
- cycle artifact writing

Key files:
- `ganglion/molt/scheduler.py`
- `ganglion/molt/candidates.py`
- `ganglion/molt/experiments.py`
- `ganglion/molt/service.py`

### Shellbank
Artifacts and portability.

Implemented:
- object store foundation
- run artifact writing
- export/import utilities
- retention policy

Key files:
- `ganglion/shellbank/object_store.py`
- `ganglion/shellbank/artifacts.py`
- `ganglion/shellbank/exports.py`
- `ganglion/shellbank/retention.py`

---

## Current repository structure

```text
ganglion/
  README.md
  DEVELOPMENT.md
  pyproject.toml
  alembic.ini
  .env.example

  ganglion/
    antennule/
      request_adapter.py
      openclaw_adapter.py
      integration_contract.py
    pleon/
      classifier.py
      orchestrator.py
    supra/
      compiler.py
      selectors.py
    carapace/
      manifests.py
      registry.py
      deployment.py
    ventral/
      service.py
    forager/
      search.py
    axon/
      router.py
      routing_profiles.py
    peduncle/
      provider_adapter.py
      providers/
    mandible/
      response_processor.py
    eyestalk/
      metrics.py
      patterns.py
      replay.py
      service.py
      costs.py
    molt/
      scheduler.py
      candidates.py
      experiments.py
      service.py
    shellbank/
      object_store.py
      artifacts.py
      exports.py
      retention.py
    storage/
      db.py
      models.py
    config/
      settings.py

  brains/
    shared/
      core/
    agents/
      surgeon/
        manifest.json
        core/
        operations/
        routing/

  artifacts/
  migrations/
  scripts/
  tests/
```

---

## Confidentiality-aware routing

Ganglion currently auto-detects confidentiality from task text.

Examples of currently flagged indicators include terms like:
- confidential
- private
- secret
- token
- api key
- password
- credential
- proprietary
- internal only
- salary
- contract

Routing logic today:

```mermaid
flowchart TD
    A[Incoming task] --> B{Confidential?}
    B -- Yes --> C[private_strong lane]
    B -- No --> D{High complexity or high risk?}
    D -- Yes --> E[strong lane]
    D -- No --> F[cheap lane]

    C --> G[Provider/model mapping]
    E --> G
    F --> G
```

Current default lane mapping:
- `cheap` -> `openrouter / openrouter/auto`
- `strong` -> `openai-codex / gpt-5.4`
- `private_strong` -> `openai-codex / gpt-5.4`
- `fallback` -> `anthropic / claude-sonnet-4-6`

Current policy behaviour:
- user can request provider/model/lane
- confidential tasks can reject unsafe cheap overrides
- fallback route exists when primary path fails

---

## Installation

### Prerequisites
- Python 3.10+ currently works in practice
- Python 3.12+ was the original target in the early scaffold spec
- Git
- virtualenv support

### Clone

```bash
git clone git@github.com:dorian-sotpyrc/ganglion.git
cd ganglion
```

### Create environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e .
```

### Environment file

Create `.env` from the example:

```bash
cp .env.example .env
```

Example values:

```env
GANGLION_ENV=development
GANGLION_LOG_LEVEL=INFO
GANGLION_ARTIFACT_ROOT=./artifacts
GANGLION_DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/ganglion
```

### Verify base installation

```bash
source .venv/bin/activate
pytest -q
```

---

## OpenClaw integration model

Ganglion is designed to sit behind OpenClaw, not replace it.

### Responsibility split

| Layer | Responsibility |
|---|---|
| OpenClaw | channel ingress, operator workflows, tool runtime, external session management |
| Ganglion | brain assembly, memory selection, routing, evaluation, optimisation, exports |

### Integration seam today

Current Step 7A seam is the OpenClaw-style envelope handled by:
- `ganglion/antennule/integration_contract.py`
- `ganglion/antennule/openclaw_adapter.py`

Current envelope shape:

```json
{
  "request_id": "req-001",
  "agent_key": "surgeon",
  "session_id": "sess-001",
  "channel_type": "discord",
  "channel_id": "channel-001",
  "user_id": "user-001",
  "task_text": "Review this confidential service failure.",
  "session_messages": ["Earlier note 1", "Earlier note 2"],
  "requested_model": "gpt-5.4",
  "requested_provider": "openai-codex",
  "requested_lane": "private_strong",
  "risk_hint": "high",
  "metadata": {
    "source": "openclaw"
  }
}
```

### What OpenClaw should pass into Ganglion

OpenClaw should provide:
- agent key
- request id
- session id
- channel metadata
- user id
- current task text
- compact recent session messages
- optional requested provider/model/lane
- optional risk hints
- metadata tags

### What Ganglion returns

Ganglion returns:
- status
- request id
- agent key
- session id
- compiled checksum
- final response text
- execution metadata

Metadata currently includes:
- classification
- routing
- memory bundle summary
- estimated cost
- artifact path

---

## Configuring Ganglion for OpenClaw

### 1. Configure the Ganglion environment

Set at minimum:

```env
GANGLION_ENV=production
GANGLION_LOG_LEVEL=INFO
GANGLION_ARTIFACT_ROOT=/path/to/ganglion/artifacts
GANGLION_DATABASE_URL=postgresql+psycopg://user:pass@host:5432/ganglion
```

### 2. Decide provider policy

Current provider mappings live in code in `ganglion/axon/router.py`.

For now, review and adapt:
- cheap lane provider/model
- strong lane provider/model
- private_strong lane provider/model
- fallback provider/model

Current structure is easy to replace later with config-backed provider maps.

### 3. Decide confidentiality policy

Current patterns live in `ganglion/pleon/classifier.py`.

Tune these for your environment:
- keywords that indicate confidential work
- keywords that imply high complexity
- keywords that imply low complexity

### 4. Decide override policy

Current override policy lives in `ganglion/axon/routing_profiles.py`.

You can choose whether users/agents may override:
- lane
- provider
- model

### 5. Wire OpenClaw to Ganglion

At the OpenClaw side, the integration point should:
- build the envelope
- call Ganglion’s OpenClaw adapter
- receive the structured result
- send the result back through the OpenClaw channel runtime

Pseudo-flow:

```python
payload = {
    "request_id": request_id,
    "agent_key": agent_key,
    "session_id": session_id,
    "channel_type": channel_type,
    "channel_id": channel_id,
    "user_id": user_id,
    "task_text": user_message,
    "session_messages": recent_messages,
    "requested_model": maybe_model,
    "requested_provider": maybe_provider,
    "requested_lane": maybe_lane,
    "metadata": extra_metadata,
}

result = handle_openclaw_request(repo_root, payload)
```

### 6. Live OpenClaw validation later

When Step 7B begins, validate:
- real request shape compatibility
- real tool runtime compatibility
- real session metadata behaviour
- real provider invocation
- real failure handling and fallback behaviour

---

## Configuring individual agents

Each agent gets a brain pack under:

```text
brains/agents/<agent_key>/
```

### Minimum files for an agent brain

```text
brains/agents/surgeon/
  manifest.json
  core/
    identity.md
    style.md
  operations/
    sops/
    skills/
  routing/
    routing_profile.json
```

### Shared brain

Shared defaults live under:

```text
brains/shared/core/
```

These act as fallback sections when the agent-specific section does not exist.

### Overlay precedence

Agent-specific core wins over shared core.

Example:
- `brains/agents/surgeon/core/style.md` overrides
- `brains/shared/core/style.md`

### Example manifest

```json
{
  "schema_version": "1.0",
  "agent_key": "surgeon",
  "brain_key": "surgeon-core",
  "version": "0.1.0",
  "extends": "shared",
  "status": "active"
}
```

### Example agent setup process

1. Create agent folder
2. Add `manifest.json`
3. Add core files
4. Add SOPs and skills
5. Add routing profile
6. Run tests / compile the brain
7. Record deployment metadata

---

## Running the local integration harness

Use the Step 7A harness:

```bash
source .venv/bin/activate
python -m scripts.run_integration_harness
```

This simulates a production-like OpenClaw request envelope without requiring a live OpenClaw runtime.

---

## Export / import / rollback

### Export an agent brain

```python
from pathlib import Path
from ganglion.shellbank.exports import BrainExportService

svc = BrainExportService()
svc.export_brain("surgeon", Path("brains/agents/surgeon"))
```

### Import an exported brain

```python
svc.import_brain(
    "artifacts/exports/surgeon",
    "artifacts/integration/surgeon_import_verify",
)
```

### Record active deployment

```python
from ganglion.carapace.deployment import DeploymentManager
mgr = DeploymentManager()
mgr.record_deployment("surgeon", "v1", "checksum123")
```

### Record rollback target

```python
mgr.rollback("surgeon", "v0", "checksum-old")
```

---

## Testing

### Run all tests

```bash
source .venv/bin/activate
pytest -q
```

### Run by phase

```bash
pytest tests/smoke -q
pytest tests/step2 -q
pytest tests/step3 -q
pytest tests/step4 -q
pytest tests/step5 -q
pytest tests/step6 -q
pytest tests/step7a -q
```

### What the tests currently verify

- manifest validation
- deterministic compile output
- request adaptation
- mocked end-to-end run path
- confidentiality-aware routing
- provider fallback handling
- memory selection
- archive search
- artifact writing
- evaluation and tuning outputs
- export/import roundtrip
- rollback record writing
- retention policy execution

---

## Actual implementation differences from the original design

The original design was intentionally broader and more database-heavy. The actual build so far is more pragmatic and implementation-first.

### 1. Storage is lighter than originally envisioned
Original direction:
- stronger early dependence on Postgres-backed state
- richer repository/data model early

Actual implementation:
- filesystem and JSON artifacts are doing most of the real work today
- SQLAlchemy/Alembic scaffold exists, but the live architecture is currently file-first

Why:
- faster proof of value
- lower implementation friction
- easier iterative development on VPS

### 2. Memory is currently in-memory seed data, not persisted state
Original direction:
- structured memory tables / metadata store

Actual implementation:
- `MemoryService` currently contains seeded critical and episodic memory in code
- selection logic works, but persistence is still future work

Why:
- allows end-to-end architecture validation before heavier persistence work

### 3. Provider invocation is mocked, not live
Original direction:
- provider abstraction over real models/providers

Actual implementation:
- Peduncle returns mocked primary/fallback results
- enough to validate routing architecture and metadata flow

Why:
- isolates architecture work from provider/API volatility

### 4. Routing is code-configured, not environment-configured yet
Original direction:
- routing profiles plus provider abstraction

Actual implementation:
- lane-to-provider/model mapping is hardcoded in `axon/router.py`
- routing profiles are present, but provider config centralisation is still pending

Why:
- simpler Step 4 proof path

### 5. Step 7 was split in practice into 7A and later 7B
Original direction:
- one Step 7 integration + hardening phase

Actual implementation:
- **7A** = integration-ready hardening without real OpenClaw runtime
- **7B** = future live OpenClaw validation

Why:
- avoids blocking the project on live environment availability

### 6. Classification gained confidentiality-aware routing earlier than the original step text implied
Original direction:
- basic task classification

Actual implementation:
- confidentiality auto-detection and policy-aware routing are already in place
- explicit model/provider/lane override support is already in place

Why:
- this was a direct design requirement for safe model selection

---

## Roadmap from here

### Next immediate phase: Step 7B
- live OpenClaw runtime validation
- actual request/response integration
- real provider calls
- real session/tool runtime compatibility

### Next strengthening phase after 7B
- database-backed persistence for deployment state, eval state, and memory state
- config-driven provider mapping
- real retention scheduling
- richer replay datasets
- stronger confidential routing policy controls

---

## Project philosophy

Ganglion is not a prompt file.
It is a **versioned nervous system** for OpenClaw agents.

The value is not just in generating responses. The value is in building:
- durable brain assets
- auditable routing decisions
- selective memory
- controllable optimisation
- provider portability
- repeatable integration behind OpenClaw

---

# Traceability and brain performance visibility

Ganglion now supports a fuller observable execution path so you can inspect:

```text
IN → detailed process step results → OUT
```

This extends the existing architecture without replacing the earlier design.

## Step-level trace flow

```mermaid
flowchart TD
    A[Request In] --> B[Antennule: envelope normalisation]
    B --> C[Pleon: orchestrator start]
    C --> D[Supra: brain compile]
    D --> E[Ventral: memory selection]
    E --> F[Axon: classification + routing]
    F --> G[Peduncle: provider/model resolution]
    G --> H[Costing + artifact capture]
    H --> I[Mandible: response shaping]
    I --> J[Response Out]
```

## What is captured per run

A run can now expose and persist:

- request envelope summary
- compiled brain checksum
- classification result
- selected memory counts
- session summary used
- routing decision
- provider/model chosen
- fallback usage
- estimated tokens, cost, and latency
- final output summary
- run artifact path
- trace artifact path

## Trace artifact design

Trace artifacts are written as structured JSON under:

```text
artifacts/traces/
```

Each trace contains:

- `input_summary`
- ordered `steps`
- `output_summary`

Typical step keys include:

1. `brain_compile`
2. `classification`
3. `memory_selection`
4. `routing`
5. `costing`
6. `artifact_capture`

## Brain performance summary

Ganglion can now generate a per-brain summary from run artifacts.

Current output location:

```text
artifacts/brain_metrics/brain_performance_summary.json
```

Current visible metrics include:

- `total_runs`
- `fallback_runs`
- `fallback_rate`
- `confidential_runs`
- `confidential_rate`
- `estimated_total_cost_usd`
- `average_latency_ms`
- `average_episodic_memories_selected`
- `average_critical_memories_selected`

## Why this matters

This gives Ganglion a visible operating loop:

```text
request
  -> compiled brain
  -> step-by-step execution record
  -> output
  -> accumulated brain metrics
  -> tuning visibility
```

That makes it easier to:
- inspect how a brain is behaving
- compare brains over time
- see whether routing policy is helping or hurting
- see where confidential tasks are flowing
- see whether fallback frequency is improving
- prepare future dashboard or Clawboard visualisation

## Current implementation shape

This was added pragmatically on top of the existing design:

- traceability is file/artifact first
- brain-performance reporting aggregates from run artifacts
- the design is integration-ready and auditable before live dashboard work

## Recommended test commands

```bash
cd ~/ganglion
source .venv/bin/activate
pytest tests/step8 -q
python -m scripts.run_integration_harness
python - <<'PY'
from ganglion.eyestalk.brain_metrics import BrainMetricsService
print(BrainMetricsService().write_summary())
PY
```

## Recommended GitHub push commands

```bash
cd ~/ganglion
git add .
git commit -m "Add traceability and brain performance visibility updates"
git push
```
