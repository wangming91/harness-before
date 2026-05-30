# Plan: Drift Quality

## Metadata

- ID: plan-040-drift-quality
- Status: closed
- Attractor: docs/architecture/attractors/abh-core-attractor.md
- Baseline: Current drift analysis is simple rule-based detection and plan non-goal checking. After the quality signal model is defined, drift findings should carry enough evidence for a human or agent to judge where the product is drifting and whether it needs action now.
- Owner: platform
- Created: 2026-05-29T13:01:02.244412+00:00
- Updated: 2026-05-29T13:16:13.695673+00:00

## Goals

- Add structured drift finding metadata for severity, confidence, rule id, matched span, source excerpt, evidence path, and recommendation.
- Preserve backward-compatible reads for existing drift reports.
- Expose the enriched drift findings through CLI JSON output and MCP drift surfaces.
- Document how drift quality signals should feed memory reuse, route ranking, project health, and abh next recommendations.

## Non-Goals

- Do not replace the local rule-based drift engine with an LLM or external service.
- Do not implement memory indexing, health reports, team policy, CI templates, or release automation in this slice.
- Do not make drift findings automatically block plan close.

## Exit Criteria

- New drift reports include structured finding metadata for severity, confidence, matched span, excerpt, evidence, and recommendation.
- Existing drift reports without the new fields remain readable.
- abh drift analyze --json returns enriched findings in the standard JSON envelope.
- MCP drift tools expose the same structured content.
- Tests cover non-goal drift, generic drift rules, legacy drift reads, and JSON output.

## Validation Checklist

- python3 -m unittest tests/test_cli.py -v
- python3 -m abh doctor
- git diff --check
- python3 -m abh roadmap check --json

## Closure Evidence

- abh/models.py
- abh/drift.py
- abh/cli.py
- abh/mcp_server.py
- tests/test_cli.py
- README.md
- docs/architecture/quality-signals.md
- docs/development-roadmap.md
- docs/task-board.md
- docs/context/codebase-map.md
- audit-040-drift-quality

## Verification Runs

- ver-3595509d65f3

## Audits

- audit-040-drift-quality
