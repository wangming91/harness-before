# Plan: Verify Runner MVP

## Metadata

- ID: plan-016-verify-runner
- Status: closed
- Attractor: docs/architecture/attractors/abh-core-attractor.md
- Baseline: docs/development-roadmap.md
- Owner: platform
- Created: 2026-05-24T06:20:25.601984+00:00
- Updated: 2026-05-24T07:26:01.755742+00:00

## Goals

- 实现 abh verify run <plan_id>，让 ABH 能执行计划验证命令并记录机器证据
- 按 plan validation checklist 执行本地命令，生成 pass/fail verification run
- 失败验证沿用现有状态机阻断 ready/running plan

## Non-Goals

- 不实现 plan update
- 不新增 MCP verify run 写工具
- 不重构 core.py 模块边界
- 不实现隔离环境或 CI runner

## Exit Criteria

- abh verify run <plan_id> 可执行 validation checklist 中的命令
- 执行成功时写入 pass verification 并关联 plan
- 执行失败时写入 fail verification、记录 failed check，并阻断 ready/running plan
- verify run 支持 JSON 输出或保持与现有 CLI 错误约定兼容
- README、roadmap、task-board 同步阶段 3 启动状态

## Validation Checklist

- python3 -m unittest tests/test_cli.py -v
- python3 -m abh doctor
- python3 -m abh verify --help

## Closure Evidence

- abh/core.py
- abh/cli.py
- tests/test_cli.py
- README.md
- docs/development-roadmap.md
- docs/task-board.md
- audit-016-verify-runner

## Verification Runs

- ver-b0ece5bd6f54
- ver-b6a153d6103e
- ver-d404ead3151a
- ver-0fe4fce2ad35

## Audits

- audit-016-verify-runner
