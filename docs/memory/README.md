# Memory

本目录保存跨 session 的外部化记忆。

Memory 不只记录成功结论，更要记录被证伪的前提、已经发散的路径和被推翻的完成判断。

## Types

- `false_assumption`：已被证伪的前提。
- `rejected_path`：已证明会发散或不合适的路径。
- `divergent_pattern`：反复出现、可复用识别的漂移模式。
- `overturned_completion`：后来被审计推翻的完成判断。

以上四个值是 canonical taxonomy，后续文档、模板和 memory 条目都应使用同一套命名。

## Rules

- memory 条目必须包含证据。
- memory 条目必须可被后续 plan 引用。
- 结论过期时不删除，标记 deprecated。
