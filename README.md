# Attractor Before Harness

`Attractor Before Harness` 是一个面向 AI 协作开发的收敛框架与 CLI 工具集。项目核心思想来自"先定义系统要收敛到哪里，再用 harness 持续纠偏"的方法论：先把吸引子、基线、计划、验证、审计和记忆显式化，再让开发过程围绕这些对象运行。

## 项目来源

这个项目源于对 AI 大规模开发协作方式的整理与工程化尝试，重点解决三个问题：

1. AI 生成结果不稳定，容易偏离长期目标。
2. 单次任务完成不等于系统轨迹正确。
3. 缺少可审计、可回放、可沉淀的开发过程记录。

因此，本项目把"吸引子"作为长期结构基线，把"harness"作为围绕基线运行的控制层，目标是让仓库本身成为事实来源，而不是把判断留在人的临时记忆里。

## 项目功能

当前项目提供一个名为 `abh` 的命令行工具，支持以下能力：

- `plan`：创建、查看和迁移计划状态（6 状态状态机）
- `verify`：记录验证命令及其结果
- `audit`：发起和记录独立审计
- `close`：在满足条件后关闭计划
- `memory`：记录和检索外部化记忆
- `route`：根据问题输出建议阅读顺序
- `drift`：识别基础漂移并生成漂移报告

所有命令把结构化数据写入 `.abh/` 目录（JSON），同时同步生成 `docs/` 下的 Markdown 文档，便于回放、审查和复用。

## 项目价值

这个项目的价值不在于"再做一个任务管理工具"，而在于把 AI 协作中的关键判断拆开：

- 计划和执行分离，避免边做边给自己验收
- 验证和审计分离，减少假完成
- 历史经验显式存档，避免重复踩坑
- 以仓库为中心沉淀长期结构，为跨 session 持续开发提供可追溯的事实记录

对于需要持续迭代、又希望保持结构稳定的工程团队，这种方式比临时性的聊天上下文更可靠。

## 安装

项目要求 Python 3.13+。先确认版本：

```bash
python3 --version
```

推荐在仓库根目录做 editable install：

```bash
python3 -m pip install -e .
```

安装后可以在任意目录使用 console script：

```bash
abh --help
```

如果没有安装包，也可以在仓库根目录直接运行：

```bash
python3 -m abh --help
```

如果在临时目录或外部目录用源码运行，需要显式提供仓库路径：

```bash
PYTHONPATH=/path/to/harness-before python3 -m abh --help
```

最小验证命令：

```bash
python3 -m unittest tests/test_cli.py
```

## 使用教程

### 1. 创建计划

先创建一个计划，绑定吸引子和基线：

```bash
abh plan create \
  --id plan-001 \
  --title "Sprint 1 Foundation" \
  --attractor docs/architecture/attractors/abh-core-attractor.md \
  --baseline docs/development-roadmap.md \
  --goal "建立标准目录结构" \
  --non-goal "实现路由分析" \
  --exit-criterion "目录与模板文件齐备" \
  --validation "检查 docs 目录结构" \
  --closure-evidence "计划文档与审计记录存在"
```

创建时默认为 `draft` 状态，也可以加上 `--status ready` 直接创建已就绪的计划。可选的 `--owner` 参数用于指定计划负责人。

### 2. 查看计划状态

```bash
abh plan status plan-001
```

### 3. 推进计划状态

计划状态机：`draft → ready → running → closing → closed`（`blocked` 为侧岔路）

```bash
abh plan transition plan-001 --to ready
abh plan transition plan-001 --to running
```

状态迁移有约束：进入 `ready` 前必须有 goals、non-goals、exit criteria 等完整信息；进入 `closing` 前必须有一条通过的验证记录。

### 4. 记录验证

```bash
abh verify record plan-001 \
  --command "python -m unittest tests/test_cli.py" \
  --result pass \
  --artifact "tests/test_cli.py"
```

验证结果支持 `pass` / `fail` / `partial`。如果结果为 `fail` 或 `partial` 且计划处于 `ready` 或 `running`，计划会自动转入 `blocked` 状态。验证失败的具体项可以通过 `--failed-check` 记录。

### 5. 发起审计

```bash
abh audit request plan-001 \
  --id audit-001 \
  --auditor "independent-review" \
  --scope "检查计划是否满足关闭条件" \
  --evidence "docs/plans/plan-001.md"
```

审计请求至少需要一条 evidence 引用（通常为文件路径）。审计记录会同时保存为 `.abh/audits/` 下的 JSON 和 `docs/audits/` 下的 Markdown。

### 6. 记录审计结论

```bash
abh audit record audit-001 \
  --result pass \
  --rationale "证据完整，计划满足关闭条件" \
  --finding "Low|No blocking issue|tests/test_cli.py|No action"
```

`--finding` 格式为 `Severity|Finding|Evidence|Recommendation`，支持多次传入。审计结论可以重复记录（后一次覆盖前一次）。

### 7. 关闭计划

关闭条件：计划必须有至少一条通过（`pass`）的审计记录，并且 `closure_evidence` 非空。

```bash
abh close plan-001
```

### 8. 记录和检索记忆

记忆用于记录被证伪的假设、被拒绝的路径、发散模式和被推翻的完成判断。

```bash
abh memory add \
  --id mem-001 \
  --type false_assumption \
  --summary "某条路径无法稳定收敛" \
  --context "在重复验证中出现漂移" \
  --implication "后续不要再作为默认方案" \
  --evidence "docs/audits/audit-001.md"

abh memory search --query "漂移"
```

记忆搜索使用子字符串匹配（不区分大小写）。如需更精确的范围，可以用 `--type` 按类型过滤。

### 9. 路由和漂移分析

根据问题输出建议阅读顺序：

```bash
abh route --question "Can we close this plan?"
```

对文本证据做基础漂移分析。先准备一份漂移源文件：

```bash
echo "Imported a remote database dependency even though the plan said no external database." > drift-source.txt
```

然后执行分析，并把漂移模式写入 memory：

```bash
abh drift analyze \
  --id drift-001 \
  --source drift-source.txt \
  --evidence drift-source.txt \
  --memory-id mem-drift-001

abh memory search --type divergent_pattern --query dependency
```

漂移分析基于关键词规则识别四类漂移：边界漂移、依赖漂移、测试漂移和术语漂移。

## 项目结构

- `abh/`：CLI 和核心逻辑
- `docs/architecture/`：吸引子与架构说明
- `docs/plans/`：计划文档（Markdown）
- `docs/audits/`：审计文档（Markdown）
- `docs/memory/`：记忆文档（Markdown）
- `docs/drift/`：漂移分析报告（Markdown）
- `.abh/`：运行时结构化数据（JSON），与 `docs/` 下的文档双向同步
- `tests/`：测试用例（unittest）

## 适用场景

- AI 参与的持续开发
- 需要审计闭环的工程流程
- 希望沉淀决策、反例和失败经验的仓库
- 需要把"完成"定义得更严格的项目

## 后续演进

当前仓库已经覆盖计划、验证、审计、关闭、记忆、路由和基础漂移分析。后续计划：

- 提升漂移分析精度：从关键词匹配升级到语义匹配
- 增加 `abh status` 全局概览命令，聚合所有计划、审计和记忆状态
- 支持 Git hook 集成，在提交前自动验证状态一致性
- 为验证记录增加 Markdown 文档输出，与计划的 closure evidence 形成完整可追溯链路
