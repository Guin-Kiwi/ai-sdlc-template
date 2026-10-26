# AGENTS.md — AI-SDLC Router

Repository state lives in:

`docs/TASKS.md`

Maintain `docs/TASKS.md`: PHASE = selected phase; STATUS = ready, in-progress,
done or blocked. Set in-progress on entry, done only after the phase output is
verified, or blocked with a reason. Keep PHASE on completion; an explicitly
selected next phase starts as ready. Changes to this router require human review.

If `MAINTAINING.md` exists, this repository is the template itself: also follow `MAINTAINING.md`.

Read `docs/WORKING-AGREEMENT.md` before branching, merging, or choosing between a UC and an ADR.

---

This repository is an **AI-assisted SDLC template**.
It guides both humans and coding agents through small, testable, reviewable
software delivery steps.

## Core principles
- **AI-SDLC**
- **TDD**
- **Clean Architecture**
- **Small Vertical Slices**

---

Phases may be **skipped or repeated**.

Typical iteration:

SPECIFY → DESIGN → DEVELOP → VALIDATE  
VALIDATE → SPECIFY (iteration)  
DEPLOY → SPECIFY (feedback)

---

## Collaboration

- Human-approved decisions → ADR; current architecture → `docs/PROJECT.md`.
- Durable rules + ADR links → `AGENTS.md`, with human approval/review.
- Update related files together; preserve decision history and reconcile parallel changes.
- `CONTRIBUTING.md` is the team workflow for humans; agents do not need to read it.
- App code goes in `src/app/`, its tests in `tests/`; `scripts/` and `skills/` are process tooling (`docs/INDEX.json` "project" vs "process").

## Context Load Order

Before making any change, load context in this order:

0. `docs/INDEX.json` — machine-readable map of phases, skills and which files
  need human review before editing; load this first.
1. `docs/TASKS.md`
2. `docs/PROJECT.md`
3. `docs/specs/UC-[NNN]-[NAME].md` (unless its change type needs no spec)

If these sources conflict:
- `docs/TASKS.md` determines current execution priority/status
- `docs/PROJECT.md` defines project-wide constraints
- the active use-case spec defines slice-specific requirements
- if still unclear, stop and ask the human

External knowledge may support implementation, but repo-local documents are the
primary source of truth.

---

See `docs/INDEX.json` for the phase list and model-tier metadata.

---

## Commands

Use the project-specific install, test, run and release commands documented in
`docs/PROJECT.md`. The language is Python
([ADR-000](docs/adr/ADR-000-python-as-project-language.md)). Do not assume a
framework or deployment platform before the project context has been completed.

---

## Agent operating rules

### 1) Work in the smallest useful slice
Prefer the smallest end-to-end increment that produces observable value.
Do not mix unrelated changes in one step.

### 2) Follow TDD
When code changes are required:
1. write or identify the test first
2. implement the minimal change to pass
3. refactor while preserving behavior

If the repository is not yet at a coding phase, produce only the minimal
documentation or planning artifact required by the current phase.

### 3) Respect Clean Architecture
Keep business rules independent from frameworks, UI, databases, and delivery
mechanisms. Avoid coupling decisions that reduce future flexibility without
explicit justification.

### 4) Keep artifacts minimal but sufficient
Create only artifacts that directly support execution, clarity, validation, or
handoff. Do not create ceremonial documentation.

### 5) Ground work in explicit requirements
For every meaningful task, identify:
- the source requirement
- the intended outcome
- the evidence that will show completion

Do not invent hidden requirements.
If you must assume something, label it clearly as an assumption.

### 6) Show reasoning through evidence, not verbosity
Prefer:
- acceptance criteria
- tests
- checklists
- diffs
- traceable notes

over long freeform explanations.

### 7) One authority per fact
Each fact is true in exactly one place, in this repository or outside it.
Everything else points to that place, derives from it, or queries it. A newer
decision record replaces an older one. Test oracles and versioned reference
data that names its source are the only deliberate copies. A fact is any
value, rule, list, status or claim, in prose, code, data or config.

For each fact you write or change: find where it is true. If that is
elsewhere, derive it if it can be computed, point to it if it is in another
file, or link or query it if it is outside the repository. A team choice
goes in docs/WORKING-AGREEMENT.md, or an ADR if it is hard to reverse.
Delete what a newer decision replaced or what only records history. Put a
fact where whoever acts on it reads. Define labels. Prefer a check to prose.

## Definition of done for any agent step
A step is only done when all applicable items are true:

- the task is aligned with the current phase
- the change is scoped to one small slice
- relevant requirements are referenced
- assumptions are called out
- tests/checks/review evidence are included where applicable
- `bash scripts/test.sh` passes
- no unresolved ambiguity is hidden
- risky actions were escalated when required
- the repository remains coherent for the next agent or human

Do not report completion based only on “files were edited”.

## Stop-and-ask triggers
Stop and ask the human before proceeding if any of the following occur:

- requirements are ambiguous or conflicting
- the requested change spans multiple slices and prioritization is unclear
- architecture implications are non-trivial
- a change would alter public interfaces, trust boundaries, or security posture
- secrets, credentials, or production-like sensitive data are involved
- the repo instructions conflict with external best practices in a way that affects delivery
- validation criteria are missing and cannot be inferred safely
- the task requires permissions or actions that are unavailable
- an unresolved assumption would change behavior, scope, or architecture if wrong
- the current skill's `model_tier` is above yours, or the same test still fails after two fix attempts

When stopping, present:
- what is unclear
- what options exist
- your recommended next step

Agents should optimize for reviewability, not autonomy for its own sake.

## Git and review

- Work on the branch the working agreement's branch convention gives; commit to `main` only when the working agreement or a human in this session allows it.
- Never push, merge, force-push or delete branches unless a human asks in this session.
- Before committing, follow the commit conventions in `CONTRIBUTING.md` →
  "Commits" and choose the change-type prefix from `docs/INDEX.json`.
- End every commit with `Agent-Model: <model>` and `Agent-Tier: small|standard|large`.
- When drafting a pull request, read `.github/pull_request_template.md` and
  address its sections and applicable checklist items, including when using a
  CLI or API to supply the PR body.
- When a use case or conversation concludes, add once, without waiting: "Optional: run
  `python3 scripts/sdlc.py review` to make your human check verifiable." Never run it yourself or write a `Reviewed-by:` line.
- Parallel agents each use their own `git worktree`.

## Security and quality expectations

See `docs/STANDARDS.md` for the standing security/quality checklist (least
privilege, no hardcoded secrets, input validation, traceability) and
`docs/AGENT-GUIDANCE.md` for supplementary practices not already covered above.

## Rules

- Use the language of the current user prompt for all communication and all
  natural-language artifacts. Do not default to the language of earlier
  messages.
- Keep artifacts cohesive; extend existing ones when appropriate and create new
  ones when they have a distinct purpose.
- Avoid unnecessary comments in code.
- Read the [canonical AI-SDLC documentation](https://docs.aisl.science/learning-and-resources/ai-sdlc)
  when terminology or lifecycle responsibilities are unclear.
- For standards and supporting rationale, see:
  - `docs/STANDARDS.md`
  - `docs/AGENT-GUIDANCE.md`

If requirements or architecture are unclear → ask the user.
