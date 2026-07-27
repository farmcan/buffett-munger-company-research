# Public company-report template contract

Version: `company-research-publication-v1`

Use this contract for every reader-facing HTML report produced from the
Buffett–Munger company-research workflow. The structured
`seed.stock-fundamentals-valuation.v2` artifact remains authoritative; this
contract controls how the same research is exposed to a reader.

## One mother template, three kinds of slots

Keep the following layers separate:

1. **Fixed publication shell** — visual theme, hero, publication state, status
   legend, navigation, long-term/event entry points, methodology, timeline,
   evidence and source access.
2. **Fixed research spine** — company snapshot, business and profit sources,
   five-year financials, latest interim/quarter, owner earnings or the valid
   sector substitute, capital/per-share bridge, valuation, market-pricing
   state, event monitor, Buffett–Munger interpretation, 25 dimensions,
   50 indicator families, nine gates and invalidation tests.
3. **Industry slots** — the operating KPIs, accounting bridge and valuation
   branch that differ by business model.

Industry differences may change slot contents. They must not create an
independent color theme, status vocabulary, navigation model, evidence
standard, or reading order.

## Canonical assets

- Visual reference: `docs/meitu-01357-hk/report.html`
- Shared visual system: `docs/company-report-theme.css`
- Reusable publication shell:
  `docs/templates/report-publication-shell-v1.html`
- Full placeholder/data contract:
  `docs/templates/report-v2-template.html`
- Executable static gate:
  `scripts/validate_report_template_parity.py`

Set this exact marker on the report body:

```html
<body data-template="company-research-publication-v1">
```

Use the shared stylesheet from a company directory:

```html
<link rel="stylesheet" href="../company-report-theme.css">
```

The Meitu report is the canonical inline-style reference and may retain its
checksum-equivalent inline theme. New reports must use the shared stylesheet.

## Required reader order

The first report sections must expose:

1. `status-legend`;
2. the two reading entries, either as `report-doors` or as adjacent
   `long-term` and `event-monitor` sections;
3. `snapshot` or `summary`.

The full page must then expose these reader jobs through stable anchors:

| Reader job | Accepted anchor |
| --- | --- |
| Status vocabulary | `status-legend` |
| Long-term dossier | `long-term` |
| Near-term monitor | `event-monitor` |
| Current snapshot | `snapshot` or `summary` |
| Five-year financial record | `financials` |
| Latest quarter/interim | `quarter`, `quarterly`, or a disclosed sector equivalent |
| Capital and fully diluted per-share economics | `capital` |
| Dated valuation/market-pricing state | `market-pricing` |
| Buffett–Munger interpretation | `buffett` |
| 25 dimensions, 50 indicators, nine gates | `research-contract`, `audit-matrix`, `dimensions`, or the canonical Meitu coverage matrix |
| Reusable methodology | `methodology` |
| Dated event history | `timeline` |
| Next evidence and invalidation tests | `monitor` |
| Fact-level evidence and sources | `evidence` or `sources` |

Use at least 15 reader sections. A shorter document is a briefing, not the
full company report.

## Required visible research

Do not hide the following solely in JSON:

- the exact meaning of publication, dimension, indicator and gate states;
- all 25 research-dimension results and both indicator-family results for each;
- all nine gate results and their blocking reasons;
- five-year financial history and the latest interim/quarter evidence boundary;
- owner-earnings, net-cash/debt and fully diluted share bridges, or the
  explicitly justified sector substitute;
- dated valuation inputs, denominator matrix and invalidation conditions;
- at least one chart adjacent to the exact table it summarizes;
- fact-level evidence drawers with page/table/line locators where available.

Tables are the auditable record. Charts are an additional reading aid and
never replace their tables.

## Industry slots

### Financial institutions

Replace industrial `CFO - capex` with regulatory capital, client-asset
segregation, parent cash/upstream dividends and distributable-earnings
analysis. Retain ROE/ROTE, capital adequacy, concentration and stress tests.

### Semiconductor foundries and other heavy-capex businesses

Show capacity, utilization, shipment/volume, price or mix, yield where
disclosed, depreciation, maintenance versus growth capex, policy/export
constraints and incremental returns. High utilization is not a moat or owner
earnings.

### Software, SaaS, AI applications and digital-rights infrastructure

Show the disclosed recurring-revenue definition, payer/customer counts,
retention/NRR where available, unit economics, cash conversion, R&D/SBC,
capitalized development, platform dependence, model-cost direction and
substitution risk. Traffic or app rank is a leading signal, not revenue.

## Revision discipline

When rebuilding an existing report:

- preserve every auditable table, chart, evidence ID, source link and caveat
  unless a source-backed correction supersedes it;
- move content into the fixed spine instead of deleting it for visual
  simplicity;
- keep company-specific conclusions and industry KPIs inside the shared shell;
- do not let parallel agents invent separate themes or status systems;
- record any removed content and its reason before publication.

## Publication gates

Run the portable artifact and template validators:

```bash
python \
  skills/research-buffett-munger-company/scripts/validate_company_research.py \
  docs/<company-slug>/combined-artifact.v2.json

python \
  skills/research-buffett-munger-company/scripts/validate_report_template_parity.py \
  docs/<company-slug>/report.html
```

Then inspect the rendered page at desktop width and at 390 CSS pixels:

- no global horizontal overflow;
- navigation links resolve and the navigation itself may scroll horizontally;
- wide tables scroll inside their own containers;
- text and chart labels remain legible;
- no content is clipped or hidden behind navigation;
- the first screen makes the publication state and evidence boundary obvious.

The publication is blocked by a failed static template gate or failed rendered
viewport check, even when the 25/50/9 research validator passes.
