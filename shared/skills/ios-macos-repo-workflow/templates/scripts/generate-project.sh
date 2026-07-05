#!/usr/bin/env bash
set -euo pipefail

# Managed by ios-macos-repo-workflow v0.1

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=common.sh
source "$SCRIPT_DIR/common.sh"

ROOT="$(repo_root)"

has_tuist_manifest() {
  [ -f "$ROOT/Tuist.swift" ] && return 0
  [ -f "$ROOT/Project.swift" ] && return 0
  find "$ROOT" -path "$ROOT/.git" -prune -o -name Project.swift -print -quit | grep -q .
}

has_xcodegen_manifest() {
  [ -f "$ROOT/project.yml" ] || [ -f "$ROOT/project.yaml" ]
}

missing_tuist() {
  cat >&2 <<'EOF'
Missing required command: tuist

This repo appears to use Tuist manifests. Install Tuist before generating:
  brew install tuist

Tuist is preferred for new generated-project Apple app repos, but this script
does not install tools or migrate projects automatically.
EOF
  exit 1
}

missing_xcodegen() {
  cat >&2 <<'EOF'
Missing required command: xcodegen

This repo appears to use XcodeGen. Install XcodeGen before generating:
  brew install xcodegen

Existing XcodeGen repos should stay on XcodeGen unless a migration proposal is
explicitly approved.
EOF
  exit 1
}

cd "$ROOT"

if has_tuist_manifest; then
  command -v tuist >/dev/null 2>&1 || missing_tuist
  run_logged "tuist generate" tuist generate
  exit 0
fi

if has_xcodegen_manifest; then
  command -v xcodegen >/dev/null 2>&1 || missing_xcodegen
  run_logged "xcodegen generate" xcodegen generate
  exit 0
fi

cat <<'EOF'
No generated-project config found.

This helper is only active for Tuist or XcodeGen-backed repos.
For new clean generated-project Apple app repos, prefer Tuist.
For existing XcodeGen repos, preserve XcodeGen unless migration is approved.
EOF
