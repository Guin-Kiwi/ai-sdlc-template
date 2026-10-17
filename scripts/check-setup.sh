#!/usr/bin/env bash
# Checks this machine's agent and environment setup. Safe to run any time.

set -uo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

failures=0
ok()   { echo "✓ $1"; }
fail() { echo "✗ $1"; echo "    Fix: $2"; failures=$((failures + 1)); }

bootstrap_skill=$(python3 - <<'PY'
import json
with open("docs/INDEX.json", encoding="utf-8") as fh:
    index = json.load(fh)
print(next(phase["skill"] for phase in index["phases"] if phase["phase"] == 0))
PY
)

linked=0
for dir in .agents .claude .cursor; do
  if [ -f "$dir/skills/${bootstrap_skill}SKILL.md" ]; then
    ok "$dir/skills resolves to the AI-SDLC skills"
    linked=1
  elif [ -e "$dir/skills" ] || [ -L "$dir/skills" ]; then
    fail "$dir/skills exists but does not contain the AI-SDLC skills" "remove it and run: bash scripts/setup-skills.sh"
  fi
done
[ "$linked" -eq 1 ] || fail "no agent can discover the skills" "bash scripts/setup-skills.sh all"

if [ -f CLAUDE.md ] && grep -q '@AGENTS.md' CLAUDE.md; then
  ok "CLAUDE.md imports AGENTS.md"
else
  fail "CLAUDE.md missing or does not import AGENTS.md" "bash scripts/setup-skills.sh claude"
fi

if [ -d environments/python ]; then
  if [ -x .venv/bin/python ] && .venv/bin/python -c "import sys" 2>/dev/null; then
    ok "Python environment in .venv"
  else
    fail "Python environment missing" "bash scripts/setup-python.sh"
  fi
fi

mapfile -t required_docs < <(python3 - <<'PY'
import json
with open("docs/INDEX.json", encoding="utf-8") as fh:
  index = json.load(fh)
print("\n".join(("docs/INDEX.json", index["lifecycle_state"], index["project_context"])))
PY
)
for f in "${required_docs[@]}"; do
  [ -f "$f" ] && ok "$f present" || fail "$f missing" "restore it from the template"
done

echo ""
if [ "$failures" -eq 0 ]; then
  echo "Setup OK. Next: ask your agent to start BOOTSTRAP (see docs/TASKS.md)."
else
  echo "$failures setup problem(s) found."
  exit 1
fi
