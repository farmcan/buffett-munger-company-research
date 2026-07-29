# 六家公司事件 Surprise × 市场共振时间轴

这不是把事件抄进一张表，而是复用 Seed 的
`earnings-season-timeline-analyst` 数据契约和确定性 renderer：

- 六条公司泳道共享一条日期轴，并用 `NOW` 分隔历史与未来；
- 历史事件保存事前基线、官方实际、Surprise、T0/T+1/T+5/T+20、行业传导和复盘；
- 没有事前冻结共识时明确显示“不可比”，不事后编造 Surprise；
- 未来事件只冻结问题，使用空心节点，不预填结果；
- 每个关键事实均链接到公司 source ledger 中的公开原始来源；
- HSTECH 只作为共享风险偏好背景，不是六家公司共同业绩基准。

公开入口：

- [`report.html`](./report.html)
- [`timeline.json`](./timeline.json)

重建 JSON，并用 Seed 的固定版本 renderer 生成独立 HTML：

```bash
python docs/company-event-timeline/build_timeline.py \
  --renderer ../seed/skills/earnings-season-timeline-analyst/scripts/render_earnings_timeline.py
```

页面是研究辅助，不构成投资建议。事件窗口只表示价格共振，不证明单一事件造成全部涨跌。
