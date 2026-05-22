# Attractor: ABH Core

## Metadata

- ID: attractor-abh-core
- Version: 0.1.0
- Status: active
- Scope: repo
- Owner: architecture
- Supersedes: none

## Intent

Attractor Before Harness 的核心结构必须收敛到一个 Git-native、证据优先、生成与验收分离的轨迹控制框架。

框架的第一性对象不是任务，也不是测试，而是长期结构吸引子。计划、验证、审计和记忆都必须围绕吸引子工作。

## Invariants

- 每个可执行 plan 必须绑定一个 active attractor。
- 每个 plan 必须声明 baseline、goals、non-goals、exit criteria 和 closure evidence。
- 验证结果只能证明机器检查状态，不能直接证明计划完成。
- 计划关闭必须依赖独立 audit。
- audit 必须引用仓库中的 evidence。
- memory 必须记录失败路径、被证伪前提或被推翻完成判断。
- 所有核心对象必须以仓库文件作为主真相。

## Boundary Rules

- Attractor 只定义高阶不变量，不承载局部任务细节。
- Plan 只定义一轮扩张如何收口，不替代吸引子。
- Verification 只负责机器可判定检查，不替代 audit。
- Audit 只做独立完成判定，不参与实现生成。
- Memory 只保存跨 session 有复用价值的轨迹经验，不做普通日志归档。

## Dependency Rules

- Plan 依赖 Attractor。
- VerificationRun 依赖 Plan。
- AuditReport 依赖 Plan 和 Evidence。
- MemoryEntry 依赖 Evidence。
- Plan 关闭依赖 AuditReport。

逻辑顺序：

```text
Attractor -> Plan -> Verification -> Audit -> Memory
```

## Anti-Patterns

- 无吸引子直接开工。
- 把 plan 当作普通 todo list。
- 把测试通过当作完成。
- 让实现 session 自己宣布最终完成。
- 只记录成功结论，不记录失败原因。
- 把吸引子写成过细的实现步骤。

## Precedence

- 本文档是当前项目的 active attractor。
- 计划文档必须服从本文档中的不变量和边界规则。
- 如果详细设计与本文档冲突，以本文档的高阶不变量为准，并发起吸引子修订。

## Change Policy

修改本吸引子需要满足至少一个条件：

- 多个 plan 暴露出同一结构规则失效。
- audit 发现当前不变量无法支撑真实收敛。
- 新能力引入后改变了核心对象之间的关系。

修改时必须记录：

- 变更原因
- 影响范围
- 与旧版本的差异
- 迁移策略

## Evidence

- `docs/attractor-before-harness-framework.md`
- `docs/attractor-before-harness-detailed-design.md`
- `docs/attractor-before-harness-prd.md`
- `docs/attractor-before-harness-task-breakdown.md`
