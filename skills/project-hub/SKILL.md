---
name: project-hub
description: 工程任务的单入口技能。用于当用户只想引用一个技能时，由它判断何时联动 spec-to-ship、done-means-done 以及相关子技能，并把工作推进到已验证收尾。
---

# Project Hub

当用户不想显式记住多个 skill，而是希望“引用一个技能就够了”时，使用这个技能。

这个技能本身不是 `spec-to-ship` 和 `done-means-done` 的替代品，而是它们的单入口编排层：

- 负责判断当前任务是否需要文档链、计划链、执行链
- 负责决定是否必须联动 `spec-to-ship`
- 负责确保最终一定落到 `done-means-done`
- 负责继续路由到前端、验收、状态化产品、外部真相源等专门 skill

## 何时使用

适用于：

- 用户想只引用一个 skill 来推进复杂工程任务
- 用户经常忘记该用 `spec-to-ship` 还是 `done-means-done`
- 任务可能会从澄清、文档、实现、验证一路推进到收尾
- 需要先判断任务复杂度，再决定流程重量

不适用于：

- 用户已经明确指定只用某个更专门的 skill
- 极小的单文件改动，且验收标准显而易见

## 路由原则

### 1. 默认把它当成“单入口”

当用户引用 `$project-hub` 时，先不要急着编码。先判断：

1. 这是不是一个需要文档链和计划链的工程任务
2. 这次是否需要把模糊需求收敛成书面契约
3. 用户是否期待端到端完成，而不只是一个局部回答

只要答案不是明显的“否”，就默认同时联动：

- `spec-to-ship`
- `done-means-done`

### 2. 何时必须联动 `spec-to-ship`

出现以下任一情况，就必须启用 `spec-to-ship`：

- 需求仍然模糊
- 任务跨多个阶段、文件或子系统
- 需要 requirements / PRD / tech spec / plan / tracker
- 任务存在明显范围漂移风险
- 用户刚改变了产品形态、边界或验收口径

### 3. 何时只需要 `done-means-done`

若任务已经清楚到不值得起完整文档链，但用户仍要求严格闭环，则至少启用 `done-means-done`。

例如：

- 明确的小修复
- 已知范围的小型实现
- 已有计划下的收尾执行
- 明确目标的文档完善或运维动作

### 4. 继续路由到专门 skill

根据任务特征，继续联动：

- 有前端页面、布局、视觉和交互质量：`frontend-design`
- 重点是质感、排版、信息层级和去 AI 味：`design-taste-frontend`
- 需要逐条验收用例矩阵：`acceptance-test-design`
- 有聊天、会话、轮询、流式、附件、生命周期：`stateful-product-validation`
- 依赖第三方 API、远端服务、部署状态或其他外部真相源：`external-system-reconciliation`
- 需要按 session / 日期 / 时间范围复盘历史对话，并据此更新技能：`session-to-skill-evolution`
- 验证失败或出现异常行为：`systematic-debugging`
- 宣称完成前：`verification-before-completion`

## 执行要求

### 1. 先定义完成

在动手前，明确：

- 用户最终想拿到什么
- 这次任务是否需要完整文档链
- 哪些验证能支撑最终完成声明
- 当前更像“从规格到交付”，还是“明确任务的强闭环执行”

### 2. 重流程，但不滥流程

不要为了“统一入口”而把所有任务都强行升格成重文档工程。

判断标准：

- 复杂、模糊、跨模块、有漂移风险：走 `spec-to-ship + done-means-done`
- 清晰、局部、范围稳定：走 `done-means-done`，并按需要补专门 skill

### 3. 最终完成一定由 `done-means-done` 收口

无论前面是否启用了 `spec-to-ship`，最终都必须满足：

- 范围内工作已闭合
- 必要验证已完成
- 文档与实现没有明显漂移
- 不把剩余必要动作包装成“可选下一步”

## 推荐用法

用户可以只说：

```text
请使用 $project-hub 处理这个任务。
如果需要文档链，就联动 $spec-to-ship；如果任务已经明确，就至少按 $done-means-done 的标准收口。
```

或者更直接：

```text
Use $project-hub as the single entrypoint for this task.
Decide whether this needs $spec-to-ship, but always finish it to $done-means-done quality.
```
