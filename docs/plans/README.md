# Plans

本目录承载每一轮开发扩张的收口计划。

Plan 不是待办列表，而是局部轨迹收敛机制。每个 plan 必须说明 baseline、目标、非目标、退出条件、验证清单和关闭证据。

## Status

- draft：计划草拟中。
- ready：已具备执行条件。
- running：正在执行。
- blocked：被失败、依赖或结构问题阻断。
- closing：正在关闭审计。
- closed：已关闭。

## Rules

- 没有绑定 attractor 的 plan 不能进入 ready。
- 没有 exit criteria 的 plan 不能进入 ready。
- 没有独立 audit 的 plan 不能 closed。
- closed plan 必须有 closure evidence。
- 关闭前应运行 `abh doctor`，确认 `.abh/` JSON 与 `docs/` Markdown 没有分裂。
