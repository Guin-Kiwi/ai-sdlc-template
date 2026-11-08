---
name: ai-sdlc-4-validate
description: Verify repository readiness for release.
---

# PHASE 4 — VALIDATE

Changes whose type needs no spec skip SPECIFY and DESIGN; see the change types in `docs/INDEX.json`.

## Goal

Verify that the repository is ready for its declared release path.

Focus on **checking existing artifacts**.

---

## Source of Truth

docs/TASKS.md  
docs/PROJECT.md  

---

## Steps

### 1. Run Local Tests

Apply `AGENTS.md`'s test-scope policy. Review available results against the active
UC and required environment. Reuse applicable successful runs, including DEVELOP
or CI evidence; run `bash scripts/test.sh` if full-suite evidence is missing or
stale. Run additional declared checks only when not already covered.

Record failures, skips and unavailable dependencies. A passing subset or skipped
required check does not establish release readiness.

---

### 2. Verify E2E Tests when declared

Review the active use case’s validation plan and demonstrate each applicable
user-facing journey using its specified automated or manual evidence. Record
any incomplete or deferred journey; do not claim it is complete from backend
checks alone.

If `docs/PROJECT.md` declares an E2E command or an E2E release requirement,
check:

tests/e2e/

Extend existing tests if needed. If E2E automation is not declared, record it as not applicable; this does
not replace the journey evidence specified above.

---

### Evaluate runtime AI when applicable

If the application uses an AI model at runtime, follow the active UC's declared
evaluation plan as well as its software tests. Tests with a model substitute
verify application behavior; they do not establish the live model's quality.

Record the model and prompt versions or identifiers, input/reference provenance,
expected-outcome basis, actual results and limitations. Keep evaluation labels
out of model inputs unless the experiment deliberately requires them. Distinguish
live runs, synthetic scenarios and recorded replays. Assess model outputs and
downstream rule execution separately so correct routing does not conceal an
incorrect assessment. Report unrun evaluations as incomplete.

Run external calls within the project's agreed access and usage budget; ordinary
CI need not make paid model calls. This section does not apply merely because
coding agents were used to develop the application.

---

### 3. Verify the declared artifact

If `docs/PROJECT.md` declares a container artifact, check:

Dockerfile

Verify the container builds and starts the application, and that the image
contains only the app (`src/`, runtime dependencies, `LICENSE`); the root
`.dockerignore` already excludes the process files. If no container or other
build artifact is declared, record the artifact check as not applicable.

---

### 4. Verify CI

Check:

.github/workflows/ci.yml

CI and release run `scripts/test.sh`. Create or update it so it runs:

- unit tests
- integration tests

using the commands documented in `docs/PROJECT.md`. Do not add a separate test
workflow. `scripts/test.sh` ships running `tests/` with `pytest`, and CI installs
the project's requirements first.

---

### 5. Verify Release Workflow

Check:

.github/workflows/release.yml

Verify it runs `scripts/test.sh` and publishes the artifact declared in
`docs/PROJECT.md`, when one exists. Verify the declared E2E checks there as
well. A template repository with no application artifact may publish a source
release and record container/E2E checks as not applicable.

Create only if missing.

---

## Rules

- Prefer **verifying and extending existing artifacts**.
- Create files only if they do not exist.
- Avoid duplicate workflows.

---

## Evidence to provide

- summary of what changed
- what was validated
- what remains out of scope
- recommended next slice

---

## Output

Applicable release checks pass with evidence for the revision being released.
Report missing required checks as incomplete validation.

Write the actual evidence (checks run, results, links) into the active UC
file's "Evidence" section, so it stays with the use case after
`docs/TASKS.md` moves on. Record phase 4 and status in `docs/TASKS.md` per
`AGENTS.md`.
