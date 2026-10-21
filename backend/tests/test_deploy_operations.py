"""Run real Bash scripts; substitute external Docker/network commands only."""

import hashlib
import os
import shutil
import subprocess
import time
from pathlib import Path

import pytest

from tests.test_deployment_profile import ROOT, bash_binary


def sandbox(tmp_path):
    bash = bash_binary()
    if not bash:
        pytest.skip("Bash required")
    project = tmp_path / "deployment with spaces"
    (project / "deploy").mkdir(parents=True)
    for filename in ("backup.sh", "compose.sh", "smoke.sh"):
        shutil.copyfile(ROOT / "deploy" / filename, project / "deploy" / filename)
    (project / ".env.production").write_text("VIETTREE_DEPLOY_PROFILE=vps8gb\n", encoding="utf8")
    return bash, project


def run_script(bash, project, setup, name, environment, arguments=()):
    fake_bin = setup.parent / "bin"
    fake_bin.mkdir()
    commands = setup.read_text(encoding="utf8")
    for executable in ("docker", "curl", "flock"):
        binary = fake_bin / executable
        binary.write_text(
            "#!/usr/bin/env bash\n" + commands + f'\n{executable} "$@"\n',
            encoding="utf8",
            newline="\n",
        )
        binary.chmod(0o755)
    return subprocess.run(
        [
            bash,
            "-c",
            'export PATH="$(cd -- "$1" && pwd):$PATH"; if [[ -n "${VIETTREE_BACKUP_DIR:-}" ]]; then export VIETTREE_BACKUP_DIR="$(cd -- "$VIETTREE_BACKUP_DIR" && pwd)"; fi; exec bash "$2" "${@:3}"',
            "check",
            str(fake_bin),
            str(project / "deploy" / name),
            *arguments,
        ],
        env={**os.environ, "BASH_ENV": "", "DOCKER_CONFIG": str(setup.parent), **environment},
        capture_output=True,
        timeout=30,
    )


@pytest.mark.parametrize("failure", ["none", "dump", "restore", "media", "lock"])
def test_backup_publishes_complete_pair_or_preserves_last_success(tmp_path, failure):
    bash, project = sandbox(tmp_path)
    backup = tmp_path / "private backups"
    backup.mkdir()
    (backup / "latest.success").write_text("previous.sha256\n")
    archive = tmp_path / "media"
    archive.mkdir()
    (archive / "photo.webp").write_bytes(b"a" * 2500000)
    setup = tmp_path / "commands.sh"
    python = Path(os.sys.executable).as_posix()
    helper = (ROOT / "backend/scripts/media_archive.py").as_posix()
    setup.write_text(
        f"""flock() {{ [[ "$FAILURE" != lock ]]; }}
docker() {{
 case "$*" in
   *pg_dump*) [[ "$FAILURE" != dump ]] || return 1; printf 'custom database dump';;
   *pg_restore*) cat > /dev/null; [[ "$FAILURE" != restore ]];;
   *'media_archive.py create'*)
     if [[ "$FAILURE" == media ]]; then printf 'broken gzip'; else "{python}" "{helper}" create; fi;;
   *'media_archive.py verify'*) "{python}" "{helper}" verify;;
   *) printf 'Unexpected Docker command' >&2; return 2;;
 esac
}}
""",
        encoding="utf8",
        newline="\n",
    )
    result = run_script(
        bash,
        project,
        setup,
        "backup.sh",
        {
            "VIETTREE_BACKUP_DIR": backup.as_posix(),
            "AI_MEDIA_ROOT": archive.as_posix(),
            "FAILURE": failure,
        },
    )
    marker = (backup / "latest.success").read_text().strip()
    if failure == "none":
        assert result.returncode == 0, result.stderr.decode(errors="replace")
        assert marker != "previous.sha256"
        lines = (backup / marker).read_text().splitlines()
        assert len(lines) == 2
        for line in lines:
            digest, filename = line.split(maxsplit=1)
            filename = filename.lstrip("*")  # GNU binary marker on Windows.
            assert hashlib.sha256((backup / filename).read_bytes()).hexdigest() == digest
    else:
        assert result.returncode != 0
        assert marker == "previous.sha256"
        assert not list(backup.glob("viettree-*.sha256"))
        assert not list(backup.glob("viettree-*.dump"))
    assert not list(backup.glob(".dump.*"))
    assert not list(backup.glob(".media.*"))


@pytest.mark.parametrize(
    "failure,backup_case",
    [
        (failure, None)
        for failure in ("none", "unhealthy", "private_cache", "docs_public", "release_not_ready")
    ]
    + [("none", case) for case in ("valid", "missing", "stale", "corrupt", "invalid_marker")],
)
def test_smoke_checks_health_api_privacy_and_hidden_routes(tmp_path, failure, backup_case):
    bash, project = sandbox(tmp_path)
    setup = tmp_path / "commands.sh"
    setup.write_text(
        """docker() {
 case "$*" in
  *'config --quiet'*) return 0;;
  *'ps -q '*) printf 'container-id';;
  inspect*) if [[ "$FAILURE" == unhealthy ]]; then printf 'running|unhealthy|false|0'; else printf 'running|healthy|false|0'; fi;;
  *'app.cli check-release'*) [[ "$FAILURE" != release_not_ready ]] || return 1; printf '{"status":"ok"}\n';;
  *'settings().origins'*) printf 'https://learn.invalid\n';;
  *) return 2;;
 esac
}
curl() {
 local headers='' body='' url='' status=200 previous=''
 for value in "$@"; do
   [[ "$previous" != -D ]] || headers=$value
   [[ "$previous" != -o ]] || body=$value
   previous=$value
   url=$value
 done
 case "$url" in
  http://*) status=308;;
  */api/v1/auth/me) status=401;;
  */ready|*/docs|*/openapi.json) status=404;;
 esac
 [[ "$FAILURE" != docs_public || "$url" != */docs ]] || status=200
 printf 'strict-transport-security: max-age=31536000\r\nx-content-type-options: nosniff\r\nlocation: https://learn.invalid/login\r\n' > "$headers"
 case "$url" in
  */api/v1/auth/me) if [[ "$FAILURE" == private_cache ]]; then printf 'cache-control: public\r\n'; else printf 'cache-control: no-store\r\n'; fi >> "$headers";;
  */learning/cat.svg) printf 'cache-control: public, max-age=3600\r\n' >> "$headers";;
 esac
 printf '{}' > "$body"
 printf '%s' "$status"
}
""",
        encoding="utf8",
        newline="\n",
    )
    environment = {"FAILURE": failure}
    if backup_case is not None:
        backups = tmp_path / "backups"
        backups.mkdir()
        environment["VIETTREE_BACKUP_DIR"] = backups.as_posix()
        manifest = "viettree-20261015T000000Z-123.sha256"
        (backups / "payload.dump").write_bytes(b"database")
        digest = hashlib.sha256(b"database").hexdigest()
        (backups / manifest).write_text(f"{digest}  payload.dump\n", newline="\n")
        marker = backups / "latest.success"
        if backup_case != "missing":
            marker.write_text(manifest + "\n", newline="\n")
        if backup_case == "stale":
            os.utime(marker, (time.time() - 95000, time.time() - 95000))
        elif backup_case == "corrupt":
            (backups / "payload.dump").write_bytes(b"corrupted")
        elif backup_case == "invalid_marker":
            marker.write_text("../../unexpected.sha256")
    result = run_script(
        bash, project, setup, "smoke.sh", environment, ("--require-backup",) if backup_case else ()
    )
    expected = failure == "none" and backup_case in (None, "valid")
    assert (result.returncode == 0) == expected, result.stderr.decode(errors="replace")
    assert (b"Deployment checks passed" in result.stdout) == expected
