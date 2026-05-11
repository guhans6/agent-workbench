#!/usr/bin/env bash
set -euo pipefail

# Managed by ios-macos-repo-workflow v0.1

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=common.sh
source "$SCRIPT_DIR/common.sh"

ROOT="$(repo_root)"

echo "Repo root: $ROOT"
echo "This repo uses ios-macos-repo-workflow."
echo "Expected canonical workflow files:"
echo "- __BUILD_PATH__"
echo "- __TEST_PATH__"
echo "- __VERIFY_FAST_PATH__"
echo "- __VERIFY_DEEP_PATH__"
echo "- __BOOTSTRAP_DEV_PATH__"
echo
echo "Use the global skill in bootstrap, refresh, or audit mode to manage workflow files."
