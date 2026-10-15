#!/usr/bin/env bash
set -euo pipefail
repo_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
cd -- "$repo_root"
env_file=${VIETTREE_ENV_FILE:-.env.production}
if [[ ! -r "$env_file" ]]; then
  printf 'Production env file not found. Create .env.production first.\n' >&2
  exit 64
fi
profile=${VIETTREE_DEPLOY_PROFILE:-}
if [[ -z "$profile" ]]; then
  # Read one selector, never source/execute the secrets file as shell code.
  profile=$(sed -nE 's/^[[:space:]]*VIETTREE_DEPLOY_PROFILE[[:space:]]*=[[:space:]]*([^#]*).*$/\1/p' "$env_file" | tail -n 1 | tr -d '[:space:]')
fi
args=(--project-name viettree --env-file "$env_file" -f docker-compose.production.yml)
case "$profile" in
  ''|standard|'"standard"'|"'standard'") ;;
  small|'"small"'|"'small'") args+=(-f docker-compose.small-vps.yml) ;;
  vps8gb|'"vps8gb"'|"'vps8gb'") args+=(-f docker-compose.vps8gb.yml) ;;
  *) printf 'VIETTREE_DEPLOY_PROFILE must be standard, small or vps8gb.\n' >&2; exit 64 ;;
esac
exec docker compose "${args[@]}" "$@"
