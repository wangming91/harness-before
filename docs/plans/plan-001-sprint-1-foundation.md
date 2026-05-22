# Plan: Sprint 1 Foundation

## Metadata

- ID: plan-001-sprint-1-foundation
- Status: closed
- Attractor: `docs/architecture/attractors/abh-core-attractor.md`
- Baseline: initial docs-only repository
- Owner: platform
- Created: 2026-05-22

## Goals

- 建立正式 `docs/architecture/`、`docs/plans/`、`docs/audits/`、`docs/memory/` 结构。
- 提供 Attractor、Plan、Audit、Memory 四类模板。
- 定义项目第一个 active attractor。
- 建立当前 Sprint 的计划文档和审计占位。
- 让后续开发可以按照固定 plan/audit/memory 流程推进。

## Non-Goals

- 不实现 CLI。
- 不实现状态机代码。
- 不接入 CI。
- 不建设 Web UI。
- 不实现自动漂移分析。

## Exit Criteria

- `docs/architecture/README.md` 存在并说明 reading order。
- `docs/architecture/policies/README.md` 存在或已明确预留。
- `docs/architecture/templates/attractor-template.md` 存在。
- `docs/plans/templates/plan-template.md` 存在。
- `docs/audits/templates/audit-template.md` 存在。
- `docs/memory/templates/memory-template.md` 存在。
- `docs/memory/README.md` 与 `docs/memory/templates/memory-template.md` 使用同一套 memory taxonomy。
- `docs/architecture/attractors/abh-core-attractor.md` 存在且状态为 active。
- `docs/audits/audit-001-sprint-1-foundation.md` 存在。
- `docs/task-board.md` 中 Sprint 1 任务状态与实际产物一致。

## Validation Checklist

- 检查所有目录和文件是否存在。
- 检查模板是否包含 metadata、evidence 或等价字段。
- 检查 active attractor 是否包含 invariants、boundary rules、dependency rules。
- 检查 plan 是否包含 goals、non-goals、exit criteria、validation checklist、closure evidence。
- 检查 audit 占位是否引用本 plan。

## Closure Evidence

- `docs/development-roadmap.md`
- `docs/task-board.md`
- `docs/architecture/README.md`
- `docs/architecture/policies/README.md`
- `docs/architecture/templates/attractor-template.md`
- `docs/plans/templates/plan-template.md`
- `docs/audits/templates/audit-template.md`
- `docs/memory/templates/memory-template.md`
- `docs/memory/README.md`
- `docs/architecture/attractors/abh-core-attractor.md`
- `docs/audits/audit-001-sprint-1-foundation.md`

## Audit Requirement

关闭前需要独立审计确认：

- Sprint 1 产物是否满足 exit criteria。
- 是否存在空模板无法承载后续开发的问题。
- task board 状态是否与实际文件一致。

## Tasks

| ID | Task | Status | Evidence |
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

## Notes

- Sprint 1 只建立承载结构，不进入 CLI 实现。
- 下一轮开发应从 `abh` CLI 技术选型和项目骨架开始。
