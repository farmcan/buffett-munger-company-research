# Company Research v2 combined artifact contract

版本：2026-07-27

状态：对现有可执行契约的说明，不是第二套 schema

适用对象：`seed.stock-fundamentals-valuation.v2`

## 结论

本目录不新增 `company-research-v2.schema.json`。当前 v2 的权威契约是 Python
validator；另造 JSON Schema 会产生两个无法保证同步的真相来源，尤其容易在 25 个维度、
50 个 indicator family、九道 gate、状态传播和估值公式上漂移。

权威文件按优先级为：

1. [`src/seed/company_research_validation.py`](../../../src/seed/company_research_validation.py)：
   可执行字段、顺序、状态、公式、日期、币种、来源和非建议语言约束；
2. [`skills/research-buffett-munger-company/references/company-research-schema.md`](../../../skills/research-buffett-munger-company/references/company-research-schema.md)：
   combined/split artifact、计算、gate、batch 和 review 的规范说明；
3. [`skills/research-buffett-munger-company/references/methodology-implementation-crosswalk.json`](../../../skills/research-buffett-munger-company/references/methodology-implementation-crosswalk.json)：
   25 个有序维度、50 个有序 indicator family、九道 gate、阶段归属和方法论归因边界；
4. [`skills/research-buffett-munger-company/references/company-research-master-checklist.md`](../../../skills/research-buffett-munger-company/references/company-research-master-checklist.md)：
   人工研究动作和行业分支；
5. [`skills/research-buffett-munger-company/scripts/validate_company_research.py`](../../../skills/research-buffett-munger-company/scripts/validate_company_research.py)：
   combined artifact 的正式验证入口。

最小可通过样例见
[`company-research-v2.example.json`](company-research-v2.example.json)。样例是虚构公司和虚构
来源，只用于字段、状态和公式演示，不得作为公司事实。

## 核心 combined artifact

核心 artifact 保持现有扁平结构，不再套一层 `long_term_dossier`。长期公司档案是以下字段的
逻辑视图：

| 研究需求 | v2 核心字段 |
| --- | --- |
| 证券身份、主体、币种、财年 | `security` |
| 研究日、价格日和价格来源 | `as_of` |
| 公司来源和内容校验和 | `source_refs` |
| 证据边界 | `source_boundaries` |
| 控制权、NCI、A/H/多股类 | `ownership_structure` |
| 多期三表与每股序列 | `financial_history` |
| 分部和业务口径 | `segment_data` |
| 25 个有序研究维度、50 个指标族 | `research_dimensions` |
| 报告利润到研究调整利润 | `earnings_quality_bridge` |
| owner earnings low/high 区间 | `owner_earnings` |
| 再投资、并购、分红、回购、发行、债务 | `capital_allocation` |
| 流动性、杠杆和净现金 | `balance_sheet_quality` |
| FY/TTM/调整后/预测/正常化 PE | `pe_matrix` |
| bear/base/upside EPS | `forward_scenarios` |
| 内在价值敏感性 | `intrinsic_value_scenarios` |
| 护城河正反证据 | `moat_evidence` |
| 独立反方结论 | `red_team` |
| 九道 gate | `gates` |
| 历史估值和价格归因 | `historical_valuation`、`price_move_attribution` |
| 缺口和失效条件 | `source_gaps`、`invalidation_tests` |
| 人工复核门槛 | `review` |
| 非建议边界 | `disclaimer` |

不要新增一个重复的 `long_term_dossier` 后再复制这些字段。重复结构会造成数值、状态和
source refs 的双写冲突。

### 财务、owner earnings、净现金和稀释桥

现有 validator 对下面四类桥的“存在性”和关键计算做不同强度的检查：

- `earnings_quality_bridge`：核心必填对象，但内部行结构目前由研究和 split fact-pack
  契约约束；
- `owner_earnings`：validator 强制 `calculated/unavailable`、币种一致、至少两个有公式的
  low-to-high 数值，以及明确限制；
- `balance_sheet_quality`：核心必填对象；可在内部保存 `net_cash_bridge`，但
  combined validator 尚未逐项验证现金、受限现金、投资、债务、租赁和可转债加总；
- `ownership_structure`：核心必填对象；可在内部保存
  `fully_diluted_share_bridge`，但最终股数、可转债双情景和库存股处理仍应由 fact-pack、
  valuation 和人工复核交叉验证。

因此，嵌套 bridge 可以用于公开可读性，但不能因为 combined validator 通过就宣称桥已被
production QA。正式事实仍绑定 split artifacts 的 checksum 和页级证据。

## 25 个维度、50 个 indicator family

`research_dimensions` 必须严格按 validator 中的固定顺序包含 25 行；每行必须严格包含
crosswalk 中的两项 indicator，共 50 项。不得排序、去重、合并或用一个“已阅读年报”占位。

状态传播规则：

- indicator 为 `observed`：必须绑定直接公司证据；
- indicator 为 `not_disclosed`：必须有 source gap，父维度必须是 `unknown`；
- indicator 为 `conflicting`：必须同时保留来源和冲突缺口，父维度必须是 `conflicting`；
- indicator 为 `not_applicable`：必须有理由；整行不适用时两项指标都要不适用；
- 任一维度 `unknown/conflicting`，其映射 gate 不能使用正向结果；
- 最终 decision gate 在任何维度未解决时不能是 readiness 或其他正向状态。

这里的 50 项只是最低问题覆盖，不替代五年序列、行业专用事实、客户/供应商交叉验证或
页级证据。

## 九道 gate

`gates` 必须严格按以下顺序出现：

1. `identity_and_source_integrity`
2. `circle_of_competence`
3. `business_economics`
4. `durable_moat`
5. `management_and_capital_allocation`
6. `owner_earnings`
7. `survival_and_balance_sheet`
8. `intrinsic_value_and_margin_of_safety`
9. `decision_and_disconfirming_evidence`

不得加权汇总。前一道 gate 的 `fail/outside_circle/blocked` 不能被后续好结果抵消。

## 页级 evidence anchor 不放入核心 contract

核心 `source_refs` 是 source-level provenance，强制 URL、来源层级、发布日期状态、访问日、
期间、审计状态、scope、covers 和 `content_sha256`。它并不保证每个数字都有页码、原文、
单位和公式。

production 页级证据应保存在 checksum 绑定的 split artifact：

- `filing-document-manifest`
- `filing-fact-pack`
- `filing-fact-pack-review`
- `company-industry-fact-sidecar`
- `red-team`
- `valuation`
- `review`

公开 HTML 的证据抽屉统一使用现有 `evidence-index.json` 契约，不新增 presentation
sidecar schema。权威实现是
[`skills/research-buffett-munger-company/scripts/validate_company_research_publication.py`](../../../skills/research-buffett-munger-company/scripts/validate_company_research_publication.py)。
`evidence-index.json` 使用
`schema_version: seed.company-research-evidence-index.v1`、顶层 `anchors`，并绑定固定文件名
`combined-artifact.v2.json` 的 SHA-256。每个 anchor 至少记录：

```json
{
  "schema_version": "seed.company-research-evidence-index.v1",
  "combined_artifact": {
    "path": "combined-artifact.v2.json",
    "sha256": "<64 hex>"
  },
  "anchors": [
    {
      "id": "FY2025:revenue",
      "claim_id": "long-term:FY2025:revenue",
      "source_id": "annual-report-2025",
      "document_sha256": "<64 hex>",
      "page": 123,
      "source_text": "Revenue ...",
      "period": "FY2025",
      "unit": "CNY million",
      "currency": "CNY",
      "scope": "consolidated_group",
      "audit_status": "audited",
      "formula": null
    }
  ]
}
```

`source-ledger.json` 中相同 `source_id` 的 `content_sha256` 或 `snapshot_sha256` 必须与 anchor
一致。公开页至少保留 `long-term`、`event-monitor` 和 `market-pricing` 三个 HTML anchor，
表格、SVG 图、`<details>` 证据抽屉和 `data-evidence-id`。evidence index 只增强展示和审计
导航，不能覆盖 fact-pack 或改变 combined artifact 的 gate 状态。

## 短期事件监控和 `market_pricing_state`

长期研究与短期事件监控应是两个产品面。核心 combined artifact 只保留当期摘要：

- `price_move_attribution`
- `historical_valuation`
- `source_gaps`
- `invalidation_tests`

更高频、容易过期的内容放 HTML/CSV 展示层，并记录数据快照日、来源和所消费的
`combined-artifact.v2.json` SHA-256：

```text
short_term_monitor
  -> monitor_as_of / stale_after
  -> completed / confirmed / TBA events
  -> T-1 / T0 / T+1 / T+5 / benchmark / excess return
  -> sector and global lead-lag
  -> overlapping events and causal confidence
  -> small-cap / liquidity / index / Stock Connect structure risks

market_pricing_state
  -> historical_valuation_percentile
  -> price_to_intrinsic_value_gap by scenario
  -> peer_premium_or_discount on a common denominator
  -> long_term_price_state
  -> formulas, as-of dates, evidence anchors and limitations
```

`market_pricing_state` 不是 v2 combined artifact 的新核心字段，也不是“便宜/贵”的主观标签。
每一项必须绑定同日价格、同币种分母、无前视偏差的历史估值、同行可比范围和内在价值情景。
它不能改写九道 gate，也不能输出买卖、仓位或行动时点措辞。

## Validator、人工复核与发布

运行：

```bash
PYTHONPATH=src python3 \
  skills/research-buffett-munger-company/scripts/validate_company_research.py \
  docs/company-research/templates/company-research-v2.example.json
```

validator 通过只说明 combined contract 和确定性公式检查通过，不等于事实已人工复核。

推荐 canonical 状态链：

```text
source_partial
  -> research_in_progress
  -> needs_red_team
  -> needs_human_review
  -> production_reviewed
```

`needs_more_evidence` 可以是报告中的读者展示标签，但不是当前
`company-research-schema.md` 的 canonical artifact status；落盘时应映射为
`source_partial`、`research_in_progress` 或更具体的 filing readiness 状态。

`review` 至少保留：

- `human_review_required`
- `status`
- `reviewer`
- `reviewed_at`
- `critical_gaps`
- fact-pack/review/valuation/red-team 的路径和 SHA-256
- publication decision 与 scope

`production_reviewed` 只能由具名人工复核设置。HTML 发布还要单独完成：

- 事实可公开性；
- 原文版权和数据许可；
- 私有路径/仓位/成本泄漏检查；
- 禁用投资指令语言检查；
- stale date 与 change log；
- `reviewed_for_publication: true`。

## 样例边界

`company-research-v2.example.json`：

- 通过当前可执行 validator；
- 完整包含 25 个维度、50 个 indicator family 和九道 gate；
- 展示三期财务加最新中期、利润桥、owner earnings、净现金、完全稀释股本和估值矩阵；
- 仍保持 `needs_human_review`；
- 使用虚构公司、虚构 URL 和虚构校验和；
- 不代表 split fact-pack、公开 `evidence-index.json`、独立 red-team 或人工发布复核已经完成。
