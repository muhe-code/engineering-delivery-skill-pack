---
name: long-running-app-harness
description: 用于 agent、bot、后台调度系统、长时间运行服务、异步工作流、Webhook/queue/cron 驱动系统或任何需要持续观测与恢复的应用。要求先设计 harness：仓库内知识入口、可复现环境、机械化约束、运行时可观测性、评估门、回滚与安全护栏。
---

# 长运行应用 Harness 设计

当任务的难点不是“写一个函数”，而是“让一个持续运行的系统能被 Codex 稳定开发、验证、观测和回滚”时，使用这个技能。

开始前阅读：

- `references/harness-checklist.md`
- `references/runtime-signals.md`
- `assets/templates/harness-contract-template.md`

这个技能的目标不是直接写业务代码，而是先把环境设计成一个 agent 能稳定工作的系统。

## 何时使用

适用于：

- agent / bot / worker / daemon / scheduler / cron
- 长时间运行的 Web 服务、后台服务、多进程系统
- 需要持续轮询、异步投影、WebSocket、Webhook、队列消费
- 需要多轮观测、恢复、降级、回滚
- “跑起来以后才知道对不对”的系统

不适用于：

- 明确的小型静态功能改动
- 无持续运行语义的单次脚本

## 核心原则

### 1. 先设计 harness，再放大自主性

不要让 Codex 先写一堆业务代码，再事后补：

- 日志
- metrics
- traces
- health checks
- replay fixtures
- kill switch
- rollback

这些不是附属品，而是长运行系统的开发地基。

### 2. 让系统对 agent 可见

Codex 只能根据它能读到的东西工作。

因此必须把关键反馈面变成 agent 可见：

- 仓库内知识入口
- 一键启动命令
- 结构化日志
- 可查询状态
- 可重复回放
- 浏览器或等价用户驱动
- 失败与恢复信号

### 3. 机械化约束优先于口头约束

架构边界、命名契约、格式、依赖方向、数据校验、关键安全边界，优先做成：

- CI gate
- linter
- schema validation
- health assertions
- runtime guardrails

不要只把这些写在文档里。

### 4. 完成声明必须依赖 harness 证据

长运行系统没有 harness 证据，就不允许宣称“已完成”。

至少要能回答：

- 怎么启动
- 怎么观察
- 怎么验证
- 怎么暂停 / 禁用
- 怎么回滚

## 必须产出的 Harness Contract

至少覆盖六部分：

1. `Knowledge Entry`
   - 仓库里哪个文件是总入口
   - deeper docs 在哪里
   - 哪些文档是 source of truth
2. `Boot & Isolation`
   - 一键启动命令
   - 环境变量来源
   - worktree / sandbox / 本地隔离策略
3. `Mechanical Invariants`
   - 哪些规则由 CI / lint / schema 强制
4. `Runtime Signals`
   - logs / metrics / traces / health / browser evidence / external receipts
5. `Evaluation Gates`
   - 能力点覆盖账本
   - happy path / negative path / recovery path / long-horizon path
6. `Safety & Rollback`
   - kill switch
   - disable path
   - rollback playbook
   - least-privilege / network / secret rules

## 工作流

### Stage 1：识别运行面

先列清：

- 长运行组件有哪些
- 谁触发它们
- 用户能看到什么 I/O
- 外部系统交互点有哪些
- 哪些地方会异步失败、延迟投影、半成功

### Stage 2：写 Harness Contract

优先使用 `assets/templates/harness-contract-template.md`。

不要接受“后面再补日志/监控/回滚”。

### Stage 3：把 contract 回写到主流程

如果当前任务也在走 `spec-to-ship`：

- requirements 写运行面与 operator model
- PRD 写用户可见长期行为与失败标准
- tech spec 写 signals / eval gates / rollback
- plan 先做 harness 任务，再做功能任务
- tracker 记录哪类证据已经拿到

### Stage 4：联动专门 skill

- 用户旅程与验收矩阵：`acceptance-test-design`
- 状态机 / 会话 / 流式 / 长任务：`stateful-product-validation`
- 外部系统与真实对账：`external-system-reconciliation`
- 最终完成声明：`verification-before-completion`

## 未完成判定

出现以下任一情况，就不能说完成：

- 只有业务功能，没有 harness contract
- 只能本地猜对，不能被真实观测
- 没有负路径与恢复路径证据
- 没有 operator control path，例如禁用、暂停、回滚
- agent 需要依赖口头知识，而不是仓库内可读知识
