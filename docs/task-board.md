# Attractor Before Harness 任务看板

## 当前阶段

 Sprint 4：路由与漂移分析

## 状态说明

- Todo：尚未开始。
- Doing：正在进行。
- Review：等待审查或验收。
- Done：已完成。

## Sprint 1

| ID | 任务 | 状态 | 产出 |
| --- | --- | --- | --- |
| S1-001 | 建立标准目录结构 | Done | `docs/architecture/`, `docs/plans/`, `docs/audits/`, `docs/memory/` |
| S1-002 | 编写 Attractor 模板 | Done | `docs/architecture/templates/attractor-template.md` |
| S1-003 | 编写 Plan 模板 | Done | `docs/plans/templates/plan-template.md` |
| S1-004 | 编写 Audit 模板 | Done | `docs/audits/templates/audit-template.md` |
| S1-005 | 编写 Memory 模板 | Done | `docs/memory/templates/memory-template.md` |
| S1-006 | 定义项目初始吸引子 | Done | `docs/architecture/attractors/abh-core-attractor.md` |
| S1-007 | 创建 Sprint 1 启动计划 | Done | `docs/plans/plan-001-sprint-1-foundation.md` |
| S1-008 | 创建 Sprint 1 审计占位 | Done | `docs/audits/audit-001-sprint-1-foundation.md` |
| S1-009 | 补充初始 memory 索引 | Done | `docs/memory/README.md` |
| S1-010 | 统一 memory taxonomy | Done | `docs/memory/README.md`, `docs/memory/templates/memory-template.md` |
| S1-011 | 补齐 architecture policies 目录 | Done | `docs/architecture/policies/README.md` |

## Sprint 2

| ID | 任务 | 状态 | 产出 |
| --- | --- | --- | --- |
| S2-001 | CLI 技术选型 | Done | Python standard library |
| S2-002 | CLI 项目骨架 | Done | `abh/`, `pyproject.toml` |
| S2-003 | Plan 创建命令 | Done | `abh plan create` |
| S2-004 | Plan 状态流转 | Done | `abh plan transition` |
| S2-005 | 验证结果记录 | Done | `abh verify record` |
| S2-006 | Sprint 2 启动计划 | Done | `docs/plans/plan-002-sprint-2-local-plan-loop.md` |
| S2-007 | Sprint 2 独立审计 | Done | `docs/audits/audit-002-sprint-2-local-plan-loop.md` |

## Sprint 3

| ID | 任务 | 状态 | 产出 |
| --- | --- | --- | --- |
| S3-001 | Audit 请求命令 | Done | `abh audit request` |
| S3-002 | Audit 记录命令 | Done | `abh audit record` |
| S3-003 | Plan 关闭命令 | Done | `abh close` |
| S3-004 | Memory 添加命令 | Done | `abh memory add` |
| S3-005 | Memory 检索命令 | Done | `abh memory search` |
| S3-006 | Sprint 3 启动计划 | Done | `docs/plans/plan-003-sprint-3-audit-memory-close.md` |
| S3-007 | Sprint 3 独立审计 | Done | `docs/audits/audit-003-sprint-3-audit-memory-close.md` |

## Sprint 4

| ID | 任务 | 状态 | 产出 |
| --- | --- | --- | --- |
| S4-001 | 路由规则设计 | Todo | route rules |
| S4-002 | Route 命令 | Todo | `abh route` |
| S4-003 | 漂移分类规则 | Todo | drift taxonomy |
| S4-004 | Drift 分析命令 | Todo | `abh drift analyze` |
| S4-005 | 漂移转 follow-up | Todo | follow-up generator |
