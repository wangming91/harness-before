from __future__ import annotations

import hashlib
import json
from pathlib import Path
from datetime import datetime

from .errors import AbhError, require_existing_path, validate_identifier
from .models import PLAN_STATUSES, PlanRecord, utc_now
from .storage import (
    ensure_workspace,
    plan_doc_path,
    plan_json_path,
    plans_dir,
    read_json,
    write_json,
    write_text,
)

ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "draft": {"ready"},
    "ready": {"running", "blocked"},
    "running": {"blocked", "closing"},
    "blocked": {"running", "closing"},
    "closing": {"closed"},
    "closed": set(),
}

PLAN_VERIFICATION_FIELDS = (
    "title",
    "attractor",
    "baseline",
    "goals",
    "non_goals",
    "exit_criteria",
    "validation_checklist",
    "closure_evidence",
)


def list_plans(cwd: Path | None = None) -> list[PlanRecord]:
    directory = plans_dir(cwd)
    if not directory.exists():
        return []
    plans: list[PlanRecord] = []
    for path in sorted(directory.glob("*.json")):
        plans.append(PlanRecord.from_dict(read_json(path)))
    return plans


def load_plan(plan_id: str, cwd: Path | None = None) -> PlanRecord:
    validate_identifier(plan_id, "plan id")
    path = plan_json_path(plan_id, cwd)
    if not path.exists():
        raise AbhError(f"plan not found: {plan_id}")
    return PlanRecord.from_dict(read_json(path))


def save_plan(plan: PlanRecord, cwd: Path | None = None, write_doc: bool = True) -> PlanRecord:
    ensure_workspace(cwd)
    plan.updated_at = utc_now()
    if write_doc:
        doc_path = plan.doc_path or str(plan_doc_path(plan.id, cwd))
        plan.doc_path = doc_path
        doc = render_plan_markdown(plan)
        doc_file = Path(doc_path)
        write_text(doc_file, doc)
    write_json(plan_json_path(plan.id, cwd), plan.to_dict())
    return plan


def create_plan(
    *,
    plan_id: str,
    title: str,
    attractor: str,
    baseline: str,
    owner: str = "platform",
    status: str = "draft",
    goals: list[str] | None = None,
    non_goals: list[str] | None = None,
    exit_criteria: list[str] | None = None,
    validation_checklist: list[str] | None = None,
    closure_evidence: list[str] | None = None,
    cwd: Path | None = None,
) -> PlanRecord:
    ensure_workspace(cwd)
    validate_identifier(plan_id, "plan id")
    if status not in {"draft", "ready"}:
        raise AbhError("plan create only supports draft or ready status")
    plan_path = plan_json_path(plan_id, cwd)
    if plan_path.exists():
        raise AbhError(f"plan already exists: {plan_id}")
    if status == "ready":
        from .attractors import is_active_attractor_reference

        if not is_active_attractor_reference(attractor, cwd):
            raise AbhError("plan ready requires current active attractor id or path")
    else:
        require_existing_path(attractor, "attractor")
    plan = PlanRecord(
        id=plan_id,
        title=title,
        attractor=attractor,
        baseline=baseline,
        owner=owner,
        status=status,
        goals=list(goals or []),
        non_goals=list(non_goals or []),
        exit_criteria=list(exit_criteria or []),
        validation_checklist=list(validation_checklist or []),
        closure_evidence=list(closure_evidence or []),
        doc_path=str(plan_doc_path(plan_id, cwd)),
    )
    if status == "ready":
        validate_plan_ready(plan)
    return save_plan(plan, cwd=cwd, write_doc=True)


def append_unique(existing: list[str], additions: list[str] | None) -> list[str]:
    values = list(existing)
    for item in additions or []:
        if item not in values:
            values.append(item)
    return values


def update_plan_record(
    *,
    plan_id: str,
    goals: list[str] | None = None,
    non_goals: list[str] | None = None,
    exit_criteria: list[str] | None = None,
    validation_checklist: list[str] | None = None,
    remove_validation_checklist: list[str] | None = None,
    closure_evidence: list[str] | None = None,
    cwd: Path | None = None,
) -> PlanRecord:
    plan = load_plan(plan_id, cwd)
    if not any((goals, non_goals, exit_criteria, validation_checklist, remove_validation_checklist, closure_evidence)):
        raise AbhError("plan update requires at least one field to append")
    plan.goals = append_unique(plan.goals, goals)
    plan.non_goals = append_unique(plan.non_goals, non_goals)
    plan.exit_criteria = append_unique(plan.exit_criteria, exit_criteria)
    plan.validation_checklist = append_unique(plan.validation_checklist, validation_checklist)
    for item in remove_validation_checklist or []:
        plan.validation_checklist = [value for value in plan.validation_checklist if value != item]
    plan.closure_evidence = append_unique(plan.closure_evidence, closure_evidence)
    return save_plan(plan, cwd=cwd, write_doc=True)


def validate_plan_ready(plan: PlanRecord) -> None:
    missing: list[str] = []
    if not plan.title.strip():
        missing.append("title")
    if not plan.attractor.strip():
        missing.append("attractor")
    if not plan.baseline.strip():
        missing.append("baseline")
    if not plan.goals:
        missing.append("goals")
    if not plan.non_goals:
        missing.append("non_goals")
    if not plan.exit_criteria:
        missing.append("exit_criteria")
    if not plan.validation_checklist:
        missing.append("validation_checklist")
    if not plan.closure_evidence:
        missing.append("closure_evidence")
    if missing:
        raise AbhError(f"plan is not ready; missing: {', '.join(missing)}")
    from .attractors import is_active_attractor_reference

    if not is_active_attractor_reference(plan.attractor):
        raise AbhError("plan is not ready; attractor must reference current active attractor id or path")


def transition_plan(plan_id: str, target_status: str, cwd: Path | None = None) -> PlanRecord:
    if target_status not in PLAN_STATUSES:
        raise AbhError(f"invalid target status: {target_status}")
    plan = load_plan(plan_id, cwd)
    allowed = ALLOWED_TRANSITIONS[plan.status]
    if target_status not in allowed:
        raise AbhError(f"invalid transition: {plan.status} -> {target_status}")
    if target_status == "ready":
        validate_plan_ready(plan)
    if target_status == "closing":
        if not plan.verification_runs:
            raise AbhError("cannot move to closing without verification runs")
        from .verifications import load_verification

        latest = load_verification(plan.verification_runs[-1], cwd)
        if latest.result != "pass":
            raise AbhError("cannot move to closing without a passing verification run")
    plan.status = target_status
    return save_plan(plan, cwd)


def close_plan(plan_id: str, cwd: Path | None = None) -> PlanRecord:
    plan = load_plan(plan_id, cwd)
    passing_audit = None
    from .audits import load_audit

    for audit_id in plan.audit_ids:
        audit = load_audit(audit_id, cwd)
        if audit.result == "pass" and audit.status == "complete":
            passing_audit = audit
    if passing_audit is None:
        raise AbhError("cannot close plan without a passing audit")
    if not plan.closure_evidence:
        raise AbhError("cannot close plan without closure evidence")
    plan.status = "closed"
    if passing_audit.id not in plan.closure_evidence:
        plan.closure_evidence.append(passing_audit.id)
    return save_plan(plan, cwd)


def render_plan_markdown(plan: PlanRecord) -> str:
    def bullet_lines(values: list[str]) -> str:
        if not values:
            return "- "
        return "\n".join(f"- {value}" for value in values)

    return (
        f"# Plan: {plan.title}\n\n"
        "## Metadata\n\n"
        f"- ID: {plan.id}\n"
        f"- Status: {plan.status}\n"
        f"- Attractor: {plan.attractor}\n"
        f"- Baseline: {plan.baseline}\n"
        f"- Owner: {plan.owner}\n"
        f"- Created: {plan.created_at}\n"
        f"- Updated: {plan.updated_at}\n\n"
        "## Goals\n\n"
        f"{bullet_lines(plan.goals)}\n\n"
        "## Non-Goals\n\n"
        f"{bullet_lines(plan.non_goals)}\n\n"
        "## Exit Criteria\n\n"
        f"{bullet_lines(plan.exit_criteria)}\n\n"
        "## Validation Checklist\n\n"
        f"{bullet_lines(plan.validation_checklist)}\n\n"
        "## Closure Evidence\n\n"
        f"{bullet_lines(plan.closure_evidence)}\n\n"
        "## Verification Runs\n\n"
        f"{bullet_lines(plan.verification_runs)}\n\n"
        "## Audits\n\n"
        f"{bullet_lines(plan.audit_ids)}\n"
    )


def plan_status_line(plan: PlanRecord) -> str:
    latest = plan.verification_runs[-1] if plan.verification_runs else "none"
    return (
        f"{plan.id} [{plan.status}]\n"
        f"title: {plan.title}\n"
        f"attractor: {plan.attractor}\n"
        f"baseline: {plan.baseline}\n"
        f"verification_runs: {len(plan.verification_runs)}\n"
        f"latest_verification: {latest}\n"
        f"audits: {len(plan.audit_ids)}"
    )


def plan_verification_payload(plan: PlanRecord) -> dict[str, object]:
    data = plan.to_dict()
    return {field: data[field] for field in PLAN_VERIFICATION_FIELDS}


def plan_verification_hash(plan: PlanRecord) -> str:
    payload = json.dumps(plan_verification_payload(plan), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def plan_verification_snapshot(plan: PlanRecord) -> dict[str, object]:
    return {
        "updated_at": plan.updated_at,
        "content_hash": plan_verification_hash(plan),
        "validation_checklist": list(plan.validation_checklist),
    }


def parse_timestamp(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def verification_commands(run) -> list[str]:
    commands = run.environment.get("commands", [])
    if isinstance(commands, list):
        values: list[str] = []
        for item in commands:
            if isinstance(item, dict) and isinstance(item.get("command"), str):
                values.append(item["command"])
        if values:
            return values
    return [part.strip() for part in run.command.split(" && ") if part.strip()]


def verification_plan_snapshot(run) -> dict[str, object]:
    plan_snapshot = run.environment.get("plan")
    return plan_snapshot if isinstance(plan_snapshot, dict) else {}


def append_git_stale_reasons(reasons: list[str], run, cwd: Path | None = None) -> None:
    recorded_git = run.environment.get("git")
    if not isinstance(recorded_git, dict) or not recorded_git.get("available"):
        return

    from .verifications import git_metadata

    root = Path.cwd() if cwd is None else Path(cwd)
    current_git = git_metadata(root)
    if not current_git.get("available"):
        return
    if recorded_git.get("commit") != current_git.get("commit"):
        reasons.append("git_commit_changed")
    if recorded_git.get("status_hash") != current_git.get("status_hash"):
        reasons.append("git_status_changed")


def verification_freshness_summary(plan: PlanRecord, cwd: Path | None = None) -> dict[str, object]:
    if not plan.verification_runs:
        return {
            "latest_id": None,
            "result": None,
            "trust_level": "unknown",
            "stale": True,
            "reasons": ["no_verification_runs"],
        }

    from .verifications import load_verification

    latest = load_verification(plan.verification_runs[-1], cwd)
    reasons: list[str] = []
    snapshot = verification_plan_snapshot(latest)
    snapshot_hash = snapshot.get("content_hash")
    if isinstance(snapshot_hash, str) and snapshot_hash != plan_verification_hash(plan):
        reasons.append("plan_updated_after_verification")
    elif not snapshot_hash:
        plan_updated = parse_timestamp(plan.updated_at)
        verification_created = parse_timestamp(latest.created_at)
        if plan_updated and verification_created and plan_updated > verification_created:
            reasons.append("plan_updated_after_verification")
    if verification_commands(latest) != list(plan.validation_checklist):
        reasons.append("validation_checklist_changed")
    append_git_stale_reasons(reasons, latest, cwd)

    return {
        "latest_id": latest.id,
        "result": latest.result,
        "trust_level": latest.trust_level,
        "stale": bool(reasons),
        "reasons": reasons,
    }
