# Attractor Before Harness 框架详细设计

## 1. 设计目标

这是一套面向 AI 大规模协作开发的轨迹收敛框架。它不把“完成”视为单次状态达标，而把开发过程看成一个不断演化的系统轨迹。

框架的目标是：

- 先显式定义系统应收敛到哪里。
- 再用计划、验证、审计和记忆去拉回轨迹。
- 让仓库成为事实来源，而不是把判断留在人的隐性经验里。

## 2. 设计原则

### 2.1 Attractor First

吸引子先于 harness。先定义长期结构，再定义控制机制。

### 2.2 Git-Native

所有关键对象都以 Markdown/YAML/JSON 进入仓库。Git 是主真相存储。

### 2.3 Evidence-First

每个结论都必须带证据。没有证据的判断只能算临时意见。

### 2.4 Independent Evaluation

实现者不能同时充当最终验收者。审计必须在独立上下文中完成。

### 2.5 Evolvable Baseline

吸引子不是静态教条。它可以演进，但演进本身必须被记录和审计。

## 3. 框架拓扑

建议把框架拆成五层：

```text
CLI / API
  -> Orchestrator
    -> Attractor Registry
    -> Plan Manager
    -> Verification Runner
    -> Audit Engine
    -> Memory Store
      -> Repo Adapter / CI / Logs / Issues
```

### 3.1 文档层

承载吸引子、计划、审计和记忆。

### 3.2 编排层

负责路由、状态流转和任务调度。

### 3.3 执行层

负责调用验证工具、测试工具、静态分析工具和审计流程。

### 3.4 持久层

负责 Git 文件、索引、缓存和历史证据存储。

### 3.5 集成层

负责对接 CI、Linter、Test Runner、Issue Tracker 和日志系统。

## 4. 权威性矩阵

不同问题需要不同权威来源：

- 问“当前行为是什么”：代码、测试、运行日志权威。
- 问“系统应该向哪里收敛”：吸引子文档权威。
- 问“这一轮怎么收口”：计划文档权威。
- 问“是否真的完成”：独立审计和外部证据权威。
- 问“为什么放弃某条路径”：记忆、缺陷和讨论记录权威。

这不是单一排序，而是按问题类型选择权威材料。

## 5. 领域模型

### 5.1 Attractor

表示长期结构基线。

字段建议：

```yaml
id: string
name: string
version: string
scope: repo | package | module
status: draft | active | superseded
owner: string
invariants: []
dependency_rules: []
boundary_rules: []
anti_patterns: []
precedence_notes: []
change_policy: string
```

### 5.2 Plan

表示一轮开发扩张的收口机制。

```yaml
id: string
title: string
attractor_ref: string
baseline_ref: string
goals: []
non_goals: []
exit_criteria: []
validation_checklist: []
closure_evidence: []
status: draft | ready | running | blocked | closing | closed
owner: string
```

### 5.3 Task

表示计划内最小可执行单元。

```yaml
id: string
plan_id: string
title: string
type: implement | refactor | test | doc | audit
status: open | in_progress | done | blocked
dependencies: []
evidence_refs: []
```

### 5.4 VerificationRun

表示一次自动化检查执行。

```yaml
id: string
plan_id: string
command: string
started_at: string
finished_at: string
result: pass | fail | partial
artifacts: []
failed_checks: []
```

### 5.5 AuditReport

表示独立审计结论。

```yaml
id: string
plan_id: string
reviewer: string
result: pass | fail | partial
findings: []
evidence_refs: []
follow_up_actions: []
timestamp: string
```

### 5.6 MemoryEntry

表示跨 session 的外部化记忆。

```yaml
id: string
type: false_assumption | rejected_path | divergent_pattern | overturned_completion
summary: string
context: string
evidence_refs: []
related_ids: []
timestamp: string
status: active | deprecated
```

### 5.7 Evidence

表示所有可引用证据。

```yaml
id: string
kind: code | doc | test | log | audit | issue | discussion
uri: string
hash: string
summary: string
```

## 6. 状态机

### 6.1 Attractor 状态

- `draft`：正在定义。
- `active`：作为当前基线。
- `superseded`：已被更高版本替代。

转移规则：

- 只有审计或架构决策可以推动吸引子升级。
- `active -> superseded` 必须保留迁移原因和差异。

### 6.2 Plan 状态

- `draft`：计划草拟中。
- `ready`：退出条件和证据要求已明确。
- `running`：正在执行。
- `blocked`：出现依赖阻塞或结构性偏离。
- `closing`：验证和审计都已通过，准备关闭。
- `closed`：已完成并沉淀记忆。

转移规则：

- 没有 baseline 和 exit criteria 的计划不能进入 `ready`。
- 任何独立审计失败都应让计划回到 `running` 或 `blocked`。
- `closed` 必须要求 closure evidence 完整。

### 6.3 Audit 状态

- `requested`
- `running`
- `need_info`
- `pass`
- `fail`

转移规则：

- 审计上下文必须是 fresh session。
- 审计不能使用实现者的主观完成声明作为唯一依据。

## 7. 核心工作流

### 7.1 启动

1. 读取当前吸引子。
2. 读取仓库 baseline。
3. 分类问题属于新需求、重构、缺陷修复还是结构升级。
4. 决定进入哪个 plan 或新建 plan。

### 7.2 计划生成

1. 绑定 attractor。
2. 写清 goals / non-goals。
3. 写清 exit criteria。
4. 写清 validation checklist。
5. 写清 closure evidence。

### 7.3 生成与实现

1. AI 根据 plan 产出代码、文档和测试。
2. 变更必须尽量局部化。
3. 每次提交都要附带可以验证的证据。

### 7.4 自动验证

1. 执行 lint / typecheck / build / test / contract check。
2. 结果归一化为统一格式。
3. 若失败，记录失败类型和对应证据。

### 7.5 独立审计

1. 使用 fresh session 重新读取 repo。
2. 按吸引子和计划检查证据链。
3. 判断是否是假完成、局部正确或真正收敛。
4. 输出明确结论和 follow-up。

### 7.6 关闭与沉淀

1. 只有审计通过才允许关闭。
2. 把反例、推翻结论和失败路径写入 memory。
3. 如果审计反复指出同一结构问题，触发吸引子更新流程。

## 8. 模块设计

### 8.1 Router

职责：

- 识别问题类型。
- 选择对应吸引子和 plan。
- 决定先读哪些文档。

输入：

- 用户请求
- 当前 repo 状态
- 最近计划和审计历史

输出：

- 路由决策
- 推荐阅读顺序
- 是否需要新 plan

### 8.2 Attractor Registry

职责：

- 创建、读取、更新吸引子。
- 维护版本差异。
- 标记适用范围和 precedence。

关键能力：

- 吸引子 diff
- 变更原因
- 兼容性说明

### 8.3 Plan Manager

职责：

- 生成和维护计划。
- 管理任务拆分。
- 跟踪收口条件。

关键能力：

- baseline 绑定
- exit criteria 校验
- closure evidence 管控

### 8.4 Verification Runner

职责：

- 封装自动化检查命令。
- 汇总输出。
- 标记失败与漂移信号。

关键能力：

- 本地执行
- CI 对接
- 结果规范化
- 失败分类

### 8.5 Audit Engine

职责：

- 独立判定完成性。
- 检查计划是否真的达到收口条件。
- 判断是否需要回滚、继续扩张或更新吸引子。

关键能力：

- fresh session 读取
- 证据交叉核对
- 假完成识别
- 审计结论生成

### 8.6 Memory Store

职责：

- 保存历史轨迹知识。
- 支持检索和引用。
- 避免重复犯错。

推荐内容：

- 被证伪的前提
- 明确失败的结构路径
- 曾被推翻的完成判断
- 术语误用记录

### 8.7 Orchestrator

职责：

- 串联 Router、Plan、Verification、Audit 和 Memory。
- 管理状态转移。
- 控制每一步的 gate。

它是框架的过程引擎。

## 9. 仓库布局建议

建议采用 Git-native 目录结构：

```text
docs/
  architecture/
    README.md
    attractors/
    policies/
  plans/
  audits/
  memory/
    false_assumption/
    rejected_path/
    overturned_completion/
.abh/
  index/
  cache/
  sessions/
```

说明：

- `docs/architecture/`：吸引子主承载区。
- `docs/plans/`：计划和收口文档。
- `docs/audits/`：独立审计记录。
- `docs/memory/`：外部化记忆。
- `.abh/`：派生索引和临时会话数据。

## 10. 接口建议

### 10.1 CLI

建议最少提供这些命令：

- `abh init`
- `abh attractor create`
- `abh attractor diff`
- `abh plan create`
- `abh plan update`
- `abh verify run`
- `abh audit request`
- `abh close`
- `abh memory add`
- `abh memory search`

### 10.2 机器接口

如果后续拆成服务，可以暴露：

- `POST /attractors`
- `GET /attractors/:id`
- `POST /plans`
- `POST /verifications`
- `POST /audits`
- `POST /memory`

### 10.3 文档模板

#### Attractor 模板

```md
# Attractor: <name>

## Intent
## Invariants
## Boundary Rules
## Dependency Rules
## Anti-Patterns
## Precedence
## Change Policy
```

#### Plan 模板

```md
# Plan: <title>

## Baseline
## Goals
## Non-Goals
## Exit Criteria
## Validation Checklist
## Closure Evidence
## Audit Requirement
```

#### Audit 模板

```md
# Audit: <plan-id>

## Scope
## Evidence Reviewed
## Findings
## Verdict
## Follow-ups
```

## 11. 漂移检测

框架需要显式识别几类漂移：

- 边界漂移：职责边界被侵蚀。
- 依赖漂移：依赖方向反转或变得含混。
- 测试漂移：测试开始服务旧实现而非当前结构。
- 术语漂移：同一术语在不同 session 里含义变了。
- 完成幻觉：实现者自认为完成，但证据链不足。
- 局部自洽漂移：局部看都对，整体方向错了。

漂移检测输出应包括：

- 漂移类型
- 严重度
- 证据引用
- 建议动作

## 12. 失败模式与恢复策略

### 12.1 没有吸引子

表现：

- 计划无法定义收口方向。

策略：

- 阻止进入 `ready`。
- 先补吸引子文档。

### 12.2 只有验证，没有审计

表现：

- 机器检查通过，但结构仍漂移。

策略：

- 强制 fresh session 审计。
- 以审计结论作为关闭门槛。

### 12.3 只有完成感，没有证据

表现：

- 实现者宣称完成，但无法证明满足 exit criteria。

策略：

- 关闭被阻断。
- 补充 closure evidence。

### 12.4 吸引子过细

表现：

- 系统被写死，失去演进空间。

策略：

- 只保留高阶不变量。
- 把局部策略放进 plan，而不是 attractor。

## 13. 非功能要求

- 可追溯：任何结论都能回到证据。
- 可版本化：吸引子、计划、审计和记忆都能 diff。
- 可移植：不依赖特定语言生态。
- 可审计：每个关闭动作都可复核。
- 可扩展：能接 CI、issue、日志和多仓库。

## 14. 指标体系

建议跟踪这些指标：

- 计划关闭前平均验证轮数
- 审计驳回率
- 重复漂移率
- 吸引子更新频率
- 关闭后回滚率
- memory 命中率

这些指标能反映轨迹是否真的在收敛。

## 15. 实施路线

### Phase 1：文档化基线

- 定义吸引子模板。
- 定义计划模板。
- 定义审计模板。
- 定义 memory 记录模板。

### Phase 2：CLI + 本地执行

- 实现 plan / verify / audit 的本地流程。
- 打通 Git-native 存储。

### Phase 3：独立审计与记忆检索

- 引入 fresh session 审计。
- 建立 memory 搜索和引用。

### Phase 4：漂移分析

- 加入结构差异分析。
- 自动识别高频偏离模式。

### Phase 5：多仓库与团队协作

- 支持多 repo 共享吸引子。
- 支持团队级 ownership 和 precedence。

## 16. 通过标准

一个最小可用版本至少满足：

- 每个计划都绑定一个吸引子。
- 每个计划都有明确 exit criteria。
- 每次关闭都需要独立审计。
- 每次审计都带证据。
- 每次推翻结论都能写入 memory。

## 17. 结语

这个框架的重点不是把 harness 做得更重，而是把“系统该向哪里收敛”变成可工程化、可版本化、可审计的第一类对象。

先有吸引子，后有 harness。先有方向，后有纠偏。
