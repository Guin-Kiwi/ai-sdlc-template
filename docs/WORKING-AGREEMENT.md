Team conventions; humans and agents both follow this file; change it by team agreement.

## Decisions

Record a consequential decision that is hard to reverse or spans use cases
(e.g. data store, auth approach, framework, a break in the layer rules) in an
ADR; otherwise, record it in the use case.

## Branches

One use case per branch and per PR, named `uc-NNN-<short-name>` (lowercase,
same NNN as the UC file).

## UC numbering

Use the GitHub issue number or the next free number; the team picks one way so
numbers do not clash.

## Review and merge

Every change to `main` goes through a PR with one teammate's approval and
passing CI, with the branch up to date with `main`; the author merges with
available merge options.

## Shared files

Shared files (`AGENTS.md`, `docs/PROJECT.md`, `docs/INDEX.json`, `.github/`)
change in their own small PR, not mixed into feature work.
