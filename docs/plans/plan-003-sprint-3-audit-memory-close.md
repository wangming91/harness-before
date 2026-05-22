# Plan: Sprint 3 Audit Memory Close

## Metadata

- ID: plan-003-sprint-3-audit-memory-close
- Status: closed
- Attractor: docs/architecture/attractors/abh-core-attractor.md
- Baseline: Sprint 2 local plan loop
- Owner: platform
- Created: 2026-05-22T16:03:50.906933+00:00
- Updated: 2026-05-22T16:04:04.842150+00:00

## Goals

- 支持 abh audit request 创建独立审计记录和文档
- 支持 abh audit record 写入审计结论、发现和后续动作
- 支持 abh close 在存在 pass audit 后关闭 plan
- 支持 abh memory add 写入外部化记忆
- 支持 abh memory search 按类型和关键词检索 memory

## Non-Goals

- 不实现远程审计协作
- 不实现全文索引服务
- 不实现 route/drift 分析
- 不接入 CI

## Exit Criteria

- abh audit request 可写入 .abh/audits/*.json 与 docs/audits/*.md
- abh audit record 可更新审计 result、findings 和 rationale
- abh close 会拒绝没有 pass audit 的 plan
- abh close 可关闭拥有 pass audit 和 closure evidence 的 plan
- abh memory add 可写入 .abh/memory/*.json 与 docs/memory/*.md
- abh memory search 可按 type 和 query 返回匹配条目
- tests/test_cli.py 可通过

## Validation Checklist

- CLI help 展示 audit、close、memory 命令
- audit request 生成本地元数据和 Markdown 文档
- partial audit 不能关闭 plan
- pass audit 可以关闭 plan
- memory add 生成本地元数据和 Markdown 文档
- memory search 可检索到目标条目

## Closure Evidence

- abh/cli.py
- abh/core.py
- abh/models.py
- abh/storage.py
- tests/test_cli.py
- docs/audits/audit-003-sprint-3-audit-memory-close.md
- Live verification: python3 -m abh --help
- Live verification: python3 -m abh audit --help
- Live verification: python3 -m abh memory --help
- Live verification: isolated audit request/record, close, memory add/search
- audit-003-sprint-3-audit-memory-close

## Verification Runs

- ver-1ca3994a77f1

## Audits

- audit-003-sprint-3-audit-memory-close
