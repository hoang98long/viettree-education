#!/usr/bin/env bash
set -euo pipefail
umask 077
repo_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
cd -- "$repo_root"
backup_root=${VIETTREE_BACKUP_DIR:-/var/backups/viettree}
install -d -m 700 -- "$backup_root"
temporary_dump=$(mktemp "$backup_root/.dump.XXXXXX")
temporary_media=$(mktemp "$backup_root/.media.XXXXXX")
trap 'rm -f -- "$temporary_dump" "$temporary_media"' EXIT
dc() {
  bash "$repo_root/deploy/compose.sh" "$@"
}
dc exec -T db sh -c 'exec pg_dump -U viettree_app -d "$POSTGRES_DB" -Fc' > "$temporary_dump"
dc exec -T db pg_restore --list < "$temporary_dump" > /dev/null
dc exec -T backend python -c 'import os, sys, tarfile; root=os.environ.get("AI_MEDIA_ROOT", "/workspace/var/ai-media"); archive=tarfile.open(fileobj=sys.stdout.buffer, mode="w|gz"); archive.add(root, arcname="ai-media"); archive.close()' > "$temporary_media"
dc exec -T backend python -c 'import sys, tarfile; archive=tarfile.open(fileobj=sys.stdin.buffer, mode="r|gz"); sum(1 for _ in archive)' < "$temporary_media"
backup_prefix="$backup_root/viettree-$(date -u +%Y%m%dT%H%M%SZ)-$$"
destination="$backup_prefix.dump"
mv -- "$temporary_dump" "$destination"
mv -- "$temporary_media" "$backup_prefix.media.tar.gz"
printf 'Backup ready: %s\n' "$destination"
printf 'Private media backup: %s\n' "$backup_prefix.media.tar.gz"
