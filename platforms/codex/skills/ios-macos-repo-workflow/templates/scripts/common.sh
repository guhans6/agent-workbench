#!/usr/bin/env bash
set -euo pipefail

# Managed by ios-macos-repo-workflow v0.1

repo_root() {
  if git_root="$(git rev-parse --show-toplevel 2>/dev/null)"; then
    printf '%s\n' "$git_root"
    return 0
  fi

  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  cd "$script_dir/.." && pwd
}

ensure_log_dir() {
  local root
  root="$(repo_root)"
  mkdir -p "$root/.logs"
}

timestamp() {
  date +"%Y%m%d-%H%M%S"
}

require_command() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Missing required command: $cmd" >&2
    exit 1
  fi
}

log_path() {
  local name="$1"
  local root
  root="$(repo_root)"
  ensure_log_dir
  printf '%s/.logs/%s-%s.log\n' "$root" "$name" "$(timestamp)"
}

sanitize_label() {
  local label="$1"
  label="${label//\//-}"
  label="${label// /-}"
  printf '%s\n' "$label"
}

run_logged() {
  local label="$1"
  shift

  local log_file
  log_file="$(log_path "$(sanitize_label "$label")")"

  echo "Running $label..."
  if "$@" >"$log_file" 2>&1; then
    echo "OK: $label"
    echo "Log: $log_file"
    return 0
  else
    local status=$?
  fi

  echo "FAILED: $label" >&2
  echo "Log: $log_file" >&2
  tail -n 40 "$log_file" >&2 || true
  return "$status"
}
