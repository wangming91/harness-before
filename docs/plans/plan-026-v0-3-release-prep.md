# Plan: v0.3 Release Prep

## Metadata

- ID: plan-026-v0-3-release-prep
- Status: closed
- Attractor: docs/architecture/attractors/abh-core-attractor.md
- Baseline: Stage 3 v0.3 Verify Runner milestone is complete, but package metadata and README still report 0.2.0.
- Owner: platform
- Created: 2026-05-24T15:11:56.015997+00:00
- Updated: 2026-05-24T15:19:01.980997+00:00

## Goals

- Bump package version metadata from 0.2.0 to 0.3.0 in pyproject.toml and abh.__version__.
- Update README, roadmap, task-board, and 阶段规划 so v0.3.0 is the current formal release and Stage 4 Attractor Registry starts after release prep.
- Add release notes for v0.3.0 summarizing Stage 1 through Stage 3 capabilities, validation evidence, and known limitations.
- Validate install, CLI, tests, doctor, JSON smoke, and release tag readiness before publishing v0.3.0.

## Non-Goals

- Do not implement Attractor Registry or any Stage 4 feature in this slice.
- Do not change CLI/MCP behavior, JSON schema semantics, plan/audit/verification state machines, close gates, stale semantics, storage behavior, or algorithms.
- Do not publish to PyPI in this slice.

## Exit Criteria

- pyproject.toml and abh/__init__.py both report version 0.3.0.
- README declares current version 0.3.0 and docs consistently say Stage 4 Attractor Registry starts after release prep.
- docs/releases/v0.3.0.md exists and contains release scope, validation commands, and known limitations.
- python3 -m unittest tests/test_cli.py -v passes.
- python3 -m abh doctor passes.
- Editable install smoke passes and console script reports ABH 0.3.0.

## Validation Checklist

- python3 -m unittest tests/test_cli.py -v
- python3 -m abh doctor
- python3 -m compileall abh tests
- git diff --check
- python3 -m abh plan status plan-026-v0-3-release-prep --json

## Closure Evidence

- docs/releases/v0.3.0.md
- README.md
- docs/development-roadmap.md
- docs/task-board.md
- docs/阶段规划.md
- pyproject.toml
- abh/__init__.py
- .abh/verifications/ver-55454a0d3263.json
- Editable install smoke: abh-0.3.0 wheel built and console script doctor/version checks passed
- audit-026-v0-3-release-prep

## Verification Runs

- ver-55454a0d3263
- ver-eff568515f85

## Audits

- audit-026-v0-3-release-prep
