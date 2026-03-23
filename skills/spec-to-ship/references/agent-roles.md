# 代理角色

只有当用户明确允许委派或要求并行工作时，才使用子代理。

主代理是控制器，负责工作流状态、产物顺序与最终验证。

## 通用规则

- 只给子代理完成任务所需的最小上下文
- 为 worker 明确定义写入所有权
- 默认不要把整段会话历史直接传给子代理
- reviewer 结论必须引用相关文档或 diff
- 不要仅凭 worker 自报完成就相信结果，必须独立验证

## 需求审查者

目的：

- 挑出歧义、缺失约束、缺失验收信号与被误写成需求的方案假设

输入：

- 当前请求摘要
- 当前需求草稿
- 相关仓库上下文

输出：

- 缺口
- 冲突假设
- 进入 PRD 前必须回问用户的问题

## PRD 审查者

目的：

- 挑出范围漂移、模糊验收、未定义边界策略与仍需工程猜测的地方

输入：

- 需求文档
- PRD 草稿

输出：

- 范围问题
- 不清晰边界
- 验收标准缺口
- 仍需回问用户的产品问题

## 技术方案审查者

目的：

- 判断技术方案是否足够详细到无需重大猜测即可实施

输入：

- PRD
- 技术方案
- 相关代码上下文

输出：

- 架构风险
- 缺失的接口或数据契约
- 测试或迁移缺口

## 实现者

目的：

- 执行一个具体任务或一个边界清晰的工作切片

输入：

- 来自实现计划的精确任务文本
- 目标文件
- 约束
- 相关 spec 摘录

输出：

- 状态：DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED
- 改了什么
- 验证了什么
- 仍然担心什么

## 质量审查者

目的：

- 按 plan、spec 与 diff 检查代码质量

输入：

- 实现计划任务
- 技术方案
- 代码 diff 或触达文件
- 验证证据

输出：

- critical issues
- important issues
- minor issues
- readiness 评估

## 推荐控制模式

串行模式：

- 控制器自己实现，或一次只委派一个任务
- 每个有意义任务/批次后做 quality review

并行模式：

- 控制器把互不重叠的切片分配给不同 implementer
- 每个切片都做 spec 或 quality review
- 控制器做最终集成 review 再继续

## Prompt 模板

具体模板位于技能目录：

- `requirements-reviewer-prompt.md`
- `prd-reviewer-prompt.md`
- `spec-reviewer-prompt.md`
- `implementer-prompt.md`
- `quality-reviewer-prompt.md`
