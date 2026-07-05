#!/usr/bin/env bash
set -euo pipefail

# Managed by ios-macos-repo-workflow v0.1

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=common.sh
source "$SCRIPT_DIR/common.sh"

echo "Implement repo-specific test command here."
echo "Use this script as the canonical routine test entrypoint."
exit 0
