# Plan: ABH Init Active Attractor

## Metadata

- ID: plan-032-abh-init-active-attractor
- Status: closed
- Attractor: docs/architecture/attractors/abh-core-attractor.md
- Baseline: Stage 4 already has Agent-First command contracts and Attractor Registry; repository initialization should bind new workspaces to active attractor without preassigning plan numbers in documentation.
- Owner: platform
- Created: 2026-05-27T05:10:35.347196+00:00
- Updated: 2026-05-27T08:16:23.289131+00:00

## Goals

- Create a non-interactive abh init flow that prepares .abh, docs directories, docs/index.md, and docs/context owner docs around the active attractor.
- Provide machine-readable preview output before writing project files.
- Avoid silent overwrite of existing README, AGENTS.md, CLAUDE.md, .abh, or docs templates.

## Non-Goals

- Do not implement agent setup, hooks, abh next, onboarding check, or distribution in this slice.

## Exit Criteria

- abh init can initialize a new workspace with an active attractor and minimum ABH directories.
- Existing files are not silently overwritten.
- Initialization output is machine-readable and suitable for agent use.

## Validation Checklist

- python3 -m unittest tests/test_cli.py -v
- python3 -m abh doctor
- git diff --check
- python3 -m abh roadmap check --json

## Closure Evidence

- README.md
- docs/development-roadmap.md
- docs/阶段规划.md
- docs/task-board.md
- docs/architecture/agent-protocol.md
- docs/architecture/README.md
- abh/init.py
- abh/cli.py
- abh/commands.py
- tests/test_cli.py
- docs/context/codebase-map.md
- docs/requirements/README.md
- docs/design/README.md
- audit-032-abh-init-active-attractor

## Verification Runs

- ver-bf9b76cdfaab
- ver-1e9ba9045ad4

## Audits

- audit-032-abh-init-active-attractor
