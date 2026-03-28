# Engineering Delivery Skill Pack

面向 Codex 的工程交付技能包。

这个仓库包含一组自定义技能，目标是让 Codex 在复杂工程任务里更像一个有纪律的工程负责人，而不是只会快速产出半成品。

它主要解决八类问题：

- 当用户只想引用一个技能时，提供单入口编排
- 把模糊请求推进成 requirements、PRD、tech spec、plan 和 execution tracker
- 强制任务真正闭环，而不是过早宣布完成
- 在实现前先设计逐条验收用例
- 按真实用户生命周期路径验证有状态产品
- 把本地推断和外部权威真相源区分开
- 把 Codex 历史会话沉淀成有证据的技能进化
- 在长时间运行系统里，先设计 harness，再做功能开发

English version: [README.md](./README.md)

## 包含的技能

### `project-hub`

给只想引用一个 skill 的用户使用的单入口技能。

它会判断当前任务需要：

- `spec-to-ship`
- `done-means-done`
- 或两者联动

它是路由与编排层，不是对底层 skill 的替代。

### `spec-to-ship`

把模糊功能请求推进为：

- requirements
- PRD
- tech spec
- implementation plan
- execution tracker
- verified delivery

它现在额外强调：

- 当产品形态变化时必须 rebaseline
- 不能只有抽象验收标准，必须形成验收用例矩阵
- 聊天 / 会话 / 流式 / 生命周期问题要走状态化产品验证
- 外部系统集成要区分本地推断与权威真相源

### `done-means-done`

要求任务真正闭环，明确防止：

- 半截交付
- 把范围内后续工作包装成可选项
- 没有证据就宣称完成
- 用户已经报 bug 后还沿用旧验证当作完成背书

它现在额外强调：

- 用户旅程级验收用例
- 正式入口与真实路径验证
- 外部系统对账
- 产品形态变化后必须重定义完成标准

### `acceptance-test-design`

把需求转成逐条可执行的验收用例矩阵，覆盖：

- 用户旅程
- 视觉效果
- 交互状态
- 功能结果
- 特殊案例
- 回归路径

### `stateful-product-validation`

用于聊天、会话、轮询、流式、附件、分页、断线恢复、长任务等状态化产品。

重点解决“接口看起来没问题，但真实产品体感仍然很差”的情况。

### `external-system-reconciliation`

用于第三方 API、远端服务、部署进程、支付/交易/通知系统、设备状态等外部权威真相源场景。

重点解决“本地日志或文案说成功，但外部真实状态并不一致”的情况。

### `session-to-skill-evolution`

用于按 session、某一天或某个时间范围回看 Codex 历史对话，提炼用户如何指导 Codex、执行里反复暴露了哪些问题，并把这些发现真正回写成 skill 更新。

它支持两种范围：

- 只更新某个根技能及其递归关联技能
- 若未指定范围，则更新全局技能集合和当前工程技能集合

### `long-running-app-harness`

用于 agent、bot、worker、scheduler、queue、Webhook、长时间运行服务或任何需要长期观测、恢复、回滚的系统。

它要求先做 harness 设计，而不是后补：

- 仓库内知识入口
- 一键启动与隔离
- 机械化约束
- 运行时信号与可观测性
- eval gate
- kill switch 与 rollback

## 安装

把 `skills/` 下的目录复制到 Codex skills 目录，例如：

```bash
cp -R skills/* ~/.codex/skills/
```

如果你的环境使用 `$CODEX_HOME/skills`，则复制到对应目录。

## 用户如何更好地使用这些技能

这些技能在以下话术下效果最好：

1. 明确目标
2. 明确交付物
3. 明确要求端到端完成
4. 明确验证要求

推荐话术：

```text
请使用 $spec-to-ship 和 $done-means-done 处理这个任务。
把需求推进成 requirements、PRD、tech spec、plan、实现、验证和收尾。
只要范围内还有实现、验证、review 修复或文档回写没有完成，就不要停。
```

如果你想只引用一个 skill：

```text
请使用 $project-hub 处理这个任务。
由它判断是否需要联动 $spec-to-ship，但最终必须按 $done-means-done 的标准收口。
```

如果你想让 Codex 从历史会话里学，并真正更新 skill：

```text
请使用 $session-to-skill-evolution 处理这些 session 或这个日期范围。
分析我是怎么指导 Codex 的、Codex 重复暴露了哪些问题，并把这些发现回写到作用域内的技能。
如果我指定了根技能，例如 $project-hub，就只更新它和它递归关联的技能。
```

如果任务是 UI / 页面 / 产品交互：

```text
请使用 $done-means-done 处理这件事。
这是用户可见界面，所以布局、交互质量、可读性、移动端体验都属于完成标准。
```

如果任务容易在产品验收时暴露 bug：

```text
请在实现前使用 $acceptance-test-design，把用户旅程、特殊案例和回归路径写成逐条验收用例。
```

如果任务是聊天、会话、流式、轮询或生命周期复杂的产品：

```text
请使用 $stateful-product-validation，并确保验证覆盖首次使用、继续使用、慢响应和恢复路径。
```

如果任务依赖第三方或远端真相源：

```text
请使用 $external-system-reconciliation，在宣称成功前先与外部权威系统完成对账。
```

如果任务是 agent、bot、后台任务、长运行服务或 scheduler：

```text
请先使用 $long-running-app-harness。
不要先堆功能实现，先把知识入口、运行时 signals、eval gate、安全护栏和回滚路径设计好。
```

## 建议直接把链接给 Codex，让它自行下载

实践里，最省事的方式通常是直接把仓库链接交给 Codex，让它从 GitHub 安装这些技能。

推荐话术：

```text
请把 https://github.com/muhe-code/engineering-delivery-skill-pack.git 里的技能安装到我的 Codex skills 目录。
以这个仓库为准，安装以下技能：
- project-hub
- spec-to-ship
- done-means-done
- acceptance-test-design
- stateful-product-validation
- external-system-reconciliation
- session-to-skill-evolution
- long-running-app-harness
```

如果你的 Codex 环境支持 skill installer 工作流，这通常会比把大段 skill 内容直接粘贴进聊天更稳。

## 为什么仓库里没有打包第三方 companion skills

本仓库故意不直接镜像第三方 companion skills。

原因：

- 避免把上游 skill 包装成这里的原创内容
- 避免来源与许可证边界不清
- 减少后续跟随上游更新的维护成本

如果你希望尽量复现作者当前的更完整工作流，通常还会想额外安装这些技能：

- `brainstorming`
- `writing-plans`
- `systematic-debugging`
- `verification-before-completion`
- `requesting-code-review`
- `frontend-design`
- `design-taste-frontend`

这些更适合直接从各自上游来源安装。

## 仓库结构

```text
skills/
  acceptance-test-design/
  done-means-done/
  external-system-reconciliation/
  long-running-app-harness/
  project-hub/
  session-to-skill-evolution/
  spec-to-ship/
  stateful-product-validation/
```

## 许可证

本仓库使用 [MIT License](./LICENSE)。
