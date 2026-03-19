# Ganglion

Ganglion is being repositioned as a **lossless-claw companion toolset** for OpenClaw.

It is **not** the primary memory engine.
The primary memory engine is **lossless-claw**.

Ganglion's role is now to improve operator visibility, safety, backupability, and tuning around the existing lossless-claw deployment.

## New design intent

Ganglion should become a tool/plugin layer focused on four jobs:

1. **Visibility**
   - inspect what lossless-claw is doing
   - surface session memory posture, summary depth, tail protection, context pressure, and retrieval state
   - make memory behaviour legible to operators

2. **Brain scanning**
   - scan an agent/session memory state
   - explain what is raw, what is summarized, what is condensed, and what is still directly available
   - provide operator-readable memory posture reports

3. **Backup / export safety**
   - snapshot or export memory state in an inspectable form
   - support backup-oriented workflows for key sessions/agents
   - preserve rollback and recovery options

4. **Memory optimisation / tuning**
   - help tune existing lossless-claw settings rather than replace them
   - recommend or apply safer settings for fresh tail, thresholds, depth, exclusions, and summarization posture
   - support measurement-driven tuning rather than intuition-driven changes

## What Ganglion is not

Ganglion is no longer positioned as:
- a competing memory system
- a replacement for lossless-claw
- a speculative parallel brain runtime
- a broad middleware layer that must own all provider traffic before it is useful

## Current repository status

This repository still contains proof-stage rebuild work from the earlier zero-base reset:
- minimum packet spine proof
- evidence writing
- live-binding pilot
- contract pack and conventions

That work is now treated as **transitional reference/prototype material** rather than the final product direction.

## New target product

The intended end-state is an OpenClaw-compatible companion/plugin/tool layer that helps operators answer questions like:
- What does lossless-claw currently remember for this session?
- What has been summarized vs preserved raw?
- What is the current context pressure?
- Are settings too aggressive or too weak?
- Can we safely back this state up before changing tuning?
- What tuning changes are recommended for this workload?

## Priority surfaces

Ganglion should eventually expose:
- memory visibility reports
- brain scan summaries
- session backup/export helpers
- tuning recommendations
- optional operator controls for safe configuration updates
- evidence artifacts for before/after tuning comparisons

## Immediate repo priorities

1. refactor docs and plan around the new role
2. define the lossless-claw companion contracts
3. specify visibility / scan / backup / optimise workflows
4. decide what prototype code to keep, adapt, or archive
5. implement the first operator-valuable feature before broadening scope

## Operator principle

Ganglion should make lossless-claw **more understandable, more inspectable, and safer to operate**.
It should not make the memory stack more mysterious.
