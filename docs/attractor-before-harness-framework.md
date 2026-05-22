# Attractor Before Harness：AI 大规模开发框架设计

## 1. 背景

本文档基于文章《Attractor Before Harness: AI 大规模开发的方法论》整理，目标是把“先定义系统收敛到哪里，再用 harness 持续纠偏”的思想，工程化落成一套可用于 AI 参与大规模开发的框架。

核心判断是：AI 协作场景下，单次状态正确不等于长期轨迹正确。框架必须先显式定义吸引子，再围绕吸引子构建验证、审计、收口与记忆机制。

## 2. 需求梳理

### 2.1 目标

- 把长期结构基线显式化、版本化、可审计。
- 让 AI 生成、验证、验收三者分离。
- 让仓库成为系统真相载体，而不是把判断留在人的隐性记忆中。
- 支持多轮 session 下的轨迹收敛，而不是只看单次任务是否完成。

### 2.2 核心问题

- 系统应当向哪里长期收敛。
- 当前改动是否在逼近收敛目标，还是制造漂移。
- 什么材料是权威依据，什么只是临时推导。
- 如何防止同一上下文既做实现又做完成判定。
- 如何保留被证伪的前提、发散的路径、失败的经验。

### 2.3 关键对象

- 吸引子：长期稳定结构，不变量集合。
- 轨迹：一系列生成、验证、纠偏后的真实演化路径。
- 控制：对轨迹施加影响的局部机制。
- Harness：路由、计划、验证、审计、记忆等收敛基础设施。

### 2.4 用户角色

- 架构定义者：提出新的吸引子。
- 开发者/Agent：围绕吸引子展开实现。
- 审计者：独立判断是否真正收敛。
- 维护者：沉淀历史、经验和失败路径。

## 3. 设计目标

1. 先方向，后执行。先有吸引子，再有 harness。
2. 生成与验收分离。验收必须基于独立证据。
3. 轨迹可见。每一次扩张都要留下可回放的证据。
4. 吸引子可版本化。系统结构可以演进，但演进要有边界。
5. 最小侵入接入。尽量适配现有仓库、CI 和文档体系。

## 4. 总体架构

框架建议拆成五层：

### 4.1 吸引子层

负责定义系统应长期收敛的结构。

输出物：

- 架构原则
- 不变量
- 依赖方向
- 边界定义
- 术语表

### 4.2 计划层

负责定义每轮扩张如何收口。

输出物：

- current baseline
- goals / non-goals
- exit criteria
- validation checklist
- closure evidence

### 4.3 验证层

负责自动化检测明确、可重复、可机器判断的偏离。

输出物：

- lint
- typecheck
- build
- test
- contract check

### 4.4 审计层

负责处理自动化无法覆盖的语义漂移、结构偏差和假完成。

输出物：

- 独立审计结论
- 偏离分类
- 风险说明
- 关闭或回滚建议

### 4.5 记忆层

负责跨 session 保存历史轨迹。

输出物：

- 已证伪前提
- 发散路径
- 已失败方案
- 被推翻的完成判断

## 5. 核心模块

### 5.1 Attractor Registry

管理吸引子定义及其版本。

能力：

- 定义吸引子文档
- 记录版本差异
- 标记适用范围
- 支持局部/全局吸引子

### 5.2 Plan Manager

管理每轮任务的收敛计划。

能力：

- 创建计划
- 绑定 baseline
- 维护退出条件
- 记录关闭证据
- 计划拆分与派生

### 5.3 Verification Runner

执行机械化验证。

能力：

- 触发本地或 CI 检查
- 汇总结果
- 对比基线
- 输出可判定失败项

### 5.4 Audit Engine

执行独立审计，避免自我验证陷阱。

能力：

- fresh session 复查
- 基于仓库证据判定
- 检查完成声明是否成立
- 输出审计报告

### 5.5 Memory Store

存储轨迹型知识。

能力：

- 保存历史结论
- 保存反例
- 保存失败原因
- 支持检索与引用

### 5.6 Router

决定问题进入哪个处理路径。

能力：

- baseline 路由
- plan 路由
- docs 路由
- incident 路由
- audit 路由

## 6. 关键数据模型

### 6.1 Attractor

```yaml
id: string
name: string
version: string
scope: repo | package | module
invariants: []
dependency_rules: []
boundary_rules: []
owner_docs: []
status: active | superseded
```

### 6.2 Plan

```yaml
id: string
title: string
baseline_ref: string
goals: []
non_goals: []
exit_criteria: []
validation_checklist: []
closure_evidence: []
status: draft | active | blocked | closed
```

### 6.3 Audit Report

```yaml
plan_id: string
result: pass | fail | partial
findings: []
evidence_refs: []
recommendations: []
reviewer: string
timestamp: string
```

### 6.4 Memory Item

```yaml
type: false_assumption | rejected_path | divergent_pattern | overturned_completion
summary: string
evidence_refs: []
related_ids: []
timestamp: string
```

## 7. 主要工作流

### 7.1 新需求进入

1. Router 识别问题类型。
2. 读取对应吸引子和 baseline。
3. 创建或更新 Plan。
4. 明确目标、非目标和退出条件。

### 7.2 AI 实现

1. Agent 按 Plan 生成变更。
2. 输出代码、文档、测试与说明。
3. 生成过程本身不等于完成。

### 7.3 机器验证

1. Verification Runner 执行检查。
2. 汇总通过/失败项。
3. 记录与 baseline 的差异。

### 7.4 独立审计

1. Audit Engine 用独立上下文重读仓库。
2. 检查实现是否真的满足退出条件。
3. 判断是否可以关闭，或需要继续扩张/回滚。

### 7.5 关闭与记忆沉淀

1. 若通过，Plan 关闭。
2. 记录 closure evidence。
3. 将关键结论写入 Memory Store。
4. 如发现旧吸引子不再成立，发起吸引子更新流程。

## 8. 接口建议

### 8.1 文档接口

- `GET /attractors`
- `POST /attractors`
- `GET /plans`
- `POST /plans`
- `POST /audits`
- `GET /memory/search`

### 8.2 Agent 接口

- `read_baseline()`
- `create_plan()`
- `run_verification()`
- `request_audit()`
- `close_plan()`

### 8.3 事件接口

- `attractor.created`
- `plan.created`
- `verification.failed`
- `audit.passed`
- `audit.failed`
- `memory.recorded`

## 9. 落地原则

- 吸引子文档要短而硬，只保留高阶不变量。
- Plan 不能退化成待办清单，必须包含收口条件。
- 验证结果不能替代审计结论。
- 完成判定必须来自独立证据，不来自实现上下文自报。
- 记忆必须保留失败原因，而不是只保留成功结论。

## 10. MVP 范围

第一阶段建议只做三件事：

1. 吸引子文档体系
2. Plan + 验证 + 审计闭环
3. 失败记忆库

这三项足以支撑最小可用的轨迹收敛框架。

## 11. 风险与约束

- 如果团队没人能定义吸引子，框架无法自动产生正确方向。
- 如果审计仍然依赖同一上下文，系统会落入自我验证陷阱。
- 如果吸引子定义过细，会把长期结构写死，削弱演进能力。
- 如果验证过度依赖机械规则，会漏掉语义漂移。

## 12. 结论

这个框架的核心不是“更强的 harness”，而是“先定义系统向哪里收敛，再把 harness 变成轨迹控制基础设施”。

一句话概括：

> 状态空间 -> 吸引子 -> 轨迹 -> 控制

这不是更复杂的流程，而是更基础的工程对象。
