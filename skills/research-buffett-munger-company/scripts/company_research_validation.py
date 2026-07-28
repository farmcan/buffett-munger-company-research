from __future__ import annotations

import json
import math
import re
from collections.abc import Iterable, Mapping
from datetime import date, datetime
from typing import Any

SCHEMA_VERSION = "seed.stock-fundamentals-valuation.v2"

METHODOLOGY_REFERENCE_CATALOG = {
    "berkshire_owner_manual": {
        "title": "Berkshire Hathaway Owner's Manual",
        "url": "https://www.berkshirehathaway.com/ownman.pdf",
        "tier": "A",
    },
    "berkshire_1977_letter": {
        "title": "1977 Chairman's Letter",
        "url": "https://www.berkshirehathaway.com/letters/1977.html",
        "tier": "A",
    },
    "berkshire_1983_letter": {
        "title": "1983 Chairman's Letter",
        "url": "https://www.berkshirehathaway.com/letters/1983.html",
        "tier": "A",
    },
    "berkshire_1986_letter": {
        "title": "1986 Chairman's Letter",
        "url": "https://www.berkshirehathaway.com/letters/1986.html",
        "tier": "A",
    },
    "berkshire_1989_letter": {
        "title": "1989 Chairman's Letter",
        "url": "https://www.berkshirehathaway.com/letters/1989.html",
        "tier": "A",
    },
    "berkshire_1996_letter": {
        "title": "1996 Chairman's Letter",
        "url": "https://www.berkshirehathaway.com/letters/1996.html",
        "tier": "A",
    },
    "berkshire_2005_letter": {
        "title": "2005 Chairman's Letter",
        "url": "https://www.berkshirehathaway.com/letters/2005ltr.pdf",
        "tier": "A",
    },
    "berkshire_2007_letter": {
        "title": "2007 Chairman's Letter",
        "url": "https://www.berkshirehathaway.com/letters/2007ltr.pdf",
        "tier": "A",
    },
    "berkshire_2009_letter": {
        "title": "2009 Chairman's Letter",
        "url": "https://www.berkshirehathaway.com/letters/2009ltr.pdf",
        "tier": "A",
    },
    "berkshire_2018_letter": {
        "title": "2018 Chairman's Letter",
        "url": "https://www.berkshirehathaway.com/letters/2018ltr.pdf",
        "tier": "A",
    },
    "berkshire_2021_letter": {
        "title": "2021 Chairman's Letter",
        "url": "https://www.berkshirehathaway.com/letters/2021ltr.pdf",
        "tier": "A",
    },
    "berkshire_2022_letter": {
        "title": "2022 Chairman's Letter",
        "url": "https://www.berkshirehathaway.com/letters/2022ltr.pdf",
        "tier": "A",
    },
    "berkshire_2023_letter": {
        "title": "2023 Chairman's Letter",
        "url": "https://www.berkshirehathaway.com/letters/2023ltr.pdf",
        "tier": "A",
    },
    "berkshire_cnbc_meeting_archive": {
        "title": "Warren Buffett Archive: Berkshire Hathaway Annual Meetings",
        "url": "https://buffett.cnbc.com/annual-meetings/",
        "tier": "A-",
    },
    "usc_2007_munger_record": {
        "title": "300 graduate from USC Law",
        "url": "https://gould.usc.edu/news/300-graduate-from-usc-law/",
        "tier": "A-",
    },
    "munger_1994_usc_transcript_chain": {
        "title": "A Lesson on Elementary, Worldly Wisdom",
        "url": "https://mungerarchive.com/recordings/usc-1994-worldly-wisdom/",
        "tier": "B",
    },
    "munger_1995_misjudgment_transcript": {
        "title": "The Psychology of Human Misjudgment",
        "url": (
            "https://jamesclear.com/great-speeches/"
            "the-psychology-of-human-misjudgment-by-charlie-munger"
        ),
        "tier": "B",
    },
    "hkex_rule_8_08_public_float": {
        "title": "HKEX Main Board Listing Rule 8.08",
        "url": (
            "https://cn-rules.hkex.com.hk/%E8%A6%8F%E5%89%87%E6%89%8B%E5%86%8A/808"
        ),
        "tier": "A",
    },
    "hkex_rule_13_32b_public_float": {
        "title": "HKEX Main Board Listing Rule 13.32B",
        "url": "https://en-rules.hkex.com.hk/entiresection/7010",
        "tier": "A",
    },
    "msci_gimi_float_method": {
        "title": "MSCI Global Investable Market Indexes Methodology",
        "url": (
            "https://www.msci.com/downloads/web/msci-com/indexes/index-resources/"
            "market-classification/MSCI_GIMIMethodology_Mar2023.pdf"
        ),
        "tier": "A-",
    },
    "spdj_index_mathematics_float": {
        "title": "Index Mathematics Methodology",
        "url": (
            "https://www.spglobal.com/spdji/en/methodology/article/"
            "index-mathematics-methodology/"
        ),
        "tier": "A-",
    },
    "field_hanka_lockup_expiration": {
        "title": "The Expiration of IPO Share Lockups",
        "url": "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=205011",
        "tier": "A-",
    },
}

PRIMARY_METHODOLOGY_TIERS = {"A", "A-"}
SOURCE_TIERS = {"A", "B", "C", "D", "L"}
SOURCE_PUBLISHED_AT_STATUSES = {"known", "not_disclosed", "not_applicable"}
SOURCE_AUDIT_STATUSES = {"audited", "unaudited", "not_applicable", "unknown"}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

EXPECTED_GATES = [
    "identity_and_source_integrity",
    "circle_of_competence",
    "business_economics",
    "durable_moat",
    "management_and_capital_allocation",
    "owner_earnings",
    "survival_and_balance_sheet",
    "intrinsic_value_and_margin_of_safety",
    "decision_and_disconfirming_evidence",
]

EXPECTED_RESEARCH_DIMENSIONS = [
    "security_and_legal_subject",
    "control_and_beneficial_ownership",
    "business_model",
    "revenue_structure",
    "industry_chain_position",
    "product_and_unit_economics",
    "customers",
    "suppliers",
    "competition_structure",
    "durable_moat",
    "revenue_quality",
    "earnings_quality",
    "cash_conversion",
    "working_capital",
    "capital_intensity",
    "returns_on_capital",
    "balance_sheet_survival",
    "capital_allocation",
    "management",
    "governance_and_related_parties",
    "accounting_and_audit",
    "tax_and_legal",
    "per_share_economics",
    "valuation",
    "disconfirming_evidence",
]

RESEARCH_DIMENSION_INDICATOR_IDS = {
    "security_and_legal_subject": (
        "exact_security_issuer_share_class_and_rights",
        "dated_price_share_count_currency_and_listing_status",
    ),
    "control_and_beneficial_ownership": (
        "controller_voting_pledges_and_cross_holdings",
        "value_transfers_nci_and_related_party_exposure",
    ),
    "business_model": (
        "payer_value_proposition_revenue_and_cash_mechanism",
        "capital_needs_and_business_failure_variables",
    ),
    "revenue_structure": (
        "segment_product_and_geography_reconciliation",
        "volume_price_mix_acquisition_and_scope_bridge",
    ),
    "industry_chain_position": (
        "upstream_process_customer_payer_and_substitute_map",
        "profit_pool_and_inventory_credit_technology_risk",
    ),
    "product_and_unit_economics": (
        "price_volume_mix_and_incremental_economics",
        "industry_denominator_scope_and_comparability",
    ),
    "customers": (
        "customer_channel_end_user_and_payer_separation",
        "concentration_retention_receivables_inventory_and_external_evidence",
    ),
    "suppliers": (
        "critical_inputs_concentration_related_parties_and_substitution",
        "terms_prepayments_availability_and_cost_pass_through",
    ),
    "competition_structure": (
        "entry_exit_capacity_price_and_substitution",
        "competitor_customer_and_regulator_corroboration",
    ),
    "durable_moat": (
        "mechanism_economic_result_durability_and_direction",
        "strongest_falsifying_evidence",
    ),
    "revenue_quality": (
        "revenue_receivables_contract_assets_returns_and_cash",
        "acquisition_period_end_channel_and_recognition_distortion",
    ),
    "earnings_quality": (
        "reported_to_normalized_parent_earnings_bridge",
        "tax_attribution_scope_and_adjustment_disagreement",
    ),
    "cash_conversion": (
        "profit_operating_cash_and_distributable_cash_bridge",
        "factoring_payment_restricted_cash_and_sector_scope",
    ),
    "working_capital": (
        "receivables_inventory_payables_prepayments_and_contract_balances",
        "sustainable_financing_vs_temporary_cash_release",
    ),
    "capital_intensity": (
        "maintenance_vs_growth_investment_range",
        "capex_capacity_utilization_and_competitive_requirements",
    ),
    "returns_on_capital": (
        "multiperiod_roe_roic_and_incremental_returns",
        "leverage_buyback_cycle_and_accounting_decomposition",
    ),
    "balance_sheet_survival": (
        "debt_liquidity_covenants_guarantees_pledges_and_off_balance",
        "adverse_scenario_financing_need",
    ),
    "capital_allocation": (
        "reinvestment_ma_dividend_buyback_issuance_debt_and_cash_ledger",
        "diluted_per_share_outcomes_and_opportunity_cost",
    ),
    "management": (
        "dated_commitments_vs_outcomes",
        "incentives_compensation_succession_insider_actions_and_candor",
    ),
    "governance_and_related_parties": (
        "related_sales_purchases_loans_guarantees_and_asset_transfers",
        "pricing_minority_fairness_oversight_and_dissent",
    ),
    "accounting_and_audit": (
        "audit_kam_standard_policy_and_restatement",
        "statement_reproduction_and_conflict_preservation",
    ),
    "tax_and_legal": (
        "effective_deferred_and_uncertain_tax",
        "litigation_penalties_compliance_and_tail_exposure",
    ),
    "per_share_economics": (
        "basic_diluted_and_fully_diluted_share_reconciliation",
        "per_share_growth_distribution_issuance_and_repurchase_outcomes",
    ),
    "valuation": (
        "currency_consistent_value_range_assumptions_and_dates",
        "reverse_expectations_sensitivities_and_cross_check",
    ),
    "disconfirming_evidence": (
        "independent_strongest_counter_thesis",
        "observable_invalidation_next_evidence_and_review_date",
    ),
}

ALLOWED_INDICATOR_STATUSES = {
    "observed",
    "not_disclosed",
    "not_applicable",
    "conflicting",
}

RESEARCH_DIMENSION_STAGE = {
    "security_and_legal_subject": "fact_pack",
    "control_and_beneficial_ownership": "fact_pack",
    "business_model": "company_research",
    "revenue_structure": "fact_pack",
    "industry_chain_position": "fact_pack",
    "product_and_unit_economics": "fact_pack",
    "customers": "fact_pack",
    "suppliers": "fact_pack",
    "competition_structure": "company_research",
    "durable_moat": "company_research",
    "revenue_quality": "fact_pack",
    "earnings_quality": "fact_pack",
    "cash_conversion": "fact_pack",
    "working_capital": "fact_pack",
    "capital_intensity": "fact_pack",
    "returns_on_capital": "company_research",
    "balance_sheet_survival": "fact_pack",
    "capital_allocation": "company_research",
    "management": "company_research",
    "governance_and_related_parties": "company_research",
    "accounting_and_audit": "fact_pack",
    "tax_and_legal": "fact_pack",
    "per_share_economics": "fact_pack",
    "valuation": "valuation",
    "disconfirming_evidence": "red_team",
}

RESEARCH_DIMENSION_GATES = {
    "security_and_legal_subject": ("identity_and_source_integrity",),
    "control_and_beneficial_ownership": (
        "identity_and_source_integrity",
        "management_and_capital_allocation",
    ),
    "business_model": ("circle_of_competence", "business_economics"),
    "revenue_structure": ("business_economics",),
    "industry_chain_position": ("business_economics", "durable_moat"),
    "product_and_unit_economics": (
        "circle_of_competence",
        "business_economics",
    ),
    "customers": (
        "circle_of_competence",
        "business_economics",
        "durable_moat",
    ),
    "suppliers": (
        "circle_of_competence",
        "business_economics",
        "survival_and_balance_sheet",
    ),
    "competition_structure": ("business_economics", "durable_moat"),
    "durable_moat": (
        "durable_moat",
        "decision_and_disconfirming_evidence",
    ),
    "revenue_quality": ("business_economics", "owner_earnings"),
    "earnings_quality": ("business_economics", "owner_earnings"),
    "cash_conversion": ("owner_earnings", "survival_and_balance_sheet"),
    "working_capital": ("business_economics", "owner_earnings"),
    "capital_intensity": ("business_economics", "owner_earnings"),
    "returns_on_capital": (
        "business_economics",
        "management_and_capital_allocation",
    ),
    "balance_sheet_survival": ("survival_and_balance_sheet",),
    "capital_allocation": (
        "management_and_capital_allocation",
        "intrinsic_value_and_margin_of_safety",
    ),
    "management": (
        "management_and_capital_allocation",
        "decision_and_disconfirming_evidence",
    ),
    "governance_and_related_parties": (
        "identity_and_source_integrity",
        "management_and_capital_allocation",
        "survival_and_balance_sheet",
    ),
    "accounting_and_audit": (
        "identity_and_source_integrity",
        "owner_earnings",
        "survival_and_balance_sheet",
    ),
    "tax_and_legal": ("survival_and_balance_sheet",),
    "per_share_economics": (
        "business_economics",
        "management_and_capital_allocation",
        "intrinsic_value_and_margin_of_safety",
    ),
    "valuation": ("intrinsic_value_and_margin_of_safety",),
    "disconfirming_evidence": ("decision_and_disconfirming_evidence",),
}

ALLOWED_DIMENSION_STATUSES = {
    "applicable",
    "not_applicable",
    "unknown",
    "conflicting",
}

ALLOWED_PE_STATUSES = {
    "calculated",
    "not_meaningful",
    "unavailable",
}

ALLOWED_OWNER_EARNINGS_STATUSES = {
    "calculated",
    "unavailable",
}

ALLOWED_FORWARD_SCENARIO_STATUSES = {
    "calculated_pe",
    "loss_case",
    "unavailable",
}

ALLOWED_INTRINSIC_VALUE_STATUSES = {
    "calculated",
    "non_positive_equity_value",
    "unavailable",
}

ALLOWED_GATE_RESULTS = {
    "pass",
    "pass_with_scope",
    "mixed_positive",
    "mixed",
    "provisional",
    "range_only",
    "inconclusive",
    "research_ready",
    "research_ready_not_decision_ready",
    "fail",
    "outside_circle",
    "blocked",
}

POSITIVE_GATE_RESULTS = {
    "pass",
    "pass_with_scope",
    "mixed_positive",
    "research_ready",
    "research_ready_not_decision_ready",
}

HARD_BLOCK_GATE_RESULTS = {"fail", "outside_circle", "blocked"}
READINESS_GATE_RESULTS = {"research_ready", "research_ready_not_decision_ready"}

REQUIRED_FIELDS = [
    "schema_version",
    "artifact_type",
    "artifact_role",
    "status",
    "generated_at",
    "security",
    "as_of",
    "methodology_refs",
    "source_refs",
    "source_boundaries",
    "ownership_structure",
    "financial_history",
    "segment_data",
    "research_dimensions",
    "earnings_quality_bridge",
    "owner_earnings",
    "capital_allocation",
    "balance_sheet_quality",
    "pe_matrix",
    "forward_scenarios",
    "intrinsic_value_scenarios",
    "moat_evidence",
    "red_team",
    "gates",
    "source_gaps",
    "invalidation_tests",
    "historical_valuation",
    "price_move_attribution",
    "review",
    "disclaimer",
]

PROHIBITED_PHRASES = [
    "建议买入",
    "建议卖出",
    "应当买入",
    "应当卖出",
    "仓位建议",
    "保证收益",
    "稳赚",
    "必涨",
    "必跌",
    "strong buy",
    "guaranteed return",
]


class Validation:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warning(self, message: str) -> None:
        self.warnings.append(message)


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _date_value(value: Any) -> date | None:
    if not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _parse_date(value: Any, label: str, result: Validation) -> date | None:
    if not isinstance(value, str):
        result.error(f"{label} must be an ISO date string")
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        result.error(f"{label} is not a valid ISO date: {value!r}")
        return None


def _parse_datetime(value: Any, label: str, result: Validation) -> datetime | None:
    if not isinstance(value, str):
        result.error(f"{label} must be an ISO datetime string")
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        result.error(f"{label} is not a valid ISO datetime: {value!r}")
        return None
    if parsed.tzinfo is None:
        result.error(f"{label} must include a timezone")
        return None
    return parsed


def _validate_block_currency(
    block: Mapping[str, Any],
    *,
    label: str,
    expected_currency: str,
    result: Validation,
) -> None:
    currency = block.get("currency")
    if not isinstance(currency, str) or not currency.strip():
        result.error(f"{label}.currency must be a non-empty ISO-style currency code")
    elif expected_currency and currency.upper() != expected_currency.upper():
        result.error(
            f"{label}.currency={currency!r} must match security.currency={expected_currency!r}"
        )


def _require_reason(block: Mapping[str, Any], *, label: str, result: Validation) -> None:
    reason = block.get("reason")
    if not isinstance(reason, str) or not reason.strip():
        result.error(f"{label}.reason must be a non-empty string")


def _require_string_field(
    block: Mapping[str, Any],
    *,
    field: str,
    label: str,
    result: Validation,
) -> None:
    value = block.get(field)
    if not isinstance(value, str) or not value.strip():
        result.error(f"{label}.{field} must be a non-empty string")


def _security_currency(data: Mapping[str, Any]) -> str:
    security = data.get("security")
    if not isinstance(security, Mapping):
        return ""
    currency = security.get("currency")
    return currency if isinstance(currency, str) else ""


def _walk_source_ref_values(value: Any) -> Iterable[str]:
    if isinstance(value, Mapping):
        for key, child in value.items():
            if key == "source_refs" and isinstance(child, list):
                yield from (item for item in child if isinstance(item, str))
            else:
                yield from _walk_source_ref_values(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_source_ref_values(child)


def _validate_methodology_refs(data: dict[str, Any], result: Validation) -> None:
    rows = data.get("methodology_refs")
    if not isinstance(rows, list) or not rows:
        result.error("methodology_refs must be a non-empty list")
        return
    ids: list[str] = []
    has_primary_methodology_source = False
    for index, row in enumerate(rows):
        label = f"methodology_refs[{index}]"
        if not isinstance(row, dict):
            result.error(f"{label} must be an object")
            continue
        for field in ("id", "title", "url", "use"):
            if not isinstance(row.get(field), str) or not row[field].strip():
                result.error(f"{label}.{field} must be a non-empty string")
        ref_id = row.get("id")
        if isinstance(ref_id, str) and ref_id:
            ids.append(ref_id)
            catalog_row = METHODOLOGY_REFERENCE_CATALOG.get(ref_id)
            if catalog_row is None:
                result.error(
                    f"{label}.id={ref_id!r} is not in the audited methodology source catalog"
                )
            else:
                if row.get("title") != catalog_row["title"]:
                    result.error(
                        f"{label}.title must exactly match the audited methodology source catalog"
                    )
                if row.get("url") != catalog_row["url"]:
                    result.error(
                        f"{label}.url must exactly match the audited methodology source catalog"
                    )
                if catalog_row["tier"] in PRIMARY_METHODOLOGY_TIERS:
                    has_primary_methodology_source = True
        url = row.get("url")
        if isinstance(url, str) and not url.startswith("https://"):
            result.error(f"{label}.url must be an HTTPS URL")
    if len(ids) != len(set(ids)):
        result.error("methodology_refs contains duplicate ids")
    if not has_primary_methodology_source:
        result.error(
            "methodology_refs requires at least one audited tier A/A- source; "
            "tier-B transcript chains are supplemental only"
        )


def _validate_sources(data: dict[str, Any], result: Validation) -> None:
    source_rows = data.get("source_refs")
    if not isinstance(source_rows, list) or not source_rows:
        result.error("source_refs must be a non-empty list")
        return

    research_date = _date_value(
        data.get("as_of", {}).get("research_date")
        if isinstance(data.get("as_of"), Mapping)
        else None
    )
    source_ids: list[str] = []
    sources_by_id: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(source_rows):
        label = f"source_refs[{index}]"
        if not isinstance(row, dict):
            result.error(f"{label} must be an object")
            continue
        source_id = row.get("id")
        if not isinstance(source_id, str) or not source_id:
            result.error(f"{label}.id must be a non-empty string")
        else:
            source_ids.append(source_id)
            sources_by_id[source_id] = row
        if not isinstance(row.get("title"), str) or not row["title"]:
            result.error(f"{label}.title must be a non-empty string")
        if row.get("tier") not in SOURCE_TIERS:
            result.error(f"{label}.tier must be A, B, C, D or L")
        for field in ("source_type", "period", "scope"):
            if not isinstance(row.get(field), str) or not row[field].strip():
                result.error(f"{label}.{field} must be a non-empty string")
        url = row.get("url")
        if not isinstance(url, str) or not url.startswith("https://"):
            result.error(f"{label}.url must be an HTTPS URL")
        content_sha256 = row.get("content_sha256")
        if not isinstance(content_sha256, str) or not SHA256_RE.fullmatch(content_sha256):
            result.error(f"{label}.content_sha256 must be a lowercase SHA-256")

        covers = row.get("covers")
        if not isinstance(covers, list) or not covers:
            result.error(f"{label}.covers must be a non-empty list")
        elif any(not isinstance(item, str) or not item.strip() for item in covers):
            result.error(f"{label}.covers must contain only non-empty strings")
        elif len(covers) != len(set(covers)):
            result.error(f"{label}.covers contains duplicate values")

        published_at_status = row.get("published_at_status")
        published_at = row.get("published_at")
        published_date: date | None = None
        if published_at_status not in SOURCE_PUBLISHED_AT_STATUSES:
            result.error(
                f"{label}.published_at_status must be one of {sorted(SOURCE_PUBLISHED_AT_STATUSES)}"
            )
        elif published_at_status == "known":
            published_date = _parse_date(
                published_at,
                f"{label}.published_at",
                result,
            )
        else:
            if published_at is not None:
                result.error(
                    f"{label}.published_at must be null when published_at_status "
                    f"is {published_at_status}"
                )
            _require_string_field(
                row,
                field="date_reason",
                label=label,
                result=result,
            )

        accessed_date = _parse_date(
            row.get("accessed_at"),
            f"{label}.accessed_at",
            result,
        )
        if (
            published_date is not None
            and accessed_date is not None
            and published_date > accessed_date
        ):
            result.error(f"{label}.published_at cannot be after accessed_at")
        if (
            research_date is not None
            and published_date is not None
            and published_date > research_date
        ):
            result.error(f"{label}.published_at cannot be after as_of.research_date")
        if (
            research_date is not None
            and accessed_date is not None
            and accessed_date > research_date
        ):
            result.error(f"{label}.accessed_at cannot be after as_of.research_date")

        audit_status = row.get("audit_status")
        if audit_status not in SOURCE_AUDIT_STATUSES:
            result.error(f"{label}.audit_status must be one of {sorted(SOURCE_AUDIT_STATUSES)}")
        elif audit_status == "unknown":
            _require_string_field(
                row,
                field="audit_reason",
                label=label,
                result=result,
            )

    if len(source_ids) != len(set(source_ids)):
        result.error("source_refs contains duplicate ids")

    dangling = sorted(set(_walk_source_ref_values(data)) - set(source_ids))
    if dangling:
        result.error(f"dangling source_refs: {', '.join(dangling)}")
    if not any(row.get("tier") == "A" for row in source_rows if isinstance(row, dict)):
        result.error("at least one tier-A primary source is required")
    price_source_ref = (
        data.get("as_of", {}).get("price_source_ref")
        if isinstance(data.get("as_of"), Mapping)
        else None
    )
    price_source = sources_by_id.get(price_source_ref)
    if price_source is not None and "price" not in (price_source.get("covers") or []):
        result.error("as_of.price_source_ref must reference a source whose covers include 'price'")


def _validate_identity(data: dict[str, Any], result: Validation) -> None:
    security = data.get("security")
    if not isinstance(security, dict):
        result.error("security must be an object")
    else:
        for field in (
            "security_id",
            "ticker",
            "exchange",
            "listing_type",
            "currency",
            "fiscal_year_end",
            "reporting_standard",
        ):
            if not isinstance(security.get(field), str) or not security[field]:
                result.error(f"security.{field} must be a non-empty string")
        if not security.get("company_name") and not security.get("company_name_zh"):
            result.error("security requires company_name or company_name_zh")

    as_of = data.get("as_of")
    if not isinstance(as_of, dict):
        result.error("as_of must be an object")
        return
    research_date = _parse_date(
        as_of.get("research_date"),
        "as_of.research_date",
        result,
    )
    price_date = _parse_date(as_of.get("price_date"), "as_of.price_date", result)
    if research_date is not None and price_date is not None and price_date > research_date:
        result.error("as_of.price_date cannot be after as_of.research_date")
    if not _is_number(as_of.get("price")) or as_of["price"] <= 0:
        result.error("as_of.price must be a positive number")
    price_source_ref = as_of.get("price_source_ref")
    if not isinstance(price_source_ref, str) or not price_source_ref:
        result.error("as_of.price_source_ref must be a non-empty source id")
    else:
        source_ids = {
            row.get("id")
            for row in data.get("source_refs", [])
            if isinstance(row, Mapping) and isinstance(row.get("id"), str)
        }
        if price_source_ref not in source_ids:
            result.error("as_of.price_source_ref must resolve to source_refs")


def _validate_financial_history(data: dict[str, Any], result: Validation) -> None:
    history = data.get("financial_history")
    periods = history.get("periods") if isinstance(history, dict) else None
    if not isinstance(periods, list) or len(periods) < 3:
        result.error("financial_history.periods must contain at least three periods")
        return
    labels = [row.get("period") for row in periods if isinstance(row, dict)]
    if len(labels) != len(periods) or any(
        not isinstance(label, str) or not label for label in labels
    ):
        result.error("every financial_history period requires a non-empty period label")
    if len(labels) != len(set(labels)):
        result.error("financial_history contains duplicate periods")


def _validate_required_objects(data: dict[str, Any], result: Validation) -> None:
    for field in (
        "ownership_structure",
        "segment_data",
        "earnings_quality_bridge",
        "capital_allocation",
        "balance_sheet_quality",
        "historical_valuation",
        "price_move_attribution",
    ):
        value = data.get(field)
        if not isinstance(value, dict) or not value:
            result.error(f"{field} must be a non-empty object")


def _validate_string_or_object_list(
    value: Any,
    *,
    label: str,
    result: Validation,
) -> bool:
    if not isinstance(value, list):
        result.error(f"{label} must be a list")
        return False
    for index, item in enumerate(value):
        if isinstance(item, str):
            if not item.strip():
                result.error(f"{label}[{index}] must not be empty")
        elif not isinstance(item, dict) or not item:
            result.error(f"{label}[{index}] must be a non-empty string or object")
    return True


def _validate_dimension_indicators(
    row: Mapping[str, Any],
    *,
    dimension: str,
    label: str,
    dimension_source_refs_valid: bool,
    result: Validation,
) -> tuple[bool, list[str]]:
    indicators = row.get("indicators")
    if not isinstance(indicators, list):
        result.error(f"{label}.indicators must be a list")
        return False, []

    expected_ids = list(RESEARCH_DIMENSION_INDICATOR_IDS.get(dimension, ()))
    actual_ids = [indicator.get("id") for indicator in indicators if isinstance(indicator, Mapping)]
    if actual_ids != expected_ids:
        result.error(f"{label}.indicators must exactly match the ordered contract: {expected_ids}")

    dimension_source_refs = (
        set(row.get("source_refs") or []) if dimension_source_refs_valid else set()
    )
    statuses: list[str] = []
    for index, indicator in enumerate(indicators):
        indicator_label = f"{label}.indicators[{index}]"
        if not isinstance(indicator, dict):
            result.error(f"{indicator_label} must be an object")
            continue
        status = indicator.get("status")
        if status not in ALLOWED_INDICATOR_STATUSES:
            result.error(
                f"{indicator_label}.status must be one of {sorted(ALLOWED_INDICATOR_STATUSES)}"
            )
            continue
        statuses.append(status)
        if not isinstance(indicator.get("summary"), str) or not indicator["summary"].strip():
            result.error(f"{indicator_label}.summary must be a non-empty string")

        source_refs = indicator.get("source_refs")
        source_refs_valid = isinstance(source_refs, list) and all(
            isinstance(source_ref, str) and source_ref for source_ref in source_refs
        )
        if not source_refs_valid:
            result.error(f"{indicator_label}.source_refs must be a list of non-empty source ids")
            source_refs = []
        elif len(source_refs) != len(set(source_refs)):
            result.error(f"{indicator_label}.source_refs contains duplicate ids")
        if source_refs_valid and not set(source_refs).issubset(dimension_source_refs):
            result.error(f"{indicator_label}.source_refs must be included in {label}.source_refs")

        source_gaps = indicator.get("source_gaps")
        source_gaps_valid = _validate_string_or_object_list(
            source_gaps,
            label=f"{indicator_label}.source_gaps",
            result=result,
        )
        if status == "observed" and not source_refs:
            result.error(f"{indicator_label}.source_refs must not be empty when observed")
        elif status == "not_disclosed":
            if source_gaps_valid and not source_gaps:
                result.error(f"{indicator_label}.source_gaps must not be empty when not_disclosed")
        elif status == "conflicting":
            if not source_refs:
                result.error(f"{indicator_label}.source_refs must not be empty when conflicting")
            if source_gaps_valid and not source_gaps:
                result.error(f"{indicator_label}.source_gaps must not be empty when conflicting")
        elif status == "not_applicable":
            reason = indicator.get("reason")
            if not isinstance(reason, str) or not reason.strip():
                result.error(f"{indicator_label}.reason is required when not_applicable")
    return True, statuses


def _validate_dimension_indicator_status_coherence(
    *,
    dimension_status: Any,
    indicator_statuses: list[str],
    label: str,
    result: Validation,
) -> None:
    if dimension_status not in ALLOWED_DIMENSION_STATUSES:
        return
    if "conflicting" in indicator_statuses and dimension_status != "conflicting":
        result.error(f"{label}.status must be conflicting when a required indicator is conflicting")
    if dimension_status == "conflicting" and "conflicting" not in indicator_statuses:
        result.error(f"{label}.status is conflicting but no required indicator is conflicting")
    if (
        "not_disclosed" in indicator_statuses
        and "conflicting" not in indicator_statuses
        and dimension_status == "applicable"
    ):
        result.error(
            f"{label}.status cannot be applicable while a required indicator is not_disclosed"
        )
    if dimension_status == "unknown" and "not_disclosed" not in indicator_statuses:
        result.error(f"{label}.status is unknown but no required indicator is not_disclosed")
    if dimension_status == "not_applicable" and any(
        status != "not_applicable" for status in indicator_statuses
    ):
        result.error(
            f"{label}.status is not_applicable but not all required indicators are not_applicable"
        )
    if dimension_status == "applicable" and "observed" not in indicator_statuses:
        result.error(f"{label}.status is applicable but no required indicator is observed")


def _validate_research_dimensions(data: dict[str, Any], result: Validation) -> None:
    rows = data.get("research_dimensions")
    if not isinstance(rows, list):
        result.error("research_dimensions must be a list")
        return
    names = [row.get("dimension") for row in rows if isinstance(row, dict)]
    if names != EXPECTED_RESEARCH_DIMENSIONS:
        result.error(
            "research_dimensions must exactly match the ordered contract: "
            f"{EXPECTED_RESEARCH_DIMENSIONS}"
        )
    for index, row in enumerate(rows):
        label = f"research_dimensions[{index}]"
        if not isinstance(row, dict):
            result.error(f"{label} must be an object")
            continue
        status = row.get("status")
        if status not in ALLOWED_DIMENSION_STATUSES:
            result.error(f"{label}.status must be one of {sorted(ALLOWED_DIMENSION_STATUSES)}")
        if not isinstance(row.get("summary"), str) or not row["summary"].strip():
            result.error(f"{label}.summary must be a non-empty string")
        list_validity = {}
        for field in (
            "source_refs",
            "positive_evidence",
            "counter_evidence",
            "source_gaps",
        ):
            list_validity[field] = _validate_string_or_object_list(
                row.get(field),
                label=f"{label}.{field}",
                result=result,
            )
        if list_validity["source_refs"]:
            source_refs = row["source_refs"]
            if any(not isinstance(item, str) for item in source_refs):
                result.error(f"{label}.source_refs must contain only source ids")
            elif len(source_refs) != len(set(source_refs)):
                result.error(f"{label}.source_refs contains duplicate ids")
        indicators_valid, indicator_statuses = _validate_dimension_indicators(
            row,
            dimension=str(row.get("dimension") or ""),
            label=label,
            dimension_source_refs_valid=(
                list_validity["source_refs"]
                and all(isinstance(item, str) for item in row["source_refs"])
            ),
            result=result,
        )
        list_validity["indicators"] = indicators_valid
        _validate_dimension_indicator_status_coherence(
            dimension_status=status,
            indicator_statuses=indicator_statuses,
            label=label,
            result=result,
        )
        if status == "applicable":
            for field in ("indicators", "source_refs", "positive_evidence"):
                if list_validity[field] and not row[field]:
                    result.error(f"{label}.{field} must not be empty when applicable")
        elif status in {"unknown", "conflicting"}:
            if list_validity["source_gaps"] and not row["source_gaps"]:
                result.error(f"{label}.source_gaps must not be empty when status is {status}")
        elif status == "not_applicable":
            reason = row.get("not_applicable_reason")
            if not isinstance(reason, str) or not reason.strip():
                result.error(f"{label}.not_applicable_reason is required when not_applicable")


def _validate_pe_matrix(data: dict[str, Any], result: Validation) -> None:
    rows = data.get("pe_matrix")
    if not isinstance(rows, list) or not rows:
        result.error("pe_matrix must be a non-empty list")
        return
    labels = {row.get("label") for row in rows if isinstance(row, dict)}
    if "reported_fy" not in labels or "reported_ttm" not in labels:
        result.error("pe_matrix requires reported_fy and reported_ttm rows")
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            result.error(f"pe_matrix[{index}] must be an object")
            continue
        _validate_block_currency(
            row,
            label=f"pe_matrix[{index}]",
            expected_currency=_security_currency(data),
            result=result,
        )
        row_label = f"pe_matrix[{index}]"
        status = row.get("status")
        eps = row.get("eps")
        pe = row.get("pe")
        price = row.get("price")
        if not _is_number(price) or price <= 0:
            result.error(f"{row_label}.price must be positive")
        _parse_date(row.get("price_as_of"), f"{row_label}.price_as_of", result)
        for field in ("eps_period", "eps_type", "confidence"):
            if not isinstance(row.get(field), str) or not row[field]:
                result.error(f"{row_label}.{field} must be a non-empty string")

        if status not in ALLOWED_PE_STATUSES:
            result.error(f"{row_label}.status must be one of {sorted(ALLOWED_PE_STATUSES)}")
            continue
        if status == "calculated":
            if not _is_number(eps) or eps <= 0:
                result.error(f"{row_label}.eps must be positive when status is calculated")
                continue
            if not isinstance(row.get("formula"), str) or not row["formula"]:
                result.error(f"{row_label}.formula must be a non-empty string when calculated")
            if not _is_number(pe):
                result.error(f"{row_label}.pe must be numeric when status is calculated")
            elif _is_number(price) and not math.isclose(
                pe,
                price / eps,
                rel_tol=2e-4,
                abs_tol=2e-3,
            ):
                result.error(f"{row_label}.pe={pe} does not reproduce price/eps={price / eps:.6f}")
        elif status == "not_meaningful":
            if not _is_number(eps) or eps > 0:
                result.error(f"{row_label}.eps must be non-positive when status is not_meaningful")
            if pe is not None:
                result.error(f"{row_label}.pe must be null when status is not_meaningful")
            _require_reason(row, label=row_label, result=result)
        else:
            if eps is not None:
                result.error(f"{row_label}.eps must be null when status is unavailable")
            if pe is not None:
                result.error(f"{row_label}.pe must be null when status is unavailable")
            _require_reason(row, label=row_label, result=result)


def _validate_owner_earnings(data: dict[str, Any], result: Validation) -> None:
    owner_earnings = data.get("owner_earnings")
    if not isinstance(owner_earnings, dict):
        result.error("owner_earnings must be an object")
        return
    _validate_block_currency(
        owner_earnings,
        label="owner_earnings",
        expected_currency=_security_currency(data),
        result=result,
    )
    status = owner_earnings.get("status")
    if status not in ALLOWED_OWNER_EARNINGS_STATUSES:
        result.error(
            f"owner_earnings.status must be one of {sorted(ALLOWED_OWNER_EARNINGS_STATUSES)}"
        )
        return
    rows = owner_earnings.get("range")
    if not isinstance(rows, list):
        result.error("owner_earnings.range must be a list")
        return
    if status == "unavailable":
        if rows:
            result.error("owner_earnings.range must be empty when status is unavailable")
        _require_reason(owner_earnings, label="owner_earnings", result=result)
        if (
            not isinstance(owner_earnings.get("limitations"), list)
            or not owner_earnings["limitations"]
        ):
            result.error("owner_earnings.limitations must be non-empty")
        return
    if len(rows) < 2:
        result.error("owner_earnings.range must contain at least two cases")
        return
    values: list[float] = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            result.error(f"owner_earnings.range[{index}] must be an object")
            continue
        value = row.get("value")
        if not _is_number(value):
            result.error(f"owner_earnings.range[{index}].value must be finite and numeric")
        else:
            values.append(float(value))
        if not isinstance(row.get("formula"), str) or not row["formula"]:
            result.error(f"owner_earnings.range[{index}].formula is required")
    if values != sorted(values):
        result.error("owner_earnings.range values must be ordered low to high")
    if not isinstance(owner_earnings.get("limitations"), list) or not owner_earnings["limitations"]:
        result.error("owner_earnings.limitations must be non-empty")


def _validate_forward_scenarios(data: dict[str, Any], result: Validation) -> None:
    block = data.get("forward_scenarios")
    rows = block.get("scenarios") if isinstance(block, dict) else None
    if not isinstance(rows, list) or len(rows) < 3:
        result.error("forward_scenarios.scenarios must contain at least three cases")
        return
    _validate_block_currency(
        block,
        label="forward_scenarios",
        expected_currency=_security_currency(data),
        result=result,
    )
    names = {row.get("scenario") for row in rows if isinstance(row, dict)}
    if not {"bear", "base", "upside"}.issubset(names):
        result.error("forward scenarios must include bear, base and upside")
    price = block.get("price_anchor")
    if not _is_number(price) or price <= 0:
        result.error("forward_scenarios.price_anchor must be positive")
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            result.error(f"forward_scenarios.scenarios[{index}] must be an object")
            continue
        label = f"forward_scenarios.scenarios[{index}]"
        status = row.get("status")
        eps = row.get("forecast_eps")
        pe = row.get("implied_pe_at_current_price")
        if status not in ALLOWED_FORWARD_SCENARIO_STATUSES:
            result.error(
                f"{label}.status must be one of {sorted(ALLOWED_FORWARD_SCENARIO_STATUSES)}"
            )
            continue
        if status == "calculated_pe":
            if not _is_number(eps) or eps <= 0:
                result.error(f"{label}.forecast_eps must be positive when calculated_pe")
            elif _is_number(price) and price > 0:
                if not _is_number(pe) or not math.isclose(
                    pe,
                    price / eps,
                    rel_tol=2e-4,
                    abs_tol=2e-3,
                ):
                    result.error(f"forward scenario {row.get('scenario')} PE does not reproduce")
            elif not _is_number(pe):
                result.error(f"{label}.implied_pe_at_current_price must be numeric")
        elif status == "loss_case":
            if not _is_number(eps) or eps > 0:
                result.error(f"{label}.forecast_eps must be non-positive when loss_case")
            if pe is not None:
                result.error(f"{label}.implied_pe_at_current_price must be null when loss_case")
            _require_reason(row, label=label, result=result)
        else:
            if eps is not None:
                result.error(f"{label}.forecast_eps must be null when unavailable")
            if pe is not None:
                result.error(f"{label}.implied_pe_at_current_price must be null when unavailable")
            _require_reason(row, label=label, result=result)


def _validate_intrinsic_value(data: dict[str, Any], result: Validation) -> None:
    block = data.get("intrinsic_value_scenarios")
    rows = block.get("scenarios") if isinstance(block, dict) else None
    if not isinstance(rows, list) or len(rows) < 3:
        result.error("intrinsic_value_scenarios.scenarios must contain at least three cases")
        return
    _validate_block_currency(
        block,
        label="intrinsic_value_scenarios",
        expected_currency=_security_currency(data),
        result=result,
    )
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            result.error(f"intrinsic_value_scenarios.scenarios[{index}] must be an object")
            continue
        label = f"intrinsic_value_scenarios.scenarios[{index}]"
        status = row.get("status")
        discount = row.get("discount_rate_pct")
        terminal = row.get("terminal_growth_pct")
        per_share = row.get("intrinsic_value_per_share")
        if status not in ALLOWED_INTRINSIC_VALUE_STATUSES:
            result.error(
                f"{label}.status must be one of {sorted(ALLOWED_INTRINSIC_VALUE_STATUSES)}"
            )
            continue
        if status == "unavailable":
            if per_share is not None:
                result.error(f"{label}.intrinsic_value_per_share must be null when unavailable")
            _require_reason(row, label=label, result=result)
            assumptions_present = discount is not None or terminal is not None
            if assumptions_present and (
                not _is_number(discount) or not _is_number(terminal) or discount <= terminal
            ):
                result.error(
                    f"intrinsic value scenario {row.get('scenario')} requires "
                    "both numeric assumptions with discount rate > terminal growth, or neither"
                )
            continue
        if not _is_number(discount) or not _is_number(terminal) or discount <= terminal:
            result.error(
                f"intrinsic value scenario {row.get('scenario')} "
                "requires discount rate > terminal growth"
            )
        if status == "calculated":
            if not _is_number(per_share) or per_share <= 0:
                result.error(
                    f"intrinsic value scenario {row.get('scenario')} "
                    "requires positive per-share value when calculated"
                )
        else:
            if not _is_number(per_share) or per_share > 0:
                result.error(
                    f"{label}.intrinsic_value_per_share must be non-positive when "
                    "status is non_positive_equity_value"
                )
            _require_reason(row, label=label, result=result)


def _validate_gates(data: dict[str, Any], result: Validation) -> None:
    rows = data.get("gates")
    if not isinstance(rows, list):
        result.error("gates must be a list")
        return
    names = [row.get("gate") for row in rows if isinstance(row, dict)]
    if names != EXPECTED_GATES:
        result.error(f"gates must exactly match the ordered contract: {EXPECTED_GATES}")
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            result.error(f"gates[{index}] must be an object")
            continue
        gate_result = row.get("result")
        if gate_result not in ALLOWED_GATE_RESULTS:
            result.error(f"gates[{index}].result must be one of {sorted(ALLOWED_GATE_RESULTS)}")
        if not isinstance(row.get("reason"), str) or not row["reason"]:
            result.error(f"gates[{index}].reason must be a non-empty string")


def _validate_gate_dimension_coherence(
    data: dict[str, Any],
    result: Validation,
) -> None:
    gate_rows = data.get("gates")
    dimension_rows = data.get("research_dimensions")
    if not isinstance(gate_rows, list) or not isinstance(dimension_rows, list):
        return
    gate_results = {
        row.get("gate"): row.get("result")
        for row in gate_rows
        if isinstance(row, dict)
        and row.get("gate") in EXPECTED_GATES
        and row.get("result") in ALLOWED_GATE_RESULTS
    }
    dimension_statuses = {
        row.get("dimension"): row.get("status")
        for row in dimension_rows
        if isinstance(row, dict)
        and row.get("dimension") in RESEARCH_DIMENSION_GATES
        and row.get("status") in ALLOWED_DIMENSION_STATUSES
    }

    unresolved_dimensions = sorted(
        dimension
        for dimension, status in dimension_statuses.items()
        if status in {"unknown", "conflicting"}
    )
    for dimension in unresolved_dimensions:
        for gate in RESEARCH_DIMENSION_GATES[dimension]:
            gate_result = gate_results.get(gate)
            if gate_result in POSITIVE_GATE_RESULTS:
                result.error(
                    f"dimension {dimension!r} is "
                    f"{dimension_statuses[dimension]!r}, so gate {gate!r} "
                    f"cannot be {gate_result!r}"
                )

    for index, gate in enumerate(EXPECTED_GATES):
        gate_result = gate_results.get(gate)
        if gate_result not in HARD_BLOCK_GATE_RESULTS:
            continue
        for later_gate in EXPECTED_GATES[index + 1 :]:
            later_result = gate_results.get(later_gate)
            if later_result in POSITIVE_GATE_RESULTS:
                result.error(
                    f"gate {gate!r} is hard-blocked by {gate_result!r}; "
                    f"later gate {later_gate!r} cannot be {later_result!r}"
                )

    decision_result = gate_results.get("decision_and_disconfirming_evidence")
    if decision_result in READINESS_GATE_RESULTS and unresolved_dimensions:
        result.error(
            f"decision gate cannot be {decision_result!r} while dimensions "
            f"remain unknown/conflicting: {unresolved_dimensions}"
        )
    elif decision_result in POSITIVE_GATE_RESULTS and unresolved_dimensions:
        result.error(
            f"decision gate cannot be positive ({decision_result!r}) while "
            f"dimensions remain unknown/conflicting: {unresolved_dimensions}"
        )
    for gate, gate_result in gate_results.items():
        if gate_result in READINESS_GATE_RESULTS and (
            gate != "decision_and_disconfirming_evidence"
        ):
            result.error(
                f"readiness result {gate_result!r} is only valid for "
                "decision_and_disconfirming_evidence"
            )
    for gate, gate_result in gate_results.items():
        if gate_result == "outside_circle" and gate != "circle_of_competence":
            result.error(f"outside_circle is only valid for circle_of_competence, not {gate!r}")


def _validate_research_controls(data: dict[str, Any], result: Validation) -> None:
    moat = data.get("moat_evidence")
    if not isinstance(moat, dict):
        result.error("moat_evidence must be an object")
    else:
        for field in ("positive_evidence", "counter_evidence", "missing_tests"):
            if not isinstance(moat.get(field), list) or not moat[field]:
                result.error(f"moat_evidence.{field} must be a non-empty list")
    for field in ("red_team", "source_gaps", "invalidation_tests"):
        if not isinstance(data.get(field), list) or not data[field]:
            result.error(f"{field} must be a non-empty list")
    review = data.get("review")
    if not isinstance(review, dict) or "human_review_required" not in review:
        result.error("review.human_review_required is required")


def _validate_advice_language(data: dict[str, Any], result: Validation) -> None:
    serialized = json.dumps(data, ensure_ascii=False).lower()
    for phrase in PROHIBITED_PHRASES:
        if phrase.lower() in serialized:
            result.error(f"prohibited advice phrase found: {phrase!r}")
    disclaimer = data.get("disclaimer")
    if not isinstance(disclaimer, str) or "investment advice" not in disclaimer.lower():
        result.warning(
            "disclaimer should explicitly state that the artifact is not investment advice"
        )


def validate_company_research(data: dict[str, Any]) -> Validation:
    result = Validation()
    for field in REQUIRED_FIELDS:
        if field not in data:
            result.error(f"missing required top-level field: {field}")
    if data.get("schema_version") != SCHEMA_VERSION:
        result.error(f"schema_version must be {SCHEMA_VERSION}")
    if data.get("artifact_type") != "stock_fundamentals_valuation":
        result.error("artifact_type must be stock_fundamentals_valuation")
    generated_at = _parse_datetime(data.get("generated_at"), "generated_at", result)
    _validate_methodology_refs(data, result)
    _validate_sources(data, result)
    _validate_identity(data, result)
    research_date = _date_value(
        data.get("as_of", {}).get("research_date")
        if isinstance(data.get("as_of"), Mapping)
        else None
    )
    if (
        generated_at is not None
        and research_date is not None
        and generated_at.date() < research_date
    ):
        result.error("generated_at cannot be before as_of.research_date")
    _validate_financial_history(data, result)
    _validate_required_objects(data, result)
    _validate_research_dimensions(data, result)
    _validate_pe_matrix(data, result)
    _validate_owner_earnings(data, result)
    _validate_forward_scenarios(data, result)
    _validate_intrinsic_value(data, result)
    _validate_gates(data, result)
    _validate_gate_dimension_coherence(data, result)
    _validate_research_controls(data, result)
    _validate_advice_language(data, result)
    return result


def validation_summary(
    data: dict[str, Any],
    *,
    artifact_path: str | None = None,
) -> dict[str, Any]:
    result = validate_company_research(data)
    return {
        "valid": not result.errors,
        "artifact": artifact_path,
        "errors": result.errors,
        "warnings": result.warnings,
        "gate_count": len(data.get("gates", [])) if isinstance(data.get("gates"), list) else 0,
        "dimension_count": (
            len(data.get("research_dimensions", []))
            if isinstance(data.get("research_dimensions"), list)
            else 0
        ),
        "indicator_count": sum(
            len(row.get("indicators", []))
            for row in data.get("research_dimensions", [])
            if isinstance(row, dict) and isinstance(row.get("indicators"), list)
        )
        if isinstance(data.get("research_dimensions"), list)
        else 0,
        "source_count": (
            len(data.get("source_refs", [])) if isinstance(data.get("source_refs"), list) else 0
        ),
    }


# Backward-compatible name used by the skill's original validator tests.
validate = validate_company_research
