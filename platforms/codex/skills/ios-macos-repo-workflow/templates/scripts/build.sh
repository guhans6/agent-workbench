#!/usr/bin/env bash
set -euo pipefail

# Managed by ios-macos-repo-workflow v0.1

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=common.sh
source "$SCRIPT_DIR/common.sh"

ROOT="$(repo_root)"

is_swiftpm_only_repo() {
  [ -f "$ROOT/Package.swift" ] || return 1
  find "$ROOT" -maxdepth 1 \( -name '*.xcodeproj' -o -name '*.xcworkspace' \) -print -quit | grep -q . && return 1
  [ -f "$ROOT/Tuist.swift" ] && return 1
  [ -f "$ROOT/Project.swift" ] && return 1
  [ -f "$ROOT/project.yml" ] && return 1
  [ -f "$ROOT/project.yaml" ] && return 1
  return 0
}

if is_swiftpm_only_repo; then
  cd "$ROOT"
  run_logged "swift build" swift build || exit $?
  exit 0
fi

echo "Implement repo-specific build command here."
echo "Use this script as the canonical build entrypoint."
exit 0
