---
name: skill-engineering
description: 用于创建、更新、拆分、合并、瘦身或优化 Codex skills。根据 Tool Wrapper、Generator、Reviewer、Inversion、Pipeline 及其组合模式选择合适结构，并把工程失败、session 证据与新需求转成技能改动。
---

# Skill Engineering

当任务本身不是业务功能，而是要创建、更新、优化或重构 skill 时，使用这个技能。

这个技能的目标不是“随手改一下 SKILL.md”，而是把 skill 当成工程资产来设计：明确触发条件、结构模式、资源拆分、验证方式和演进依据。

## 何时使用

适用于：

- 新建一个 skill
- 更新已有 skill 的触发条件、流程、资源或验证方式
- 把一个过胖的 skill 拆成主 skill + 子 skill
- 把多个重复 skill 合并成更清晰的能力边界
- 基于 session、验收 bug、verifier issue 或新工程方法论反哺 skill
- 需要判断某个能力更适合写成 Tool Wrapper、Generator、Reviewer、Inversion、Pipeline 还是组合模式

不适用于：

- 只是在业务代码里顺手写几句提示
- 不需要沉淀为长期复用能力的一次性说明

## 核心原则

### 1. 先判断“需不需要 skill”

不要把每个流程、偏好或一次性 workaround 都做成 skill。

优先做成 skill 的情况：

- 高频复用
- 容易反复出错
- 上下文依赖强
- 需要固定 gate / checklist / 模板 / 资源
- 值得长期演化

### 2. 先选模式，再写内容

优先判断下面哪种模式最匹配：

- `Tool Wrapper`
  - 目标：提供某个库、框架、规范或领域的专家知识
  - 结构：`SKILL.md` + `references/`
- `Generator`
  - 目标：稳定产出固定结构的文档、模板、脚手架或报告
  - 结构：`assets/` + `references/`
- `Reviewer`
  - 目标：按 checklist 做评审、审计、验收或评分
  - 结构：`references/` 中的检查表 + 明确输出格式
- `Inversion`
  - 目标：先收集信息，再行动
  - 结构：分阶段提问 + gate
- `Pipeline`
  - 目标：多步骤顺序流程，阶段之间有明确 gate
  - 结构：步骤、gate、分阶段资源加载

大多数成熟 skill 都是组合模式，而不是纯一种模式。

### 3. 主 skill 要瘦，细节按需下沉

`SKILL.md` 保留：

- 触发条件
- 核心工作流
- 关键 gate
- 何时读取哪类资源

细节应下沉到：

- `references/`：规则、checklist、领域知识
- `assets/`：模板、样板、输出骨架
- `scripts/`：需要确定性执行的逻辑

### 4. 触发描述是路由入口，不是装饰文案

`description` 必须回答：

- 什么时候应该触发这个 skill
- 哪类任务不该触发它
- 它解决什么失败模式

如果 description 写得空泛，skill 基本等于不存在。

### 5. 以真实失败反哺，而不是靠想象补规则

优先吸收：

- 用户验收 bug
- verifier issue
- session 复盘
- 长运行系统里的观测失败
- 文档和实现反复漂移的模式

不要只凭“我觉得应该更完善”就堆规则。

## 工作流

### Stage 1：定义本轮 skill 任务

先明确是：

- 新建
- 更新
- 拆分
- 合并
- 瘦身
- 模式重选

同时明确输入来源：

- 当前工程需求
- session 复盘
- 验证失败
- 外部文章 / 方法论
- 用户新偏好

### Stage 2：做模式判断

至少回答：

- 这是知识封装、固定输出、评审、访谈、流程控制中的哪一类
- 是否需要组合模式
- 是否需要把一个胖 skill 拆成主 skill + 子 skill
- 是否应该新增 `references/`、`assets/` 或 `scripts/`

### Stage 3：设计 skill 结构

至少明确：

- `name`
- `description`
- `SKILL.md` 的核心工作流
- 是否需要 `agents/openai.yaml`
- 是否需要 `references/`
- 是否需要 `assets/`
- 是否需要 `scripts/`

### Stage 4：做最小正确改动

更新原则：

- 不要把 skill 改成更长但更混乱
- 不要把多个失败模式塞进一个模糊大段
- 能拆成子 skill 就不要继续往主 skill 里灌
- 能把细节下沉到 references，就不要堆满主文件

### Stage 5：验证

至少完成：

- `quick_validate`
- 检查 `agents/openai.yaml` 是否仍与 skill 一致
- 检查是否真的解决了本轮失败模式
- 检查是否引入了新的触发歧义或职责重叠

## 与现有技能体系的关系

在当前工程里，常见映射是：

- `spec-to-ship`：以 `Inversion + Pipeline` 为主
- `done-means-done`：以 `Pipeline + Reviewer` 为主
- `independent-verification`：以 `Reviewer` 为主
- `acceptance-test-design`：以 `Generator + Reviewer` 为主
- `project-hub`：编排层，不是单一模式
- `session-to-skill-evolution`：复盘驱动的 skill 演化入口

当这些 skill 需要新增能力、拆分职责或吸收新的工程思想时，应该先经过本技能做模式判断，再修改文本。

## 输出要求

最终输出至少说明：

- 本轮是新建还是更新
- 选择了哪种模式或组合模式
- 为什么这样设计
- 改了哪些 skill
- 为什么这些改动能更好地解决对应失败模式
