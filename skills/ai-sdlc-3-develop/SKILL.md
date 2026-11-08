---
name: ai-sdlc-3-develop
description: Implement the current use case using strict TDD.
---

# PHASE 3 — DEVELOP

Changes whose type needs no spec skip SPECIFY and DESIGN; see the change types in `docs/INDEX.json`.

## Goal

Implement the current use case using **Test-Driven Development**.

---

## Source of Truth

docs/TASKS.md  
docs/specs/UC-[NNN]-[NAME].md  
docs/PROJECT.md

---

## Test Derivation

Derive tests from the UC. Choose the appropriate boundary (unit, integration or
end-to-end) for the behavior and risk.

Before adding a case, inspect nearby tests. For the same behavior with different
inputs and expected outcomes, prefer a readable parameterized table with named
cases and meaningful boundaries and errors. Keep distinct behaviors or setups
separate, and expected values independent of implementation logic.

Work in small TDD cycles: fail, implement the smallest change, then refactor.

## Refactor after green

Review the implementation and whole affected test files for mixed responsibilities,
repeated setup or assertions, and helpers that obscure the case. Split by
responsibility, parameterize equivalent cases or share setup when this improves
clarity; file size alone is not a reason to split. Preserve meaningful coverage
and boundaries. Add characterization tests if needed before refactoring, and
avoid speculative abstractions or tests that mirror the implementation.

Rerun relevant tests. Report the refactor or why none was needed. If a necessary
refactor exceeds the slice, record its reason and impact as a follow-up.

Apply AGENTS.md rule 7 to every file this change touched.

---

## Commands

Use the commands in `docs/PROJECT.md` with the test-scope policy in `AGENTS.md`.
During TDD, select the affected test or group; use the full entrypoint at the
completed slice handoff.

---

## Rules

- Tests before code.
- Ask the user if requirements are unclear.

---

## Evidence to provide

- tests added/updated first when applicable
- minimal implementation
- impacted files
- validation results

---

## Output

Implementation complete.

Affected tests and applicable handoff checks pass; report any missing evidence.

Record phase 3 and status in `docs/TASKS.md` per `AGENTS.md`.
