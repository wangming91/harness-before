from __future__ import annotations

from pathlib import Path

from .attractors import active_attractor
from .commands import command_contract


AGENT_TARGETS = ("codex", "claude-code", "mcp")

REQUIRED_READING = [
    "docs/architecture/attractors/abh-core-attractor.md",
    "docs/index.md",
    "docs/context/source-of-truth.md",
    "docs/architecture/agent-protocol.md",
]

WORKFLOW_RULES = [
    "no plan, no implementation work",
    "verification is evidence, not completion",
    "close requires independent audit",
    "failures and false assumptions belong in memory when they can prevent repeat mistakes",
]

RECOMMENDED_COMMANDS = [
    "attractor.active",
    "roadmap.list",
    "plan.status",
    "verification.run",
]


def _recommended_command(command_id: str) -> str:
    command = command_contract(command_id).cli_command
    if command_id == "plan.status":
        command = f"{command} <plan-id>"
    elif command_id == "verification.run":
        command = f"{command} <plan-id>"
    return f"abh {command} --json"


def agent_setup_bundle(agent: str, *, cwd: Path | None = None) -> dict[str, object]:
    if agent not in AGENT_TARGETS:
        raise ValueError(f"unsupported agent setup target: {agent}")
    attractor = active_attractor(cwd)
    bundle: dict[str, object] = {
        "agent": agent,
        "active_attractor": {
            "id": attractor.id,
            "path": attractor.path,
            "title": attractor.title,
            "version": attractor.version,
        },
        "required_reading": list(REQUIRED_READING),
        "workflow_rules": list(WORKFLOW_RULES),
        "commands": [_recommended_command(command_id) for command_id in RECOMMENDED_COMMANDS],
        "write_policy": {
            "mode": "read_only",
            "writes": [],
            "reason": "setup export describes recommended files and commands; it does not write agent config files",
        },
    }
    if agent == "codex":
        bundle["target"] = {
            "config_file": "AGENTS.md",
            "description": "Use this bundle as Codex project instructions input.",
        }
    elif agent == "claude-code":
        bundle["target"] = {
            "config_file": "CLAUDE.md",
            "description": "Use this bundle as Claude Code project instructions input.",
        }
    else:
        bundle["server"] = {
            "command": "python3 -m abh.mcp_server",
            "transport": "stdio",
        }
        bundle["target"] = {
            "config_file": "MCP client config",
            "description": "Use this bundle to configure a generic MCP client manually.",
        }
    return bundle
