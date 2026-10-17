#!/usr/bin/env python3
"""Advisory checks for a pull request. Prints warnings and notices; never fails.

Usage: python3 scripts/pr_advisory.py BASE_SHA HEAD_SHA BRANCH
"""

import json
import os
import re
import subprocess
import sys

TIERS = ("small", "standard", "large")

AGENT_CO_AUTHOR = re.compile(
    r"^co-authored-by:.*\b(claude|copilot|codex|gpt|gemini|cursor|agent)\b",
    re.IGNORECASE | re.MULTILINE,
)


def _trailer(message, name):
    match = re.search(rf"^{name}:\s*(.+?)\s*$", message, re.IGNORECASE | re.MULTILINE)
    return match.group(1) if match else None


def tier_of(message):
    value = _trailer(message, "Agent-Tier")
    return value.lower() if value else None


def model_of(message):
    return _trailer(message, "Agent-Model")


def is_agent_commit(message):
    tier = tier_of(message)
    if tier is not None:
        return tier in TIERS
    return bool(AGENT_CO_AUTHOR.search(message))


def reviewer_of(message):
    return _trailer(message, "Reviewed-by")


def load_gated(root="."):
    try:
        with open(os.path.join(root, "docs", "INDEX.json"), encoding="utf-8") as fh:
            return list(json.load(fh)["review_gated"]["paths"])
    except (OSError, KeyError, ValueError):
        return []


def load_advisory_rules(root="."):
    try:
        with open(os.path.join(root, "docs", "INDEX.json"), encoding="utf-8") as fh:
            config = json.load(fh)["pr_advisory"]
            return {"high_judgement": list(config["high_judgement"])}
    except (OSError, KeyError, ValueError, TypeError):
        return {"high_judgement": ()}


def _matches(path, prefixes):
    return any(path == p or path.startswith(p) for p in prefixes)


def _review_after(commits, index):
    for later in commits[index + 1:]:
        reviewer = reviewer_of(later["message"])
        if reviewer:
            name = reviewer.split("<")[0].strip() or reviewer
            return name, later["sha"][:7]
    return None


def _flag(findings, commits, index, text):
    text = text.rstrip(".")
    review = _review_after(commits, index)
    if review:
        name, sha = review
        findings.append(("notice", f"{text}; human-reviewed by {name} in {sha}."))
    else:
        findings.append(("warning", f"{text}; not yet human-reviewed: review carefully, or "
                                    "record a review with `python3 scripts/sdlc.py review`."))


def advise(commits, changed, branch, gated=(), high_judgement=None, root="."):
    """commits are oldest first."""
    rules = load_advisory_rules(root)
    high_judgement = rules["high_judgement"] if high_judgement is None else high_judgement
    findings = []

    for i, c in enumerate(commits):
        short = c["sha"][:7]
        tier = tier_of(c["message"])
        agent = is_agent_commit(c["message"])
        risky = [f for f in c["files"] if _matches(f, high_judgement)] if tier == "small" else []
        gated_files = [f for f in c["files"] if _matches(f, gated)] if agent else []
        if risky:
            _flag(findings, commits, i,
                  f"Commit {short} (Agent-Tier: small) changed high-judgement files: "
                  f"{', '.join(risky)}; review thoroughly, ideally with a second review "
                  "by a larger model (CONTRIBUTING.md).")
        elif gated_files:
            _flag(findings, commits, i,
                  f"Commit {short} (agent) changed review-gated files: {', '.join(gated_files)}.")
        if tier is None and agent:
            findings.append((
                "notice",
                f"Commit {short} looks agent-written but has no Agent-Tier trailer; "
                "model tier unknown.",
            ))

    return findings


def _git(args, cwd):
    return subprocess.run(["git", *args], cwd=cwd, check=True,
                          capture_output=True, text=True).stdout


def collect(base, head, cwd=None):
    log = _git(["log", "--reverse", "--no-merges", "--format=%x1e%H%x1f%B%x1f", "--name-only",
                f"{base}..{head}"], cwd)
    commits = []
    for record in log.split("\x1e")[1:]:
        sha, message, files = record.split("\x1f")
        commits.append({
            "sha": sha,
            "message": message,
            "files": [f for f in files.splitlines() if f.strip()],
        })
    diff = _git(["diff", "--name-status", "--no-renames", f"{base}...{head}"], cwd)
    changed = [tuple(line.split("\t", 1)) for line in diff.splitlines() if line.strip()]
    return commits, changed


def report(findings):
    on_actions = bool(os.environ.get("GITHUB_ACTIONS"))
    if not findings:
        print("✓ No advisory findings.")
    for level, text in findings:
        print(f"{'⚠' if level == 'warning' else 'ℹ'} {text}")
        if on_actions:
            print(f"::{level}::{text}")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a") as fh:
            fh.write("## PR advisory\n\n")
            if not findings:
                fh.write("No advisory findings.\n")
            for level, text in findings:
                fh.write(f"- **{level}:** {text}\n")


def main(argv):
    if len(argv) != 4:
        print(__doc__.strip())
        return 0
    _, base, head, branch = argv
    commits, changed = collect(base, head)
    report(advise(commits, changed, branch, gated=load_gated(), root="."))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
