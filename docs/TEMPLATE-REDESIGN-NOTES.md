# AI-SDLC Template Review — Snapshot

Oct 17, 2026 · @Ayla

## Snapshot

Everything below reflects both repositories on 17 October 2026, before any changes were made.

| Repository | Branch | Commit | Role |
| --- | --- | --- | --- |
| [Guin-Kiwi/ai-sdlc-template](https://github.com/Guin-Kiwi/ai-sdlc-template/tree/17b315c34ee9879aa7409dc37c593fa3a640925a) | main | 17b315c | Template under review |
| [Guin-Kiwi/pay-align-dev](https://github.com/Guin-Kiwi/pay-align-dev/tree/8343b2dae65b456e9d44f428fb7d090141867072) | main | 8343b2d | Team repo built from the template |

Open PRs in pay-align-dev at snapshot: #12, #17, #19, #20. Their branches were not read.

**Read in the template:** AGENTS.md, CLAUDE.md, CONTRIBUTING.md, README.md, all six SKILL.md files, one skill index.json, docs/INDEX.json, PROJECT.md, TASKS.md, STANDARDS.md, AGENT-GUIDANCE.md, UC-TEMPLATE, ADR-TEMPLATE, ADR-000, docs/future, all four workflows, rulesets (team, solo), CODEOWNERS, PR template, issue template, Copilot prompt and instructions, check-lifecycle.sh, test-lifecycle.sh, check-setup.sh, setup-skills.sh, test.sh, pr\_advisory.py, sdlc.py, .dockerignore, tests/unit/test\_architecture.py.

**Not read in the template:** scripts/tests/, .vscode/, environments/, .devcontainer/, setup-python.sh, release-tags.json, the other five index.json files, LICENSE, CITATION.cff, .zenodo.json, .gitignore.

**Read in pay-align-dev:** constants.py, payroll\_calculation.py, employment.py, test\_payroll\_calculation.py, test\_payroll\_golden.py, test\_architecture.py, PROJECT.md, calculations.md, UC-002, ADR-002, the PR list, diffs of #4 and #19, and the description of #16.

## Ayla's stated positions

These are the positions Ayla stated clearly, quoted as written. Questions she has not answered yet are listed under Open decisions.

| Position | Quote |
| --- | --- |
| The template creates too many branches and PRs | "I am noticing too many branches are being made with them template." |
| The problem is the template's behaviour, not the team repo | "My issue is not with the repo its the behaviour this template is producing in the repo of https://github.com/Guin-Kiwi/pay-align-dev/" |
| DRY applies to all code | "DRy should be for any code written." |
| Constants and inline comments are scattered and conflict with rules elsewhere | "I dont like how constants are being stored inside tests and in other places, in line commetns seem to be overwriting some rules established in other places." |
| Specs should ship with code so reviewers see the implications | "I think it would be better to also have code in the PR so you can see the reality rather than just specs and the concept" |
| The goal is to enhance the template, possibly rewriting skills | "I want to try to enhance the ai-sdlc template in ways that reduces these issues or at least aligns some docs, perhaps skill should be rewritten." |
| ADRs need a reason to be read, not a standing expectation | "it would be good if they were referenced somewhere, with a reason to read them rather that expectation to read them everytime" |
| A dedicated pre-PR check for documentation linkage | "it would be great if there was a skill to check the documentation linkage, one specific skill which you run before making a PR, or a step in a PR skill" |
| The check must catch doc drift and code-doc mismatch, not just template conformance | "I need something to check the links between docs, so we dont have doc drift, and that changes actually match the docs." |
| Think in processes | "I think we need to try to think in processes" |
| Express an expected workflow instead of black-and-white categories | "I think I want a better expected workflow expressed, and not try to define which which is"fast track" or needs a new branch, it feels too black and white" |
| Bootstrap should ask how the team works | "is this a team or a solo project, will you work together on the same branches, UC or tier based , or do you prefer to keep branches to one person?" |
| Bootstrap should ask who may commit to main | "can anyone commit to main, can humans commit to main." |
| Team TASKS should be fragmented | "I think for any team work Tasks needs to be fragmented, like tasks-username or tasks-arch or tasks-ucNNN" |
| TASKS.md becomes a router, set at bootstrap | "TASKS.md can be something which explains where tasks live, an can be modified automatically during the bootstrap session" |
| Agents should ask for and infer naming conventions | "Id also like some nomenclature prompts, or rules, and the agents to ask which names are preferred, it might also be inferrable at the bootstrap stage" |
| Enforcement level is itself a bootstrap question | "I feel like your question is also a question for bootstrapping" |
| Bootstrap should work like refinement, including language questions | "it would be nice if bootstrapping was more like refinement, it could even ask, what language should notes be in?" |
| Split bootstrap into mandatory and QOL questions | "I think we should have some mandatory questions and QOL questions" |
| Agrees with the mandatory/QOL line | "I think you have drawn a pretty good line." |

She also called the slice-lifecycle versus fact-lifecycle framing helpful ("this helps clarify things"), without adopting it as a decision.

## What the template produced in pay-align-dev

The same payroll rules are written in at least five places, and several of those places disagree.

**Constants**

- Rates and limits sit in `constants.py`, but `HOLIDAY_PREMIUM_RATE` is defined in `payroll_calculation.py`.
- The NBU threshold is a bare `8` in `calculate_employee_deductions`.
- `holiday_entitlement` defaults to `20` in `employment.py`.
- `test_payroll_calculation.py` retypes rates and formulas as literals and comments (`4000 * 0.053`).
- `len(PUBLIC_HOLIDAYS_2026) == 9` restates the constant. The annual-limit test's 18000, 50000 and 11000 only work against limits in another file.
- ADR-002 rejected "unversioned global constants", yet `constants.py` is exactly that.
- UC-002 restates the rates, the CHF limits and the 8-hour threshold.
- The golden test is the right pattern: expected values come from workbook fixtures.

**Comments that override or duplicate rules**

- Admin charge: `calculations.md` and the code use employer AHV × 5%, the workbook uses gross × 10.6% × 5%. Two tests assert opposite values, held together by `@expectedFailure` and a docstring.
- `employment.py` says `# Annual paid holiday days (default: 20)`, while the ADR-004 amendment (open in #19) replaces that field.
- `TODO(PR #3 review) … Owner: Aaron` repeats PROJECT.md. PR #16 existed to delete `TODO(PR #13 merge)` blocks.

**Spec-only PRs**

- \#4 (three ADRs) and #19 (ADR-003 and ADR-004 amendments) contain only docs.
- \#19 changes nine facts; its only trace of the code impact is one closing consequence.
- \#19 and #20 (the saving schema) are open in parallel, though #19 changes what #20's schema should be.

**Doc drift**

- PROJECT.md's Structure lists `src/domain/`; the repo has `src/app/domain/`.
- UC-002 has three hour categories; the ADR-004 amendment has four.
- PROJECT.md's Commands section is in German; the rest is English.
- UC file names use Title-Case; the specify skill asks for uppercase.

**Possible gap (read, not run):** `test_architecture.py` only flags imports starting with `app.`, but pay-align-dev imports `src.app.…`.

## Causes in the template

The template splits docs from code by rule, has no home for conventions, and never routes agents to ADRs.

- **Specify and design forbid code.** Specify says "Do not generate code or tests"; design says "Do not implement code" and "Do not generate tests". Phases 1–2 can only produce docs.
- **Fast Track always branches.** Specify creates `fix-<name>` or `docs-<name>` before writing anything, so a one-line correction becomes a branch and a PR.
- **Shared files get their own PR.** CONTRIBUTING sends AGENTS.md, PROJECT.md, INDEX.json and `.github/` to separate PRs "not mixed into feature work". PROJECT.md is classed as project, not review-gated, in INDEX.json.
- **Branch rules are decided by change type.** CONTRIBUTING's commit / Fast Track / use case / ADR ladder decides branches, not dependency or readiness.
- **REFACTOR has no criteria.** The develop skill names RED→GREEN→REFACTOR but defines nothing for the refactor step.
- **ADRs sit outside the chain.** AGENTS.md's load order and conflict ranking stop at the UC. Develop's sources are TASKS, UC and PROJECT only.
- **No home for conventions.** Durable rules belong in AGENTS.md, which is review-gated. pay-align-dev's AGENTS.md is byte-identical to the template's, so no ADR rule was ever promoted there. This may push rules into comments (unverified).
- **Language follows the prompt.** AGENTS.md writes artefacts in the current prompt's language, which produced mixed-language docs.
- **Single TASKS.md per branch.** It describes only that branch's use case, so it conflicts on every merge.
- **The template's own scripts restate rules.** `pr_advisory.py` hard-codes Fast Track exclusions and the `fix-`/`docs-` prefixes as constants.

## Layers and dependencies

A skill should own only how to do its phase and take every fact from the layer that owns it, with a pointer that says what to look for.

&#91;embedded content: template layers · what points to what\]

ADRs and reference docs are the only layer no skill names as a source; they are reached only when PROJECT.md or a UC happens to link them.

**Missing links**

1. ADRs and domain rules sit outside the load order and the conflict ranking, so disagreements have no tie-breaker.
2. Conventions have no home, and the designated home for durable rules (AGENTS.md) is review-gated.
3. Skills forbid the evidence reviewers need: specify and design ban code, REFACTOR has no criteria.

**When a skill should point rather than state**

- Cross-phase rule → once in AGENTS.md; skills point.
- Phase procedure → in the skill.
- Project fact (commands, structure, conventions) → PROJECT.md; skills point.
- Decision with alternatives → ADR; PROJECT.md states the outcome and links it.
- Slice requirement → UC; skills never restate values.
- Domain rule values → one reference doc; UCs cite a section, code has one implementation, tests use independent fixtures.
- Status → TASKS only, never PROJECT.md or code comments.

A pointer costs a file load, so the middle path is a pointer plus one line naming what to read it for.

## Proposals discussed

The proposals share one idea: each fact has one home, and everything else points to it with a reason to look.

**Read-when index for ADRs and reference docs**

- PROJECT.md gets a Decisions section with one line per ADR: title, status and a "read when" trigger.
- Resources gets the same "read when" per reference file.
- At SPECIFY or DESIGN the agent matches the slice against the index and cites the matches in the UC's "Notes for implementation".
- Develop already reads the UC, so its source list and AGENTS.md may not need to change.
- Triggers must name something visible (a noun in the UC, a kind of change); "when relevant" fails.

**Linkage check before a PR**

- Mechanical checks belong in a script: links resolve, every ADR is indexed, Structure matches folders, no `TODO(PR #…)` in code.
- Judgement checks belong in a skill: contradictions between docs, restated values, wrong ADR citations, stale triggers.
- A combined option runs the script first and then a semantic pass over docs touched by the diff.
- `sdlc.py` does none of this; it records a human's review answers as a commit.

**Two lifecycles**

- *Slice lifecycle* (what the template has): specify, design, develop, validate, deploy.
- *Fact lifecycle* (missing): a fact is defined, cited, implemented, verified and changed. "Changed" has no process; PR #19 shows the gap.

**Workflow by dependency, not change type**

- A branch isolates work not ready for `main`; it ends when `main` stays coherent.
- Wait only when an unsettled decision would change structure; otherwise continue with a written assumption behind an interface.
- Open a draft PR early when others must agree before building on it.
- Park side findings in tasks rather than branching automatically.

**Bootstrap as refinement**

- Bootstrap proposes defaults, infers from the repo, asks the rest and records each answer once.
- Mandatory questions start as `TBD`, which the existing check already blocks. QOL answers are marked `default` or `confirmed`.
- Criterion: mandatory if a wrong default is hard to undo or changes how others work.
- Later phases ask unanswered questions just in time, then record them.

| Mandatory | QOL | Borderline |
| --- | --- | --- |
| Purpose and framework | Naming patterns | Naming on a fresh repo |
| Solo or team | Notes and comments language | Code identifier language |
| Who may commit to `main` | Enforcement level per check | Enforcement levels in general |
| Branch model | Commit prefix style |  |
| TASKS layout | Glossary seeding |  |
| Artefact language | Model tier habits |  |
| Who approves decisions |  |  |
| Licence |  |  |

**TASKS.md as a router**

- TASKS.md declares a layout (`single` or `per-thread`) and lists active threads.
- Thread files live in `docs/tasks/`, one per UC or area, naming owners and branch.
- `check-lifecycle.sh` must follow the pointer; it currently parses TASKS.md directly.
- Skills say "the current use case" in the singular; the agent needs a branch-to-thread link.

**Nomenclature and language**

- Four kinds of name: process names, code names, domain terms and artefact language.
- Bootstrap infers conventions in an existing repo and asks only what it cannot infer.
- Language splits into conversation, artefacts, code identifiers and comments.

## Brainstorm list (unevaluated)

These ideas were generated for breadth and have not been judged.

**Link integrity**

- Markdown link checker over `docs/` (paths and anchors)
- Every ADR in the Decisions index, and every entry has a file
- Resources and `docs/reference/` match both ways
- ADR citations in UCs resolve
- Generated backlinks: each ADR lists the UCs and code citing it
- Orphan finder for unlinked docs
- `# see ADR-003` comments in code validated
- PROJECT.md Structure checked against folders

**Drift between docs**

- One rules file that doc tables are rendered from; UCs cite by key
- Number scanner: the same percentage or CHF amount in more than one doc
- ADR status checked against index and PROJECT.md
- Supersede-chain checker
- Glossary as the single definition source
- "Verified against commit X" field per doc
- Per-doc owner in CODEOWNERS
- Phase list generated once for all its copies

**Changes matching docs**

- Code↔doc map with a PR advisory when one side changes alone
- Docs-only PR warning
- Acceptance-criterion IDs with tagged tests, checked both ways
- Golden fixtures generated from the workbook, failing if stale
- Test asserting the code ruleset equals the rules file
- AST scan for numeric literals outside the ruleset and fixtures
- Comment linter for numbers, "must" or `TODO(PR #…)`
- Docstrings link formulas instead of restating them
- Semantic skill comparing docs against changed symbols
- Second-model review with a drift prompt
- Public signatures recorded in docs with a diff check
- "Change this constant" impact report

**Process hooks**

- SYNC sub-step between DEVELOP and VALIDATE
- Pre-commit hook running the linkage script
- Sixth review-report question about touched docs
- PR template checkbox filled by the script
- Drift report posted as a PR comment
- Weekly scheduled drift job on `main`
- Known drifts tracked as debt in TASKS
- ADR amendments must name their implementing PR

**Wild**

- Docs hold no hand-typed values; all rendered from code or the rules file
- Code generated from spec tables
- Paragraph IDs that code comments must cite
- Regenerate the UC from code and diff it
- Untraceable doc claims fail CI
- Knowledge graph where drift shows as broken edges

## Plan sketch

Eight steps, each a PR carrying its own docs and code; owners are TBD for every step and no deadline is set.

**Scope**

- **Goal:** the template produces DRY code, keeps docs linked to code, and configures its workflow at bootstrap.
- **Fixed:** Ayla is the only code owner of every review-gated path in the template.
- **Gated:** AGENTS.md, CLAUDE.md, CONTRIBUTING.md, INDEX.json, CODEOWNERS, workflows, rulesets, `sdlc.py`.
- **Not gated:** skills, PROJECT.md, TASKS.md, UC-TEMPLATE, other scripts.
- **Flexible:** order of steps 4–6 and the tooling choices.

**Sequence**

1. **Template ADR** recording the redesign. Every later step points to it.
2. **Answer homes:** Workflow, Conventions and Decisions sections in the PROJECT.md template, plus "read when" in Resources. Everything else points here.
3. **Bootstrap as refinement** with a question bank. Depends on 2.
4. **Skill pointer pass:** pointers instead of restated rules; specify and design may produce code or tests per Workflow; REFACTOR criteria; UCs cite ADRs. Includes the gated AGENTS.md changes. Depends on 2 and 3.
5. **TASKS router** plus `check-lifecycle.sh` and its tests. Depends on 3. Riskiest: the path is wired in everywhere.
6. **Mechanical linkage script** in `test.sh`. Depends only on 2, so it can run in parallel with 4 and 5.
7. **Semantic pre-PR skill** using the script's output. Depends on 6.
8. **Pilot in pay-align-dev,** a team decision since it changes their workflow mid-capstone.

**Risks that could shift the plan**

- No automatic sync from template to derived repos; step 8 is a manual merge.
- UC-TEMPLATE heading changes fail every existing UC in derived repos.
- A new template ADR-001 collides with pay-align-dev's ADR-001 under the duplicate-number check.
- Steps 5–7 are Python; writing them with scaffolding is the slowest part.
- CONTRIBUTING's "shared files in their own PR" rule conflicts with code-and-docs-together PRs until changed.

## Single source of truth map

Each doc owns one kind of fact; a duplicate is allowed only as a checked copy that a script verifies.

| Doc | SSOT for | Points to | Pointed to by | Change |
| --- | --- | --- | --- | --- |
| AGENTS.md | Cross-phase agent rules: load order, precedence, stop-and-ask, git rules, the DRY rule | INDEX.json, TASKS, PROJECT, STANDARDS, AGENT-GUIDANCE | CLAUDE.md, Copilot files, every skill | Gated: drop phase list, language rule as pointer, add precedence and DRY rule |
| CLAUDE.md, copilot-instructions.md | Nothing (adapters) | AGENTS.md | Tools | None |
| ai-sdlc.prompt.md | Nothing; phase dropdown is a checked copy | AGENTS.md, INDEX.json, skills | Copilot | Checked copy |
| docs/INDEX.json | Phase→skill map, gated paths, templates, project/process split | Listed paths | AGENTS.md, check-lifecycle, prompt, pr\_advisory | May host the ADR index (open) |
| CODEOWNERS | Who must review | None | GitHub | Paths are a checked copy |
| Rulesets JSON | Branch protection, minus bypass | None | GitHub import | Bypass set in GitHub settings |
| CONTRIBUTING.md | Human how-to | AGENTS.md, PROJECT.md Workflow | README | Gated: rules become links |
| STANDARDS, AGENT-GUIDANCE | Standards rationale, heuristics | None | AGENTS.md | None |
| docs/PROJECT.md | Project-wide facts plus Workflow, Conventions, Decisions index, Resources with read-when | ADRs, reference docs, glossary | AGENTS.md, skills; bootstrap writes it | Three new sections, answers marked confirmed or default |
| docs/TASKS.md | Layout mode and active threads; full state in solo mode | Thread files | AGENTS.md, INDEX.json, skills, check-lifecycle | Router |
| docs/tasks/\<thread>.md (new) | One thread's phase, status, slice, blockers, next step, owners, branch | Its UC or area | TASKS.md, check-lifecycle | No acceptance or evidence |
| UC-NNN.md | Slice requirements, acceptance criteria, evidence | Reference sections, glossary, ADRs | Thread file, tests | Cites values instead of restating |
| ADR-NNN.md | One decision with status, approvers, confirmation | Code and tests in its confirmation, related ADRs | Decisions index, UCs | Template gains a confirmation section |
| docs/reference/\* | Domain rule values and formulas | None | Resources, UCs, code ruleset, fixtures | Only prose home for values |
| glossary.md (new, QOL) | Domain term definitions | Reference docs | UCs, Conventions | Optional |
| skills/\*/SKILL.md | Phase procedure only | AGENTS, PROJECT, UC, thread file | INDEX.json, prompt, tools | Pointers instead of restated rules |
| Bootstrap questions.md (new) | Questions, mandatory or QOL, defaults, answer destinations | PROJECT.md, TASKS.md | Bootstrap SKILL.md | New |
| Pre-PR skill (new) | Semantic-check procedure | Script output, UC, ADRs, reference | AGENTS.md or CONTRIBUTING | New |
| UC-TEMPLATE, ADR-TEMPLATE | Section structure | None | Specify, design, check-lifecycle | UC heading changes break derived repos |
| check-lifecycle.sh | Structural rules | INDEX.json, TASKS, thread files, UC-TEMPLATE | test.sh | Follows the router |
| Linkage script (new) | Mechanical link rules | What it checks | test.sh, pre-PR skill | New |
| Template ADR (new) | Why this redesign | AGENTS, PROJECT template, skills | Maintainers | Needs its own numbering |

Project-side homes, named in Conventions rather than shipped: a ruleset module in `src/app/domain/` as the single implementation of reference values, and `tests/fixtures/` for independent expected values.

## DRY review

The plan is DRY in intent but not in method: it mostly polices duplicates, adds about eight artefacts, and leaves the template's own duplication untouched.

**The template's own duplication**

| Fact | Copies | Where |
| --- | --- | --- |
| Fast Track rules | 7 | AGENTS.md, CONTRIBUTING, four skills, constants in pr\_advisory.py |
| Phase list | 7 | AGENTS.md, INDEX.json, each skill's index.json, Copilot prompt, README, TASKS.md legend, CONTRIBUTING tier table |
| Project vs process files | 4 | INDEX.json, README table, .dockerignore, AGENTS.md |
| "Deploy only the app" | 4 | .dockerignore, validate skill, deploy skill, README |
| Review-gated list | 4+ | INDEX.json, CODEOWNERS, gated-file headers, PR template |
| Skill identity | 3–4 per skill | Folder, SKILL.md name, index.json name, phase and goal |
| Bootstrap checklist | 3 | bootstrap.yml issue body, bootstrap skill, CONTRIBUTING setup |
| Load order | 2 | AGENTS.md, Copilot prompt |
| CI verify steps | 2 | ci.yml and release.yml; check-lifecycle also runs twice per job |
| UC fields | 2 | Issue template, UC-TEMPLATE |
| TASKS.md structure | 2 | TASKS.md, test-lifecycle.sh fixture writer |
| git helper | 2 | sdlc.py, pr\_advisory.py |

Two implicit couplings: `bootstrap.yml` greps a PROJECT.md sentence that bootstrap deletes, and `main-team.json` requires a check named `structure`, matching `ci.yml`'s job name.

Already done well: skills record status "per AGENTS.md", commands come from PROJECT.md, check-lifecycle derives UC headings from UC-TEMPLATE, pr\_advisory reads gated paths from INDEX.json, and sdlc.py imports its trailer parser.

**Where the plan falls short**

- `pr_advisory.py` would contradict step 4: softening Fast Track in docs leaves the script enforcing the old rule.
- "Checked copies" keep duplication and catch drift late.
- Thread files duplicate UCs; a state block inside the UC is DRYer for UC threads.
- New surfaces only pay off if each removes more copies than it adds.
- "Who can commit to main" would live in rulesets, CONTRIBUTING and PROJECT.md Workflow.
- Enforcement levels really live in the scripts unless the scripts read them from config.

**Four strategies for each duplicate**

| Strategy | Gains | Costs | Fits |
| --- | --- | --- | --- |
| Eliminate | Fewest places to edit | More agent file loads; terser human docs | Load order, Fast Track prose, "deploy only the app", bootstrap checklist |
| Generate | Readable copies, no drift | Generator script; regeneration PRs for gated files | Phase list, Decisions index, CODEOWNERS paths, README artefact table |
| Check | Cheapest to start | Duplication stays; drift caught late | CI job ↔ ruleset name |
| Config the code reads | Rule lives once and is enforced | Parsing work in scripts | Fast Track rules, enforcement levels, branch prefixes |

Some duplication is deliberate: README and CONTRIBUTING serve students and assessors. A human summary with a link is defensible; one that restates a rule is not.

`docs/future/SKILL-DESIGN-SOURCES.md` tests new skills: recurs across two or more phases, stable steps, removes meaningful duplication. The pre-PR skill likely passes; folding it into validate would add no artefact.

Suggested first slice (not yet agreed): remove the template's own duplication with these strategies before adding anything new.

## Thinking since the snapshot

Organising sources by data class leaves about eight hand-edited sources; everything else is a link or a generated view that CI checks.

Where this section differs from an earlier section, this section is current.

**Positions stated after the snapshot**

| Position | Quote |
| --- | --- |
| Fewer sources of truth means fewer issues | "realistically minimal sources of truth minimizes issues." |
| Ungated docs could hold the truth, gated docs the connectors | "Can we not reverse it so that ungated docs hole fthe truth and gated docs hold the connectors" |
| Change data means recorded changes to master data, to stop agents keeping redundant code alive | "by change data I think I meant when master data changes, so that descisions are known, and to hopefully minimise the AI tendancy to want to make legacy code operatioonal, even when its been made redundant and should be trimmed not build with supporting it in mind" |
| Both UCs and ADRs may retire things | "I would say yes, either can retire things" |
| PROJECT.md must not grow too large | "My worry is that PROJECT will start to get too big" |
| Avoid a sudden sprawl of files and new duplication | "I just worry we are going to end up with many many doc files again all of a sudden, with duplciations again" |

**Data classes**

| Class | Changes when | Handling |
| --- | --- | --- |
| Reference | Rarely: per legal year or template version | Versioned; a change is a new version |
| Master | Bootstrap, phase boundaries, decision changes | One home each; changes ripple through a change record |
| Change (master changes) | When a decision supersedes another | Front matter of the superseding record |
| Transactional | Every session, commit, PR | Per thread; never copied into master data |
| History | Automatically | Git; never hand-written |
| Metadata | When structure changes | Generated where possible |

Many issues are data in the wrong class: PR numbers and owners in code comments, status in PROJECT.md, rates restated in UCs and tests, amendment history inside ADR-004.

**Hand-edited sources**

- Template-owned (gated where it routes everyone's process): `INDEX.json` as the process registry, AGENTS.md rules, skills, UC and ADR templates.
- Project-owned (ungated): PROJECT.md, the working agreement, UCs, ADRs, the versioned ruleset data, reference prose, thread files, glossary.
- Gating rule: template-owned and rarely changed, not "connector". This mostly confirms Ayla's reversal; `INDEX.json` is gated template truth.

**Generated views**

- Generated regions sit between HTML comment markers; a script fills them from the source and a `--check` run in CI fails on any mismatch.
- Copies, not includes: GitHub does not expand includes and agents read raw files.
- Generated means never edited by hand; merge conflicts inside a region are resolved by regenerating.
- Registries are hand-edited; indexes are views. The Decisions index comes from ADR front matter, Resources from reference-doc front matter, the TASKS thread list from thread files, and the README, prompt and CODEOWNERS copies from `INDEX.json`.
- Candidate tool: Cog (Python, `--check` mode). Alternative: a standard-library script. Undecided.

**Change records and retirement**

- The superseding UC or ADR carries `supersedes` and `retires` in front matter, with retire, version or migrate per item.
- Lifecycle: deprecated until a date (code still works and warns, if callers need it), then retired (deleted; tombstone records the last commit), then restore only through a human-reviewed restore entry.
- Commenting code out as a grace period was proposed by Ayla; the counter-proposal above uses the change record instead. Not yet agreed.
- Tombstones are computed from front matter by the check script; no separate hand-edited list.
- Agent rule, once in AGENTS.md: retired means deleted, with no shims or fallbacks unless the record says version or migrate.

**Working agreement**

- `docs/WORKING-AGREEMENT.md` holds Workflow and Conventions and absorbs TASKS.md's Working agreement section. The name is proposed, not agreed.
- Split by kind, not audience: CONTRIBUTING.md keeps generic procedure; the working agreement holds the team's answers for humans and agents alike.
- PROJECT.md stays small (purpose, architecture, structure, commands) because it is loaded on nearly every task.

**Test oracles**

- Expected values must come from a source the code does not read, and the fixture names that source. This is the one duplication kept on purpose.
- Generating fixtures from the code's own ruleset would make tests agree with the code's mistakes.
- Tests should name the rule they check and include boundary values (exactly 8 hours, exactly the limits).

**File budget rule (proposed)**

A new file must remove at least one existing copy or hold a data class that has no home yet. On that test the pre-PR check becomes a step in validate, not a new skill.

**Settled since the snapshot**

- The read-when trigger lives in ADR front matter; the Decisions index is generated.
- Both UCs and ADRs may retire things.
- First Codex slice: `INDEX.json` becomes the single source for the phase list and skill metadata. On 17 October Codex stopped before making changes because this notes file was not yet in the repo.

## Open decisions and unverified items

None of these has been decided; each needs an answer before the step that depends on it.

**Open decisions**

- [ ] Should specs stay reviewable before code exists, or be reviewed only once code is in the PR?
- [ ] Where does the generated Decisions index live: its own file (proposed, to keep PROJECT.md small) or a PROJECT.md section?
- [ ] Settled: the read-when trigger lives in ADR front matter and the index is generated.
- [ ] How does an agent know its thread: branch name, user statement, or a TASKS assignment?
- [ ] Does an accepted ADR win over a UC when they disagree?
- [ ] May accepted ADRs be amended, or must they be superseded? ADR-TEMPLATE says supersede, not delete; pay-align-dev amended ADR-004.
- [ ] Link checking: lychee (a Rust binary, new dependency) or a Python stdlib script?
- [ ] Does the enforcement vocabulary (Block, Warn, Info) move from CONTRIBUTING to AGENTS.md?
- [ ] Does a UC thread keep state in its own task file or inside the UC?
- [ ] Which numbering namespace do template ADRs use, to avoid colliding with derived repos?
- [ ] Is the first slice removing the template's own duplication?
- [ ] Do changes stay in this copy, or go upstream to the template authors (Andreas Martin and Sandro Schwander, FHNW, CC BY 4.0)?
- [ ] When does pay-align-dev adopt changes, if at all?
- [ ] Is there a deadline?

**Unverified**

- The `src.app` import gap in `test_architecture.py` was read, not run.
- Whether gated AGENTS.md is why rules ended up in comments is a hypothesis.
- Whether a ruleset JSON import honours `bypass_actors`: the files carry the field (empty), but GitHub excludes bypass lists from exports.
- Files listed as not read in the Snapshot.

## Sources

These pages were seen through search results, not read in full; open them before relying on details.

| Source | Clarifies |
| --- | --- |
| [GitHub: managing rulesets](https://docs.github.com/organizations/managing-organization-settings/managing-rulesets-for-repositories-in-your-organization) | Bypass lists by role, team or app; bypass lists are excluded from exported JSON |
| [GitHub community: bypass list behaviour](https://github.com/orgs/community/discussions/150269) | Community report that bypass is a case-by-case opt-out, not an exemption (unofficial) |
| [trunkbaseddevelopment.com: short-lived feature branches](https://trunkbaseddevelopment.com/short-lived-feature-branches/) | Branches not shared within a team; more than two days risks a long-lived branch |
| [Mergify: short-lived branches in practice](https://mergify.com/learn/trunk-based-development/short-lived-branches) | Stacked PRs, branch by abstraction, feature flags, splitting by execution path |
| [Claude Code: skills](https://code.claude.com/docs/en/skills.md) | A skill is a folder with SKILL.md plus supporting files; follows the Agent Skills open standard |
| [MADR](https://adr.github.io/madr/) | Decision makers, a Confirmation section for how a decision is verified, supersede instead of amend |
| [lychee](https://github.com/lycheeverse/lychee) | Link checking for Markdown with relative links and anchors; CLI and GitHub Action; offline mode |
| [GitHub community: syncing template changes](https://github.com/orgs/community/discussions/23528) | No automatic updates from a template to repos created from it |
