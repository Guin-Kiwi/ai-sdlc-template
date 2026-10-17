---
name: ai-sdlc-1-specify
description: Create or update a minimal use case specification.
---

# PHASE 1 — SPECIFY

Changes whose type needs no spec skip SPECIFY and DESIGN; see the change types in `docs/INDEX.json`.

## Goal

Create or update a **minimal use case specification**.

---

## Input

User story or feature description.

If missing → ask the user.

---

## Use Case File

docs/specs/UC-[NNN]-[NAME].md

Rules:

- NNN and the branch name → follow `docs/WORKING-AGREEMENT.md`.
- NAME = short uppercase identifier
- words separated with `-`

Determine the next number by scanning:

docs/specs/

If a UC for the feature already exists → **update it instead of creating a new one**.

---

## Branch

Create or join the branch before writing anything; use its name per
`docs/WORKING-AGREEMENT.md`.

---

## Steps

1. Open template

docs/specs/UC-TEMPLATE.md

2. Create or update the UC with minimal content, following the template's
   sections:

- Goal
- Business value
- Scope (in / out)
- Actors
- Preconditions
- Trigger
- Main flow
- Alternate / edge flows
- Errors / failure cases
- Acceptance criteria
- Security / trust-boundary notes
- Validation plan
- Open questions / assumptions
- Notes for implementation

Do not add unnecessary text. Write "none" for sections that don't apply.

---

## Rules

- Prefer **updating existing UC files**.
- Create a new UC only if none exists.
- Do not invent functionality.
- Ask the user if requirements are unclear.
- Do **not generate code or tests**.

---

## Evidence to provide

- acceptance criteria
- boundaries
- interfaces or components affected
- risks / tradeoffs
- validation approach

---

## Output

UC specification created or updated.

Record phase 1 and status in `docs/TASKS.md` per `AGENTS.md`.
