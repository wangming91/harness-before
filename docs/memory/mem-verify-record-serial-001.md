# Memory: Parallel verify record can drop plan verification references

## Metadata

- ID: mem-verify-record-serial-001
- Type: divergent_pattern
- Status: active
- Created: 2026-05-24T03:24:48.321609+00:00
- Updated: 2026-05-24T03:24:48.321808+00:00
- Related: plan-014-readonly-mcp-server

## Summary

Parallel verify record can drop plan verification references

## Context

During plan-014, three python3 -m abh verify record commands were run in parallel. All three verification JSON files were created, but the plan record kept only two verification run references because each command read and rewrote the same plan file independently.

## Evidence

- .abh/plans/plan-014-readonly-mcp-server.json
- .abh/verifications/ver-51297abb60e4.json

## Implication

Run .abh state-mutating commands sequentially unless the command itself has concurrency control; otherwise plan/audit/memory indexes can lose updates even when individual JSON artifacts exist.

## Deprecation Policy

Mark deprecated when evidence no longer applies.
