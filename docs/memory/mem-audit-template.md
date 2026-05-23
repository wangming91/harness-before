# Memory: ABH 独立审计子 agent 提示词模版

## Metadata

- ID: mem-audit-template
- Type: divergent_pattern
- Status: active
- Created: 2026-05-23T03:29:39.080431+00:00
- Updated: 2026-05-23T03:29:39.080761+00:00
- Related: mem-independent-audit

## Summary

ABH 独立审计子 agent 提示词模版

## Context

通过 audit-007b 验证的独立审计流程：用 agent_open 启动独立子 agent，角色为 explorer，传入结构化的审计 prompt。子 agent 与实现者完全隔离，避免确认偏差。

## Evidence

- docs/audits/audit-007b-zero-dep-install.md

## Implication

后续所有 audit 均复制本模版，仅替换审计对象、exit criteria 和文件列表

## Deprecation Policy

Mark deprecated when evidence no longer applies.

---

## 独立审计子 agent 提示词模版

> 使用方法：复制以下内容，替换 `{{PLACEHOLDER}}` 部分，通过 `agent_open` 传入子 agent。

```
你是独立审计者，角色是 impartial auditor，不是这个项目的实现者。你的任务是对 {{PLAN_ID}} 做独立审计。

## 审计任务

{{PLAN_TITLE}} 的目标是：{{PLAN_GOAL_SUMMARY}}

### 你需要检查的关键文件

{{每行一个文件路径，列出所有相关证据文件}}

### 审计标准（对照计划原文的 exit criteria）

计划声明的 exit criteria：
{{逐条列出 exit criteria，每条前缀 - }}

### 输出格式

请以如下格式输出审计结论：

AUDIT RESULT: [pass / fail / partial]

SUMMARY: 一句话总结

FINDINGS: 每行格式 Severity|Finding|Evidence|Recommendation
至少一条，如无发现则写 "Low|No blocking issue|N/A|No action"

RATIONALE: 详细判断依据，逐条对照 exit criteria 说明是否满足

### 重要提示

- 你是独立的审计者，不要因为发起审计的人说"通过了"就相信。
- 对照 exit criteria 逐条检查，给出具体证据（文件路径、行号）。
- 如果发现任何问题，哪怕拼写错误，也要报告为 finding。
- 不需要运行代码，只做静态分析即可。
- 对无法验证的条目，标注为 Low severity 并说明原因。
```
