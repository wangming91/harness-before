# Plan: Sprint 8 Roadmap Sync and Doctor

## Metadata

- ID: plan-008-roadmap-sync-and-doctor
- Status: closed
- Attractor: docs/architecture/attractors/abh-core-attractor.md
- Baseline: docs/development-roadmap.md
- Owner: platform
- Created: 2026-05-23T07:22:28.746295+00:00
- Updated: 2026-05-23T07:46:36.308593+00:00

## Goals

- 同步长期路线图与任务看板到当前进度
- 新增 abh doctor 一致性检查命令
- 为 doctor 行为补充测试覆盖

## Non-Goals

- 不重构存储层
- 不新增外部依赖
- 不引入 Web UI 或服务端

## Exit Criteria

- abh doctor 可检查 docs 与 .abh 的核心对象一致性
- README、development-roadmap、task-board 均反映 Sprint 8 和 doctor
- 现有 CLI 测试全部通过

## Validation Checklist

- python3 -m unittest tests/test_cli.py -v
- python3 -m abh doctor

## Closure Evidence

- docs/plans/plan-008-roadmap-sync-and-doctor.md
- tests/test_cli.py
- abh/core.py
- abh/cli.py
- docs/development-roadmap.md
- docs/task-board.md
- audit-008-roadmap-sync-and-doctor

## Verification Runs

- ver-6e38644ea959
- ver-a8dd4f580af3

## Audits

- audit-008-roadmap-sync-and-doctor
