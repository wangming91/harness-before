# Attractor Before Harness 开发任务拆解

## 1. 拆解目标

将框架从文档推进到可交付的最小可用版本，并直接支持迭代排期。

## 2. 迭代原则

- 先文档与模型，后执行与自动化。
- 先最小闭环，后扩展能力。
- 每个迭代都必须产出可验证交付物。

## 3. 里程碑规划

### Milestone 1：定义最小闭环

目标：让吸引子、计划、验证、审计、记忆具备统一数据结构和文档模板。

交付物：

- 吸引子模板
- 计划模板
- 审计模板
- memory 模板
- 仓库目录规范

### Milestone 2：本地可执行流程

目标：可以在本地完成计划创建、验证执行、审计记录和记忆沉淀。

交付物：

- CLI 雏形
- 计划状态机
- 验证结果记录
- 审计结果记录

### Milestone 3：独立审计与漂移识别

目标：完成 fresh session 审计和基础漂移分析。

交付物：

- 独立审计流程
- 证据链检查
- 假完成识别
- 漂移分类器

### Milestone 4：团队可用

目标：支持多人协作和多仓库扩展。

交付物：

- 吸引子版本管理
- 共享 memory 索引
- 多 repo 路由

## 4. 迭代拆解

### Iteration 1：项目骨架与文档规范

任务：

1. 建立 `docs/architecture/`、`docs/plans/`、`docs/audits/`、`docs/memory/` 目录。
2. 定义 Attractor 模板。
3. 定义 Plan 模板。
4. 定义 Audit 模板。
5. 定义 Memory 模板。

验收：

- 仓库中存在统一目录结构。
- 模板字段已固定。
- 目录用途清晰可读。

依赖：

- 无。

### Iteration 2：领域模型与状态机

任务：

1. 定义 Attractor 数据模型。
2. 定义 Plan 数据模型。
3. 定义 Task、VerificationRun、AuditReport、MemoryEntry。
4. 定义状态机与状态转移规则。
5. 定义权威性矩阵。

验收：

- 所有核心对象都有字段定义。
- 状态转移规则已写清。
- 权威性矩阵可用于路由决策。

依赖：

- Iteration 1。

### Iteration 3：计划管理闭环

任务：

1. 支持创建计划。
2. 支持绑定吸引子。
3. 支持设置 baseline、goals、non-goals。
4. 支持设置 exit criteria 和 closure evidence。
5. 支持计划状态流转。

验收：

- 没有吸引子的计划不能进入 ready。
- 计划能进入 running、blocked、closing、closed。
- 每个计划可追溯到对应吸引子。

依赖：

- Iteration 2。

### Iteration 4：验证执行器

任务：

1. 封装 lint、typecheck、build、test 的执行结果。
2. 统一结果格式。
3. 记录失败项与产物。
4. 支持基于计划的验证清单。

验收：

- 验证结果可被统一读取。
- 失败项可定位到具体检查。
- 验证结果能挂接到 plan。

依赖：

- Iteration 3。

### Iteration 5：独立审计流程

任务：

1. 实现 fresh session 审计入口。
2. 支持基于仓库证据重新判定完成性。
3. 输出 pass / fail / partial。
4. 支持 need_info 反馈。

验收：

- 审计上下文与实现上下文分离。
- 审计结果必须引用证据。
- 无证据不能关闭计划。

依赖：

- Iteration 4。

### Iteration 6：Memory Store

任务：

1. 支持记录 false assumption。
2. 支持记录 rejected path。
3. 支持记录 overturned completion。
4. 支持按关键字和类型检索。

验收：

- memory 条目可持久化。
- memory 可检索。
- 历史经验可在后续计划中引用。

依赖：

- Iteration 5。

### Iteration 7：路由与导航

任务：

1. 根据问题类型推荐读取顺序。
2. 区分 baseline、plan、audit、history。
3. 提供新任务入口判断。

验收：

- 能将不同问题路由到正确对象。
- 能输出建议阅读路径。

依赖：

- Iteration 2、3、6。

### Iteration 8：漂移分析

任务：

1. 定义边界漂移、依赖漂移、测试漂移、术语漂移。
2. 输出漂移分类和严重度。
3. 提供修复建议。

验收：

- 能识别至少四类漂移。
- 漂移报告能引用证据。
- 漂移结果能反向影响 plan。

依赖：

- Iteration 5、6。

## 5. 建议排期

### Sprint 1

- Iteration 1
- Iteration 2

产出：

- 完整文档骨架
- 核心领域模型
- 状态机

### Sprint 2

- Iteration 3
- Iteration 4

产出：

- 可创建计划
- 可执行验证
- 可记录结果

### Sprint 3

- Iteration 5
- Iteration 6

产出：

- 独立审计
- 外部化记忆
- 历史经验沉淀

### Sprint 4

- Iteration 7
- Iteration 8

产出：

- 路由与导航
- 漂移分析
- 计划回收机制

## 6. 角色分工

### 架构负责人

- 定义吸引子。
- 审批吸引子升级。

### 平台开发者

- 实现文档模板、状态机和 CLI。
- 对接验证与审计流程。

### 审计人员

- 负责独立验收。
- 输出 audit report。

### 维护人员

- 负责 memory 记录和检索。
- 负责沉淀失败经验。

## 7. Definition of Done

一个迭代完成，必须同时满足：

- 任务有明确产出。
- 任务产出可在仓库中定位。
- 任务状态可追踪。
- 验证或审计至少覆盖一个关键路径。
- 失败经验进入 memory 或被显式解释。

## 8. 风险项

- 只做文档不做状态机，框架会停留在理念层。
- 只有自动化验证没有独立审计，会产生假完成。
- 吸引子定义过细会削弱演进能力。
- memory 不做检索会失去复用价值。

## 9. 直接排期建议

如果按两周一个迭代，建议顺序为：

1. 第 1 迭代：文档骨架 + 领域模型
2. 第 2 迭代：计划闭环 + 验证执行
3. 第 3 迭代：独立审计 + memory
4. 第 4 迭代：路由 + 漂移分析

这样可以先拿到最小闭环，再逐步增强轨迹控制能力。
