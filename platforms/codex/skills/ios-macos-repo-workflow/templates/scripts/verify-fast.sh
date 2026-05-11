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
  bash "$SCRIPT_DIR/build.sh"
  bash "$SCRIPT_DIR/test.sh"
  exit 0
fi

echo "Implement repo-specific fast verification here."
echo "Expected shape: cheap build plus routine validation."
exit 0
