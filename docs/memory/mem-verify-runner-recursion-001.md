# Memory: verify runner checklist must avoid recursive self-invocation

## Metadata

- ID: mem-verify-runner-recursion-001
- Type: divergent_pattern
- Status: active
- Created: 2026-05-24T06:25:45.799375+00:00
- Updated: 2026-05-24T06:25:45.799558+00:00
- Related: plan-016-verify-runner

## Summary

verify runner checklist must avoid recursive self-invocation

## Context

During plan-016 dogfooding, the initial validation checklist included python3 -m abh verify run plan-016-verify-runner. A runner that blindly executes the checklist would recursively invoke itself.

## Evidence

- docs/plans/plan-016-verify-runner.md
- .abh/plans/plan-016-verify-runner.json

## Implication

Future verify runner and plan update work should detect or document recursive self-invocation risks, and dogfood plans should use non-recursive smoke commands unless recursion is intentionally tested.

## Deprecation Policy

Mark deprecated when evidence no longer applies.
