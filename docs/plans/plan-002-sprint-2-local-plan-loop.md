# Plan: Sprint 2 Local Plan Loop

## Metadata

- ID: plan-002-sprint-2-local-plan-loop
- Status: closed
- Attractor: `docs/architecture/attractors/abh-core-attractor.md`
- Baseline: Sprint 1 docs baseline + new `abh` CLI skeleton
- Owner: platform
- Created: 2026-05-22

## Goals

- 提供可运行的 `abh` CLI 入口。
- 支持 plan 创建、状态查询、状态流转。
- 支持 verification run 记录。
- 支持 plan 文档和本地元数据同步。
- 为后续 audit / memory / close 能力建立基础。

## Non-Goals

- 不实现 audit 命令。
- 不实现 memory 命令。
- 不实现 route / drift 分析。
- 不接入 CI。

## Exit Criteria

- `python3 -m abh --help` 可运行。
- `abh plan create` 可创建 plan 记录和文档。
- `abh plan status` 可展示当前状态。
- `abh plan transition` 可推进状态并拒绝非法状态迁移。
- `abh verify record` 可写入验证记录并关联 plan。
- `tests/test_cli.py` 可通过。

## Validation Checklist

- CLI help 可用。
- plan create 生成 `.abh/plans/*.json` 与 `docs/plans/*.md`。
- plan status 输出当前状态。
- verify record 能落盘验证结果。
- 失败或 partial 验证可将 plan 标记为 blocked。

## Closure Evidence

- `abh/cli.py`
- `abh/core.py`
- `abh/models.py`
- `abh/storage.py`
- `tests/test_cli.py`
- `.gitignore`
- `pyproject.toml`
- `docs/audits/audit-002-sprint-2-local-plan-loop.md`
- Live verification: `python3 -m abh --help`
- Live verification: `python3 -m unittest tests/test_cli.py`
- Live verification: isolated `plan create/status/transition/verify record`

## Audit Requirement

关闭前需要独立审计确认：

- CLI 命令是否达到 plan 的 exit criteria。
- 文档和本地存储是否同步。
- 状态流转是否拒绝非法迁移。

## Tasks

| ID | Task | Status | Evidence |
| --- | --- | --- | --- |
| S2-001 | CLI 技术选型 | Done | Python standard library |
| S2-002 | CLI 项目骨架 | Done | `abh/`, `pyproject.toml` |
| S2-003 | Plan 创建命令 | Done | `abh plan create` |
| S2-004 | Plan 状态流转 | Done | `abh plan transition` |
| S2-005 | 验证结果记录 | Done | `abh verify record` |

## Notes

- 当前实现是零依赖骨架，便于快速进入下一阶段。
- 如果后续需要 richer 状态和 audit 能力，可以在此基础上扩展。
