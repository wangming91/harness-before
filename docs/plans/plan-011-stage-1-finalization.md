# Plan: Stage 1 Governance Finalization

## Metadata

- ID: plan-011-stage-1-finalization
- Status: closed
- Attractor: docs/architecture/attractors/abh-core-attractor.md
- Baseline: docs/development-roadmap.md
- Owner: platform
- Created: 2026-05-23T14:05:12.869653+00:00
- Updated: 2026-05-23T14:14:23.933745+00:00

## Goals

- 迁移历史 .abh JSON 对象补齐 schema_version
- 增强 abh doctor 检查 schema_version 和 doc_path 基础一致性
- 补齐 CI editable install 步骤提升发布路径可靠性
- 更新 roadmap/task-board 标记阶段 1 完成并顺延 verify-runner 到下一计划

## Non-Goals

- 不实现 verify run
- 不重构 core.py 模块拆分
- 不发布 PyPI

## Exit Criteria

- 所有 .abh 核心 JSON 对象包含 schema_version
- abh doctor 能发现缺失 schema_version 的 JSON 对象
- CI workflow 包含 python3 -m pip install -e .
- roadmap 显示阶段 1 完成且下一计划进入阶段 2 verify runner

## Validation Checklist

- python3 -m unittest tests/test_cli.py -v
- python3 -m abh doctor
- python3 -m abh plan list

## Closure Evidence

- docs/plans/plan-011-stage-1-finalization.md
- abh/core.py
- tests/test_cli.py
- .github/workflows/ci.yml
- docs/development-roadmap.md
- docs/task-board.md
- audit-011-stage-1-finalization

## Verification Runs

- ver-3cee2d5ffe61
- ver-3429dd7422bb
- ver-f31c39b5d6c8
- ver-9077c3ae82df

## Audits

- audit-011-stage-1-finalization
