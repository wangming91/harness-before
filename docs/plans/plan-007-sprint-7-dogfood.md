# Plan: Sprint 7: Dogfooding 驱动的基础能力深化

## Metadata

- ID: plan-007-sprint-7-dogfood
- Status: closed
- Attractor: docs/architecture/attractors/abh-core-attractor.md
- Baseline: docs/development-roadmap.md
- Owner: platform
- Created: 2026-05-22T16:25:21.772170+00:00
- Updated: 2026-05-22T16:34:01.611612+00:00

## Goals

- 新增 plan list / memory list / audit list 查询命令
- 改进 route 命令以支持扫描计划状态
- 改进 drift 命令以 plan 基准做对比分析

## Non-Goals

- 不修改吸引子定义
- 不重构存储层
- 不新增 CLI 范式以外的命令

## Exit Criteria

- plan list 可列出所有计划并显示 id/title/status
- memory list 可列出所有记忆
- audit list 可列出所有审计
- route 能根据计划状态给出更精准的阅读顺序
- drift 能以 plan 的 goals/non-goals 为基准做检测
- 新功能有测试覆盖且全通过

## Validation Checklist

- python3 -m unittest tests/test_cli.py -v

## Closure Evidence

- docs/plans/plan-007-sprint-7-dogfood.md
- tests/test_cli.py
- audit-007-sprint-7-dogfood

## Verification Runs

- ver-1e5c121459fc

## Audits

- audit-007-sprint-7-dogfood
