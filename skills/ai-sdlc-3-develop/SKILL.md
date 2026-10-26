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

Derive tests from the UC.

Choose unit, integration or end-to-end checks according to the behavior and
risk. Cover the observable outcome at an appropriate boundary. Keep tests
focused; create or split files when that gives them a clear responsibility.

Work in small TDD cycles: identify or write a failing test, implement the
smallest change, then refactor while preserving behavior. During refactoring,
look for mixed responsibilities, unclear names and harmful duplication. Add
characterization tests first if existing coverage does not protect the behavior.
Avoid abstractions based only on speculative needs.

Apply AGENTS.md rule 7 to every file this change touched.

---

## Commands

Run the project-specific unit tests documented in `docs/PROJECT.md`.

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

Unit tests pass.

Record phase 3 and status in `docs/TASKS.md` per `AGENTS.md`.
