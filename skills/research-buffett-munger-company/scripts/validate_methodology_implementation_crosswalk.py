#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from company_research_validation import (  # noqa: E402
    ALLOWED_DIMENSION_STATUSES,
    ALLOWED_INDICATOR_STATUSES,
    EXPECTED_GATES,
    EXPECTED_RESEARCH_DIMENSIONS,
    RESEARCH_DIMENSION_GATES,
    RESEARCH_DIMENSION_INDICATOR_IDS,
    RESEARCH_DIMENSION_STAGE,
)
from company_research_validation import (  # noqa: E402
    SCHEMA_VERSION as COMPANY_SCHEMA_VERSION,
)

SCHEMA_VERSION = "seed.buffett-munger-methodology-implementation-crosswalk.v1"
LEDGER_SCHEMA_VERSION = "seed.buffett-munger-methodology-source-ledger.v1"
ORIGINS = {"primary_method", "mixed", "seed_operating_control"}
EVIDENCE_LAYERS = [
    "facts",
    "reported_claims",
    "interpretations",
    "assumptions",
    "source_gaps",
]
ROW_FIELDS = [
    "dimension",
    "status",
    "summary",
    "indicators",
    "source_refs",
    "positive_evidence",
    "counter_evidence",
    "source_gaps",
]
INDICATOR_FIELDS = [
    "id",
    "status",
    "summary",
    "source_refs",
    "source_gaps",
]


def _load_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: root must be a JSON object")
    return payload


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _skill_relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(SKILL_ROOT.resolve()))
    except ValueError:
        return str(path)


def _string_list(
    value: object,
    *,
    label: str,
    errors: list[str],
    minimum: int = 0,
) -> list[str]:
    if not isinstance(value, list):
        errors.append(f"{label} must be a list")
        return []
    rows = [item for item in value if isinstance(item, str) and item.strip()]
    if len(rows) != len(value):
        errors.append(f"{label} must contain only non-empty strings")
    if len(rows) < minimum:
        errors.append(f"{label} must contain at least {minimum} item(s)")
    if len(rows) != len(set(rows)):
        errors.append(f"{label} contains duplicate values")
    return rows


def validate_crosswalk(
    crosswalk: dict[str, Any],
    *,
    ledger: dict[str, Any],
    ledger_path: Path,
) -> list[str]:
    errors: list[str] = []
    if crosswalk.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    if crosswalk.get("artifact_type") != "buffett_munger_methodology_implementation_crosswalk":
        errors.append("artifact_type must be buffett_munger_methodology_implementation_crosswalk")
    try:
        generated_at = datetime.fromisoformat(
            str(crosswalk.get("generated_at") or "").replace("Z", "+00:00")
        )
        if generated_at.tzinfo is None:
            errors.append("generated_at must include a timezone")
    except ValueError:
        errors.append("generated_at must be an ISO-8601 timestamp")

    if ledger.get("schema_version") != LEDGER_SCHEMA_VERSION:
        errors.append(f"methodology ledger must use {LEDGER_SCHEMA_VERSION}")
    claim_rows = [row for row in ledger.get("method_claims") or [] if isinstance(row, dict)]
    claim_by_id = {str(row["id"]): row for row in claim_rows if isinstance(row.get("id"), str)}
    core_claim_ids = {
        claim_id for claim_id, row in claim_by_id.items() if row.get("method_role") == "core"
    }

    origin_definitions = crosswalk.get("origin_definitions")
    if not isinstance(origin_definitions, dict):
        errors.append("origin_definitions must be an object")
    else:
        if set(origin_definitions) != ORIGINS:
            errors.append(f"origin_definitions must define exactly {sorted(ORIGINS)}")
        for origin, definition in origin_definitions.items():
            if not isinstance(definition, str) or not definition.strip():
                errors.append(f"origin_definitions.{origin} must be a non-empty string")

    ledger_ref = crosswalk.get("methodology_ledger")
    if not isinstance(ledger_ref, dict):
        errors.append("methodology_ledger must be an object")
    else:
        expected_path = _skill_relative(ledger_path)
        if ledger_ref.get("path") != expected_path:
            errors.append(
                f"methodology_ledger.path must be {expected_path!r}, got {ledger_ref.get('path')!r}"
            )
        expected_sha = _sha256(ledger_path)
        if ledger_ref.get("sha256") != expected_sha:
            errors.append("methodology_ledger.sha256 does not match the current ledger")

    company_contract = crosswalk.get("company_contract")
    if not isinstance(company_contract, dict):
        errors.append("company_contract must be an object")
    else:
        if company_contract.get("schema_version") != COMPANY_SCHEMA_VERSION:
            errors.append(f"company_contract.schema_version must match {COMPANY_SCHEMA_VERSION}")
        if company_contract.get("implementation") != "scripts/company_research_validation.py":
            errors.append("company_contract.implementation must point to the v2 validator")
        if company_contract.get("dimension_count") != len(EXPECTED_RESEARCH_DIMENSIONS):
            errors.append("company_contract.dimension_count must match the v2 contract")

    shared_contract = crosswalk.get("shared_row_contract")
    if not isinstance(shared_contract, dict):
        errors.append("shared_row_contract must be an object")
    else:
        if shared_contract.get("required_company_artifact_fields") != ROW_FIELDS:
            errors.append(
                "shared_row_contract.required_company_artifact_fields "
                "must match the v2 row contract"
            )
        if set(shared_contract.get("applicability_statuses") or []) != set(
            ALLOWED_DIMENSION_STATUSES
        ):
            errors.append("shared_row_contract.applicability_statuses must match the v2 statuses")
        if shared_contract.get("evidence_layers") != EVIDENCE_LAYERS:
            errors.append("shared_row_contract.evidence_layers must match the evidence model")
        if shared_contract.get("indicator_fields") != INDICATOR_FIELDS:
            errors.append("shared_row_contract.indicator_fields must match the v2 indicator fields")
        if shared_contract.get("indicator_statuses") != sorted(ALLOWED_INDICATOR_STATUSES):
            errors.append(
                "shared_row_contract.indicator_statuses must match the v2 indicator statuses"
            )

    dimensions = [row for row in crosswalk.get("dimensions") or [] if isinstance(row, dict)]
    ids = [str(row.get("id") or "") for row in dimensions]
    if ids != EXPECTED_RESEARCH_DIMENSIONS:
        errors.append("dimensions must exactly match the ordered v2 research contract")
    if len(ids) != len(set(ids)):
        errors.append("dimensions contains duplicate ids")

    covered_gates: set[str] = set()
    direct_claim_ids: set[str] = set()
    context_claim_ids: set[str] = set()
    for index, row in enumerate(dimensions):
        dimension_id = str(row.get("id") or f"<missing-{index}>")
        label = f"dimensions[{index}]({dimension_id})"
        origin = row.get("origin")
        if origin not in ORIGINS:
            errors.append(f"{label}.origin must be one of {sorted(ORIGINS)}")
        expected_stage = RESEARCH_DIMENSION_STAGE.get(dimension_id)
        if row.get("stage") != expected_stage:
            errors.append(f"{label}.stage must be {expected_stage!r}, got {row.get('stage')!r}")
        if not isinstance(row.get("label_zh"), str) or not row["label_zh"].strip():
            errors.append(f"{label}.label_zh must be a non-empty string")
        if (
            not isinstance(row.get("attribution_boundary"), str)
            or not row["attribution_boundary"].strip()
        ):
            errors.append(f"{label}.attribution_boundary must be a non-empty string")
        gate_ids = _string_list(
            row.get("gate_ids"),
            label=f"{label}.gate_ids",
            errors=errors,
            minimum=1,
        )
        unknown_gates = set(gate_ids) - set(EXPECTED_GATES)
        if unknown_gates:
            errors.append(f"{label}.gate_ids has unknown gates {sorted(unknown_gates)}")
        expected_gate_ids = list(RESEARCH_DIMENSION_GATES.get(dimension_id, ()))
        if gate_ids != expected_gate_ids:
            errors.append(f"{label}.gate_ids must match the v2 gate mapping {expected_gate_ids!r}")
        covered_gates.update(gate_ids)
        required_indicator_ids = _string_list(
            row.get("required_indicator_ids"),
            label=f"{label}.required_indicator_ids",
            errors=errors,
            minimum=1,
        )
        expected_indicator_ids = list(RESEARCH_DIMENSION_INDICATOR_IDS.get(dimension_id, ()))
        if required_indicator_ids != expected_indicator_ids:
            errors.append(
                f"{label}.required_indicator_ids must match the v2 indicator "
                f"contract {expected_indicator_ids!r}"
            )

        method_claim_ids = _string_list(
            row.get("method_claim_ids"),
            label=f"{label}.method_claim_ids",
            errors=errors,
        )
        row_context_claim_ids = _string_list(
            row.get("context_claim_ids"),
            label=f"{label}.context_claim_ids",
            errors=errors,
        )
        unknown_claim_ids = (set(method_claim_ids) | set(row_context_claim_ids)) - set(claim_by_id)
        if unknown_claim_ids:
            errors.append(f"{label} references unknown method claims {sorted(unknown_claim_ids)}")
        overlap = set(method_claim_ids) & set(row_context_claim_ids)
        if overlap:
            errors.append(f"{label} repeats claims as direct and context: {sorted(overlap)}")
        if origin in {"primary_method", "mixed"} and not method_claim_ids:
            errors.append(f"{label}.method_claim_ids must not be empty for origin {origin}")
        if origin in {"primary_method", "mixed"} and not (set(method_claim_ids) & core_claim_ids):
            errors.append(
                f"{label}.method_claim_ids requires at least one core "
                f"primary-supported claim for origin {origin}"
            )
        if origin == "seed_operating_control":
            if method_claim_ids:
                errors.append(
                    f"{label} cannot directly attribute method claims when "
                    "origin is seed_operating_control"
                )
            if not row_context_claim_ids:
                errors.append(
                    f"{label}.context_claim_ids must explain which method "
                    "question the Seed control protects"
                )
        if origin in {"mixed", "seed_operating_control"}:
            rationale = row.get("seed_control_rationale")
            if not isinstance(rationale, str) or not rationale.strip():
                errors.append(f"{label}.seed_control_rationale is required for origin {origin}")
        _string_list(
            row.get("required_checks"),
            label=f"{label}.required_checks",
            errors=errors,
            minimum=2,
        )
        direct_claim_ids.update(method_claim_ids)
        context_claim_ids.update(row_context_claim_ids)

    uncovered_core = core_claim_ids - direct_claim_ids
    if uncovered_core:
        errors.append(
            f"core methodology claims lack direct implementation: {sorted(uncovered_core)}"
        )
    missing_gates = set(EXPECTED_GATES) - covered_gates
    if missing_gates:
        errors.append(f"methodology gates lack implementation: {sorted(missing_gates)}")

    origins = Counter(row.get("origin") for row in dimensions)
    stages = Counter(row.get("stage") for row in dimensions)
    summary = crosswalk.get("audit_summary")
    if not isinstance(summary, dict):
        errors.append("audit_summary must be an object")
    else:
        expected_summary = {
            "dimension_count": len(dimensions),
            "required_indicator_count": sum(
                len(RESEARCH_DIMENSION_INDICATOR_IDS.get(dimension_id, ()))
                for dimension_id in EXPECTED_RESEARCH_DIMENSIONS
            ),
            "origin_counts": {
                origin: origins.get(origin, 0)
                for origin in (
                    "primary_method",
                    "mixed",
                    "seed_operating_control",
                )
            },
            "stage_counts": {
                stage: stages.get(stage, 0)
                for stage in (
                    "fact_pack",
                    "company_research",
                    "red_team",
                    "valuation",
                )
            },
            "direct_method_claim_count": len(direct_claim_ids),
            "core_method_claim_count": len(core_claim_ids),
            "uncovered_core_method_claim_count": len(uncovered_core),
            "covered_gate_count": len(covered_gates & set(EXPECTED_GATES)),
            "github_method_authority_count": 0,
        }
        for key, expected in expected_summary.items():
            if summary.get(key) != expected:
                errors.append(f"audit_summary.{key} must be {expected!r}, got {summary.get(key)!r}")
    return errors


def main() -> int:
    skill_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(
        description=("Validate the Buffett-Munger methodology-to-company-contract crosswalk.")
    )
    parser.add_argument("crosswalk", type=Path)
    parser.add_argument(
        "--ledger",
        type=Path,
        default=skill_root / "references" / "methodology-source-ledger.json",
    )
    args = parser.parse_args()
    crosswalk = _load_object(args.crosswalk)
    ledger = _load_object(args.ledger)
    errors = validate_crosswalk(
        crosswalk,
        ledger=ledger,
        ledger_path=args.ledger,
    )
    result = {
        "valid": not errors,
        "crosswalk": str(args.crosswalk),
        "ledger": str(args.ledger),
        "dimension_count": len(crosswalk.get("dimensions") or []),
        "required_indicator_count": sum(
            len(row.get("required_indicator_ids") or [])
            for row in crosswalk.get("dimensions") or []
            if isinstance(row, dict)
        ),
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
