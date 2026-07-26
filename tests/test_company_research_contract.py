from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = (
    ROOT / "skills" / "research-buffett-munger-company" / "scripts" / "validate_company_research.py"
)


def _load_validator() -> ModuleType:
    spec = importlib.util.spec_from_file_location("validate_company_research", VALIDATOR_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VALIDATOR = _load_validator()


def _research_dimensions() -> list[dict]:
    return [
        {
            "dimension": dimension,
            "status": "applicable",
            "summary": f"Evidence-backed test coverage for {dimension}.",
            "indicators": [
                {
                    "id": indicator_id,
                    "status": "observed",
                    "summary": f"Observed evidence for {indicator_id}.",
                    "source_refs": ["annual-report"],
                    "source_gaps": [],
                }
                for indicator_id in VALIDATOR.RESEARCH_DIMENSION_INDICATOR_IDS[dimension]
            ],
            "source_refs": ["annual-report"],
            "positive_evidence": ["Primary filing evidence."],
            "counter_evidence": [],
            "source_gaps": [],
        }
        for dimension in VALIDATOR.EXPECTED_RESEARCH_DIMENSIONS
    ]


def _set_dimension_unknown(row: dict, *, gap: str) -> None:
    row["status"] = "unknown"
    row["source_gaps"] = [gap]
    indicator = row["indicators"][0]
    indicator.update(
        {
            "status": "not_disclosed",
            "summary": gap,
            "source_refs": [],
            "source_gaps": [gap],
        }
    )


def _set_dimension_conflicting(row: dict, *, gap: str) -> None:
    row["status"] = "conflicting"
    row["source_gaps"] = [gap]
    indicator = row["indicators"][0]
    indicator.update(
        {
            "status": "conflicting",
            "summary": gap,
            "source_gaps": [gap],
        }
    )


def _artifact() -> dict:
    gates = [
        {
            "gate": gate,
            "result": "pass",
            "reason": "Evidence-backed calibration result.",
        }
        for gate in VALIDATOR.EXPECTED_GATES
    ]
    return {
        "schema_version": VALIDATOR.SCHEMA_VERSION,
        "artifact_type": "stock_fundamentals_valuation",
        "artifact_role": "synthetic_example",
        "status": "needs_human_review",
        "generated_at": "2026-07-26T12:00:00+08:00",
        "security": {
            "security_id": "CN-SSE-000001",
            "company_name": "Synthetic Example Company",
            "ticker": "EXAMPLE",
            "exchange": "TEST",
            "listing_type": "synthetic_security",
            "currency": "CNY",
            "fiscal_year_end": "12-31",
            "reporting_standard": "PRC_ASBE",
        },
        "as_of": {
            "research_date": "2026-07-26",
            "price": 10.0,
            "price_date": "2026-07-25",
            "price_source_ref": "price-source",
        },
        "methodology_refs": [
            {
                "id": "berkshire_1996_letter",
                "title": "1996 Chairman's Letter",
                "url": "https://www.berkshirehathaway.com/letters/1996.html",
                "use": "Circle-of-competence and predictability gate.",
            }
        ],
        "source_refs": [
            {
                "id": "annual-report",
                "tier": "A",
                "source_type": "exchange_filing",
                "title": "Annual report",
                "url": "https://example.com/annual-report.pdf",
                "published_at_status": "known",
                "published_at": "2026-03-20",
                "accessed_at": "2026-07-26",
                "period": "FY2025",
                "audit_status": "audited",
                "scope": "consolidated_group",
                "covers": ["financial_statements", "business", "governance"],
                "content_sha256": "a" * 64,
            },
            {
                "id": "price-source",
                "tier": "C",
                "source_type": "market_data",
                "title": "Price source",
                "url": "https://example.com/price-source",
                "published_at_status": "known",
                "published_at": "2026-07-25",
                "accessed_at": "2026-07-26",
                "period": "2026-07-25",
                "audit_status": "not_applicable",
                "scope": "listed_security",
                "covers": ["price"],
                "content_sha256": "b" * 64,
            },
        ],
        "source_boundaries": {"facts": "Primary filing facts."},
        "ownership_structure": {"controller": "Test controller"},
        "financial_history": {
            "periods": [
                {"period": "FY2023"},
                {"period": "FY2024"},
                {"period": "FY2025"},
            ]
        },
        "segment_data": {"status": "applicable", "segments": ["Test segment"]},
        "research_dimensions": _research_dimensions(),
        "earnings_quality_bridge": {"reported_parent_net_income": 1.0},
        "capital_allocation": {"status": "reviewed", "uses": ["reinvestment"]},
        "balance_sheet_quality": {"status": "reviewed", "net_debt": 0.0},
        "owner_earnings": {
            "status": "calculated",
            "currency": "CNY",
            "range": [
                {"case": "low", "value": 0.8, "formula": "earnings - reinvestment"},
                {"case": "high", "value": 1.0, "formula": "earnings - maintenance"},
            ],
            "limitations": ["Maintenance capex is estimated."],
        },
        "pe_matrix": [
            {
                "label": "reported_fy",
                "status": "calculated",
                "price": 10.0,
                "currency": "CNY",
                "price_as_of": "2026-07-25",
                "eps": 1.0,
                "eps_period": "FY2025",
                "eps_type": "reported_diluted",
                "formula": "10 / 1",
                "pe": 10.0,
                "confidence": "high",
            },
            {
                "label": "reported_ttm",
                "status": "calculated",
                "price": 10.0,
                "currency": "CNY",
                "price_as_of": "2026-07-25",
                "eps": 1.0,
                "eps_period": "TTM",
                "eps_type": "reported_diluted",
                "formula": "10 / 1",
                "pe": 10.0,
                "confidence": "high",
            },
        ],
        "forward_scenarios": {
            "currency": "CNY",
            "price_anchor": 10.0,
            "scenarios": [
                {
                    "scenario": "bear",
                    "status": "calculated_pe",
                    "forecast_eps": 0.8,
                    "implied_pe_at_current_price": 12.5,
                },
                {
                    "scenario": "base",
                    "status": "calculated_pe",
                    "forecast_eps": 1.0,
                    "implied_pe_at_current_price": 10.0,
                },
                {
                    "scenario": "upside",
                    "status": "calculated_pe",
                    "forecast_eps": 1.25,
                    "implied_pe_at_current_price": 8.0,
                },
            ],
        },
        "intrinsic_value_scenarios": {
            "currency": "CNY",
            "scenarios": [
                {
                    "scenario": "conservative",
                    "status": "calculated",
                    "discount_rate_pct": 10.0,
                    "terminal_growth_pct": 1.0,
                    "intrinsic_value_per_share": 7.0,
                },
                {
                    "scenario": "base",
                    "status": "calculated",
                    "discount_rate_pct": 9.0,
                    "terminal_growth_pct": 2.0,
                    "intrinsic_value_per_share": 10.0,
                },
                {
                    "scenario": "high",
                    "status": "calculated",
                    "discount_rate_pct": 8.0,
                    "terminal_growth_pct": 2.5,
                    "intrinsic_value_per_share": 13.0,
                },
            ],
        },
        "moat_evidence": {
            "positive_evidence": ["High returns with primary-source support."],
            "counter_evidence": ["Returns may regress."],
            "missing_tests": ["Independent customer evidence."],
        },
        "red_team": [{"risk": "Demand"}],
        "gates": gates,
        "historical_valuation": {"status": "limited_history"},
        "price_move_attribution": {"status": "not_causal"},
        "source_gaps": [{"gap": "Maintenance capex"}],
        "invalidation_tests": [{"test": "Margin durability"}],
        "review": {"human_review_required": True},
        "disclaimer": "Research support only; not investment advice.",
    }


def test_valid_company_research_contract_passes() -> None:
    artifact = _artifact()
    result = VALIDATOR.validate(artifact)
    assert result.errors == []
    summary = VALIDATOR.validation_summary(artifact)
    assert summary["dimension_count"] == 25
    assert summary["indicator_count"] == 50


def test_pe_mismatch_and_gate_order_fail_validation() -> None:
    artifact = _artifact()
    artifact["pe_matrix"][0]["pe"] = 7.0
    artifact["gates"] = list(reversed(artifact["gates"]))

    result = VALIDATOR.validate(artifact)

    assert any("does not reproduce" in error for error in result.errors)
    assert any("ordered contract" in error for error in result.errors)


def test_dangling_sources_and_advice_language_fail_validation() -> None:
    artifact = _artifact()
    artifact["earnings_quality_bridge"]["source_refs"] = ["missing-source"]
    artifact["review"]["note"] = "建议买入"

    result = VALIDATOR.validate(artifact)

    assert any("dangling source_refs" in error for error in result.errors)
    assert any("prohibited advice phrase" in error for error in result.errors)


def test_company_sources_require_reproducible_provenance_fields() -> None:
    artifact = _artifact()
    source = artifact["source_refs"][0]
    source.pop("content_sha256")
    source["covers"] = []
    source["audit_status"] = "looks_audited"
    source["url"] = "http://example.com/unverified-copy"

    result = VALIDATOR.validate(artifact)

    assert any("content_sha256 must be a lowercase SHA-256" in error for error in result.errors)
    assert any(".covers must be a non-empty list" in error for error in result.errors)
    assert any(".audit_status must be one of" in error for error in result.errors)
    assert any(".url must be an HTTPS URL" in error for error in result.errors)


def test_undated_source_requires_explicit_status_and_reason() -> None:
    artifact = _artifact()
    source = artifact["source_refs"][0]
    source.update(
        {
            "published_at_status": "not_disclosed",
            "published_at": None,
            "date_reason": "The official page does not state a publication date.",
        }
    )

    valid_result = VALIDATOR.validate(artifact)

    assert valid_result.errors == []

    source.pop("date_reason")
    missing_reason_result = VALIDATOR.validate(artifact)

    assert any(
        ".date_reason must be a non-empty string" in error for error in missing_reason_result.errors
    )


def test_source_and_price_dates_cannot_use_future_information() -> None:
    artifact = _artifact()
    artifact["source_refs"][0]["published_at"] = "2026-07-27"
    artifact["source_refs"][0]["accessed_at"] = "2026-07-27"
    artifact["as_of"]["price_date"] = "2026-07-27"
    artifact["generated_at"] = "2026-07-25T12:00:00+08:00"

    result = VALIDATOR.validate(artifact)

    assert any(
        ".published_at cannot be after as_of.research_date" in error for error in result.errors
    )
    assert any(
        ".accessed_at cannot be after as_of.research_date" in error for error in result.errors
    )
    assert any(
        "as_of.price_date cannot be after as_of.research_date" in error for error in result.errors
    )
    assert any(
        "generated_at cannot be before as_of.research_date" in error for error in result.errors
    )


def test_unknown_audit_status_requires_reason() -> None:
    artifact = _artifact()
    artifact["source_refs"][0]["audit_status"] = "unknown"

    result = VALIDATOR.validate(artifact)

    assert any(".audit_reason must be a non-empty string" in error for error in result.errors)


def test_price_anchor_requires_a_resolved_price_source() -> None:
    artifact = _artifact()
    artifact["as_of"]["price_source_ref"] = "annual-report"

    wrong_coverage_result = VALIDATOR.validate(artifact)

    assert any(
        "price_source_ref must reference a source whose covers include 'price'" in error
        for error in wrong_coverage_result.errors
    )

    artifact["as_of"]["price_source_ref"] = "missing-price-source"
    missing_result = VALIDATOR.validate(artifact)

    assert any(
        "as_of.price_source_ref must resolve to source_refs" in error
        for error in missing_result.errors
    )


def test_security_reporting_standard_is_required() -> None:
    artifact = _artifact()
    artifact["security"].pop("reporting_standard")

    result = VALIDATOR.validate(artifact)

    assert any(
        "security.reporting_standard must be a non-empty string" in error for error in result.errors
    )


def test_methodology_reference_is_required_and_must_use_https() -> None:
    artifact = _artifact()
    artifact["methodology_refs"] = []

    empty_result = VALIDATOR.validate(artifact)

    assert any(
        "methodology_refs must be a non-empty list" in error for error in empty_result.errors
    )

    artifact = _artifact()
    artifact["methodology_refs"][0]["url"] = "http://example.com/method"

    insecure_result = VALIDATOR.validate(artifact)

    assert any("must be an HTTPS URL" in error for error in insecure_result.errors)


def test_methodology_reference_must_match_audited_catalog() -> None:
    artifact = _artifact()
    artifact["methodology_refs"][0].update(
        {
            "id": "invented_buffett_rule",
            "title": "Invented Buffett rule",
            "url": "https://example.com/invented-method",
        }
    )

    unknown_result = VALIDATOR.validate(artifact)

    assert any(
        "is not in the audited methodology source catalog" in error
        for error in unknown_result.errors
    )

    artifact = _artifact()
    artifact["methodology_refs"][0]["title"] = "Paraphrased title that hides source drift"
    artifact["methodology_refs"][0]["url"] = "https://example.com/real-looking-copy"

    drift_result = VALIDATOR.validate(artifact)

    assert any("title must exactly match" in error for error in drift_result.errors)
    assert any("url must exactly match" in error for error in drift_result.errors)


def test_supplemental_transcript_chain_cannot_be_the_only_method_authority() -> None:
    artifact = _artifact()
    source_id = "munger_1995_misjudgment_transcript"
    catalog_row = VALIDATOR.METHODOLOGY_REFERENCE_CATALOG[source_id]
    artifact["methodology_refs"] = [
        {
            "id": source_id,
            "title": catalog_row["title"],
            "url": catalog_row["url"],
            "use": "Bias checklist as a supplemental transcript chain.",
        }
    ]

    result = VALIDATOR.validate(artifact)

    assert any("requires at least one audited tier A/A- source" in error for error in result.errors)


def test_research_dimensions_cover_operating_and_governance_contract() -> None:
    required = {
        "revenue_structure",
        "industry_chain_position",
        "customers",
        "suppliers",
        "competition_structure",
        "management",
        "governance_and_related_parties",
        "accounting_and_audit",
        "valuation",
        "disconfirming_evidence",
    }

    assert required <= set(VALIDATOR.EXPECTED_RESEARCH_DIMENSIONS)
    assert len(VALIDATOR.EXPECTED_RESEARCH_DIMENSIONS) == 25
    assert list(VALIDATOR.RESEARCH_DIMENSION_INDICATOR_IDS) == (
        VALIDATOR.EXPECTED_RESEARCH_DIMENSIONS
    )
    assert sum(len(ids) for ids in VALIDATOR.RESEARCH_DIMENSION_INDICATOR_IDS.values()) == 50


def test_missing_or_reordered_research_dimension_fails_validation() -> None:
    artifact = _artifact()
    artifact["research_dimensions"] = list(reversed(artifact["research_dimensions"][:-1]))

    result = VALIDATOR.validate(artifact)

    assert any("ordered contract" in error for error in result.errors)


def test_applicable_dimension_requires_indicators_sources_and_evidence() -> None:
    artifact = _artifact()
    row = artifact["research_dimensions"][0]
    row["indicators"] = []
    row["source_refs"] = []
    row["positive_evidence"] = []

    result = VALIDATOR.validate(artifact)

    assert any(".indicators must not be empty when applicable" in error for error in result.errors)
    assert any(".source_refs must not be empty when applicable" in error for error in result.errors)
    assert any(
        ".positive_evidence must not be empty when applicable" in error for error in result.errors
    )


def test_dimension_indicators_must_match_ordered_check_family_contract() -> None:
    artifact = _artifact()
    row = next(item for item in artifact["research_dimensions"] if item["dimension"] == "customers")
    row["indicators"] = list(reversed(row["indicators"][:-1]))

    result = VALIDATOR.validate(artifact)

    assert any(
        ".indicators must exactly match the ordered contract" in error for error in result.errors
    )


def test_observed_indicator_requires_direct_source_binding() -> None:
    artifact = _artifact()
    row = artifact["research_dimensions"][0]
    row["indicators"][0]["source_refs"] = []
    row["indicators"][1]["source_refs"] = ["unlisted-source"]

    result = VALIDATOR.validate(artifact)

    assert any(".source_refs must not be empty when observed" in error for error in result.errors)
    assert any(
        ".source_refs must be included in research_dimensions[0].source_refs" in error
        for error in result.errors
    )


def test_methodology_reference_cannot_substitute_for_company_evidence() -> None:
    artifact = _artifact()
    row = artifact["research_dimensions"][0]
    methodology_id = artifact["methodology_refs"][0]["id"]
    row["source_refs"] = [methodology_id]
    for indicator in row["indicators"]:
        indicator["source_refs"] = [methodology_id]

    result = VALIDATOR.validate(artifact)

    assert any(f"dangling source_refs: {methodology_id}" in error for error in result.errors)


def test_not_disclosed_indicator_forces_unknown_dimension_status() -> None:
    artifact = _artifact()
    row = artifact["research_dimensions"][0]
    indicator = row["indicators"][0]
    indicator.update(
        {
            "status": "not_disclosed",
            "summary": "Exact security rights were not disclosed.",
            "source_refs": [],
            "source_gaps": ["Exact security rights remain unavailable."],
        }
    )

    result = VALIDATOR.validate(artifact)

    assert any(
        ".status cannot be applicable while a required indicator is not_disclosed" in error
        for error in result.errors
    )


def test_unknown_dimension_requires_explicit_source_gap() -> None:
    artifact = _artifact()
    row = artifact["research_dimensions"][6]
    _set_dimension_unknown(row, gap="Independent customer evidence is missing.")
    row["source_gaps"] = []

    result = VALIDATOR.validate(artifact)

    assert any(
        ".source_gaps must not be empty when status is unknown" in error for error in result.errors
    )


def test_hkd_company_uses_currency_neutral_valuation_fields() -> None:
    artifact = _artifact()
    artifact["security"]["security_id"] = "XHKG:00001"
    artifact["security"]["ticker"] = "00001"
    artifact["security"]["exchange"] = "HKEX"
    artifact["security"]["listing_type"] = "ordinary_hk_share"
    artifact["security"]["currency"] = "HKD"
    artifact["security"]["reporting_standard"] = "HKFRS"
    artifact["owner_earnings"]["currency"] = "HKD"
    artifact["forward_scenarios"]["currency"] = "HKD"
    artifact["intrinsic_value_scenarios"]["currency"] = "HKD"
    for row in artifact["pe_matrix"]:
        row["currency"] = "HKD"

    result = VALIDATOR.validate(artifact)

    assert result.errors == []


def test_loss_making_hkd_company_preserves_negative_economics_without_fake_pe() -> None:
    artifact = _artifact()
    artifact["security"].update(
        {
            "security_id": "XHKG:09999",
            "ticker": "09999",
            "exchange": "HKEX",
            "listing_type": "ordinary_hk_share",
            "currency": "HKD",
            "reporting_standard": "HKFRS",
        }
    )
    artifact["owner_earnings"].update(
        {
            "currency": "HKD",
            "range": [
                {"case": "low", "value": -2.0, "formula": "loss - maintenance"},
                {"case": "high", "value": -0.5, "formula": "loss - minimum upkeep"},
            ],
        }
    )
    for row in artifact["pe_matrix"]:
        row.update(
            {
                "status": "not_meaningful",
                "currency": "HKD",
                "eps": -1.0,
                "pe": None,
                "reason": "Reported EPS is non-positive, so PE has no economic meaning.",
            }
        )
        row.pop("formula")
    artifact["forward_scenarios"]["currency"] = "HKD"
    for index, row in enumerate(artifact["forward_scenarios"]["scenarios"], start=1):
        row.update(
            {
                "status": "loss_case",
                "forecast_eps": -0.25 * index,
                "implied_pe_at_current_price": None,
                "reason": "Scenario EPS remains non-positive.",
            }
        )
    artifact["intrinsic_value_scenarios"]["currency"] = "HKD"
    artifact["intrinsic_value_scenarios"]["scenarios"][0].update(
        {
            "status": "non_positive_equity_value",
            "intrinsic_value_per_share": -1.0,
            "reason": "Conservative cash-flow value is exhausted by net obligations.",
        }
    )
    for gate in artifact["gates"]:
        if gate["gate"] in {
            "owner_earnings",
            "intrinsic_value_and_margin_of_safety",
        }:
            gate["result"] = "mixed"
    artifact["gates"][-1]["result"] = "provisional"

    result = VALIDATOR.validate(artifact)

    assert result.errors == []


def test_unavailable_calculations_require_explicit_states_and_reasons() -> None:
    artifact = _artifact()
    artifact["owner_earnings"].update(
        {
            "status": "unavailable",
            "range": [],
            "reason": "Maintenance reinvestment cannot be separated from growth capex.",
        }
    )
    artifact["pe_matrix"][1].update(
        {
            "status": "unavailable",
            "eps": None,
            "pe": None,
            "reason": "Comparable TTM diluted EPS is unavailable.",
        }
    )
    artifact["pe_matrix"][1].pop("formula")
    artifact["forward_scenarios"]["scenarios"][1].update(
        {
            "status": "unavailable",
            "forecast_eps": None,
            "implied_pe_at_current_price": None,
            "reason": "Segment disclosure does not support a base EPS estimate.",
        }
    )
    artifact["intrinsic_value_scenarios"]["scenarios"][2].update(
        {
            "status": "unavailable",
            "discount_rate_pct": None,
            "terminal_growth_pct": None,
            "intrinsic_value_per_share": None,
            "reason": "No defensible terminal assumptions are available.",
        }
    )

    result = VALIDATOR.validate(artifact)

    assert result.errors == []


def test_pe_status_rejects_sign_and_value_mismatches() -> None:
    artifact = _artifact()
    artifact["pe_matrix"][0]["eps"] = -1.0
    artifact["pe_matrix"][1].update(
        {
            "status": "not_meaningful",
            "pe": None,
            "reason": "Claimed loss case.",
        }
    )

    result = VALIDATOR.validate(artifact)

    assert any("eps must be positive when status is calculated" in error for error in result.errors)
    assert any(
        "eps must be non-positive when status is not_meaningful" in error for error in result.errors
    )


def test_loss_and_unavailable_states_reject_synthetic_values_or_missing_reason() -> None:
    artifact = _artifact()
    artifact["forward_scenarios"]["scenarios"][0].update(
        {
            "status": "loss_case",
            "forecast_eps": -0.5,
            "reason": "Loss case.",
        }
    )
    artifact["pe_matrix"][1].update(
        {
            "status": "unavailable",
            "eps": None,
            "pe": None,
        }
    )
    artifact["pe_matrix"][1].pop("formula")

    result = VALIDATOR.validate(artifact)

    assert any(
        "implied_pe_at_current_price must be null when loss_case" in error
        for error in result.errors
    )
    assert any("pe_matrix[1].reason must be a non-empty string" in error for error in result.errors)


def test_intrinsic_value_status_rejects_positive_value_labeled_non_positive() -> None:
    artifact = _artifact()
    artifact["intrinsic_value_scenarios"]["scenarios"][0].update(
        {
            "status": "non_positive_equity_value",
            "reason": "Contradictory test label.",
        }
    )

    result = VALIDATOR.validate(artifact)

    assert any("intrinsic_value_per_share must be non-positive" in error for error in result.errors)


def test_valuation_currency_must_match_security_currency() -> None:
    artifact = _artifact()
    artifact["forward_scenarios"]["currency"] = "HKD"

    result = VALIDATOR.validate(artifact)

    assert any(
        "forward_scenarios.currency='HKD' must match security.currency='CNY'" in error
        for error in result.errors
    )


def test_unknown_dimension_blocks_positive_mapped_gates() -> None:
    artifact = _artifact()
    customer_row = next(
        row for row in artifact["research_dimensions"] if row["dimension"] == "customers"
    )
    _set_dimension_unknown(
        customer_row,
        gap="Independent customer evidence is missing.",
    )

    result = VALIDATOR.validate(artifact)

    for gate in (
        "circle_of_competence",
        "business_economics",
        "durable_moat",
    ):
        assert any(
            "dimension 'customers' is 'unknown'" in error
            and f"gate '{gate}' cannot be 'pass'" in error
            for error in result.errors
        )


def test_unresolved_dimension_allows_non_positive_gate_results() -> None:
    artifact = _artifact()
    customer_row = next(
        row for row in artifact["research_dimensions"] if row["dimension"] == "customers"
    )
    _set_dimension_unknown(
        customer_row,
        gap="Independent customer evidence is missing.",
    )
    mapped_gates = set(VALIDATOR.RESEARCH_DIMENSION_GATES["customers"])
    for gate in artifact["gates"]:
        if gate["gate"] in mapped_gates:
            gate["result"] = "provisional"
    artifact["gates"][-1]["result"] = "provisional"

    result = VALIDATOR.validate(artifact)

    assert result.errors == []


def test_unresolved_dimension_blocks_positive_final_decision_gate() -> None:
    artifact = _artifact()
    customer_row = next(
        row for row in artifact["research_dimensions"] if row["dimension"] == "customers"
    )
    _set_dimension_unknown(
        customer_row,
        gap="Independent customer evidence is missing.",
    )
    for gate in artifact["gates"]:
        if gate["gate"] in VALIDATOR.RESEARCH_DIMENSION_GATES["customers"]:
            gate["result"] = "provisional"

    result = VALIDATOR.validate(artifact)

    assert any(
        "decision gate cannot be positive ('pass')" in error and "customers" in error
        for error in result.errors
    )


def test_hard_blocked_gate_prevents_later_positive_gate_results() -> None:
    artifact = _artifact()
    artifact["gates"][0]["result"] = "blocked"

    result = VALIDATOR.validate(artifact)

    assert any(
        "gate 'identity_and_source_integrity' is hard-blocked by 'blocked'" in error
        and "later gate 'circle_of_competence' cannot be 'pass'" in error
        for error in result.errors
    )


def test_readiness_result_rejects_unresolved_dimensions() -> None:
    artifact = _artifact()
    tax_row = next(
        row for row in artifact["research_dimensions"] if row["dimension"] == "tax_and_legal"
    )
    _set_dimension_conflicting(
        tax_row,
        gap="Tax exposure remains conflicting.",
    )
    survival_gate = next(
        row for row in artifact["gates"] if row["gate"] == "survival_and_balance_sheet"
    )
    survival_gate["result"] = "inconclusive"
    artifact["gates"][-1]["result"] = "research_ready"

    result = VALIDATOR.validate(artifact)

    assert any(
        "decision gate cannot be 'research_ready'" in error and "tax_and_legal" in error
        for error in result.errors
    )


def test_readiness_and_outside_circle_results_are_gate_specific() -> None:
    artifact = _artifact()
    artifact["gates"][0]["result"] = "research_ready"
    artifact["gates"][2]["result"] = "outside_circle"

    result = VALIDATOR.validate(artifact)

    assert any(
        "readiness result 'research_ready' is only valid" in error for error in result.errors
    )
    assert any(
        "outside_circle is only valid for circle_of_competence" in error for error in result.errors
    )


def test_unknown_gate_result_fails_validation() -> None:
    artifact = _artifact()
    artifact["gates"][0]["result"] = "looks_good"

    result = VALIDATOR.validate(artifact)

    assert any("gates[0].result must be one of" in error for error in result.errors)
