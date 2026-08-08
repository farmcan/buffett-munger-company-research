#!/usr/bin/env python3
"""Build one embedded event-surprise terminal for each public company report."""

from __future__ import annotations

import argparse
import csv
import json
import re
import urllib.request
from datetime import date
from html import escape
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
DOCS = HERE.parent
AS_OF = "2026-07-30T18:00:00+08:00"
START = "2024-10-01"
END = "2026-10-15"

COMPANIES = {
    "horizon": {
        "name": "地平线机器人",
        "ticker": "09660.HK",
        "slug": "horizon-robotics-09660-hk",
        "market": "HKEX",
        "bucket": "智能驾驶 / 边缘 AI",
        "color": "#c14f3c",
    },
    "meitu": {
        "name": "美图公司",
        "ticker": "01357.HK",
        "slug": "meitu-01357-hk",
        "market": "HKEX",
        "bucket": "AI 应用 / 创意软件",
        "color": "#176b50",
    },
    "nanhua": {
        "name": "南华期货",
        "ticker": "02691.HK",
        "slug": "nanhua-futures-02691-hk",
        "market": "HKEX / SSE",
        "bucket": "期货金融 / 跨境",
        "color": "#a66f16",
    },
    "smic": {
        "name": "中芯国际",
        "ticker": "00981.HK",
        "slug": "smic-00981-hk",
        "market": "HKEX / STAR",
        "bucket": "晶圆代工 / 半导体",
        "color": "#386a8e",
    },
    "vobile": {
        "name": "阜博集团",
        "ticker": "03738.HK",
        "slug": "fubo-group-03738-hk",
        "market": "HKEX",
        "bucket": "内容科技 / AI 版权",
        "color": "#8b5a91",
    },
    "xpeng": {
        "name": "小鹏汽车",
        "ticker": "09868.HK / XPEV",
        "slug": "xpeng-09868-hk",
        "market": "HKEX / NYSE",
        "bucket": "智能电动车 / 物理 AI",
        "color": "#215f59",
    },
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def find_row(rows: list[dict[str, str]], event_date: str) -> dict[str, str] | None:
    for row in rows:
        date_value = (
            row.get("event_date")
            or row.get("announcement_date")
            or row.get("date")
            or row.get("disclosure_date")
        )
        if date_value == event_date:
            return row
    return None


def number(value: str | None) -> float | None:
    if value in (None, ""):
        return None
    return float(value)


def fmt_pct(value: str | None) -> str:
    parsed = number(value)
    return "待补" if parsed is None else f"{parsed:+.2f}%"


def resonance(value: float | None) -> str:
    if value is None:
        return "pending"
    if value >= 3:
        return "positive_resonance"
    if value <= -3:
        return "negative_resonance"
    return "mixed_or_neutral"


def load_reactions() -> dict[str, list[dict[str, str]]]:
    return {
        "meitu": read_csv(DOCS / "meitu-01357-hk/data/event-price-reactions.csv"),
        "nanhua": read_csv(DOCS / "nanhua-futures-02691-hk/data/event-price-windows.csv"),
        "smic": read_csv(DOCS / "smic-00981-hk/data/event-price-reactions.csv"),
        "vobile": read_csv(DOCS / "fubo-group-03738-hk/data/event-price-reactions.csv"),
        "xpeng": read_csv(DOCS / "xpeng-09868-hk/data/event-price-reactions.csv"),
    }


def reaction_for(
    company: str,
    event_date: str,
    reactions: dict[str, list[dict[str, str]]],
) -> dict[str, Any]:
    rows = reactions.get(company, [])
    if company == "nanhua":
        nanhua_event_names = {
            "2025-12-22": "IPO",
            "2026-01-16": "Stock Connect inclusion",
            "2026-03-27": "Annual results and governance package",
            "2026-04-01": "Regulatory warning",
            "2026-04-21": "2026Q1 report",
            "2026-06-24": "H-share repurchase plan",
            "2026-07-07": "2026H1 profit alert",
            "2026-07-16": "EGM repurchase approval",
        }
        event_name = nanhua_event_names.get(event_date)
        row = next((item for item in rows if item.get("event") == event_name), None)
    else:
        row = find_row(rows, event_date)
    if not row:
        return {
            "intraday": None,
            "t1": None,
            "t5": None,
            "t20": None,
            "benchmark": None,
            "benchmark_adjusted": None,
            "volume_ratio": None,
            "resonance": "pending",
            "source_refs": [],
        }
    if company == "meitu":
        window = number(row.get("t_minus_1_to_t_plus_5_pct"))
        return {
            "intraday": (
                f"T−1 HK${row['t_minus_1_close_hkd']} → "
                f"T0 HK${row['t0_close_hkd']}"
            ),
            "t1": None,
            "t5": (
                f"T−1→T+5 {fmt_pct(row.get('t_minus_1_to_t_plus_5_pct'))}；"
                f"T0→T+5 {fmt_pct(row.get('t0_to_t_plus_5_pct'))}"
            ),
            "t20": None,
            "benchmark": "HSTECH",
            "benchmark_adjusted": (
                f"同窗 HSTECH {fmt_pct(row.get('hstech_same_window_pct'))}；"
                f"超额 {fmt_pct(row.get('abnormal_vs_hstech_pct'))}"
            ),
            "volume_ratio": None,
            "resonance": resonance(window),
            "source_refs": ["meitu-P01"],
            "attribution_confidence": row.get("attribution_confidence"),
            "limitations": row.get("overlap_note"),
        }
    if company == "nanhua":
        window = number(row.get("tminus1_to_t5_pct"))
        return {
            "intraday": f"T0 {fmt_pct(row.get('t0_return_pct'))}",
            "t1": None,
            "t5": f"T−1→T+5 {fmt_pct(row.get('tminus1_to_t5_pct'))}",
            "t20": None,
            "benchmark": None,
            "benchmark_adjusted": None,
            "volume_ratio": (
                f"{float(row['volume_ratio']):.2f}×"
                if row.get("volume_ratio")
                else None
            ),
            "resonance": resonance(window),
            "source_refs": ["nanhua-P01"],
            "limitations": row.get("adjustment_note"),
        }
    if company == "smic":
        window = number(row.get("t_plus_5_pct"))
        return {
            "intraday": f"首个反应日 {fmt_pct(row.get('first_reaction_pct'))}",
            "t1": None,
            "t5": fmt_pct(row.get("t_plus_5_pct")),
            "t20": None,
            "benchmark": "HSTECH",
            "benchmark_adjusted": f"T+5超额 {fmt_pct(row.get('t_plus_5_excess_pct'))}",
            "volume_ratio": None,
            "resonance": resonance(window),
            "source_refs": ["smic-P_H", "shared-hstech"],
            "limitations": row.get("interpretation"),
        }
    if company == "vobile":
        window = number(row.get("t5_return_pct"))
        return {
            "intraday": f"T0 {fmt_pct(row.get('t0_return_pct'))}",
            "t1": fmt_pct(row.get("t1_return_pct")),
            "t5": fmt_pct(row.get("t5_return_pct")),
            "t20": None,
            "benchmark": "HSI",
            "benchmark_adjusted": f"T0超额 {fmt_pct(row.get('t0_excess_vs_hsi_pct'))}",
            "volume_ratio": None,
            "resonance": resonance(window),
            "source_refs": ["vobile-M01", "vobile-M02"],
            "attribution_confidence": row.get("causal_confidence"),
            "limitations": row.get("limitations"),
        }
    window = number(row.get("t5_pct"))
    return {
        "intraday": f"T0 {fmt_pct(row.get('t0_pct'))}",
        "t1": None,
        "t5": fmt_pct(row.get("t5_pct")),
        "t20": fmt_pct(row.get("t20_pct")),
        "benchmark": "HSTECH",
        "benchmark_adjusted": f"T+5超额 {fmt_pct(row.get('t5_excess_hstech_pct'))}",
        "volume_ratio": None,
        "resonance": resonance(window),
        "source_refs": ["xpeng-M01", "xpeng-M03"],
        "attribution_confidence": row.get("causal_confidence"),
        "limitations": "事件窗口是相关性观察，不证明单一公告造成全部涨跌。",
    }


def source_refs() -> list[dict[str, Any]]:
    selected = {
        "horizon": ["H01", "H03", "H04", "H05", "H06", "M02"],
        "meitu": [
            "F01",
            "F03",
            "F04",
            "F05",
            "F08",
            "F14",
            "F16",
            "M02",
            "P01",
            "P03",
            "R05",
            "T10",
        ],
        "nanhua": ["F01", "F02", "F03", "F04", "F05", "F06", "F09", "F11", "P01"],
        "smic": [
            "Q2_2025",
            "Q3_2025",
            "Q4_2025",
            "Q1_2026",
            "SMNC_BOOK",
            "TSMC_Q2",
            "P_H",
            "P_HSTECH",
        ],
        "vobile": ["F01", "F02", "F03", "F04", "F05", "H01", "M01", "M02"],
        "xpeng": [
            "F01",
            "F03",
            "F04",
            "F08",
            "F09",
            "F10",
            "F11",
            "F12",
            "F13",
            "F14",
            "M01",
            "M03",
        ],
    }
    refs: list[dict[str, Any]] = []
    market_ids = {
        "horizon": {"M02"},
        "meitu": {"P01", "P03"},
        "nanhua": {"P01"},
        "smic": {"P_H", "P_HSTECH"},
        "vobile": {"M01", "M02"},
        "xpeng": {"M01", "M03"},
    }
    for key, ids in selected.items():
        company = COMPANIES[key]
        ledger_path = DOCS / company["slug"] / "source-ledger.json"
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        by_id = {
            (item.get("id") or item.get("source_id")): item
            for item in ledger.get("sources", [])
        }
        for source_id in ids:
            item = by_id[source_id]
            kind = str(item.get("kind") or "").lower()
            if source_id in market_ids[key] or "market" in kind:
                tier = "market_data"
            elif "management" in kind:
                tier = "company_claim"
            else:
                tier = "primary"
            refs.append(
                {
                    "id": f"{key}-{source_id}",
                    "title": (
                        f"{company['name']}｜"
                        f"{item.get('title') or item.get('name') or source_id}"
                    ),
                    "tier": tier,
                    "url": item.get("url") or item.get("original_url"),
                    "accessed_at": (
                        item.get("accessed_at")
                        or item.get("accessed_date")
                        or (
                            item.get("retrieved_at")
                            if key == "xpeng"
                            or (key == "meitu" and source_id in {"F16", "P03"})
                            else None
                        )
                        or "2026-07-29"
                    ),
                }
            )
    hstech = next(ref for ref in refs if ref["id"] == "smic-P_HSTECH")
    refs.append(
        {
            **hstech,
            "id": "shared-hstech",
            "title": "恒生科技指数日线｜共享风险偏好代理，不是六家公司共同业绩基准",
        }
    )
    return refs


def no_baseline(reason: str) -> dict[str, Any]:
    return {
        "direction": "not_comparable",
        "raw": None,
        "percent": None,
        "score": None,
        "method": "not_comparable_without_frozen_expectation",
        "confidence": "high",
        "reason": reason,
        "source_refs": [],
    }


def completed_event(
    company_key: str,
    event_id: str,
    event_date: str,
    title: str,
    event_type: str,
    source_ids: list[str],
    actual_metrics: list[str],
    why: str,
    transmission: list[str],
    next_check: str,
    reactions: dict[str, list[dict[str, str]]],
    *,
    importance: str = "high",
    impact: int = 4,
    expectation: Any = None,
    surprise: dict[str, Any] | None = None,
    review: str,
    source_gap: str,
    reaction_date: str | None = None,
    manual_reaction: dict[str, Any] | None = None,
    reported_at: str | None = None,
    event_time: str | None = None,
    beijing_time: str | None = None,
    definition_changes: list[str] | None = None,
    expectation_baseline: str | None = None,
    validation_status: str | None = None,
) -> dict[str, Any]:
    company = COMPANIES[company_key]
    prefixed = [f"{company_key}-{source_id}" for source_id in source_ids]
    market = manual_reaction or reaction_for(
        company_key, reaction_date or event_date, reactions
    )
    resolved_validation_status = validation_status or (
        "market_reviewed"
        if market.get("resonance") != "pending"
        else "actual_reported"
    )
    return {
        "event_id": event_id,
        "date": event_date,
        "time": event_time,
        "event_timezone": "Asia/Shanghai",
        "beijing_time": beijing_time or event_date,
        "date_status": "completed",
        "event_type": event_type,
        "company": f"{company['name']}｜{title}",
        "ticker": company["ticker"],
        "market": company["market"],
        "chain_bucket": company["bucket"],
        "importance": importance,
        "impact_score": impact,
        "why_it_matters": why,
        "expectation_snapshot": expectation,
        "expectation_baseline": expectation_baseline or (
            None
            if expectation
            else "没有可审计、事前冻结的一致预期；不做事后 surprise 打分。"
        ),
        "actual_results": {
            "reported_at": reported_at or f"{event_date}T18:00:00+08:00",
            "metrics": actual_metrics,
            "definition_changes": definition_changes or [],
            "source_refs": prefixed,
        },
        "surprise": surprise or no_baseline(
            "有实际披露，但没有在事件发生前冻结的可比共识或官方指引。同比增长不等于预期差。"
        ),
        "market_reaction": market,
        "transmission_paths": transmission,
        "holdings_impacted": [
            f"研究主体：{company['name']}（{company['ticker']}）",
            "跨公司读取只作行业或风险偏好映射，不把主题相近写成经济等价。",
        ],
        "validation": {
            "status": resolved_validation_status,
            "next_check_at": next_check,
            "thesis_impact": review,
            "review_score": None,
        },
        "post_event_review": review,
        "source_refs": prefixed + market.get("source_refs", []),
        "source_gap": source_gap,
    }


def scheduled_event(
    company_key: str,
    event_id: str,
    event_date: str | None,
    title: str,
    source_ids: list[str],
    why: str,
    questions: list[str],
    *,
    date_status: str = "confirmed",
    timeline_anchor_date: str | None = None,
    beijing_time: str | None = None,
    official_guidance: list[str] | None = None,
    previous_actual: list[str] | None = None,
    transmission_paths: list[str] | None = None,
    next_check_at: str | None = None,
    source_gap: str | None = None,
    frozen_at: str | None = None,
) -> dict[str, Any]:
    company = COMPANIES[company_key]
    prefixed = [f"{company_key}-{source_id}" for source_id in source_ids]
    axis_anchor = timeline_anchor_date or event_date
    if axis_anchor is None:
        raise ValueError(f"{event_id} requires a timeline anchor")
    return {
        "event_id": event_id,
        "date": event_date,
        "timeline_anchor_date": axis_anchor,
        "time": None,
        "event_timezone": "Asia/Shanghai",
        "beijing_time": beijing_time or event_date or "TBA",
        "date_status": date_status,
        "event_type": "future_validation",
        "company": f"{company['name']}｜{title}",
        "ticker": company["ticker"],
        "market": company["market"],
        "chain_bucket": company["bucket"],
        "importance": "high",
        "impact_score": 5,
        "why_it_matters": why,
        "expectation_snapshot": {
            "frozen_at": frozen_at or AS_OF,
            "official_guidance": official_guidance or [],
            "consensus": [],
            "previous_actual": previous_actual or [],
            "source_refs": prefixed,
        },
        "actual_results": None,
        "surprise": {
            "direction": "pending",
            "raw": None,
            "percent": None,
            "score": None,
            "method": "pending",
            "confidence": "pending",
            "reason": "事件尚未发生，不预填方向。",
            "source_refs": prefixed,
        },
        "market_reaction": {
            "intraday": None,
            "t1": None,
            "t5": None,
            "t20": None,
            "benchmark": None,
            "benchmark_adjusted": None,
            "volume_ratio": None,
            "resonance": "pending",
            "source_refs": [],
        },
        "transmission_paths": transmission_paths
        or [
            "官方披露 → 核对口径与前期基线 → 计算实际变化 → 再观察价格与成交量共振"
        ],
        "holdings_impacted": [f"研究主体：{company['name']}（{company['ticker']}）"],
        "validation": {
            "status": "expectation_frozen",
            "next_check_at": next_check_at or axis_anchor,
            "thesis_impact": "pending",
            "review_score": None,
        },
        "pre_event_questions": questions,
        "post_event_review": None,
        "source_refs": prefixed,
        "source_gap": source_gap
        or "未来实际、T+1/T+5/T+20和成交量只能在事件后追加。",
    }


def build_events(reactions: dict[str, list[dict[str, str]]]) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    add = events.append

    add(
        completed_event(
            "horizon",
            "horizon-ipo-2024",
            "2024-10-24",
            "港交所上市",
            "listing",
            ["H01"],
            ["09660.HK开始交易", "上市后才形成可观察的公开价格与流通历史"],
            "上市建立价格发现，但短交易历史不支持无前视偏差的长期估值分位。",
            ["公开上市 → 流通供给/定价", "后续融资与奖励 → 完全摊薄每股经济"],
            "首份完整年报、自由流通量与后续稀释",
            reactions,
            manual_reaction={
                "intraday": "IPO没有可比T−1收盘",
                "t1": None,
                "t5": None,
                "t20": None,
                "benchmark": None,
                "benchmark_adjusted": None,
                "volume_ratio": None,
                "resonance": "not_comparable",
                "source_refs": ["horizon-M02"],
                "limitations": "上市首日无法使用常规T−1事件窗。",
            },
            review="上市价格只是起点，长期价值需由收入、现金与稀释后的每股经济验证。",
            source_gap="上市前没有同证券连续行情，无法计算常规事件窗。",
        )
    )
    add(
        completed_event(
            "meitu",
            "meitu-deepseek-cost-shock-2025",
            "2025-01-27",
            "DeepSeek与开源模型成本冲击",
            "industry_model",
            ["T10"],
            ["低成本/开源模型冲击扩散至中国AI应用叙事", "这是行业事件，不是美图单一公告"],
            "模型降价既可能降低推理成本，也可能强化模型厂商直接包住应用的替代风险。",
            ["模型成本下降 → AI功能毛利/试用增加", "模型能力上升 → 原生平台替代独立应用"],
            "付费转化、毛利和模型厂商直接产品边界",
            reactions,
            review="T−1到T+5上涨45.1%，但属于宽行业叙事，不能作为单一公司因果证明。",
            source_gap="多个AI催化剂同时发生，缺少可隔离的公司特定信息。",
        )
    )
    add(
        completed_event(
            "meitu",
            "meitu-alibaba-cb-2025",
            "2025-05-21",
            "阿里可转债与战略合作",
            "capital_strategy",
            ["F14"],
            ["阿里认购US$250m可转债", "初始转股价HK$6.00", "同时披露战略合作"],
            "资本、分发和模型合作可同时改变小盘AI应用公司的估值叙事，但债务与稀释必须分别建模。",
            ["平台合作 → 分发/模型调用 → 付费转化与推理成本", "可转债 → 现金缓冲或转股稀释"],
            "中报核对商业贡献、净现金和全摊薄股数",
            reactions,
            review="首日重估明显，五日回吐；合作标题不能代替收入和每股现金验证。",
            source_gap="合作收入、模型调用成本和渠道转化未单独披露。",
        )
    )
    add(
        completed_event(
            "vobile",
            "vobile-h1-2025",
            "2025-08-28",
            "2025H1业绩",
            "earnings_release",
            ["F02"],
            ["收入HK$1,456.3m", "订阅收入HK$609.9m", "增值服务HK$846.4m", "归母利润HK$102.3m"],
            "验证订阅和内容变现双引擎是否同时增长，以及利润能否转为现金。",
            ["平台内容量 → 指纹/权利识别 → 订阅与分成收入 → 回款"],
            "2025全年与2026Q1经营更新",
            reactions,
            review="T0上涨但T+5转弱，表明财报后仍需验证现金和可转债供给。",
            source_gap="没有冻结的卖方共识和历史surprise分布。",
        )
    )
    add(
        completed_event(
            "smic",
            "smic-q2-2025",
            "2025-08-07",
            "2025Q2业绩",
            "earnings_release",
            ["Q2_2025"],
            ["收入US$2.209bn", "环比-1.7%", "毛利率20.4%", "产能利用率92.5%"],
            "利用率、ASP、毛利率和资本开支是晶圆代工周期比单一收入增长更早的验证变量。",
            ["国内晶圆需求 → 利用率/ASP → 毛利率 → 折旧吸收与FCF"],
            "2025Q3实际",
            reactions,
            review="经营数据进入上行段，但没有保存事前一致预期，不能追溯打分。",
            source_gap="该公开包没有冻结2025Q2发布前的市场共识。",
        )
    )
    add(
        completed_event(
            "xpeng",
            "xpeng-q2-2025",
            "2025-08-19",
            "2025Q2业绩",
            "earnings_release",
            ["F08", "F09"],
            [
                "交付103,181辆",
                "收入RMB18.27bn",
                "毛利率17.3%",
                "vehicle margin 14.3%",
                "净亏损RMB0.48bn",
                "现金类资产RMB47.57bn",
            ],
            "这是产品周期、毛利修复和亏损收窄同步改善的历史参照点，但发布后五日涨幅被后续增持事件显著污染。",
            ["车型换代 → 交付/ASP → vehicle margin → 费用杠杆 → CFO"],
            "2025Q3实际",
            reactions,
            expectation={
                "frozen_at": "2025-05-21T20:00:00+08:00",
                "official_guidance": [
                    "Q2交付102,000至108,000辆",
                    "Q2收入RMB17.5bn至18.7bn",
                ],
                "consensus": [],
                "previous_actual": [
                    "2025Q1收入RMB15.81bn",
                    "2025Q1 vehicle margin 10.5%",
                    "2025Q1净亏损RMB0.66bn",
                ],
                "source_refs": ["xpeng-F08"],
            },
            surprise={
                "direction": "neutral_on_guided_metrics",
                "raw": "交付103,181辆、收入RMB18.27bn，均在官方指引区间内",
                "percent": "交付较指引中点-1.7%；收入较指引中点+0.9%",
                "score": 0,
                "method": "actual_vs_frozen_official_guidance",
                "confidence": "high",
                "reason": (
                    "交付和收入都只是符合官方指引；vehicle margin环比+3.8个百分点、"
                    "亏损环比收窄28.1%是质量亮点，但没有冻结共识，不能量化成市场surprise。"
                ),
                "source_refs": ["xpeng-F08", "xpeng-F09"],
            },
            manual_reaction={
                "intraday": "T0 -1.85%",
                "t1": "T−1→T+1 +2.48%",
                "t5": "T−1→T+5 +19.94%（含8月21日创始人增持事件）",
                "t20": "+6.11%",
                "benchmark": "HSTECH",
                "benchmark_adjusted": "T+5超额 +16.30%，不可归因于财报单一事件",
                "volume_ratio": None,
                "resonance": "positive_resonance",
                "source_refs": ["xpeng-M01", "xpeng-M03", "xpeng-F10"],
                "attribution_confidence": "low",
                "limitations": "财报后窗口与创始人增持及新P7发布预期重叠。",
            },
            review=(
                "财报当日跌1.85%；窗口内最大单日上涨发生在增持披露后的8月22日。"
                "因此原T+5 +19.94%只能定义为事件簇结果，不能写成Q2财报大超预期。"
            ),
            source_gap="没有冻结卖方一致预期；毛利与亏损改善只能作为结果亮点，不能事后制造surprise分数。",
        )
    )
    add(
        completed_event(
            "xpeng",
            "xpeng-founder-purchase-2025",
            "2025-08-21",
            "何小鹏增持3.1m股",
            "insider_action",
            ["F10"],
            [
                "何小鹏通过全资实体在8月20日至21日买入3.1m股A类普通股",
                "平均价HK$80.49",
                "成交金额约HK$249.5m",
                "增持后披露经济权益约18.9%",
            ],
            "这是2025Q2财报窗口内最清晰的新增催化；它能验证真金白银投入，但不能替代后续经营结果。",
            [
                "内部人现金买入 → 信心信号与流通需求 → 短线重估",
                "后续经营兑现/不兑现 → 信号持续或衰减",
            ],
            "后续交付、毛利、现金与是否继续增持",
            reactions,
            manual_reaction={
                "intraday": "首个反应日8月22日 +13.60%（HK$80.90→HK$91.90）",
                "t1": "T−1→T+1 +13.10%",
                "t5": "T−1→T+5 +3.71%",
                "t20": "+4.02%",
                "benchmark": "HSTECH",
                "benchmark_adjusted": "T+5 HSTECH +3.20%；超额仅+0.51%",
                "volume_ratio": "首个反应日约3.92×此前20日均量",
                "resonance": "positive_resonance",
                "source_refs": ["xpeng-M01", "xpeng-M03"],
                "attribution_confidence": "medium",
                "limitations": "T0冲击清晰，但T+5已回吐大部分超额，且新P7发布预期重叠。",
            },
            review=(
                "短线最强冲击更接近创始人增持，而不是8月19日财报；"
                "但五日后相对HSTECH只剩约0.5个百分点超额，说明信心交易并未形成持续趋势。"
            ),
            source_gap="无法识别全部买盘来源，也不能由一次增持推断未来业绩或后续继续买入。",
        )
    )
    add(
        completed_event(
            "xpeng",
            "xpeng-next-p7-launch-2025",
            "2025-08-27",
            "全新P7发布",
            "product_launch",
            ["F11"],
            ["8月27日正式发布全新P7", "8月28日开始全国交付"],
            "它是财报后产品周期叙事的下一兑现点，也构成增持后价格窗口的重叠事件。",
            [
                "新品发布/价格 → 订单 → 交付与车型结构 → ASP/vehicle margin",
                "预期提前交易 → 发布日兑现 → 价格回吐风险",
            ],
            "P7订单、9月量产爬坡与车型毛利",
            reactions,
            manual_reaction={
                "intraday": "同日收盘T0 -1.75%",
                "t1": "T−1→T+1 -9.82%",
                "t5": "T−1→T+5 -16.14%",
                "t20": "-11.52%",
                "benchmark": "HSTECH",
                "benchmark_adjusted": "T+5 HSTECH -1.70%；超额 -14.44%",
                "volume_ratio": "T0约0.94×此前20日均量",
                "resonance": "negative_resonance",
                "source_refs": ["xpeng-M01", "xpeng-M03"],
                "attribution_confidence": "low",
                "limitations": "发布会具体时点未冻结，且财报、增持和大盘风险偏好仍在同一窗口。",
            },
            review=(
                "新P7发布后五日显著回吐，符合‘预期先交易、落地后再验证订单与毛利’的模式；"
                "它进一步证明财报T+5不能被当作单一事件收益。"
            ),
            source_gap="没有冻结发布前订单共识、车型毛利和发布会精确市场时点。",
        )
    )
    add(
        completed_event(
            "vobile",
            "vobile-cb-proposal-2025",
            "2025-09-23",
            "HK$16亿零息可转债方案",
            "financing",
            ["F04"],
            ["建议发行HK$1.6bn零息可转债", "2026年到期", "形成偿债、回购或转股三分支"],
            "短期限融资会直接影响净债务、流通供给和每股价值，不能只看票息为零。",
            ["现金融资 → 投资/营运资金", "到期前 → 回购/赎回/转股 → 股本或现金变化"],
            "月报、回购公告与到期处理",
            reactions,
            review="市场短窗正向，但真正关键是资金用途、到期现金和充分摊薄分母。",
            source_gap="债券持有人对冲与实际借券结构不可得。",
        )
    )
    add(
        completed_event(
            "vobile",
            "vobile-cb-completion-2025",
            "2025-09-29",
            "可转债发行完成",
            "financing",
            ["F04", "H01"],
            ["HK$1.6bn可转债发行完成", "转股或现金偿还风险开始进入存续期"],
            "发行完成把融资方案变成真实资本结构，后续回购不等于风险消失。",
            ["债券存续 → 转股价/股价/现金 → 潜在供给或偿债压力"],
            "2026到期前现金、回购和转换状态",
            reactions,
            reaction_date="2025-09-29",
            review="T0与T+5正共振，但资本结构风险需要用月报持续更新。",
            source_gap="公开事件窗不能识别套利盘和方向性资金。",
        )
    )
    add(
        completed_event(
            "smic",
            "smic-q3-2025",
            "2025-11-13",
            "2025Q3业绩",
            "earnings_release",
            ["Q3_2025"],
            ["收入US$2.382bn", "环比+7.8%", "毛利率22.0%", "产能利用率95.8%"],
            "利用率升至接近满载后，下一变量从数量转向ASP、产品组合和扩产回报。",
            ["利用率上升 → 折旧吸收改善", "接近满载 → 扩产/瓶颈 → 资本开支与回报压力"],
            "2025Q4实际",
            reactions,
            review="基本面继续改善，但事件层未冻结共识，保持不可比状态。",
            source_gap="缺少发布前官方指引和一致预期的结构化快照。",
        )
    )
    add(
        completed_event(
            "xpeng",
            "xpeng-q3-2025",
            "2025-11-17",
            "2025Q3业绩",
            "earnings_release",
            ["F01"],
            [
                "交付116,007辆",
                "收入RMB20.38bn",
                "毛利率20.1%",
                "vehicle margin 13.1%",
                "净亏损RMB0.38bn",
            ],
            "收入和毛利继续改善，但事件后股价可以因估值、指引和产品预期转弱。",
            ["交付增长 → 毛利/亏损", "指引与产品预期 → 估值再定价"],
            "2025Q4实际与首次季度盈利持续性",
            reactions,
            review="T+5和T+20均弱，典型说明“业绩仍增”不等于增速预期继续上修。",
            source_gap="没有逐项保存发布前市场预期，无法定位哪一个分项触发重估。",
        )
    )
    add(
        completed_event(
            "smic",
            "smic-q4-2025",
            "2026-02-10",
            "2025Q4业绩",
            "earnings_release",
            ["Q4_2025"],
            ["收入US$2.489bn", "环比+4.5%", "毛利率19.2%", "产能利用率95.7%"],
            "收入和利用率保持强势但毛利率回落，提示扩产、折旧与产品组合的压力。",
            ["高利用率 → 收入韧性", "毛利率回落 → 成本/折旧/组合压力"],
            "2025年报与2026Q1实际",
            reactions,
            review="周期景气不能只看收入；毛利率是重要反证。",
            source_gap="缺少该季度可复核事件价格窗与冻结预期。",
        )
    )
    add(
        completed_event(
            "horizon",
            "horizon-drobotics-deconsolidation",
            "2026-03-31",
            "D-Robotics出表",
            "accounting_scope",
            ["H01"],
            ["自2026-03-31起终止合并并列作终止经营", "仍为最大单一股东并改用权益法"],
            "合并口径改善不等于经济风险消失，必须把报表变化和真实现金/权益风险分开。",
            ["出表 → 收入/亏损口径变化", "权益法与承诺 → 经济风险继续存在"],
            "2026H1持续经营与终止经营桥",
            reactions,
            manual_reaction={
                "intraday": "3月31日收HK$6.62；事件与年度结果、回购等重叠",
                "t1": "4月1日收HK$6.91",
                "t5": "4月9日收HK$6.99",
                "t20": None,
                "benchmark": None,
                "benchmark_adjusted": None,
                "volume_ratio": None,
                "resonance": "mixed_or_neutral",
                "source_refs": ["horizon-M02"],
                "limitations": "重叠事件较多，不能把窗口归因于出表。",
            },
            review="先重列口径，再比较持续经营；不把一次性公允价值变化当核心盈利。",
            source_gap="缺少独立的市场共识和事件隔离条件。",
        )
    )
    add(
        completed_event(
            "xpeng",
            "xpeng-fy2025",
            "2026-03-20",
            "FY2025与Q4首次季度盈利",
            "earnings_release",
            ["F01"],
            [
                "FY2025交付429,445辆",
                "收入RMB76.72bn",
                "毛利率18.87%",
                "FY净亏损RMB1.14bn",
                "Q4净利润RMB0.383bn",
            ],
            "规模和毛利显著改善，但单季盈利必须接受下一季度持续性检验。",
            ["规模放量 → 毛利改善 → 单季盈利", "下一季回落 → 变量从高向低风险"],
            "2026Q1实际",
            reactions,
            review="事件后窗口走弱，随后Q1亏损扩大，说明首次盈利不能直接年化。",
            source_gap="没有冻结发布前盈利与指引共识。",
        )
    )
    add(
        completed_event(
            "nanhua",
            "nanhua-ipo-2025",
            "2025-12-22",
            "H股上市",
            "listing",
            ["F01"],
            ["02691.HK上市", "上市首日收HK$9.10"],
            "新上市小盘H股的流通量、港股通资格和A/H价格发现会放大基本面之外的弹性。",
            ["H股上市 → 新流通供给", "A/H双重上市 → 跨市场价格发现"],
            "港股通、成交量与自由流通盘",
            reactions,
            review="上市后五个交易日收HK$9.91；没有T−1，不解释为异常收益。",
            source_gap="IPO没有常规T−1基线，且早期成交受配售和流通结构影响。",
        )
    )
    add(
        completed_event(
            "nanhua",
            "nanhua-stock-connect-2026",
            "2026-01-16",
            "纳入港股通",
            "stock_connect",
            ["F09"],
            ["上交所公告调整港股通标的", "新增南向资金可交易资格"],
            "资格改变潜在投资者范围，但不保证净买入，也不改变公司内在经营。",
            ["港股通资格 → 潜在南向资金/流动性", "成交与持仓 → 价格发现"],
            "南向持仓、成交量与A/H溢价",
            reactions,
            review="公告后首个完整交易日下跌且放量，证明“纳入”不是机械利好。",
            source_gap="公开窗口不能分离配售、短线资金和基本面因素。",
        )
    )
    add(
        completed_event(
            "vobile",
            "vobile-fy2025",
            "2026-03-27",
            "FY2025业绩",
            "earnings_release",
            ["F01"],
            ["收入HK$2.872bn", "归母利润HK$199.3m", "全年CFO约HK$69.9m"],
            "利润增长需要由现金转化、应收和资本化研发共同验证。",
            ["订阅/变现增长 → 会计利润 → CFO → 扣维持投入后的owner earnings"],
            "2026Q1经营数据与H1现金流",
            reactions,
            review="T0负、T+5正，短窗分歧大；现金质量比单日方向重要。",
            source_gap="未冻结一致预期；T+5仍受市场和融资事件影响。",
        )
    )
    add(
        completed_event(
            "nanhua",
            "nanhua-annual-governance-2026",
            "2026-03-27",
            "年报与治理公告包",
            "earnings_governance",
            ["F01"],
            ["2025年报披露", "同日还有审计、关联交易上限、分红和会计估计等治理事项"],
            "多项公告同日发布时必须作为事件包，不能把价格窗单独归因于利润标题。",
            ["年报利润/净资本 → 基本面", "治理与会计估计 → 盈利质量/风险折价"],
            "2026Q1与后续治理披露",
            reactions,
            review="首个交易日温和上涨、T+5接近持平；公告包内因素不可分离。",
            source_gap="同日多项公告，缺少事件隔离条件。",
        )
    )
    add(
        completed_event(
            "nanhua",
            "nanhua-regulatory-warning-2026",
            "2026-04-01",
            "证监局警示函",
            "regulatory",
            ["F11"],
            ["浙江证监局出具警示函", "合规事件进入正式监管证据层"],
            "金融小盘股的合规风险可能直接影响风险资本、客户信任和估值折价。",
            ["内控/合规 → 监管措施", "监管措施 → 客户/资本/估值风险"],
            "整改、重复违规和监管资本",
            reactions,
            review="首个反应日下跌5.8%；相关性与事件性质一致，但仍不证明全部因果。",
            source_gap="无法从公开窗口量化潜在业务流失或后续监管成本。",
        )
    )
    add(
        completed_event(
            "nanhua",
            "nanhua-q1-2026",
            "2026-04-21",
            "2026Q1报告",
            "earnings_release",
            ["F02"],
            ["营业收入RMB433.1m，同比+60.7%", "归母利润RMB204.8m，同比+138.8%"],
            "利润高增长必须拆成经纪、利息、风险管理和投资收益，不能直接外推全年。",
            ["交易活跃/利率/基差 → 收入结构 → 归母利润", "监管净资本 → 可扩张能力"],
            "2026H1利润与业务分项",
            reactions,
            review="强利润增长对应负事件窗，说明预期、流动性和结构质量比同比标题更重要。",
            source_gap="没有冻结Q1共识；H股流动性和A/H价格发现可能放大窗口。",
        )
    )
    add(
        completed_event(
            "meitu",
            "meitu-q1-2026",
            "2026-05-06",
            "2026Q1经营更新",
            "operating_update",
            ["F03"],
            [
                "核心影像与设计收入RMB852m，同比+34.3%",
                "付费用户超过17.9m，同比+30.2%",
                "生产力付费用户2.34m，同比+52.9%",
                "AI生产力ARR RMB580m，同比+56.2%",
            ],
            "付费人数、生产力占比和ARR比新品演示更接近AI应用商业化主线，但未披露利润和现金。",
            ["模型能力/推理成本 → 产品体验 → 付费转化/ARPU → 毛利与现金"],
            "2026H1：Q2增量、毛利、现金和净股数",
            reactions,
            review="T−1到T+5上涨20.3%，是六家公司中较清晰的经营KPI正共振之一；仍需中报财务闭环。",
            source_gap="Q1更新未经审阅，未披露利润、毛利率、CFO和分产品留存。",
        )
    )
    add(
        completed_event(
            "smic",
            "smic-q1-2026",
            "2026-05-14",
            "2026Q1业绩与Q2指引",
            "earnings_release",
            ["Q1_2026"],
            [
                "收入US$2.505bn，同比+11.5%",
                "毛利率20.1%",
                "产能利用率93.1%",
                "Q2收入指引环比+14%至+16%",
                "Q2毛利率指引20%至22%",
            ],
            "Q2指引把下一验证点冻结下来：收入增速能否加快，同时守住毛利率。",
            ["需求/国产替代 → 利用率与出货 → 收入", "资本开支/折旧/组合 → 毛利率与FCF"],
            "2026Q2实际对比+14%至+16%与20%至22%",
            reactions,
            review="T+5相对HSTECH较强；真正的surprise要等Q2实际与本次官方指引比较。",
            source_gap="Q1本身的发布前一致预期未冻结。",
        )
    )
    add(
        completed_event(
            "vobile",
            "vobile-q1-2026",
            "2026-05-19",
            "2026Q1经营数据",
            "operating_update",
            ["F03"],
            ["公司披露2026Q1未经审计经营数据", "用于跟踪活跃资产、MRR与业务增长"],
            "经营KPI要继续桥接到收入确认、现金和可转债偿债能力。",
            ["活跃资产/MRR → 订阅收入 → 毛利 → 回款", "内容变现规模 → 平台依赖与分成经济"],
            "2026H1正式财务结果",
            reactions,
            review="T0小幅正、T+5持平，市场没有给出持久方向；等待H1现金和债务处理。",
            source_gap="经营更新不等于完整季度财报，利润、CFO和应收口径待补。",
        )
    )
    add(
        completed_event(
            "xpeng",
            "xpeng-q1-2026",
            "2026-05-28",
            "2026Q1业绩与Q2指引",
            "earnings_release",
            ["F03"],
            [
                "交付62,682辆，同比-33.3%",
                "收入RMB13.03bn，同比-17.6%",
                "vehicle margin 12.1%",
                "净亏损RMB1.78bn",
                "Q2交付指引100,000至106,000辆",
                "Q2收入指引RMB19.6bn至20.8bn",
            ],
            "Q1可能是公司产品周期低点，但只有Q2/Q3同比、毛利和现金同步改善才构成增长变量上行。",
            ["新品/改款 → Q2交付修复", "ASP/车型组合 → vehicle margin", "库存/应付 → CFO质量"],
            "Q2财务实际与Q3交付同比",
            reactions,
            review="T0/T+5正共振，但T+20显著回落；短线修复不等于盈利底确认。",
            source_gap="Q2财务尚未披露；Q1现金下降和库存上升需要后续解释。",
        )
    )
    add(
        completed_event(
            "meitu",
            "meitu-imaging-governance-cluster",
            "2026-06-18",
            "影像节与披露治理事件簇",
            "product_governance_cluster",
            ["M02", "R05"],
            [
                "6月17日影像节提出apps-to-agents路线",
                "6月18日披露早前业绩视频误发调查与整改",
                "同时披露两项理财认购迟报",
            ],
            "产品发布与治理负面在相邻交易日重叠，必须作为事件簇而不是强行单因果归因。",
            ["产品路线 → 付费/留存验证", "披露控制缺陷 → 风险折价与事件跳空"],
            "无重复迟报；中报验证agent收入与成本",
            reactions,
            reaction_date="2026-06-18",
            review="T−1到T+5下跌13.7%；产品叙事未抵消治理与风险偏好压力。",
            source_gap="相邻事件与公司回购重叠，不能分离每个因素的价格贡献。",
        )
    )
    add(
        completed_event(
            "nanhua",
            "nanhua-repurchase-plan",
            "2026-06-24",
            "H股回购计划",
            "capital_allocation",
            ["F04", "F05"],
            ["董事会提出H股回购计划", "股东会后获授权", "授权不等于已经成交"],
            "小盘股回购只有在实际成交、净股数下降且不损害监管资本时才产生每股效果。",
            ["授权 → 实际成交 → 库存/注销 → 流通供给与每股价值", "现金使用 → 监管净资本"],
            "月报与next-day disclosure中的实际回购",
            reactions,
            review="T0小幅正、T+5近乎持平；不把授权公告当完成回购。",
            source_gap="截至研究日未发现实际回购成交披露。",
        )
    )
    add(
        completed_event(
            "smic",
            "smic-smnc-acquisition",
            "2026-06-25",
            "收购中芯北方剩余49%",
            "capital_allocation",
            ["SMNC_BOOK"],
            ["发行547.182m股A股", "非控股权益归属和充分摊薄股数发生变化"],
            "交易改变归母利润、股本和资本回报口径，必须做法定与备考桥。",
            ["并表权益变化 → 归母利润", "新股发行 → 稀释", "产能资产 → 折旧/现金回报"],
            "后续归母EPS、ROIC与资本开支",
            reactions,
            reaction_date="2026-06-25",
            review="首日与T+5均弱于HSTECH，和稀释/交易担忧一致但不证明因果。",
            source_gap="事件窗口与半导体板块波动重叠。",
        )
    )
    add(
        completed_event(
            "xpeng",
            "xpeng-q2-delivery-2026",
            "2026-07-02",
            "2026Q2交付",
            "operating_update",
            ["F04"],
            ["Q2交付103,295辆", "环比+64.8%", "同比+0.1%", "位于公司100,000至106,000辆指引中部"],
            "交付从Q1低点修复，但同比几乎持平；Q3同比和Q2财务决定变量是否真正由低向高。",
            ["车型上新 → 交付修复", "收入/ASP/vehicle margin → 财务确认", "Q3同比 → 趋势确认"],
            "Q2财务与Q3月度交付",
            reactions,
            expectation={
                "frozen_at": "2026-05-28T19:00:00+08:00",
                "official_guidance": ["Q2交付100,000至106,000辆"],
                "consensus": [],
                "previous_actual": ["2026Q1交付62,682辆"],
                "source_refs": ["xpeng-F03"],
            },
            surprise={
                "direction": "neutral",
                "raw": "实际103,295辆，较指引中点103,000辆高295辆",
                "percent": "较指引中点+0.3%，位于官方区间内",
                "score": 0,
                "method": "actual_vs_frozen_official_guidance",
                "confidence": "high",
                "reason": "实际交付位于指引中部，属于符合指引，不是超预期突破。",
                "source_refs": ["xpeng-F03", "xpeng-F04"],
            },
            review="T0正但T+5相对HSTECH偏弱；市场等待收入、毛利、亏损与现金。",
            source_gap="交付不提供ASP、利润和现金信息。",
        )
    )
    add(
        completed_event(
            "xpeng",
            "xpeng-july-delivery-2026",
            "2026-08-01",
            "2026年7月交付",
            "operating_update",
            ["F04", "F09", "F12", "F14"],
            [
                "7月交付38,027辆",
                "同比+4%",
                "较6月40,126辆环比-5.2%",
                "累计交付超过1.2m辆",
            ],
            "7月是Q2低点修复能否继续加速的第一笔Q3数据；结果同比略增、环比回落，尚不足以确认新一轮上行。",
            [
                "月度订单/排产 → 交付与车型结构 → Q3收入节奏",
                "促销/新品切换 → ASP与vehicle margin → 现金消耗",
            ],
            "8月24日Q2财务与8—9月交付",
            reactions,
            expectation={
                "frozen_at": "2026-07-30T18:00:00+08:00",
                "official_guidance": [],
                "consensus": [],
                "previous_actual": [
                    "2026年6月交付40,126辆",
                    "2025年7月交付36,717辆",
                    "事前问题：能否维持6月约40,126辆的运行率",
                ],
                "source_refs": ["xpeng-F04", "xpeng-F09"],
            },
            surprise=no_baseline(
                "没有公司单月指引或冻结一致预期；同比+4%、环比-5.2%是实际变化，不等于正式miss。"
            ),
            manual_reaction={
                "intraday": "首个反应日8月3日 -3.08%（HK$50.60→HK$49.04）",
                "t1": "T−1→T+1 -7.11%",
                "t5": None,
                "t20": None,
                "benchmark": "HSTECH",
                "benchmark_adjusted": "截至8月7日T+4：小鹏-7.83%、HSTECH+0.60%，超额-8.43%",
                "volume_ratio": "首个反应日0.82×此前20日均量；8月4日约1.64×",
                "resonance": "negative_resonance",
                "source_refs": ["xpeng-M01", "xpeng-M03"],
                "attribution_confidence": "low",
                "limitations": "只有四个完整交易日；8月4日同时公布Q2董事会日期，且无冻结单月共识。",
            },
            review=(
                "7月交付说明销量从Q1低点恢复，但没有在6月基础上继续抬升；"
                "截至8月7日价格显著跑输HSTECH，但样本只有T+4，不能把跌幅全归因于交付。"
            ),
            source_gap="未披露车型结构、订单积压、促销、ASP和单车毛利；T+5/T+20仍待形成。",
        )
    )
    add(
        scheduled_event(
            "xpeng",
            "xpeng-q2-results-2026",
            "2026-08-24",
            "2026Q2完整财务结果",
            ["F03", "F04", "F12", "F13"],
            (
                "这是把Q2交付修复桥接到收入、ASP、vehicle margin、亏损、库存和现金的"
                "关键节点，也是判断增长变量是否真正由低向高的主验证。"
            ),
            [
                "收入落在RMB19.6bn至20.8bn指引的什么位置，交付符合指引后ASP是否仍承压？",
                "gross margin与vehicle margin相对Q1的20.6%和12.1%是改善还是回落？",
                "净亏损、经营现金流、库存和现金能否扭转Q1恶化？",
                "Q3交付及收入指引是否支持同比重新加速，而不只是环比反弹？",
            ],
            date_status="confirmed",
            beijing_time="2026-08-24 20:00｜公司已公告",
            official_guidance=[
                "2026Q2交付指引100,000至106,000辆；实际已披露103,295辆",
                "2026Q2收入指引RMB19.6bn至20.8bn",
            ],
            transmission_paths=[
                "交付 × ASP → 汽车收入 → vehicle margin",
                "服务收入/大众合作 → 集团毛利 → 亏损收窄",
                "库存/应付/资本开支 → CFO与现金安全垫",
                "Q3官方指引 → 同比增速预期 → 估值与风险偏好",
            ],
            previous_actual=[
                "2026Q1收入RMB13.03bn，gross margin 20.6%，vehicle margin 12.1%",
                "2026Q1净亏损RMB1.78bn，现金类资产约RMB42.09bn",
                "2026年7月交付38,027辆，同比+4%、环比-5.2%",
            ],
            next_check_at="2026-08-24 20:00结果与电话会后立即回填",
            source_gap=(
                "发布日期已确认；市场一致预期、Q2实际财务和Q3官方指引仍待披露，"
                "不得在8月24日前预填结果。"
            ),
            frozen_at="2026-08-08T12:00:00+08:00",
        )
    )
    add(
        scheduled_event(
            "xpeng",
            "xpeng-q3-delivery-2026",
            "2026-10-09",
            "2026Q3交付与同比增速验证（预计窗口）",
            ["F01", "F03", "F04", "F12"],
            "Q2交付同比仅+0.1%、7月同比+4%且环比回落；只有Q3交付重新超过上年同期并与收入、毛利和现金一致，才能把环比修复升级为增长变量上行。",
            [
                "Q3交付能否超过2025Q3的116,007辆并形成同比正增长？",
                "已有7月38,027辆；8—9月月均至少38,991辆才刚好超过上年Q3，至少44,791辆才达到Q3同比+10%。",
                "Q2业绩给出的Q3官方指引是否兑现，月度交付是否依赖单次新品脉冲？",
                "销量增长能否伴随vehicle margin稳定和现金消耗收窄？",
            ],
            date_status="estimated",
            beijing_time="预计2026年10月上旬｜非官宣",
            previous_actual=[
                "2025Q3交付116,007辆",
                "2026Q2交付103,295辆，同比+0.1%",
                "2026年7月交付38,027辆，同比+4%、环比-5.2%",
            ],
            transmission_paths=[
                "Q3交付同比 → 增速拐点确认/否定",
                "车型结构与促销 → ASP/vehicle margin → 每股经济",
                "行业价格战与同业上新 → 订单份额 → 风险偏好弹性",
            ],
            source_gap=(
                "2026-10-09只是季度结束后的研究复核锚点，不是公司确认日期；"
                "Q3官方指引需在Q2完整业绩披露后冻结。"
            ),
            frozen_at="2026-08-08T12:00:00+08:00",
        )
    )
    add(
        completed_event(
            "meitu",
            "meitu-founder-purchase-2026",
            "2026-07-03",
            "创始人增持160万股",
            "insider_action",
            ["F05"],
            ["创始人兼董事长以均价约HK$4.023购入1.6m股"],
            "增持是利益一致性信号，不是估值底或未来业绩的充分证据。",
            ["内部人买入 → 信号/流通供给", "每股价值仍取决于经营、稀释和现金"],
            "后续增持、净股数与中报每股经济",
            reactions,
            review="初始上涨未延续至T+5；小额增持不能压过基本面与行业情绪。",
            source_gap="无法从单次交易推断管理层私有信息或未来收益。",
        )
    )
    add(
        completed_event(
            "meitu",
            "meitu-h1-preliminary-2026",
            "2026-07-30",
            "2026H1初步业务及财务更新",
            "business_and_financial_update",
            ["F16"],
            [
                "核心业务收入约人民币18亿元，同比+30.9%",
                "调整后归母利润同比+36%至+40%；IFRS归母利润至少+35%",
                "付费用户超过1,844万；AI生产力ARR约人民币6.2亿元",
                "AI credits在Q1和Q2均环比消耗增长超过46%",
            ],
            "首次把用户、ARR和收入增长连接到H1调整后及IFRS归母利润方向。",
            [
                "ARPU/credits → 收入 → 毛利与费用杠杆",
                "调整利润 → 扣SBC/CFO/摊薄 → 每股owner earnings",
            ],
            "2026-08-26正式中报",
            reactions,
            impact=5,
            expectation_baseline=(
                "没有可审计、事前冻结的一致预期；只与Q1已知增速和FY2025/H1基数对照，"
                "不制造精确surprise。"
            ),
            surprise=no_baseline("缺少事前冻结的可比共识；增长本身不等于预期差。"),
            manual_reaction={
                "intraday": "公告7月30日盘后；7月31日首个完整交易日+10.28%",
                "t1": "T−1 7月30日收盘至8月3日+11.45%（部分窗口）",
                "t5": None,
                "t20": None,
                "benchmark": "HSTECH",
                "benchmark_adjusted": "同部分窗口HSTECH +1.50%；超额约+9.95pct",
                "volume_ratio": None,
                "resonance": "positive_resonance_partial_window",
                "chart_value_pct": 11.45,
                "chart_window": "partial",
                "chart_title": "截至8月3日部分窗口 +11.45%",
                "chart_label": "+11.4%*",
                "source_refs": ["meitu-P03"],
                "attribution_confidence": "medium",
                "limitations": "T+5尚未形成；7月29日股价已先涨13.1%，公告不能解释全部窗口收益。",
            },
            reported_at="2026-07-30T17:48:00+08:00",
            event_time="17:48:00",
            beijing_time="2026-07-30T17:48:00+08:00",
            definition_changes=[
                "公告基于未经审核和未经审阅的管理账，正式报表仍待2026-08-26"
            ],
            validation_status="market_reviewed_partial",
            review=(
                "H1预告把未来一年盈利增长从猜测升级为有官方区间支持的假设，"
                "但没有证明十年护城河或现价安全边际。"
            ),
            source_gap=(
                "正式毛利率、渠道/模型成本、SBC、CFO、递延收入、净现金和同日"
                "完全摊薄股数待8月26日。"
            ),
        )
    )
    add(
        completed_event(
            "nanhua",
            "nanhua-h1-profit-alert",
            "2026-07-07",
            "2026H1业绩预增",
            "earnings_preliminary",
            ["F03"],
            ["归母利润预计RMB375m至405m", "上年同期RMB231.3m", "推算Q2归母利润约RMB170.2m至200.2m"],
            "Q1高速增长后，Q2隐含利润用于判断增速是否继续向上；预告仍需正式分部和现金验证。",
            ["期货市场活跃/利率 → 经纪、利息、投资收益 → 利润", "正式中报 → 分部/净资本/现金质量"],
            "正式2026中报与分部利润",
            reactions,
            review="T0/T+5温和正向；预告未审计且没有冻结共识，不把同比增幅等同surprise。",
            source_gap="正式收入、分部、现金流和风险资本尚未披露。",
        )
    )
    add(
        completed_event(
            "vobile",
            "vobile-cb-repurchase-2026",
            "2026-07-07",
            "月报披露可转债回购",
            "capital_allocation",
            ["F05"],
            ["六月月报披露可转债回购变化", "降低部分到期本金但不自动消除剩余偿债/稀释风险"],
            "回购债券的价值取决于折价、现金成本、剩余本金和到期选择。",
            ["现金回购债券 → 净债务/流动性", "剩余债券 → 到期偿还或转股"],
            "剩余本金、现金余额与到期处理",
            reactions,
            review="T0小幅正、T+5转负；资本结构问题仍需定量桥。",
            source_gap="公开月报不足以观察持有人对冲和实际融资成本。",
        )
    )
    add(
        completed_event(
            "smic",
            "smic-tsmc-readthrough-2026",
            "2026-07-16",
            "台积电Q2全球映射",
            "global_mapping",
            ["TSMC_Q2"],
            ["台积电Q2结果提供先进制程与AI需求读数", "不能机械映射为中芯同节点、同客户或同盈利"],
            "美国/台湾先进制程强势只是一层行业映射，中芯还受节点结构、出口管制与A/H估值影响。",
            ["全球AI需求 → 先进制程景气", "节点/设备约束差异 → 中芯经济并不等价"],
            "中芯Q2实际与官方指引对比",
            reactions,
            review="正向同业财报对应中芯负事件窗，说明跨市场映射必须经过节点和估值过滤。",
            source_gap="这不是中芯公司事件；窗口仅用于检验主题传导。",
        )
    )
    add(
        completed_event(
            "horizon",
            "horizon-h1-update-2026",
            "2026-07-21",
            "2026H1业绩更新",
            "earnings_preliminary",
            ["H03"],
            [
                "持续经营收入预计RMB1.93bn至2.08bn，同比+24.8%至+34.5%",
                "调整后净亏损预计RMB1.4bn至1.7bn，亏损扩大",
            ],
            "收入增长与调整亏损扩大并存，是判断规模能否转成经营杠杆的核心矛盾。",
            ["车型定点/SOP → 芯片与许可收入", "研发/营运资本 → 调整亏损与现金"],
            "正式中报的毛利、客户、应收、库存与CFO",
            reactions,
            manual_reaction={
                "intraday": "7月21日收HK$4.45，较前收HK$4.39约+1.4%",
                "t1": "7月22日收HK$4.75；与CARIAD事件重叠",
                "t5": "7月28日收HK$5.00；随后多项资本事件重叠",
                "t20": None,
                "benchmark": None,
                "benchmark_adjusted": None,
                "volume_ratio": None,
                "resonance": "positive_resonance",
                "source_refs": ["horizon-M02"],
                "limitations": "7月21日至26日形成密集事件簇，无法单独归因。",
            },
            review="收入增长得到确认，但亏损绝对额继续扩大；价格上行不能替代现金OE验证。",
            source_gap="更新未经审计且未获审计委员会复核；没有正式现金流。",
        )
    )
    add(
        completed_event(
            "horizon",
            "horizon-cariad-amendment-2026",
            "2026-07-22",
            "CARIAD旧贷重组",
            "capital_allocation",
            ["H04"],
            [
                "拟发行约1.302bn股新B股抵销US$662.4m本息",
                "另付约US$398.9m现金",
                "赎回约716m潜在转换股",
            ],
            "交易同时改变现金、债务和股本；必须看交割而不是只看名义减少转换权。",
            ["现金支付 → 净现金下降", "新股发行 → 稀释", "旧转换权赎回 → 潜在供给减少"],
            "交割完成公告与月报股数",
            reactions,
            manual_reaction={
                "intraday": "7月22日收HK$4.75，较前收约+6.7%",
                "t1": "7月23日收HK$4.57；与新CB定价重叠",
                "t5": "7月29日收HK$5.28；多事件重叠",
                "t20": None,
                "benchmark": None,
                "benchmark_adjusted": None,
                "volume_ratio": None,
                "resonance": "positive_resonance",
                "source_refs": ["horizon-M02"],
                "limitations": "与H1更新、新CB和奖励事件重叠。",
            },
            review="价格窗口偏强，但经济实质是现金和稀释的重排，不是免费消债。",
            source_gap="截至截止日交割未确认完成。",
        )
    )
    add(
        completed_event(
            "horizon",
            "horizon-new-cb-2026",
            "2026-07-23",
            "US$4.5亿新零息可转债",
            "financing",
            ["H05"],
            [
                "US$450m零息CB，2027到期",
                "初始转股价HK$5.55",
                "全转约635.6m股",
                "主要用于CARIAD现金支付",
            ],
            "新融资解决近期支付，同时把一年后现金偿还或转股稀释带入资本结构。",
            ["融资现金 → CARIAD支付", "股价/转股价 → 转股稀释或到期偿债"],
            "发行完成、转换、回购或2027到期现金",
            reactions,
            manual_reaction={
                "intraday": "7月23日收HK$4.57，较前收约-3.8%",
                "t1": "7月24日收HK$4.42",
                "t5": None,
                "t20": None,
                "benchmark": None,
                "benchmark_adjusted": None,
                "volume_ratio": None,
                "resonance": "negative_resonance",
                "source_refs": ["horizon-M02"],
                "limitations": "同一周多个事件，不能把全部波动归因于新CB。",
            },
            review="融资缓解近期现金需求，但一年期到期与潜在稀释构成新的验证点。",
            source_gap="没有债券持有人对冲和最终转换路径数据。",
        )
    )
    add(
        completed_event(
            "horizon",
            "horizon-share-awards-2026",
            "2026-07-26",
            "股份奖励",
            "share_supply",
            ["H06"],
            ["授予约90.6m股B股奖励", "无业绩条件", "进入已知完全摊薄股本桥"],
            "亏损期无业绩目标的股份奖励会影响每股价值和流通供给预期。",
            ["SBC → 员工激励", "新增潜在股份 → 充分摊薄每股经济"],
            "归属、发行/库存股转出与净股数",
            reactions,
            manual_reaction={
                "intraday": "公告在周末；7月27日收HK$4.62",
                "t1": "7月28日收HK$5.00",
                "t5": None,
                "t20": None,
                "benchmark": None,
                "benchmark_adjusted": None,
                "volume_ratio": None,
                "resonance": "mixed_or_neutral",
                "source_refs": ["horizon-M02"],
                "limitations": "公告后上涨与前述资本事件及市场情绪重叠。",
            },
            review="价格未表现为简单稀释折价；经济成本仍应进入全摊薄分母。",
            source_gap="最终归属、发行或库存股转出时点待后续披露。",
        )
    )
    add(
        scheduled_event(
            "nanhua",
            "nanhua-capitalisation-shares-2026",
            "2026-08-11",
            "资本化H股预计开始交易",
            ["F06"],
            "新增流通供给可能改变小盘股稀缺度、换手和A/H价格发现。",
            ["实际发行股数和总股本是否与通函一致？", "成交量、自由流通盘和A/H溢价如何变化？"],
            date_status="expected_not_completed",
        )
    )
    add(
        scheduled_event(
            "meitu",
            "meitu-h1-results-2026",
            "2026-08-26",
            "2026H1正式业绩",
            ["F08", "F03", "F16"],
            "这是把H1初步收入和利润增长桥接到毛利、现金、推理成本、SBC和净股数的主要决策节点。",
            [
                "核心收入约+30.9%、调整后归母+36%至+40%能否由正式报表复核？",
                "生产力收入占比、ARR和AI credits是否转成高质量确认收入与毛利？",
                "毛利率、CFO、SBC、回购和可转债后的每股owner earnings如何？",
            ],
        )
    )
    return sorted(events, key=lambda item: (axis_date(item), item["event_id"]))


def fetch_hstech() -> dict[str, Any]:
    url = (
        "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?"
        "param=hkHSTECH,day,2024-10-01,2026-07-29,650,qfq"
    )
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=20) as response:
        payload = json.load(response)
    rows = payload["data"]["hkHSTECH"]["day"]
    points = []
    for row in rows:
        if row[0] < START or row[0] > AS_OF[:10]:
            continue
        points.append(
            {
                "date": row[0],
                "value": float(row[2]),
                "volume": float(row[5]),
            }
        )
    return {
        "label": "HSTECH风险偏好代理｜不是六家公司共同业绩基准",
        "ticker": "HSTECH",
        "listing": "HKEX index",
        "kind": "line",
        "timezone": "Asia/Shanghai",
        "adjustment_policy": "Tencent qfq daily close; frozen through 2026-07-29",
        "price_timestamp": "2026-07-29 close",
        "source_ref": "shared-hstech",
        "points": points,
    }


def build_report() -> dict[str, Any]:
    reactions = load_reactions()
    try:
        market_series = fetch_hstech()
    except (OSError, KeyError, ValueError, json.JSONDecodeError):
        market_series = {
            "label": "HSTECH风险偏好代理｜抓取失败，保留事件账本",
            "ticker": "HSTECH",
            "kind": "line",
            "points": [],
            "source_ref": "shared-hstech",
        }
    events = build_events(reactions)
    return {
        "artifact_type": "earnings_season_timeline",
        "version": "1.1",
        "title": "六家公司：事件 Surprise 与市场共振时间轴",
        "subtitle": (
            "复用 Seed AI 硬件事件终端：把公司披露、资本结构、行业映射、"
            "T0/T+5/T+20与下一验证放到同一条证据轴。"
        ),
        "as_of": AS_OF,
        "timezone": "Asia/Shanghai",
        "date_range": {"start": START, "end": END},
        "scope": {
            "theme": (
                "company fundamentals × capital structure × industry transmission "
                "× small-cap event elasticity"
            ),
            "markets": ["HK", "A-share", "US mapping"],
            "watchlist": [company["ticker"] for company in COMPANIES.values()],
            "user_holdings": [],
        },
        "not_investment_advice": True,
        "market_series": market_series,
        "scenario_paths": [],
        "events": events,
        "source_refs": source_refs(),
        "data_quality": {
            "missing": [
                "多数历史事件没有在发生前冻结卖方一致预期，因此不做事后surprise打分。",
                "地平线7月21日至26日、美图6月17日至18日属于事件簇，无法隔离单一因素。",
                "六家公司业务不同，HSTECH只作风险偏好背景，不是共同业绩基准。",
                "尚未发生的正式结果、T+1/T+5/T+20和成交量必须事件后追加。",
            ],
            "conflicts": [
                "同比高增长可以对应负价格窗，说明预期、估值、流动性和利润质量不能被同比标题替代。",
                "行业映射可能与公司价格反向；台积电强不等于中芯同节点、同客户、同盈利。",
            ],
            "manual_review_required": [
                "2026年8月上旬复核小鹏7月交付；官方公布Q2业绩日期后把TBA替换为确认日期。",
                "小鹏Q2完整业绩后回填收入、vehicle margin、亏损、现金/库存及Q3官方指引。",
                "2026年10月上旬用Q3交付同比检验小鹏是否从环比修复升级为增速上行。",
                "2026-08-11复核南华资本化H股实际上市和流通供给。",
                "2026-08-26回填美图H1实际、Q2增量和事件后市场反应。",
                "各公司下一份正式财报后冻结新基线，不改写本页历史预期。",
            ],
        },
    }


COMPONENT_START = "<!-- company-event-terminal:start -->"
COMPONENT_END = "<!-- company-event-terminal:end -->"

COMPONENT_CSS = """
<style>
  .event-terminal{margin:22px 0 26px;padding:20px;border:1px solid #cad4ce;
  border-radius:18px;background:linear-gradient(145deg,#fbfdfb,#f7f4eb)}
  .event-terminal *{box-sizing:border-box}
  .et-head{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(260px,.8fr);
  gap:18px;align-items:start}
  .et-kicker{color:var(--green);font-size:11px;font-weight:850;letter-spacing:.12em;
  text-transform:uppercase}
  .et-head h3{margin:4px 0 7px;font-size:clamp(21px,2.6vw,30px)}
  .et-head p{margin:0;color:var(--muted);font-size:13px}
  .et-summary{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
  .et-stat{padding:10px 12px;border:1px solid var(--line);border-radius:11px;background:#fff}
  .et-stat b{display:block;font-size:21px;line-height:1.15}
  .et-stat span{color:var(--muted);font-size:11px}
  .et-legend{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:8px;
  margin:15px 0 12px}
  .et-legend>div{display:grid;grid-template-columns:18px 1fr;gap:7px;align-items:center;
  padding:9px 10px;border:1px solid var(--line);border-radius:10px;background:#fff}
  .et-legend b{font-size:11px}.et-legend small{grid-column:2;color:var(--muted);
  font-size:10px;line-height:1.35}
  .et-shape{display:block;width:12px;height:12px;border:2px solid var(--green);
  border-radius:50%;background:#fff}
  .et-shape.filled{background:var(--green)}
  .et-shape.ring{background:var(--green);box-shadow:0 0 0 3px rgba(23,107,80,.2)}
  .et-shape.diamond{border:0;border-radius:1px;background:#65716b;transform:rotate(45deg)}
  .et-axis-shell{overflow-x:auto;border:1px solid var(--line);border-radius:13px;background:#fff}
  .et-axis{position:relative;min-width:780px;height:148px;
  background-image:linear-gradient(to right,rgba(217,215,206,.5) 1px,transparent 1px);
  background-size:10% 100%}
  .et-axis:before{content:"";position:absolute;left:3%;right:3%;top:76px;
  border-top:2px solid #d7dcd8}
  .et-axis-label{position:absolute;top:112px;transform:translateX(-50%);
  color:var(--muted);font-size:10px;white-space:nowrap}
  .et-axis-label.start{transform:none}.et-axis-label.end{transform:translateX(-100%)}
  .et-now{position:absolute;top:0;bottom:0;border-left:2px solid var(--red);z-index:1}
  .et-now span{position:absolute;top:7px;left:5px;color:var(--red);font-size:10px;
  font-weight:850;white-space:nowrap}
  .et-node{position:absolute;z-index:2;width:15px;height:15px;border:3px solid var(--green);
  border-radius:50%;background:var(--green);transform:translate(-50%,-50%);
  box-shadow:0 2px 7px rgba(23,34,30,.18)}
  .et-node.future{background:#fff}.et-node.reviewed{box-shadow:0 0 0 4px rgba(23,107,80,.2)}
  .et-node.not-comparable{border:0;border-radius:2px;background:#65716b;
  transform:translate(-50%,-50%) rotate(45deg)}
  .et-node:hover,.et-node:focus{outline:3px solid rgba(49,95,143,.2);outline-offset:3px}
  .et-node-date{position:absolute;left:50%;top:18px;transform:translateX(-50%) rotate(-34deg);
  transform-origin:left top;color:#52605a;font-size:9px;white-space:nowrap}
  .et-chart{margin:14px 0;padding:14px;border:1px solid var(--line);
  border-radius:13px;background:#fff}
  .et-chart-head{display:flex;justify-content:space-between;gap:12px;align-items:start}
  .et-chart h4{margin:0;font-size:15px}.et-chart p{margin:2px 0 0;color:var(--muted);font-size:11px}
  .et-chart-legend{display:flex;gap:10px;flex-wrap:wrap;color:var(--muted);font-size:10px}
  .et-chart-legend i{display:inline-block;width:10px;height:7px;margin-right:4px;border-radius:2px}
  .et-reaction-axis{display:grid;grid-template-columns:145px 1fr;margin:12px 0 5px;
  color:var(--muted);font-size:9px}
  .et-reaction-axis>div{display:flex;justify-content:space-between}
  .et-reaction-row{display:grid;grid-template-columns:145px 1fr;gap:10px;align-items:center;
  margin:6px 0}
  .et-reaction-label{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:11px}
  .et-reaction-plot{position:relative;height:34px;border-radius:7px;background:#f7f6f1}
  .et-reaction-plot:before{content:"";position:absolute;left:50%;top:0;bottom:0;
  border-left:1px solid #aeb7b1}
  .et-bar{position:absolute;height:7px;border-radius:3px;min-width:1px}
  .et-bar.positive{left:50%}.et-bar.negative{right:50%}
  .et-bar.t0{top:3px;background:var(--green)}
  .et-bar.t5{top:13px;background:var(--blue)}
  .et-bar.t20{top:23px;background:var(--amber)}
  .et-bar em{position:absolute;top:-4px;font-style:normal;font-size:8px;font-weight:800;
  white-space:nowrap}
  .et-bar.positive em{left:calc(100% + 3px)}.et-bar.negative em{right:calc(100% + 3px)}
  .et-ledger-title{display:flex;justify-content:space-between;gap:12px;align-items:end;
  margin:17px 0 8px}
  .et-ledger-title h4{margin:0;font-size:16px}.et-ledger-title span{color:var(--muted);
  font-size:10px}
  .et-event{margin:8px 0;border:1px solid var(--line);border-radius:12px;background:#fff;
  scroll-margin-top:86px}
  .et-event:target{border-color:var(--blue);box-shadow:0 0 0 3px rgba(49,95,143,.12)}
  .et-event summary{display:grid;grid-template-columns:92px minmax(0,1fr) auto;
  gap:10px;align-items:center;padding:12px 13px}
  .et-event summary::marker{color:var(--green)}
  .et-event-date{font-size:11px;font-weight:800;color:var(--muted)}
  .et-event-title{font-size:13px;font-weight:820}
  .et-badges{display:flex;gap:5px;flex-wrap:wrap;justify-content:flex-end}
  .et-badge{padding:2px 7px;border-radius:999px;font-size:9px;font-weight:820;background:#ecefe9;
  color:#52605a}.et-badge.reviewed{background:var(--green-soft);color:var(--green)}
  .et-badge.future{background:var(--amber-soft);color:var(--amber)}
  .et-badge.nocomp{background:#edf0f2;color:#56636b}
  .et-badge.date-estimated{background:#fff3d8;color:#8b5d00}
  .et-badge.date-tba{background:#f2eafb;color:#67448a}
  .et-date-legend{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:-4px 0 12px;
  color:var(--muted);font-size:10px}
  .et-date-legend span{padding:4px 7px;border:1px solid var(--line);border-radius:999px;
  background:#fff}
  .et-diagnosis{margin:12px 0;padding:13px 15px;border-left:4px solid var(--blue);
  border-radius:10px;background:#eef4f8;color:#344a56;font-size:12px;line-height:1.65}
  .et-diagnosis strong{color:#203943}.et-diagnosis a{font-weight:800;color:var(--blue)}
  .et-event-body{padding:0 14px 14px}
  .et-evidence-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
  .et-evidence{padding:10px 11px;border-radius:9px;background:#f7f6f1}
  .et-evidence b{display:block;margin-bottom:3px;color:#4e5b55;font-size:10px;
  letter-spacing:.04em}.et-evidence p,.et-evidence ul{margin:0;color:#46534d;font-size:11px}
  .et-evidence ul{padding-left:17px}.et-evidence li{margin:2px 0}
  .et-source-links{display:flex;flex-wrap:wrap;gap:6px;margin-top:9px}
  .et-source-links a{padding:3px 7px;border:1px solid var(--line);border-radius:999px;
  text-decoration:none;font-size:9px;font-weight:750}
  .et-preserved-label{margin:24px 0 8px!important;padding-top:18px;border-top:1px solid var(--line);
  font-size:16px!important}
  @media(max-width:820px){.et-head{grid-template-columns:1fr}
  .et-legend{grid-template-columns:1fr 1fr}}
  @media(max-width:620px){.event-terminal{padding:14px}.et-legend{grid-template-columns:1fr}
  .et-reaction-axis,.et-reaction-row{grid-template-columns:92px 1fr}.et-event summary{
  grid-template-columns:78px 1fr}.et-badges{grid-column:1/-1;justify-content:flex-start}
  .et-evidence-grid{grid-template-columns:1fr}}
</style>
"""


def lifecycle(event: dict[str, Any]) -> str:
    if event.get("date_status") != "completed":
        return "expectation_frozen"
    validation_status = str((event.get("validation") or {}).get("status") or "")
    if validation_status == "market_reviewed_partial":
        return validation_status
    market = event.get("market_reaction") or {}
    if market.get("resonance") not in (None, "pending"):
        return "market_reviewed"
    return "actual_reported"


def is_not_comparable(event: dict[str, Any]) -> bool:
    surprise = event.get("surprise") or {}
    return str(surprise.get("method") or "").startswith("not_comparable")


def event_title(event: dict[str, Any]) -> str:
    return str(event["company"]).split("｜", 1)[-1]


def axis_date(event: dict[str, Any]) -> str:
    value = event.get("timeline_anchor_date") or event.get("date")
    if not value:
        raise ValueError(f"Event {event.get('event_id')} has no axis date")
    return str(value)


def display_date(event: dict[str, Any]) -> str:
    if event.get("date_status") == "completed" and event.get("date"):
        return str(event["date"])
    return str(event.get("beijing_time") or event.get("date") or "TBA")


def axis_node_label(event: dict[str, Any]) -> str:
    status = str(event.get("date_status") or "")
    if status == "tba":
        return "TBA"
    anchor = axis_date(event)
    prefix = "预计" if status in {"estimated", "expected_not_completed"} else ""
    return f"{prefix}{anchor[5:]}"


def source_links(
    event: dict[str, Any],
    sources: dict[str, dict[str, Any]],
) -> str:
    links = []
    for source_id in dict.fromkeys(event.get("source_refs") or []):
        source = sources.get(source_id)
        if not source or not source.get("url"):
            continue
        title = str(source.get("title") or source_id).split("｜", 1)[-1]
        links.append(
            f'<a href="{escape(str(source["url"]))}" rel="noreferrer">'
            f'{escape(title)}</a>'
        )
    return "".join(links) or "<span>本节点没有新增可点击来源。</span>"


def list_html(values: list[str] | None, empty: str) -> str:
    if not values:
        return f"<p>{escape(empty)}</p>"
    return "<ul>" + "".join(f"<li>{escape(str(value))}</li>" for value in values) + "</ul>"


def reaction_value(event: dict[str, Any], key: str) -> float | None:
    text = str((event.get("market_reaction") or {}).get(key) or "")
    matches = re.findall(r"([+−-]\d+(?:\.\d+)?)%", text)
    if not matches:
        return None
    return float(matches[0].replace("−", "-"))


def event_axis(
    events: list[dict[str, Any]], start: date, end: date, as_of_date: str
) -> str:
    span = max((end - start).days, 1)

    def position(value: str) -> float:
        return min(97.0, max(3.0, (date.fromisoformat(value) - start).days / span * 100))

    nodes = []
    for index, event in enumerate(events):
        state = lifecycle(event)
        classes = ["et-node"]
        if state == "expectation_frozen":
            classes.append("future")
        elif state.startswith("market_reviewed"):
            classes.append("reviewed")
        if is_not_comparable(event):
            classes.append("not-comparable")
        top = 48 + (index % 3) * 25
        title = (
            f"{display_date(event)}｜{event_title(event)}｜{state}"
            + ("｜不可比" if is_not_comparable(event) else "")
        )
        nodes.append(
            f'<a class="{" ".join(classes)}" href="#event-{escape(event["event_id"])}" '
            f'style="left:{position(axis_date(event)):.3f}%;top:{top}px" '
            f'title="{escape(title)}"><span class="et-node-date">{escape(axis_node_label(event))}'
            f"</span></a>"
        )
    now = position(as_of_date)
    return f"""
      <div class="et-axis-shell" aria-label="公司事件横向时间轴">
        <div class="et-axis">
          <span class="et-axis-label start" style="left:3%">{start.isoformat()}</span>
          <span class="et-axis-label" style="left:{now:.3f}%">{as_of_date}</span>
          <span class="et-axis-label end" style="left:97%">{end.isoformat()}</span>
          <span class="et-now" style="left:{now:.3f}%"><span>NOW</span></span>
          {"".join(nodes)}
        </div>
      </div>
    """


def reaction_chart(events: list[dict[str, Any]]) -> str:
    rows: list[tuple[dict[str, Any], dict[str, float]]] = []
    for event in events:
        market = event.get("market_reaction") or {}
        if market.get("chart_value_pct") is not None:
            values = {"partial": float(market["chart_value_pct"])}
        else:
            values = {
                key: value
                for key in ("intraday", "t5", "t20")
                if (value := reaction_value(event, key)) is not None
            }
        if values:
            rows.append((event, values))
    max_abs = max(
        (abs(value) for _, values in rows for value in values.values()),
        default=10.0,
    )
    scale = max(10.0, (int(max_abs / 10) + 1) * 10.0)
    row_html = []
    class_for = {"intraday": "t0", "t5": "t5", "t20": "t20", "partial": "t5"}
    label_for = {"intraday": "T0", "t5": "T+5", "t20": "T+20", "partial": "部分窗口"}
    for event, values in rows:
        bars = []
        market = event.get("market_reaction") or {}
        for key, value in values.items():
            width = min(48.0, abs(value) / scale * 48.0)
            direction = "positive" if value >= 0 else "negative"
            title = (
                str(market.get("chart_title"))
                if key == "partial"
                else f"{label_for[key]} {value:+.2f}%"
            )
            label = (
                str(market.get("chart_label"))
                if key == "partial"
                else f"{value:+.1f}%"
            )
            bars.append(
                f'<span class="et-bar {class_for[key]} {direction}" '
                f'style="width:{width:.3f}%" title="{escape(title)}">'
                f"<em>{escape(label)}</em></span>"
            )
        row_html.append(
            f'<div class="et-reaction-row"><a class="et-reaction-label" '
            f'href="#event-{escape(event["event_id"])}" title="{escape(event_title(event))}">'
            f'{escape(event["date"][2:])} {escape(event_title(event))}</a>'
            f'<div class="et-reaction-plot">{"".join(bars)}</div></div>'
        )
    if not row_html:
        row_html.append("<p>没有可比较的百分比事件窗；价格水平仍保留在下方事件卡。</p>")
    return f"""
      <div class="et-chart" role="img" aria-label="事件后价格窗口柱状图">
        <div class="et-chart-head">
          <div><h4>事件后价格窗口</h4>
          <p>相关性观察，不证明单一公告造成全部涨跌；缺失窗口不画成 0。</p></div>
          <div class="et-chart-legend"><span><i style="background:var(--green)"></i>T0</span>
          <span><i style="background:var(--blue)"></i>T+5</span>
          <span><i style="background:var(--amber)"></i>T+20</span></div>
        </div>
        <div class="et-reaction-axis"><span></span><div><span>−{scale:.0f}%</span><span>0</span>
        <span>+{scale:.0f}%</span></div></div>
        {"".join(row_html)}
      </div>
    """


def event_card(
    event: dict[str, Any],
    sources: dict[str, dict[str, Any]],
    *,
    open_card: bool,
) -> str:
    state = lifecycle(event)
    not_comparable = is_not_comparable(event)
    expectation = event.get("expectation_snapshot")
    if state == "expectation_frozen":
        future_baseline = []
        if expectation:
            future_baseline.extend(
                f"官方指引：{value}"
                for value in expectation.get("official_guidance") or []
            )
            future_baseline.extend(
                f"上一期实际：{value}"
                for value in expectation.get("previous_actual") or []
            )
        future_baseline.extend(
            f"待回答：{value}" for value in event.get("pre_event_questions") or []
        )
        expectation_html = list_html(
            future_baseline,
            "尚未冻结可比共识；只保留下一步观察问题。",
        )
    elif expectation:
        expectation_html = list_html(
            expectation.get("consensus") or expectation.get("official_guidance"),
            "有冻结快照，但未录入可比数值。",
        )
    else:
        expectation_html = (
            "<p>事件前没有可审计、冻结的可比共识；"
            "因此不以事后同比增速制造 Surprise。</p>"
        )
    actual = event.get("actual_results") or {}
    actual_html = list_html(
        actual.get("metrics"),
        "事件尚未发生，实际值保持为空。",
    )
    surprise = event.get("surprise") or {}
    surprise_text = (
        "not_comparable｜没有可比基线，不等于负面。"
        if not_comparable
        else str(surprise.get("reason") or surprise.get("direction") or "pending")
    )
    market = event.get("market_reaction") or {}
    market_lines = [
        f"{label}：{market[key]}"
        for key, label in (
            ("intraday", "T0/首个反应"),
            ("t1", "T+1"),
            ("t5", "T+5"),
            ("t20", "T+20"),
            ("benchmark_adjusted", "基准调整"),
            ("volume_ratio", "量比"),
        )
        if market.get(key) not in (None, "")
    ]
    market_html = list_html(market_lines, "价格窗口尚未形成或没有可比基线。")
    transmission_html = list_html(
        event.get("transmission_paths"),
        "传导路径待补。",
    )
    next_check = (event.get("validation") or {}).get("next_check_at") or "待补"
    review = event.get("post_event_review") or "未来事件，等待实际披露后追加复盘。"
    badges = [
        f'<span class="et-badge {"future" if state == "expectation_frozen" else "reviewed"}">'
        f"{escape(state)}</span>",
        f'<span class="et-badge">影响 {escape(str(event.get("impact_score") or "—"))}/5</span>',
    ]
    if not_comparable:
        badges.append('<span class="et-badge nocomp">not_comparable</span>')
    date_status = str(event.get("date_status") or "")
    date_status_labels = {
        "confirmed": ("已确认日期", ""),
        "expected_not_completed": ("公司预计｜待发生", "date-estimated"),
        "estimated": ("预计窗口｜非官宣", "date-estimated"),
        "tba": ("日期TBA｜官方未公布", "date-tba"),
    }
    if date_status in date_status_labels:
        label, css_class = date_status_labels[date_status]
        badges.append(
            f'<span class="et-badge {css_class}">{escape(label)}</span>'
        )
    open_attr = " open" if open_card else ""
    why_text = escape(str(event.get("why_it_matters") or "待补"))
    gap_text = escape(str(event.get("source_gap") or "无"))
    sources_html = source_links(event, sources)
    return f"""
      <details class="et-event" id="event-{escape(event["event_id"])}"{open_attr}>
        <summary><span class="et-event-date">{escape(display_date(event))}</span>
        <span class="et-event-title">{escape(event_title(event))}</span>
        <span class="et-badges">{"".join(badges)}</span></summary>
        <div class="et-event-body">
          <div class="et-evidence-grid">
            <div class="et-evidence"><b>为什么重要</b><p>{why_text}</p></div>
            <div class="et-evidence"><b>冻结预期 / 事前问题</b>{expectation_html}</div>
            <div class="et-evidence"><b>官方实际</b>{actual_html}</div>
            <div class="et-evidence"><b>Surprise 状态</b><p>{escape(surprise_text)}</p></div>
            <div class="et-evidence"><b>市场反应</b>{market_html}</div>
            <div class="et-evidence"><b>行业 / 资本结构传导</b>{transmission_html}</div>
            <div class="et-evidence"><b>复盘结论</b><p>{escape(str(review))}</p></div>
            <div class="et-evidence"><b>下一验证与缺口</b>
            <p>{escape(str(next_check))}｜{gap_text}</p></div>
          </div>
          <div class="et-source-links"><strong>原始来源：</strong>{sources_html}</div>
        </div>
      </details>
    """


def company_artifact(report: dict[str, Any], company_key: str) -> dict[str, Any]:
    company = COMPANIES[company_key]
    events = [
        event for event in report["events"] if event["ticker"] == company["ticker"]
    ]
    used_refs = {
        source_id
        for event in events
        for source_id in event.get("source_refs") or []
    }
    sources = [
        source for source in report["source_refs"] if source["id"] in used_refs
    ]
    return {
        **report,
        "as_of": (
            "2026-08-08T12:00:00+08:00"
            if company_key == "xpeng"
            else (
                "2026-08-04T10:18:00+08:00"
                if company_key == "meitu"
                else report["as_of"]
            )
        ),
        "title": f"{company['name']}：事件 Surprise 与市场共振",
        "subtitle": (
            "该终端只展示本公司事件；把冻结预期、官方实际、价格窗口、"
            "行业/资本结构传导与下一验证放在一条证据轴。"
        ),
        "scope": {
            "theme": company["bucket"],
            "markets": [company["market"]],
            "watchlist": [company["ticker"]],
            "user_holdings": [],
        },
        "events": events,
        "source_refs": sources,
        "market_series": None,
        "data_quality": {
            "missing": [
                "没有事前冻结共识的历史事件保持 not_comparable。",
                "缺失的 T+1/T+5/T+20 不按 0 处理。",
            ],
            "conflicts": [
                "同比增长、事件后涨跌和长期基本面不是同一个判断。",
            ],
            "manual_review_required": [
                "未来节点发生后追加官方实际与价格窗口，不改写旧预期。",
            ],
        },
    }


def component_html(artifact: dict[str, Any], company_key: str) -> str:
    company = COMPANIES[company_key]
    events = artifact["events"]
    sources = {source["id"]: source for source in artifact["source_refs"]}
    start = date.fromisoformat(min(axis_date(event) for event in events))
    end = max(
        date.fromisoformat(END),
        max(date.fromisoformat(axis_date(event)) for event in events),
    )
    reviewed = sum(lifecycle(event).startswith("market_reviewed") for event in events)
    reviewed_label = (
        "已复核/部分价格窗"
        if any(lifecycle(event) == "market_reviewed_partial" for event in events)
        else "已复核价格窗"
    )
    nocomp = sum(is_not_comparable(event) for event in events)
    future = sum(lifecycle(event) == "expectation_frozen" for event in events)
    latest_completed = max(
        (
            axis_date(event)
            for event in events
            if event.get("date_status") == "completed"
        ),
        default="",
    )
    cards = "".join(
        event_card(
            event,
            sources,
            open_card=(
                axis_date(event) == latest_completed
                or lifecycle(event) == "expectation_frozen"
            ),
        )
        for event in events
    )
    cluster_note = ""
    if company_key == "xpeng":
        cluster_note = """
  <div class="et-diagnosis"><strong>先读结论：</strong>2025Q2的T+5 +19.94%不是
  单一财报反应。财报当日为-1.85%；<a href="#event-xpeng-founder-purchase-2025">创始人增持</a>
  披露后的首个交易日涨13.60%、量比约3.92×，而
  <a href="#event-xpeng-next-p7-launch-2025">新P7发布</a>后T+5又跌16.14%。
  2026年7月交付38,027辆，同比+4%但环比-5.2%；截至8月7日四个交易日跑输HSTECH约8.43个百分点。
  当前更像“低点修复、尚未重新加速”；下一硬验证是8月24日Q2财务与Q3指引。</div>
        """
    as_of_date = str(artifact["as_of"])[:10]
    html = f"""
{COMPONENT_START}
{COMPONENT_CSS}
<div class="event-terminal" data-company="{escape(company_key)}"
  data-contract="seed.earnings-season-timeline.v1.1-compatible">
  <div class="et-head">
    <div><div class="et-kicker">Company event validation terminal</div>
    <h3>{escape(company["name"])}｜事件 Surprise × 市场共振</h3>
    <p>只放本公司事件。图上点击节点可跳到证据卡；价格反应是相关性观察，不是买卖指令或单因果证明。</p></div>
    <div class="et-summary">
      <div class="et-stat"><b>{len(events)}</b><span>公司事件</span></div>
      <div class="et-stat"><b>{reviewed}</b><span>{reviewed_label}</span></div>
      <div class="et-stat"><b>{nocomp}</b><span>不可比 Surprise</span></div>
      <div class="et-stat"><b>{future}</b><span>未来验证节点</span></div>
    </div>
  </div>
  <div class="et-legend" aria-label="事件状态图例">
    <div><i class="et-shape"></i><b>expectation_frozen</b>
    <small>空心：只冻结问题，不预填实际。</small></div>
    <div><i class="et-shape filled"></i><b>actual_reported</b>
    <small>实心：官方实际已披露。</small></div>
    <div><i class="et-shape ring"></i><b>market_reviewed</b>
    <small>外圈：至少一个价格窗口已复核。</small></div>
    <div><i class="et-shape ring"></i><b>market_reviewed_partial</b>
    <small>部分窗口：T+5/T+20尚未形成，不能当完整复盘。</small></div>
    <div><i class="et-shape diamond"></i><b>not_comparable</b>
    <small>菱形：无可靠基线；不等于负面。</small></div>
  </div>
  <div class="et-date-legend" aria-label="未来事件日期口径">
    <b>日期口径：</b><span>已确认日期＝公司已公告</span>
    <span>预计窗口＝研究锚点，非官宣</span><span>TBA＝官方尚未公布日期</span>
  </div>
  {cluster_note}
  {event_axis(events, start, end, as_of_date)}
  {reaction_chart(events)}
  <div class="et-ledger-title"><h4>纵向证据账本</h4>
  <span>预期 → 实际 → Surprise → 价格 → 传导 → 下一验证</span></div>
  {cards}
  <p class="chart-note">研究边界：影响分只用于排序研究注意力，不是收益预测；
  未来节点保持空心，缺失窗口不画成 0。</p>
</div>
<script>
(() => {{
  const openTarget = () => {{
    const id = location.hash.slice(1);
    if (!id) return;
    const target = document.getElementById(id);
    if (target && target.matches('details.et-event')) target.open = true;
  }};
  openTarget();
  window.addEventListener('hashchange', openTarget);
}})();
</script>
<h3 class="et-preserved-label">原报告事件表与更长历史（保留）</h3>
{COMPONENT_END}
    """.strip()
    return "\n".join(line.rstrip() for line in html.splitlines())


def inject_component(report_path: Path, component: str) -> None:
    html = report_path.read_text(encoding="utf-8")
    block_pattern = re.compile(
        re.escape(COMPONENT_START) + r".*?" + re.escape(COMPONENT_END),
        flags=re.DOTALL,
    )
    if block_pattern.search(html):
        updated = block_pattern.sub(component, html, count=1)
    else:
        old_callout = re.compile(
            r'\s*<p class="callout blue"><strong>深度事件终端：</strong>'
            r'.*?</p>',
            flags=re.DOTALL,
        )
        updated = old_callout.sub("", html, count=1)
        section_start = updated.find('<section id="timeline"')
        if section_start == -1:
            raise RuntimeError(f"Missing #timeline section: {report_path}")
        heading_end = updated.find("</h2>", section_start)
        if heading_end == -1:
            raise RuntimeError(f"Missing #timeline heading: {report_path}")
        insert_at = heading_end + len("</h2>")
        updated = updated[:insert_at] + "\n" + component + updated[insert_at:]
    report_path.write_text(updated, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--company",
        choices=sorted(COMPANIES),
        help="只重建指定公司的事件 artifact 与嵌入式 HTML；默认重建全部公司。",
    )
    args = parser.parse_args()
    report = build_report()
    company_keys = [args.company] if args.company else list(COMPANIES)
    for company_key in company_keys:
        company = COMPANIES[company_key]
        artifact = company_artifact(report, company_key)
        json_path = DOCS / company["slug"] / "data" / "event-terminal.json"
        json_path.write_text(
            json.dumps(artifact, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        report_path = DOCS / company["slug"] / "report.html"
        inject_component(report_path, component_html(artifact, company_key))
        print(json_path)
        print(report_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
