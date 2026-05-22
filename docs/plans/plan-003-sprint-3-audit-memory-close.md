# Plan: Sprint 3 Audit Memory Close

## Metadata

- ID: plan-003-sprint-3-audit-memory-close
- Status: closed
- Attractor: `docs/architecture/attractors/abh-core-attractor.md`
- Baseline: Sprint 2 local plan loop
- Owner: platform
- Created: 2026-05-22

## Goals

- 支持 `abh audit request` 创建独立审计记录和文档。
- 支持 `abh audit record` 写入审计结论、发现和后续动作。
- 支持 `abh close` 在存在 pass audit 后关闭 plan。
- 支持 `abh memory add` 写入外部化记忆。
- 支持 `abh memory search` 按类型和关键词检索 memory。

## Non-Goals

- 不实现远程审计协作。
- 不实现全文索引服务。
- 不实现 route / drift 分析。
- 不接入 CI。

## Exit Criteria

- `abh audit request` 可写入 `.abh/audits/*.json` 与 `docs/audits/*.md`。
- `abh audit record` 可更新审计 result、findings 和 rationale。
- `abh close` 会拒绝没有 pass audit 的 plan。
- `abh close` 可关闭拥有 pass audit 和 closure evidence 的 plan。
- `abh memory add` 可写入 `.abh/memory/*.json` 与 `docs/memory/*.md`。
- `abh memory search` 可按 type 和 query 返回匹配条目。
- `tests/test_cli.py` 可通过。

## Validation Checklist

- CLI help 展示 `audit`、`close`、`memory` 命令。
- audit request 生成本地元数据和 Markdown 文档。
- partial audit 不能关闭 plan。
- pass audit 可以关闭 plan。
- memory add 生成本地元数据和 Markdown 文档。
- memory search 可检索到目标条目。

## Closure Evidence

- `abh/cli.py`
- `abh/core.py`
- `abh/models.py`
- `abh/storage.py`
- `tests/test_cli.py`
- `docs/audits/audit-003-sprint-3-audit-memory-close.md`
- Live verification: `python3 -m abh --help`
- Live verification: `python3 -m abh audit --help`
- Live verification: `python3 -m abh memory --help`
- Live verification: isolated `audit request/record`, `close`, `memory add/search`

## Audit Requirement

关闭前需要独立审计确认：

- audit 命令是否达到 plan 的 exit criteria。
- close 是否强制 pass audit gate。
- memory 是否使用 canonical taxonomy 并能检索。

## Tasks

| ID | Task | Status | Evidence |
| --- | --- | --- | --- |
| S3-001 | Audit 请求命令 | Done | `abh audit request` |
| S3-002 | Audit 记录命令 | Done | `abh audit record` |
| S3-003 | Plan 关闭命令 | Done | `abh close` |
| S3-004 | Memory 添加命令 | Done | `abh memory add` |
| S3-005 | Memory 检索命令 | Done | `abh memory search` |

## Notes

- close 只接受 pass audit，不接受 partial 或 need_info。
- memory 类型沿用 `docs/memory/README.md` 的 canonical taxonomy。
