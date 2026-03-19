# Ganglion Zero-Base Rebuild Brief
## Ground-up strategic reset and staged execution plan

**Owner:** Sam  
**Primary implementation lead:** Declan  
**Project:** Ganglion  
**Status:** Full reset approved  
**Build posture:** Zero-base rebuild from nothing

---

# 1. Executive directive

Ganglion is to be restarted from absolute zero.

This is not a refactor.  
This is not a salvage exercise.  
This is not a continuation of the prior implementation.  
This is not a staged recovery of partially working code.

Treat Ganglion as though **no valid implementation currently exists**.

The previous repository state, experiments, integrations, and runtime attempts are to be preserved only as **archived historical reference**. They are not to be used as the active implementation base.

The new Ganglion must be built from first principles around a smaller, more disciplined, more testable strategic direction.

The old attempt moved too far too fast and introduced too much complexity before the core runtime path was proven. The new approach is to build a narrow, deterministic, evidence-first runtime spine and then layer capability onto it in controlled stages.

---

# 2. Strategic reset intent

The purpose of this reset is to re-establish Ganglion as a system that is:

- small at the start
- operationally honest
- deterministic
- easy to inspect
- easy to test
- easy to extend
- safe to evolve
- aligned with long-term goals without prematurely implementing them

Ganglion must still retain its identity, intelligence model, and clever crustacean naming architecture. That naming is a feature, not a gimmick. It should remain part of the design language of the project.

However, each named component must also map to a clear engineering responsibility, so that the system remains understandable to operators and contributors.

---

# 3. Strategic principles

## 3.1 Start with the smallest real success
The first meaningful win is not a dashboard, memory layer, analytics system, or self-learning loop.

The first meaningful win is:

`User -> OpenClaw -> Ganglion -> API/provider -> Ganglion -> OpenClaw -> User`

That path must work end to end, be observable, be reproducible, and be auditable.

## 3.2 Build vertical slices, not broad systems
Each stage should produce a complete, testable operational capability.

## 3.3 Evidence before claims
No stage is complete until there is operator-verifiable evidence.

## 3.4 Design for the long term from day one
Even early stages must use interfaces, file structure, and naming that will support future capabilities cleanly.

## 3.5 Preserve Ganglion’s intelligence identity
Ganglion should keep its “crustacean nervous system” architecture style. Component names can remain clever and thematic, but they must also have plain-language definitions.

## 3.6 Determinism before sophistication
Before adding memory, tuning, routing intelligence, or self-learning, prove stable packet handling and runtime flow.

---

# 4. Long-term end goals

These remain the intended long-term capabilities of Ganglion and should inform design decisions from the beginning.

## 4.1 Brain portability
Ganglion brains must be importable and exportable as portable, inspectable, versionable assets.

## 4.2 Standardized filesystem layout
Ganglion must use strict naming and predictable structure for:

- bootstrap files
- brain definitions
- memory layers
- evidence artifacts
- cost traces
- tuning records
- performance records
- import/export bundles
- packet captures
- operator-readable logs

## 4.3 Self-learning and compaction tuning
Ganglion should eventually support a supervised improvement loop that:

- reviews outcomes
- compacts learnings
- tunes brain components
- preserves rollback safety
- prevents uncontrolled drift

## 4.4 Local deep memory search
Ganglion should eventually support deterministic local retrieval across memory layers with inspectable recall behaviour.

## 4.5 Cost tracing
Ganglion must eventually provide local cost tracing at run level and component level where possible.

## 4.6 Local performance tracking
Ganglion must eventually expose performance and health information via a lightweight local API endpoint.

## 4.7 Envelope security
Ganglion should eventually support encoding/encryption of outbound request envelopes and corresponding decode/decrypt handling on return.

## 4.8 Seamless OpenClaw integration
Ganglion must eventually integrate so cleanly with OpenClaw that Ganglion takes ownership of the request envelope before the provider/API call is shipped.

---

# 5. Definition of Ganglion in the new plan

At the start of the rebuild, Ganglion is not “the whole brain platform.”

Initially, Ganglion is:

**A deterministic middleware execution layer behind OpenClaw with evidence capture**

Its first responsibilities are:

- receive a request from OpenClaw
- normalize the request into a canonical Ganglion packet
- apply minimal deterministic handling
- forward the request through one controlled provider adapter
- receive the result
- shape the result into a clean return payload
- record evidence, timing, and trace information
- fail visibly and safely

That is the first product.

Everything else comes later.

---

# 6. What is out of scope at the beginning

The following are explicitly not first-stage build targets unless absolutely required for the packet path:

- dashboard development
- speculative databases
- broad API platform design
- advanced multi-provider routing
- self-learning logic
- tuning loops
- compaction engines
- deep memory search
- advanced analytics
- brain import/export
- rich metrics UI
- generalized orchestration frameworks
- large plugin ecosystems

If a feature does not help prove the end-to-end packet path, it should not be built in the first stage.

---

# 7. Engineering philosophy for the rebuild

## 7.1 Build from first principles
Every file, interface, module, and runtime responsibility must be justified.

## 7.2 Prefer boring correctness over clever architecture
The code should be explicit, inspectable, and predictable.

## 7.3 Test every boundary
Each module must have a clear input contract, output contract, and failure contract.

## 7.4 Keep the system file-first initially
Use files, structured logs, and local artifacts before introducing complex services or storage systems.

## 7.5 No hidden magic
If behaviour cannot be explained simply, it is too complex for the current phase.

## 7.6 No “probably working”
Completion is based on proof, not confidence.

## 7.7 One major concern per stage
No stage should try to prove multiple subsystems simultaneously.

---

# 8. Ganglion component naming model

The crustacean naming should be preserved as part of the project’s architecture language, but each component must also have a plain engineering meaning.

The naming model below should be used as the canonical interpretation.

## 8.1 Antennule
**Role:** ingress sensing and intake normalization

**Plain meaning:** receives incoming request signals from OpenClaw and normalizes them into a known pre-packet form.

## 8.2 Pleon
**Role:** packet assembly and transport body

**Plain meaning:** constructs the canonical Ganglion runtime packet and carries core execution fields.

## 8.3 Supraesophageal Ganglion
**Role:** high-order policy and top-level routing logic

**Plain meaning:** responsible for future strategic choices such as policy, model selection, and high-level route decisions.

## 8.4 Ventral Ganglion
**Role:** operational execution coordination

**Plain meaning:** handles lower-level execution flow, validations, and run progression.

## 8.5 Axon
**Role:** outbound signaling path

**Plain meaning:** carries prepared payloads to provider transport layers.

## 8.6 Peduncle
**Role:** provider/API interface bridge

**Plain meaning:** adapts Ganglion packet structures into provider-specific request formats and receives provider responses.

## 8.7 Mandible
**Role:** response shaping and consumable return

**Plain meaning:** converts provider output into an OpenClaw-compatible response shape.

## 8.8 Carapace
**Role:** protection and envelope guard

**Plain meaning:** future security and integrity layer, including encode/encrypt and decode/decrypt behaviour.

## 8.9 Cortex
**Role:** observation and metrics surface

**Plain meaning:** lightweight local metrics, trace summaries, and operator insight surfaces.

## 8.10 Molt
**Role:** controlled version transition

**Plain meaning:** future upgrade path for brain transitions, tuning changes, and safe promotion of new behaviour.

## 8.11 Brood
**Role:** exportable portable brain bundles

**Plain meaning:** future import/export and packaged brain portability format.

These names are to be retained, but internal documentation must always pair each themed name with a plain-language role.

---

# 9. End-state domain model

When mature, Ganglion should include the following domains.

## 9.1 Runtime ingress domain
Accepts and validates OpenClaw-origin input.

## 9.2 Packet assembly domain
Builds the canonical Ganglion packet.

## 9.3 Brain domain
Loads active brain definitions, bootstrap logic, and future memory/tuning hooks.

## 9.4 Routing domain
Selects provider, model, and execution path according to deterministic policy.

## 9.5 Provider transport domain
Executes outbound provider/API calls.

## 9.6 Response shaping domain
Produces OpenClaw-compatible return output.

## 9.7 Evidence domain
Captures packet traces, timings, costs, statuses, and artifacts.

## 9.8 Metrics domain
Exposes local operational visibility through a small read-only interface.

## 9.9 Brain portability domain
Handles import/export and version-safe activation of brains.

## 9.10 Security envelope domain
Handles optional encode/decode or encryption/decryption around provider traffic.

These are the end-state domains, not first-stage implementation requirements.

---

# 10. Required delivery sequence

Ganglion should be rebuilt in carefully controlled phases.

---

# Phase 0 — archive and hard reset

## Objective
Preserve the old implementation safely and establish a clean zero-base start.

## Required outcomes
- existing work archived safely
- archive clearly labeled as historical reference
- active implementation reset to fresh baseline
- explicit declaration in repo that Ganglion is restarting from zero
- no old runtime code retained as active logic

## Deliverables
- archive branch/tag/snapshot method
- archive identifier
- reset statement document
- fresh repo baseline
- staged roadmap document

## Definition of done
A new engineer can enter the repo and immediately understand:
“This project is starting from zero.”

---

# Phase 1 — define contracts before code

## Objective
Write the interfaces and rules before implementation begins.

## Required documents
- OpenClaw ingress envelope contract
- Ganglion canonical packet schema
- provider adapter request contract
- provider adapter response contract
- OpenClaw return envelope contract
- evidence artifact schema
- error schema
- trace and correlation ID rules
- file naming and path conventions

## Required examples
- valid input example
- invalid input example
- success response example
- failure response example
- evidence artifact example

## Definition of done
A third party can implement or test Stage 1 components without guessing.

---

# Phase 2 — build the minimum packet spine

## Objective
Implement the smallest true end-to-end runtime path.

## Required components
- Antennule: ingress adapter
- Pleon: packet builder
- Ventral Ganglion: packet validator and run coordinator
- Peduncle: provider adapter
- Mandible: response shaper
- Cortex Seed: evidence recorder and structured logs

## Required runtime path
`OpenClaw request -> Ganglion packet -> provider call -> Ganglion response -> OpenClaw response`

## Not included
- memory system
- tuning
- import/export
- encryption
- multi-provider intelligence
- dashboard

## Definition of done
A real request can traverse the full path and return successfully with evidence captured.

---

# Phase 3 — add observability hardening

## Objective
Make the packet spine trustworthy and inspectable.

## Required capabilities
- structured logs for each stage
- per-run evidence files
- timing capture
- cost capture where available
- request and response summaries
- safe redaction rules
- failure reason capture
- replayable fixtures

## Definition of done
Every run can be inspected afterwards without relying on UI or memory.

---

# Phase 4 — introduce minimal brain structure

## Objective
Add the lightest useful brain structure without destabilizing the core path.

## Required capabilities
- bootstrap file
- active brain definition
- deterministic load order
- naming conventions
- simple compile/load routine

## Definition of done
Ganglion can load a named brain package and use it predictably in packet handling.

---

# Phase 5 — add cost and local metrics exposure

## Objective
Support local operational visibility.

## Required capabilities
- per-run cost records
- aggregate latency/success/failure summaries
- local metrics snapshot
- lightweight read-only API endpoint

## Definition of done
An operator can inspect cost and health locally without a dashboard.

---

# Phase 6 — introduce import/export

## Objective
Make Ganglion brains portable.

## Required capabilities
- export format
- import validation
- manifest schema
- activation rules
- rollback-safe handling

## Definition of done
A brain can be exported, moved, re-imported, and activated predictably.

---

# Phase 7 — introduce local deep memory search

## Objective
Add deterministic retrieval across memory layers.

## Required capabilities
- memory layer schema
- local indexing
- query interface
- ranking logic
- recall evidence artifacts

## Definition of done
Ganglion can show what memory was recalled and why.

---

# Phase 8 — introduce tuning and self-learning

## Objective
Create a supervised improvement loop.

## Required capabilities
- run review inputs
- compaction process
- tuning proposals
- approval gate
- rollback path
- drift controls

## Definition of done
Ganglion can improve under supervision without uncontrolled behavioural drift.

---

# Phase 9 — introduce security envelope processing

## Objective
Support encode/decode or encrypt/decrypt transport wrapping.

## Required capabilities
- outbound transform
- inbound reverse transform
- integrity validation
- failure-safe fallback
- interoperability preservation

## Definition of done
Security wrapping works without degrading the OpenClaw-facing response path.

---

# 11. Initial zero-base repository structure

The new repository should begin small and deliberate.

```text
ganglion/
  README.md
  RESET_BRIEF.md
  ROADMAP_ZERO_BASE.md
  docs/
    contracts/
      openclaw_ingress.md
      ganglion_packet.md
      provider_adapter.md
      openclaw_return.md
      evidence_schema.md
      error_schema.md
    conventions/
      naming.md
      paths.md
      trace_ids.md
      crustacean_components.md
  src/
    ganglion/
      __init__.py
      antennule/
      pleon/
      ventral/
      peduncle/
      mandible/
      cortex_seed/
      shared/
  tests/
    contracts/
    integration/
    fixtures/
  runtime/
    evidence/
    traces/
    samples/
  brains/
    .keep
  exports/
    .keep
```

This is intentionally minimal.

No large subsystem trees should be introduced until they are actually needed.

---

# 12. Naming and filesystem conventions

Ganglion’s long-term success depends heavily on predictable file layout and names.

## 12.1 Naming requirements

Names must be:

* explicit
* stable
* sortable
* grep-friendly
* environment-safe
* human-readable

## 12.2 Areas that require naming discipline

* brains
* bootstrap files
* memory layers
* exports
* evidence artifacts
* cost traces
* metrics snapshots
* packet captures
* trace IDs
* tuning records

## 12.3 Suggested rules

* lowercase only
* predictable separators
* sortable timestamps
* manifest-first export bundles
* deterministic “active brain” path names
* no ambiguous abbreviations unless standardized

## 12.4 Example structure

```text
brains/
  active/
    brain_main_v001/
      manifest.json
      bootstrap.md
      policies.json
      memory_layers/
```

## 12.5 Evidence naming example

```text
runtime/evidence/2026-03-19T14-22-31Z_trace_ab12cd34_run.json
```

---

# 13. Stage 1 detailed implementation brief

## Stage 1 title

**Packet Spine Proof**

## Stage 1 objective

Prove that Ganglion can sit between OpenClaw and a provider/API and successfully handle a request-response round trip with evidence.

## Stage 1 functional goal

A user request arriving through OpenClaw must be passed into Ganglion, normalized into a Ganglion packet, sent through a provider adapter, received back, wrapped into a return envelope, and handed back to OpenClaw.

## Stage 1 non-goals

Do not include:

* memory
* tuning
* import/export
* deep search
* dashboard
* encryption
* advanced metrics
* multi-brain management
* adaptive routing

---

# 14. Stage 1 component breakdown

## 14.1 Antennule

**Responsibility:** ingress sensing and normalization

Tasks:

* receive OpenClaw-origin input
* parse required fields
* reject invalid envelope structures early
* preserve source metadata

## 14.2 Pleon

**Responsibility:** canonical packet construction

Tasks:

* assign trace ID
* assign run ID
* normalize message content
* define packet version
* preserve routing and metadata defaults

## 14.3 Ventral Ganglion

**Responsibility:** validation and runtime coordination

Tasks:

* validate packet completeness
* validate field types
* reject invalid packets with structured errors
* coordinate stage progression

## 14.4 Peduncle

**Responsibility:** provider/API bridge

Tasks:

* map Ganglion packet to one provider request format
* send the request
* receive response
* capture raw timing and transport metadata

## 14.5 Mandible

**Responsibility:** response shaping

Tasks:

* normalize provider response into Ganglion result
* transform Ganglion result into OpenClaw-compatible return payload

## 14.6 Cortex Seed

**Responsibility:** evidence capture and logging seed

Tasks:

* persist request summary
* persist response summary
* persist timing
* persist provider/model information
* persist status and errors
* emit structured stage logs

---

# 15. Stage 1 required contracts

These must be written before implementation starts.

## 15.1 OpenClaw ingress contract

At minimum:

* source request identifier
* session or conversation identifier if available
* message content
* model/provider hint if available
* timestamp
* metadata bag

## 15.2 Ganglion packet contract

At minimum:

* packet_version
* trace_id
* run_id
* source_system
* ingress_timestamp
* normalized_messages
* provider_target
* model_target
* routing_mode
* evidence_mode
* metadata

## 15.3 Provider request contract

Must define exactly what gets sent to the chosen provider.

## 15.4 Provider response contract

Must define exactly what normalized shape Ganglion expects back.

## 15.5 OpenClaw return contract

Must define exactly what is returned after Ganglion processing.

## 15.6 Evidence artifact contract

Must include:

* run_id
* trace_id
* status
* start time
* end time
* duration
* provider used
* model used
* request summary
* response summary
* error summary
* cost fields if available

## 15.7 Error contract

Must explicitly distinguish:

* ingress error
* validation error
* provider transport error
* response shaping error
* evidence write error

---

# 16. Stage 1 testing plan

## 16.1 Contract tests

For each schema:

* valid example passes
* missing required field fails
* malformed field fails
* unknown field handling is defined explicitly

## 16.2 Unit tests

Test:

* trace ID generation
* packet normalization
* packet validation
* response shaping
* evidence writing
* error shaping

## 16.3 Integration tests

Simulate:

* valid request full round trip
* invalid ingress request
* provider timeout
* provider malformed response
* evidence write failure

## 16.4 Local smoke test

Run one real or controlled provider/API request through the full chain and inspect:

* returned output
* logs
* evidence artifact
* timing
* cost if available

---

# 17. Stage 1 evidence requirements

Stage 1 is not complete until Declan provides:

* exact sample input
* exact Ganglion packet produced
* exact provider request summary
* exact provider response summary
* exact output returned to OpenClaw
* exact evidence file path
* exact logs for one success run
* exact logs for one failure run
* explicit pass/fail statement
* list of known limitations

---

# 18. Stage 1 acceptance criteria

Stage 1 is accepted only if all of the following are true:

1. A request can enter Ganglion from OpenClaw path assumptions.
2. Ganglion produces a canonical packet.
3. Ganglion forwards that packet through one provider adapter.
4. Ganglion receives and normalizes the provider response.
5. Ganglion returns a valid response to OpenClaw.
6. Ganglion writes local evidence artifacts.
7. Ganglion logs each stage transition clearly.
8. Failure cases return controlled structured errors.
9. No unsupported advanced features were silently introduced.
10. Another engineer can repeat the validation steps.

---

# 19. Required outputs after Stage 1

Declan must hand back:

## 19.1 Reset report

What was archived and how.

## 19.2 Fresh baseline report

What files exist in the new implementation and why.

## 19.3 Contract pack

The written schemas and interface definitions.

## 19.4 Stage 1 implementation summary

Which files/modules were created and what each one does.

## 19.5 Validation pack

* commands run
* tests executed
* results
* evidence artifact sample
* structured log sample
* known issues
* hard pass/fail status

---

# 20. Rules for all future stages

These apply to every stage after Stage 1.

## 20.1 No stage without a definition of done

## 20.2 No new subsystem without a written interface

## 20.3 No claim of completion without proof artifacts

## 20.4 No dashboard-led validation

## 20.5 No heavy persistent infrastructure until file-first limits are reached

## 20.6 No tuning without rollback

## 20.7 No memory without recall evidence

## 20.8 No encryption mode without interoperability proof

## 20.9 No import/export without manifest validation

## 20.10 No metrics endpoint without a local truth source

---

# 21. Immediate instruction to Declan

Use the following operating posture:

Ganglion is being restarted from absolute zero.
Do not reuse the existing implementation as the active base.
Archive the old state and then create a clean new baseline.
Treat the old repo only as historical reference.
Start by defining the contracts, conventions, naming rules, and staged roadmap.
Then implement only the minimum packet spine required to prove:

`OpenClaw -> Ganglion -> provider/API -> Ganglion -> OpenClaw`

Do not build advanced features until this path is operational and evidenced.

For every stage, provide:

* exact inputs
* exact outputs
* test method
* logs
* evidence artifacts
* known gaps
* hard pass/fail statement

---

# 22. Final success condition

This rebuild is successful only when Ganglion becomes:

* technically honest
* strategically disciplined
* small at first
* easy to reason about
* easy to verify
* easy to extend
* safe to evolve
* still true to its Ganglion/crustacean identity

The first win is not sophistication.

The first win is a **clean, proven, inspectable packet path**.

Once that is real, Ganglion earns the right to grow into:

* brain portability
* memory layers
* local deep search
* cost tracing
* performance APIs
* tuning loops
* self-learning
* secure envelopes
* richer crustacean subsystem behaviour

Until then, the only priority is to build the spine correctly.

---

# 23. Summary statement

Ganglion now restarts from zero with a new strategic direction:

* retain the intelligence and naming identity
* discard implementation inheritance
* build from first principles
* prove the packet path first
* layer all future capability onto a trustworthy base

This is a full reset.

This is the correct move.

This is how Ganglion becomes real.
