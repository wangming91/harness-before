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

当前进入 Sprint 4。

本轮只追求一个结果：把路由建议和基础漂移分析闭环做出来。

## 9. 风险控制

- 如果模板过重，会降低使用率。模板必须短而硬。
- 如果没有初始 attractor，后续 plan 无法收口。
- 如果 Sprint 1 范围扩张到 CLI，会影响基础结构稳定。
- 如果 memory 只记录成功结论，会丢失真正有价值的失败轨迹。
