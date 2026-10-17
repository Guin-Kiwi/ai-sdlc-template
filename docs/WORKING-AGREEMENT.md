# Working agreement

Team conventions; humans and agents both follow this file; change it by team agreement.

## Workflow
| Topic | Agreement |
| --- | --- |
| Solo or team | TBD |
| Branches | One use case per branch and per PR, named `uc-NNN-<short-name>` (lowercase, same NNN as the UC file). |
| Review and merge | As the repository's imported ruleset requires; the rulesets the template ships are described under Repository setup in CONTRIBUTING.md. |
| Shared files | Shared files (`AGENTS.md`, `docs/PROJECT.md`, `docs/INDEX.json`, `.github/`) change in their own small PR, not mixed into feature work. |

## Conventions
| Topic | Agreement |
| --- | --- |
| Decision records | Record a consequential decision that is hard to reverse or spans use cases (e.g. data store, auth approach, framework, a break in the layer rules) in an ADR; otherwise, record it in the use case. |
| UC numbering | The issue number zero-padded to three digits (issue #42 → 042), otherwise the next sequential number (001, 002, …). |
