# Architecture

本目录承载项目的吸引子定义、架构原则和结构基线。

## Reading Order

1. `../index.md`：仓库级文档路由入口。
2. `../context/source-of-truth.md`：跨文档冲突时的真相源优先级。
3. `attractors/`：当前系统应长期收敛到的稳定结构。
4. `agent-protocol.md`：AI Agent 可程序化读写 ABH 的协议基线。
5. `policies/`：跨模块规则和治理策略。
6. `templates/`：架构文档模板。

## Authority

- 问“系统应该向哪里收敛”，以 active attractor 为准。
- 问“当前实现是什么”，以代码和测试为准。
- 问“某轮任务如何收口”，以对应 plan 为准。
- 问“多个文档不一致时谁优先”，以 `docs/context/source-of-truth.md` 为准。

## Active Attractor

- `attractors/abh-core-attractor.md`
