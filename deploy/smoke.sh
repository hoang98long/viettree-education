#!/usr/bin/env bash
# Read-only checks after deployment. Never logs credentials or creates users.
set -euo pipefail
repo_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
cd -- "$repo_root"
dc() { bash "$repo_root/deploy/compose.sh" "$@"; }
require_backup=false
case "${1:-}" in
  '') ;;
  --require-backup) require_backup=true ;;
  *) printf 'Usage: bash deploy/smoke.sh [--require-backup]\n' >&2; exit 64 ;;
esac
dc config --quiet
for service in db backend frontend caddy; do
  identifier=$(dc ps -q "$service")
  [[ -n "$identifier" ]] || { printf 'Missing container: %s\n' "$service" >&2; exit 1; }
  state=$(docker inspect --format '{{.State.Status}}|{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}|{{.State.OOMKilled}}|{{.RestartCount}}' "$identifier")
  case "$state" in
    running\|healthy\|false\|*|running\|none\|false\|*) ;;
    *) printf 'Container check failed: %s %s\n' "$service" "$state" >&2; exit 1 ;;
  esac
  printf 'Container %s: %s\n' "$service" "$state"
done
dc exec -T backend python -m app.cli check-launch
origin=$(dc exec -T backend python -c 'from app.core.config import settings; print(settings().origins[0])' | tr -d '\r')
[[ "$origin" == https://* && "$origin" != *example.com* ]] || { printf 'Configure the real HTTPS domain.\n' >&2; exit 1; }
headers=$(mktemp)
body=$(mktemp)
trap 'rm -f -- "$headers" "$body"' EXIT
check_http() {
  local resource=$1 expected=$2 code
  code=$(curl --proto '=https' --tlsv1.2 --connect-timeout 10 --max-time 45 --silent --show-error -D "$headers" -o "$body" --write-out '%{http_code}' "$origin$resource")
  [[ "$code" == "$expected" ]] || { printf 'HTTP check failed: %s status=%s expected=%s\n' "$resource" "$code" "$expected" >&2; exit 1; }
  printf 'HTTPS %s: %s\n' "$resource" "$code"
}
check_http /login 200
grep -qi '^strict-transport-security:' "$headers"
grep -qi '^x-content-type-options: nosniff' "$headers"
check_http /health 200
check_http /api/v1/auth/me 401
grep -qi '^cache-control:.*no-store' "$headers"
check_http /learning/cat.svg 200
grep -qi '^cache-control:.*public.*max-age=3600' "$headers"
for resource in /ready /docs /openapi.json; do check_http "$resource" 404; done
redirect=$(curl --proto '=http' --connect-timeout 10 --max-time 15 --silent --show-error -D "$headers" -o /dev/null --write-out '%{http_code}' "http://${origin#https://}/login")
[[ "$redirect" == 301 || "$redirect" == 308 ]]
grep -qi "^location: $origin/login" "$headers"
if "$require_backup"; then
  backup_root=${VIETTREE_BACKUP_DIR:-/var/backups/viettree}
  latest="$backup_root/latest.success"
  [[ -f "$latest" ]] || { printf 'No successful backup marker.\n' >&2; exit 1; }
  manifest=$(cat -- "$latest")
  [[ "$manifest" =~ ^viettree-[0-9TZ-]+\.sha256$ ]] || { printf 'Invalid backup marker.\n' >&2; exit 1; }
  age=$(( $(date +%s) - $(stat -c %Y -- "$latest") ))
  (( age >= 0 && age <= 93600 )) || { printf 'Last successful backup is older than 26 hours or clock is incorrect.\n' >&2; exit 1; }
  (cd -- "$backup_root" && sha256sum --check -- "$manifest")
  printf 'Last backup checksum and age: OK\n'
fi
printf 'Deployment checks passed.\n'
