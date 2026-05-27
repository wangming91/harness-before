# Plan: Git Hooks Guardrails

## Metadata

- ID: plan-034-git-hooks-guardrails
- Status: closed
- Attractor: docs/architecture/attractors/abh-core-attractor.md
- Baseline: Install ABH hook profiles that protect plan, verification, audit, and doctor invariants.
- Owner: platform
- Created: 2026-05-27T15:36:37.283453+00:00
- Updated: 2026-05-27T16:24:00.572057+00:00

## Goals

- Add shared Agent-First command contract entries for local hook profile inspection and installation.
- Expose abh hooks profile --json as a read-only preview of the default pre-commit guardrail profile.
- Expose abh hooks install --write --confirm --json to install a managed local .git/hooks/pre-commit guardrail hook.
- The managed hook should run lightweight ABH invariants: python3 -m abh doctor, python3 -m abh roadmap check --json, and git diff --check.
- Document the hook guardrail MVP in README, Agent Protocol, roadmap, task-board, and codebase map.

## Non-Goals

- Do not install hooks without both --write and --confirm.
- Do not overwrite a non-ABH existing hook; report it as a blocker instead.
- Do not implement team policy, remote hook distribution, release automation, or post-commit/pre-push profiles in this slice.
- Do not change plan, verification, audit, close, or doctor state machines beyond adding hook guardrail commands.

## Exit Criteria

- abh hooks profile --json returns a stable profile payload with hook path, managed marker, commands, invariants, and write policy.
- abh hooks install --json previews the install without writing .git/hooks/pre-commit.
- abh hooks install --write --json fails with a structured confirmation error and does not write the hook.
- abh hooks install --write --confirm --json creates an executable managed .git/hooks/pre-commit hook when no conflicting hook exists.
- Existing non-managed hooks are not overwritten and are reported as blockers.
- Hook commands are represented in abh.commands before or alongside the CLI adapter.

## Validation Checklist

- python3 -m unittest tests/test_cli.py -v
- python3 -m abh doctor
- git diff --check
- python3 -m abh roadmap check --json
- python3 -m abh hooks profile --json
- python3 -m abh hooks install --json
- python3 -m abh plan status plan-034-git-hooks-guardrails --json

## Closure Evidence

- README.md
- docs/development-roadmap.md
- docs/task-board.md
- docs/architecture/agent-protocol.md
- docs/context/codebase-map.md
- abh/hooks.py
- abh/cli.py
- abh/commands.py
- tests/test_cli.py
- audit-034-git-hooks-guardrails

## Verification Runs

- ver-4b6212dd48da

## Audits

- audit-034-git-hooks-guardrails
