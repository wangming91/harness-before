# Plan: 能力深化与 Dogfooding 闭环

## Metadata

- ID: plan-006-stabilize
- Status: closed
- Attractor: docs/architecture/attractors/abh-core-attractor.md
- Baseline: docs/development-roadmap.md
- Owner: platform
- Created: 2026-05-22T15:59:30.983999+00:00
- Updated: 2026-05-22T16:06:56.564404+00:00

## Goals

- 将历史计划迁移到 abh CLI 管理
- 补充 drift/memory 运行时目录的自动初始化
- 确保所有已知的 README 问题已被修正并通过审计

## Non-Goals

- 引入外部数据库
- 重构 CLI 参数结构

## Exit Criteria

- 至少有一条通过 audit 关闭的本项目计划
- docs/ 下所有计划文档与 .abh/ JSON 状态一致

## Validation Checklist

- python -m unittest tests/test_cli.py
- 所有 abh 命令 smoke test 通过

## Closure Evidence

- docs/audits/audit-006-stabilize.md
- docs/plans/plan-006-stabilize.md
- audit-006-stabilize

## Verification Runs

- ver-f19cba2675de

## Audits

- audit-006-stabilize
