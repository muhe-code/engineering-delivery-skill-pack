---
name: session-to-skill-evolution
description: 用于按 session id、某一天、某个时间范围或最近会话抓取 Codex 对话，分析用户如何指导 Codex、执行中暴露了哪些问题，并把这些发现回写到指定范围的技能中。支持按根技能递归更新关联技能；若未指定范围，则默认覆盖全局技能与当前工程技能。
---

# 从会话反哺技能

当用户希望拿历史会话来反向优化 Codex skills，而不是只做一次聊天总结时，使用这个技能。

这个技能的目标不是“写一份复盘”就停下，而是把复盘真正转化成技能更新。

开始前阅读：

- `references/analysis-framework.md`
- `references/scope-rules.md`
- `references/platform-patterns.md`

优先使用脚本：

- `scripts/build_retrospective_bundle.py`
- `scripts/resolve_skill_scope.py`

## 何时使用

适用于：

- 用户指定一个或多个 session，希望分析完整对话并更新技能
- 用户指定某一天或某个时间范围，希望复盘这段时间内 Codex 的行为模式
- 用户想知道“我是怎么指导 Codex 的”“Codex 哪里没理解我”“这些问题该怎么沉淀进 skill”
- 用户希望只更新某个根技能及其关联技能，或希望全局更新技能集合

不适用于：

- 只想导出 HTML 日报，不需要技能更新
- 只想对单个 bug 做一次局部修复，不需要会话级归因

## 核心原则

### 1. 先拿到完整证据，再谈技能更新

不要只凭印象修改 skill。

必须先拿到：

- 目标 session 集合
- 可读 transcript
- 执行层证据，例如 tool failure、error、turn abort、用户复验反馈
- 若存在 verifier issue ledger，也应纳入证据，而不是只看会话叙述
- 作用域解析结果

### 2. 更新范围必须显式

如果用户指定了根技能，例如 `project-hub`：

- 先用 `scripts/resolve_skill_scope.py` 解析递归闭包
- 只更新该根技能及其可达关联技能

如果用户没指定范围：

- 默认更新全局技能集合：`~/.codex/skills`
- 再叠加当前工程里的 `skills/` 目录（如果存在）

### 3. 先抽模式，再改文本

必须明确区分：

- 用户如何表达真实诉求
- Codex 在哪里误解了用户
- Codex 在执行里哪里缺验证、缺边界、缺真实路径
- 哪些问题属于单次偶发，哪些已经形成模式

不要直接把某条对话原话机械塞进 skill。

### 4. 平台借鉴只能做启发，不能做拼贴

参考 OpenAI、Anthropic、GitHub Copilot、LangGraph 等平台时：

- 提炼的是设计思想和 workflow
- 不是抄别人的文案结构
- 最终仍要回到这台机器上的 Codex session 证据

## 工作流

按顺序执行，不要跳阶段。

### Stage 1：确定会话范围

支持四种输入方式：

- `--session-id <id>`：一个或多个会话
- `--date YYYY-MM-DD`：某一天
- `--date-from YYYY-MM-DD --date-to YYYY-MM-DD`：时间范围
- `--latest N`：最近 N 个会话，适合“当前 session / 最近几轮”

运行：

```bash
python3 ~/.codex/skills/session-to-skill-evolution/scripts/build_retrospective_bundle.py --session-id 019d10ac-c633-75d1-b44a-cc1c5b08c4bd
```

或：

```bash
python3 ~/.codex/skills/session-to-skill-evolution/scripts/build_retrospective_bundle.py --date-from 2026-03-21 --date-to 2026-03-28
```

产物至少应包含：

- `sessions.json`
- `transcript.md`
- `summary.md`

### Stage 2：确定更新作用域

如果用户指定了根技能：

```bash
python3 ~/.codex/skills/session-to-skill-evolution/scripts/resolve_skill_scope.py --skills-root ~/.codex/skills --skills-root ./skills --root-skill project-hub
```

如果用户未指定：

- 默认把 `~/.codex/skills` 作为全局作用域
- 如果当前工程存在 `./skills`，再把它加入工程作用域

必须记录：

- 根技能
- 递归闭包
- 每个技能的实际路径

### Stage 3：做会话级归因

阅读 `transcript.md` 与 `summary.md`，按 `references/analysis-framework.md` 提炼：

- 用户指导 Codex 的语言模式
- 用户真实在意的成功标准
- Codex 的误解类型
- 执行层失败类型
- 验证问题里反复出现的模式，例如自证完成、遗漏回归、轻视影响面
- 现有 skill 哪些规则没覆盖到
- 应该新增规则、重写规则，还是拆子 skill

如果用户明确抱怨过“你不懂我”“你只是机械执行”，必须把这类信号单独归档，不得混入普通 bug 列表。

### Stage 4：把发现回写进技能

更新顺序：

1. 先改根技能或主路由技能
2. 再改被它显式依赖的相关技能
3. 再改必要的 references / scripts / templates

只要问题已经被证据证明是“模式”，就不要把它留成口头建议。

需要时可以：

- 新增子 skill
- 增加路由规则
- 增加完成定义
- 增加验收矩阵要求
- 增加作用域 / 记忆 / 复盘 / eval 规则

### Stage 5：验证

对每个改过的 skill：

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py <skill_dir>
```

若脚本被修改，还要运行对应测试。

完成前必须确认：

- 作用域内目标技能已更新
- 非作用域技能未被误改
- 复盘证据与 skill 改动有明确映射

## 输出要求

最终汇报至少包含：

- 使用了哪些 session / 日期范围
- 识别出了哪些用户指导模式
- 识别出了哪些 Codex 失败模式
- 更新了哪些 skill
- 为什么这些改动是由这些会话直接驱动的
- 还剩哪些未纳入本轮的非模式化个案

如果用户要求“更新 skill”，就不要只交付分析报告。
