#!/usr/bin/env bash
set -euo pipefail
umask 077
repo_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
cd -- "$repo_root"
backup_root=${VIETTREE_BACKUP_DIR:-/var/backups/viettree}
if [[ ! -d "$backup_root" ]]; then mkdir -p -- "$backup_root"; fi
chmod 700 -- "$backup_root"
command -v flock >/dev/null || { printf 'Install util-linux (flock) before backup.\n' >&2; exit 69; }
exec 9>"$backup_root/.backup.lock"
flock -n 9 || { printf 'Another backup is running; no files changed.\n' >&2; exit 75; }
temporary_dump=$(mktemp "$backup_root/.dump.XXXXXX")
temporary_media=$(mktemp "$backup_root/.media.XXXXXX")
temporary_checksums=$(mktemp "$backup_root/.checksums.XXXXXX")
temporary_status=$(mktemp "$backup_root/.status.XXXXXX")
trap 'rm -f -- "$temporary_dump" "$temporary_media" "$temporary_checksums" "$temporary_status"' EXIT
dc() {
  bash "$repo_root/deploy/compose.sh" "$@"
}
dc exec -T db sh -c 'exec pg_dump -U viettree_app -d "$POSTGRES_DB" -Fc' > "$temporary_dump"
dc exec -T db pg_restore --list < "$temporary_dump" > /dev/null
# One-off helpers also work while the API is stopped for maintenance.
dc run --rm -T --no-deps --entrypoint python backend scripts/media_archive.py create > "$temporary_media"
dc run --rm -T --no-deps --entrypoint python backend scripts/media_archive.py verify < "$temporary_media"
backup_prefix="$backup_root/viettree-$(date -u +%Y%m%dT%H%M%SZ)-$$"
destination="$backup_prefix.dump"
mv -- "$temporary_dump" "$destination"
mv -- "$temporary_media" "$backup_prefix.media.tar.gz"
# Publish the manifest last: it marks a complete pair. A failed run never
# advances latest.success; orphaned files are not reported as valid backups.
(cd -- "$backup_root" && sha256sum -- "$(basename -- "$destination")" "$(basename -- "$backup_prefix.media.tar.gz")") > "$temporary_checksums"
mv -- "$temporary_checksums" "$backup_prefix.sha256"
printf '%s\n' "$(basename -- "$backup_prefix.sha256")" > "$temporary_status"
mv -- "$temporary_status" "$backup_root/latest.success"
printf 'Backup ready: %s\n' "$destination"
printf 'Private media backup: %s\n' "$backup_prefix.media.tar.gz"
printf 'Checksums: %s\n' "$backup_prefix.sha256"
