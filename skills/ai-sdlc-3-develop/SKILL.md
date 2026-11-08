---
name: ai-sdlc-3-develop
description: Implement the current use case using strict TDD.
---

# PHASE 3 — DEVELOP

Implement the active UC using small TDD cycles: failing test, minimum change,
then refactor. Changes needing no spec skip SPECIFY and DESIGN per
`docs/INDEX.json`; use their existing requirements.

## Write tests from requirements

Derive tests from requirements. Choose unit, integration or end-to-end boundaries
according to behavior and risk. Inspect nearby tests before adding cases.

For the same behavior with different inputs and expected outcomes, prefer a
readable parameterized table with named cases covering relevant boundaries and
errors. Keep distinct behaviors or setups separate, and expected values
independent of implementation.

## Refactor after green

Inspect the implementation and whole affected test files for mixed responsibilities,
repeated setup/assertions and obscuring helpers. Split by responsibility,
parameterize equivalent cases or share setup when clarity improves. File size
alone does not justify splitting. Preserve meaningful coverage and boundaries;
add characterization tests before refactoring where needed. Avoid speculative
abstractions and tests that mirror implementation.

Rerun affected tests. Record necessary work beyond the slice as a follow-up with
its reason and impact.

Apply `AGENTS.md` rule 7 to every touched file.

## Validation and handoff

Use `docs/PROJECT.md` commands and `AGENTS.md`'s test-scope and status rules.
Before the final response:

- Update phase 3 and STATUS in `docs/TASKS.md` using the actual check results.
- Report tests added or updated, TDD evidence where applicable, implementation
  and affected files.
- State what was refactored or why none was needed.
- Report commands, results and missing checks; claim completion only when the
  required outputs and checks are satisfied.
