# Engineering Delivery Skill Pack

面向 Codex 的工程交付技能包。

这个仓库聚焦一组互相配合的自定义技能：

- `spec-to-ship`
- `done-means-done`
- `acceptance-test-design`
- `stateful-product-validation`
- `external-system-reconciliation`

目标是让 Codex 在复杂工程任务里更像一个有纪律的工程负责人，而不是只会快速产出半成品。

## 包含的技能

### `spec-to-ship`

把模糊需求推进到：

- requirements
- PRD
- tech spec
- implementation plan
- execution tracker
- verified delivery

它现在额外强调：

- 产品形态变化时必须 rebaseline
- 不能只有抽象验收标准，必须形成验收用例矩阵
- 聊天 / 会话 / 流式 / 生命周期问题要走状态化产品验证
- 外部系统集成要区分本地推断与权威真相源

### `done-means-done`

要求任务真正闭环，不接受：

- 半截交付
- 把范围内工作包装成可选项
- 没有证据就宣称完成
- 被用户验出 bug 后还沿用旧验证为完成背书

它现在额外强调：

- 用户旅程级验收用例
- 真实路径与正式入口验证
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

## 安装

把 `skills/` 下需要的目录复制到本机的 Codex skills 目录，例如：

```bash
cp -R skills/* ~/.codex/skills/
```

如果你的环境使用 `$CODEX_HOME/skills`，则复制到对应目录。

## 为什么仓库里没有打包第三方 companion skills

本仓库故意不直接镜像第三方 companion skills。

原因：

- 避免把上游 skill 误包装成这里的原创内容
- 避免公开仓库里出现来源与许可证边界不清
- 减少后续同步上游时的维护成本

如果你希望完整复现作者当前的工作流，通常还需要额外安装这些技能：

- `brainstorming`
- `writing-plans`
- `systematic-debugging`
- `verification-before-completion`
- `requesting-code-review`
- `frontend-design`
- `design-taste-frontend`

建议从各自上游来源安装，而不是依赖这个仓库的镜像副本。

## 仓库结构

```text
skills/
  acceptance-test-design/
  done-means-done/
  external-system-reconciliation/
  spec-to-ship/
  stateful-product-validation/
```

## 许可证

当前仓库尚未附带统一 LICENSE 文件。

如果你准备正式对外宣称“欢迎自由复用”，建议先补充明确许可证。
