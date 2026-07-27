# 南华期货（02691.HK）公司研究公开包

状态：`needs_human_review`。研究日：2026-07-27。此目录是可公开审阅的 production-shaped 包，但没有人类审批，不得标为 `production_reviewed`。

## 入口

- [可读报告](./report.html)
- [25维度 / 50+指标 / 9 Gate 合并产物](./combined-artifact.v2.json)
- [来源账本](./source-ledger.json)
- [关键证据索引](./evidence-index.json)
- [机器反方审查](./red-team.json)
- [校验结果](./validator-results.json)

## 研究结论边界

- 02691.HK 与 603093.SH 是同一发行人的 H/A 普通股；截至研究日，沪深两份南向官方名单均显示 02691 eligible。
- 金融机构分支不使用“合并 CFO 减资本开支”作为 owner earnings。客户保证金流动、隔离资产和监管资本必须单独处理。
- 2026Q1 经营增长真实存在，但投资收益、减值转回、公允价值与汇兑共同影响利润质量。
- H1预告隐含Q2仍同比增长、但低于Q1；正式中报和净资本恢复是下一关键证据。
- FY、TTM、简单周期正常化 PE 与 P/B-ROE 情景同时保留；没有单点结论。
- 美国 CME / IBKR 只标为 `thematic_peer`，不是同公司或同等经济敞口。

## 数据表

`data/` 保留五年财务、季度/H1、收入与手续费、分部与地域、Q1盈利质量桥、监管资本、完全摊薄股本、PE/PB正常化、owner-earnings敏感性、行业周期、港股通、治理、事件时间轴、真实五日窗口、小盘风险及美国主题映射。

## 方法

按照 Buffett–Munger 公司研究合同：证券身份 → 能力圈 → 商业经济性 → 护城河 → 管理层与资本配置 → owner earnings → 生存能力 → 估值区间 → 反方证据。所有派生值保留期间、币种、范围与公式；找不到的资料保持 unknown。

This package is for evidence review and is not investment advice.
