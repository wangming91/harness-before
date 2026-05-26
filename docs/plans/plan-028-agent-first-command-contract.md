# Plan: Agent-First Command Contract

## Metadata

- ID: plan-028-agent-first-command-contract
- Status: closed
- Attractor: docs/architecture/attractors/abh-core-attractor.md
- Baseline: Stage 4 has a documented Agent-First direction, but CLI JSON helpers and MCP tool schemas still duplicate command contract metadata; MCP plan status also lacks the CLI verification_summary.
- Owner: platform
- Created: 2026-05-25T16:16:31.346354+00:00
- Updated: 2026-05-26T08:35:04.347867+00:00

## Goals

- Introduce a shared Agent-First command contract module that records stable command ids, tool names, read/write classification, confirmation boundary, side effects, and MCP input schemas for existing agent-facing commands.
- Make CLI JSON envelope/error helpers and MCP tool metadata consume the shared contract where practical without changing existing user-facing command names.
- Align MCP abh_plan_status output with CLI plan status --json by returning verification_summary.
- Document plan-028 as the Stage 4 implementation foundation for attractor registry, init, agent setup, hooks, next, and onboarding checks.

## Non-Goals

- Do not implement abh attractor, abh init, abh agent setup, hooks, abh next, onboarding check, distribution, or new user-visible commands in this slice.
- Do not change plan/audit/verification state machines, close gates, stale semantics, storage format, or MCP write confirmation rules.
- Do not redesign CLI argparse structure beyond reusing shared contract helpers.

## Exit Criteria

- A shared command contract module exists and covers current agent-facing CLI/MCP commands with stable command ids, read/write classification, confirmation boundary, and side effects.
- MCP tool definitions are generated from shared command contract metadata instead of a separate ad hoc schema table.
- CLI JSON envelope and structured ABH errors are provided by the shared contract/helper layer while preserving current JSON shape.
- MCP abh_plan_status returns verification_summary matching CLI plan status --json.
- python3 -m unittest tests/test_cli.py -v passes.
- python3 -m abh doctor passes.

## Validation Checklist

- python3 -m unittest tests/test_cli.py -v
- python3 -m abh doctor
- git diff --check
- python3 -m abh plan status plan-028-agent-first-command-contract --json

## Closure Evidence

- docs/plans/plan-028-agent-first-command-contract.md
- tests/test_cli.py
- abh/commands.py
- abh/cli.py
- abh/mcp_server.py
- docs/architecture/agent-protocol.md
- audit-028-agent-first-command-contract

## Verification Runs

- ver-4d435668387f
- ver-400d1483ff53
- ver-f92d4091f4e4

## Audits

- audit-028-agent-first-command-contract
