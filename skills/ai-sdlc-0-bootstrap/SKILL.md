---
name: ai-sdlc-0-bootstrap
description: Initialize or align a repository for AI-SDLC based on the intended system.
---

# PHASE 0 — BOOTSTRAP

Align the repository with the intended system. Clarify its purpose and framework
with the user; ask before proceeding if unclear. Python is established by ADR-000;
do not ask the user to choose a language.

## 1. Identify existing code and authoritative inputs

Inspect structure, dependencies, code and tests. Identify authoritative briefs,
requirements, models and supplied inputs; link them under Resources in
`docs/PROJECT.md`, noting relevant scope and versions. Distinguish approved requirements,
proposals and assumptions. Resolve conflicts affecting the first slice before
implementing it; recency alone does not establish authority.

## 2. Align structure

Reuse compatible structure. Ensure Clean Architecture layers under `src/app/`:
`domain/`, `application/`, `interfaces/`, `infrastructure/`; and `tests/unit/`,
`tests/integration/`, `tests/e2e/`.

The template supplies this skeleton, `__init__.py` files for test discovery and
`tests/unit/test_architecture.py` for dependency rules. Create only missing parts;
avoid duplication or unnecessary restructuring.

## 3. Dependencies

Inspect `requirements.txt` and `pyproject.toml`; reuse existing manifests and
create a minimal one only if missing.

Keep the Python/FastAPI default profile: devcontainer, `environments/python/`,
`scripts/setup-python.sh` and Python `.gitignore` entries. Setup copies
`requirements.txt`, `.python-version` and `.vscode/launch.json` into the project.
Adjust requirements for the chosen framework and commit the copied files. For a
non-Python project, stop and ask the user (ADR-000).

## 4. Define the project and working agreement

Update `docs/PROJECT.md`, or create it if missing. Cover purpose, architecture,
structure, resources and reference links, commands, and dependencies.

Confirm `docs/WORKING-AGREEMENT.md` with the owner/team. Retain suitable conventions
and resolve placeholders needed for the first slice. Record agreed choices there;
clarify unresolved conventions before relying on them. Link to its rules rather
than copying them elsewhere.

## 5. Cleanup with user confirmation

Identify unused files, irrelevant boilerplate and mismatched structure. Obtain
confirmation before cleanup or removal.

- Replace template instructions in project documents with project content rather
  than deleting the documents.
- Replace or remove template identity: README badges (AI-SDLC, DOI, arXiv),
  `MAINTAINING.md`, `CITATION.cff`, `.zenodo.json` and the template owner in
  `.github/CODEOWNERS`.
- Remove `docs/future/`, which contains template roadmap notes.
- Rewrite `README.md`: app purpose and run instructions first, then a short
  AI-SDLC development section linking `CONTRIBUTING.md`, `docs/specs/` and `docs/adr/`.
- Preserve `LICENSE` section 1 and its CC BY 4.0 attribution. Ask the team for its
  application licence and complete section 2.

## Completion evidence

Report the clarified objective, constraints, assumptions, smallest proposed slice
and open questions. State whether the repository is aligned with the intended
system. Record phase 0 and status in `docs/TASKS.md` per `AGENTS.md`.
