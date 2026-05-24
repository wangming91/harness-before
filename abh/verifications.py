from __future__ import annotations

import os
import sys
import hashlib
import shlex
import subprocess
import time
import uuid
from pathlib import Path

from . import __version__
from .errors import AbhError
from .models import VERIFICATION_RESULTS, VERIFICATION_TRUST_LEVELS, VerificationRun
from .plans import load_plan, plan_verification_snapshot, save_plan
from .storage import ensure_workspace, read_json, verification_path, write_json

GIT_STATUS_HASH_IGNORED_PREFIXES = (
    ".abh/plans/",
    ".abh/verifications/",
    "docs/plans/",
)


def load_verification(run_id: str, cwd: Path | None = None) -> VerificationRun:
    path = verification_path(run_id, cwd)
    if not path.exists():
        raise AbhError(f"verification run not found: {run_id}")
    return VerificationRun.from_dict(read_json(path))


def record_verification(
    *,
    plan_id: str,
    command: str,
    result: str,
    artifacts: list[str] | None = None,
    failed_checks: list[str] | None = None,
    failure_classifications: list[dict[str, object]] | None = None,
    environment: dict | None = None,
    trust_level: str = "manual_record",
    cwd: Path | None = None,
) -> VerificationRun:
    if result not in VERIFICATION_RESULTS:
        raise AbhError(f"invalid verification result: {result}")
    if trust_level not in VERIFICATION_TRUST_LEVELS:
        raise AbhError(f"invalid verification trust level: {trust_level}")
    if not command.strip():
        raise AbhError("verification command is required")
    plan = load_plan(plan_id, cwd)
    ensure_workspace(cwd)
    metadata = dict(environment or {})
    metadata.setdefault("plan", plan_verification_snapshot(plan))
    run = VerificationRun(
        id=f"ver-{uuid.uuid4().hex[:12]}",
        plan_id=plan_id,
        command=command,
        result=result,
        artifacts=list(artifacts or []),
        failed_checks=list(failed_checks or []),
        failure_classifications=[dict(item) for item in failure_classifications or []],
        environment=metadata,
        trust_level=trust_level,
    )
    write_json(verification_path(run.id, cwd), run.to_dict())
    plan.verification_runs.append(run.id)
    if result in {"fail", "partial"} and plan.status in {"ready", "running"}:
        plan.status = "blocked"
    save_plan(plan, cwd)
    return run


def is_recursive_verify_command(command: str, plan_id: str) -> bool:
    try:
        parts = shlex.split(command)
    except ValueError:
        return False
    if len(parts) < 5:
        return False
    for index in range(len(parts) - 4):
        if parts[index:index + 4] == ["python3", "-m", "abh", "verify"] and "run" in parts[index + 4:]:
            return plan_id in parts[index + 4:]
        if parts[index:index + 4] == ["python", "-m", "abh", "verify"] and "run" in parts[index + 4:]:
            return plan_id in parts[index + 4:]
    return False


def git_metadata(root: Path) -> dict[str, object]:
    metadata: dict[str, object] = {
        "commit": None,
        "dirty": None,
        "status_hash": None,
        "available": False,
    }
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            text=True,
            capture_output=True,
            timeout=5,
            check=False,
        )
        if commit.returncode != 0:
            return metadata
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=root,
            text=True,
            capture_output=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return metadata

    metadata["commit"] = commit.stdout.strip()
    normalized_status = normalized_git_status(status.stdout) if status.returncode == 0 else ""
    metadata["dirty"] = bool(normalized_status) if status.returncode == 0 else None
    metadata["status_hash"] = (
        hashlib.sha256(normalized_status.encode("utf-8")).hexdigest() if status.returncode == 0 else None
    )
    metadata["available"] = True
    return metadata


def normalized_git_status(status: str) -> str:
    lines = [line for line in status.splitlines() if not is_ignored_git_status_line(line)]
    return "\n".join(lines)


def is_ignored_git_status_line(line: str) -> bool:
    if len(line) < 4:
        return False
    path = line[3:]
    paths = path.split(" -> ")
    return all(any(item.startswith(prefix) for prefix in GIT_STATUS_HASH_IGNORED_PREFIXES) for item in paths)


def split_command(command: str) -> list[str]:
    try:
        return shlex.split(command)
    except ValueError:
        return []


def failure_classification(
    *,
    command: str,
    category: str,
    message: str,
    details: dict[str, object] | None = None,
) -> dict[str, object]:
    return {
        "command": command,
        "category": category,
        "message": message,
        "details": dict(details or {}),
    }


def environment_snapshot(*, root: Path, commands: list[str], timeout_seconds: int) -> dict[str, object]:
    env_allowlist = {name: os.environ[name] for name in ("CI", "VIRTUAL_ENV") if name in os.environ}
    return {
        "cwd": str(root.resolve()),
        "git": git_metadata(root),
        "abh": {"version": __version__},
        "python": {"version": sys.version, "executable": sys.executable},
        "runner": {
            "timeout_seconds": timeout_seconds,
            "shell": True,
            "check_count": len(commands),
        },
        "commands": [{"command": command, "argv": split_command(command)} for command in commands],
        "environment_variables": env_allowlist,
    }


def run_verification(
    *,
    plan_id: str,
    timeout_seconds: int = 120,
    cwd: Path | None = None,
) -> VerificationRun:
    plan = load_plan(plan_id, cwd)
    if not plan.validation_checklist:
        raise AbhError("plan has no validation checklist")
    if timeout_seconds <= 0:
        raise AbhError("timeout must be greater than zero")

    root = Path.cwd() if cwd is None else Path(cwd)
    artifacts: list[str] = []
    failed_checks: list[str] = []
    failure_classifications: list[dict[str, object]] = []
    commands = list(plan.validation_checklist)
    environment = environment_snapshot(root=root, commands=commands, timeout_seconds=timeout_seconds)

    for command in commands:
        if is_recursive_verify_command(command, plan_id):
            artifacts.append(f"command={command!r}; exit_code=recursive_verify_guard")
            failed_checks.append(command)
            failure_classifications.append(
                failure_classification(
                    command=command,
                    category="recursive_guard",
                    message="validation command would recursively invoke verify run for the same plan",
                )
            )
            continue
        started = time.perf_counter()
        try:
            completed = subprocess.run(
                command,
                cwd=root,
                shell=True,
                text=True,
                capture_output=True,
                timeout=timeout_seconds,
                check=False,
            )
            duration = time.perf_counter() - started
            stdout = completed.stdout.strip().replace("\n", "\\n")[:500]
            stderr = completed.stderr.strip().replace("\n", "\\n")[:500]
            artifacts.append(
                f"command={command!r}; exit_code={completed.returncode}; duration_seconds={duration:.3f}; "
                f"stdout={stdout!r}; stderr={stderr!r}"
            )
            if completed.returncode != 0:
                failed_checks.append(command)
                failure_classifications.append(
                    failure_classification(
                        command=command,
                        category="validation_failure",
                        message="validation command exited with non-zero status",
                        details={"exit_code": completed.returncode},
                    )
                )
        except subprocess.TimeoutExpired as exc:
            duration = time.perf_counter() - started
            stdout = (exc.stdout or "").strip().replace("\n", "\\n")[:500] if isinstance(exc.stdout, str) else ""
            stderr = (exc.stderr or "").strip().replace("\n", "\\n")[:500] if isinstance(exc.stderr, str) else ""
            artifacts.append(
                f"command={command!r}; exit_code=timeout; duration_seconds={duration:.3f}; "
                f"timeout_seconds={timeout_seconds}; stdout={stdout!r}; stderr={stderr!r}"
            )
            failed_checks.append(command)
            failure_classifications.append(
                failure_classification(
                    command=command,
                    category="timeout",
                    message="validation command exceeded timeout",
                    details={"timeout_seconds": timeout_seconds},
                )
            )
        except OSError as exc:
            duration = time.perf_counter() - started
            artifacts.append(
                f"command={command!r}; exit_code=environment_error; duration_seconds={duration:.3f}; "
                f"exception_type={type(exc).__name__!r}; error={str(exc)!r}"
            )
            failed_checks.append(command)
            failure_classifications.append(
                failure_classification(
                    command=command,
                    category="environment_failure",
                    message="validation command could not be executed by the local runner",
                    details={"exception_type": type(exc).__name__},
                )
            )

    result = "pass" if not failed_checks else "fail"
    return record_verification(
        plan_id=plan_id,
        command=" && ".join(commands),
        result=result,
        artifacts=artifacts,
        failed_checks=failed_checks,
        failure_classifications=failure_classifications,
        environment=environment,
        trust_level="local_shell",
        cwd=cwd,
    )
