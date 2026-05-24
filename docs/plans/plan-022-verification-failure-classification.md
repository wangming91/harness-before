# Plan: Verification Failure Classification

## Metadata

- ID: plan-022-verification-failure-classification
- Status: closed
- Attractor: docs/architecture/attractors/abh-core-attractor.md
- Baseline: Stage 3 verify run can execute validation checklist and record trust/stale metadata, but failed checks are still only raw command strings and artifacts, making validation failures, timeouts, recursive guards, and runner environment failures harder to audit.
- Owner: platform
- Created: 2026-05-24T12:33:36.852108+00:00
- Updated: 2026-05-24T12:49:28.802144+00:00

## Goals

- Persist structured failure classifications on verification records without changing pass/fail/partial semantics.
- Classify verify run failures as validation_failure, timeout, recursive_guard, environment_failure, or unknown as appropriate.
- Expose failure classifications through verify run --json and persisted verification JSON for audit use.
- Keep ready/running blocked behavior compatible with existing failed verification rules.

## Non-Goals

- Do not implement flaky retry, network diagnostics, automatic repair, CI execution, or isolated execution in this slice.
- Do not change close gate behavior or stale semantics.
- Do not bypass or weaken existing record_verification state transition rules.

## Exit Criteria

- Non-zero validation command records validation_failure classification with command and exit_code.
- Timeout records timeout classification with timeout_seconds.
- Recursive verify guard records recursive_guard classification without executing recursion.
- Runner OS/subprocess exception records environment_failure classification and produces a fail verification instead of crashing.
- Existing verification JSON without failure_classifications still loads successfully.
- python3 -m unittest tests/test_cli.py -v passes.
- python3 -m abh doctor passes.

## Validation Checklist

- python3 -m unittest tests/test_cli.py -v
- python3 -m abh doctor

## Closure Evidence

- tests/test_cli.py failure classification coverage
- docs synchronized for plan-022
- audit-022-verification-failure-classification
- .abh/verifications/ver-0b0b5694cf4f.json

## Verification Runs

- ver-a6d056905360
- ver-0b0b5694cf4f
- ver-2f52885cdfbf

## Audits

- audit-022-verification-failure-classification
