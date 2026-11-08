---
name: ai-sdlc-4-validate
description: Verify repository readiness for release.
---

# PHASE 4 — VALIDATE

Verify release readiness against `docs/PROJECT.md` and the active UC's validation
plan. Inspect existing artifacts first; update only where needed and create
files only if missing. Avoid duplicate workflows.

Changes needing no spec skip SPECIFY and DESIGN; see `docs/INDEX.json`.

## Check test evidence

Apply `AGENTS.md`'s test-scope policy. Match evidence to the revision and required
environment. Reuse applicable DEVELOP or CI results; run `bash scripts/test.sh`
when full-suite evidence is missing or stale. Run uncovered declared checks.
For example, a full run's unit results do not need a separate unit rerun.

Record failures, skips and unavailable dependencies. A passing subset does not
satisfy a required check that failed or did not run.

## Demonstrate user journeys

Demonstrate each applicable UC journey with its planned automated or manual
evidence. Backend checks alone do not establish a complete user journey.

If E2E automation is declared, inspect and extend `tests/e2e/` as needed.
Otherwise mark automation not applicable and use a manual demonstration where
appropriate. Missing automation alone does not defer the journey. Record any
incomplete or deferred journey explicitly.

## Evaluate runtime AI when used

For applications using AI at runtime, execute the UC's evaluation plan as well
as software tests. Model substitutes test application behavior, not live model
quality. Coding-agent use alone does not trigger this section.

Record model/prompt versions or identifiers, input/reference provenance, the
basis for expected outcomes, actual results and limitations. Keep evaluation
labels out of model inputs unless deliberately required by the experiment.
Distinguish live runs, synthetic scenarios and replays. Evaluate model outputs
and downstream rules separately. Report unrun evaluations as incomplete.

Keep external calls within agreed access and usage budgets; ordinary CI need
not make paid model calls.

## Verify the declared artifact

For a declared container, inspect `Dockerfile` and verify build, app startup and
runtime contents: `src/`, runtime dependencies and `LICENSE`. Process files stay
outside the image via `.dockerignore`. If no build artifact is declared, record
this check as not applicable.

## Verify CI and release

Inspect `.github/workflows/ci.yml` and `.github/workflows/release.yml`. Both must
run `scripts/test.sh` with the documented unit/integration checks. Update that
entrypoint as needed; it ships running `tests/` with pytest, after CI installs
dependencies. Do not add a separate test workflow.

Verify release publishes the declared artifact and includes declared E2E checks.
A template without an application artifact may publish a source release and
mark container/E2E checks not applicable. Create a release workflow only if missing.

## Record completion evidence

Write commands, results and evidence links in the UC's Evidence section so they
remain available after `docs/TASKS.md` advances. Report changes, validation,
what remains out of scope and the next recommended slice.

Declare readiness only when required checks pass for the release revision.
Otherwise identify the failed check or missing prerequisite and the next action.
Use that result to update phase 4 and STATUS in `docs/TASKS.md` under `AGENTS.md`'s
status rules; include the reason and next action in the handoff.
