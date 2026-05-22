# Plan: Sprint 5 Runtime Docs Install

## Metadata

- ID: plan-005-runtime-docs-install
- Status: closed
- Attractor: `docs/architecture/attractors/abh-core-attractor.md`
- Baseline: Sprint 4 route and drift loop
- Owner: platform
- Created: 2026-05-22

## Goals

- 明确 Python 3.13+ 是运行前提。
- 明确推荐运行方式是仓库根目录 editable install。
- 明确临时目录或外部目录运行时需要安装包或设置 `PYTHONPATH`。
- 修正 README 中与当前 CLI 不匹配的示例。
- 给出最小验证命令。

## Non-Goals

- 不发布到 PyPI。
- 不新增依赖管理工具。
- 不改 CLI 行为。
- 不实现 Sprint 5 范围以外的新能力。

## Exit Criteria

- README 明确 Python 3.13+ 要求。
- README 明确 `python3 --version` 检查方式。
- README 明确 `python3 -m pip install -e .` 安装方式。
- README 明确仓库根目录运行与外部目录运行差异。
- README 明确 `PYTHONPATH=/path/to/repo python3 -m abh ...` 兜底方式。
- README 中 `audit record --finding` 示例符合 `Severity|Finding|Evidence|Recommendation` 格式。
- README 包含 `python3 -m pytest tests/test_cli.py` 或等价测试命令。

## Validation Checklist

- `README.md` 包含 Python 3.13+。
- `README.md` 包含 editable install。
- `README.md` 包含 `PYTHONPATH`。
- `README.md` 示例命令与 CLI 参数一致。
- `tests/test_cli.py` 可通过。

## Closure Evidence

- `README.md`
- `docs/plans/plan-005-runtime-docs-install.md`
- `docs/audits/audit-005-runtime-docs-install.md`
- Live verification: `python3 -m unittest tests/test_cli.py`
- Live verification: `python3 -m abh --help`
- Independent review: `docs/audits/audit-005-runtime-docs-install.md`

## Audit Requirement

关闭前需要独立审计确认：

- README 是否覆盖运行环境和安装方式。
- README 示例是否与当前 CLI 一致。
- 测试是否通过。

## Tasks

| ID | Task | Status | Evidence |
| --- | --- | --- | --- |
| S5-001 | Runtime 要求说明 | Done | `README.md` |
| S5-002 | Editable install 说明 | Done | `README.md` |
| S5-003 | PYTHONPATH 兜底说明 | Done | `README.md` |
| S5-004 | CLI 示例修正 | Done | `README.md` |
| S5-005 | Sprint 5 审计占位 | Done | `docs/audits/audit-005-runtime-docs-install.md` |

## Notes

- 本计划只修文档，不改变 CLI 行为。
- 本计划已通过独立会话审计并关闭。
