"""Validate merged deployment contracts without starting containers or using real secrets."""

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def bash_binary():
    git_bash = Path("C:/Program Files/Git/bin/bash.exe")
    return str(git_bash) if git_bash.exists() else shutil.which("bash")


def run_wrapper(tmp_path, profile, *arguments):
    bash = bash_binary()
    if not bash:
        pytest.skip("Bash is required for deployment wrapper checks")
    env = {
        **os.environ,
        "DOCKER_CONFIG": str(tmp_path),
        "VIETTREE_ENV_FILE": ".env.production.small.example",
        "VIETTREE_DEPLOY_PROFILE": profile,
    }
    return subprocess.run(
        [bash, str(ROOT / "deploy/compose.sh"), *arguments],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )


def test_unknown_profile_fails_before_using_docker(tmp_path):
    response = run_wrapper(tmp_path, "mistyped-profile", "config", "--quiet")
    assert response.returncode == 64
    assert "must be standard, small or vps8gb" in response.stderr


def test_small_profile_keeps_storage_private_ports_and_bounded_resources(tmp_path):
    if not shutil.which("docker"):
        pytest.skip("Docker Compose CLI required; Engine not required")
    small_response = run_wrapper(tmp_path, "small", "config", "--format", "json")
    standard_response = run_wrapper(tmp_path, "standard", "config", "--format", "json")
    assert small_response.returncode == standard_response.returncode == 0
    small, standard = json.loads(small_response.stdout), json.loads(standard_response.stdout)
    assert small["name"] == standard["name"] == "viettree"
    assert small["volumes"] == standard["volumes"]
    services = small["services"]
    caps = sum(int(services[name]["mem_limit"]) for name in ("db", "backend", "frontend", "caddy"))
    assert caps <= 1536 * 1024 * 1024  # leave at least 512 MiB outside the application containers
    for name in ("backend", "frontend"):
        assert "build" not in services[name]
        assert services[name]["platform"] == "linux/amd64"
    for name in ("db", "backend", "frontend"):
        assert not services[name].get("ports")
        assert services[name].get("volumes", []) == standard["services"][name].get("volumes", [])
    backend_env = services["backend"]["environment"]
    assert backend_env["SERVER_WORKERS"] == backend_env["PASSWORD_VERIFY_CONCURRENCY"] == "1"
    assert int(backend_env["DB_POOL_SIZE"]) + int(backend_env["DB_POOL_MAX_OVERFLOW"]) <= 6
    assert backend_env["AI_TRAINING_ONLY"] == "true"
    pg_options = services["db"]["command"]
    assert "fsync=off" not in pg_options and "synchronous_commit=off" not in pg_options
    assert "max_connections=30" in pg_options
    assert services["caddy"]["networks"] == standard["services"]["caddy"]["networks"]


def test_vps8gb_profile_budget_database_and_private_network(tmp_path):
    if not shutil.which("docker"):
        pytest.skip("Docker Compose CLI required; Engine not required")
    result = run_wrapper(tmp_path, "vps8gb", "config", "--format", "json")
    assert result.returncode == 0, result.stderr
    merged = json.loads(result.stdout)
    assert merged["name"] == "viettree"
    services = merged["services"]
    caps = sum(int(services[name]["mem_limit"]) for name in ("db", "backend", "frontend", "caddy"))
    assert caps == 4864 * 1024 * 1024
    for name in ("db", "backend", "frontend"):
        assert not services[name].get("ports")
        assert services[name]["pids_limit"] <= 256
    environment = services["backend"]["environment"]
    assert environment["SERVER_WORKERS"] == "2"
    assert int(environment["DB_POOL_SIZE"]) + int(environment["DB_POOL_MAX_OVERFLOW"]) == 6
    assert environment["AI_TRAINING_ONLY"] == "true"
    assert services["db"]["environment"]["TZ"] == "UTC"
    pg_options = services["db"]["command"]
    assert "shared_buffers=512MB" in pg_options and "max_connections=60" in pg_options
    assert not any(value in pg_options for value in ("fsync=off", "synchronous_commit=off"))
    assert services["caddy"]["networks"]["app"]["ipv4_address"] == "172.30.40.2"
    assert services["caddy"]["environment"]["MAINTENANCE_MODE"] == "true"
    assert any(
        item.get("protocol") == "udp" and item["target"] == 443
        for item in services["caddy"]["ports"]
    )
