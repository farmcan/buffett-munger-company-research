from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = (
    ROOT
    / "skills"
    / "research-buffett-munger-company"
    / "scripts"
    / "validate_report_template_parity.py"
)
REPORTS = (
    "horizon-robotics-09660-hk",
    "meitu-01357-hk",
    "nanhua-futures-02691-hk",
    "smic-00981-hk",
    "fubo-group-03738-hk",
)


def test_all_public_reports_use_the_fixed_reader_contract() -> None:
    for slug in REPORTS:
        report = ROOT / "docs" / slug / "report.html"
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), str(report)],
            check=False,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stdout or result.stderr
        payload = json.loads(result.stdout)
        assert payload["valid"] is True
        assert payload["template_version"] == "company-research-publication-v1"
        assert payload["contract_counts"] == {
            "required_dimensions": 25,
            "visible_dimension_results": 25,
            "required_indicator_ids": 50,
            "visible_indicator_ids": 50,
            "required_gate_ids": 9,
            "visible_gate_ids": 9,
        }
        assert payload["missing_fragment_targets"] == []
