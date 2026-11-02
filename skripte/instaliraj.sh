#!/usr/bin/env bash
# Instalacija PGH skillova i agenata na korisničkoj razini (macOS / Linux / WSL)
# Pokretanje iz korijena repozitorija:  bash skripte/instaliraj.sh [--opcionalno]
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$HOME/.claude/agents" "$HOME/.claude/skills"
cp "$REPO"/.claude/agents/*.md "$HOME/.claude/agents/"
SRC=("$REPO/.claude/skills")
[[ "${1:-}" == "--opcionalno" ]] && SRC+=("$REPO/skills-opcionalno")
for s in "${SRC[@]}"; do
  for d in "$s"/*/; do
    n=$(basename "$d"); rm -rf "$HOME/.claude/skills/$n"; cp -r "$d" "$HOME/.claude/skills/$n"; echo "skill -> $n"
  done
done
echo "Gotovo. Ponovno pokrenite Claude Code."
