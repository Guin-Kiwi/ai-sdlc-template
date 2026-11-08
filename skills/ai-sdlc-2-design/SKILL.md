---
name: ai-sdlc-2-design
description: Determine minimal architecture components for the current use case.
---

# PHASE 2 — DESIGN

Identify the minimum architecture needed for the current use case. Generate no
code, tests or implementation details.

Changes needing no spec skip SPECIFY and DESIGN; see `docs/INDEX.json`.

## Read the use case and project constraints

Read the active `docs/specs/UC-[NNN]-[NAME].md` and `docs/PROJECT.md`. Ask the user
if the UC is missing.

## Identify required components

Identify components across domain, application, interfaces and infrastructure:
entities, use-case services, repository interfaces, persistence adapters or API
endpoints as needed. Check whether the existing architecture satisfies the UC;
propose only necessary changes.

Extend components while responsibilities stay cohesive; separate distinct
responsibilities. Avoid speculative abstractions and file-length-driven splits.
Keep descriptions concise.

## Record design decisions

Use `docs/WORKING-AGREEMENT.md` to decide whether a choice belongs in the UC or
an ADR. When an ADR is needed, use `docs/adr/ADR-TEMPLATE.md` and record status,
context, alternatives, decision and consequences. After human acceptance, update
`docs/PROJECT.md` and propose any durable agent rules in `AGENTS.md`. Preserve
superseded ADRs and review related changes together.

## Completion evidence

Report acceptance criteria, boundaries, affected components/interfaces, risks,
tradeoffs and validation approach. State whether architecture was verified or
minimally updated.

Record phase 2 and status in `docs/TASKS.md` per `AGENTS.md`.
