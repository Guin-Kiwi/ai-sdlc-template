---
mode: agent
description: Start or continue an AI-SDLC phase in this repository.
---

Follow `AGENTS.md`. Follow the context load order in AGENTS.md.

<!-- BEGIN GENERATED PHASE LIST -->
Phase: ${input:phase:bootstrap | specify | design | develop | validate | deploy}
<!-- END GENERATED PHASE LIST -->
Request: ${input:request:What should this phase deliver?}

Open the skill listed for the phase in docs/INDEX.json and follow it.
Set `docs/TASKS.md` to that phase with status in-progress. If the skill's
required input is missing, ask me before doing anything else.
