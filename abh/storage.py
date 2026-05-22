from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def root_dir(cwd: Path | None = None) -> Path:
    return Path.cwd() if cwd is None else Path(cwd)


def abh_dir(cwd: Path | None = None) -> Path:
    return root_dir(cwd) / ".abh"


def plans_dir(cwd: Path | None = None) -> Path:
    return abh_dir(cwd) / "plans"


def verifications_dir(cwd: Path | None = None) -> Path:
    return abh_dir(cwd) / "verifications"


def audits_dir(cwd: Path | None = None) -> Path:
    return abh_dir(cwd) / "audits"


def memory_dir(cwd: Path | None = None) -> Path:
    return abh_dir(cwd) / "memory"


def docs_dir(cwd: Path | None = None) -> Path:
    return root_dir(cwd) / "docs"


def docs_plans_dir(cwd: Path | None = None) -> Path:
    return docs_dir(cwd) / "plans"


def docs_audits_dir(cwd: Path | None = None) -> Path:
    return docs_dir(cwd) / "audits"


def docs_memory_dir(cwd: Path | None = None) -> Path:
    return docs_dir(cwd) / "memory"


def plan_json_path(plan_id: str, cwd: Path | None = None) -> Path:
    return plans_dir(cwd) / f"{plan_id}.json"


def plan_doc_path(plan_id: str, cwd: Path | None = None) -> Path:
    return docs_plans_dir(cwd) / f"{plan_id}.md"


def verification_path(run_id: str, cwd: Path | None = None) -> Path:
    return verifications_dir(cwd) / f"{run_id}.json"


def audit_json_path(audit_id: str, cwd: Path | None = None) -> Path:
    return audits_dir(cwd) / f"{audit_id}.json"


def audit_doc_path(audit_id: str, cwd: Path | None = None) -> Path:
    return docs_audits_dir(cwd) / f"{audit_id}.md"


def memory_json_path(memory_id: str, cwd: Path | None = None) -> Path:
    return memory_dir(cwd) / f"{memory_id}.json"


def memory_doc_path(memory_id: str, cwd: Path | None = None) -> Path:
    return docs_memory_dir(cwd) / f"{memory_id}.md"


def ensure_workspace(cwd: Path | None = None) -> None:
    for directory in (
        abh_dir(cwd),
        plans_dir(cwd),
        verifications_dir(cwd),
        audits_dir(cwd),
        memory_dir(cwd),
        docs_plans_dir(cwd),
        docs_audits_dir(cwd),
        docs_memory_dir(cwd),
    ):
        directory.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
