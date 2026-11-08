---
name: ai-sdlc-5-deploy
description: Verify or collaboratively define the deployment workflow.
disable-model-invocation: true
---

# PHASE 5 — DEPLOY

Verify the continuous deployment workflow for the validated artifact. Define
deployment together with the user.

## Verify or define the CD workflow

Inspect `.github/workflows/`.

For an existing CD workflow, verify:

- Triggers, deployment steps and required secrets.
- Which validated commit or artifact each path deploys, including manual paths.
- How to confirm the intended version is serving; availability alone may show
  an older version.

For stored-data or schema changes, plan compatibility, migration or reset, and
recovery before deployment. Record the decisions and required authorization.

Update only as needed; obtain confirmation before overwriting workflows.

If no CD workflow exists, ask for the deployment platform, propose a minimal
workflow and create it only after confirmation.

## Deployment constraints

Deploy only the app (`src/`, runtime dependencies, `LICENSE`); keep process files
in the repository. Never store secrets in the repository.

## Completion evidence

Report changes, validation, what remains out of scope and the next slice. State
whether the workflow was verified or updated.

Record phase 5 and status in `docs/TASKS.md` per `AGENTS.md`.
