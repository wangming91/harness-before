# Plan: Agent Contract Setup

## Metadata

- ID: plan-033-agent-contract-setup
- Status: closed
- Attractor: docs/architecture/attractors/abh-core-attractor.md
- Baseline: Stage 4 already has active attractor, Agent-First command contracts, roadmap queue, AGE owner docs, and abh init. This slice exports read-only setup bundles for Codex, Claude Code, and generic MCP clients from the shared command contract.
- Owner: platform
- Created: 2026-05-27T12:47:15.087350+00:00
- Updated: 2026-05-27T15:29:10.799126+00:00

## Goals

- Expose non-interactive JSON setup bundles for Codex, Claude Code, and generic MCP clients.
- Derive the setup bundle from the shared Agent-First command contract, active attractor, and AGE owner-doc baseline.
- Keep this slice read-only: setup commands explain recommended files and commands but do not write AGENTS.md, CLAUDE.md, MCP config, hooks, or repository files.

## Non-Goals

- Do not implement setup file writes, hook installation, abh next, onboarding check, distribution, or MCP write tools in this slice.
- Do not change existing MCP server runtime behavior beyond documenting setup bundle output.

## Exit Criteria

- abh agent setup codex --json returns a stable setup bundle with active attractor, required reading, workflow rules, recommended commands, and write policy.
- abh agent setup claude-code --json returns the same contract shape with Claude Code-specific setup target metadata.
- abh agent setup mcp --json returns generic MCP setup metadata including python3 -m abh.mcp_server server command.
- Setup command contracts are registered in abh.commands before or alongside CLI adapters.
- README, Agent Protocol, roadmap, task-board, and codebase map describe the setup export MVP and its non-write boundary.

## Validation Checklist

- python3 -m unittest tests/test_cli.py -v
- python3 -m abh doctor
- git diff --check
- python3 -m abh roadmap check --json

## Closure Evidence

- README.md
- docs/development-roadmap.md
- docs/task-board.md
- docs/architecture/agent-protocol.md
- docs/context/codebase-map.md
- abh/agent_setup.py
- abh/cli.py
- abh/commands.py
- tests/test_cli.py
- audit-033-agent-contract-setup

## Verification Runs

- ver-bbc14588405b
- ver-7015dd17f30b
- ver-442291d3dee0
- ver-c7909ee03a12
- ver-61c77ac21c9b
- ver-36d72d698245
- ver-36f29e9dd356
- ver-25a1f3a18265

## Audits

- audit-033-agent-contract-setup
