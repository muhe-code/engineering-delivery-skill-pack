# Runtime Signals

长运行系统至少要有一种可被 Codex 直接读取的运行时信号，而不是只能靠人肉盯着看。

推荐信号面：

- 结构化日志
- metrics counters / gauges
- traces / spans
- health endpoints
- browser recordings / screenshots
- external receipts / control-plane status
- replay transcript

## 设计要求

- 每个关键能力点都要映射到一种可观察信号
- 每个高风险负路径都要能留下可追溯证据
- 若存在异步投影，必须区分“执行成功但尚未投影”与“根本未成功”

## 反模式

- 只能看控制台滚屏，无法查询
- 只有“服务活着”的 health，没有业务级 health
- 只能看 happy path，负路径全靠猜
- 出错后只能重跑，无法区分是投影延迟、权限问题还是真实失败
