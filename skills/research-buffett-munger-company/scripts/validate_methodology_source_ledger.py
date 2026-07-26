#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from company_research_validation import (  # noqa: E402
    METHODOLOGY_REFERENCE_CATALOG,
)

SCHEMA_VERSION = "seed.buffett-munger-methodology-source-ledger.v1"
PRIMARY_TIERS = {"A", "A-"}
SUPPLEMENTAL_TIERS = {"B"}
ENGINEERING_TIER = "C"
GIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def _load_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: root must be a JSON object")
    return payload


def _valid_https_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def _duplicate_ids(items: list[dict[str, Any]]) -> set[str]:
    ids = [str(item.get("id") or "") for item in items]
    return {item_id for item_id in ids if ids.count(item_id) > 1}


def validate_ledger(
    ledger: dict[str, Any],
    *,
    methodology_document: str | None = None,
) -> list[str]:
    errors: list[str] = []
    if ledger.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    if ledger.get("artifact_type") != "buffett_munger_methodology_source_ledger":
        errors.append("artifact_type must be buffett_munger_methodology_source_ledger")
    try:
        snapshot_at = datetime.fromisoformat(
            str(ledger.get("snapshot_at") or "").replace("Z", "+00:00")
        )
        if snapshot_at.tzinfo is None:
            errors.append("snapshot_at must include a timezone")
    except ValueError:
        errors.append("snapshot_at must be an ISO-8601 timestamp")

    official_sources = [
        item for item in ledger.get("official_sources") or [] if isinstance(item, dict)
    ]
    claims = [item for item in ledger.get("method_claims") or [] if isinstance(item, dict)]
    engineering_sources = [
        item for item in ledger.get("engineering_sources") or [] if isinstance(item, dict)
    ]
    if not official_sources:
        errors.append("official_sources must not be empty")
    if not claims:
        errors.append("method_claims must not be empty")
    if not engineering_sources:
        errors.append("engineering_sources must not be empty")

    for label, items in (
        ("official_sources", official_sources),
        ("method_claims", claims),
        ("engineering_sources", engineering_sources),
    ):
        duplicates = _duplicate_ids(items)
        if duplicates:
            errors.append(f"{label} has duplicate ids: {sorted(duplicates)}")
        missing = [index for index, item in enumerate(items) if not item.get("id")]
        if missing:
            errors.append(f"{label} has missing ids at indexes: {missing}")

    source_by_id = {str(source["id"]): source for source in official_sources if source.get("id")}
    catalog_ids = set(METHODOLOGY_REFERENCE_CATALOG)
    ledger_source_ids = set(source_by_id)
    if ledger_source_ids != catalog_ids:
        errors.append(
            "official_sources must exactly match the executable methodology catalog; "
            f"missing={sorted(catalog_ids - ledger_source_ids)}, "
            f"unexpected={sorted(ledger_source_ids - catalog_ids)}"
        )
    for source_id in sorted(ledger_source_ids & catalog_ids):
        source = source_by_id[source_id]
        catalog_source = METHODOLOGY_REFERENCE_CATALOG[source_id]
        for field in ("title", "url", "tier"):
            if source.get(field) != catalog_source[field]:
                errors.append(f"{source_id}: {field} must match the executable methodology catalog")
    claim_by_id = {str(claim["id"]): claim for claim in claims if claim.get("id")}
    for source_id, source in source_by_id.items():
        tier = source.get("tier")
        if tier not in PRIMARY_TIERS | SUPPLEMENTAL_TIERS:
            errors.append(f"{source_id}: invalid source tier {tier!r}")
        if not _valid_https_url(source.get("url")):
            errors.append(f"{source_id}: url must be a valid HTTPS URL")
        status = source.get("http_status")
        if not isinstance(status, int) or not 100 <= status <= 599:
            errors.append(f"{source_id}: http_status must be an HTTP status integer")
        if not source.get("allowed_use") or not source.get("rights_boundary"):
            errors.append(f"{source_id}: allowed_use and rights_boundary are required")
        for claim_id in source.get("claim_ids") or []:
            if claim_id not in claim_by_id:
                errors.append(f"{source_id}: unknown claim_id {claim_id!r}")
            elif source_id not in (claim_by_id[claim_id].get("source_ids") or []):
                errors.append(f"{source_id}: claim {claim_id} does not backlink to the source")

    valid_gate_names = {
        "identity_and_source_integrity",
        "circle_of_competence",
        "business_economics",
        "durable_moat",
        "management_and_capital_allocation",
        "owner_earnings",
        "survival_and_balance_sheet",
        "intrinsic_value_and_margin_of_safety",
        "decision_and_disconfirming_evidence",
    }
    for claim_id, claim in claim_by_id.items():
        role = claim.get("method_role")
        if role not in {"core", "supplemental"}:
            errors.append(f"{claim_id}: method_role must be core or supplemental")
        source_ids = claim.get("source_ids") or []
        if not source_ids:
            errors.append(f"{claim_id}: source_ids must not be empty")
            continue
        missing_source_ids = [
            source_id for source_id in source_ids if source_id not in source_by_id
        ]
        if missing_source_ids:
            errors.append(f"{claim_id}: unknown source_ids {sorted(missing_source_ids)}")
            continue
        source_tiers = {source_by_id[source_id].get("tier") for source_id in source_ids}
        if role == "core" and not source_tiers.intersection(PRIMARY_TIERS):
            errors.append(f"{claim_id}: core claim requires at least one A/A- source")
        if role == "supplemental" and not source_tiers.issubset(PRIMARY_TIERS | SUPPLEMENTAL_TIERS):
            errors.append(f"{claim_id}: supplemental claim has an invalid source tier")
        unknown_gates = set(claim.get("gate_mappings") or []) - valid_gate_names
        if unknown_gates:
            errors.append(f"{claim_id}: unknown gates {sorted(unknown_gates)}")
        for source_id in source_ids:
            if claim_id not in (source_by_id[source_id].get("claim_ids") or []):
                errors.append(f"{claim_id}: source {source_id} does not backlink to the claim")

    for engineering in engineering_sources:
        engineering_id = str(engineering.get("id") or "<missing>")
        if engineering.get("tier") != ENGINEERING_TIER:
            errors.append(f"{engineering_id}: engineering source tier must be C")
        if engineering.get("method_authority") is not False:
            errors.append(f"{engineering_id}: method_authority must be false")
        if not _valid_https_url(engineering.get("url")):
            errors.append(f"{engineering_id}: url must be a valid HTTPS URL")
        if not isinstance(engineering.get("stars"), int) or engineering["stars"] < 0:
            errors.append(f"{engineering_id}: stars must be a non-negative integer")
        if not GIT_SHA_RE.fullmatch(str(engineering.get("head_sha") or "")):
            errors.append(f"{engineering_id}: head_sha must be a 40-char git SHA")
        if not engineering.get("license_spdx"):
            errors.append(f"{engineering_id}: license_spdx is required")
        if not engineering.get("adopt_patterns"):
            errors.append(f"{engineering_id}: adopt_patterns must not be empty")
        if not engineering.get("reject_patterns"):
            errors.append(f"{engineering_id}: reject_patterns must not be empty")
        if "no_code_copied" not in str(engineering.get("code_reuse_status") or ""):
            errors.append(f"{engineering_id}: code_reuse_status must explicitly say no_code_copied")

    summary = ledger.get("audit_summary")
    if not isinstance(summary, dict):
        errors.append("audit_summary must be an object")
    else:
        expected_summary = {
            "official_source_count": len(official_sources),
            "core_claim_count": sum(claim.get("method_role") == "core" for claim in claims),
            "supplemental_claim_count": sum(
                claim.get("method_role") == "supplemental" for claim in claims
            ),
            "engineering_source_count": len(engineering_sources),
            "github_method_authority_count": sum(
                engineering.get("method_authority") is True for engineering in engineering_sources
            ),
            "copied_code_source_count": sum(
                "no_code_copied" not in str(engineering.get("code_reuse_status") or "")
                for engineering in engineering_sources
            ),
        }
        for key, expected in expected_summary.items():
            if summary.get(key) != expected:
                errors.append(f"audit_summary.{key} must be {expected}, got {summary.get(key)!r}")

    if methodology_document is not None:
        for source in official_sources:
            if str(source["url"]) not in methodology_document:
                errors.append(
                    f"methodology document is missing official source URL {source['url']}"
                )
        for engineering in engineering_sources:
            if str(engineering["url"]) not in methodology_document:
                errors.append(
                    f"methodology document is missing engineering source URL {engineering['url']}"
                )
            stars = f"| {engineering['stars']:,} |"
            if stars not in methodology_document:
                errors.append(
                    f"methodology document is missing star snapshot {stars} "
                    f"for {engineering['repository']}"
                )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate the Buffett-Munger methodology source ledger."
    )
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--document", type=Path)
    args = parser.parse_args()
    ledger = _load_object(args.ledger)
    document = args.document.read_text(encoding="utf-8") if args.document is not None else None
    errors = validate_ledger(ledger, methodology_document=document)
    result = {
        "valid": not errors,
        "ledger": str(args.ledger),
        "document": str(args.document) if args.document else None,
        "official_sources": len(ledger.get("official_sources") or []),
        "method_claims": len(ledger.get("method_claims") or []),
        "engineering_sources": len(ledger.get("engineering_sources") or []),
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
