# Attractor Before Harness 开发排期

## 1. 排期目标

根据现有 PRD、详细设计和任务拆解，将项目推进为可执行开发计划。本文档作为当前阶段的主排期基线。

## 2. 排期假设

- 采用两周一个 Sprint。
- 先以 Git-native 文档框架和 CLI 最小闭环为目标。
- 初期不建设 Web UI。
- 初期不依赖外部数据库。
- 所有关键对象先落在仓库文件中。

## 3. 版本目标

### v0.1：文档与模型基线

周期：Sprint 1

目标：

- 建立正式目录结构。
- 建立 Attractor、Plan、Audit、Memory 模板。
- 建立第一个项目吸引子。
- 建立第一份启动计划。
- 固定验收规则和状态流转。

### v0.2：本地计划闭环

周期：Sprint 2

目标：

- 实现计划创建和状态流转。
- 实现本地验证结果记录。
- 支持计划绑定吸引子。
- 支持 closure evidence 收集。

### v0.3：独立审计与记忆

周期：Sprint 3

目标：

- 实现审计记录流程。
- 实现 memory 记录和检索。
- 强制关闭前审计。
- 支持假完成和证据不足记录。

### v0.4：路由与漂移分析

周期：Sprint 4

目标：

- 实现问题路由建议。
- 实现基础漂移分类。
- 把漂移发现反向写入计划和 memory。

### v0.5：运行说明与自举稳定

周期：Sprint 5-7

目标：

- 明确 Python、pip、uvx 和 uv tool install 的运行路径。
- 将历史手写计划迁移到 abh CLI 双写数据。
- 新增 plan / memory / audit list 查询能力。
- 增强 route 和 drift，使其能利用当前计划状态和计划 non-goals。
- 通过 dogfooding 记录文档同步、独立审计和安装门槛相关 memory。

### v0.6：路线同步与一致性检查

周期：Sprint 8

目标：

- 将 roadmap 和 task-board 同步到当前实际进度。
- 新增 `abh doctor`，检查 `.abh/` JSON 与 `docs/` Markdown 是否一致。
- 将文档/运行态一致性纳入 plan 关闭前验证。
- 为 doctor 命令补充测试覆盖。

## 4. Sprint 1 计划

### Sprint 1 目标

完成项目的工程化承载结构，让后续所有开发任务都能被 plan、audit 和 memory 承接。

### Sprint 1 范围

- `docs/architecture/` 目录
- `docs/plans/` 目录
- `docs/audits/` 目录
- `docs/memory/` 目录
- Attractor 模板
- Plan 模板
- Audit 模板
- Memory 模板
- 当前项目初始吸引子
- Sprint 1 启动计划

### Sprint 1 不做

- 不实现 CLI。
- 不实现自动化验证执行器。
- 不接 CI。
- 不做 Web UI。

### Sprint 1 验收标准

- 所有标准目录存在。
- 所有模板可直接复制使用。
- 至少存在一个 active attractor。
- 至少存在一个 active plan。
- plan 明确 goals、non-goals、exit criteria 和 closure evidence。
- audit 模板可以用于独立审计。
- memory 模板可以记录被证伪前提和发散路径。

## 5. Sprint 2 计划

### Sprint 2 目标

实现本地最小计划闭环。

### Sprint 2 范围

- CLI 项目骨架。
- `abh plan create`
- `abh plan status`
- `abh plan transition`
- `abh verify record`
- 计划状态机校验。

### Sprint 2 验收标准

- 计划创建必须绑定吸引子。
- 无 exit criteria 的计划不能进入 ready。
- 验证结果可以写入计划 evidence。
- blocked / closing / closed 状态转移可被记录。

## 6. Sprint 3 计划

### Sprint 3 目标

实现独立审计和外部化记忆。

### Sprint 3 范围

- `abh audit request`
- `abh audit record`
- `abh close`
- `abh memory add`
- `abh memory search`

### Sprint 3 验收标准

- 无审计报告不能关闭计划。
- 审计报告必须引用 evidence。
- memory 条目可按类型和关键词检索。
- 被推翻的完成判断能被记录。

## 7. Sprint 4 计划

### Sprint 4 目标

实现路由和基础漂移分析。

### Sprint 4 范围

- `abh route`
- `abh drift analyze`
- 漂移分类规则
- 漂移报告模板

### Sprint 4 验收标准

- 能输出建议阅读顺序。
- 能识别边界漂移、依赖漂移、测试漂移、术语漂移。
- 漂移结果可引用 evidence。
- 漂移发现可转成 plan follow-up 或 memory。

## 8. 当前执行焦点

当前进入 Sprint 8。

本轮只追求一个结果：恢复路线图权威性，并把 `.abh/` 与 `docs/` 的一致性检查变成可执行命令。

## 9. 后续长期路线

### Phase A：内核治理

- 扩展 `abh doctor`，逐步检查 schema version、doc_path、closure evidence 和 audit evidence。
- 建立 CI，让 `python3 -m unittest tests/test_cli.py -v` 与 `python3 -m abh doctor` 成为默认门禁。
- 清理 demo 或过期 draft 计划，降低状态噪音。

### Phase B：验证执行器

- 将 `verify record` 扩展为 `verify run`。
- 保存退出码、运行耗时、stdout/stderr 摘要和 artifact。
- 失败时自动生成 blocked 证据。

### Phase C：Attractor Registry

- 新增 `abh attractor list/show/create/supersede`。
- 让 plan ready gate 校验 active attractor。
- 支持吸引子版本升级、差异说明和迁移策略。

### Phase D：独立审计协议

- 新增 audit prompt/bundle 能力。
- 标记审计来源和独立上下文。
- 关闭 plan 时优先要求独立审计证据。

### Phase E：团队与集成

- 支持 `abh init` 初始化任意仓库。
- 增加 JSON 输出模式以便 agent/MCP/CI 消费。
- 提供 GitHub Actions 和 Git hook 示例。

## 10. 风险控制

- 如果模板过重，会降低使用率。模板必须短而硬。
- 如果没有初始 attractor，后续 plan 无法收口。
- 如果 Sprint 1 范围扩张到 CLI，会影响基础结构稳定。
- 如果 memory 只记录成功结论，会丢失真正有价值的失败轨迹。
- 如果 roadmap、task-board、README 与 `.abh/` 状态不同步，仓库事实来源会再次分裂。
