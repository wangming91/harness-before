# Attractor Before Harness 开发排期

## 1. 文档定位

本文档是项目的主排期基线，负责同时承载两条线：

- 历史执行线：记录 Sprint 1-8 已经交付的版本和计划。
- 长期阶段线：按照 `docs/阶段规划.md` 的六阶段路线，规划后续 12 个月演进。

当两条线发生冲突时，已关闭 plan 和 audit 是历史事实来源；长期阶段线是未来排期来源。新的 plan 应优先从长期阶段线中切出最小可关闭范围。

## 1.1 术语说明

- Sprint：时间盒或阶段性工作批次，用于描述项目推进节奏。
- Plan：ABH 中可验证、可审计、可关闭的最小工作单元。
- Sprint 编号和 plan 编号不要求一一对应。一个 Sprint 可以包含多个 plan，例如 Sprint 7 同时包含 `plan-007-sprint-7-dogfood` 和 `plan-007-zero-dep-install`；一个长期阶段也可以跨多个 Sprint 和 plan。
- 从 Sprint 12 开始，建议 plan ID 按全局递增编号命名，避免把 Sprint 编号误认为 plan 编号。

## 2. 排期假设

- 采用两周一个 Sprint。
- 初期继续保持 Git-native、本地优先、零外部数据库。
- 不急于建设 Web UI，先让 CLI 和 Agent 协议稳定。
- 所有关键对象先落在仓库文件中，并通过 `abh doctor` 防止 `.abh/` 与 `docs/` 分裂。
- 每个阶段都必须能被 plan、verification、audit 和 memory 闭环承接。

## 3. 历史执行线

本节记录已经完成并审计关闭的历史事实。若本节与当前计划状态不一致，以 `.abh/` 中已关闭 plan 和对应 audit 为准。

### v0.1：文档与模型基线

周期：Sprint 1

目标：

- 建立正式目录结构。
- 建立 Attractor、Plan、Audit、Memory 模板。
- 建立第一个项目吸引子。
- 建立第一份启动计划。
- 固定验收规则和状态流转。

状态：已完成，对应 `plan-001-sprint-1-foundation`。

### v0.2：本地计划闭环

周期：Sprint 2

目标：

- 实现计划创建和状态流转。
- 实现本地验证结果记录。
- 支持计划绑定吸引子。
- 支持 closure evidence 收集。

状态：已完成，对应 `plan-002-sprint-2-local-plan-loop`。

### v0.3：独立审计与记忆

周期：Sprint 3

目标：

- 实现审计记录流程。
- 实现 memory 记录和检索。
- 强制关闭前审计。
- 支持假完成和证据不足记录。

状态：已完成，对应 `plan-003-sprint-3-audit-memory-close`。

### v0.4：路由与漂移分析

周期：Sprint 4

目标：

- 实现问题路由建议。
- 实现基础漂移分类。
- 把漂移发现反向写入计划和 memory。

状态：已完成，对应 `plan-004-sprint-4-route-drift`。

### v0.5：运行说明与自举稳定

周期：Sprint 5-7

目标：

- 明确 Python、pip、uvx 和 uv tool install 的运行路径。
- 将历史手写计划迁移到 abh CLI 双写数据。
- 新增 plan / memory / audit list 查询能力。
- 增强 route 和 drift，使其能利用当前计划状态和计划 non-goals。
- 通过 dogfooding 记录文档同步、独立审计和安装门槛相关 memory。

状态：已完成，对应 `plan-005-runtime-docs-install`、`plan-006-stabilize`、`plan-007-sprint-7-dogfood`、`plan-007-zero-dep-install`。

### v0.6：路线同步与一致性检查

周期：Sprint 8

目标：

- 将 roadmap 和 task-board 同步到当前实际进度。
- 新增 `abh doctor`，检查 `.abh/` JSON 与 `docs/` Markdown 是否一致。
- 将文档/运行态一致性纳入 plan 关闭前验证。
- 为 doctor 命令补充测试覆盖。

状态：已完成，对应 `plan-008-roadmap-sync-and-doctor`。

### v0.7：长期阶段路线对齐

周期：Sprint 9

目标：

- 将本路线图改为“历史执行线 + 长期阶段线”的双层结构。
- 严格承接 `docs/阶段规划.md` 的阶段 1-6 长期路线。
- 明确 Sprint 1-8 与长期阶段的映射关系。
- 列出下一批推荐计划，作为后续 plan 切分入口。

状态：已完成，对应 `plan-009-roadmap-phase-alignment`。

### v0.8：内核治理硬化

周期：Sprint 10

目标：

- 清理 `plan-200-demo` 遗留 draft 状态噪音。
- 为核心 JSON 对象加入 `schema_version`。
- 建立 CI 基础门禁。
- 明确包版本和 README 功能版本之间的关系。
- 把关闭后文档同步检查纳入治理门禁。

状态：已完成，对应 `plan-010-core-governance-hardening`。

### v0.9：阶段 1 治理收尾

周期：Sprint 11

目标：

- 迁移历史 `.abh` JSON 对象补齐 `schema_version`。
- 增强 `abh doctor`，检查缺失 `schema_version` 的核心 JSON 对象。
- 在 CI 中补齐 editable install 路径。
- 标记阶段 1 完成，并把下一轮路线推进到阶段 2。

状态：已完成，对应 `plan-011-stage-1-finalization`。

## 4. 当前执行焦点

当前准备进入 Sprint 12。

阶段 1 已完成，下一轮建议进入阶段 2，只追求一个结果：把验证从人工记录升级为本地执行器，让 plan 的 validation checklist 能被 `abh` 直接运行和记录。

建议计划：`plan-012-verify-runner`。

## 5. 长期阶段线

### 阶段 1：恢复权威基线，稳住内核

周期：1 个月

目标：让项目自身不再漂移。

核心事项：

- 更新 `docs/development-roadmap.md` 和 `docs/task-board.md`，把 Sprint 6/7、零门槛安装和 Sprint 8 纳入正式路线。
- 建立 `abh doctor`，检查 `.abh/*.json` 与 `docs/*.md` 是否一致。
- 清理或关闭遗留 draft 计划，尤其是 `plan-200-demo`，降低状态噪音。
- 给数据对象加 schema/version 字段，为后续迁移做准备。
- 建立 CI：运行 `python3 -m unittest tests/test_cli.py -v`，并验证 `python3 -m abh --help`、`python3 -m abh plan list`、`python3 -m abh doctor`。
- 把版本号从当前 `0.1.0` 进入可解释的发布节奏，避免 README 功能与包版本脱节。

当前状态：

- 已完成：Sprint 6/7/8 纳入路线、`abh doctor` 第一版、路线图和看板同步、清理 `plan-200-demo`、新对象 schema version、历史 JSON schema 迁移、CI 基础门禁、editable install CI 路径、版本策略说明。
- 阶段 1 判定：完成。阶段 1 的必需治理门禁已经具备，可以进入阶段 2。
- 延期项：更深的内容级 doctor 校验和正式发布自动化，推迟到后续质量/发布计划，不阻塞阶段 2 启动。

建议后续计划：

- `plan-012-verify-runner`：把验证从人工记录升级为本地执行器。

### 阶段 2：从“记录验证”升级到“执行验证”

周期：1-3 个月

目标：让 `verify` 从人工记录结果升级为本地验证执行器。

核心事项：

- 新增 `abh verify run <plan>`，按 plan 的 validation checklist 执行命令。
- 保存 stdout/stderr 摘要、退出码、耗时和 artifact。
- 失败时自动把 plan 转入 `blocked`，并生成可审计证据。
- 支持 `abh plan update`，补充 goals、non-goals、exit criteria、validation checklist 和 closure evidence。
- 在不破坏现有 CLI 的前提下，逐步拆分 `core.py` 为更小的领域模块，例如 `plans.py`、`audits.py`、`memory.py`、`drift.py`、`routing.py`。

建议版本：v0.7。

建议后续计划：

- `plan-011-verify-runner`
- `plan-012-plan-update`
- `plan-013-core-module-split`

### 阶段 3：补齐 Attractor Registry

周期：3-4 个月

目标：把吸引子从文档约定升级为 CLI 可管理的一等对象。

核心事项：

- 新增 `abh attractor list/show/create/supersede`。
- plan 进入 `ready` 前校验引用的是 active attractor。
- 记录吸引子版本差异、升级原因、影响范围和迁移策略。
- route/drift 优先读取 active attractor，而不是只靠固定路径和关键词。

建议版本：v0.8。

建议后续计划：

- `plan-014-attractor-registry`
- `plan-015-attractor-aware-route-drift`

### 阶段 4：真正独立审计

周期：4-6 个月

目标：让“独立审计”从流程原则升级为工具支持。

核心事项：

- 新增 `abh audit prompt <plan>`，生成独立审计提示词。
- 新增 `abh audit bundle <plan>`，打包审计所需证据清单。
- `abh audit record` 增加 auditor context/source 字段。
- 关闭计划时检查是否有 fresh/independent 标记的通过审计。
- 固化审计模板，避免每次靠人工记忆。

建议版本：v0.9。

建议后续计划：

- `plan-016-audit-prompt-bundle`
- `plan-017-independent-audit-gate`

### 阶段 5：漂移与记忆质量提升

周期：6-9 个月

目标：降低 drift 误报/漏报，让 memory 从列表检索升级为可复用轨迹知识。

核心事项：

- drift finding 增加 severity、matched span、source excerpt 和 confidence。
- memory 支持标签、状态废弃、related plan/audit 反向索引。
- route 从关键词匹配升级为“对象图 + 简单权重排序”。
- 新增 `abh report`，展示计划关闭率、审计驳回率、重复漂移率和 memory 命中情况。

建议版本：v0.10。

建议后续计划：

- `plan-018-drift-quality`
- `plan-019-memory-index`
- `plan-020-reporting`

### 阶段 6：团队可用与生态集成

周期：9-12 个月

目标：让 ABH 成为任何仓库都能接入的本地优先治理层。

核心事项：

- 新增 `abh init`，一键初始化任意仓库。
- 提供 GitHub Actions 模板：PR 中自动跑 `abh doctor`、测试和漂移检查。
- 提供 Git hooks 可选集成：关闭 plan 前检查审计和证据链。
- 支持多仓库共享 attractor/memory 的导入导出。
- 增加 Agent/MCP 友好的 JSON 输出模式，例如 `--json`。
- 发布到 PyPI，同时保留 `uvx --from git+...` 路径。

建议版本：v1.0。

建议后续计划：

- `plan-021-init-and-ci-templates`
- `plan-022-json-output`
- `plan-023-multi-repo-sharing`
- `plan-024-pypi-release`

## 6. 历史执行线与长期阶段映射

| 长期阶段 | 已完成历史计划 | 已完成内容 | 剩余内容 |
| --- | --- | --- | --- |
| 阶段 1：恢复权威基线，稳住内核 | `plan-006-stabilize`, `plan-007-zero-dep-install`, `plan-008-roadmap-sync-and-doctor`, `plan-009-roadmap-phase-alignment`, `plan-010-core-governance-hardening`, `plan-011-stage-1-finalization` | 历史计划迁移、安装门槛降低、`abh doctor`、路线图对齐、demo 清理、schema version、历史 schema 迁移、CI、版本策略 | 已完成；内容级 doctor、发布自动化转入后续质量/发布计划 |
| 阶段 2：验证执行器 | `plan-002-sprint-2-local-plan-loop` | `verify record` 可记录验证结果 | `verify run`、失败自动证据、plan update、模块拆分 |
| 阶段 3：Attractor Registry | `plan-001-sprint-1-foundation` | active attractor 文档和模板 | attractor CLI、版本迁移、active 校验 |
| 阶段 4：真正独立审计 | `plan-003-sprint-3-audit-memory-close`, `plan-007-zero-dep-install`, `plan-008-roadmap-sync-and-doctor` | audit request/record/close 闭环，人工独立审计流程已 dogfood | audit prompt/bundle、独立上下文字段、关闭门禁 |
| 阶段 5：漂移与记忆质量提升 | `plan-004-sprint-4-route-drift`, `plan-007-sprint-7-dogfood` | 关键词 drift、route 注入活跃计划和记忆 | severity/confidence、memory 索引、对象图路由、report |
| 阶段 6：团队可用与生态集成 | `plan-007-zero-dep-install` | uvx/uv tool install 降低接入门槛 | init、CI 模板、Git hooks、JSON 输出、多仓库、PyPI |

## 7. 下一批推荐计划

### plan-010-core-governance-hardening

范围：

- 关闭或废弃 `plan-200-demo`。
- 为核心 JSON 对象加入 schema/version。
- 建立 CI 配置，运行 unittest、`abh doctor` 和基础 smoke test。
- 明确包版本和 README 功能版本之间的关系。

不做：

- 不实现 `verify run`。
- 不重构核心模块。

### plan-011-verify-runner

范围：

- 实现 `abh verify run <plan>`。
- 执行 validation checklist 中的命令。
- 保存退出码、耗时、输出摘要和 artifact。
- 失败时自动阻断计划。

不做：

- 不实现 CI 服务端。
- 不改变 audit 关闭规则。

### plan-012-plan-update

范围：

- 支持更新 plan 的 goals、non-goals、exit criteria、validation checklist 和 closure evidence。
- 确保更新后 JSON 与 Markdown 双写一致。

不做：

- 不引入交互式编辑器。

## 8. 风险控制

- 如果 roadmap、task-board、README 与 `.abh/` 状态不同步，仓库事实来源会再次分裂。
- 如果模板过重，会降低使用率。模板必须短而硬。
- 如果没有 active attractor 校验，后续 plan 仍可能绕过吸引子。
- 如果 memory 只记录成功结论，会丢失真正有价值的失败轨迹。
- 如果过早做 Web UI，会削弱 CLI 和 Agent 协议这条最关键路径。
