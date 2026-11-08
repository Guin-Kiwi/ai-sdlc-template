# AI-SDLC Router

Changes to this file require human review. If `MAINTAINING.md` exists, follow it
for template maintenance. Read `docs/WORKING-AGREEMENT.md` before branching,
merging or choosing between a UC and an ADR.

## Context Load Order

Before changes, read:

0. `docs/INDEX.json` — phases, skill paths, model tiers, change types and review gates.
1. `docs/TASKS.md` — current priority, phase and status.
2. `docs/PROJECT.md` — project constraints, architecture and commands.
3. The active `docs/specs/UC-[NNN]-[NAME].md` — slice requirements, unless the
   change type needs no spec.

Use each source for its stated scope. Resolve conflicts with the human when
these scopes do not settle them. External knowledge supports implementation;
repo-local requirements govern it.

Follow the selected phase's skill. Phases may be skipped or repeated:
SPECIFY → DESIGN → DEVELOP → VALIDATE, then iterate or DEPLOY.

Maintain `docs/TASKS.md`: PHASE identifies the selected phase. Use STATUS ready
when a new phase is explicitly selected, in-progress while work or review is
underway, and done when required outputs are verified and required checks pass.
While in-progress, explain what remains, any missing decision or prerequisite,
and the next action. Keep PHASE unchanged when work finishes.

## Project structure and commands

App code: `src/app/`. App tests: `tests/`. Process tooling: `scripts/` and
`skills/`; see `docs/INDEX.json` for the full project/process split.

Use install, test, run and release commands from `docs/PROJECT.md`. Python is
established by [ADR-000](docs/adr/ADR-000-python-as-project-language.md). Do not
assume a framework or deployment platform before project setup establishes it.

Keep current architecture in `docs/PROJECT.md`, human-approved consequential
decisions in ADRs, and durable agent rules and ADR links here. Update related
files together, preserve decision history and reconcile parallel changes.

## Agent operating rules

### 1) Work in the smallest useful slice
Choose the smallest end-to-end increment with observable value; keep unrelated
changes separate.

### 2) Follow TDD
For code changes: identify or write a failing test, implement the minimum to pass,
then refactor while preserving behavior. Before a coding phase, produce only the
planning or documentation that the selected phase needs.

### 3) Respect Clean Architecture
Keep business rules independent of frameworks, UI, databases and delivery.
Justify coupling that reduces flexibility.

### 4) Keep artifacts useful
Create or extend cohesive artifacts for execution, clarity, validation or handoff.
Create new files when they have a distinct purpose; avoid unnecessary code comments.

### 5) Ground work in requirements
Identify each task's source requirement, outcome and completion evidence. Label
assumptions; do not invent requirements.

### 6) Show evidence concisely
Explain work through acceptance criteria, tests, checklists, diffs and traceable
notes. Use the current prompt's language for communication and prose artifacts.

### 7) One authority per fact
Before writing or changing a value, rule, list, status or claim, find its single
authority inside or outside the repo. Derive computed facts; link or query other
authorities. Only test oracles and versioned reference data naming their source
are deliberate copies.

Put facts where their users act on them. Team choices belong in
`docs/WORKING-AGREEMENT.md`, or an ADR if hard to reverse. Newer decisions replace
older ones; remove superseded content and history-only notes from shipped files.
Define labels and prefer checks to prose. Resolve local evidence links relative
to the containing document and verify that their targets exist.

## Test scope

- During TDD, run the smallest selection covering the change. Use the UC plan and
  affected behavior; include impacted callers, integration boundaries and shared
  fixtures. Broaden when impact is uncertain.
- Rerun affected tests after refactoring. Code/tooling handoff requires passing
  `bash scripts/test.sh` evidence. Reuse a passing run for unchanged code,
  configuration and relevant environment; otherwise run it at handoff. CI and
  release retain full checks. A phase transition alone does not require a rerun.
- Prose-only changes need document/skill checks unless executable behavior or
  tooling contracts are affected.
- Record commands, scope, outcomes, skips and unavailable checks. A targeted pass
  proves that scope only. Missing required evidence means incomplete validation;
  linked CI may supply it for the same revision and required environment.

## Definition of done

The step fits its phase and slice, references requirements, labels assumptions,
passes applicable checks and includes required review evidence. Disclose unresolved
ambiguity and missing checks, obtain required authorization, and leave a coherent
handoff. Edited files alone do not establish completion.

## Stop and ask

Ask before proceeding when:

- Requirements conflict or remain ambiguous; priorities across slices are unclear.
- Architecture implications are non-trivial, or public interfaces, trust boundaries
  or security posture would change.
- Secrets, credentials or production-like sensitive data are involved.
- External best practices conflict with repo instructions in a way affecting delivery.
- Validation criteria cannot be safely inferred, or required access is unavailable.
- An unresolved assumption could change behavior, scope or architecture.
- The skill requires a higher model tier, or the same test fails after two fix attempts.

State the uncertainty, options and recommended next step.

## Git and review

- Follow the working agreement's branch convention. Commit to `main` only when
  the agreement or a human in this session allows it. Parallel agents use separate
  `git worktree`s.
- Push, merge, force-push and branch deletion require a human request in this session.
- Before committing, read `CONTRIBUTING.md` → "Commits"; use the change type from
  `docs/INDEX.json`. End agent commits with `Agent-Model: <model>` and
  `Agent-Tier: small|standard|large`.
- Before drafting a PR, read `.github/pull_request_template.md` and address its
  sections and applicable checklist, including for CLI/API submissions. Prepare
  documents in their intended merged state: an ADR submitted for acceptance may
  say Accepted, with acceptance established through the agreed review and merge.
  Keep exploratory ADRs Proposed and report only actual test and approval evidence.
- At use-case or conversation end, add once: "Optional: run
  `python3 scripts/sdlc.py review` to make your human check verifiable."
  Never run it yourself or write a `Reviewed-by:` line.

## Supporting guidance

`CONTRIBUTING.md` is the human workflow; agents need only its referenced sections.
Load `docs/STANDARDS.md` for security/quality checks (least privilege, secrets,
input validation and traceability), and `docs/AGENT-GUIDANCE.md` for supplementary
examples and response guidance when relevant. Read the
[canonical AI-SDLC documentation](https://docs.aisl.science/learning-and-resources/ai-sdlc)
when terminology or lifecycle responsibilities are unclear.
