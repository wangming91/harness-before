from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

PLAN_STATUSES = ("draft", "ready", "running", "blocked", "closing", "closed")
VERIFICATION_RESULTS = ("pass", "fail", "partial")
AUDIT_RESULTS = ("pass", "fail", "partial", "need_info")
MEMORY_TYPES = ("false_assumption", "rejected_path", "divergent_pattern", "overturned_completion")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(slots=True)
class VerificationRun:
    id: str
    plan_id: str
    command: str
    result: str
    artifacts: list[str] = field(default_factory=list)
    failed_checks: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "plan_id": self.plan_id,
            "command": self.command,
            "result": self.result,
            "artifacts": list(self.artifacts),
            "failed_checks": list(self.failed_checks),
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "VerificationRun":
        return cls(
            id=data["id"],
            plan_id=data["plan_id"],
            command=data["command"],
            result=data["result"],
            artifacts=list(data.get("artifacts", [])),
            failed_checks=list(data.get("failed_checks", [])),
            created_at=data.get("created_at", utc_now()),
        )


@dataclass(slots=True)
class AuditFinding:
    severity: str
    finding: str
    evidence: str
    recommendation: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "severity": self.severity,
            "finding": self.finding,
            "evidence": self.evidence,
            "recommendation": self.recommendation,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AuditFinding":
        return cls(
            severity=data["severity"],
            finding=data["finding"],
            evidence=data["evidence"],
            recommendation=data["recommendation"],
        )


@dataclass(slots=True)
class AuditRecord:
    id: str
    plan_id: str
    auditor: str
    scope: str
    status: str = "requested"
    result: str = "need_info"
    rationale: str = ""
    evidence: list[str] = field(default_factory=list)
    findings: list[AuditFinding] = field(default_factory=list)
    follow_ups: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)
    doc_path: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "plan_id": self.plan_id,
            "auditor": self.auditor,
            "scope": self.scope,
            "status": self.status,
            "result": self.result,
            "rationale": self.rationale,
            "evidence": list(self.evidence),
            "findings": [finding.to_dict() for finding in self.findings],
            "follow_ups": list(self.follow_ups),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "doc_path": self.doc_path,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AuditRecord":
        return cls(
            id=data["id"],
            plan_id=data["plan_id"],
            auditor=data["auditor"],
            scope=data["scope"],
            status=data.get("status", "requested"),
            result=data.get("result", "need_info"),
            rationale=data.get("rationale", ""),
            evidence=list(data.get("evidence", [])),
            findings=[AuditFinding.from_dict(item) for item in data.get("findings", [])],
            follow_ups=list(data.get("follow_ups", [])),
            created_at=data.get("created_at", utc_now()),
            updated_at=data.get("updated_at", utc_now()),
            doc_path=data.get("doc_path", ""),
        )


@dataclass(slots=True)
class MemoryRecord:
    id: str
    memory_type: str
    summary: str
    context: str
    implication: str
    status: str = "active"
    related: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    deprecation_policy: str = "Mark deprecated when evidence no longer applies."
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)
    doc_path: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "type": self.memory_type,
            "summary": self.summary,
            "context": self.context,
            "implication": self.implication,
            "status": self.status,
            "related": list(self.related),
            "evidence": list(self.evidence),
            "deprecation_policy": self.deprecation_policy,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "doc_path": self.doc_path,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MemoryRecord":
        return cls(
            id=data["id"],
            memory_type=data["type"],
            summary=data["summary"],
            context=data["context"],
            implication=data["implication"],
            status=data.get("status", "active"),
            related=list(data.get("related", [])),
            evidence=list(data.get("evidence", [])),
            deprecation_policy=data.get("deprecation_policy", "Mark deprecated when evidence no longer applies."),
            created_at=data.get("created_at", utc_now()),
            updated_at=data.get("updated_at", utc_now()),
            doc_path=data.get("doc_path", ""),
        )


@dataclass(slots=True)
class PlanRecord:
    id: str
    title: str
    attractor: str
    baseline: str
    owner: str = "platform"
    status: str = "draft"
    goals: list[str] = field(default_factory=list)
    non_goals: list[str] = field(default_factory=list)
    exit_criteria: list[str] = field(default_factory=list)
    validation_checklist: list[str] = field(default_factory=list)
    closure_evidence: list[str] = field(default_factory=list)
    verification_runs: list[str] = field(default_factory=list)
    audit_ids: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)
    doc_path: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "attractor": self.attractor,
            "baseline": self.baseline,
            "owner": self.owner,
            "status": self.status,
            "goals": list(self.goals),
            "non_goals": list(self.non_goals),
            "exit_criteria": list(self.exit_criteria),
            "validation_checklist": list(self.validation_checklist),
            "closure_evidence": list(self.closure_evidence),
            "verification_runs": list(self.verification_runs),
            "audit_ids": list(self.audit_ids),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "doc_path": self.doc_path,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PlanRecord":
        return cls(
            id=data["id"],
            title=data["title"],
            attractor=data["attractor"],
            baseline=data["baseline"],
            owner=data.get("owner", "platform"),
            status=data.get("status", "draft"),
            goals=list(data.get("goals", [])),
            non_goals=list(data.get("non_goals", [])),
            exit_criteria=list(data.get("exit_criteria", [])),
            validation_checklist=list(data.get("validation_checklist", [])),
            closure_evidence=list(data.get("closure_evidence", [])),
            verification_runs=list(data.get("verification_runs", [])),
            audit_ids=list(data.get("audit_ids", [])),
            created_at=data.get("created_at", utc_now()),
            updated_at=data.get("updated_at", utc_now()),
            doc_path=data.get("doc_path", ""),
        )
