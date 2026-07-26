#!/usr/bin/env python3
"""Validate a combined Buffett–Munger company-research artifact."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import company_research_validation as core_validation  # noqa: E402

# Backward-compatible entry point used by existing tests and callers.
SCHEMA_VERSION = core_validation.SCHEMA_VERSION
ALLOWED_GATE_RESULTS = core_validation.ALLOWED_GATE_RESULTS
ALLOWED_FORWARD_SCENARIO_STATUSES = core_validation.ALLOWED_FORWARD_SCENARIO_STATUSES
ALLOWED_INDICATOR_STATUSES = core_validation.ALLOWED_INDICATOR_STATUSES
ALLOWED_INTRINSIC_VALUE_STATUSES = core_validation.ALLOWED_INTRINSIC_VALUE_STATUSES
ALLOWED_OWNER_EARNINGS_STATUSES = core_validation.ALLOWED_OWNER_EARNINGS_STATUSES
ALLOWED_PE_STATUSES = core_validation.ALLOWED_PE_STATUSES
EXPECTED_GATES = core_validation.EXPECTED_GATES
EXPECTED_RESEARCH_DIMENSIONS = core_validation.EXPECTED_RESEARCH_DIMENSIONS
METHODOLOGY_REFERENCE_CATALOG = core_validation.METHODOLOGY_REFERENCE_CATALOG
PRIMARY_METHODOLOGY_TIERS = core_validation.PRIMARY_METHODOLOGY_TIERS
RESEARCH_DIMENSION_GATES = core_validation.RESEARCH_DIMENSION_GATES
RESEARCH_DIMENSION_INDICATOR_IDS = core_validation.RESEARCH_DIMENSION_INDICATOR_IDS
PROHIBITED_PHRASES = core_validation.PROHIBITED_PHRASES
REQUIRED_FIELDS = core_validation.REQUIRED_FIELDS
Validation = core_validation.Validation
validate = core_validation.validate_company_research
validation_summary = core_validation.validation_summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path, help="Combined company-research JSON artifact")
    args = parser.parse_args()

    try:
        data = json.loads(args.artifact.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"valid": False, "errors": [str(exc)]}, ensure_ascii=False, indent=2))
        return 2
    if not isinstance(data, dict):
        print(
            json.dumps(
                {"valid": False, "errors": ["artifact root must be a JSON object"]},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 2

    output = core_validation.validation_summary(data, artifact_path=str(args.artifact))
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if output["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
