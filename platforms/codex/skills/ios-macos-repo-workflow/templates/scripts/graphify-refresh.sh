#!/usr/bin/env bash
set -euo pipefail

# Managed by ios-macos-repo-workflow v0.1

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=common.sh
source "$SCRIPT_DIR/common.sh"

ROOT="$(repo_root)"

if ! command -v graphify >/dev/null 2>&1; then
  cat >&2 <<'EOF'
Missing required command: graphify

Install or enable graphify before refreshing the context graph.
This script is optional and is not part of normal build/test verification.
EOF
  exit 1
fi

cd "$ROOT"
run_logged "graphify update" graphify update "$ROOT"

echo "Graphify context outputs:"
if [ -f "$ROOT/graphify-out/graph.json" ]; then
  echo "- graphify-out/graph.json"
fi
if [ -f "$ROOT/graphify-out/GRAPH_REPORT.md" ]; then
  echo "- graphify-out/GRAPH_REPORT.md"
fi
html_output="$(find "$ROOT/graphify-out" -maxdepth 1 -name '*.html' -print -quit 2>/dev/null || true)"
if [ -n "$html_output" ]; then
  echo "- ${html_output#"$ROOT/"}"
fi

echo
echo "Agent usage:"
echo "- graphify query \"<question>\" --graph graphify-out/graph.json"
echo "- graphify path \"<node A>\" \"<node B>\" --graph graphify-out/graph.json"
echo "- graphify explain \"<node>\" --graph graphify-out/graph.json"
