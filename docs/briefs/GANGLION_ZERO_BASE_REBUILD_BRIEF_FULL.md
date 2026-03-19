# Ganglion Strategic Refocus Brief
## lossless-claw visibility, brain scanning, backup, and memory optimisation companion

**Owner:** Sam  
**Primary implementation lead:** Declan  
**Project:** Ganglion  
**Status:** Refocus approved  
**Build posture:** refactor around the existing lossless-claw memory engine

---

# 1. Executive directive

Ganglion is no longer to be developed as a competing memory system.

The memory engine decision has been made:
- **lossless-claw is the integrated memory solution**

Ganglion must now be designed as a companion layer that improves the operability of that solution.

This means Ganglion should focus on:
- visibility
- inspectability
- brain scanning
- backup/export safety
- memory optimisation and tuning support
- operator evidence and change confidence

The prior zero-base rebuild was still useful because it forced the repo into a smaller, more disciplined state. However, the governing direction is now different from the earlier packet-spine-first ambition.

---

# 2. Strategic intent

The purpose of Ganglion is now to make lossless-claw:
- easier to understand
- easier to inspect
- easier to back up
- easier to tune
- safer to evolve
- more legible to operators

Ganglion should reduce mystery, not add more layers of mystery.

---

# 3. Core product definition

Ganglion is now defined as:

**A lossless-claw companion tool/plugin system for visibility, brain scanning, backup, and memory optimisation.**

At minimum, Ganglion should help an operator answer:
- What does this agent/session currently remember?
- What is still raw vs summarized vs condensed?
- How much fresh tail is protected?
- Is the current context threshold appropriate?
- Are session patterns or exclusions misconfigured?
- Can we safely capture a backup before changing settings?
- What tuning changes are recommended, and why?

---

# 4. Strategic principles

## 4.1 Use the chosen memory engine
Do not rebuild a parallel memory engine by default.

## 4.2 Be operator-first
The first useful outputs should be reports, scans, evidence artifacts, and safe change plans.

## 4.3 Evidence before claims
No recommendation, scan, or tuning plan is complete without operator-verifiable evidence.

## 4.4 Safety before automation
Backup, diff, rollback, and validation come before any write-path automation.

## 4.5 Explainability over cleverness
Ganglion should expose memory posture in a way a human can understand and verify.

## 4.6 Optimise the real system, not an imagined one
Ganglion should inspect and improve the live lossless-claw deployment that actually exists.

---

# 5. Primary capability lanes

## 5.1 Visibility
Expose readable views of current memory state.

Examples:
- session memory posture summary
- summary depth distribution
- raw tail preservation status
- context pressure summary
- ignored/stateless session pattern visibility

## 5.2 Brain scanning
Provide a richer diagnostic scan of a session or agent memory state.

A brain scan should help an operator see:
- important raw messages still in direct view
- summarized strata
- condensed strata
- memory gaps or anomalies
- tuning pressure indicators

## 5.3 Backup and export safety
Allow the operator to snapshot relevant memory state before risky changes.

Examples:
- SQLite snapshot metadata
- exported scan bundle
- report bundle for audit/review
- rollback-oriented config capture

## 5.4 Memory optimisation
Recommend safer tuning changes around the existing LCM configuration.

Examples:
- fresh tail count too low/high
- threshold too aggressive or too lax
- exclusion patterns causing missing recall
- stateful/stateless hygiene issues
- summarization-model posture mismatches

---

# 6. Target integration posture

Ganglion should integrate as a plugin/tool layer around OpenClaw + lossless-claw.

Possible surfaces include:
- read-only inspection tools
- report generators
- local artifact writers
- optional config patch planning helpers
- optional plugin config or command surface for operator tuning

Ganglion should be able to work without replacing core message execution paths.

---

# 7. What is now out of scope by default

Unless explicitly revived, Ganglion should not primarily be:
- a replacement memory engine
- a full speculative middleware runtime that must own provider traffic
- a broad analytics/dashboard program before useful operator tooling exists
- a generalized AI orchestration framework
- a parallel brain platform that duplicates lossless-claw’s purpose

---

# 8. Existing prototype code posture

Current repo contents such as:
- packet spine proof
- evidence writing
- live-binding prototype

should be treated as **transitional prototype material**.

They may still be reused if they help with:
- report generation
- evidence capture
- artifact writing
- controlled interfaces

But they should not dictate the future product identity.

---

# 9. First implementation targets

The first useful Ganglion outputs should be:

1. **Visibility report**
   - concise session/agent memory posture summary

2. **Brain scan report**
   - deeper operator-readable analysis of what memory state looks like

3. **Backup artifact**
   - inspectable snapshot/export bundle before changes

4. **Optimisation recommendation report**
   - recommended tuning changes, rationale, tradeoffs, and rollback notes

---

# 10. Success criteria

Ganglion is succeeding when it helps the operator:
- understand current lossless-claw memory behaviour quickly
- capture safe backups before tuning
- make tuning decisions with evidence
- improve recall/compaction behaviour without guesswork
- keep the memory system inspectable over time

---

# 11. Development discipline

- docs must describe the real product intent
- implementation must follow the new companion role
- every write-path should have rollback posture
- every recommendation should be evidence-backed
- avoid product drift back into “Ganglion replaces memory” framing

---

# 12. Canonical short description

Ganglion is a **lossless-claw visibility, brain scanning, backup, and memory optimisation companion for OpenClaw**.
