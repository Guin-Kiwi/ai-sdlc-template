# Agent Guidance

Read [AGENTS.md](../AGENTS.md) first. Load this file for help sizing work,
explaining results or applying its review rules.

## Explain work for review

From the response and linked evidence, a reviewer should understand what changed,
why, how it was validated and what remains unknown. Name the requirement, phase,
affected files and intended outcome; connect completion claims to evidence.

When useful, structure a response as: goal, inputs consulted, plan, changes,
validation, assumptions/open questions, next smallest step. Keep enough detail
for review; this is an optional format.

## Choose a reviewable slice

Split work when it contains independently valuable changes, requirements remain
incomplete, architecture could be affected, or the work would be difficult to
review, validate or reverse. Keep implementation and its validation together even across files.

State the next task in one or two sentences. If that is not possible, narrow or
clarify it before execution.

For example, implementing a new field and checking its API-to-storage behavior
can be one slice; an unrelated navigation redesign should be separate.

## Apply external guidance

Use external sources to improve task structure, prompts, verification, security
and risk assessment. Apply the router's source-precedence and stop-and-ask rules
when guidance conflicts with project intent. Avoid expanding scope or adding
heavyweight process without agreement.

A standards reference should lead to a relevant decision or check. A citation
alone does not establish that a change satisfies it; see [Standards](STANDARDS.md).

## Recognize work needing review

Flag the risk when work affects authentication, authorization, secrets, trust
boundaries, integrations, data handling, deployment or release. Use [AGENTS.md](../AGENTS.md#stop-and-ask) to determine when approval is required.

Check for these warning signs: unsupported completion claims, unlabelled
assumptions, unnecessary rewrites or scope expansion, and skipped validation.
Resolve them against the source requirement and actual evidence.
