# 平台借鉴与设计思想

以下内容用于启发这个 skill 的设计，不是要逐字复刻别的平台。

## Anthropic / Claude Code

来源：

- Claude Code memory: https://docs.anthropic.com/en/docs/claude-code/memory
- Prompt improver: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-improver
- XML tags: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags
- Evaluation tool: https://docs.anthropic.com/en/docs/test-and-evaluate/eval-tool

可借鉴点：

- 把长期记忆分层：项目、用户、组织
- 允许显式导入更多上下文，而不是把所有规则都堆在一个文件里
- 用“当前问题反馈 + 示例输入输出”来迭代 prompt，而不是只靠主观感觉改 prompt
- 用结构化标签和评估工具提升可维护性

## OpenAI

来源：

- File search: https://developers.openai.com/api/docs/guides/tools-file-search
- Agent evals: https://developers.openai.com/api/docs/guides/agent-evals
- Trace grading: https://developers.openai.com/api/docs/guides/trace-grading

可借鉴点：

- 将历史对话和技能知识库分开管理，但允许检索增强
- 不只看最终回答质量，也看 trace 级别的错误位置
- 用 datasets / evals / trace grading 形成持续改进飞轮

## GitHub Copilot

来源：

- Repository custom instructions: https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions
- Response customization: https://docs.github.com/en/copilot/concepts/response-customization

可借鉴点：

- 同时支持仓库级、路径级、agent 级指令
- 把“作用域”做成一等概念，而不是所有规则全局生效
- 让引用的指令文件在响应里可追溯

## LangGraph / LangChain

来源：

- Memory overview: https://docs.langchain.com/oss/javascript/langgraph/memory
- Add memory: https://docs.langchain.com/oss/python/langgraph/add-memory

可借鉴点：

- 明确区分 thread-scoped short-term memory 和 namespace-scoped long-term memory
- 记忆更新既可以走热路径，也可以走后台异步路径
- 长上下文问题应通过 trim / summarize / checkpoint 管理，而不是无限堆历史

## MemGPT

来源：

- GitHub: https://github.com/goempirical/MemGPT

可借鉴点：

- 区分工作记忆与归档记忆
- 把“记住什么、何时检索、何时回写”设计成显式机制

## 结论

这个 skill 最应该借鉴的不是某一家的具体接口，而是三条共通原则：

1. 会话证据要结构化
2. 作用域要显式
3. 技能改动要和评估 / 验证绑在一起
