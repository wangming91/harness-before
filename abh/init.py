from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .attractors import create_attractor, list_attractors
from .errors import AbhError
from .storage import (
    abh_dir,
    audits_dir,
    attractors_dir,
    docs_attractors_dir,
    docs_audits_dir,
    docs_dir,
    docs_memory_dir,
    docs_plans_dir,
    memory_dir,
    plans_dir,
    root_dir,
    verifications_dir,
    write_text,
)


DEFAULT_ATTRACTOR_ID = "attractor-abh-core"
DEFAULT_ATTRACTOR_PATH = "docs/architecture/attractors/abh-core-attractor.md"


@dataclass(frozen=True, slots=True)
class InitAction:
    path: str
    kind: str
    reason: str
    content: str = ""

    def to_dict(self) -> dict[str, str]:
        return {"path": self.path, "kind": self.kind, "reason": self.reason}


def _relative(path: Path, cwd: Path) -> str:
    return path.relative_to(cwd).as_posix()


def _directory_action(path: Path, cwd: Path, reason: str) -> InitAction:
    return InitAction(path=_relative(path, cwd), kind="directory", reason=reason)


def _file_action(path: str, reason: str, content: str) -> InitAction:
    return InitAction(path=path, kind="file", reason=reason, content=content)


def _index_doc() -> str:
    return (
        "# ABH Documentation Index\n\n"
        "This index routes Agent and maintainer questions to the owner docs that should answer them.\n\n"
        "## Required Reading Order\n\n"
        "1. `docs/architecture/attractors/abh-core-attractor.md`\n"
        "2. `docs/context/project-context.md`\n"
        "3. `docs/context/source-of-truth.md`\n"
        "4. `docs/context/conventions.md`\n"
        "5. `docs/context/codebase-map.md`\n"
        "6. `docs/development-roadmap.md`\n"
        "7. `docs/architecture/agent-protocol.md`\n"
    )


def _source_of_truth_doc() -> str:
    return (
        "# Source of Truth\n\n"
        "Repository files are the truth surface, but no single file answers every question.\n\n"
        "## Precedence\n\n"
        "- Active attractor: long-term convergence target.\n"
        "- Plan: scope, non-goals, exit criteria, and validation checklist for one slice.\n"
        "- Code and tests: current implementation behavior.\n"
        "- Verification records: commands that actually ran.\n"
        "- Audit records: completion judgment for closure.\n"
        "- Roadmap queue: future intent before a plan is materialized.\n"
    )


def _project_context_doc() -> str:
    return (
        "# Project Context\n\n"
        "This repository uses Attractor Before Harness to keep AI-assisted work evidence-first and convergent.\n\n"
        "## Operating Model\n\n"
        "- Start from the active attractor.\n"
        "- Materialize or create a plan before implementation.\n"
        "- Verify with recorded commands.\n"
        "- Close only after independent audit.\n"
    )


def _conventions_doc() -> str:
    return (
        "# ABH Conventions\n\n"
        "- Future work starts as a roadmap queue key before it becomes a concrete plan id.\n"
        "- Plans must bind to the active attractor before running.\n"
        "- Verification is evidence, not completion.\n"
        "- Audit is the completion decision layer.\n"
        "- Memory is for reusable lessons, not ordinary progress updates.\n"
    )


def _codebase_map_doc() -> str:
    return (
        "# Codebase Map\n\n"
        "- `.abh/` stores machine-readable ABH state.\n"
        "- `docs/` stores human-readable mirrors and owner docs.\n"
        "- `docs/architecture/attractors/` stores attractor documents.\n"
        "- `docs/plans/`, `docs/audits/`, and `docs/memory/` store control records.\n"
    )


def _requirements_readme_doc() -> str:
    return (
        "# Requirements\n\n"
        "Implementation-ready requirements live here when a slice needs durable product or behavior requirements.\n\n"
        "Use this layer for what the system must do. Keep implementation plans in `docs/plans/`.\n"
    )


def _design_readme_doc() -> str:
    return (
        "# Design\n\n"
        "Application behavior, workflows, and user-facing design notes live here when they need to outlive one plan.\n\n"
        "Use this layer for how the product experience should behave. Keep technical structure in `docs/architecture/`.\n"
    )


def _attractor_doc() -> str:
    return (
        "# Attractor: ABH Core\n\n"
        "## Intent\n\n"
        "Keep this repository converging around a Git-native, evidence-first, audit-gated workflow.\n\n"
        "## Invariants\n\n"
        "- Work starts from an active attractor.\n"
        "- Implementation slices close through plan, verification, audit, and memory when needed.\n"
        "- Machine-readable state and Markdown records must stay consistent.\n"
    )


def _readme_doc() -> str:
    return (
        "# ABH Workspace\n\n"
        "This repository has been initialized for Attractor Before Harness.\n\n"
        "Start by reading `docs/index.md`, then bind work to the active attractor before implementation.\n"
    )


def planned_init_actions(cwd: Path | None = None) -> list[InitAction]:
    root = root_dir(cwd)
    return [
        _directory_action(abh_dir(root), root, "ABH machine-readable state root"),
        _directory_action(plans_dir(root), root, "plan JSON records"),
        _directory_action(audits_dir(root), root, "audit JSON records"),
        _directory_action(verifications_dir(root), root, "verification JSON records"),
        _directory_action(attractors_dir(root), root, "attractor JSON records"),
        _directory_action(memory_dir(root), root, "memory JSON records"),
        _directory_action(docs_dir(root), root, "ABH human-readable docs root"),
        _directory_action(docs_plans_dir(root), root, "plan Markdown records"),
        _directory_action(docs_audits_dir(root), root, "audit Markdown records"),
        _directory_action(docs_memory_dir(root), root, "memory Markdown records"),
        _directory_action(docs_attractors_dir(root), root, "attractor Markdown records"),
        _directory_action(root / "docs" / "context", root, "AGE owner-doc context"),
        _directory_action(root / "docs" / "requirements", root, "implementation-ready requirements"),
        _directory_action(root / "docs" / "design", root, "application design docs"),
        InitAction(path=".abh/attractors/attractor-abh-core.json", kind="generated_file", reason="default active attractor registry record"),
        _file_action("README.md", "minimal ABH workspace README", _readme_doc()),
        _file_action("docs/index.md", "documentation routing entry", _index_doc()),
        _file_action("docs/context/source-of-truth.md", "source-of-truth precedence", _source_of_truth_doc()),
        _file_action("docs/context/project-context.md", "project context", _project_context_doc()),
        _file_action("docs/context/conventions.md", "ABH conventions", _conventions_doc()),
        _file_action("docs/context/codebase-map.md", "codebase map", _codebase_map_doc()),
        _file_action("docs/requirements/README.md", "requirements owner-doc placeholder", _requirements_readme_doc()),
        _file_action("docs/design/README.md", "design owner-doc placeholder", _design_readme_doc()),
        _file_action(DEFAULT_ATTRACTOR_PATH, "default active attractor document", _attractor_doc()),
    ]


def _existing_reserved_files(cwd: Path) -> list[InitAction]:
    skips: list[InitAction] = []
    for path_text in ("AGENTS.md", "CLAUDE.md"):
        if (cwd / path_text).exists():
            skips.append(InitAction(path=path_text, kind="file", reason="existing agent setup file is reserved for a future setup command"))
    return skips


def preview_init(*, cwd: Path | None = None, write: bool = False, confirmed: bool = False) -> dict[str, object]:
    root = root_dir(cwd)
    actions = planned_init_actions(root)
    writes: list[InitAction] = []
    skips: list[InitAction] = _existing_reserved_files(root)
    for action in actions:
        path = root / action.path
        if path.exists():
            skips.append(InitAction(path=action.path, kind=action.kind, reason="already exists; will not overwrite"))
        else:
            writes.append(action)
    return {
        "mode": "write" if write else "preview",
        "write": write,
        "confirmed": confirmed,
        "active_attractor": {
            "id": DEFAULT_ATTRACTOR_ID,
            "path": DEFAULT_ATTRACTOR_PATH,
            "source": "default",
        },
        "writes": [action.to_dict() for action in writes],
        "skips": [action.to_dict() for action in skips],
        "blockers": [],
    }


def run_init(*, cwd: Path | None = None, write: bool = False, confirmed: bool = False) -> dict[str, object]:
    if write and not confirmed:
        raise AbhError("abh init --write requires --confirm")
    root = root_dir(cwd)
    result = preview_init(cwd=root, write=write, confirmed=confirmed)
    if not write:
        return result
    for action in planned_init_actions(root):
        path = root / action.path
        if path.exists():
            continue
        if action.kind == "directory":
            path.mkdir(parents=True, exist_ok=True)
        elif action.kind == "file":
            write_text(path, action.content)
    if not list_attractors(root):
        create_attractor(
            attractor_id=DEFAULT_ATTRACTOR_ID,
            title="ABH Core",
            version="0.1.0",
            path=DEFAULT_ATTRACTOR_PATH,
            intent="Keep this repository converging around a Git-native, evidence-first, audit-gated workflow.",
            invariants=[
                "Work starts from an active attractor.",
                "Implementation slices close through plan, verification, audit, and memory when needed.",
                "Machine-readable state and Markdown records must stay consistent.",
            ],
            cwd=root,
        )
    return result
