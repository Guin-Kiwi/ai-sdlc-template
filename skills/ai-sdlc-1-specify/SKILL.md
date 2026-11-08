---
name: ai-sdlc-1-specify
description: Create or update a minimal use case specification.
---

# PHASE 1 — SPECIFY

Create or update a minimal UC from the user story or feature description. Ask if
input is missing or requirements are unclear. Generate no code or tests; do not
invent functionality.

Changes needing no spec skip SPECIFY and DESIGN; see `docs/INDEX.json`.

## Select the UC file and branch

Update the existing UC for the feature; create one only if none exists. Use
`docs/specs/UC-[NNN]-[NAME].md`, with a short uppercase, hyphen-separated NAME.
Follow `docs/WORKING-AGREEMENT.md` for numbering and branch naming; inspect
`docs/specs/` before assigning a number.

Create or join the appropriate branch before writing.

## Write requirements and validation criteria

Read `docs/specs/UC-TEMPLATE.md` and follow its sections. Keep content concise;
write "none" where a section does not apply.

Link source requirements to acceptance criteria and the checks planned to verify
them. Record actual results when those checks run.
For external rule tables, formulas or models, identify the authoritative version
and how implementation consistency will be checked. Record unresolved policy
choices explicitly.

For user-facing outcomes, describe the complete journey, dependencies on other
slices and how it will be demonstrated. Choose automated or manual evidence as
appropriate; explicitly record deferred or incomplete journeys.

## Completion evidence

Report acceptance criteria, boundaries, affected interfaces/components, risks,
tradeoffs and validation approach. Identify the created or updated UC.

Record phase 1 and status in `docs/TASKS.md` per `AGENTS.md`.
